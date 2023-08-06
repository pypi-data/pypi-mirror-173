def write_to_file(findings, output_file_path):
    with open(output_file_path, 'a') as output_file:
        output_file.write('Id;Category;Subcategory;Rating;Description;Remediation\n')

        for anchor, finding in findings.items():
            output_file.write('{};{};{};{};{};{}\n'.format(anchor, finding['category'], finding['subcategory'],
                                                           finding['level'], finding['description'],
                                                           finding['remediation']['description'] if finding.get(
                                                               'remediation') else ''))


def write_to_stdout(findings):
    print('Id;Category;Subcategory;Rating;Description;Remediation')

    for anchor, finding in findings.items():
        print('{};{};{};{};{};{}\n'.format(anchor, finding['category'], finding['subcategory'],
                                           finding['level'], finding['description'],
                                           finding['remediation']['description'] if finding.get('remediation') else ''))
