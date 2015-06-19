#!/usr/bin/env python

import sys, yaml
import os, re

def fix_latex(line):
    corr = re.match('.*(href{}).*',line)
    if corr:
        line = line.replace(corr.group(1), "path")
    corr = re.match('.*begin{lstlisting}',line)
    if corr:
        line = "\leavevmode" + line

    corr = re.match('.*section{APIs}.*',line)
    if corr:
        line = "\leavevmode\pagebreak\n" + line

    corr = re.match('(.*includegraphics)(.*btstack-architecture.*)',line)
    if corr:
        line = corr.group(1) + "[width=\\textwidth]" + corr.group(2)

    corr = re.match('(.*includegraphics)(.*singlethreading-btstack.*)',line)
    if corr:
        line = corr.group(1) + "[width=0.3\\textwidth]" + corr.group(2)

    corr = re.match('(.*includegraphics)(.*multithreading-monolithic.*)',line)
    if corr:
        line = corr.group(1) + "[width=0.8\\textwidth]" + corr.group(2)

    corr = re.match('(.*includegraphics)(.*multithreading-btdaemon.*)',line)
    if corr:
        line = corr.group(1) + "[width=0.8\\textwidth]" + corr.group(2)

    corr = re.match('(.*includegraphics)(.*btstack-protocols.*)',line)
    if corr:
        line = corr.group(1) + "[width=0.8\\textwidth]" + corr.group(2)

    return line


def main(argv):
    docs_folder = "docs"
    yml_file = "mkdocs.yml"
    mk_file  = "latex/btstack_generated.md"

    with open(mk_file, 'w') as aout:
        with open(yml_file, 'r') as yin:
            doc = yaml.load(yin)
            for page in doc["pages"]:
                md_file = page[0]
                title = page[1]
                with open(docs_folder +"/"+ md_file, 'r') as mdin:
                    aout.write("\n\n#"+ title +"\n\n")
                    for line in mdin:
                        # remove path from section reference
                        # e.g. [the SPP Counter example](examples/generated/#sec:sppcounterExample)
                        # replace with [the SPP Counter example](#sec:sppcounterExample)
                        section_ref = re.match('.*\(((.*)(#sec:.*))\).*',line)
                        if section_ref:
                            line = line.replace(section_ref.group(2),"")
                        aout.write(line)               

    pandoc_cmd = "pandoc -f markdown -t latex --filter pandoc-fignos --listings latex/btstack_generated.md -o latex/btstack_generated.tex"
    p = os.popen(pandoc_cmd,"r")
    while 1:
        line = p.readline()
        if not line: break
        print line


    # btstatck_root_file = "latex/btstack_gettingstarted.tex"
    btstack_generated_file = "latex/btstack_generated.tex"
    btstack_final_file = "latex/btstack_final.tex"

    with open(btstack_final_file, 'w') as aout:
        aout.write("% !TEX root = btstack_gettingstarted.tex\n\n")

        with open(btstack_generated_file, 'r') as fin:
            for line in fin:
                line = fix_latex(line)
                aout.write(line)       
             

if __name__ == "__main__":
   main(sys.argv[1:])