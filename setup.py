import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["pygame","numpy","sys","math","tkinter","qiskit_aer","qiskit","retworkx","rustworkx"], "include_files":["logo.png"] }

#"includes":["qiskit_aer","qiskit.circuit","qiskit.execute_function"]

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Q in a ROW",
    version="0.1",
    description="Quantum 4 in a ROW Game !!",
    options={"build_exe": build_exe_options},
    executables=[Executable("Q_in_a_ROW.py", base=base)],
)