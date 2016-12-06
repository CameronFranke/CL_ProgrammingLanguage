section .bss
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

_cl_greater_than:
        cmp r13b, "i"	;type check
        jne ._set_not_greater ;return 0 on failed type check 
        cmp r11, r12
        jg ._set_greater
	ret 
._set_greater:
        mov qword [exprResolutionBuffer], 1
        ret
._set_not_greater:
	mov qword [exprResolutionBuffer], 0
        ret

_cl_less_than:
        cmp r13b, "i"   ;type check
        jne ._set_not_less ;return 0 on failed type check 
        cmp r11, r12
        jl ._set_less
        ret
._set_less:
        mov qword [exprResolutionBuffer], 1
        ret
._set_not_less:
        mov qword [exprResolutionBuffer], 0
        ret

_cl_greater_than_or_equal:
        cmp r13b, "i"                   ;type check
        jne ._set_not_greater_or_equal     ;return 0 on failed type check 
        cmp r11, r12
        jge ._set_greater_or_equal
        ret
._set_greater_or_equal:
        mov qword [exprResolutionBuffer], 1
        ret
._set_not_greater_or_equal:
        mov qword [exprResolutionBuffer], 0
        ret

_cl_less_than_or_equal:
        cmp r13b, "i"   		;type check
        jne ._set_not_less_or_equal 	;return 0 on failed type check 
        cmp r11, r12
        jle ._set_less_or_equal
        ret
._set_less_or_equal:
        mov qword [exprResolutionBuffer], 1
        ret
._set_not_less_or_equal:
        mov qword [exprResolutionBuffer], 0
        ret
