from ai_translator.book.content import Content


class Page:
    """书籍单页数据。"""

    def __init__(self):
        """初始化一个空白的单页。"""
        self.contents: list[Content] = []

    def add_content(self, content: Content) -> None:
        """添加页面内容。

        Args:
            content: 页面内容。
        """
        self.contents.append(content)
