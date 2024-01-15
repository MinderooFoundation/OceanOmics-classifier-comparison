import sys
from random import randint
# #ID     Fake
# ASV_1   531
print('#ID\tFake\n')

for line in open(sys.argv[1]):
    if line.startswith('>'):
        name = line.split()[0].replace('>','')
        print(f'{name}\t{randint(400, 600)}')
