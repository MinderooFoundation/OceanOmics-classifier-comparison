import sys
for line in open(sys.argv[1]):
    if line.startswith('>'):
        line = line.split(' ')[0]
        if not line.endswith('.1'):
            line = line + '.1'
        line += '\n'
    print(line, end ='')
