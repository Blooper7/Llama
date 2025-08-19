# Llama
Llama is a lambda calculus REPL written fully from scratch in Python. It's capable of handling any lambda expression you would write by hand.

When you run Llama, you have the option to run it in debug mode by simply adding debug after running it.
```
$ ./llama.py debug
```
Debug mode will show the AST and the variable-resolved AST of expressions that you enter into the REPL.

---
## About the REPL
In the REPL, you can access the help menu with the `:help` command, which will return list of commands and their functions. These commands are `:show`, `:how2`, and `church`. The functions are as follows:
|Command|Function|
|:------|:-------|
|`:show <var>`| Show the value of a variable. Alternatively, just execute :show to see all variables and their values |
|`:how2`| Shows a simple lambda calculus guide |
|`church <n>` | Converts a number to a church numeral |

A note on variable naming: currently, this resolves all variables before reducing (eta reduction). This means that if you define a function `F:=\x.\y.`, then define another function `G:=\x.F x 1`, it won't reduce like you want it to. For example, if you define `SUCC:=\x.ADD x 1` (using the built-in ADD function) and run `SUCC 3`, you'll get `(\f. (\x. ((x f) (f x))))` instead of 4, because ADD uses x. If I have time, I'll fix that.

---
## Included Features
So far, Llama includes the following:
- Expression evaluation
- Variable assignment
- Beta reduction

## Future Features
In the future, I will add:
- Infix operators, such as +, -, *, and /.
- Typing
- Alpha renaming
