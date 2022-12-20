from qiskit import Aer
from qiskit import QuantumCircuit
from qiskit import execute

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def ping():
    return 'Quantum Computing server for Q in a ROW game !!'

@app.route('/collapse')
def board_collapse() :
    args = request.args
    n = int(args.get("pairs"))
    circuit = QuantumCircuit(n, n)

    for i in range(n) :
        circuit.h(i)

    circuit.measure(range(n), range(n))

    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit,backend, shots=1, memory=True)
    result = job.result()
    result_string = result.get_memory(circuit)
    return result_string[0]
 
if __name__ == '__main__':
    app.run(host="0.0.0.0")
