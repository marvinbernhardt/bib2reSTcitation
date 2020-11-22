#!/usr/bin/env python3

import argparse
import sys
import re


def displaymatch(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())


def bib2rest(input_bibfile, output_txtfile):
    fields = ('author', 'title', 'journal', 'year', 'doi')
    patterns = {field: re.compile(r"^(?: |\t)*" + field + r"[ \t]*=[ \t]*\{(.+)\}(?: |\t)*,(?: |\t)*$", re.IGNORECASE) for field in fields}
    start_pattern = re.compile(r"^(?: |\t)*\@(book|article|incollection|inproceedings)\{(.+), *$")
    end_pattern = re.compile("^(?: |\t)*}(?: |\t)*$")
    with open(input_bibfile, 'r') as input_handle, open(output_txtfile, 'w') as output_handle:
        in_a_bib_block = False
        ref_data = {}
        output_handle.write("Bibliography\n============\n\n")
        for line in input_handle:
            if not in_a_bib_block:
                if start_pattern.match(line):
                    matches = start_pattern.match(line)
                    in_a_bib_block = True
                    ref_data = {}
                    ref_data['type'] = matches.group(1)
                    ref_data['key'] = matches.group(2)
                else:
                    pass
            else:
                # in a bib block
                if end_pattern.match(line):
                    in_a_bib_block = False
                    rest_ref_block = '.. [' + ref_data['key'] + '] '
                    for f, field in enumerate((field for field in fields
                                               if field in ref_data)):
                        if f > 0:
                            rest_ref_block += ', '
                        if field == 'doi':
                            rest_ref_block += 'https://dx.doi.org/'
                        rest_ref_block += ref_data[field]
                    output_handle.write(rest_ref_block + "\n")
                for field in fields:
                    if patterns[field].match(line):
                        ref_data[field] = patterns[field].match(line).group(1)
                else:
                    pass


if __name__ == '__main__':
    throot = "/".join(sys.path[0].split("/")[:])
    parser = argparse.ArgumentParser(description='bib2reSTcitation is a tool to convert bib tex file to reStructuredText Markup citation format.')
    parser.add_argument('-o', '--output', help='output file path')
    parser.add_argument('-i', '--input', help='input file path')
    args = parser.parse_args()
    input_file = args.input
    if input_file is None:
        input_file = 'tex.bib'
    output_file = args.output
    if output_file is None:
        output_file = "references.txt"
    bib2rest(input_file, output_file)
