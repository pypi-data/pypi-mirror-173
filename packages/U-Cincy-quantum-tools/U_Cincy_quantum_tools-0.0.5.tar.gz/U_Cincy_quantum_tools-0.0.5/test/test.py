from UC_Quantum_Lab.commands import display, state, counts
from qiskit import QuantumCircuit

qc = QuantumCircuit(2, 2)

qc.h(0)
state(qc)
qc.measure_all()
display(qc)
counts(qc)