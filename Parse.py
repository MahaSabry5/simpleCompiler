import sys
import re

f = open("test1.txt", "r")  # open file and read contents into a list (without "\n")
filelines = f.read().splitlines()
f.close()

keywordchecklist = [ "if", "int", "void"]  # list of all keywords

# our regular expressions for the lexical analyzer
wordsRegex = "[a-z]+"  # gets all words/ID's
numbersRegex = "[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?"  # gets all NUM's/float numbers
symRegex = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"  # gets all special symbols
errorRegex = "\S"

incomment = 0  # check to see if in comment
token = []  # create List to hold all tokens
i = 0  # token counter for parser

# ------------------Begin going through the file and getting tokens----------------------- #

for flines in filelines:
    fline = flines

    if not fline:
        continue
   

    regex = "(%s)|(%s)|(%s)|(%s)" % (wordsRegex, numbersRegex, symRegex, errorRegex)
    '([a-z]+)|([0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?)|'
    '("\/\*|\*\/|\+|-|\*|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]|//")|(\S)'

    for t in re.findall(regex, fline):
        if t[0] and incomment == 0:
            if t[0] in keywordchecklist:
                token.append(t[0])
            else:
                token.append(t[0])
        elif t[1] and incomment == 0:
            if "." in t[1]:
                token.append(t[1])
            elif "E" in t[1]:
                token.append(t[1])
            else:
                token.append(t[1])
        elif t[5]:
            if t[5] == "/*":
                incomment = incomment + 1

            elif t[5] == "*/" and incomment > 0:
                incomment = incomment - 1
            elif t[5] == "//" and incomment == 0:
                break
            elif incomment == 0:
                if t[5] == "*/":
                    if "*/*" in fline:
                        token.append("*")
                        incomment += 1
                        continue
                    else:
                        token.append("*")
                        token.append("/")
                else:
                    token.append(t[5])
        elif t[6] and incomment == 0:
            token.append(t[6])
# ------------ end of for loop for the file and getting tokens --------------------------- #

token.append("$")  # add to end to check if done parsing

# ---------------------------------- parsing functions ----------------------------------- #

def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)

def program():  # 1
    dl()
    if token[i] == "$":
        print ("ACCEPT")
    else:
        print ("REJECT")

def dl():  # 2
    declaration()
    dlprime()

def dlprime():  # 3
    if token[i] == "int" or token[i] == "void":
        declaration() #(4)
        dlprime() #(3)
    elif token[i] == "$":
        return
    else:
        return

#Check declaration
def declaration():  # 4
    global i
    types()
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        if token[i] == ";":
            i += 1  # Accept ;
        elif token[i] == "[":
            i += 1  # Accept [
            y = hasnum(token[i])
            if y is True:
                i += 1  # Accept NUM/FLOAT
                if token[i] == "]":
                    i += 1  # Accept ]
                    if token[i] == ";":
                        i += 1  # Accept ;
                    else:
                        print ("REJECT")
                        sys.exit(0)
                else:
                    print ("REJECT")
                    sys.exit(0)
            else:
                print ("REJECT")
                sys.exit(0)
        elif token[i] == "(":
            i += 1  # Accept (
            params()
            if token[i] == ")":
                i += 1  # Accept )
                compoundstmt()
            else:
                print ("REJECT")
                sys.exit(0)
        else:
            print ("REJECT")
            sys.exit(0)
    else:
        print ("REJECT")
        sys.exit(0)
#check variable definition
def vd():  # 5
    global i
    types()

    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
    else:
        print ("REJECT")
        sys.exit(0)

    if token[i] == ";":
        i += 1  # Accept ;
    else:
        print ("REJECT")
        sys.exit(0)
            
    #print ("Accept 'S > ID ;' : ",token [i-3:i:1])

#Check Types
def types():  # 6
    global i
    if token[i] == "int" :
        i += 1  # Accept int/void
        print ("Accept 'S > Type ID ' : ", token[i-1:i+1])
    elif token[i] == "void" :
        i += 1  # Accept int/void
        print ("Accept 'S > Type ID ()' : ", token[i-1:i+1])
    else:
        
        return
#Check Type _ declaration
def params():  # 7
    global i
    if token[i] == "int" :
        param() #(11)
        paramslistprime() #(10)
    elif token[i] == "void":
        i += 1  # Accept void
        return
    else:
        print ("REJECT")
        sys.exit(0)



#multiple value in function
def paramslistprime():  # 8
    global i
    if token[i] == ",":
        i += 1  # Accept ,
        param() #(9)
        paramslistprime() #(8)
    elif token[i] == ")":
        return
    else:
        return

# Check Var_name []
def param():  # 9
    global i
    types()
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
    else:
        return
    if token[i] == "[":
        i += 1  # Accept [
        if token[i] == "]":
            i += 1  # Accept ]
            return
        else:
            print ("REJECT")
            sys.exit(0)
    else:
        return

#Check main Fun first_End
def compoundstmt():  # 10
    global i
    if token[i] == "{":
        i += 1  # Accept {
    else:
        print ("REJECT NO Start of main s > ID(){")    
        sys.exit(0)
        #return
    
    localdeclarationsprime() #(14)
    statementlistprime() #(16)

    if token[i] == "}":
        i += 1  # Accept }
        print("END of main: S> ID(){L , L> EXP}, EXP > All ", token[i-1])
        
    else:
        print ("REJECT NO End of main S> ID(){L , L> EXP}")
        sys.exit(0)

