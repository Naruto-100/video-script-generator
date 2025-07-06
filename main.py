import streamlit as st
from matplotlib.pyplot import title
from openai import api_key

from utils import generate_script

st.title("🎥 视频脚本一键生成")

with st.sidebar:
    api_key = st.text_input("🔑 请输入你的OpenAI API密钥：", type="password")
    st.write("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

subject = st.text_input("✍️ 请输入你的视频主题：")

video_length = st.number_input("⏱️ 请输入你的视频预期时长（单位：分钟）：",
                               value=0.5,
                               min_value=0.1,
                               max_value=100.0,
                               step=0.1)

creativity = st.slider("✨ 请设置脚本生成的创造性数值（数值越低越有逻辑性，数值越高越有随机性）：",
                       value=0.50,
                       min_value=0.01,
                       max_value=1.00,
                       step=0.01)

submit = st.button("🪄 生成脚本")

if submit and not api_key:
    st.info("😶‍🌫️ 请输入你的OpenAI API密钥！")
    st.stop()
if submit and not subject:
    st.info("😶‍🌫️ 请输入你的视频主题！")
    st.stop()
if submit and not video_length:
    st.info("😶‍🌫️ 请输入你的视频时长！")
    st.stop()
if submit and not creativity:
    st.info("😶‍🌫️ 请设置脚本创造性数值！")
    st.stop()

if submit:
    with st.spinner("🛠️ 正在思考中，请稍等..."):
        script, title, search_result = generate_script(subject, video_length, creativity, api_key)
    st.write("🎆 生成完毕！")
    st.subheader("🎞️ 视频标题：")
    st.write(title)
    st.subheader("📋 视频脚本：")
    st.write(script)
    with st.expander("🔍 维基百科搜索结果："):
        st.info(search_result)