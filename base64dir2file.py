import sys
from os.path import isfile, join, isdir
from os import listdir, system, remove
from re import split

if len(sys.argv) <= 1:
    print('need absolute path to dir with files in 1st arg')
    sys.exit(1)

dir = sys.argv[1]
if not isdir(dir):
    print('need absolute path to dir with files in 1st arg')
    sys.exit(1)


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


files = [f for f in listdir(dir) if isfile(join(dir, f))]
files = natural_sort(files)

file = [f for f in files if '-0.part' in f][0].replace('-0.part', '')
with open(f'{dir}/{file}', 'w', encoding='utf8') as out_f:
    for _file in files:
        with open(dir + '/' + _file, 'r', encoding='utf8') as in_f:
            out_f.write(in_f.read())
new_file_name = file.replace(".base64", "")
system(f'openssl base64 -d -in "{dir}/{file}" -out "{dir}/{new_file_name}"')
remove(f'{dir}/{file}')
print(f'file written in {dir}/{new_file_name}')
