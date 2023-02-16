exp = "5/3-2"
# exp = "5 / 3 - 2"

out = []
for char in exp:
    if char in "+-*/":
        out.append(" ")
        out.append(char)
        out.append(" ")
        continue
    out.append(char)

print("".join(out))
    