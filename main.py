from scanner import Scanner
from parser import Parser
from vm import VM

source = """
var x = 10
+ 3
var y = x + 5
x = x * 2
if (x > 15) {
    print(x)
}
var i = 0
while (i < 5) {
    print("hello")
    print(i)
    i = i + 1
}
"""

tokens = Scanner(source).scan()
ast = Parser(tokens).parse()
VM().run(ast)   
