import pandas as pd

def extract_features(data, n, m, instance_name):
    df = pd.DataFrame(data)
    
    # Cálculo de características
    n_m = n / m
    min_pij = df.min().min()
    max_pij = df.max().max()
    q = max_pij / min_pij
    range_pij = max_pij - min_pij
    mean_pij = df.values.flatten().mean()
    std_pij = df.values.flatten().std()
    cv_pij = (std_pij / mean_pij) * 100

    lowest = df.min(axis=1)
    cv_min_pij = lowest.std() / lowest.mean() * 100

    coincidencias = df.eq(lowest, axis=0)
    n_fastest = coincidencias.sum(axis=0)
    cv_n_fastest = n_fastest.std() / n_fastest.mean() * 100
    below_n_m = (n_fastest < n_m).sum()

    diff_fastest = df.apply(lambda fila: sorted(fila)[1] - sorted(fila)[0], axis=1)
    max_diff_fastest = diff_fastest.max()
    mean_diff_fastest = diff_fastest.mean()

    return {
        'Instancia': instance_name,
        'm': m,
        'n': n,
        'n_m': n_m,
        'below_n_m': below_n_m,
        'q': q,
        'min_pij': min_pij,
        'max_pij': max_pij,
        'range_pij': range_pij,
        'mean_pij': mean_pij,
        'cv_pij': cv_pij,
        'cv_min_pij': cv_min_pij,
        'cv_n_fastest': cv_n_fastest,
        'max_diff_fastest': max_diff_fastest,
        'mean_diff_fastest': mean_diff_fastest
    }