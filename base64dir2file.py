import base64
import sys
from os import listdir
from os.path import isfile, join
from pathlib import Path
from re import split


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def decode_file(input, output):
    base64.decode(open(input, "rb"), open(output, "wb"))


def main():
    dir = sys.argv[1]

    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    files = natural_sort(files)

    file = [f for f in files if '-0.part' in f][0].replace('-0.part', '')
    with open(f'{dir}/{file}', 'w', encoding='utf8') as out_file:
        for _file in files:
            with open(dir + '/' + _file, 'r', encoding='utf8') as in_file:
                out_file.write(in_file.read())
    new_file_name = file.replace(".base64", "")
    decode_file(f'{dir}/{file}', f'{dir}/{new_file_name}')
    Path(f'{dir}/{file}').unlink()
    print(f'file written in {dir}/{new_file_name}')


if __name__ == '__main__':
    if len(sys.argv) <= 1 or not Path(sys.argv[1]).is_dir():
        print('need absolute path to dir with files in 1st arg')
        sys.exit(1)
    else:
        main()
