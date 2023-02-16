.text
#
la $a0, str_literal_0
li $v0, 4
syscall
li $a0, 10
li $v0, 11
syscall

##.data
str_literal_0: .word 0