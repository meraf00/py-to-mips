pycode = """
x = 3
y = "a"
z = x
if x == 2:
    x = 4
    while x < 10:
        x = x + 1
    print(2)
print(x)
"""

pycode = """
x = 3
print(x)
x = 5
z = x
print(z)
print(x)
"""

pycode = """
x = "apple"
print(x)
y = 34 + 1
print(y)
"""

pycode = """
x = 31
y = 34 + x
z = 4 + 5
a = x + z
print(y)
print(a)
"""

data_segment = {}


def typ(char):
    if char.isalpha():
        tp = "str"
    elif char.isdigit():
        tp = "num"
    else:
        tp = "sym"
    return tp


def tokenize(line):
    line = line.strip()
    token = []
    itera = enumerate(line)
    i = 0
    while i < len(line):
        char = line[i]

        if char in ["'", '"']:
            j = i
            i += 1
            while i < len(line):
                if line[i] == char:
                    break
                i += 1
            else:
                raise Exception("unterminated string >" + line)

            token.append(line[j:i+1])
        elif char in [" ", "\t"]:
            continue
        else:
            cur = []
            t = typ(char)

            while i < len(line):
                char = line[i]
                if char in [" ", "\n", "\t"] or typ(char) != t:
                    break
                cur.append(char)
                i += 1

            cur = "".join(cur)
            if cur.isnumeric():
                token.append(int(cur))
            else:
                token.append(cur)
        i += 1
    return token


class Block:
    def __init__(self):
        self.child = []

    def __repr__(self):
        return str(self.child)

    def recreate(self, depth=0):
        for child in self.child:
            if isinstance(child, str):
                yield (depth, child)
            else:
                yield from child.recreate(depth + 1)

    def print_int(self, num):
        return f"li $a0, {num}\nli $v0, 1\nsyscall\nli $a0, 10\nli $v0, 11\nsyscall\n"

    def print_var_int(self, var):
        return f"lw $a0, {var}\nli $v0, 1\nsyscall\nli $a0, 10\nli $v0, 11\nsyscall\n"

    def print_var_str(self, var):
        return f"la $a0, {var}\nli $v0, 4\nsyscall\nli $a0, 10\nli $v0, 11\nsyscall\n"

    def input(self, dest):
        return f"li $a0, {dest}\n\nli $v0, 1\nsyscall\n"

    def add(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nadd $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nadd $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nadd $t0, $t0, $t1\nsw $t0, {dest}\n"

    def sub(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nsub $t0, $t0, $t1\nsw $t0, {dest}\n"

    def mul(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nmul $t0, $t0, $t1\nsw $t0, {dest}\n"

    def div(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nadiv $t0, $t0, $t1\nsw $t0, {dest}\n"

    def assign(self, exp, dest):
        if len(exp) == 1:
            value = exp[0]
            if isinstance(value, int):
                if dest not in data_segment:
                    data_segment[dest] = value
                return f"li $t0, {value}\nsw $t0, {dest}"

            elif isinstance(value, str):
                if value[0] in ["'", '"']:  # actual str
                    data_segment[dest] = value[1:-1]

                else:  # variable
                    if dest not in data_segment:
                        data_segment[dest] = 0
                    return f"lw $t0, {value}\nsw $t0, {dest}"

        elif len(exp) == 3:
            ops = {"+": "add", "-": "sub", "*": "mul", "/": "div"}

            op1, op, op2 = exp

            if dest not in data_segment:
                data_segment[dest] = 0

            if isinstance(op1, int) and isinstance(op2, int):
                return self.assign([int(eval("".join(map(str, exp))))], dest)

            else:
                operation = self.__getattribute__(ops.get(op))
                return operation(op1, op2, dest)

        return ""

    def to_mips(self, python_code):
        tokens = tokenize(python_code)
        ins_type = match_pattern(tokens)

        if ins_type == "PRINT":
            arg = tokens[1]
            if isinstance(arg, int):
                return self.print_int(arg)
            elif isinstance(arg, str):
                argument_value = data_segment.get(arg)
                if isinstance(argument_value, int):
                    return self.print_var_int(arg)
                elif isinstance(argument_value, str):
                    return self.print_var_str(arg)

        elif ins_type == "ASSIGN":
            variable = tokens[0]
            args = tokens[2:]
            return self.assign(args, variable)

        return ""

    def compile(self):
        for child in self.walk():
            # if isinstance(child, str):
            yield self.to_mips(child)
            # else:
            #     yield from child.compile()

    # def compile(self):
    #     for child in self.walk():
    #         if isinstance(child, str):
    #             yield self.to_mips(child)
    #         else:
    #             yield from child.compile()

    def walk(self):
        for child in self.child:
            if isinstance(child, str):
                yield child
            else:
                yield from child.walk()


def isblank(line):
    return len(line.strip()) == 0


def indent(line):
    cnt = 0
    for char in line:
        if char == " ":
            cnt += 1
        else:
            break
    return cnt


def is_assignment(tokens):
    if len(tokens) >= 3 and tokens[1] == "=":
        return True


def is_conditional(tokens):
    if len(tokens) >= 1 and tokens[0] == "if":
        return True


def is_for_loop(tokens):
    if len(tokens) >= 1 and tokens[0] == "for":
        return True


def is_while_loop(tokens):
    if len(tokens) >= 1 and tokens[0] == "while":
        return True


def is_print(tokens):
    if len(tokens) >= 1 and tokens[0] == "print":
        return True


def is_input(tokens):
    if len(tokens) >= 1 and tokens[0] == "input":
        return True


def match_pattern(tokens):
    if is_assignment(tokens):
        return "ASSIGN"
    elif is_conditional(tokens):
        return "CONDITIONAL"
    elif is_for_loop(tokens):
        return "FOR"
    elif is_while_loop(tokens):
        return "WHILE"
    elif is_print(tokens):
        return "PRINT"
    elif is_input(tokens):
        return "INPUT"


blocks = [Block()]

prev = 0
for line in pycode.split("\n"):
    print(line)
    if isblank(line):
        continue
    cur = blocks[-1]
    i = indent(line)
    if i == prev:
        cur.child.append(line.strip())

    elif i > prev:
        new = Block()
        new.child.append(line.strip())
        cur.child.append(new)
        blocks.append(new)
    else:
        for _ in range((prev - i) // 4):
            blocks.pop()
        cur = blocks[-1]

        cur.child.append(line.strip())
    prev = i

print(blocks)

for ins in blocks[0].walk():
    tokens = tokenize(ins)
    ins_type = match_pattern(tokens)
    print(ins, tokens, ins_type)

mips_code = [".text"]
for mips in blocks[0].compile():
    mips_code.append(mips)

dataseg = [".data"]


def build_data_segment():
    for varname, value in data_segment.items():
        if isinstance(value, int):
            dataseg.append(f"{varname}: .word {value}")

        elif isinstance(value, str):
            dataseg.append(f'{varname}: .asciiz "{value}"')


build_data_segment()
with open("mips.asm", "w") as f:
    f.write("\n".join(mips_code))
    f.write("\n".join(dataseg))
