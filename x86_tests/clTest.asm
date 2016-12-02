section .bss
	g_val_a:	 resq 1
	g_type_a:	 resb 1
	g_val_b:	 resq 1
	g_type_b:	 resb 1
	g_val_c:	 resq 1
	g_type_c:	 resb 1
	g_val_d:	 resq 1
	g_type_d:	 resb 1
	g_val_newline:	 resb 1
	g_type_newline:	 resb 1
	exprResolutionBuffer: 	resq 1
	typeBuffer resb 8
        digitBuffer resb 100
        digitSpacePos resb 8


section .text
	global _start

_start:
	mov byte [g_type_a], "i"
	mov word [g_val_a], 5
	mov byte [g_type_b], "i"
	mov word [g_val_b], 10
	mov byte [g_type_c], "i"
	mov word [g_val_c], 10
	mov byte [g_type_d], "i"
	mov byte [g_type_newline], "c"
	mov byte [g_val_newline], `\n`
	mov r11b, [g_val_c];mov op1 to reg
	mov r12b, [g_val_b];mov op2 to reg
	call _cl_is_equal
	mov r11, [exprResolutionBuffer]
	mov qword [g_val_d], r11
        mov r9, [g_val_d]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_d]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


	mov r11b, [g_val_c];mov op1 to reg
	mov r12b, [g_val_b];mov op2 to reg
	call _cl_is_equal
	mov r11, [exprResolutionBuffer]
	mov qword [g_val_a], r11
        mov r9, [g_val_a]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_a]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_newline]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_newline]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


_exit:
	mov rax, 60
	mov rdi, 0
	syscall
_cl_is_equal:
	cmp r11, r12
	je ._set_true 
	jne ._set_false	
._set_true:
	mov qword [exprResolutionBuffer], 1
	ret	
._set_false:
	mov qword [exprResolutionBuffer], 0
	ret
_cl_is_not_equal:
        cmp r11, r12
        je ._set_not_true
        jne ._set_not_false
._set_not_true:
        mov qword [exprResolutionBuffer], 0
        ret
._set_not_false:
        mov qword [exprResolutionBuffer], 1
        ret
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

