OPERATORS = {"+", "-", "*", "/"}
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "neg": 3}


def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isspace():
            i += 1
        elif char in "0123456789":
            start = i
            while i < len(expression) and expression[i] in "0123456789":
                i += 1
            tokens.append(int(expression[start:i]))
        elif char in "+-*/()":
            tokens.append(char)
            i += 1
        else:
            raise ValueError(f"Invalid character '{char}' in expression")

    if not tokens:
        raise ValueError("Expression is empty")
    return tokens


def to_postfix(tokens):
    output = []
    stack = []
    previous = None

    for token in tokens:
        if isinstance(token, int):
            if isinstance(previous, int) or previous == ")":
                raise ValueError("Missing operator before a number")
            output.append(token)

        elif token == "(":
            if isinstance(previous, int) or previous == ")":
                raise ValueError("Missing operator before '('")
            stack.append(token)

        elif token == ")":
            if previous is None or previous in OPERATORS or previous == "(":
                raise ValueError("Missing value before ')'")
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Brackets do not match")
            stack.pop()

        else:
            is_unary = previous is None or previous in OPERATORS or previous == "("
            if is_unary:
                if token == "-":
                    stack.append("neg")
                elif token != "+":
                    raise ValueError(f"Operator '{token}' has no left value")
            else:
                while stack and stack[-1] != "(" and PRECEDENCE[stack[-1]] >= PRECEDENCE[token]:
                    output.append(stack.pop())
                stack.append(token)

        previous = token

    if previous in OPERATORS:
        raise ValueError("Expression cannot end with an operator")

    while stack:
        top = stack.pop()
        if top == "(":
            raise ValueError("Brackets do not match")
        output.append(top)

    return output


def evaluate_postfix(postfix):
    stack = []
    for token in postfix:
        if isinstance(token, int):
            stack.append(token)
        elif token == "neg":
            stack.append(-stack.pop())
        else:
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.append(left / right)

    if len(stack) != 1:
        raise ValueError("Malformed expression")
    return float(stack[0])


def calculate(expression):
    if not isinstance(expression, str):
        raise TypeError("Expression must be a string")
    return evaluate_postfix(to_postfix(tokenize(expression)))


def main():
    tests = ["-(3 + 2) * 4 + 18 / 3", "2 + 3 * 4", "(2 + 3) * 4", "--5", "10 / 4",
             "5 / (3 - 3)", "2 +", "(2 + 3", "2 3", "()", "4 $ 4", ""]
    for text in tests:
        try:
            print(f"{text!r:28} = {calculate(text)}")
        except (ValueError, ZeroDivisionError) as error:
            print(f"{text!r:28} -> Error: {error}")


if __name__ == "__main__":
    main()