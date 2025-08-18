git stat# Example PLA Files

This directory contains various PLA (Programmable Logic Array) files to test the Espresso algorithm implementation.

## Examples

### `simple.pla` (3 inputs, 1 output)
- Basic example with alternating outputs
- Good for testing basic functionality

### `2x1_simple.pla` (2 inputs, 1 output)
- Smallest example with XOR-like behavior
- Quick testing of the algorithm

### `3x1_majority.pla` (3 inputs, 1 output)
- Majority function: output is 1 when 2 or more inputs are 1
- Shows how the algorithm can find patterns

### `4x1_parity.pla` (4 inputs, 1 output)
- Parity function: output is 1 when odd number of inputs are 1
- More complex pattern that should be hard to minimize

### `3x2_adder.pla` (3 inputs, 2 outputs)
- 1-bit full adder: sum and carry outputs
- Tests multi-output functionality

### `5x1_complex.pla` (5 inputs, 1 output)
- Complex function with 32 minterms
- Tests performance with larger inputs

### `expand_test.pla` (3 inputs, 1 output)
- Designed to show expansion working
- All 0-inputs produce 1, all 1-inputs produce 0

### `reduce_test.pla` (3 inputs, 1 output)
- Designed to show reduction working
- All 0-inputs produce 1, all 1-inputs produce 0

### `dont_care.pla` (3 inputs, 1 output, with don't-cares)
- Demonstrates use of `-` in outputs to indicate don't-care rows
- Useful to showcase expansions that leverage don't-cares

## Usage

```bash
# Test with any example
python main.py examples/simple.pla
python main.py examples/3x1_majority.pla
python main.py examples/4x1_parity.pla
```

## Expected Results

- **2x1_simple**: Should minimize to 2 cubes
- **3x1_majority**: Should minimize significantly (majority has a simple pattern)
- **4x1_parity**: May not minimize much (parity is inherently complex)
- **expand_test/reduce_test**: Should show clear expansion and reduction
