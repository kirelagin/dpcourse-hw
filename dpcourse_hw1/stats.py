# SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>
#
# SPDX-License-Identifier: MPL-2.0

# Statistical stuff

from math import sqrt
from scipy.stats import t
from typing import Tuple


class Estimator:
  """Estimates the mean and (unbiased) variance of streaming data.

  The mean is estimated using the standard algorithm everyone knows
  (or can devise themselves).

  The variance estimation is done with some magic a-la Knuth.
  """

  def __init__(self) -> None:
    """Initialise the estimator."""
    self._count: int = 0
    self._mean: float = 0
    self._vsum: float = 0

  def observe(self, x: float) -> None:
    """Take in a new observation."""
    self._count += 1

    old_mean = self._mean
    self._mean += (x - self._mean) / self._count
    self._vsum += (x - old_mean) * (x - self._mean)

  def estimate(self, confidence: float) -> Tuple[float, float]:
    """Return the current estimate mean and error margin."""
    assert 0.0 <= confidence <= 1.0, "Confidence level has to be between 0 and 1"

    # (Unbiased) variance
    var = self._vsum / (self._count - 1)
    # Standard error
    sterr = sqrt(var)

    # Sigma of the t-distribution
    scale: float = sterr / sqrt(self._count)
    # Critical t-value
    margin: float = t.ppf((1 + confidence) / 2, df=self._count-1, scale=scale)

    return (self._mean, margin)
