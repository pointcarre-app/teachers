# Custom Python code example
import sys

print(f"Python version: {sys.version}")

# Test some basic Python functionality
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]
print(f"Original numbers: {numbers}")
print(f"Squared numbers: {squared}")

# Try using antlr4 in a simple way
try:
    import antlr4
    from importlib.metadata import version

    print(f"ANTLR4 is available, version: {version('antlr4-python3-runtime')}")

    # List some available classes
    available_classes = [attr for attr in dir(antlr4) if not attr.startswith("_")]
    print(f"Available ANTLR4 classes: {available_classes[:10]}...")  # Show first 10

    "Custom code execution completed"
except Exception as e:
    print(f"Error with ANTLR4: {e}")
    str(e)
