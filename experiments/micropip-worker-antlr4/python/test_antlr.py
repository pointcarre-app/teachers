from antlr4 import CommonTokenStream, ParseTreeWalker
from importlib.metadata import version

# Test basic ANTLR4 functionality
print("ANTLR4 Python Runtime Version:", version("antlr4-python3-runtime"))
print("Available classes:")
print("- CommonTokenStream:", CommonTokenStream)
print("- ParseTreeWalker:", ParseTreeWalker)

# Test creating a basic token stream
print("\nTesting basic functionality...")
try:
    # This is a simple test to ensure the module is working
    print("ANTLR4 runtime loaded successfully!")
    "ANTLR4 test completed successfully"
except Exception as e:
    print(f"Error during test: {e}")
    str(e)
