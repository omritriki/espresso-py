from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Cube:
    bits: str   # e.g. "01-" (0/1/-)
    out: str    # single bit "0" or "1"

@dataclass
class PLA:
    n_inputs: int
    n_outputs: int
    cubes: List[Cube]

def parse_pla(path: str) -> PLA:
    n_in = n_out = None
    cubes: List[Cube] = []
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith(('#', '.type')):
                continue
            if line.startswith('.i'):
                n_in = int(line.split()[1])
            elif line.startswith('.o'):
                n_out = int(line.split()[1])
            elif line.startswith('.e'):
                break
            elif line[0] in '01-':
                parts = line.split()
                bits = parts[0]
                out = parts[1] if len(parts) > 1 else '1'
                cubes.append(Cube(bits, out))
    if n_in is None or n_out is None:
        raise ValueError("Missing .i or .o header")
    # sanity
    for c in cubes:
        if len(c.bits) != n_in:
            raise ValueError(f"Cube length mismatch: {c.bits}")
        if len(c.out) != n_out:
            raise ValueError(f"Output length mismatch: {c.out}")
    return PLA(n_in, n_out, cubes)

def to_pla_text(pla: PLA) -> str:
    lines = [f".i {pla.n_inputs}", f".o {pla.n_outputs}"]
    for c in pla.cubes:
        lines.append(f"{c.bits} {c.out}")
    lines.append(".e")
    return "\n".join(lines)
