# SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>
#
# SPDX-License-Identifier: MPL-2.0

from collections import Counter
from math import ceil, floor
import numpy as np
from numpy.random import default_rng
from typing import Optional, Sequence
import numpy.typing

rng = default_rng()


def median(record: np.ndarray, r: int, eps: float) -> int:
  # scale = 1 / lambda
  scale: float = 1 / eps

  def trim(x: float) -> int:
    if x > r: return r
    elif x < 1: return 1
    else: return round(x)

  # counting sort, lol
  count: np.ndarray = np.zeros(r, dtype=int)
  for x in record:
    # elements are from 1 to r, so subtract 1 when indexing
    count[trim(x) - 1] += 1

  result: int = 0
  result_score: Optional[float] = None

  # looks like it is slightly faster to sample all noises at once
  noise = rng.exponential(scale=scale, size=r)

  below: int = 0
  above: int = record.size
  for y in range(1, r + 1):
    above -= count[y - 1]
    score = -abs(below - above) + noise[y - 1]
    if result_score is None or score > result_score:
      (result, result_score) = (y, score)
    below += count[y - 1]

  return result
