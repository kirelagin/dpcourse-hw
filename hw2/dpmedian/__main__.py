# SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>
#
# SPDX-License-Identifier: MPL-2.0

import dpmedian as dp
from math import sqrt
import numpy as np
from numpy.random import default_rng
import scipy.stats as stats  # type: ignore
from typing import Any, Callable, List, NewType, Sequence, Tuple

# Globl variables FTW
rng = default_rng()


R = NewType('R', int)
N = NewType('N', int)
Distr = Callable[[R, N], np.ndarray]

# Return the rank of `x` in _sorted_ array `arr`.
def rank(arr: np.ndarray, x: float) -> int:
  r: int = 0
  for a in arr:
    if a > x:
      return r
    r += 1
  return r

def evaluate(distr: Distr, r: R, n: N) -> Tuple[float, float, float]:
  err = np.empty((50, 10))

  for i in range(50):
    record = distr(r, n)
    record.sort()  # the algorithm does not care if it is sorted, sorting for `rank`
    for j in range(10):
      result = dp.median(record, r=r, eps=0.1)
      err[i][j] = abs(float(rank(record, result)) - n / 2)

  return (err.mean(), err.std(ddof=1), err.std(ddof=1, axis=1).mean())

# Bimodal distribution
def bimodal(k: int, r: int, n: int) -> np.ndarray:
  return rng.choice([r/2 - k, r/2 + k], n)

def main() -> None:

  distrs: List[Tuple[str, List[int], Distr]] = [
    ('Gaussian', [100, 1000, 10000], lambda r, n: rng.normal(r/4, r/sqrt(10), n)),
    ('Poisson', [100, 1000, 10000], lambda _r, n: rng.poisson(50, n)),
  ] + [
    (f'Bimodal (k={k})', [1000], lambda r, n: bimodal(k, r, n)) for k in [10, 100, 200]
  ]
  for (name, rs, distr) in distrs:
    print()
    print(f'{name}:')
    print(f'---')
    for n in [50, 100, 500, 2000, 10000]:
      print(f' n = {n}', end=' ')
      for r in rs:
        (avg, std, rec_avg_std) = evaluate(distr, R(r), N(n))
        print(f'&  {avg:.2f} / {std:.2f} / {rec_avg_std:.2f}', end=' ')
      print(r' \\')

if __name__ == '__main__':
  main()
