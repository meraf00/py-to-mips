pycode = """
x = 3
if x:
    x = 4
    while x < 10:
        x = x + 1
    print(2)
print(x)
"""
def typ(char):
     if char.isalpha():
        tp="str"
     elif char.isdigit():
        tp = "num"
     else:
        tp = "sym"
     return tp

def match_pattern(line):
    line = line.strip()
    token = []
    itera = enumerate(line)
    i =0
    while i < len(line):
        char = line[i]
        if char in ["'", '"']:
            for j in range(i+1, len(line)):
                if j == char:
                    break
            else:
                raise Exception("unterminated string >" + line)
            
            token.append(line[i:j+1])
        elif char in [" ", "\t"]:
            continue
        else:
            cur =[char]
            t=typ(char)
            
            while i < len(line):
                char = line[i]
                if char in [" ", "\n", "\t"] or typ(char) != t:
                    i += 1
                    break                
                cur.append(char)
                i += 1            
                
            cur = "".join(cur)
            if cur.isnumeric():
                token.append(float(cur))
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
    
    def walk(self):
        for child in self.child:
            if isinstance(child, str):
                yield child
            else:
                yield from child.walk()

def isblank(line):
    return len(line.strip() ) ==0       
def indent(line):
    cnt = 0
    for char in line:
        if char == " ":
            cnt += 1
        else:
            break
    return cnt

blocks = [Block()]

prev = 0            
for line in pycode.split("\n"):
    print(line)
    if isblank(line):
        continue
    cur = blocks[-1]
    i =   indent(line)
    if i == prev:
        cur.child.append(line.strip())
        
    elif i > prev:
        new = Block()
        new.child.append(line.strip())
        cur.child.append(new)
        blocks.append(new)
    else:
        for _ in range( (prev - i) // 4):
            blocks.pop()
        cur = blocks[-1]
        
        cur.child.append(line.strip())
    prev = i
print(blocks)        

for ins in blocks[0].walk():
    print(ins)
    print(match_pattern(ins))
    print()
