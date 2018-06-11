# Semantics

**Pour tester :**

nasm -felf64 sortie.asm

gcc -no-pie sortie.o

./a.out *inputs*


## Explications du code

1. Grammaire

Par rapport à la grammaire de base, les *lhs* (Left Hand Side) ainsi que les *string* ont été introduits.
Les *string* sont simplement une suite de lettres délimitée par des guillemets (exemple : `"abcd"`).
Les *lhs* sont constitués des *ID* (nom de variables) et des *ID_str* (nom d'une chaine de caractères avec sélection. Exemple `chaine[2]`)
Ils apparaissent tout les deux dans les *expressions*. Ainsi on peut les utiliser sans restriction pour la commande d'assignation. Exemple : `chaine = "abcd"`, `chaine[2] = "e"` et `chaine[2] = chaine2[3]` sont possibles.

2. Arbre de Syntaxe Abstraite
3. Code assembleur

## Limites du code

1. Le code assembleur ne permet pas d'afficher à l'écran les caractères sous forme de lettres.
