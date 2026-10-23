IO0 EQU 0168H
CODE SEGMENT
    ASSUME CS:CODE
START:
	MOV DX,IO0
    MOV AL,00H   ;数码管显示0
    OUT DX,AL
    MOV CX,0E000H
    LOOP $
    MOV AL,01H   ;数码管显示1
    OUT DX,AL
    MOV CX,0E000H
    LOOP $	
    MOV AL,02H   ;数码管显示2
    OUT DX,AL
    MOV CX,0E000H
    LOOP $	
    MOV AL,03H    ;数码管显示3
    OUT DX,AL
    MOV CX,0E000H
    LOOP $	
    MOV AL,04H    ;数码管显示4
    OUT DX,AL
    MOV CX,0E000H
    LOOP $	
    MOV AL,05H    ;数码管显示5
    OUT DX,AL
    MOV CX,0E000H
    LOOP $	
    MOV AL,06H    ;数码管显示6
    OUT DX,AL
    MOV CX,0E000H
    LOOP $	
    MOV AL,07H    ;数码管显示7
    OUT DX,AL
    MOV CX,0E000H
    LOOP $	
	MOV AL,08H    ;数码管显示8
    OUT DX,AL
    MOV CX,0E000H
    LOOP $	
	MOV AL,09H    ;数码管显示9
    OUT DX,AL
    MOV CX,0E000H
    LOOP $
    JMP START
ENDLESS:
    JMP ENDLESS
CODE ENDS
    END START
