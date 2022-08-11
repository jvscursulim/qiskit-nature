# This code is part of Qiskit.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test HeisenbergModel."""

from test import QiskitNatureTestCase
from retworkx import PyGraph, is_isomorphic
from qiskit_nature.second_q.properties.lattices import Lattice
from qiskit_nature.second_q.properties import HeisenbergModel, IsingModel


class TestHeisenbergModel(QiskitNatureTestCase):
    """TestHeisenbergModel"""

    def test_init(self):
        """Test init."""
        graph = PyGraph(multigraph=False)
        graph.add_nodes_from(range(2))
        weighted_edge_list = [(0, 1, 1.0)]
        graph.add_edges_from(weighted_edge_list)
        ism_graph = PyGraph(multigraph=False)
        ism_graph.add_nodes_from(range(2))
        ism_weighted_edge_list = [(0, 1, -1.0), (0, 0, -1.0), (1, 1, -1.0)]
        ism_graph.add_edges_from(ism_weighted_edge_list)
        triangle_graph = PyGraph(multigraph=False)
        triangle_graph.add_nodes_from(range(3))
        triangle_weighted_edge_list = [(0, 1, 1.0), (0, 2, 1.0), (1, 2, 1.0), (0, 0, 1.0), (1, 1, 1.0), (2, 2, 1.0)]
        triangle_graph.add_edges_from(triangle_weighted_edge_list)
        lattice = Lattice(graph)
        ism_lattice = Lattice(ism_graph)
        ism = IsingModel(ism_lattice)
        heisenberg_model = HeisenbergModel(lattice)
        coupling_constants = (0.0, 0.0, -1.0)
        ext_magnetic_field = (-1.0, 0.0, 0.0)
        hm_to_ism = HeisenbergModel(ism_lattice, coupling_constants, ext_magnetic_field)
        xy_coupling = (0.5, 0.5, 0.0)
        xy_ext_magnetic_field = (-0.75, 0.25, 0.0)
        xy_test_hm = HeisenbergModel(lattice, xy_coupling, xy_ext_magnetic_field)
        triangle_lattice = Lattice(triangle_graph)
        ext_magnetic_field_y = (0.0, 1.0, 0.0)
        triangle_y_heisenberg_model = HeisenbergModel(triangle_lattice, ext_magnetic_field=ext_magnetic_field_y)
        xyz_ext_magnetic_field = (1.0, 1.0, 1.0)
        xyz_test_hm = HeisenbergModel(lattice, ext_magnetic_field=xyz_ext_magnetic_field)

        with self.subTest("Check the graph."):
            self.assertTrue(
                is_isomorphic(
                    heisenberg_model.lattice.graph, lattice.graph, edge_matcher=lambda x, y: x == y
                )
            )
            
        with self.subTest("Check the graph of triangular model."):
            self.assertTrue(
                is_isomorphic(
                    triangle_y_heisenberg_model.lattice.graph, triangle_lattice.graph, edge_matcher=lambda x, y: x == y
                )
            )

        with self.subTest("Check the second q op representation."):
            coupling = [("X_0 X_1", 1.0), ("Y_0 Y_1", 1.0), ("Z_0 Z_1", 1.0)]

            hamiltonian = coupling

            self.assertSetEqual(set(hamiltonian), set(heisenberg_model.second_q_ops().to_list()))

        with self.subTest("Check if the HeisenbergModel reproduce IsingModel in a special case."):

            self.assertSetEqual(
                set(ism.second_q_ops().to_list()),
                set(hm_to_ism.second_q_ops().to_list()),
            )
            
        with self.subTest("Check if if x and y params are being applied."):
            coupling = [("X_0 X_1", 0.5), ("Y_0 Y_1", 0.5), ("X_0", -0.75), ("X_1", -0.75), ("Y_0", 0.25), ("Y_1", 0.25)]

            hamiltonian = coupling

            self.assertSetEqual(set(hamiltonian), set(xy_test_hm.second_q_ops().to_list()))
            
        with self.subTest("Check if if x, y and z params are being applied."):
            coupling = [("X_0 X_1", 1.0), ("Y_0 Y_1", 1.0), ("Z_0 Z_1", 1.0), ("X_0", 1.0), ("X_1", 1.0), ("X_2", 1.0), ("Y_0", 1.0), ("Y_1", 1.0), ("Y_2", 1.0), ("Z_0", 1.0), ("Z_1", 1.0), ("Z_2", 1.0)]

            hamiltonian = coupling

            self.assertSetEqual(set(hamiltonian), set(xyz_test_hm.second_q_ops().to_list()))  
            
        with self.subTest("Check the second q ops in the triangular lattice with param in y axis."):
            coupling = [("X_0 X_1", 1.0), ("Y_0 Y_1", 1.0), ("Z_0 Z_1", 1.0), ("X_0 X_2", 1.0), ("Y_0 Y_2", 1.0), ("Z_0 Z_2", 1.0), ("X_1 X_2", 1.0), ("Y_1 Y_2", 1.0), ("Z_1 Z_2", 1.0), ("Y_0", 1.0), ("Y_1", 1.0), ("Y_2", 1.0)]

            hamiltonian = coupling

            self.assertSetEqual(set(hamiltonian), set(triangle_y_heisenberg_model.second_q_ops().to_list()))
            
        
