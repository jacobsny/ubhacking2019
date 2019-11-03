keywords = ["auto", "double", "int", "struct", "break", "else", "long",
            "switch", "case", "enum", "register", "typedef", "const",
            "extern", "return", "union", "char", "float", "short", "unsigned",
            "continue", "for", "signed", "volatile", "default", "goto",
            "sizeof", "void", "do", "if", "static", "while"]

requires_brace = ["else", "switch", "for", "do", "if", "while"]

errors = []


def check_syntax(text):
    code = text.split('\n')
    check_semicolon(code)
    check_matching_brace(code)
    print(errors)


def check_semicolon(code):
    first = True
    line_number = 0
    for line in code:
        line_number += 1
        if first:
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


check_syntax("int example(){\n"
             "\tprintf(\"hello world\");\n"
             "\tint count = 0;\n"
             "\tfor( int i = 0; i < 5; i++ ){\n"
             "\t\tcount++;\n"
             "\t}\n"
             "}")

