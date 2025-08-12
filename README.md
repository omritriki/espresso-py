# espresso-py

Educational Python reimplementation of the Espresso two-level Boolean logic minimizer.

## 🚧 Work in Progress 🚧

This is an educational implementation of the Espresso algorithm for Boolean function minimization. The core algorithm functions (expand, reduce, irredundant) are currently placeholders and need to be implemented.

## Project Structure

```
espresso-py/
├── src/
│   ├── pla.py              # PLA data structures and parsing
│   ├── visualization.py    # Truth table display functions
│   └── espresso.py         # Core Espresso algorithm (WIP)
├── examples/
│   └── simple.pla          # Example PLA file
├── main.py                 # Entry point
└── README.md
```

## Goals
- Implement core Espresso loop: expand → reduce → irredundant
- Focus on clarity and correctness, not performance
- Support small `.pla` inputs
- Provide clear visualization of truth tables

## Usage

```bash
# Run with an example file
python main.py examples/simple.pla

# Run with your own PLA file
python main.py path/to/your/file.pla
```

## Current Status
- ✅ PLA file parsing and data structures
- ✅ Truth table visualization using pandas
- ✅ Project structure and modular design
- 🚧 Core Espresso algorithm implementation (expand, reduce, irredundant)
- 🚧 Boolean logic optimization

## Dependencies
- Python 3.7+
- pandas (for truth table visualization)

## Credits
Based on the original C implementation of Espresso from UC Berkeley.
