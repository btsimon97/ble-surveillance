#!/bin/bash
#This is a startup script to correctly launch the GUI program since its
#dependencies are in a Python venv and not in the system's Python packages

#Path to where we should be executing files from
SCRIPT_EXEC_ROOT="/opt/bluemon/gui"

#Path to where the Python venv's root is.
VENV_ROOT="/opt/bluemon/venv"

#Name of the Python file we are attempting to run
PYTHON_SCRIPT_FILENAME="gui.py"

#Arguments to pass into the Python script, if any.
PYTHON_SCRIPT_ARGS=""

cd $SCRIPT_EXEC_ROOT
$VENV_ROOT/bin/python3 $PYTHON_SCRIPT_FILENAME $PYTHON_SCRIPT_ARGS
