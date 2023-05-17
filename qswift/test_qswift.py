import logging
from unittest import TestCase
from qwrapper.hamiltonian import Hamiltonian, to_matrix_hamiltonian
from qwrapper.obs import PauliObservable
from benchmark.molecule import MolecularHamiltonian

from qswift.exact import ExactComputation
from qswift.initializer import XBasisInitializer
from qswift.qswift import QSwift


class TestQSwift(TestCase):
    def test_qswift(self):
        logging.getLogger().setLevel(logging.INFO)
        t = 1

        obs = Hamiltonian([1], [PauliObservable("ZIIIIIII")], 8)
        hamiltonian = MolecularHamiltonian(8, "6-31g", "hydrogen")
        initializer = XBasisInitializer()

        exact = ExactComputation(to_matrix_hamiltonian(obs),
                                 to_matrix_hamiltonian(hamiltonian), t, initializer)
        ex = exact.compute()

        N = 200
        qswift = QSwift(hamiltonian, obs, initializer, t=t, N=N, K=1, nshot=100, n_p=10000, tool="qulacs")
        result = qswift.evaluate()
        print(ex, result.sum(0), result.sum(1))
