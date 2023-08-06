def harmonic_mean(values: list[float]) -> float:
    N = len(values)
    sum_reciprocals = sum(1/value for value in values)
    return N/sum_reciprocals
