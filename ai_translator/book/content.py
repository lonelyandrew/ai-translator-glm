import json
from typing import Any, Optional

import pandas as pd
from enum import Enum, auto

from loguru import logger
from pandas import DataFrame
from PIL import Image as PILImage


class ContentType(Enum):
    """内容类型枚举。"""

    TEXT = auto()  # 文本
    TABLE = auto()  # 表格
    IMAGE = auto()  # 图片


class Content:
    """内容数据。"""

    def __init__(self, content_type: ContentType, original: Any, translation: Optional[str] = None):
        """初始化内容数据。

        Args:
            content_type: 内容类型。
            original: 原始内容。
            translation: 翻译结果。
        """
        self.content_type: ContentType = content_type
        self.original: Any = original
        self.translation: Any = translation
        self.status: bool = False

    def set_translation(self, translation: str, status: bool) -> None:
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def __str__(self) -> str:
        return str(self.original)

    def check_translation_type(self, translation):
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation, PILImage.Image):
            return True
        return False


class TableContent(Content):
    def __init__(self, data: list[list[str]]) -> None:
        df: DataFrame = pd.DataFrame(data[1:], columns=data[0])
        # Verify if the number of rows and columns in the data and DataFrame object match
        if len(data) - 1 != len(df) or len(data[0]) != len(df.columns):
            raise ValueError(
                "The number of rows and columns in the extracted table data and DataFrame object do not match."
            )

        super().__init__(ContentType.TABLE, df)

    def set_translation(self, translation: str, status: bool) -> None:
        try:
            if not isinstance(translation, str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

            if translation.startswith("```json"):
                translation = translation.strip()
                translation = translation[len("```json"):]
                translation = translation[:-len("```")]
                logger.debug(translation)
            translation_df = DataFrame(json.loads(translation))
            logger.debug(translation_df)
            self.translation = translation_df
            self.status = status
        except Exception as e:
            logger.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False

    def __str__(self):
        return json.dumps(self.original.to_dict(orient="records"), ensure_ascii=False)

    def iter_items(self, translated=False):
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, item in enumerate(row):
                yield row_idx, col_idx, item

    def update_item(self, row_idx, col_idx, new_value, translated=False):
        target_df: DataFrame = self.translation if translated else self.original
        target_df.at[row_idx, col_idx] = new_value
