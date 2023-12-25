import streamlit as st
from qiskit import Aer, QuantumCircuit, transpile, execute
from qiskit.visualization import plot_histogram, plot_bloch_multivector, circuit_drawer


def bit_flip_code(error_qubit):
    # Create a quantum circuit with 3 qubits (plus one ancillary qubit)
    qc = QuantumCircuit(4, 3)

    # Step 1: Encode the qubit in a superposition of states
    qc.h(0)          # Hadamard gate creates a superposition
    qc.cx(0, 3)      # CNOT gate entangles the qubit with an ancillary qubit

    try:
        # Apply an X gate to simulate a bit-flip error on the specified qubit
        qc.x(error_qubit)
        
        # Add measurements for all qubits
        qc.measure_all()

    except ValueError as e:
        st.error(f"Error: {e}")
        return

    # Step 3: Implement error correction
    qc.cx(0, 1)       # CNOT gates to check for errors
    qc.cx(0, 2)
    qc.ccx(2, 1, 3)   # Toffoli gate helps correct the error using an ancillary qubit
    qc.cx(0, 1)       # CNOT gates to correct errors
    qc.cx(1, 2)

    # Visualization of the quantum circuit
    col1, col2 = st.columns(2)
    col1.pyplot(circuit_drawer(qc, output='mpl', fold=-1))

    # Step 4: Simulate the quantum circuit
    backend_simulator = Aer.get_backend('statevector_simulator')
    transpiled_qc = transpile(qc, backend_simulator)
    result = execute(transpiled_qc, backend_simulator, shots=1024).result()
    
    # Display the Bloch vector of the specified qubit
    statevector = result.get_statevector()
    col2.pyplot(plot_bloch_multivector(statevector))

    # Display the histogram of measurement results
    counts = result.get_counts(qc)
    col1.pyplot(plot_histogram(counts))


def main():
    st.write('<div style="text-align:center; padding: 20 px;"><h1>Quantum Error Correction</h1></div>', unsafe_allow_html = True)

    # User Interaction: Ask the user which qubit to apply the bit-flip error
    error_qubit = st.slider("Select the qubit number to apply the bit-flip error", min_value=0, max_value=2, value=0)

    # Run the quantum error correction code
    bit_flip_code(error_qubit)

if __name__ == "__main__":
    main()