# Semantics

## Requis

* ply (pour le lexer)
* yacc (pour le parsing)
* nasm (pour l'assembleur)
* gcc (pour linker)


## Pour tester

* Ecrire le code dans `code.txt`. Sauvegarder.
* Taper : python3 semantic.py *code* où *code* est le fichier dans lequel le code à compiler est écrit
* Taper : nasm -felf64 sortie.asm ; gcc -no-pie sortie.o
* Taper : ./a.out *inputs* où les *inputs* sont les arguments du code.


## Explications du code

1. Grammaire

Par rapport à la grammaire de base, les *lhs* (Left Hand Side) ainsi que les *string* ont été introduits.
* Les *string* sont simplement une suite de lettres délimitées par des guillemets (exemple : `"abcd"`).
* Les *lhs* sont constitués des *ID* (nom de variables) et des *id_str* (nom d'une chaine de caractères avec sélection. Exemple `chaine[2]`)
Ils apparaissent tout les deux dans les *expressions*. Ainsi on peut les utiliser sans restriction pour la commande d'assignation. Exemple : `chaine = "abcd"`, `chaine[2] = "e"` et `chaine1[2] = chaine2[3]` sont possibles.

* Les *tokens* `[]` (`LCRO` et `RCRO`) ont bien sûr également été ajouté.

* Enfin, pour permettre l'usage de la fonction `len()`, le *token* `LEN` a été créé puis utilisé dans les *expressions*. Cette fonction prend en paramètre un *ID*.

2. Arbre de Syntaxe Abstraite (*AST*)

* Il n'y a que deux nouveautés à ce niveau. La première concerne les *id_str*. Ce type de mot est représenté sous forme d'un *AST* dont le type est `id_str` et le label est le nom de l'*ID* en question. Cet *AST* possède un sucsesseur représentant le *number* qui indique le caractère sélectionné.

Exemple : `chaine[2]` se traduit par `(id_str:chaine) [(number:2) []]`

* La seconde nouveauté concerne la fonction `len()`. Celle-ci se traduit simplement pour un *AST* dont le type est `len` et le label est le nom de l'*ID* entré en paramètre.

Exemple : `len(chaine)`se traduit par `(len:chaine)`

3. Code assembleur

* On attribut à chaque *string* (exemple : "abcd") une variable (i.e. une place en mémoire). Les *ID* (exemple : `chaine = "abcd"`) réprésentant des chaines de caractères contiennent donc en réalité la valeur de la case mémoire à laquelle la chaine de caractères est réellement stockée. 
Dans notre exemple la valeur de `chaine` est donc l'adresse de `abcd` qui contient la chaine `"abcd"`
Voici le bout de code assembleur correspondant à la mise en mémoire de `"abcd"` :

	abcd : dq "abcd", 0

La variable `chaine` s'initialise en revanche comme toutes les autres.

* Pour assigner une chaine de caractère à une variable (exemple : `chaine = "abcd"`), on enregistre donc simplement l'adresse de `abcd` dans `chaine`.
Voici le bout de code assembleur correspondant à `chaine = "abcd"`

	mov rax, abcd
	mov [chaine], rax

* Pour sélectionner un caractère avec un `id_str` (exemple : `chaine[2]`) on récupère l'adresse de la chaine de caractères puis on lui ajoute l'identifiant de la position du caractère sélectionné. 
Voici le bout de code assembleur correspondant à `chaine[2]`:

	mov rax, [chaine]
	add rax, 2

Ceci permet de faire des assignements où l'`id_str`est du côté gauche du signe égal. Pour sélectionner un seul caractères et l'assigner à une nouvelle variable (exemple : `x = chaine[2]`) il faut le spécifier en faisant appel aux registres d'un octet.
Voici le bout de code assembleur correspondant à `x = chaine[2]`: 

	mov rax, [chaine]
	add rax, 2
	mov al, byte [rax]
	mov [x], al

Enfin, dans le cas où l'`id_str` est au gauche et à droite du signe égal il suffit de faire successivement les deux étapes précédentes en prenant soin de retenir la première adresse.
Voici le bout de code assembleur correspondant à `chaine1[2] = chaine2[3]`:

	mov rax, [chaine1]
	add rax, 2
	mov rbx, rax
	mov rax [chaine2]
	add rax, 3
	mov al, byte [rbx]
	mov [rax], al

* La fonction `len()` repose sur le principe qu'une chaine de caractère se termine par le caractère nul. Chercher la longueur d'une chaine revient donc à trouver la position du 0 terminal. On procède donc avec une boucle `while` qui incrémente un compteur tant que le caractère considéré est différent de 0. 
Voici le bout de code assembleur correspondant à `len(chaine)` :

	mov rbx, [chaine]
	xor rdx, rdx
	while:
	mov al, byte [rbx+rdx]
	cmp al, 0
	je end
	add rdx, 1
	jmp while
	end:
	mov rax, rdx

A l'issue de ce bout de code, le registre *rax* contient la longueur de la chaine de caractère.
	


## Limites du code

1. La grammaire ne permet pas à la fonction `len()` de prendre autre chose qu'un *ID* en paramètre. Or on pourrait très bien imager qu'on souhaite calculer la longueur d'une chaine qui n'est pas associée à une variable (exemple : `len("abcd")`).

2. Le choix de la grammaire ne permet d'utiliser une expression pour définir l'indice du caractère que l'on veut sélectionner. Exemple : `chaine[1 + 1]` n'est pas reconnu. 

3. Le code assembleur ne permet pas d'afficher à l'écran les caractères sous forme de lettre.

4. Il faut nécessairement renseigner un argument pour lancer le `main`.

## Quelques exemples

Une série d'exemple on été ajouté dans le répertoir afin de pouvoir tester rapidement les différentes implémentations.

1. **Exemple1** : Cet exemple montre comment une chaine de caractère est stockée, puis comment modifier un de ses caractères. Enfin on sélectionne le caractère modifié puis on le retourne.

2. **Exemple2** : Cet exemple montre comment une chaine de caractère est stockée (même si celle-ci fait plus de 8 octets), puis comment on calcule sa longueur.

3. **Exemple3** : Cet exemple montre comment on peut modifier un caractère d'une première chaine de caractères à partir d'un caractère sélectionné dans un seconde chaine.