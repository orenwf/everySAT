import argparse
import subprocess
import shutil

PARSER = argparse.ArgumentParser(description='Process a DIMACS file.')
PARSER.add_argument('in_file', type=str,
                    help='the DIMACS file you want processed')
PARSER.add_argument('out_file', type=str, help='the name of the output file')
ARGS = PARSER.parse_args()
EVERYSAT_CNF = 'everysat.cnf'

def run():
    shutil.copyfile(ARGS.in_file, EVERYSAT_CNF)
    count = 1
    # grab output file o, if o is unsat, stop
    while solve(str(count)):
        # grab the last output file, and the cnf file,
        with open(ARGS.out_file, "r") as o, open(EVERYSAT_CNF, "r+") as eso:
            o.readline()
            # copy the solution, negate the literals
            negation = ' '.join([str(-int(s)) for s in o.readline().split()])+'\n'
            # edit header in the cnf input file
            header = eso.readline().split()
            header[-1] = str(int(header[-1])+1)
            eso.seek(0)
            eso.write(' '.join(header)+'\n')
            eso.seek(0,2)
            # append negated solution to cnf
            eso.write(negation)
        
        if count > 1000:
            break
        count += 1


def solve(count):
    # run it through minisat
    subprocess.run(["minisat", EVERYSAT_CNF, ARGS.out_file])
    with open(ARGS.out_file, "r") as o:
        if o.readline().find("UNSAT") >= 0:
            print('Finished after {} tries'.format(count))
        else:
            return True


if __name__ == "__main__":
    run()
