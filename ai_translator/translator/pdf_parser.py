from pathlib import Path
from typing import Optional

import pdfplumber
import streamlit as st
from pdfplumber.page import Page as PdfPage
from loguru import logger

from ai_translator.book.book import Book
from ai_translator.book.content import Content, ContentType, TableContent
from ai_translator.book.page import Page
from ai_translator.translator.exceptions import PageOutOfRangeException


class PDFParser:

    @classmethod
    @st.cache_data
    def parse_pdf(cls, pdf_file_path: str, page_count: Optional[int] = None) -> Book:
        """解析PDF文件内容。

        Args:
            pdf_file_path: PDF文件路径。
            page_count: 解析页面数量。

        Returns:
            返回一个Book对象。
        """
        book: Book = Book(Path(pdf_file_path))

        with pdfplumber.open(pdf_file_path) as pdf:
            if page_count is not None and page_count > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), page_count)

            pages_to_parse: list[PdfPage] = pdf.pages[:page_count] if page_count else pdf.pages

            for pdf_page in pages_to_parse:
                page: Page = Page()

                # Store the original text content
                raw_text: str = pdf_page.extract_text()
                tables: list[list[list[Optional[str]]]] = pdf_page.extract_tables()

                # Remove each cell's content from the original text
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines: list[str] = raw_text.splitlines()
                    cleaned_raw_text_lines: list[str] = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text: str = "\n".join(cleaned_raw_text_lines)

                    text_content: Content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.add_content(text_content)
                    logger.debug(f"[raw_text]\n {cleaned_raw_text}")

                # Handling tables
                if tables:
                    for table in tables:
                        table_content: TableContent = TableContent(table)
                        page.add_content(table_content)
                        logger.debug(f"[table]\n{table_content.original}")
                book.add_page(page)
        return book
