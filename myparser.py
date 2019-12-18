from mytoken import Token, availableTokens

class Parser:
    def __init__(self, tokenslist):
        self.tokenslist = tokenslist
        self.currentToken = None
        self.index = -1
        self.statements = list()

    def error(self, error_msg):
        print("Error! " + error_msg)

    def advance(self):
        self.index+=1
        if self.index >= len(self.tokenslist):
            self.currentToken = Token("", "")
        else:
            self.currentToken = self.tokenslist[self.index]
        print("advance: " + self.currentToken.value)

    def disadvance(self):
        self.index-=1
        self.currentToken = self.tokenslist[self.index]
        print("disadvance: " + self.currentToken.value)


    def match(self, token1, token2=None):
        if self.currentToken.type == availableTokens[token1]:
            # self.advance()
            return token1
        elif token2 != None and self.currentToken.type == availableTokens[token2]:
            # self.advance()
            return token2
        else:
            self.error("Expecting '" + token1  + "'")
            return "error"

    def parse(self):
        while self.index < len(self.tokenslist) :
            stmt_sq = self.stmt_sequence()
            self.statements.append(stmt_sq)
        return self.statements

    def stmt_sequence(self):
        statement = self.statement()
        # self.advance()
        while (self.match(";") != "error"):
            operator = self.match(";")
            # self.advance()
            statement +=  " " + operator + " " + self.statement()
            # self.advance()
        return statement

    def statement(self):
        self.advance()
        if self.currentToken.type == "READ":
            return self.read_stmt()
        elif self.currentToken.type == "WRITE":
            return self.write_stmt()
        elif self.currentToken.type == "IF":
            return self.if_stmt()
        elif self.currentToken.type == "REPEAT":
            return self.repeat_stmt()
        elif self.currentToken.type== "IDENTIFIER":
            return self.assign_stmt()

    def read_stmt(self):
        self.advance()
        if self.currentToken.type == "IDENTIFIER":
            instruction = "read " + self.currentToken.value
            self.advance()
            return instruction

    def write_stmt(self):
        self.advance()
        instruction = "write " + self.expression()
        return instruction
  

    def if_stmt(self):
        self.advance()
        instruction = "if " + self.expression()
        operator = self.match("then")
        instruction += " " + operator + " "
        stmt_sq = self.stmt_sequence()
        instruction += stmt_sq + " "
        # operator = self.match("end")
        # self.advance()
        # instruction += operator 
        operator = self.match("end", "else")
        if operator == "end":
            self.advance()
            instruction += operator
        elif operator == "else":
            instruction += "else "
            stmt_sq = self.stmt_sequence()
            operator = self.match("end")
            self.advance()
            instruction += stmt_sq + " " + operator
        return instruction

    def repeat_stmt(self):    
        instruction = "repeat " + self.stmt_sequence() + " "
        operator = self.match("until")
        self.advance()
        instruction += operator + " " + self.expression()
        return instruction

    def assign_stmt(self):
        identifier = self.currentToken.value
        self.advance()
        operator = self.match(":=")
        self.advance()
        instruction = identifier + operator + self.expression()
        return instruction

    def expression(self):
        instruction = self.simple_expression()
        # self.advance()
        operator = self.match("<", "=")
        if operator != "error":
            self.advance()
            simpleExp = self.simple_expression()
            instruction += operator + simpleExp
        return instruction

    def simple_expression(self):
        instruction = self.term()
        # self.advance()
        while (self.match("+", '-') != "error"):
            operator = self.match("+", '-')
            self.advance()
            instruction += operator + self.term()
            # self.advance()
        # self.disadvance()
        return instruction       
        
    def term(self):
        instruction = self.factor()
        # self.advance()
        while (self.match("*", '/') != "error"):
            operator = self.match("*", '/')
            self.advance()
            instruction += operator + self.factor()
            # self.advance()
        # self.disadvance()
        return instruction

    def factor(self):
        instruction = ""
        if self.currentToken.type == "IDENTIFIER":
            instruction = self.currentToken.value
        elif self.currentToken.type == "NUMBER":
            instruction = str(self.currentToken.value)
        elif self.match("(") != "error":
            operator = self.match("(")
            self.advance()
            exp = self.expression()
            operator2 = self.match(")")
            # self.advance()
            instruction = operator + exp + operator2
        self.advance()
        return instruction
