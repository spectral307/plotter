from .entry import Entry


class Parser:
    def parse_file(self, file: str) -> list[Entry]:
        raise NotImplementedError()

    def parse_files(self, files: list[str]) -> list[Entry]:
        raise NotImplementedError()
