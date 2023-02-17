.text
li $t0, 10
sw $t0, x

li $t0, 5
sw $t0, y

lw $t0, x
lw $t1, y
add $t0, $t0, $t1
sw $t0, z

la $a0, str_literal_0
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

lw $a0, z
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall

lw $t0, x
lw $t1, y
sub $t0, $t0, $t1
sw $t0, z

la $a0, str_literal_1
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

lw $a0, z
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall

lw $t0, x
lw $t1, y
mul $t0, $t0, $t1
sw $t0, z

la $a0, str_literal_2
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

lw $a0, z
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall

lw $t0, x
lw $t1, y
div $t0, $t0, $t1
sw $t0, z

la $a0, str_literal_3
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

lw $a0, z
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall
.data
x: .word 10
y: .word 5
z: .word 0
str_literal_0: .asciiz "Addition"
str_literal_1: .asciiz "Subtraction"
str_literal_2: .asciiz "Multiplication"
str_literal_3: .asciiz "Division"