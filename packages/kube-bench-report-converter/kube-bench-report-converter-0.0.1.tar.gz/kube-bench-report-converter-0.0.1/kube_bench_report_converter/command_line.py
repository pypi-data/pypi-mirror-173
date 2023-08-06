import argparse

from kube_bench_report_converter import parser as report_parser
from kube_bench_report_converter import writer as report_writer


def main():
    parser = argparse.ArgumentParser(description='Converts kube-bench checks console output to CSV format.')
    parser.add_argument('--output_file_path', default=None, help='kube-bench CSV report file path.')
    parser.add_argument('--input_file_path', default=None, help='kube-bench execution console output.')

    args = parser.parse_args()

    if args.input_file_path:
        findings = report_parser.parse_from_file(args.input_file_path)
    else:
        findings = report_parser.parse_from_stdin()

    if args.output_file_path:
        report_writer.write_to_file(findings, args.output_file_path)
    else:
        report_writer.write_to_stdout(findings)
