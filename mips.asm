.text


li $t0, 10
sw $t0, i
lw $t7, i
li $t8, 20
lw $t9, -

loop_0:

blt $t9, $zero, decreasing_0
bge $t7, $t8, end_loop_0
j end_guard_0

decreasing_0:
ble $t7, $t8, end_loop_0
end_guard_0:
        
lw $a0, i
li $v0, 1
syscall
li $a0, 10
li $v0, 11
syscall


add $t7, $t7, $t9
sw $t7, i
j loop_0
end_loop_0:
.data
i: .word 10