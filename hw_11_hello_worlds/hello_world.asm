section .data
    prompt  db "What is your name? "
    prompt_len equ $ - prompt
    greeting db "Hello, "
    greeting_len equ $ - greeting
    exclamation db "!"
    newline db 10

section .bss
    name resb 100

section .text
    global _start

_start:
    ; Print the prompt
    mov eax, 1                  ; sys_write
    mov edi, 1                  ; stdout
    mov rsi, prompt
    mov edx, prompt_len
    syscall

    ; Read the name
    mov eax, 0                  ; sys_read
    mov edi, 0                  ; stdin
    mov rsi, name
    mov edx, 100
    syscall
    test rax, rax
    jle .exit
    mov r12, rax                ; number of bytes read

    ; Remove the trailing newline, if present
    cmp byte [name + r12 - 1], 10
    jne .print
    dec r12

.print:
    ; Print "Hello, "
    mov eax, 1
    mov edi, 1
    mov rsi, greeting
    mov edx, greeting_len
    syscall

    ; Print the name
    mov eax, 1
    mov edi, 1
    mov rsi, name
    mov rdx, r12
    syscall

    ; Print the exclamation mark
    mov eax, 1
    mov edi, 1
    mov rsi, exclamation
    mov edx, 1
    syscall

    ; Print a newline
    mov eax, 1
    mov edi, 1
    mov rsi, newline
    mov edx, 1
    syscall

.exit:
    mov eax, 60                 ; sys_exit
    xor edi, edi
    syscall
