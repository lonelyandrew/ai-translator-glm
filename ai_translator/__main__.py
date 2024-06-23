from config import Config, GLMConfig, OpenAIConfig
from ai_translator.llm.glm_model import GLMModel
from ai_translator.llm.openai_model import OpenAIModel
from ai_translator.translator.pdf_translator import PDFTranslator
from ai_translator.utils.argument_parser import ArgumentParser
from logger import init_logger


if __name__ == "__main__":
    init_logger("ai_translator.log", rotation="02:00")
    config: Config = Config()
    if config.llm_type == "OpenAIModel":
        openai_config: OpenAIConfig = config.openai
        model: OpenAIModel = OpenAIModel(openai_config.model, openai_config.api_key, str(openai_config.base_url))
    elif config.llm_type == "GLMModel":
        glm_config: GLMConfig = config.glm
        model: GLMModel = GLMModel(glm_config.base_url, glm_config.time_out)
    else:
        raise ValueError(f"未知模型类型: {config.llm_type}")
    translator: PDFTranslator = PDFTranslator(model)

    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    translator.translate_pdf(pdf_file_path=args.book, output_file_path=args.output, target_language=args.target_lang)
