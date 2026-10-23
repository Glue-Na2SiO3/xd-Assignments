.data
stack_size: .word 100  # 栈大小，可根据实际需求调整
stack: .space 400  # 栈空间
top: .word 0  # 栈顶指针初始化为0
input_buffer: .space 200  # 输入缓冲区，存放用户输入的中缀表达式
postfix_buffer: .space 200  # 后缀表达式缓冲区，用于转换后的结果存放
result: .word 0  # 用于存储最终计算结果

# 操作符优先级表，使用ASCII码作为索引，存储优先级值
op_priority: .byte 0, 1, 2, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

.text
main:
    jal read_input
    la $a0, input_buffer
    la $a1, postfix_buffer
    jal infix_to_postfix
    la $s0, postfix_buffer
    jal evaluate_postfix
    lw $t2, result
    li $v0, 1
    move $a0, $t2
    syscall
    li $v0, 10
    syscall

read_input:
    li $v0, 8
    la $a0, input_buffer
    li $a1, 200  # 允许输入的最大字符数（包括字符串结束符'\0'）
    syscall
    jr $ra

infix_to_postfix:
    move $t0, $a0
    move $t1, $a1

infix_loop:
    lb $t2, ($t0)
    beq $t2, '\0', end_infix_loop
    blt $t2, '0', is_operator
    bgt $t2, '9', is_operator
    sb $t2, ($t1)
    addi $t1, $t1, 1
    addi $t0, $t0, 1
    j infix_loop

is_operator:
    la $t3, op_priority
    addi $t5, $t2, -45  # 将操作符ASCII码转换为索引，'-' 为 45，所以减去 45 得到 0-based 索引
    lbu $t4, ($t3 + $t5)
    beq $t2, '(', push_operator
    beq $t2, ')', pop_until_left_paren
    j push_operator

push_operator:
    addi $sp, $sp, -4
    sw $t2, 4($sp)  # 将操作符压入栈中
    j infix_loop

pop_until_left_paren:
    addi_loop:
        addi $sp, $sp, 4
        lw $t4, 4($sp)
        beq $t4, '(', continue_infix_loop
        sb $t4, ($t1)
        addi $t1, $t1, 1
        j addi_loop

continue_infix_loop:
    j infix_loop

end_infix_loop:
pop_all_operators:
    lw $t4, 4($sp)
    beq $t4, $zero, end_infix
    sb $t4, ($t1)
    addi $t1, $t1, 1
    j pop_all_operators

end_infix:
    sb $zero, ($t1)  # 在后缀表达式末尾添加字符串结束符
    jr $ra

evaluate_postfix:
    move $t0, $s0

evaluate_loop:
    lb $t2, ($t0)
    beq $t2, '\0', end_evaluate_loop
    blt $t2, '0', is_operator_evaluate
    bgt $t2, '9', is_operator_evaluate
    addi $t4, $t2, -48  # 将ASCII码转换为整数
    addi $sp, $sp, -4
    sw $t4, 4($sp)  # 将数字压入栈中
    addi $t0, $t0, 1
    j evaluate_loop

is_operator_evaluate:
    lw $t3, 4($sp)  # 弹出两个操作数
    lw $t4, 8($sp)
    lw $t5, 12($sp)
    sw $t3, 8($sp)  # 将第一个操作数放入正确的位置
    sw $t5, 4($sp)  # 将第二个操作数放入正确的位置
    beq $t2, '+', add_operation
    beq $t2, '-', sub_operation
    beq $t2, '*', mul_operation
    beq $t2, '/', div_operation
    j evaluate_loop

add_operation:
    add $t6, $t4, $t3
    sw $t6, 4($sp)  # 将结果压回栈中
    jr $ra

sub_operation:
    sub $t6, $t4, $t3
    sw $t6, 4($sp)
    jr $ra

mul_operation:
    mult $t4, $t3
    mflo $t6
    sw $t6, 4($sp)
    jr $ra

div_operation:
    beq $t3, $zero, div_zero_error
    div $t4, $t3
    mflo $t6
    sw $t6, 4($sp)
    jr $ra

div_zero_error:
    # 处理除以零的错误
    li $v0, 10  # 退出程序
    syscall
    jr $ra

end_evaluate_loop:
    lw $t2, 4($sp)  # 获取栈顶元素作为结果
    sw $t2, result
    jr $ra