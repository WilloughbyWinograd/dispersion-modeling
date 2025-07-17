# AERMOD Air Pollution Dispersion Modeling

This repository contains a compiled and tested version of AERMOD (Air Pollution Dispersion Modeling) for macOS, along with utility scripts for input file preparation and post-processing.

## Installation Summary

- **Compiler Used**: gfortran 15.1.0 (Homebrew)
- **Source**: https://github.com/mattfung/AERMOD.git
- **Compilation Date**: July 15, 2024
- **Status**: ✅ Successfully compiled and tested

## Directory Structure

```
dispersion-modeling/
├── AERMOD/                    # Main AERMOD installation
│   ├── src/                   # Source code and executable
│   │   ├── aermod             # Compiled AERMOD executable
│   │   ├── *.f                # Fortran source files
│   │   └── makefile           # Compilation configuration
│   └── test/                  # Test cases and examples
│       ├── inputs/            # Input files for testing
│       └── Outputs/           # Expected output files
├── run_aermod.sh              # Convenience script to run AERMOD
├── complete_fix.py            # Utility: Fix DISCCART lines in input files
├── fix_receptors.py           # Utility: Fix receptor elevations in input files
├── requirements.txt           # Python requirements for utility scripts
└── README.md                  # This file
```

## Usage

### Quick Start

1. **Prepare your input file**: Copy or create an `aermod.inp` file in your working directory
2. **Run AERMOD**: Use the convenience script:
   ```bash
   ./run_aermod.sh
   ```

### Manual Usage

1. **Navigate to your input directory**:
   ```bash
   cd /path/to/your/input/files
   ```
2. **Ensure you have an `aermod.inp` file** in the current directory
3. **Run AERMOD**:
   ```bash
   /path/to/dispersion-modeling/AERMOD/src/aermod
   ```

### Test Cases

The installation includes numerous test cases in `AERMOD/test/inputs/`:
- `aertest.inp` - Basic test case (✅ verified working)
- `testpm10.inp` - PM10 particulate matter test
- `testpm25.inp` - PM2.5 particulate matter test
- `testgas.inp` - Gas dispersion test
- And many more...

To run a test case:
```bash
cd AERMOD/test/inputs
cp aertest.inp aermod.inp
../../src/aermod
```

## Utility Scripts

This repository includes Python scripts to help prepare and fix AERMOD input files:

- `complete_fix.py`: Ensures all DISCCART lines in an input file have the correct 5-parameter format (X Y ZELEV ZHILL ZFLAG).
- `fix_receptors.py`: Adds or corrects elevation information for all DISCCART receptor lines.

### Running the Scripts

Install Python requirements:
```bash
pip install -r requirements.txt
```

Run a script, for example:
```bash
python complete_fix.py
python fix_receptors.py
```

## Compilation Details

The makefile was modified to use gfortran instead of g95:

```makefile
FC=gfortran
FCFLAGS=-c -fbounds-check -O2 -mtune=native
```

## Output Files

After running AERMOD, you'll find:
- `aermod.out` - Main output file with results and any error messages
- Additional output files as specified in your input configuration

## Troubleshooting

### Common Issues

1. **"aermod.inp not found"**: Make sure you have an input file named exactly `aermod.inp` in your current directory
2. **Permission denied**: Make sure the aermod executable has execute permissions:
   ```bash
   chmod +x AERMOD/src/aermod
   ```
3. **Compilation errors**: If you need to recompile, navigate to `AERMOD/src/` and run:
   ```bash
   make clean
   make
   ```

### Verification

The installation was verified by running the `aertest.inp` test case, which completed successfully with no fatal errors.

## EPA Documentation

- [EPA Air Quality Dispersion Modeling - Preferred and Recommended Models](https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models)
- [AERMOD Implementation Guide (PDF)](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/preferred/aermod/aermod_implementation_guide.pdf)

These resources provide official documentation, regulatory guidance, and technical details for AERMOD and related models. For the latest updates and best practices, always refer to the EPA SCRAM website.

## References

- Original installation guide: Based on M. Fung's "AERMOD Installation for Mac & Linux - Quick Guide v1.2"
- AERMOD documentation: https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models#aermod
- Source repository: https://github.com/mattfung/AERMOD.git 