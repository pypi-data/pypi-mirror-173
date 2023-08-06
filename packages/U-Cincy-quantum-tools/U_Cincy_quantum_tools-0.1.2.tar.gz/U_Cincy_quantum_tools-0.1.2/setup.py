from setuptools import setup
setup(
    name='U_Cincy_quantum_tools',
    version='0.1.2',
    author='Marek Brodke, with support from the University of Cincinnati',
    description='Provides functionaliy for UC_Quantum_Lab development tools',
    long_description="Provides functionaliy for UC_Quantum_Lab development tools",
    keywords='development',
    python_requires='>=3.7',
    license="MIT",
    author_email="brodkemd@mail.uc.edu",
    url="https://github.com/brodkemd/UCQ_tools",
    install_requires=[
        'qiskit>=0.36',
        'matplotlib>=2.2.0',
        'qiskit-aer>=0.10.4',
        'qiskit-ibmq-provider>=0.19.1',
        'qiskit-ignis>=0.7.0',
        'qiskit-terra>=0.20.1',
        "pylatexenc>=2.0"
    ]
)