SSTACK SEGMENT STACK
    DW 64 DUP(?)  ; 定义栈段，预留64个DWORD空间
SSTACK ENDS

CODE SEGMENT
    ASSUME CS:CODE  ; 设置代码段寄存器

START:
    XOR AX, AX     ; 清零AX
    MOV CX, 0004H  ; 设置循环计数为4
    MOV SI, 3500H  ; SI指向BCD码数组起始地址

    ; 初始化BCD码数组
    MOV [SI], 01H
    MOV [SI+1], 02H
    MOV [SI+2], 03H
    MOV [SI+3], 04H

    ; 由于是四个二位十进制数，这里只初始化了前四个，需要补全
    MOV [SI+4], 05H
    MOV [SI+5], 06H
    MOV [SI+6], 07H
    MOV [SI+7], 08H

    MOV DI, 3510H  ; DI指向结果存储起始地址

A1:
    MOV AL, [SI]  ; 从SI指向的内存地址加载BCD码到AL
    ADD AL, AL     ; 将AL中的BCD码转换为对应的十进制数值（错误操作，应为ADD AL, '0'x）
    MOV BL, AL     ; 暂存转换后的数值
    ADD AL, AL     ; 继续错误地翻倍AL的值
    ADD AL, AL     ; 继续错误操作
    ADD AL, BL     ; 将BL的值加回AL（无意义）
    INC SI         ; 移动到下一个BCD码位置
    ADD AL, [SI]  ; 错误地将下一个BCD码加到AL
    MOV [DI], AL  ; 存储错误的结果到DI指向的地址
    INC SI         ; 错误地再次递增SI
    INC DI         ; 递增DI指向下一个存储位置
    LOOP A1        ; 循环直到CX为0

    MOV AX, 4C00H  ; 设置程序退出代码
    INT 21H        ; 调用中断，退出程序

CODE ENDS
END START