class NameParser():
    def __init__(self, input_files: tuple):
        self.input_files = input_files

    def __determine_delim(self) -> str:
        self.delim = None
        if '-' in self.input_files[0]:
            self.delim = '-'
        if '_' in self.input_files[0]:
            self.delim = '_'

    def __fields(self) -> list:
        self.__determine_delim()
        return(self.input_files[0].split(self.delim))

    def __positions(self):
        pass

