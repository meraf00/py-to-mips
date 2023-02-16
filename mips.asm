.text
li $t0, 31
sw $t0, x
li $t0, 34
lw $t1, x
add $t0, $t0, $t1
sw $t0, y

li $t0, 9
sw $t0, z
lw $t0, x
lw $t1, z
add $t0, $t0, $t1
sw $t0, a

lw $a0, y
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall

lw $a0, a
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall
.data
x: .word 31
y: .word 0
z: .word 0
a: .word 0