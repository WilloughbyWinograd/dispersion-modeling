#!/usr/bin/env python3
"""
Fix receptor elevations in CaCO3 AERMOD input file.
Add proper elevation format to all DISCCART receptor lines.
"""


def fix_receptor_elevations(input_file, output_file):
    """Fix receptor elevations by adding proper elevation format to all 
    DISCCART lines."""
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    for line in lines:
        # Check if this is a DISCCART line without elevation
        if line.strip().startswith('DISCCART') and line.count(' ') >= 2:
            # Split the line and check if it has only X and Y coordinates
            parts = line.strip().split()
            if len(parts) == 3:  # DISCCART X Y (missing elevation)
                # Add elevation format: ZELEV=100.0, ZHILL=100.0, ZFLAG=0.0
                fixed_line = f"   DISCCART   {parts[1]}   {parts[2]}   " + \
                            "100.0   100.0   0.0\n"
                fixed_lines.append(fixed_line)
            else:
                # Line already has elevation or is malformed
                fixed_lines.append(line)
        else:
            # Not a DISCCART line, keep as is
            fixed_lines.append(line)
    
    with open(output_file, 'w') as f:
        f.writelines(fixed_lines)
    
    print(f"Fixed receptor elevations in {input_file}")
    print(f"Output written to {output_file}")
    print("Format: DISCCART X Y ZELEV ZHILL ZFLAG")
    print("Where: ZELEV=100.0m, ZHILL=100.0m, ZFLAG=0.0m")


if __name__ == "__main__":
    fix_receptor_elevations("caco3_test_100m.inp", "caco3_test_100m_fixed.inp") 