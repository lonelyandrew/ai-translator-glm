from abc import ABC

from ai_translator.book.content import Content, ContentType


class LLMBase(ABC):
    """LLM翻译模型基类。"""

    @classmethod
    def make_text_prompt(cls, text: str, source_language: str, target_language: str) -> str:
        """生成文本翻译Prompt。

        Args:
            text: 待翻译文本。
            source_language: 源语言。
            target_language: 目标语言。

        Returns:
            返回生成好的Prompt字符串。
        """
        return f"""
            请将下面的{source_language}文本翻译为{target_language}，只返回翻译结果，待翻译文本以```包裹，翻译结果不需要用```包裹：
            
            ```{text}```
        """

    @classmethod
    def make_table_prompt(cls, table: str, source_language: str, target_language: str) -> str:
        """生成表格翻译的Prompt。

        Args:
            table: 待翻译表格字符串。
            source_language: 源语言。
            target_language: 目标语言。

        Returns:
            返回生成好的Prompt字符串。
        """
        return f"""
            请将{source_language}表格翻译为{target_language}，待翻译的表格以```包裹，待翻译内容为JSON格式，翻译结果以纯JSON格式返回，只返回翻译结果JSON字符串，翻译结果不需要用```包裹，
            例如 [{{"key1": "value1", ...}}]
            
            ```{table}```
        """

    @classmethod
    def translate_prompt(cls, content: Content, source_language: str, target_language: str) -> str:
        """根据内容类型，自动生成对应的内容翻译Prompt。

        Args:
            content: 内容对象。
            source_language: 翻译源语言。
            target_language: 翻译目标语言。

        Returns:
            返回生成好的Prompt字符串。
        """
        if content.content_type == ContentType.TEXT:
            return cls.make_text_prompt(str(content), source_language, target_language)
        elif content.content_type == ContentType.TABLE:
            return cls.make_table_prompt(str(content), source_language, target_language)
        raise ValueError(f"不支持的内容格式: {content.content_type}")

    def make_request(self, prompt: str, model_name: str) -> tuple[str, bool]:
        """发送翻译请求。

        Args:
            prompt: Prompt文本。
            model_name: 模型版本名称。

        Returns:
            返回(翻译结果, 是否成功响应)。
        """
        raise NotImplementedError("子类必须实现 make_request 方法")
