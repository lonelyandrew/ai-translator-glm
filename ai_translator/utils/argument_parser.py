import argparse


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Translate English PDF book to Chinese.")
        self.parser.add_argument("--book", type=str, help="PDF file to translate.")
        self.parser.add_argument("--target_lang", type=str, help="Target language.", default="中文")
        self.parser.add_argument(
            "--output",
            type=str,
            help="The file format of translated book. Now supporting PDF and Markdown",
        )

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args