#inside main
def localdeclarationsprime():  # 11
    if token[i] == "int" or token[i] == "void" :
        vd()
        localdeclarationsprime()

    else:
        return


def statementlistprime():  # 12
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        statement() #(17)
        statementlistprime()
    elif y is True:
        statement()
        statementlistprime()
    elif token[i] == "(" or token[i] == ";" or token[i] == "{" or token[i] == "if" :
        statement()
        statementlistprime()
    elif token[i] == "}":
        return
    else:
        return


def statement():  # 13
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        expstmt()
    elif y is True:
        expstmt()
    elif token[i] == "(" or token[i] == ";":
        expstmt()
    elif token[i] == "{":
        compoundstmt()
    elif token[i] == "if":
        selectionstmt()
    
    else:
        print ("REJECT")
        sys.exit(0)

#Ckeck END by (;)
def expstmt():  # 14
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
        else:
            print ("REJECT")
            sys.exit(0)
    elif y is True:
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
        else:
            print ("REJECT")
            sys.exit(0)
    elif token[i] == "(":
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
        else:
            print ("REJECT")
            sys.exit(0)
    elif token[i] == ";":
        i += 1  # Accept ;
        
    else:
        print ("REJECT")
        sys.exit(0)

# check if and else
def selectionstmt():  # 15
    global i
    if token[i] == "if":
        i += 1  # Accept if
    else:
        return

    if token[i] == "(":
        i += 1  # Accept (
    else:
        print ("REJECT S> IF(L)C")
        sys.exit(0)

    exp()

    if token[i] == ")":
        i += 1  # Accept )
        
    else:
        print ("REJECT S> IF(L)C")
        sys.exit(0)

    print("Accept >S> IF(L)C ,L> EXP ,EXP> ID Com ID,C> EXP,EXP > ID OP NUM ;,OP>*|/|+|-,Com> >=|<=|==|>|<")
    statement()

#Check expression
def exp():  # 16
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        ex()
    elif token[i] == "(":
        i += 1  # Accept (
        exp()
        if token[i] == ")":
            i += 1  # Accept )
            termprime()
            addexpprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                           token[i] == ">=" or token[i] == "==" :
                relop()
                addexp()
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" :
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" :
                relop()
                addexp()
            else:
                return
        else:
            print ("REJECT")
            sys.exit(0)
    elif y is True:
        i += 1  # Accept NUM/FLOAT
        termprime()
        addexpprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" :
            relop()
            addexp()
        elif token[i] == "+" or token[i] == "-":
            addexpprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                           token[i] == ">=" or token[i] == "==" :
                relop()
                addexp()
        elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                         token[i] == ">=" or token[i] == "==" :
                relop()
                addexp()
        else:
            return
    else:
        print ("REJECT")
        sys.exit(0)


def ex():  # 17
    global i
    if token[i] == "=":
        i += 1  # Accept =
        exp()
    elif token[i] == "(":
        i += 1  # Accept (
        args()
        if token[i] == ")":
            i += 1  # Accept )
            if token[i] == "*" or token[i] == "/":
                termprime()
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
                else:
                    return
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            else:
                return
        else:
            print ("REJECT")
            sys.exit(0)
    elif token[i] == "*" or token[i] == "/":
        termprime()
        addexpprime()
        print("S>ID=L,L>ID op ID,op>*|/|+|- ",token[i-5:i:1])
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        else:
            return
    elif token[i] == "+" or token[i] == "-":
        addexpprime()
        print("S>ID=L,L>ID op ID,op>*|/|+|-",token[i-5:i:1])
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        else:
            return
    elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                     token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        relop()
        addexp()
    else:
        return


#Check Compare Operators
def relop():  # 18
    global i
    if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                   token[i] == ">=" or token[i] == "==" :
        i += 1  # Accept <=, <, >, >=, ==
    else:
        return

def addexp():  # 19
    factor()
    termprime()
    addexpprime()

def addexpprime():  # 20
    if token[i] == "+" or token[i] == "-":
        addop()
        factor()
        termprime()
        addexpprime()
    else:
        return

#Check + or -
def addop():  # 21
    global i
    if token[i] == "+" or token[i] == "-":
        i += 1  # Accept +, -
    else:
        return


def termprime():  # 22
    if token[i] == "*" or token[i] == "/":
        mulop()
        factor()
        termprime()
    else:
        return

# Check * and /
def mulop():  # 23
    global i
    if token[i] == "*" or token[i] == "/":
        i += 1  # Accept *, /
    else:
        return


def factor():  # 24
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        
        if token[i] == "(":
            i += 1  # Accept (
            if token[i] == ")":
                i += 1  # Accept )
            else:
                return
        else:
            return
    elif y is True:
        i += 1  # Accept NUM/FLOAT
    elif token[i] == "(":
        i += 1  # Accept (
        exp()
        if token[i] == ")":
            i += 1  # Accept )
        else:
            return
    else:
        print ("REJECT")
        sys.exit(0)


# ----------------------------- end of parsing functions --------------------------------- #

# begin parsing
#program()
