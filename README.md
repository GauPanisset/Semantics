# Semantics

## Requis

* ply (pour le lexer)
* yacc (pour le parsing)
* nasm (pour l'assembleur)
* gcc (pour linker)


## Pour tester

* Ecrire le code dans code.txt. Sauvegarder.
* Taper : python3 whyle_2018.py.
* Taper : nasm -felf64 sortie.asm ; gcc -no-pie sortie.o
* Taper : ./a.out *inputs* où les *inputs* sont les arguments du code.


## Explications du code

1. Grammaire

Par rapport à la grammaire de base, les *lhs* (Left Hand Side) ainsi que les *string* ont été introduits.
Les *string* sont simplement une suite de lettres délimitée par des guillemets (exemple : `"abcd"`).
Les *lhs* sont constitués des *ID* (nom de variables) et des *id_str* (nom d'une chaine de caractères avec sélection. Exemple `chaine[2]`)
Ils apparaissent tout les deux dans les *expressions*. Ainsi on peut les utiliser sans restriction pour la commande d'assignation. Exemple : `chaine = "abcd"`, `chaine[2] = "e"` et `chaine[2] = chaine2[3]` sont possibles.

Les *tokens* `[]` (`LCRO` et `RCRO`) ont bien sûr également été ajouté.

Enfin, pour permettre l'usage de la fonction `len()`, le *token* `LEN` a été créé puis utilisé dans les *expressions*. Cette fonction prend en paramètre un *ID*.

2. Arbre de Syntaxe Abstraite (*AST*)

Il n'y a que deux nouveautés à ce niveau. La première concerne les *id_str*. Ce type de mot est représenté sous forme d'un *AST* dont le type est `id_str` et le label est le nom de l'*ID* en question. Cet *AST* possède un sucsesseur représentant le *number* qui indique le caractère sélectionné.

Exemple : `chaine[2]` se traduit par `(id_str:chaine) [(number:2) []]`

La seconde nouveauté concerne la fonction `len()`. Celle-ci se traduit simplement pour un *AST* dont le type est `len` et le label est le nom de l'*ID* entré en paramètre.

Exemple : `len(chaine)`se traduit par `(len:chaine)`

3. Code assembleur




## Limites du code

1. La grammaire ne permet pas à la fonction `len()` de prendre autre chose qu'un *ID* en paramètre. Or on pourrait très bien imager qu'on souhaite calculer la longueur d'une chaine qui n'est pas associé à une variable (exemple : `len("abcd")`).

2. Le choix de l'*AST* ne permet d'utiliser une expression pour définir l'indice du caractère que l'on veut sélection. Exemple : `chaine[1 + 1]` n'est pas reconnu. 

3. Le code assembleur ne permet pas d'afficher à l'écran les caractères sous forme de lettres.

## Quelques exemples