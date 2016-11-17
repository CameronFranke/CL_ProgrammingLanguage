section .bss
	g_val_x:	 resq 1
	g_type_x:	 resb 1
	g_val_myChar:	 resb 1
	g_type_myChar:	 resb 1

section .text
	global _start

_start:
	mov word [g_val_x], 5
	mov byte [g_type_x], "i"
	mov byte [g_val_myChar], "x"
	mov byte [g_type_myChar], "c"
	mov rax, 60
	mov rdi, 0
	syscall
