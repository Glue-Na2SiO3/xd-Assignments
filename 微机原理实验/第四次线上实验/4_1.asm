START:
    MOV DX, 0001H
    MOV BX, 0002H
NEXT1:
    MOV AL, BL
    INC BL
    MUL BL
    ADD DX, AX
    CMP AX, 00C8H          
    JNA NEXT1

    SUB DX, AX           
    MOV AX, DX
    MOV DX, 0000H
    MOV DI, 0AH
    MOV CX, 0
    ToTen:
    DIV DI
    PUSH DX
    INC CX
    CMP AX, 0
    JE NEXT
    CWD
    JMP ToTen
NEXT:
    POP DX
    ADD DL, 30H
    MOV AH, 2H
    INT 21H
    LOOP NEXT
END START