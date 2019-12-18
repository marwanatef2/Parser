class Token:
    def __init__(self, val, typo):
        self.value=val
        self.type=typo


availableTokens = {':=' : "ASSIGN", ';' : "SEMICOLON" , '<' : "LESSTHAN" , '=' : "EQUAL" ,
 '+' : "PLUS" , '-' : "MINUS" , '*' : "MULT" , '/' : "DIV" , '(' : "OPENBRACKET" ,
  ')' : "CLOSEDBRACKET",'if':"IF", 'then':"THEN",
  'else':"ELSE",'end':"END",'read':"READ",'write':"WRITE",'repeat':"REPEAT", 'until':"UNTIL"}

