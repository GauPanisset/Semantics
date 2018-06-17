global main
extern printf, atoi
section .data
hello: db "return %d", 10, 0

e: dq "e", 0
x: dq 0
abcd: dq "abcd", 0
chaine: dq 0


section .text

main:
sub rsp, 16
mov [rsp+8], rdi
mov [rsp], rsi


mov rdx, [rsp]
mov rdi, [rdx+8]
call atoi
mov [x], rax




mov rax, abcd

mov [chaine], rax


mov rax, e

mov rbx, rax
mov rax, [chaine]
add rax, 2
mov rcx, [rbx] 
mov [rax], rcx



mov rax, [chaine]
add rax, 2

mov al, byte [rax]
mov [x], al




mov rax, [x]

mov rsi, rax
mov rdi, hello
xor rax, rax
call printf

add rsp, 16
ret
