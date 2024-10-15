import base64
import ntpath
import sys
from pathlib import Path

lines_per_file = 240000


def encode_file(input, output):
    base64.encode(open(input, "rb"), open(output, "wb"))


def main():
    file = sys.argv[1]

    base64_filename = file + '.base64'
    encode_file(file, base64_filename)

    smallfile = None
    index = 0
    small_files_dir = base64_filename + '_parts'
    Path(small_files_dir).mkdir(exist_ok=True)
    with open(base64_filename, encoding='utf8') as in_f:
        for lineno, line in enumerate(in_f):
            if lineno % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                name = f'{small_files_dir}/{ntpath.split(base64_filename)[1]}-{index}.part'
                smallfile = open(name, 'w', encoding='utf8')
                index += 1
            smallfile.write(line)
        if smallfile:
            smallfile.close()

    Path(base64_filename).unlink()
    print('written file in to ' + small_files_dir)


if __name__ == '__main__':
    if len(sys.argv) <= 1 or not Path(sys.argv[1]).is_absolute():
        print('need absolute path to file in 1st arg')
        sys.exit(1)
    else:
        main()
