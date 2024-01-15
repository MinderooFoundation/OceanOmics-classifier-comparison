import sys
print('Representative_Sequence\ttotal\tFake')
for line in open(sys.argv[1]):
    if line.startswith('>'):
        name = line.replace('>', '').rstrip()
        print(f'{name}\t1\t1')

