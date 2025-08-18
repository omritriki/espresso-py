from .pla import PLA, Cube, parse_pla, to_pla_text
from .visualization import print_truth_table, print_boolean_expression, count_literals


def covers_bits(candidate_bits: str, minterm_bits: str) -> bool:
    """Return True if cube bits (with '-') cover the specific minterm bits."""
    for cb, mb in zip(candidate_bits, minterm_bits):
        if cb != '-' and cb != mb:
            return False
    return True

def expand(pla: PLA, spec: PLA) -> PLA:
    """Expand phase – grow cubes to cover more minterms."""
    expanded_cubes = []
    
    for cube in pla.cubes:
        # Try to expand each cube by replacing 0s and 1s with don't-cares
        expanded = expand_cube(cube, pla, spec)
        # Only add if not already present
        if expanded not in expanded_cubes:
            expanded_cubes.append(expanded)
    
    return PLA(pla.n_inputs, pla.n_outputs, expanded_cubes)

def expand_cube(cube: Cube, pla: PLA, spec: PLA) -> Cube:
    """Expand a single cube by replacing values with don't-cares where possible.

    Iterate until no more bits can be expanded without hitting the off-set for any asserted output bit.
    """
    bits = list(cube.bits)
    changed = True
    while changed:
        changed = False
        for i in range(len(bits)):
            if bits[i] in '01':
                original_bit = bits[i]
                bits[i] = '-'
                if is_valid_expansion(bits, cube.out, spec):
                    changed = True
                else:
                    bits[i] = original_bit
    return Cube(''.join(bits), cube.out)

def is_valid_expansion(bits: list, output: str, spec: PLA) -> bool:
    """Check expansion against the off-set per output bit using the original spec.

    For each output bit j asserted in `output`, ensure the candidate cube does not cover
    any minterm that is labeled 0 for bit j in the specification PLA.
    """
    candidate_bits = ''.join(bits)
    for j, out_bit in enumerate(output):
        if out_bit != '1':
            continue
        for row in spec.cubes:
            if len(row.out) <= j:
                continue
            if row.out[j] == '0' and covers_bits(candidate_bits, row.bits):
                return False
    return True

def generate_minterms(bits: list) -> list:
    """Generate all minterms covered by a cube with don't-cares."""
    minterms = ['']
    
    for bit in bits:
        if bit == '-':
            # For don't-care, double the current minterms with 0 and 1
            new_minterms = []
            for minterm in minterms:
                new_minterms.append(minterm + '0')
                new_minterms.append(minterm + '1')
            minterms = new_minterms
        else:
            # For specific value, append to all current minterms
            minterms = [minterm + bit for minterm in minterms]
    
    return minterms

def reduce(pla: PLA, spec: PLA) -> PLA:
    """Reduce phase – shrink cubes to minimal size while maintaining coverage."""
    reduced_cubes = []
    
    for cube in pla.cubes:
        # Try to reduce each cube by making don't-cares more specific
        reduced = reduce_cube(cube, pla, spec)
        reduced_cubes.append(reduced)
    
    return PLA(pla.n_inputs, pla.n_outputs, reduced_cubes)

def reduce_cube(cube: Cube, pla: PLA, spec: PLA) -> Cube:
    """Reduce a single cube by making don't-cares more specific where possible, preserving F coverage."""
    bits = list(cube.bits)
    for i in range(len(bits)):
        if bits[i] == '-':
            # Try replacing with 0
            bits[i] = '0'
            if not is_valid_reduction(bits, cube, pla, spec):
                # Try replacing with 1
                bits[i] = '1'
                if not is_valid_reduction(bits, cube, pla, spec):
                    bits[i] = '-'
    return Cube(''.join(bits), cube.out)

