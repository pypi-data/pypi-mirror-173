# kube-bench-report-converter

Converts kube-bench execution console output to a CSV report.

## Install

### PyPI

    pip install -U kube-bench-report-converter

### Source

    git clone git@github.com:build-failure/kube-bench-report-converter.git
    cd kube-bench-report-converter/
    pip install .

## Use


    cat kube-bench.log | kube-bench-report-converter > kube-bench-report.csv
    
or
    
    kube-bench-report-converter --input_file_path 'kube-bench.log' --output_file_path 'kube-bench-report.csv'
    
## Arguments

| Name | Description | Default |
|---|---|---|
| input_file_path  | kube-bench execution console output. | Read from stdin. |
| output_file_path  | kube-bench CSV report file path. | Write to stdout. |