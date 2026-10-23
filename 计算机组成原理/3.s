.text
.globl main

main:
    la $t0, varl
    lw $t1, 0($t0)
    lw $t2, 4($t0)
    lw $t3, 8($t0)
    add $t4, $t1, $t2
    add $t5, $t4, $t3
    sw $t5, 12($t0)
    li $v0, 1
    move $a0, $t5
    syscall

    li $v0, 10
    syscall

.data
    varl:.word 10, 20, 30