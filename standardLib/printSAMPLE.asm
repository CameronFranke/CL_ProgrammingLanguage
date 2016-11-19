section .data
        var db 0,0 

section .bss
	typeBuffer resb 8
        digitBuffer resb 100
        digitSpacePos resb 8

        g_val_x:         resq 1
        g_type_x:        resb 1
        g_val_y:    resb 1
        g_type_y:   resb 1



section .text
        global _start

_start:

        mov word [g_val_x], 598
        mov byte [g_type_x], "i"
        mov byte [g_val_y], "x"
        mov byte [g_type_y], "c"













        mov r9, [g_val_x] 			;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_x]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer

_testForInt:
        mov r9b, "i"
        cmp byte [typeBuffer], r9b 
        jne _testForChar
        mov rax, [digitBuffer]
	call _printNum

_testForChar:
	mov r9b, "c"
        cmp byte [typeBuffer], r9b
        jne _exit
        call _printChar

_exit:

        mov rax, 60
        mov rdi, 0
        syscall

_printChar:
        mov rax, 1
        mov rdi, 1
        mov rsi, digitBuffer
        mov edx, 1 
        syscall
	ret

_printNum:
        mov rcx, digitBuffer
        mov rbx, 10
        mov [rcx], rbx 
        inc rcx 
        mov [digitSpacePos], rcx 

_printNumLoop:
        mov rdx, 0
        mov rbx, 10
	div rbx
        push rax
        add rdx, 48

        mov rcx, [digitSpacePos]
        mov [rcx], dl
        inc rcx
        mov [digitSpacePos], rcx

        pop rax
        cmp rax, 0
        jne _printNumLoop

_printNumLoop2:
        mov rcx, [digitSpacePos]

        mov rax, 1
        mov rdi, 1
        mov rsi, rcx
        mov rdx, 1
        syscall

        mov rcx, [digitSpacePos]
        dec rcx
        mov [digitSpacePos], rcx

        cmp rcx, digitBuffer
        jge _printNumLoop2

        ret

