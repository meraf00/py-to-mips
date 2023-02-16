.text
lw $t0, x
li $t1, 1
beq $t0, $t1, label_0

la $a0, str_literal_0
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

label_0:
.data
str_literal_0: .word 0