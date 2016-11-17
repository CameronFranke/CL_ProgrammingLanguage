section .data
	var db 0,0 

section .bss
	digitSpace resb 100
	digitSpacePos resb 8
	printBuffer resb 8
	x:       resw 2
     	y:	 resb 1

	g_val_x:         resq 1
        g_type_x:        resb 1
        g_val_myChar:    resb 1
        g_type_myChar:   resb 1



section .text
	global _start

_start:

	mov word [g_val_x], 5
        mov byte [g_type_x], "i"
        mov byte [g_val_myChar], "x"
        mov byte [g_type_myChar], "c"


	mov word [x], 10
	mov word [x+2], 9876


	mov r9, [x]
	mov [printBuffer], r9
	call _printChar
	
	mov rax, [x+1]
	call _printNum 

	mov r9, [g_val_myChar]
	mov [printBuffer], r9
	;mov [digitSpace], r9
	;mov rax, [g_val_x]

	;mov r9b, 5
	;cmp byte [g_val_x], r9b
	;jne _test
	mov rax, 123;[digitSpace]
	call _printNum

_test:

	mov rax, 60
	mov rdi, 0
	syscall

_printChar:
	mov rax, 1
	mov rdi, 1
	mov rsi, printBuffer
	mov rdx, 1
	syscall


_printNum:
	mov rcx, digitSpace
	mov rbx, 10
	mov [rcx], rbx
	inc rcx
	mov [digitSpacePos], rcx

_printNumLoop:
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
	jne _printNumLoop

_printNumLoop2:
	mov rcx, [digitSpacePos]

	mov rax, 1
	mov rdi, 1
	mov rsi, rcx
	mov rdx, 1
	syscall

	mov rcx, [digitSpacePos]
	dec rcx
	mov [digitSpacePos], rcx

	cmp rcx, digitSpace
	jge _printNumLoop2

	ret



