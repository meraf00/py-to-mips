.text
li $t0, 3
sw $t0, x
lw $t0, x
li $t1, 2
bne $t0, $t1, label_0

la $a0, str_literal_0
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

j else_label_0

label_0:

lw $t0, x
li $t1, 1
bne $t0, $t1, label_1

la $a0, str_literal_1
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

j else_label_0

label_1:


la $a0, str_literal_2
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

else_label_0:.data
x: .word 3
str_literal_0: .asciiz "If statement"
str_literal_1: .asciiz "Elif statement"
str_literal_2: .asciiz "Else statement"