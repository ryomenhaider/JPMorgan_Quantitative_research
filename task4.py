import pandas as pd
import numpy as np

df = pd.read_csv('/mnt/D06A89C26A89A5B6/projects/Forage/JPMorgan_Quantitative_research/data/Loan_Data.csv')

def compute_log_likelihood(n, k):
    if n == 0 or k == 0 or k == n:
        return 0
    p = k / n
    return k * np.log(p) + (n - k) * np.log(1 - p)

def log_likelihood_buckets(df, n_buckets):
    df_sorted = df.sort_values('fico_score').reset_index(drop=True)
    scores    = df_sorted['fico_score'].values
    defaults  = df_sorted['default'].values
    n         = len(scores)

    cum_defaults = np.cumsum(defaults)

    def bucket_ll(start, end):
        count = end - start
        deflt = cum_defaults[end-1] - (cum_defaults[start-1] if start > 0 else 0)
        return compute_log_likelihood(count, deflt)

    dp    = np.full((n + 1, n_buckets + 1), -np.inf)
    split = np.zeros((n + 1, n_buckets + 1), dtype=int)
    dp[0][0] = 0

    for i in range(1, n + 1):
        for b in range(1, n_buckets + 1):
            for j in range(b - 1, i):
                ll = dp[j][b-1] + bucket_ll(j, i)
                if ll > dp[i][b]:
                    dp[i][b]    = ll
                    split[i][b] = j

    boundaries = []
    i = n
    for b in range(n_buckets, 0, -1):
        i = split[i][b]
        if i > 0:
            boundaries.append(scores[i])

    boundaries = sorted(boundaries)
    boundaries = [scores[0]] + boundaries + [scores[-1]]
    return boundaries

def create_rating_map(boundaries, n_buckets):
    def get_rating(fico):
        for i in range(len(boundaries) - 1):
            if boundaries[i] <= fico <= boundaries[i+1]:
                return n_buckets - i
        return n_buckets
    return get_rating

n_buckets  = 5
boundaries = log_likelihood_buckets(df, n_buckets)
get_rating = create_rating_map(boundaries, n_buckets)

print("Bucket Boundaries:", boundaries)

for fico in [600, 650, 700, 750, 800]:
    print(f"FICO {fico} → Rating {get_rating(fico)}")