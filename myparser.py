from mytoken import Token, availableTokens
from graphviz import Digraph
from mygraph import dot,Node
from error import *

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

    def match(self, token1, token2=None):
        if self.currentToken.type == availableTokens[token1]:
            return token1
        elif token2 != None and self.currentToken.type == availableTokens[token2]:
            return token2
        else:
            return "error"

    def parse(self):
        dot.clear()
        while self.index < len(self.tokenslist) :
            stmt_sq = self.stmt_sequence()
            # self.statements.append(stmt_sq)
        # return self.statements
        dot.render('round-table.gv', view=True)

    def stmt_sequence(self):
        statement = self.statement()
        opnode=statement
        while (self.match(";") != "error"):
            operator = self.match(";")
            opnode = Node(str(self.index), availableTokens[operator]+"\n"+operator)
            opnode.addNode()
            opnode.addChild(statement)
            stm = self.statement()
            opnode.addChild(stm)
            # statement +=  " " + operator + " " + self.statement()
        statement = opnode
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
        instruction = Node(str(self.index), "read", "rect")
        instruction.addNode()
        self.advance()
        if self.currentToken.type == "IDENTIFIER":
            # instruction = "read " + self.currentToken.value
            child = Node(str(self.index),self.currentToken.type + "\n" + self.currentToken.value)
            child.addNode()
            instruction.addChild(child)
            self.advance()
            return instruction
        else :
            # self.error("Expecting an Identifier!")
            raise ExpectingIdentifier

    def write_stmt(self):
        instruction = Node(str(self.index), "write", "rect")
        instruction.addNode()
        self.advance()
        # instruction = "write " + self.expression()
        exp = self.expression()
        instruction.addChild(exp)
        return instruction

    def if_stmt(self):
        instruction = Node(str(self.index), availableTokens['if'], "rect")
        instruction.addNode()
        self.advance()
        expr = self.expression()
        instruction.addChild(expr)
        # instruction = "if " + self.expression()
        operator = self.match("then")
        if operator=="error":
            # self.error("Expecting 'then'!")
            raise ExpectingThen
        then = Node(str(self.index), availableTokens[operator]+"\n"+operator)
        then.addNode()
        instruction.addChild(then)
        # instruction += " " + operator + " "
        stmt_sq = self.stmt_sequence()
        # instruction += stmt_sq + " "
        then.addChild(stmt_sq)
        # operator = self.match("end")
        # if operator == "error":
        #     self.error("Expecting 'end'!")
        # # instruction += operator 
        # end = Node(str(self.index), availableTokens[operator]+"\n"+operator)
        # end.addNode()
        # instruction.addChild(end)
        # self.advance()
        operator = self.match("end", "else")
        if operator == "end":
            self.advance()
            # instruction += operator
            end = Node(str(self.index), availableTokens[operator]+"\n"+operator)
            end.addNode()
            instruction.addChild(end)
        elif operator == "else":
            # instruction += "else "
            elsee = Node(str(self.index), availableTokens[operator]+"\n"+operator)
            elsee.addNode()
            instruction.addChild(elsee)
            stmt_sq = self.stmt_sequence()
            elsee.addChild(stmt_sq)
            operator = self.match("end")
            end = Node(str(self.index), availableTokens[operator]+"\n"+operator)
            end.addNode()
            instruction.addChild(end)
            self.advance()
            # instruction += stmt_sq + " " + operator
        else:
            # self.error("Expecting 'end' or 'else'")
            raise ExpectingEnd
        return instruction

    def repeat_stmt(self):    
        # instruction = "repeat " + self.stmt_sequence() + " "
        instruction = Node(str(self.index), availableTokens['repeat'], "rect")
        instruction.addNode()
        stm_sq = self.stmt_sequence()
        instruction.addChild(stm_sq)
        operator = self.match("until")
        if operator == "error":
            # self.error("Expecting 'until'!")
            raise ExpectingUntil
        until = Node(str(self.index), availableTokens[operator]+"\n"+operator)
        until.addNode()
        instruction.addChild(until)
        self.advance()
        # instruction += operator + " " + self.expression()
        exp = self.expression()
        until.addChild(exp)
        return instruction

    def assign_stmt(self):
        # identifier = self.currentToken.value
        identifier = Node(str(self.index), self.currentToken.type + "\n" + self.currentToken.value)
        identifier.addNode()
        self.advance()
        operator = self.match(":=")
        if operator == "error":
            # self.error("Expecting ':='!")
            raise ExpectingAssign
        assignnode = Node(str(self.index), availableTokens[operator], "rect")
        assignnode.addNode()
        assignnode.addChild(identifier)
        self.advance()
        # instruction = identifier + operator + self.expression()
        exp = self.expression()
        assignnode.addChild(exp)
        instruction = assignnode
        return instruction

    def expression(self):
        instruction = self.simple_expression()
        if instruction.name != "error":
            operator = self.match("<", "=")
            if operator != "error":
                opnode = Node(str(self.index), availableTokens[operator]+"\n"+operator)
                opnode.addNode()
                opnode.addChild(instruction)
                self.advance()
                simpleExp = self.simple_expression()
                if simpleExp.name != "error":
                    # instruction += operator + simpleExp
                    opnode.addChild(simpleExp)
                    instruction = opnode
                else :
                    self.error("Expecting Simple Expression!")
        return instruction

    def simple_expression(self):     
        instruction = self.term()
        if instruction.name != "error":
            while (self.match("+", '-') != "error"):
                operator = self.match("+", '-')
                opnode = Node(str(self.index), availableTokens[operator]+"\n"+operator)        
                opnode.addNode()
                opnode.addChild(instruction)
                self.advance()
                trm = self.term()
                if trm.name != "error":
                    # instruction += operator + trm
                    opnode.addChild(trm)
                    instruction = opnode
                else:
                    self.error("Expecting term!")
        return instruction       
        
    def term(self):
        instruction = self.factor()
        if instruction.name != "error":
            while (self.match("*", '/') != "error"):
                operator = self.match("*", '/')
                opnode = Node(str(self.index), availableTokens[operator]+"\n"+operator)    
                opnode.addNode()   
                opnode.addChild(instruction)
                self.advance()
                fact = self.factor()
                if fact.name != "error":
                    # instruction += operator + fact
                    opnode.addChild(fact)
                    instruction = opnode
                else:
                    self.error("Expecting factor!")
        return instruction

    def factor(self):
        # instruction = "error"
        instruction = Node("error", self.currentToken.value)
        if self.currentToken.type == "IDENTIFIER":
            # instruction = self.currentToken.value
            instruction.text = self.currentToken.type + "\n" + self.currentToken.value
            instruction.name = str(self.index)
        elif self.currentToken.type == "NUMBER":
            # instruction = str(self.currentToken.value)
            instruction.text = self.currentToken.type + "\n" + str(self.currentToken.value)
            instruction.name = str(self.index)
        elif self.match("(") != "error":
            instruction.text= "( ) Expression"
            instruction.name = str(self.index)
            operator = self.match("(")
            leftbracket = Node(str(self.index*10), availableTokens[operator]+"\n"+operator)    
            leftbracket.addNode()  
            self.advance()
            exp = self.expression()
            if exp == "error":
                self.error("Expecting expression!")
            instruction.addChild(leftbracket)
            instruction.addChild(exp)
            operator2 = self.match(")")
            if operator2 == "error":
                # self.error("Expecting ')'!")
                raise ExpectingRightBracket
            # instruction = operator + exp + operator2
            rightbracket = Node(str(self.index), availableTokens[operator2]+"\n"+operator2)    
            rightbracket.addNode()  
            instruction.addChild(rightbracket)
        else:
            # self.error("Expecting identifier, number or '('!")
            raise ExpectingNumorId
        self.advance()
        instruction.addNode()
        return instruction
