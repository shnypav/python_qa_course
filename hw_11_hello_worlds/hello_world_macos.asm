section .data
    log_start db "[INFO] Program started", 10
    log_start_len equ $ - log_start
    log_done db "[INFO] Greeting printed", 10
    log_done_len equ $ - log_done
    prompt db "What is your name? ", 0
    greeting db "Hello, %s!", 10, 0

section .bss
    name resb 100

section .text
    global _main
    extern _write
    extern _printf
    extern _fgets
    extern ___stdinp

_main:
    push rbp
    mov rbp, rsp

    mov edi, 2                  ; stderr
    lea rsi, [rel log_start]
    mov edx, log_start_len
    call _write

    ; Print the prompt.
    lea rdi, [rel prompt]
    xor eax, eax
    call _printf

    ; Read a line from standard input.
    lea rdi, [rel name]
    mov esi, 100
    ; macOS defines stdin as __stdinp; load the FILE pointer through the GOT.
    mov rax, [rel ___stdinp wrt ..gotpcrel]
    mov rdx, [rax]
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

    mov edi, 2
    lea rsi, [rel log_done]
    mov edx, log_done_len
    call _write

.done:
    xor eax, eax
    pop rbp
    ret
