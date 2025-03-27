#!/usr/bin/env python3

import argparse
import csv
import os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('results_file', help='Path to ChampSim results file')
    parser.add_argument('--cache-level', default='LLC', choices=('L2', 'LLC'), help='Cache level to compute stats for (default: %(default)s)')
    parser.add_argument('--base', default=None, help='Path to ChampSim base settings results file with no prefetcher for more accurate statistics')
    parser.add_argument('--format', default='default', choices=('default', 'csv'), help='Format of the prefetcher file (default: %(default)s)')
    parser.add_argument('--delimiter', default=',', help='Delimiter for CSV format (default: %(default)s)')
    parser.add_argument('--instr-col', default=0, type=int, help='Column index for instruction ID in CSV format (default: %(default)s)')
    parser.add_argument('--addr-col', default=1, type=int, help='Column index for prefetch address in CSV format (default: %(default)s)')

    return parser.parse_args()


def read_file(path, cache_level):
    if path is None:
        return None

    expected_keys = ('ipc', 'total_miss', 'useful', 'useless', 'load_miss', 'rfo_miss', 'kilo_inst')
    data = {}
    with open(path, 'r') as f:
        for line in f:
            if 'Finished CPU' in line:
                data['ipc'] = float(line.split()[9])
                data['kilo_inst'] = int(line.split()[4]) / 1000
            if cache_level not in line:
                continue
            line = line.strip()
            if 'LOAD' in line:
                data['load_miss'] = int(line.split()[-1])
            elif 'RFO' in line:
                data['rfo_miss'] = int(line.split()[-1])
            elif 'TOTAL' in line:
                data['total_miss'] = int(line.split()[-1])
            elif 'USEFUL' in line:
                data['useful'] = int(line.split()[-3])
                data['useless'] = int(line.split()[-1])

    if not all(key in data for key in expected_keys):
        return None

    return data


def convert_prefetcher_format(input_file, output_file, args):
    """Convert prefetcher file to ChampSim format"""
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        if args.format == 'csv':
            reader = csv.reader(f_in, delimiter=args.delimiter)
            for row in reader:
                if len(row) > max(args.instr_col, args.addr_col):
                    f_out.write(f"{row[args.instr_col]} {row[args.addr_col]}\n")
        else:  # default format
            for line in f_in:
                f_out.write(line)


def main(args=None):
    if args is None:
        args = get_args()

    # Convert prefetcher file if needed
    if args.format != 'default':
        temp_file = args.results_file + '.temp'
        convert_prefetcher_format(args.results_file, temp_file, args)
        args.results_file = temp_file

    results = read_file(args.results_file, args.cache_level)
    if results is None:
        print("Error: Could not read results file")
        return

    useful, useless, ipc, load_miss, rfo_miss, kilo_inst = (
        results['useful'], results['useless'], results['ipc'], results['load_miss'], results['rfo_miss'], results['kilo_inst']
    )
    results_total_miss = load_miss + rfo_miss + useful
    total_miss = results_total_miss

    results_mpki = (load_miss + rfo_miss) / kilo_inst

    base = read_file(args.base, args.cache_level)
    if base is not None:
        base_total_miss, base_ipc = base['total_miss'], base['ipc']
        base_mpki = base_total_miss / kilo_inst

    if useful + useless == 0:
        print('Accuracy: N/A [All prefetches were merged and were not useful or useless]')
    else:
        print('Accuracy:', useful / (useful + useless) * 100, '%')
    if total_miss == 0:
        print('Coverage: N/A [No misses. Did you run this simulation for long enough?]')
    else:
        print('Coverage:', useful / total_miss * 100, '%')
    print('MPKI:', results_mpki)
    if base is not None:
        print('MPKI Improvement:', (base_mpki - results_mpki) / base_mpki * 100, '%')
    print('IPC:', ipc)
    if base is not None:
        print('IPC Improvement:', (ipc - base_ipc) / base_ipc * 100, '%')

    # Clean up temporary file if created
    if args.format != 'default' and os.path.exists(temp_file):
        os.remove(temp_file)


if __name__ == '__main__':
    main()
