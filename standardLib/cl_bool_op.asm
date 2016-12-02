section .bss
	exprResolutionBuffer: 	resq 1
section .text
        global _start
_start:
	;pass
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
