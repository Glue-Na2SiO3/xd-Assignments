data segment
    str1 db 'please input a:$'  ; 提示输入a的字符串
    str2 db 'please input b:$'  ; 提示输入b的字符串
    str3 db 'result c = a*b =$'               ; 输出结果的字符串
    a dw ?  ; 定义变量a，字类型
    b dw ?  ; 定义变量b，字类型
    c dw ?  ; 定义变量c，字类型
data ends

code segment
assume cs:code,ds:data
    main proc far
    start:
        mov ax,data
        mov ds,ax
        lea dx,str1  ; 输出提示信息str1
        mov ah,9h
        int 21h
        call input  ; 调用input过程输入a
        mov a,bx     ; 将输入的a保存到a中
        lea dx,str2  ; 输出提示信息str2
        mov ah,9h
        int 21h
        call input  ; 调用input过程输入b
        mov b,bx     ; 将输入的b保存到b中
        lea dx,str3  ; 输出提示信息str3
        mov ah,9h
        int 21h
        mov ax,a
        aad
        mov bx,ax
        mov ax,b
        aad
        mul bx                   ; ax = a*b
        mov word ptr c,ax   ; 将结果c保存到c中
        mov di,0ah             ; di = 10
        mov cx,0
    ToTen:  ; 将结果转换为十进制
        div di
        push dx
        inc cx
        cmp ax,0
        je print
        cwd
        jmp ToTen
    print:  ; 输出结果
        pop dx
        add dl,30h
        mov ah,2h
        int 21h
    loop print
        mov ah,00h
        int 21h
    main endp
    input proc
        mov bx,0
        inputa:
        mov ah,1    ; 读取第一个字符
        int 21h
        sub al,30h
        mov bl,al
        mov ah,1        ; 读取第二个字符
        int 21h
        cmp al,0dh  ; 比较是否按下Enter键
        je exit
        sub al,30h
        mov cl,8     ; 设定位移操作
        rol bx,cl
        mov bl,al
        jmp exit
    exit:
        call crlf
        ret
    input endp

    ; 输出换行
    crlf proc near
        mov dl,0ah
        mov ah,2h
        int 21h
        mov dl,0dh
        mov ah,2h
        int 21h
        ret
    crlf endp
code ends
    end start
