import ntpath
import sys

from os.path import isabs
from os import system, mkdir, remove

if len(sys.argv) <= 1:
    print('need absolute path to file in 1st arg')
    sys.exit(1)

file = sys.argv[1]
if not isabs(file):
    print('need absolute path to file in 1st arg')
    sys.exit(1)

base64_filename = file + '.base64'
system(f'openssl base64 -in "{file}" -out "{base64_filename}"')

lines_per_file = 320000
smallfile = None
index = 0
small_files_dir = base64_filename + '_parts'
mkdir(small_files_dir)
with open(base64_filename, encoding='utf8') as in_f:
    for lineno, line in enumerate(in_f):
        if lineno % lines_per_file == 0:
            if smallfile:
                smallfile.close()
            smallfile = open(f'{small_files_dir}/{ntpath.split(base64_filename)[1]}-{index}.part', 'w', encoding='utf8')
            index += 1
        smallfile.write(line)
    if smallfile:
        smallfile.close()

remove(base64_filename)
print('written file in to ' + small_files_dir)
