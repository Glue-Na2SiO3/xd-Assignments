data segment
    prompt1 db 'number a:$'
    prompt2 db 'number b:$'
    prompt3 db 'number c:$'
    prompt4 db 'number d:$'
    result_msg db 'a+(b-c)*d=$'
    a dw 0
    b dw 0
    c dw 0
    d dw 0
    result dw 0  ; 结果存储在 result 中
data ends

code segment
    main proc 
        assume cs:code,ds:data
start: 
     mov ax,data
     mov ds,ax  
     lea dx,prompt1
     mov ah,9h
     int 21h 
     call input ; 输入 a 
     mov a,bx   
     lea dx,prompt2  
     mov ah,9h
     int 21h
     call input ; 输入 b 
     mov b,bx  
     lea dx,prompt3 
     mov ah,9h
     int 21h
     call input ; 输入 c 
     mov c,bx
     lea dx,prompt4 
     mov ah,9h
     int 21h
     call input ; 输入 d 
     mov d,bx
     lea dx,result_msg 
     mov ah,9h
     int 21h    ; 输出结果提示
     ; 计算过程 
     mov ax,b 
     sub ax,c
     mov bx,ax
     mov ax,d  
    ; 计算 (b-c)*d
     imul bx   ; 16位乘法，结果放在AX寄存器中
     add ax,a  ; 加上a
     mov result,ax
     ; 输出结果 
     test ax,8000h
     jz  print_positive   ; 如果是正数
     jnz print_negative   ; 如果是负数

print_negative: 
            mov  dl,'-'
            mov ah,02h    ; 显示输出。入口参数：AH=02H; DL=要显示的字符
            int 21h         
            mov ax,result
            neg ax 
            call print_number
            jmp exit_program

print_positive:  
            mov ax,result 
            call print_number
            jmp exit_program

print_number:
            mov di,10 ; DI = 10
            mov cx,0
convert_to_decimal:
            div di
            push dx
            inc cx
            cmp ax,0
            jne convert_to_decimal

output_number:
            pop dx
            add dl,30h
            mov ah,02h
            int 21h
            loop output_number
            ret

exit_program:
        mov ax,4c00h  ; 程序中止
        int 21h

main endp 

; 输入子程序    
input proc  
    mov bx,0  ; 清空BX
    input_loop:
        mov ah,01h ; 输入一个字符，AL等于输入的字符
        int 21h
        cmp al,0dh ; 检查是否为回车
        je input_done
        sub al,30h ; 转换为十进制 
        mov cl,4   ; 左移4位
        shl bx,cl  ; BX左移4位
        add bl,al  ; 将AL加到BX低位
        jmp input_loop
    input_done:
        call newline
        ret
input endp 

; 换行操作
newline proc 
    mov dl,0ah ; 换行
    mov ah,2h
    int 21h
    mov dl,0dh ; 回车
    mov ah,2h
    int 21h     
    ret
newline endp    

code ends
   end start
