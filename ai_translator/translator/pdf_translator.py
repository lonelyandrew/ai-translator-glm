from pathlib import Path
from typing import Optional

from loguru import logger

from ai_translator.book.book import Book
from ai_translator.llm.llm_base import LLMBase
from ai_translator.translator.pdf_parser import PDFParser
from ai_translator.translator.writer import Writer


class PDFTranslator:
    def __init__(self, model: LLMBase):
        self.model: LLMBase = model
        self.writer: Writer = Writer()
        self.book: Optional[Book] = None

    def translate_pdf(
        self,
        pdf_file_path: str,
        target_language: Optional[str] = None,
        output_file_path: Optional[str] = None,
        page_count: Optional[int] = None,
    ) -> None:
        """翻译PDF文件。

        Args:
            pdf_file_path: PDF文件路径。
            target_language: 目标语言。
            output_file_path: 输出文件路径。
            page_count: 翻译页数。
        """
        if not target_language:
            target_language = "中文"
        self.book = PDFParser.parse_pdf(pdf_file_path, page_count)

        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                logger.debug(content.content_type)
                prompt: str = self.model.translate_prompt(content, target_language)
                logger.debug(prompt)
                translation: str
                status: bool
                translation, status = self.model.make_request(prompt)
                logger.info(translation)
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        self.writer.save_translated_book(self.book, Path(output_file_path))
