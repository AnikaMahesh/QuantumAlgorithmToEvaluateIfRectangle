from qiskit import *
import numpy as np
from qiskit.visualization import plot_histogram
from math import atan

# determine whether or not 4 sides A,B,C,D can form a rectangle
# inputs A,B,C,D - int - side lengths of rectangle
# returns: 1 if rectangle and 0 if not rectangle
def is_rectangle(A, B, C, D):
    # this is the oracle where the booleons are encoded as vectors on the z axis
    rectangle_oracle = QuantumCircuit(2, name='rectangle_oracle')
    rectangle_oracle.rz(int(2 * atan(15 * ((A - C) + (D - B)))), 0)
    rectangle_oracle.rz(int(2 * atan(15 * ((A - B) - (D - C)))), 1)
    rectangle_oracle.cz(1, 0)
    # diffuser that amplifies the amplitude of both qubits so they are most likely to collapse into a classical 1 or 2
    reflection= QuantumCircuit(2, name='reflection')
    reflection.h(range(2))
    reflection.z(range(2))
    reflection.cz(1, 0)
    reflection.h(range(2))
    #combines diffuser and oracle in order to complete quantum circuit
    circ = QuantumCircuit(3, 1)
    circ.h(range(2))
    circ.append(rectangle_oracle,range(2))
    circ.append(reflection, range(2))
    # makes sure 00 is displayed as 0 and 10,11,01 is displayed as 1 on a result qubit
    backend = Aer.get_backend("qasm_simulator")
    circ.x(range(2))
    circ.ccx(0, 1, 2)
    circ.x(2)
    circ.measure(2,0)
    counts = execute(circ, backend, shots = 1).result().get_counts()
    result = {i for i in counts if counts[i] == 1}
    return(int(list(result)[0]))
