section .bss
	exprResolutionBuffer:	resq 1
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
_exit:
	mov rax, 60
	mov rdi, 0
	syscall
