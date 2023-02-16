# Define the input Python expression
expression = "x + (y * 4) - z"

# Split the expression into tokens
tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()

# Initialize a register counter and a stack for operators and operands
register_counter = 0
stack = []
mips_instruction = []

# Define a function to handle arithmetic operations on the stack
def handle_operation():
    operator = stack.pop()
    operand2 = stack.pop()
    operand1 = stack.pop()
    result_register = f"$t{register_counter}"
    mips_instruction = ""
    if operator == '+':
        mips_instruction = f"add {result_register}, {operand1}, {operand2}"
    elif operator == '-':
        mips_instruction = f"sub {result_register}, {operand1}, {operand2}"
    elif operator == '*':
        mips_instruction = f"mul {result_register}, {operand1}, {operand2}"
    elif operator == '/':
        mips_instruction = f"div {operand1}, {operand2}\nmflo {result_register}"
    stack.append(result_register)
    return mips_instruction

mips_code = []
# Generate MIPS code for each token
for token in tokens:
    if token.isnumeric():
        operand_mips = f"addi $t{register_counter}, $zero, {token}"
        stack.append(f"$t{register_counter}")
        register_counter += 1
    elif token.isalpha():
        operand_mips = f"lw $t{register_counter}, {token}"
        stack.append(f"$t{register_counter}")
        register_counter += 1
    elif token in ['+', '-', '*', '/']:
        while stack and stack[-1] in ['*', '/']:
            mips_instruction = handle_operation()
            mips_code.append(mips_instruction)
        stack.append(token)
    elif token == '(':
        stack.append(token)
    elif token == ')':
        while stack and stack[-1] != '(':
            mips_instruction = handle_operation()
            mips_code.append(mips_instruction)
        stack.pop()

# Handle remaining operators on the stack
while len(stack) > 1:
    mips_instruction = handle_operation()
    mips_code.append(mips_instruction)

# Generate MIPS code for storing the result
result_register = stack.pop()
store_mips = f"sw {result_register}, 0($zero)"

# Combine all the MIPS code
mips_code = [operand_mips for operand_mips in mips_code if operand_mips] + [store_mips]
mips_code = '\n'.join(mips_code)

# Print the generated MIPS code
print(mips_code)