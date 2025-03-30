from re import search, fullmatch

class Validate:
    ESCAPE_CHAR = r'\\|/|:|\*|\?|"|<|>|\|'
    # %P = value of the entry if the edit is allowed

    def __init__(self) -> None:
        pass

    def separatorValidate(self, user_input: str) -> bool:
        if len(user_input) < 2 and not bool(search(self.ESCAPE_CHAR, user_input)):
            return True
        return False
    
    def is_valid_int(self, s) -> bool:
        if not fullmatch(r'^-?(0|([1-9]\d*))$', s):
            return False
        if s.startswith('-'):
            num_part = s[1:]
        else:
            num_part = s
        if num_part == '0':
            return True
        if all(c == '0' for c in num_part):
            return False
        return True

    def intValidate(self, user_input: str) -> bool:
        if self.is_valid_int(user_input):
            return True
        return False
    
    def floatValidate(self, user_input: str) -> bool:
        if all(c in '0123456789' for c in user_input):
            return True
        return False
    
    def strValidate(self, user_input: str) -> bool:
        if not bool(search(self.ESCAPE_CHAR, user_input)):
            return True
        return False
    
    def folderValidate(self, user_input: str) -> bool:
        if not bool(search(self.ESCAPE_CHAR[7:], user_input)):
            return True
        return False
    
