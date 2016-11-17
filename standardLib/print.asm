section .data
        var db 0,0 

section .bss
	typeBuffer resb 8
        digitBuffer resb 100
        digitSpacePos resb 8

        g_val_x:         resq 1
        g_type_x:        resb 1
        g_val_myChar:    resb 1
        g_type_myChar:   resb 1



section .text
        global _start

_start:

        mov word [g_val_x], 5
        mov byte [g_type_x], "i"
        mov byte [g_val_myChar], "x"
        mov byte [g_type_myChar], "c"













        mov r9, [g_val_myChar]
	mov [digitBuffer], r9
	mov r9b, [g_type_myChar]
	mov [typeBuffer], r9b

_testForInt:
        mov r9b, "i"
        cmp byte [typeBuffer], r9b 
        jne _testForChar
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
        mov rdx, 1
        syscall


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

