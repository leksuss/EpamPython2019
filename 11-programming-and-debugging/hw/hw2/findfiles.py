import os
import argparse
from hashlib import sha256


def hash_file(file: str, block_size: int=65536) -> str:
    file_hash: str = sha256()
    with open(file, 'rb') as f:
        block: str = f.read(block_size)
        while block:
            file_hash.update(block)
            block: str = f.read(block_size)
    return file_hash.hexdigest()


def find_file_in(folder: str, hash: str) -> list:
    file_list: list[str] = []
    for root_path, dirs, files in os.walk(folder):
        for file in files:
            path_to_file: str = root_path.rstrip('/') + '/' + file
            if hash_file(path_to_file) == hash:
                file_list.append(path_to_file)
    return file_list


if __name__ == '__main__':
    parser: argparse.ArgumentParser
    parser = argparse.ArgumentParser(
        description='This utility iterates through files inside directory and \
        prints absolute path to files with equal calculated sha256 and given',
        prog='Get files by sha256',
    )
    parser.add_argument('-dir', help='absolute path to directory')
    parser.add_argument('-hash', help='sha256 hash of a searching file')
    args: list = parser.parse_args()
    file_list: list = find_file_in(args.dir, args.hash)
    print("\n".join(file_list) or "files not found")
