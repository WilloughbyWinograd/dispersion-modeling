# AERMOD Air Pollution Dispersion Modeling

This repository contains a successfully installed and compiled version of AERMOD (Air Pollution Dispersion Modeling) for macOS.

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
│   │   ├── aermod            # Compiled AERMOD executable
│   │   ├── *.f               # Fortran source files
│   │   └── makefile          # Compilation configuration
│   └── test/                 # Test cases and examples
│       ├── inputs/           # Input files for testing
│       └── Outputs/          # Expected output files
├── run_aermod.sh             # Convenience script to run AERMOD
└── README.md                 # This file
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

## References

- Original installation guide: Based on M. Fung's "AERMOD Installation for Mac & Linux - Quick Guide v1.2"
- AERMOD documentation: https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models#aermod
- Source repository: https://github.com/mattfung/AERMOD.git 