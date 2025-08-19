splashText="""
           [[ Llama ]]
A minimalist lambda calculus REPL
      Type ':help' for help
"""

helpText=r"""
Llama is a simple lambda calculus REPL

Don't worry about typing lambdas. The interpreter isn't meant to handle that anyway. Just type '\'!

Available commands:
     :help       | You're here!
 :show <varname> | Show a variable. Alternatively, just execute :show to see all variables
     :how2       | Shows a simple lambda calculus guide
   :church <n>   | Displays the church numberal for any number
     :quit       | Leave the REPL
"""

lambdaCalculus=r"""
So, you want to learn the ropes?
You asked for it...

Here's an example lambda: \x. x
That's basically the same as f(x)=x

Here's an example two-argument lambda: \x.\y. x
(That's equivalent to f(x,y)=x

But wait, how do you call them if they don't have names? Well, in normal lambda calculus, you don't call them. You would simply write (\x. x) 3 to apply the function to 3. Cool, right?

Boiling it down, it's really simple. You have essentially four different concepts:
1. Functions, the basis of all lambda calculus
2. Applications, or how functions are applied to other functions
3. Reductions, or how you really "solve" a function

Functions and applications are pretty self-explanatory, but "reductions" seems intimidating at first glance. Don't worry about it so much. If you've done any kind of algebra, you've done beta-reductions before, which is all I'm going to teach you.
Basically, a beta-reduction is substitution.
If we define f(x)=2x+1, then apply f to the number 5 via f(5), we get f(5)=2(5)+1. Boom. Beta-reduction.

That's basically it!

Oh, another thing: functions are able to be passed around as arguments. That'll probably be important for logic.

Here's an example:
TRUE := \x.\y.x
FALSE := \x.\y.y

These past two functions act as selectors between x and y. But why is that important? Well, take a look at a definition of logical NOT:
NOT := \b.b FALSE TRUE

Now, to use it, we simply do "NOT TRUE" or "NOT FALSE"

Let's break it down.
If we plug in TRUE to not, we get this function:
\TRUE.TRUE FALSE TRUE

Looks like a bunch of junk, huh? Let me restrucure it in a more friendly notation for you:
NOT(TRUE)=TRUE(FALSE, TRUE)

Now, if we think back to our earlier definition of TRUE, we can see that TRUE takes in two items and selects the first. So let's see what this gets us:
NOT(TRUE)=FALSE

Perfect!

Now that you have a basic understanding, go nuts! Lambda calculus has a lot to offer you!
"""
