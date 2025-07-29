from antlr4 import InputStream, CommonTokenStream, Parser, Lexer
import antlr4

from antlr4.tree.Trees import Trees

def parse(input_string):
    # Create an input stream from the input string
    input_stream = InputStream(input_string)

    # Create a buffer of tokens pulled from the lexer
    token_stream = CommonTokenStream(lexer)
    
    # Create a lexer that feeds off the input stream
    lexer = Lexer(input_stream)
    
    # Create a buffer of tokens pulled from the lexer
    token_stream = CommonTokenStream(lexer)

    # Create a parser that feeds off the token stream
    parser = Parser(token_stream)
    
    
    # Print the parse tree
    print(Trees.toStringTree(tree, None, parser))
    
    return tree

input_string = "(hello (nested) world)"
parsed = parse(input_string)



# Send structured data via missive
missive(
    {
        "antlr4_version": antlr4.__version__,
        "input_string": input_string,
        "parsed": parsed
    }
)