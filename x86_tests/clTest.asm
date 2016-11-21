section .bss
	g_val_a:	 resb 1
	g_type_a:	 resb 1
	g_val_b:	 resb 1
	g_type_b:	 resb 1
	g_val_c:	 resb 1
	g_type_c:	 resb 1
	g_val_d:	 resb 1
	g_type_d:	 resb 1
	g_val_e:	 resb 1
	g_type_e:	 resb 1
	g_val_f:	 resb 1
	g_type_f:	 resb 1
	g_val_g:	 resb 1
	g_type_g:	 resb 1
	g_val_h:	 resb 1
	g_type_h:	 resb 1
	g_val_i:	 resb 1
	g_type_i:	 resb 1
	g_val_j:	 resb 1
	g_type_j:	 resb 1
	g_val_k:	 resb 1
	g_type_k:	 resb 1
	g_val_l:	 resb 1
	g_type_l:	 resb 1
	typeBuffer resb 8
        digitBuffer resb 100
        digitSpacePos resb 8


section .text
	global _start

_start:
	mov byte [g_val_a], "H"
	mov byte [g_type_a], "c"
	mov byte [g_val_b], "e"
	mov byte [g_type_b], "c"
	mov byte [g_val_c], "l"
	mov byte [g_type_c], "c"
	mov byte [g_val_d], "l"
	mov byte [g_type_d], "c"
	mov byte [g_val_e], "o"
	mov byte [g_type_e], "c"
	mov byte [g_val_f], "!"
	mov byte [g_type_f], "c"
	mov byte [g_val_g], "w"
	mov byte [g_type_g], "c"
	mov byte [g_val_h], "o"
	mov byte [g_type_h], "c"
	mov byte [g_val_i], "r"
	mov byte [g_type_i], "c"
	mov byte [g_val_j], "l"
	mov byte [g_type_j], "c"
	mov byte [g_val_k], "d"
	mov byte [g_type_k], "c"
	mov byte [g_val_l], "!"
	mov byte [g_type_l], "c"
        mov r9, [g_val_a]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_a]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_b]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_b]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_c]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_c]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_d]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_d]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_e]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_e]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_f]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_f]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_g]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_g]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_h]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_h]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_i]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_i]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_j]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_j]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_k]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_k]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


        mov r9, [g_val_l]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [g_type_l]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print


_exit:
	mov rax, 60
	mov rdi, 0
	syscall
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
        mov rbx, 10
        mov [rcx], rbx 
        inc rcx 
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

