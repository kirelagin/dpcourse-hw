# SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>
#
# SPDX-License-Identifier: MPL-2.0

import sys

from typing import Callable, Generator, Sequence


# The solver function takes a generator of noisy prefix sums and a hint
SolverInput = Generator[int, None, None]
SolverHint = Sequence[int]
Solver = Callable[[SolverInput, SolverHint], Sequence[int]]
