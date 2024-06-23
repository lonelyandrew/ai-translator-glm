import base64
from pathlib import Path

import streamlit as st
from loguru import logger
from pandas import DataFrame
from streamlit.runtime.uploaded_file_manager import UploadedFile

from ai_translator.book.book import Book
from ai_translator.book.content import ContentType
from ai_translator.llm.glm_model import GLMModel
from ai_translator.translator.pdf_parser import PDFParser
from ai_translator.translator.writer import Writer
from config import Config
from logger import init_logger


def get_file_downloader_html(file_path: Path, btn_text: str) -> None:
    """生成用于下载文件的 HTML 代码"""
    with open(file_path, "rb") as f:
        file_content = f.read()

    # 创建下载链接
    st.markdown(
        f"""
           <a href="data:application/octet-stream;base64,{base64.b64encode(file_content).decode()}"
           download="{file_path.name}">
           {btn_text}
           </a>
        """,
        unsafe_allow_html=True,
    )


init_logger("ai_translator.log", rotation="02:00")

config: Config = Config()
supported_llm_versions: list[str] = [
    "GLM-3-Turbo",
    "GLM-4",
]

# 设置页面标题和描述
st.set_page_config(page_title="AI Translator")
st.title("PDF 翻译工具")
st.write("上传 PDF 文件并选择目标语言进行翻译")

# 选择目标语言
llm_model_version: str = st.selectbox("选择使用模型版本", supported_llm_versions)
model: GLMModel = GLMModel(config.api_key)

# 上传文件
uploaded_file: UploadedFile = st.file_uploader("上传 PDF 文件", type=["pdf"])

# 选择源语言
source_language: str = st.selectbox("选择源语言", ["英语", "法语", "德语", "西班牙语", "日语", "韩语", "粤语", "汉语"])

# 选择目标语言
target_language: str = st.selectbox(
    "选择目标语言", ["汉语", "法语", "德语", "西班牙语", "日语", "韩语", "粤语", "英语"]
)


if uploaded_file is not None:
    # 显示上传的文件名
    st.write("已上传文件:", uploaded_file.name)

    if st.button("开始翻译"):
        if source_language == target_language:
            st.error("源语言与目标语言不得相同")
            st.stop()
        with st.spinner(text="翻译中..."):
            with open(f"data/upload/{uploaded_file.name}", "wb+") as temp_pdf_file:
                temp_pdf_file.write(uploaded_file.read())
                book: Book = PDFParser.parse_pdf(temp_pdf_file.name)

            # 通过调用翻译函数翻译 PDF 文件
            for page_idx, page in enumerate(book.pages):
                for content_idx, content in enumerate(page.contents):
                    logger.debug(content.content_type)
                    prompt: str = model.translate_prompt(content, source_language, target_language)
                    logger.debug(prompt)
                    translation: str
                    status: bool
                    translation, status = model.make_request(prompt, llm_model_version)
                    logger.info(translation)
                    book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        # 显示翻译结果
        st.subheader("翻译结果:")

        with st.container(border=True):
            for page in book.pages:
                for content in page.contents:
                    if content.status:
                        if content.content_type == ContentType.TEXT:
                            text: str = content.translation
                            for frag in text.split("\n"):
                                st.write(frag)
                        elif content.content_type == ContentType.TABLE:
                            table: DataFrame = content.translation
                            st.dataframe(table, hide_index=True)
                if page != book.pages[-1]:
                    st.divider()

        download_file_path: Path = Writer.save_translated_book_pdf(book)
        get_file_downloader_html(download_file_path, "下载为PDF文件")
        download_file_path: Path = Writer.save_translated_book_markdown(book)
        get_file_downloader_html(download_file_path, "下载为md文件")
