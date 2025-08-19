# Llama
Llama is a lambda calculus REPL written fully from scratch in Python. It's capable of handling any lambda expression you would write by hand.

When you run Llama, you have the option to run it in debug mode by simply adding debug after running it.
```
$ ./llama.py debug
```
Debug mode will show the AST and the variable-resolved AST of expressions that you enter into the REPL.

---
In the REPL, you can access the help menu with the `:help` command, which will return list of commands and their functions. These commands are `:show`, `:how2`, and `church`. The functions are as follows:
|Command|Function|
|:------|:-------|
|`:show <var>`| Show the value of a variable. Alternatively, just execute :show to see all variables and their values |
|`:how2`| Shows a simple lambda calculus guide |
|`church <n>` | Converts a number to a church numeral |

