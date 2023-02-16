.text
li $t0, 3
sw $t0, x

li $t0, 4
sw $t0, x


li $a0, 2
li $v0, 1
syscall
.data
x: .word 3