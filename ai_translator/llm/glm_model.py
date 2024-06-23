from zhipuai import ZhipuAI
from zhipuai.types.chat.chat_completion import Completion

from ai_translator.llm.llm_base import LLMBase


class GLMModel(LLMBase):
    """GLM模型。"""

    def __init__(self, api_key: str) -> None:
        """模型初始化。

        Args:
            api_key: API密钥。
        """
        self.api_key: str = api_key
        self.client: ZhipuAI = ZhipuAI(api_key=self.api_key)

    def make_request(self, prompt: str, model_name: str) -> tuple[str, bool]:
        try:
            response: Completion = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )
            translation: str = response.choices[0].message.content
            return translation, True
        except Exception as e:
            raise Exception(f"发生了未知错误：{e}")
