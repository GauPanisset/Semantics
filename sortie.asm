global main
extern printf, atoi
section .data
hello: db "return %d", 10, 0

ghijkl: dq "ghijkl", 0
x: dq 0
abcdef: dq "abcdef", 0
chaine2: dq 0
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




mov rax, abcdef

mov [chaine], rax


mov rax, ghijkl

mov [chaine2], rax



mov rax, [chaine2]
add rax, 5

mov rbx, rax
mov rax, [chaine]
add rax, 3
mov rcx, [rbx] 
mov [rax], rcx



mov rax, [chaine]
add rax, 3

mov al, byte [rax]
mov [x], al





mov rax, [x]

mov rsi, rax
mov rdi, hello
xor rax, rax
call printf

add rsp, 16
ret
