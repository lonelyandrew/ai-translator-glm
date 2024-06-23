from pathlib import Path
from typing import Optional

from loguru import logger
from pandas import DataFrame
from reportlab.lib import colors, pagesizes
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Table, TableStyle

from ai_translator.book.book import Book
from ai_translator.book.content import ContentType


class Writer:

    @classmethod
    def save_translated_book(cls, book: Book, output_file_path: Optional[Path] = None) -> None:
        """保存翻译结果。

        Args:
            book: 书籍对象。
            output_file_path: 输出文件路径。
        """
        if output_file_path:
            file_format: str = output_file_path.suffix.lower()
        else:
            file_format = ".pdf"

        if file_format == ".pdf":
            cls.save_translated_book_pdf(book, output_file_path)
        elif file_format == ".md":
            cls.save_translated_book_markdown(book, output_file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")

    @classmethod
    def save_translated_book_pdf(cls, book: Book, output_file_path: Optional[Path] = None) -> Path:
        """将翻译结果保存为PDF文件。

        Args:
            book: 书籍对象。
            output_file_path: 保存文档路径。

        Returns:
            返回文件保存路径。
        """
        if not output_file_path:
            output_file_path = book.pdf_file_path.parent / f"{book.pdf_file_path.stem}_translated.pdf"

        logger.info(f"pdf_file_path: {book.pdf_file_path}")
        logger.info(f"开始翻译: {output_file_path}")

        font_path: str = "fonts/simsun.ttc"  # 请将此路径替换为您的字体文件路径
        pdfmetrics.registerFont(TTFont("SimSun", font_path))

        # Create a new ParagraphStyle with the SimSun font
        simsun_style: ParagraphStyle = ParagraphStyle("SimSun", fontName="SimSun", fontSize=12, leading=14)

        # Create a PDF document
        doc: SimpleDocTemplate = SimpleDocTemplate(str(output_file_path), pagesize=pagesizes.letter)
        story: list[Flowable] = []

        # Iterate over the pages and contents
        for page in book.pages:
            for content in page.contents:
                if content.status:
                    if content.content_type == ContentType.TEXT:
                        # Add translated text to the PDF
                        text: str = content.translation
                        for frag in text.split("\n"):
                            para: Paragraph = Paragraph(frag, simsun_style)
                            story.append(para)
                    elif content.content_type == ContentType.TABLE:
                        # Add table to the PDF
                        table: DataFrame = content.translation
                        table_style: TableStyle = TableStyle(
                            [
                                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                ("FONTNAME", (0, 0), (-1, 0), "SimSun"),  # 更改表头字体为 "SimSun"
                                ("FONTSIZE", (0, 0), (-1, 0), 14),
                                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                                ("FONTNAME", (0, 1), (-1, -1), "SimSun"),  # 更改表格中的字体为 "SimSun"
                                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                            ]
                        )
                        pdf_table: Table = Table([table.columns] + table.values.tolist())
                        pdf_table.setStyle(table_style)
                        story.append(pdf_table)
            # Add a page break after each page except the last one
            if page != book.pages[-1]:
                story.append(PageBreak())

        # Save the translated book as a new PDF file
        doc.build(story)
        logger.info(f"翻译完成: {output_file_path}")
        return output_file_path

    @classmethod
    def save_translated_book_markdown(cls, book: Book, output_file_path: str = None) -> Path:
        if output_file_path is None:
            output_file_path = book.pdf_file_path.parent / f"{book.pdf_file_path.stem}_translated.md"

        logger.info(f"pdf_file_path: {book.pdf_file_path}")
        logger.info(f"开始翻译: {output_file_path}")
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            # Iterate over the pages and contents
            for page in book.pages:
                for content in page.contents:
                    if content.status:
                        if content.content_type == ContentType.TEXT:
                            # Add translated text to the Markdown file
                            text: str = content.translation
                            for frag in text.split("\n"):
                                output_file.write(frag + "\n\n")

                        elif content.content_type == ContentType.TABLE:
                            # Add table to the Markdown file
                            table = content.translation
                            header = "| " + " | ".join(str(column) for column in table.columns) + " |" + "\n"
                            separator = "| " + " | ".join(["---"] * len(table.columns)) + " |" + "\n"
                            # body = '\n'.join(['| ' + ' | '.join(row) + ' |' for row in table.values.tolist()]) + '\n\n'
                            body = (
                                "\n".join(
                                    [
                                        "| " + " | ".join(str(cell) for cell in row) + " |"
                                        for row in table.values.tolist()
                                    ]
                                )
                                + "\n\n"
                            )
                            output_file.write(header + separator + body)

                # Add a page break (horizontal rule) after each page except the last one
                if page != book.pages[-1]:
                    output_file.write("---\n\n")

        logger.info(f"翻译完成: {output_file_path}")
        return output_file_path
