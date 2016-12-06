section .bss
	typeBuffer resb 8
        digitBuffer resb 100
        digitSpacePos resb 8
section .text
        global _start
_start:
        mov r9, [<INSERT_VALUE>]		;mov value to reg
	mov [digitBuffer], r9			;mov reg to value buffer
	mov r9b, [<INSERT_TYPE>]		;mov type to reg
	mov byte [typeBuffer], r9b		;mov reg to type buffer
	call _print
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
