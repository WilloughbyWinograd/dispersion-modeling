#!/usr/bin/env python3
"""
Complete fix for DISCCART lines in CaCO3 AERMOD input file.
Ensure all DISCCART lines have proper 5-parameter format.
"""


def complete_disccart_fix(input_file, output_file):
    """Ensure all DISCCART lines have 5 parameters: X Y ZELEV ZHILL ZFLAG."""
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    fixed_count = 0
    
    for line in lines:
        # Check if this is a DISCCART line
        if line.strip().startswith('DISCCART'):
            parts = line.strip().split()
            if len(parts) == 4:  # DISCCART X Y ZELEV (missing ZHILL ZFLAG)
                # Add ZHILL=100.0 and ZFLAG=0.0
                fixed_line = f"   DISCCART   {parts[1]}   {parts[2]}   " + \
                            f"{parts[3]}   100.0   0.0\n"
                fixed_lines.append(fixed_line)
                fixed_count += 1
            elif len(parts) == 3:  # DISCCART X Y (missing ZELEV ZHILL ZFLAG)
                # Add ZELEV=100.0, ZHILL=100.0, ZFLAG=0.0
                fixed_line = f"   DISCCART   {parts[1]}   {parts[2]}   " + \
                            "100.0   100.0   0.0\n"
                fixed_lines.append(fixed_line)
                fixed_count += 1
            elif len(parts) == 6:  # Already correct format
                fixed_lines.append(line)
            else:
                # Keep line as is if it doesn't match expected patterns
                fixed_lines.append(line)
        else:
            # Not a DISCCART line, keep as is
            fixed_lines.append(line)
    
    with open(output_file, 'w') as f:
        f.writelines(fixed_lines)
    
    print(f"Fixed {fixed_count} DISCCART lines")
    print(f"Output written to {output_file}")


if __name__ == "__main__":
    complete_disccart_fix("caco3_test_100m_fixed.inp", 
                          "caco3_test_100m_complete.inp") 