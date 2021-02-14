# SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>
#
# SPDX-License-Identifier: MPL-2.0

from functools import partial
from math import ceil
import numpy as np
import numpy.random as rand
from typing import Sequence, Tuple

from dpcourse_hw1.typing import Solver, SolverHint, SolverInput
from dpcourse_hw1.stats import Estimator

rng = rand.default_rng()


def outputs(xs: Sequence[int]) -> SolverInput:
  """Given secret inputs, generate prefix sums with noise."""
  sum: int = 0
  for x in xs:
    sum += x
    yield sum + rng.integers(low=0, high=2, size=1)[0]


def run_solver(s: Solver, n: int, p: float) -> int:
  """Run solver on a random input and count correct guesses.

  n is the size of the input to generate
  p is the probability that each bit in the hint is correct
  """
  # Random data record
  xs = rng.random(n) <= 1/2
  # Hint
  hint_mask = rng.random(n) <= p
  hint = hint_mask * xs + (1 - hint_mask) * (1 - xs)
  # Run the solver on it
  guess = s(outputs(xs), hint)
  correct: int = np.sum(xs == guess)
  return correct

def evaluate(s: Solver, n: int, confidence: float, p: float = 0.5) -> Tuple[float, float]:
  """Evaluate a solver on inputs of the given size.

  Runs solver `s` on inputs of size `n` where each input bit is sampled from
  Bernoulli(p). Returns `(estimate, margin)` such that the fraction of inputs
  the solver guesses correctly is within (estimate ± margin) with `confidence`.
  """
  est = Estimator()

  trials: int = max(10, ceil(10000 / n))
  for _i in range(trials):
    res = run_solver(s, n, p)
    est.observe(res / n)

  (mean, margin) = est.estimate(confidence)
  return (mean, margin)


###
# For testing from the command line
###

def dumb_solver(sums: SolverInput, hint: SolverHint) -> Sequence[int]:
  """A solver that just returns the hint."""
  return hint

if __name__ == '__main__':
  (mean, margin) = evaluate(dumb_solver, 100, .99)
  print(f'Mean = {mean:.4} ± {margin:.4}')

  (mean, margin) = evaluate(partial(dumb_solver), 100, .99, p=2/3)
  print(f'Mean = {mean:.4} ± {margin:.4}')
