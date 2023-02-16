.text

la $a0, x
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

li $t0, 35
sw $t0, y
lw $a0, y
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall
.data
x: .asciiz "apple"
y: .word 35