import argparse
import pathlib
from onlyfirst import onlyfirst


def main():
    parser = argparse.ArgumentParser("only first word remains")
    parser.add_argument('file', help='file path')
    args = parser.parse_args()
    if args.file:
        file_path = pathlib.Path(args.file)
        if file_path.exists():
            res = onlyfirst.process_paragraph(file_path.read_text())
            new_path = args.file + '.new'
            pathlib.Path(new_path).write_text(res)
            print(f'{new_path} is added.')
    else:
        print('No files in.')
