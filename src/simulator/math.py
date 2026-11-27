__all__ = [
    'clampf', 'clampi',
]

def clampf(a: float, val: float, b: float) -> float:
    if val < a: return a
    if val > b: return b
    return val

def clampi(a: int, val: int, b: int) -> int:
    if val < a: return a
    if val > b: return b
    return val
