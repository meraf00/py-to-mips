.text
li $t0, 3
sw $t0, x
loop_0:
lw $t0, x
li $t1, 0
ble $t0, $t1, endloop_0

lw $a0, x
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall

lw $t0, x
li $t1, 1
sub $t0, $t0, $t1
sw $t0, x

j loop_0
endloop_0:
.data
x: .word 3