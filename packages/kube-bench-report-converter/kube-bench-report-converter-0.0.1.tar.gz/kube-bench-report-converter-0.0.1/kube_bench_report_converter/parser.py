import re
import sys

FINDING = '['
REMEDIATION_SECTION = '== Remediations'
SUMMARY_SECTION = '== Summary'
STATUS_PATTERN = re.compile('\\[([a-zA-Z]+)]\\s([0-9.]+)\\s(.*)')
ANCHOR_PATTERN = re.compile('[0-9]*\\.*([0-9]*)\\.*([0-9]*)')
REMEDIATION_PATTERN = re.compile('([0-9]+\\.[0-9]+\\.[0-9]+)\\s(.*)')


def parse_finding_details(value):
    match = STATUS_PATTERN.match(value)
    level = match.group(1)
    anchor = match.group(2)
    description = match.group(3)
    section = ANCHOR_PATTERN.match(anchor)
    subcategory = section.group(1) if len(section.groups()) > 0 else None
    finding = section.group(2) if len(section.groups()) > 1 else None

    return {
        'level': level,
        'anchor': anchor,
        'description': description,
        'is_category': not finding and not subcategory,
        'is_subcategory': subcategory and not finding
    }


def parse_remediation(value):
    match = REMEDIATION_PATTERN.match(value)
    anchor = match.group(1)
    description = match.group(2).rstrip()

    return {
        'anchor': anchor,
        'description': description
    }


def is_remediation_start(value):
    return REMEDIATION_PATTERN.match(value)


def is_summary_section(value):
    return value.startswith(SUMMARY_SECTION)


def is_remediation_section(value):
    return value.startswith(REMEDIATION_SECTION)


def is_finding(value):
    return value.startswith(FINDING)


def parse_line(line, context, findings):
    if is_summary_section(line):
        return False

    if not context['remediation_section']:
        context['remediation_section'] = is_remediation_section(line)

    if context['remediation_section']:
        if is_remediation_start(line):
            context['remediation_details'] = parse_remediation(line)
            findings[context['remediation_details']['anchor']]['remediation'] = context['remediation_details']
        elif line and context['remediation_details']:
            context['remediation_details']['description'] += ' ' + line.rstrip()

    if is_finding(line):
        finding_details = parse_finding_details(line)
        if finding_details['is_category']:
            context['category'] = finding_details['description']
        elif finding_details['is_subcategory']:
            context['subcategory'] = finding_details['description']
        else:
            finding_details['category'] = context['category']
            finding_details['subcategory'] = context['subcategory']
            findings[finding_details['anchor']] = finding_details

    return True


def parse_from_stdin():
    findings = {}
    context = {
        'remediation_section': False,
        'remediation_details': {},
        'category': '',
        'subcategory': ''
    }

    for line in sys.stdin:
        if not parse_line(line, context, findings):
            break

    return findings


def parse_from_file(input_file_path):
    findings = {}
    context = {
        'remediation_section': False,
        'remediation_details': {},
        'category': '',
        'subcategory': ''
    }

    with open(input_file_path) as input_file:
        for line in input_file:
            if not parse_line(line, context, findings):
                break

    return findings
