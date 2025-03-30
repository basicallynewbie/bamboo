from src.start import Start
from src.importjson import importJson
from argparse import ArgumentParser


class Bamboo:
    def __init__(self) -> None:
        self.config = {"language": "english", "font": "TkTextFont", "size": 15}

    def updateConfig(self, jsonfile: str = "config.json", encode: str = "utf-8-sig") -> None:
        importJson(jsonfile, self.config, encode)
        if not isinstance(self.config["size"], int):
            try:
                self.config.update({"size": int(self.config["size"])})
            except:
                self.config.update({"size": 10})

    def cli(self) -> None:
        parser = ArgumentParser(prog="bamboo")
        parser.add_argument(
            "-j",
            "--jsonfile",
            type=str,
            help="The path of your jsonfile",
            required=False,
            default="config.json",
        )
        parser.add_argument(
            "-e",
            "--encode",
            type=str,
            help="The encode of your jsonfile",
            required=False,
            default="utf-8-sig",
        )
        args = parser.parse_args()
        self.updateConfig(jsonfile=args.jsonfile, encode=args.encode)
        Start(self.config).loop()

    def __call__(self) -> None:
        self.cli()

if __name__ == '__main__':
    Bamboo()()
