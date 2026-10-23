.text
.globl main

main:
la $t0,varl
lw $t1,0($t0)
lw $t2,4($t0)
add $t3,$t1,$t2

sw   $t3,8($t0)
li $v0,1
    move $a0,$t3
syscall
li $v0,10
syscall

.data
varl: .word 15, 35
