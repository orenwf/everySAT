import argparse
import subprocess
import os

parser = argparse.ArgumentParser(description='Process a DIMACS file.')
parser.add_argument('in_file', type=str, help='the DIMACS file you want processed')
args = parser.parse_args()
everysat_cnf = 'everysat.cnf'
out = 'm.out'
subprocess.call(['cp', args.in_file, everysat_cnf])
clauses = []

def solve(count):
    # run it through minisat
    subprocess.call(['minisat', everysat_cnf, out])
    # grab output file o, if o is unsat, stop
    with open(out, 'r') as o:
        if o.readline().find('UNSAT') >= 0:
            print('Finished after {} tries'.format(str(count)))
            return None
        else:
            return o.readline()


while True:
    clause = solve(len(clauses)+1)
    if clause == None:
        break
    # grab the last output file, and the cnf file,
    clauses.append(clause)
    # copy the solution, negate the literals
    negation = ' '.join([str(-int(s)) for s in clause.split()])+'\n'
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
    print('Found additional solution: {}.'.format(c.strip()))

os.remove(out)