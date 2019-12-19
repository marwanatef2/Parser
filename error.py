class TinyLanguageSyntaxError(Exception):
    pass

class ExpectingIdentifier(TinyLanguageSyntaxError):
    pass

class ExpectingThen(TinyLanguageSyntaxError):
    pass

class ExpectingEnd(TinyLanguageSyntaxError):
    pass

class ExpectingUntil(TinyLanguageSyntaxError):
    pass

class ExpectingAssign(TinyLanguageSyntaxError):
    pass

class ExpectingNumorId(TinyLanguageSyntaxError):
    pass

class ExpectingRightBracket(TinyLanguageSyntaxError):
    pass