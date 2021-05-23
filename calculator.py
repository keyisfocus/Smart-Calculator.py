import collections
import re

VAR_REGEX = re.compile(r'[a-zA-Z]+')
variables = {}


def execute_command(command) -> bool:
    if command == '/exit':
        print('Bye!')
        return True
    elif command == '/help':
        print('The program calculates given expression')
    else:
        print('Unknown command')
    return False


def apply_operator(operator, operand1, operand2):
    if operator == '+':
        return operand1 + operand2
    if operator == '-':
        return operand1 - operand2
    if operator == '*':
        return operand1 * operand2
    if operator == '/':
        return operand1 // operand2


def parse_plus_minus(string):
    plus = True
    for char in string:
        plus = plus if char == '+' else not plus
    return '+' if plus else '-'


def assignment(string):
    pair = string.split('=')
    if len(pair) != 2:
        print('Invalid assignment')
    pair = [p.strip() for p in pair]

    if not VAR_REGEX.fullmatch(pair[0]):
        print('Invalid identifier')

    if VAR_REGEX.fullmatch(pair[1]):
        if pair[1] in variables:
            variables[pair[0]] = variables[pair[1]]
        else:
            print('Unknown variable')
    elif re.fullmatch(r'\+?-?[0-9]+', pair[1]):
        variables[pair[0]] = pair[1]
    else:
        print('Invalid expression')


def get_precedence(operator):
    if operator in ('-', '+'):
        return 1
    elif operator in ('*', '/'):
        return 2
    else:
        return -1


while True:
    line = input().strip()

    if line.startswith('/'):
        if execute_command(line):
            break
        continue

    if line:
        if '=' in line:
            assignment(line)
            continue

        stack = collections.deque()
        postfix = ''

        error = 0

        i = 0
        while i < len(line):
            if line[i].isnumeric() or (line[i] in ('-', '+') and line[i + 1].isnumeric()):
                num = line[i]
                i += 1
                while i < len(line) and line[i] != ' ' and line[i].isnumeric():
                    num += line[i]
                    i += 1
                postfix += num + ' '
            elif VAR_REGEX.fullmatch(line[i]) or (line[i] in ('-', '+') and VAR_REGEX.fullmatch(line[i + 1])):
                var = line[i]
                i += 1
                while i < len(line) and line[i] != ' ' and VAR_REGEX.fullmatch(line[i]):
                    var += line[i]
                    i += 1
                if var not in variables and var[1:] not in variables:
                    error = 'Unknown variable'
                    break
                postfix += variables.get(var, variables.get(var[1:], None)) + ' '
            elif line[i] in ('-', '+', '*', '/', '(', ')'):
                if line[i] in ('-', '+'):
                    sign = line[i]
                    i += 1
                    while i < len(line) and line[i] != ' ':
                        sign += line[i]
                        i += 1
                    op = parse_plus_minus(sign)
                else:
                    op = line[i]
                    i += 1

                if op == ')':
                    if not stack or '(' not in stack:
                        error = 'Invalid expression'
                        break
                    while stack[-1] != '(':
                        postfix += stack.pop() + ' '
                    stack.pop()
                elif len(stack) == 0 or stack[-1] == '(' or op == '(' or get_precedence(op) > get_precedence(stack[-1]):
                    stack.append(op)
                elif get_precedence(op) <= get_precedence(stack[-1]):
                    while len(stack) > 0 and stack[-1] != '(' and get_precedence(op) <= get_precedence(stack[-1]):
                        postfix += stack.pop() + ' '
                    stack.append(op)
            elif line[i] == ' ':
                i += 1
            else:
                error = 'Invalid expression'
                break

        while len(stack) > 0:
            o = stack.pop()
            if o in ('(', ')'):
                error = 'Invalid expression'
                break
            postfix += o + ' '
        postfix = postfix.strip()

        if error:
            print(error)
            continue

        for part in postfix.split():
            if part.isnumeric() or part[1:].isnumeric():
                stack.append(int(part))
            else:
                if len(stack) < 2:
                    print('Invalid expression')
                    break
                operand2 = stack.pop()
                stack.append(apply_operator(part, stack.pop(), operand2))

        print(stack.pop())
