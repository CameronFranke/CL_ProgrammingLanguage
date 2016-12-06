section .bss
section .text
        global _start
_start:
	;operands to need to be loaded to r11 and r12
_cl_addition:
	add r11, r12
	mov qword [exprResolutionBuffer], r11
	ret
_cl_subtraction:
	sub r11, r12
	mov qword [exprResolutionBuffer], r11
        ret
_cl_multiplication:
	mov rax, r11
	mul r12
	mov qword [exprResolutionBuffer], rax
        ret
_cl_division:
	xor rdx, rdx
	mov qword [exprResolutionBuffer], rax
        mov rax, r11	
	div r12
        mov word [exprResolutionBuffer], ax
	ret		
