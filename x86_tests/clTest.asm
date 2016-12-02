section .bss
	g_val_a:	 resq 6
	g_type_a:	 resb 2
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
	mov byte [g_type_a], "a"
	mov byte [g_type_a+1], "i"
	mov byte [g_val_a+0],1
	mov byte [g_val_a+8],1
	mov byte [g_val_a+16],2
	mov byte [g_val_a+24],3
	mov byte [g_val_a+32],5
	mov byte [g_val_a+40],8
	mov byte [g_type_d], "i"
	mov byte [g_type_newline], "c"
	mov byte [g_val_newline], `\n`
	mov r11, [g_val_a+0];mov op1 to reg
	mov r12, [g_val_a+8];mov op2 to reg
	mov r13, [g_type_a+1]; mov op1 type to reg
	call _cl_is_not_equal
	mov r11, [exprResolutionBuffer]
	mov qword [g_val_d], r11
        mov r9, [g_val_d]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_d]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_newline]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_newline]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


	mov r11, [g_val_a+8];mov op1 to reg
	mov r12, [g_val_a+16];mov op2 to reg
	mov r13, [g_type_a+1]; mov op1 type to reg
	call _cl_is_equal
	mov r11, [exprResolutionBuffer]
	mov qword [g_val_d], r11
        mov r9, [g_val_d]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_d]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_newline]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_newline]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


	mov r11, [g_val_a+16];mov op1 to reg
	mov r12, [g_val_a+40];mov op2 to reg
	mov r13, [g_type_a+1]; mov op1 type to reg
	call _cl_is_not_equal
	mov r11, [exprResolutionBuffer]
	mov qword [g_val_d], r11
        mov r9, [g_val_d]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_d]		;mov type to reg
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
	cmp r13b, "i"
	je ._int 	
	cmp r13b, "c"
	je ._char	

._int:
	cmp r11, r12
	je ._set_true_i 
	jne ._set_false_i	
._set_true_i:
	mov qword [exprResolutionBuffer], 1
	ret	
._set_false_i:
	mov qword [exprResolutionBuffer], 0
	ret

._char:
        cmp r11b, r12b
        je ._set_true_c
        jne ._set_false_c
._set_true_c:
        mov qword [exprResolutionBuffer], 1
        ret
._set_false_c:
        mov qword [exprResolutionBuffer], 0
        ret


_cl_is_not_equal:
        cmp r13b, "i"
        je ._int
        cmp r13b, "c"
        je ._char

._int:
        cmp r11, r12
        je ._set_not_true_i
        jne ._set_not_false_i
._set_not_true_i:
        mov qword [exprResolutionBuffer], 0
        ret
._set_not_false_i:
        mov qword [exprResolutionBuffer], 1
        ret

._char:
        cmp r11b, r12b
        je ._set_not_true_c
        jne ._set_not_false_c
._set_not_true_c:
        mov qword [exprResolutionBuffer], 0
        ret
._set_not_false_c:
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

