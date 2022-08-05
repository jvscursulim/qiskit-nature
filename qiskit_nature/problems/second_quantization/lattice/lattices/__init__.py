# This code is part of Qiskit.
#
# (C) Copyright IBM 2021, 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""A class containing information about the Lattice."""
from .boundary_condition import BoundaryCondition
from .hyper_cubic_lattice import HyperCubicLattice
from .lattice import LatticeDrawStyle, Lattice
from .line_lattice import LineLattice
from .square_lattice import SquareLattice
from .triangular_lattice import TriangularLattice
from .....deprecation import warn_deprecated, DeprecatedType, NatureDeprecationWarning

warn_deprecated(
    "0.5.0",
    old_type=DeprecatedType.PACKAGE,
    old_name="qiskit_nature.problems.second_quantization.lattice.lattices",
    new_type=DeprecatedType.PACKAGE,
    new_name="qiskit_nature.second_q.hamiltonians",
    stack_level=3,
    category=NatureDeprecationWarning,
)
