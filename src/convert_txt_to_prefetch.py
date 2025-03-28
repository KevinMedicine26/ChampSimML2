#!/usr/bin/env python3

import argparse

def convert_txt_to_prefetch(input_file, output_file, format_type='default', delimiter=',', instr_col=0, addr_col=1):
    """
    Convert a text file to a prefetch file format that ChampSim can use.
    
    Args:
        input_file: Path to the input file
        output_file: Path to the output file
        format_type: Format of the input file ('default' or 'csv')
        delimiter: Delimiter for CSV format
        instr_col: Column index for instruction ID in CSV format
        addr_col: Column index for prefetch address in CSV format
    """
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        if format_type == 'csv':
            for line in f_in:
                if line.strip() and not line.startswith('#'):
                    row = line.strip().split(delimiter)
                    if len(row) > max(instr_col, addr_col):
                        # Convert address to hex format without '0x' prefix if it's not already
                        addr = row[addr_col]
                        if not addr.startswith('0x'):
                            try:
                                # Try to convert from decimal to hex
                                addr = format(int(addr), 'x')
                            except ValueError:
                                # If conversion fails, keep as is
                                pass
                        else:
                            # Remove '0x' prefix if present
                            addr = addr[2:]
                        
                        f_out.write(f"{row[instr_col]} {addr}\n")
        else:  # default format
            for line in f_in:
                if line.strip() and not line.startswith('#'):
                    f_out.write(line)

def main():
    parser = argparse.ArgumentParser(description='Convert text file to ChampSim prefetch format')
    parser.add_argument('input_file', help='Path to input file')
    parser.add_argument('output_file', help='Path to output prefetch file')
    parser.add_argument('--format', default='default', choices=('default', 'csv'), 
                        help='Format of the input file (default: %(default)s)')
    parser.add_argument('--delimiter', default=',', 
                        help='Delimiter for CSV format (default: %(default)s)')
    parser.add_argument('--instr-col', default=0, type=int, 
                        help='Column index for instruction ID in CSV format (default: %(default)s)')
    parser.add_argument('--addr-col', default=1, type=int, 
                        help='Column index for prefetch address in CSV format (default: %(default)s)')
    
    args = parser.parse_args()
    
    convert_txt_to_prefetch(
        args.input_file, 
        args.output_file, 
        args.format, 
        args.delimiter, 
        args.instr_col, 
        args.addr_col
    )
    
    print(f"Conversion complete. Prefetch file saved to {args.output_file}")

if __name__ == '__main__':
    main()