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

pycode = """
x = 4 * 2
y = 4 - x
y = 16 / x
print(x)
print(y)
print("Hello world")
"""

pycode = """
x = input(1)
print(x)
x = input("apple")
print(x)
"""

pycode = """
x = 2
if x == 1:
    print(x)
"""

pycode = """
x = 1
if x == 1:
    print(x)
    print("X is printed!!")

if x == 2:
    print(x)
    print("X will not be printed!!")

"""

pycode = """
x = 1
if x == 2:
    print(x)
    print("this will not be printed!!")

elif x == 1:
    print(x)
    print("1 is printed!!")
"""

pycode = """
x = 3
if x == 2:    
    print("If statement")
elif x == 1:    
    print("Elif statement")
else:
    print("Else statement")
"""

pycode = """
x = 3
while x > 0:
    print(x)
    x = x - 1
"""

pycode = """
for i in range(10):
    print("Yay")
"""

pycode = """
for i in range(10, 20):
    print("Yay")
"""

pycode = """
for i in range(10, 20):
    print(i)
"""

data_segment = {}
var_counter = {"str": 0, "label": 0, "loop": 0}

markers_stack = []


class TemporaryMarker:
    def __init__(self, default, alt, label):
        self.value = default
        self.alt_value = alt
        self.label = label

    def __str__(self):
        return self.value


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
            i += 1
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

    while "(" in token:
        token.remove("(")
    while ")" in token:
        token.remove(")")

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

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nsub $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nsub $t0, $t0, $t1\nsw $t0, {dest}\n"

    def mul(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nmul $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nmul $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nmul $t0, $t0, $t1\nsw $t0, {dest}\n"

    def div(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\ndiv $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\ndiv $t0, $t0, $t1\nsw $t0, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\ndiv $t0, $t0, $t1\nsw $t0, {dest}\n"

    def beq(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nbeq $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nbeq $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nbeq $t0, $t1, {dest}\n"

    def bne(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nbne $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nbne $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nbne $t0, $t1, {dest}\n"

    def blt(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nblt $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nblt $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nblt $t0, $t1, {dest}\n"

    def bgt(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nbgt $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nbgt $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nbgt $t0, $t1, {dest}\n"

    def ble(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nble $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nble $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nble $t0, $t1, {dest}\n"

    def bge(self, op1, op2, dest):
        if isinstance(op1, str) and isinstance(op2, str):
            return f"lw $t0, {op1}\nlw $t1, {op2}\nbge $t0, $t1, {dest}\n"

        elif isinstance(op1, int) and isinstance(op2, str):
            return f"li $t0, {op1}\nlw $t1, {op2}\nbge $t0, $t1, {dest}\n"

        elif isinstance(op1, str) and isinstance(op2, int):
            return f"lw $t0, {op1}\nli $t1, {op2}\nbge $t0, $t1, {dest}\n"

    def assign(self, exp, dest):
        if len(exp) == 1:
            value = exp[0]
            if value == "input":
                raise Exception("unsuppotred")
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

        elif len(exp) == 2:
            preamble = ""
            arg = exp[1]
            print_ = f"print({arg})"
            preamble = self.to_mips(print_)

            take_input = f"la $a0, {dest}\nli $a1, 20\nli $v0, 8\nsyscall\n"
            if dest not in data_segment:
                data_segment[dest] = " " * 20
            return preamble + take_input

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

    def for_loop(self, start, end, step, loop_variable):
        load_start = f"lw $t7, {loop_variable}"

        if isinstance(end, int):
            load_end = f"li $t8, {end}"
        else:
            load_end = f"lw $t8, {end}"

        if isinstance(step, int):
            load_step = f"li $t9, {step}"
        else:
            load_step = f"lw $t9, {step}"

        end_loop = f"end_loop_{var_counter['loop']}"

        before = f"""

{self.assign([start], loop_variable)}
{load_start}
{load_end}
{load_step}

loop_{var_counter['loop']}:

blt $t9, $zero, decreasing_{var_counter['loop']}
bge $t7, $t8, {end_loop}
j end_guard_{var_counter['loop']}

decreasing_{var_counter['loop']}:
ble $t7, $t8, {end_loop}
end_guard_{var_counter['loop']}:
        """

        after = f"""
add $t7, $t7, $t9
sw $t7, {loop_variable}
j loop_{var_counter['loop']}
{end_loop}:
"""

        var_counter['loop'] += 1

        return before, [after]

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
                elif argument_value == None:
                    var = f"str_literal_{var_counter['str']}"

                    self.assign([arg], var)
                    var_counter['str'] += 1
                    return self.print_var_str(var)

        elif ins_type == "ASSIGN":
            variable = tokens[0]
            args = tokens[2:]
            return self.assign(args, variable)

        elif ins_type == "CONDITIONAL":
            # before - a single mips line that should precede a block
            # after - list of mips lines that should follow a block
            before = after = ""

            if tokens[0] == 'else':
                last_marker = markers_stack.pop()
                last_marker.value = last_marker.alt_value
                after = f"{last_marker.label}:"
                return before, [after]

            op1, comp, op2 = tokens[1:]
            # OPPOSITE !!!
            ops = {"==": "bne", "<": "bge", ">": "ble",
                   "<=": "bgt", ">=": "blt", "!=": "beq"}

            if isinstance(op1, int) and isinstance(op2, int):
                if not eval("".join(map(str, tokens[1:]))):
                    end_label = f"label_{var_counter['label']}"
                    else_label = f"else_label_{var_counter['label']}"

                    var_counter["label"] += 1
                    before = f"j {end_label}"

                    if tokens[0] == "if":
                        marker = TemporaryMarker(f"{end_label}:\n",
                                                 f"j {else_label}\n{end_label}:\n",
                                                 else_label)
                        markers_stack.append(marker)

                    # marker can be activated or not depending on the
                    # existence of else in future line
                    after = [markers_stack[-1], f"{end_label}:\n"]

            else:
                compare_and_jump = self.__getattribute__(ops.get(comp))

                end_label = f"label_{var_counter['label']}"
                else_label = f"else_label_{var_counter['label']}"
                var_counter["label"] += 1

                if tokens[0] == "if":
                    marker = TemporaryMarker("",
                                             f"j {else_label}\n",
                                             else_label)
                    markers_stack.append(marker)

                before = compare_and_jump(op1, op2, end_label)

                # marker can be activated or not depending on the
                # existence of else in future line
                after = [markers_stack[-1], f"{end_label}:\n"]

            return (before, after)

        elif ins_type == "WHILE":
            op1, comp, op2 = tokens[1:]
            # OPPOSITE !!!
            ops = {"==": "bne", "<": "bge", ">": "ble",
                   "<=": "bgt", ">=": "blt", "!=": "beq"}

            if isinstance(op1, int) and isinstance(op2, int):
                if not eval("".join(map(str, tokens[1:]))):
                    end_label = f"loop_{var_counter['label']}"

                    var_counter["loop"] += 1
                    before = f"j {end_label}"

            else:
                compare_and_jump = self.__getattribute__(ops.get(comp))

                start_label = f"loop_{var_counter['loop']}"
                end_label = f"endloop_{var_counter['loop']}"
                var_counter["loop"] += 1

                before = f"{start_label}:\n" + \
                    compare_and_jump(op1, op2, end_label)

                after = [f"j {start_label}\n{end_label}:\n"]

            return (before, after)

        elif ins_type == "FOR":
            loop_variable = tokens[1]

            length = len(tokens[4:])

            if length == 2:
                start = 0
                end = tokens[4]
                step = 1
            elif length == 3:
                start = tokens[4]
                end = tokens[5]
                step = 1
            elif length == 4:
                start = tokens[4]
                end = tokens[5]
                step = tokens[6]

            return self.for_loop(start, end, step, loop_variable)

        return ""

    # def compile(self):
    #     for child in self.walk():
    #         yield self.to_mips(child)
    def compile(self):
        after = before = "#"
        for child in self.child:
            if isinstance(child, str):
                token = tokenize(child)
                ins_type = match_pattern(token)

                if ins_type in ("CONDITIONAL", "WHILE", "FOR"):
                    before, after = self.to_mips(child)
                    yield before

                else:
                    yield self.to_mips(child)

            else:
                yield from child.compile()
                for item in after:
                    yield item

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
    if len(tokens) >= 1 and tokens[0] in ("if", "elif", "else"):
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
    f.write("\n".join(map(str, mips_code)))
    f.write("\n".join(dataseg))
