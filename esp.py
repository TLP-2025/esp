import sys
from modules import scanner, state, tokenizer
from modules.rd_parcer.parser import RDParser


def run(source: str):
    # Reiniciar estado de error
    state.hadError = False

    # Paso previo: tokenizar automáticamente si la frase no viene anotada
    annotated = tokenizer.annotate_source(source)

    tokens = list(scanner.tokens(annotated))

    parser = RDParser(tokens)
    try:
        parrafo = parser.parse()
    except Exception:
        # El propio parser ya reporta el error vía state.parseError
        return

    if state.hadError:
        return

    # Si llegó hasta aquí, todo se parseó correctamente
    print("Acceptado")


def runPrompt():
    try:
        while True:
            try:
                line = input("esp> ")
            except EOFError:
                break

            if not line.strip():
                continue

            run(line)
    except KeyboardInterrupt:
        print()


def runFile(path: str):
    with open(path, 'r', encoding='utf-8') as file:
        run(file.read())


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        runPrompt()
    elif len(args) == 1:
        runFile(args[0])
    else:
        sys.exit(64)