def is_valid_reduction(bits: list, original_cube: Cube, pla: PLA, spec: PLA) -> bool:
    """Ensure all on-set minterms originally covered by original_cube remain covered by the union.

    For each output bit j asserted by original_cube, consider each minterm M covered by original_cube
    that is on (1) for j in the specification. The tentative cube (with `bits`) plus other cubes in `pla`
    that assert bit j must still cover M.
    """
    tentative_bits = ''.join(bits)
    original_bits = original_cube.bits
    for j, out_bit in enumerate(original_cube.out):
        if out_bit != '1':
            continue
        for m in generate_minterms(list(original_bits)):
            # Check if M is on-set for bit j in spec
            is_on_in_spec = False
            for row in spec.cubes:
                if len(row.out) > j and row.bits == m and row.out[j] == '1':
                    is_on_in_spec = True
                    break
            if not is_on_in_spec:
                continue
            # Check coverage by tentative cube or other cubes with bit j asserted
            covered = covers_bits(tentative_bits, m)
            if not covered:
                for other in pla.cubes:
                    if other is original_cube:
                        continue
                    if len(other.out) > j and other.out[j] == '1' and covers_bits(other.bits, m):
                        covered = True
                        break
            if not covered:
                return False
    return True

def subsumes(a: Cube, b: Cube) -> bool:
    """Return True if cube a subsumes cube b (same output, a >= b)."""
    if a.out != b.out:
        return False
    for ai, bi in zip(a.bits, b.bits):
        if ai != '-' and ai != bi:
            return False
    return True

def irredundant(pla: PLA) -> PLA:
    """Remove cubes redundant for every asserted output bit under union coverage."""
    cubes = pla.cubes
    keep = []
    for i, ci in enumerate(cubes):
        # Quick subsumption by an identical or more general cube with exact same outputs
        subsumed = False
        for j, cj in enumerate(cubes):
            if i != j and subsumes(cj, ci) and cj.out == ci.out:
                subsumed = True
                break
        if subsumed:
            continue

        # For each asserted output bit, ensure there exists some minterm of ci that is not covered by others.
        # If for all asserted bits all minterms are covered by others, ci is redundant.
        all_asserted_bits_redundant = True
        for bit_index, bit_value in enumerate(ci.out):
            if bit_value != '1':
                continue
            minterms_ci = generate_minterms(list(ci.bits))
            bit_redundant = True
            for m in minterms_ci:
                covered_elsewhere = False
                for k, other in enumerate(cubes):
                    if k == i:
                        continue
                    if len(other.out) > bit_index and other.out[bit_index] == '1' and covers_bits(other.bits, m):
                        covered_elsewhere = True
                        break
                if not covered_elsewhere:
                    bit_redundant = False
                    break
            if not bit_redundant:
                all_asserted_bits_redundant = False
                break
        if not all_asserted_bits_redundant:
            keep.append(ci)
    return PLA(pla.n_inputs, pla.n_outputs, keep)

def espresso(path: str):
    """Main Espresso algorithm function."""
    pla = parse_pla(path)
    
    # Show original truth table and Boolean expression
    print("Original PLA:")
    print_truth_table(pla)
    print_boolean_expression(pla, "Original Boolean Expression")
    original_pla = pla
    original_literals = count_literals(original_pla)
    
    # Use the parsed PLA as the fixed specification (on/off per output bit)
    spec = original_pla

    # Apply Espresso algorithm with a small iterative loop until no literal improvement
    best_pla = pla
    best_cost = count_literals(best_pla)
    max_iters = 5
    for _ in range(max_iters):
        candidate = expand(best_pla, spec)
        candidate = reduce(candidate, spec)
        candidate = irredundant(candidate)
        cand_cost = count_literals(candidate)
        if cand_cost < best_cost:
            best_pla, best_cost = candidate, cand_cost
        else:
            break
    pla = best_pla
    
    # Show optimized result as truth table and Boolean expression
    print("\nOptimized PLA:")
    print_truth_table(pla)
    print_boolean_expression(pla, "Optimized Boolean Expression")
    optimized_literals = count_literals(pla)
    print("Literal Count Comparison:")
    print("-" * 50)
    print(f"Before: {original_literals}")
    print(f"After : {optimized_literals}")
    if original_literals > 0:
        reduction = original_literals - optimized_literals
        pct = (reduction / original_literals) * 100
        direction = "reduction" if reduction >= 0 else "increase"
        print(f"Change : {reduction} ({pct:.1f}% {direction})")
    print("-" * 50)
