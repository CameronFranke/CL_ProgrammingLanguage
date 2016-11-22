section .bss
	g_val_c:	 resb 1
	g_type_c:	 resb 1
	g_val_d:	 resq 1
	g_type_d:	 resb 1
	typeBuffer resb 8
        digitBuffer resb 100
        digitSpacePos resb 8

	g_val_x:	 resb 1
	g_type_x:	 resb 1

section .text
	global _start

_start:
	mov byte [g_val_c], `y`
	mov byte [g_type_c], "c"
	mov byte [g_val_d], 100
	mov byte [g_type_d], "i"
        mov r9, [g_val_c]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_d]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_d]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


	mov byte [g_val_x], `\n`
	mov byte [g_type_x], "c"
        mov r9, [g_val_x]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_x]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


_exit:
	mov rax, 60
	mov rdi, 0
	syscall
_print:
._testForInt:
        mov r9b, "i"
        cmp byte [typeBuffer], r9b 
        jne ._testForChar
        mov rax, [digitBuffer]
	call ._printNum
	ret

._testForChar:
	mov r9b, "c"
        cmp byte [typeBuffer], r9b
        jne _exit
        call ._printChar
	ret

._printChar:
        mov rax, 1
        mov rdi, 1
        mov rsi, digitBuffer
        mov edx, 1 
        syscall
	ret

._printNum:
        mov rcx, digitBuffer
        mov rbx, 10
        mov [rcx], rbx 
        inc rcx 
        mov [digitSpacePos], rcx 

._printNumLoop:
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
        jne ._printNumLoop

._printNumLoop2:
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
        jge ._printNumLoop2

        ret

