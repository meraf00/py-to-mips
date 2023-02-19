.text
li $t0, 0
sw $t0, k

loop_0:
lw $t0, k
li $t1, 10
bge $t0, $t1, endloop_0

lw $a0, k
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall


j loop_0
endloop_0:

.data
k: .word 0
