def readNumber(line, index):
    number = 0
    flag = 0
    keta = 1
    while index < len(line) and (line[index].isdigit() or line[index] == '.'):
        if line[index] == '.':
            flag = 1
        else:
            number = number * 10 + int(line[index])
            if flag == 1:
                keta *= 0.1
        index += 1
    token = {'type': 'NUMBER', 'number': number * keta}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readTimes(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def readLeftPar(line, index):
    token = {'type': 'LEFTPAR'}
    return token, index + 1

def readRightPar(line, index):
    token = {'type': 'RIGHTPAR'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readTimes(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readLeftPar(line, index)
        elif line[index] == ')':
            (token, index) = readRightPar(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens


def parcount(tokens):
    leftcount = 0
    rightcount = 0
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'LEFTPAR':
            leftcount += 1
        elif tokens[index]['type'] == 'RIGHTPAR':
            rightcount += 1
        index += 1
    if leftcount == rightcount:
        return 'OK'
    else:
        print '! the number of left parenthesis and that of right parenthesis are different\n'
        return 'NG'


#calculate until () disappear
def evaluateParentheses(tokens):
    index = 1
    while index < len(tokens):
#        print index
        if tokens[index]['type'] == 'RIGHTPAR':
            right = index
#            print 'right:''+str(right)
            for left in xrange(right-1, -1, -1):
#                print 'leftrange:'+str(left)
                if tokens[left]['type'] == 'LEFTPAR':
#                    print 'left:'+str(left)
                    partokens = tokens[left+1:right]
#                    print("partokens")
#                    for p in partokens:
#                        print(p)
                    tokens.insert(left, {'type': 'NUMBER', 'number': evaluate(partokens)})
                    del tokens[left+1:right+2]
#                    print("tokens")
#                    for t in tokens:
#                        print(t)
                    index = 0
                    break
        index += 1
    return tokens

def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'TIMES':
            mul = tokens[index-1]['number'] * tokens[index+1]['number']
            tokens.insert(index-1, {'type': 'NUMBER', 'number': mul})
            del tokens[index:index+3]
        elif tokens[index]['type'] == 'DIVIDE':
            div = float(tokens[index-1]['number']) / tokens[index+1]['number']
            tokens.insert(index-1, {'type': 'NUMBER', 'number': div})
            del tokens[index:index+3]
        else:
            index += 1
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax'
        index += 1
    return answer


def test(line, expectedAnswer):
    tokens = tokenize(line)
    evaluateParentheses(tokens)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("2.5*5", 12.5)
    test("1+2*3-4/5", 6.2)
    test("6/4*5", 7.5)
    test("1+2*(3+4)", 15)
    test("((3.0+4*(2-1))/5)*10", 14)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    finish = 0
    if '(' in line:
        if parcount(tokens) == 'OK':    #if the number of ( and ) are the same
            evaluateParentheses(tokens)         #handle ()
        else:                           #if the number of ( and ) are different, the calculation is stopped
            finish = 1
    if finish == 0:
        answer = evaluate(tokens)
        print "answer = %f\n" % answer
