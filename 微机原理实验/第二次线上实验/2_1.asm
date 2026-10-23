; 定义栈段，分配64个字的空间用于栈操作
STACK SEGMENT STACK
    DW 64 DUP(?)
STACK ENDS

; 定义数据段，存储ASCII码表示的数字
DATA SEGMENT
SADD DB 30H, 30H, 32H, 35H, 36H ; ASCII码表示的数字00256
DATA ENDS

; 定义代码段
CODE SEGMENT
ASSUME CS:CODE, DS:DATA ; 假设代码段地址在CS寄存器，数据段地址在DS寄存器

START:
    MOV AX, DATA ; 将数据段地址加载到AX
    MOV DS, AX    ; 将AX中的地址传递给DS，使得数据段可访问

    MOV AX, OFFSET SADD ; 将SADD数组的偏移地址加载到AX
    MOV SI, AX          ; 将SADD数组的偏移地址传递给SI，用于访问数组

    MOV BX, 000AH ; BX用于乘法操作，初始化为10（ASCII '0'的十进制值）
    MOV CX, 0004H ; 设置CX为4，用于控制循环次数（数组长度减1）
    MOV AH, 00H   ; 清零AH，用于清零高8位
    MOV AL, [SI]  ; 将数组的第一个字节加载到AL

SUB AL, 30H ; 将AL中的ASCII字符转换为对应的十进制数值

A1:
    IMUL BX ; 将AL中的数值乘以BX（10），结果存回AX
    MOV DX, [SI+01] ; 将SI指向的下一个字节加载到DX
    AND DX, 00FFH    ; 清除DX的高8位，保留低8位
    ADC AX, DX       ; 将DX加到AX，并考虑进位标志CF
    SBB AX, 30H     ; 从AX减去30H，将ASCII码转换为十进制数值
    INC SI          ; 增加SI的值，指向下一个字节
    LOOP A1         ; 减少CX的值，如果CX不为0则跳回A1

A2: ; 无限循环，用于调试时的断点
    JMP A2

CODE ENDS
END START ; 程序结束，START是程序的入口点