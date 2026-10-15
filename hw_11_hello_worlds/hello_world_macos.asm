section .data
    prompt db "What is your name? ", 0
    greeting db "Hello, %s!", 10, 0

section .bss
    name resb 100

section .text
    global _main
    extern _printf
    extern _fgets
    extern _stdin

_main:
    push rbp
    mov rbp, rsp

    ; Print the prompt.
    lea rdi, [rel prompt]
    xor eax, eax
    call _printf

    ; Read a line from standard input.
    lea rdi, [rel name]
    mov esi, 100
    mov rdx, [rel _stdin]
    call _fgets
    test rax, rax
    jz .done

    ; Replace the line ending with a null terminator.
    lea r8, [rel name]
.trim:
    cmp byte [r8], 0
    je .greet
    cmp byte [r8], 10
    je .remove_newline
    inc r8
    jmp .trim
.remove_newline:
    mov byte [r8], 0

.greet:
    lea rdi, [rel greeting]
    lea rsi, [rel name]
    xor eax, eax
    call _printf

.done:
    xor eax, eax
    pop rbp
    ret
