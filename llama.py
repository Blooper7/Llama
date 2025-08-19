from parsing import Parser, tokenize
import texts

def flatten(expr):
    # Returns a list of all nodes for 'in' checks
    kind=expr[0]
    if kind=='var':
        return [expr]
    elif kind in ('lambda','app'):
        return [expr]+flatten(expr[1])+flatten(expr[2])
    else:
        return [expr]


def make_church_number(n):
	f=('var','f')
	x=('var','x')
	result=x
	for _ in range(n):
		result=('app',f,result)
	return ('lambda','f',('lambda','x',result))

def detect_church_num(expr):
    if expr[0]!='lambda': return None
    f=expr[1]
    inner=expr[2]
    if inner[0]!='lambda': return None
    x=inner[1]
    body=inner[2]

    if ('var', f) not in flatten(body):
    	return None

    # Count how many times 'f' is applied to something
    count=0
    current=body
    while current[0]=='app' and current[1]==('var',f):
        count+=1
        current=current[2]

    if current==('var', x):
        return count
    return None

def substitute(expr, var_name, value):
    kind=expr[0]
    if kind=='var':
        if expr[1]==var_name:
            return value
        else:
            return expr
    elif kind=='lambda':
        arg,body=expr[1],expr[2]
        if arg==var_name:
            return expr  # Don't substitute inside shadowed var
        else:
            return ('lambda',arg,substitute(body,var_name,value))
    elif kind=='app':
        return ('app',substitute(expr[1],var_name,value),substitute(expr[2],var_name,value))
    else:
        return expr

def beta_reduce(expr):
    kind=expr[0]
    
    if kind=='var':
        return expr
    
    elif kind=='lambda':
        arg,body=expr[1],expr[2]
        return ('lambda',arg,beta_reduce(body))

    elif kind=='app':
        func=beta_reduce(expr[1])
        arg=beta_reduce(expr[2])
        
        if func[0]=='lambda':
            # Apply the function to the argument
            param=func[1]
            body=func[2]
            result=substitute(body,param,arg)
            return beta_reduce(result)
        else:
            return ('app',func,arg)

    else:
        return expr

env={
	"ADD":('lambda', 'm', ('lambda', 'n', ('lambda', 'f', ('lambda', 'x', ('app', ('app', ('var', 'm'), ('var', 'f')), ('app', ('app', ('var', 'n'), ('var', 'f')), ('var', 'x'))))))),
	"MULT":('lambda', 'm', ('lambda', 'n', ('lambda', 'f', ('app', ('var', 'm'), ('app', ('var', 'n'), ('var', 'f')))))),
	"TRUE":('lambda', 'x', ('lambda', 'y', ('var', 'x'))),
	"FALSE":('lambda', 'x', ('lambda', 'y', ('var', 'y'))),
	"AND":('lambda', 'a', ('lambda', 'b', ('app', ('app', ('var', 'a'), ('var', 'b')), ('var', 'FALSE')))),
	"OR":('lambda', 'a', ('lambda', 'b', ('app', ('app', ('var', 'a'), ('var', 'a')), ('var', 'b')))),
	"XOR":('lambda', 'a', ('lambda', 'b', ('app', ('app', ('var', 'a'), ('app', ('var', 'NOT'), ('var', 'b'))), ('var', 'b')))),
	"NOT":('lambda', 'b', ('app', ('app', ('var', 'b'), ('var', 'FALSE')), ('var', 'TRUE')))
}

block_back_ref=False

def pretty(expr, ign_church=False):
    num=detect_church_num(expr)
    if num is not None and not ign_church:
    	return str(num)
    
    kind=expr[0]
    if kind=='var':
        return expr[1]
    elif kind=='lambda':
        arg=expr[1]
        body=expr[2]
        return f"(\\{arg}. {pretty(body)})"
    elif kind=='app':
        f=pretty(expr[1])
        x=pretty(expr[2])
        return f"({f} {x})"
    else:
        return str(expr)

# Recursively resolve named variables from env
def resolve_env(expr):
    kind = expr[0]
    if kind == 'var':
        name = expr[1]
        if name in env:
            return resolve_env(env[name])
        elif name.isdigit():
            return make_church_number(int(name))
        else:
            return expr
    elif kind == 'lambda':
        return ('lambda', expr[1], resolve_env(expr[2]))
    elif kind == 'app':
        return ('app', resolve_env(expr[1]), resolve_env(expr[2]))
    else:
        return expr

def normalize(expr):
    prev = None
    curr = resolve_env(expr) # resolve once at the start
    while curr != prev:
        prev = curr
        curr = beta_reduce(curr)
        curr = resolve_env(curr) # re‐inline any newly‐uncovered defs
    return curr


def repl(debug=False):
    print(texts.splashText)
    print("Labcoats on, team. We're going bug hunting.") if debug else None
    while True:
        try:
            line=input('λ> ').strip()
            if not line:
                continue

            # Handle variable assignment
            if ':=' in line:
                name,expr=line.split(':=', 1)
                name=name.strip()
                expr=expr.strip()
                tokens=tokenize(expr)
                ast=Parser(tokens).parse()
                env[name]=ast
                print(f"{name} defined.")
                print(ast) if debug else None
            elif line==":help":
            	print(texts.helpText)
            elif line==":how2":
            	print(texts.lambdaCalculus)
            elif line.startswith(':church'):
            	num=line[8:]
            	if num=="":
            		print("Enter a number!")
            	else:
            		print(pretty(make_church_number(int(num)), ign_church=True))
            elif line==":quit":
            	break
            elif line.startswith(":show"):
            	varname=line[6:]
            	if varname=="":
            		for i in env.keys():
            			print(f"{i} : {pretty(env[i])}")
            	else:
            		print(pretty(env[varname]))
            else:
                tokens=tokenize(line)
                ast=Parser(tokens).parse()
                print("AST :",ast) if debug else None

                # Substitute any named variables with their definitions
                evaluated=resolve_env(ast)
                print("Resolved AST :",evaluated) if debug else None
                #print(pretty(beta_reduce(evaluated)))
                print(pretty(normalize(evaluated)))
        except KeyboardInterrupt:
            print("Hey! Use :quit like a nice user!")
        #except Exception as e:
            #print("Error:", e)



if __name__=="__main__":
	import sys
	debugMode=False
	try:
		if sys.argv[1]=="debug":
			debugMode=True
	except:
		pass
	repl(debugMode)
