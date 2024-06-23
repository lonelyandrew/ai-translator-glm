from pathlib import Path

from ai_translator.book.page import Page


class Book:
    """书籍信息。"""

    def __init__(self, pdf_file_path: Path):
        """初始化书籍。

        Args:
            pdf_file_path: Pdf文件路径。
        """
        if not pdf_file_path.exists():
            raise FileNotFoundError(f"PDF文件不存在: {pdf_file_path}")
        self.pdf_file_path: Path = pdf_file_path
        self.pages: list[Page] = []

    def add_page(self, page: Page) -> None:
        """添加分页内容。

        Args:
            page: 单页数据。
        """
        self.pages.append(page)
