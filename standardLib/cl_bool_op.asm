section .bss
	exprResolutionBuffer: 	resq 1
section .text
        global _start
_start:
	;pass

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
