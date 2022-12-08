import lexer
import RDA

f1 = open("test1.txt")
f2 = open("test2.txt")
text = f2.read()
result = lexer.run(text)
print(result)
parser = RDA.Parser(result)
print(parser.start())