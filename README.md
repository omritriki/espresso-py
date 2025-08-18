# espresso-py

Educational Python reimplementation of the Espresso two-level Boolean logic minimizer.

## Overview
This project provides a small, readable implementation of the classic Espresso flow (expand → reduce → irredundant) for Boolean function minimization over PLA inputs. It prints the original and optimized truth tables, the Boolean expressions (sum-of-products), and compares literal counts before and after optimization.

Focused on clarity and correctness for small PLAs; not intended for large-scale/industrial use.

## Project Structure

```
espresso-py/
├── src/
│   ├── pla.py              # PLA data structures and parsing
│   ├── visualization.py    # Truth table + SOP printing and metrics
│   └── espresso.py         # Expand/Reduce/Irredundant + simple iterative loop
├── examples/               # Example PLA files
├── main.py                 # CLI entry point
├── requirements.txt        # Minimal dependencies
└── README.md
```

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Run with an example file
python main.py examples/simple.pla

# Run with your own PLA file
python main.py path/to/your/file.pla
```

The program prints the original/optimized truth tables and SOP expressions, and a literal count comparison.

## Features
- PLA parsing and validation
- Truth table rendering (pandas DataFrame)
- SOP expression printing (single and multi-output)
- Simple Espresso-style cycle: expand → reduce → irredundant with a small iterative improvement loop
- Literal count comparison before/after optimization

## Limitations
- Educational heuristic, not a full Espresso reimplementation
- No explicit handling of separate on/off/don’t-care sets
- Aimed at small inputs; no performance tuning

## Example

```bash
python main.py examples/4x1_parity.pla
```

Don't-care demo (shows a clear reduction by leveraging `-` rows):

```bash
python main.py examples/dont_care.pla
```

## Requirements
- Python 3.8+
- pandas

## License
MIT — see `LICENSE`.

## Credits
Inspired by the original Espresso implementation (UC Berkeley).
