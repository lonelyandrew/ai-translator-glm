class PageOutOfRangeException(Exception):
    def __init__(self, book_page_count: int, requested_page_num: int):
        self.book_page_count: int = book_page_count
        self.requested_page_num: int = requested_page_num
        super().__init__(
            f"Page out of range: Book has {book_page_count} pages, but {requested_page_num} pages were requested."
        )
