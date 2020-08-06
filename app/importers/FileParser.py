import operator


TARGET_COLUMN = "7_2009"


class FileParser:

    def __init__(self, file):
        self.file = file
        self.file_data = None
        self.header = None
        self.columns = None
        self.exit = False
        self.line_length = None
        self.separator = None
        self.target_idx = None
        self.errors = []
        self.output = None

    def run(self):
        self.read_file()
        if self.exit:
            return
        self.set_header()
        self.set_separator()
        self.set_columns()
        self.set_target_col_idx()
        if self.exit:
            return
        self.parse_file()

    def read_file(self):
        data = self.file.read().decode(encoding="utf-8", errors="ignore")
        self.exit = True
        if data:
            self.file_data = data.splitlines()
        if self.file_data:
            self.exit = False
        else:
            self.errors.append(f"Can't parse file or no data in file")

    def set_header(self):
        self.header = self.file_data[0]

    def set_target_col_idx(self):
        try:
            self.target_idx = self.columns.index(TARGET_COLUMN)
        except ValueError:
            self.exit = True
            self.errors.append(f"Column {TARGET_COLUMN} not found in data file")

    def set_separator(self):
        self.separator = '\t'  # default
        if self.header and isinstance(self.header, str):
            sep_lengs = {}
            possible_separators = [',', ';', '|', '\t']
            for sep in possible_separators:
                sep_lengs[sep] = len(self.header.split(sep))
            separator = max(sep_lengs.items(), key=operator.itemgetter(1))[0]
            self.separator = separator

    def set_columns(self):
        self.columns = self.file_data[0].split(self.separator)
        self.line_length = len(self.columns)

    def parse_file(self):
        output = []
        for row in self.file_data[1:]:
            _line = row.split(self.separator)
            curr_len = len(_line)
            if curr_len != self.line_length:
                self.errors.append(f"Line: {row} has wrong length, skipping")
                continue
            output_row = {
                "data": _line[self.target_idx].strip()
            }
            output.append(output_row)
        self.output = output

    def get_parsed_data(self):
        return self.output
