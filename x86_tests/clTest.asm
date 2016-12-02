section .bss
	g_val_c:	 resq 4
	g_type_c:	 resb 2
	g_val_newline:	 resb 1
	g_type_newline:	 resb 1
	g_val_temp:	 resq 1
	g_type_temp:	 resb 1
	typeBuffer resb 8
        digitBuffer resb 100
        digitSpacePos resb 8


section .text
	global _start

_start:
	mov byte [g_type_c], "a"
	mov byte [g_type_c+1], "i"
	mov byte [g_val_c+0],1
	mov byte [g_val_c+8],2
	mov byte [g_val_c+16],3
	mov byte [g_val_c+24],4
	mov byte [g_type_newline], "c"
	mov byte [g_val_newline], `\n`
	mov byte [g_type_temp], "i"
mov r9, [g_val_c+24]
mov [g_val_temp], r9
        mov r9, [g_val_c+0]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c+1]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_c+8]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c+1]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_c+16]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c+1]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_c+24]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c+1]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_newline]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_newline]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_temp]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_temp]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_newline]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_newline]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


	mov byte [g_val_temp], 9
mov r9, [g_val_temp]
mov [g_val_c+24], r9
        mov r9, [g_val_c+0]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c+1]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_c+8]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c+1]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_c+16]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c+1]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_c+24]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c+1]		;mov type to reg
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
        ;mov rbx, 10
        ;mov [rcx], rbx 
        ;inc rcx 
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

