import pandas as pd
from .pla import PLA

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
