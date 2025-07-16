#!/bin/bash

# AERMOD Runner Script
# This script makes it easy to run AERMOD from any directory

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AERMOD_EXEC="$SCRIPT_DIR/AERMOD/src/aermod"

# Check if aermod executable exists
if [ ! -f "$AERMOD_EXEC" ]; then
    echo "Error: AERMOD executable not found at $AERMOD_EXEC"
    echo "Please make sure AERMOD is properly compiled."
    exit 1
fi

# Check if aermod.inp exists in current directory
if [ ! -f "aermod.inp" ]; then
    echo "Error: aermod.inp not found in current directory"
    echo "Please make sure you have an aermod.inp file in the current directory."
    echo "You can copy one of the test files from AERMOD/test/inputs/"
    echo "Example: cp AERMOD/test/inputs/aertest.inp aermod.inp"
    exit 1
fi

# Run AERMOD
echo "Running AERMOD..."
"$AERMOD_EXEC"

# Check if run was successful
if [ $? -eq 0 ]; then
    echo "AERMOD completed successfully!"
    echo "Check aermod.out for results."
else
    echo "AERMOD encountered an error. Check aermod.out for details."
fi 