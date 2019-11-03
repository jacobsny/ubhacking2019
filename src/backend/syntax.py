keywords = ["auto", "double", "int", "struct", "break", "else", "long",
            "switch", "case", "enum", "register", "typedef", "const",
            "extern", "return", "union", "char", "float", "short", "unsigned",
            "continue", "for", "signed", "volatile", "default", "goto",
            "sizeof", "void", "do", "if", "static", "while"]

operators = ["+", "-", "*", "/", "=", "==", "+=", "-=", "&&", "||", "<", ">", "<=", ">="]

requires_brace = ["else", "switch", "for", "do", "if", "while"]
requires_paren = ["for", "sizeof", "if", "while"]
first_type = ["signed", "unsigned", "short", "long"]
second_type = ["char", "int", "float", "double"]

declared_variables = []
errors = []


def check_syntax(text):
    code = text.split('\n')
    check_semicolon(code)
    check_matching_brace(code)
    check_matching_paren(code)
    check_matching_bracket(code)
    check_conditional_enclosed(code)
    check_kw_case(code)
    check_vars_declared(code)
    return errors


def check_semicolon(code):
    first = True
    line_number = 0
    for line in code:
        line_number += 1
        if line != "":
            if first and line[0] != "#":
                first = False
            else:
                contained = False
                for word in requires_brace:
                    if word in line:
                        contained = True
                        break
                if len(line) > 0 and line[len(line) - 1] != ";" and line[0] != "{" and line[0] != "}" \
                        and line[len(line) - 1] != '{' and line[len(line) - 1] != '}' and not contained:
                    errors.append({"location": line_number, "description": "Missing semicolon"})


def check_matching_brace(code):
    if '{' not in code[0] and '}' not in code[len(code) - 1]:
        errors.append({"location": 1, "description": "Function declaration must be within braces"})
    stack = []
    line_number = 0
    for line in code:
        line_number += 1
        for char in line:
            if char == '{':
                stack.append(['{', line_number])
            if char == '}' and len(stack) > 0:
                stack.pop()
            elif char == '}' and len(stack) < 1:
                errors.append({"location": line_number, "description": "Missing open brace"})
    if len(stack) > 0:
        for lst in stack:
            errors.append({"location": lst[1], "description": "Missing close brace"})


def check_matching_paren(code):
    stack = []
    line_number = 0
    for line in code:
        line_number += 1
        for char in line:
            if char == '(':
                stack.append(['(', line_number])
            if char == ')' and len(stack) > 0:
                stack.pop()
            elif char == ')' and len(stack) < 1:
                errors.append({"location": line_number, "description": "Missing open paren"})
    if len(stack) > 0:
        for lst in stack:
            errors.append({"location": lst[1], "description": "Missing close paren"})


def check_matching_bracket(code):
    stack = []
    line_number = 0
    for line in code:
        line_number += 1
        for char in line:
            if char == '[':
                stack.append(['[', line_number])
            if char == ']' and len(stack) > 0:
                stack.pop()
            elif char == ']' and len(stack) < 1:
                errors.append({"location": line_number, "description": "Missing open bracket"})
    if len(stack) > 0:
        for lst in stack:
            errors.append({"location": lst[1], "description": "Missing close bracket"})


def check_conditional_enclosed(code):
    line_number = 0
    for line in code:
        line_number += 1
        for word in requires_paren:
            if word in line and '(' not in line and ')' not in line:
                errors.append({"location": line_number, "description": "Statements using \"" + word +
                                                                       "\" must be enclosed by parenthesis"})


def check_kw_case(code):
    line_number = 0
    for line in code:
        line_number += 1
        words = line.split(' ')
        for word in words:
            if word.lower() in keywords and word != word.lower():
                errors.append({"location": line_number, "description": "Keywords must be completely lowercase"})


def check_vars_declared(code):
    line_number = 0
    for line in code:
        line_number += 1
        words = line.split(' ')
        if '' in words:
            words.remove('')
        if is_declaration(line, line_number):
            i = 0
            while i < 4:
                if words[i] in first_type:
                    i += 1
                elif words[i] in second_type:
                    i += 1
                    break
                else:
                    break
            declared_variables.append(words[i].strip('\r*;'))
        elif is_assignment(line):
            if words[0] not in declared_variables:
                errors.append({"location": line_number, "description": "\"" + words[0] + "\"" + " is not defined"})
    print(declared_variables)


def is_declaration(line, line_number):
    words = line.split(' ')
    if (words[0] not in first_type and words[0] not in second_type) or words[0] == '':
        return False
    i = 0
    while i < 4:
        if words[i] in first_type:
            i += 1
        elif words[i] in second_type:
            i += 1
            break
        else:
            if i > 0:
                if words[i - 1] == "signed" or words[i - 1] == "unsigned":
                    errors.append({"location": line_number, "description": "\""
                                   + words[i - 1] + "\"" + " is not a declarable type"})
            break
    if ';' in words[i]:
        return True
    if '(' and ')' in words[i]:
        return False
    if words[i+1] != '=':
        return False
    return True


def is_assignment(line):
    words = line.split(' ')
    if '' in words:
        words.remove('')
    if not len(words) >= 2:
        return False
    if words[1] not in operators:
        return False
    return True


print(check_syntax("int example(){\n"
                   "printf(\"hello world\");\n"
                   "char *x;\n"
                   "long int varName = 5;\n"
                   "for( int i = 0; i < count.length; i++ ){\n"
                   "double count = sizeof(int);\n"
                   "}\n"
                   "}"))


#NOTES: a loop such as "for int i = 0; i < sizeof(int); i++ " would not thow an error, as the line contains "()" from sizeof().
       #This could be expanded in later versions, but is too intensive for tonight.