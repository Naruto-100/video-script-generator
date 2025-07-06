from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper


def generate_script(subject, video_length, creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """
             你是一个短视频频道的博主。根据以下标题和相关信息，为短视频写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本长度尽量遵循视频时长要求。
             要求开头抓住眼球，中间提供干活，结尾有惊喜，脚本格式请按照【开头、中间、结尾】分隔。
             整体内容表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出来的的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```
             """)
        ]
    )

    model = ChatOpenAI(
        model = "gpt-3.5-turbo",
        openai_api_key = api_key,
        openai_api_base = "https://api.aigc369.com/v1",
        temperature = creativity
    )

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    script = script_chain.invoke(
        {
            "title": title,
            "duration": video_length,
            "wikipedia_search": search_result
        }
    ).content

    return script, title, search_result