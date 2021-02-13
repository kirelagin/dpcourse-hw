# SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>
#
# SPDX-License-Identifier: MPL-2.0

from functools import partial
import numpy as np
import numpy.random as rand
from typing import Sequence, Tuple

from dpcourse_hw1.typing import Solver, SolverInput
from dpcourse_hw1.stats import Estimator

rng = rand.default_rng()


def outputs(xs: Sequence[int]) -> SolverInput:
  """Given secret inputs, generate prefix sums with noise."""
  sum: int = 0
  for x in xs:
    sum += x
    yield sum + rng.integers(low=0, high=2, size=1)[0]


def run_solver(s: Solver, n: int, p: float) -> int:
  """Run solver on a random input and count correct guesses."""
  # Random data record
  xs = rng.random(n) <= p
  # Run the solver on it
  guess = s(outputs(xs))
  correct: int = np.sum(xs == guess)
  return correct

def evaluate(s: Solver, n: int, confidence: float, p: float = 0.5) -> Tuple[float, float]:
  """Evaluate a solver on inputs of the given size.

  Runs solver `s` on inputs of size `n` where each input bit is sampled from
  Bernoulli(p). Returns `(estimate, margin)` such that the fraction of inputs
  the solver guesses correctly is within (estimate ± margin) with `confidence`.
  """
  est = Estimator()

  trials: int = 100
  for _i in range(trials):
    res = run_solver(s, n, p)
    est.observe(res / n)

  (mean, margin) = est.estimate(confidence)
  return (mean, margin)


###
# For testing from the command line
###

def dumb_solver(sums: SolverInput, p: float = 0.5) -> Sequence[int]:
  """A solver that makes a completely random guess."""
  n = sum(1 for _s in sums)  # count items in the generator without looking at them
  guess: Sequence[int] = rng.random(n) <= p
  return guess

if __name__ == '__main__':
  (mean, margin) = evaluate(dumb_solver, 100, .99)
  print(f'Mean = {mean:.4} ± {margin:.4}')

  (mean, margin) = evaluate(partial(dumb_solver, p=2/3), 100, .99, p=2/3)
  print(f'Mean = {mean:.4} ± {margin:.4}')
