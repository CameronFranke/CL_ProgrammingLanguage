
section .text
	global _start

_start:
_exit:
	mov rax, 60
	mov rdi, 0
	syscall
