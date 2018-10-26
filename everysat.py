import argparse
import subprocess
import os

def preprocess(dimacs_in, dimacs_out):
    with open(dimacs_in, 'r') as i, open(dimacs_out, 'w') as o:
        for l in i:
            line = l.lstrip()
            if line.strip() == '' or line.split()[0] == 'c':
                continue
            else:
                o.write(line)


def solve(dimacs):
    # run it through minisat
    subprocess.call(['minisat', dimacs, 'out'])
    # grab output file o, if o is unsat, stop
    with open('out', 'r') as o:
        if o.readline().find('UNSAT') >= 0:
            return None
        else:
            return o.readline()


parser = argparse.ArgumentParser(description='Process a DIMACS file.')
parser.add_argument('in_file', type=str, help='the DIMACS file you want processed')
args = parser.parse_args()
everysat_cnf = 'everysat.cnf'
clauses = []
preprocess(args.in_file, everysat_cnf)

while True:
    clause = solve(everysat_cnf)
    if clause == None:
        break
    # grab the last output file, and the cnf file,
    clauses.append(clause)
    # copy the solution, negate the literals
    negation = ' '.join(str(-int(s)) for s in clause.split())+'\n'
    with open(everysat_cnf, 'r+') as eso:
        # edit header in the cnf input file
        header = eso.readline().split()
        header[-1] = str(int(header[-1])+1)
        eso.seek(0)
        eso.write(' '.join(header)+'\n')
        eso.seek(0,2)
        # append negated solution to cnf
        eso.write(negation)

for c in clauses:
    print('Found solution: {}.'.format(c.strip()))

os.remove('out')