# SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>
#
# SPDX-License-Identifier: MPL-2.0

import sys

from typing import Callable, Generator, Sequence


# The solver function takes a generator of noisy prefix sums
SolverInput = Generator[int, None, None]
Solver = Callable[[SolverInput], Sequence[int]]
