section .bss
section .text
        global _start
_start:
	;operands to need to be loaded to r11 and r12
_cl_addition:
	add r11, r12
	mov qword [exprResolutionBuffer], r11
	ret
		
