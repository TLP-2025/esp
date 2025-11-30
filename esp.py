import sys
from modules import scanner
from modules.rd_parcer.parser import RDParser
from modules import state
from modules.rd_parcer.printer import print_esp
from modules.tokenizer import annotate_source


def run(source:str):
    prefixed = annotate_source(source)
    tokens = list(scanner.tokens(prefixed))
    ## Print Tokens
    # for t in tokens:
    #     print(t)

    parser = RDParser(tokens)
    parrafo = parser.parse()

    if (state.hadError): return

    print_esp(parrafo)
    print ("Acceptado")


def runPrompt():
    while (True):
        try:
            line = input("esp> ")
            if (line == ""): continue
        except EOFError: break
        except KeyboardInterrupt: break
        run(line)
        state.hadError = False

def runFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        run(file.read())

match len(sys.argv)-1:
    case 0:
        runPrompt()
    case 1:
        path = sys.argv[1]
        runFile(path)
    case _:
        sys.exit(64)
        

