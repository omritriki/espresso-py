#!/usr/bin/env python3
"""
Espresso Algorithm Implementation
A Python implementation of the Espresso algorithm for Boolean function minimization.
"""

import sys
from src.espresso import espresso

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.pla>")
        print("Example: python main.py examples/simple.pla")
        sys.exit(1)
    
    try:
        espresso(sys.argv[1])
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
