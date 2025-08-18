import pandas as pd
from .pla import PLA, Cube

def visualize_truth_table(pla: PLA) -> pd.DataFrame:
    """Convert PLA to a pandas DataFrame for easy visualization of the truth table."""
    # Create input column names
    input_cols = [f'x{i}' for i in range(pla.n_inputs)]
    output_cols = [f'y{i}' for i in range(pla.n_outputs)]
    
    # Convert cubes to DataFrame rows
    rows = []
    for cube in pla.cubes:
        # Convert input bits to individual columns
        input_values = list(cube.bits)
        output_values = list(cube.out)
        
        # Create row with input and output values
        row = input_values + output_values
        rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=input_cols + output_cols)
    
    # Add a row index for better readability
    df.index = [f'Row {i+1}' for i in range(len(df))]
    
    return df

def print_truth_table(pla: PLA):
    """Print a nicely formatted truth table."""
    df = visualize_truth_table(pla)
    print(f"\nTruth Table ({pla.n_inputs} inputs, {pla.n_outputs} outputs):")
    print("=" * 50)
    print(df.to_string())
    print("=" * 50)

def cube_to_boolean(cube: Cube, input_names: list = None) -> str:
    """Convert a cube to a Boolean expression."""
    if input_names is None:
        input_names = [f'x{i}' for i in range(len(cube.bits))]
    
    terms = []
    for i, bit in enumerate(cube.bits):
        if bit == '0':
            terms.append(f"{input_names[i]}'")
        elif bit == '1':
            terms.append(input_names[i])
        # bit == '-' means don't care, so we don't include it
    
    if not terms:
        return "1"  # All don't cares
    
    return "".join(terms)  # No & symbol, just concatenation

def pla_to_boolean_expression(pla: PLA) -> str:
    """Convert a PLA to a Boolean expression in sum-of-products form.

    For single-output PLAs: include only cubes with output '1'.
    For multi-output PLAs: produce one equation per output bit yj using cubes where out[j] == '1'.
    """
    if not pla.cubes:
        return "0"

    if pla.n_outputs == 1:
        on_cubes = [c for c in pla.cubes if c.out == '1']
        if not on_cubes:
            return "0"
        return " + ".join(cube_to_boolean(c) for c in on_cubes)

    # Multi-output
    expressions = []
    for j in range(pla.n_outputs):
        cubes_j = [c for c in pla.cubes if len(c.out) > j and c.out[j] == '1']
        if cubes_j:
            rhs = " + ".join(cube_to_boolean(c) for c in cubes_j)
        else:
            rhs = "0"
        expressions.append(f"y{j} = {rhs}")
    return "\n".join(expressions)

def print_boolean_expression(pla: PLA, title: str = "Boolean Expression"):
    """Print the Boolean expression for a PLA."""
    print(f"\n{title}:")
    print("=" * 50)
    expr = pla_to_boolean_expression(pla)
    print(expr)
    print("=" * 50)

def count_literals(pla: PLA) -> int:
    """Count the total number of literals in the PLA's sum-of-products representation.

    For each cube, count how many input positions are specified (i.e., '0' or '1').
    Cubes that do not assert any output bit ('1') are ignored for counting.
    """
    total_literals = 0
    for cube in pla.cubes:
        if '1' not in cube.out:
            continue
        total_literals += sum(1 for bit in cube.bits if bit in ('0', '1'))
    return total_literals
