"""
Реализовать метод __str__, позволяющий выводить все папки и файлы из данной, например так:
> print(folder1)
V folder1
|-> V folder2
|   |-> V folder3
|   |   |-> file3
|   |-> file2
|-> file1
А так же возможность проверить, находится ли файл или папка в другой папке:
> print(file3 in folder2)
True
"""
import os


class PrintableFolder:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        printable = ''
        for root_path, _, files in os.walk(self.name):
            current_level = root_path.count(os.sep) - self.name.count(os.sep)
            indent = '|----' * current_level
            printable += indent + '[' + os.path.basename(root_path) + ']\n'
            for file in files:
                printable += indent + '|----' + file + '\n'
        return printable

    def __contains__(self, item):
        for root_path, dirs, files in os.walk(self.name):
            if item in files or item in dirs:
                return True
        return False


folder = PrintableFolder('sample_dir_structure')

print(folder)
print('zzzet' in folder)
print('т е с т.py' in folder)
print('absent_file' in folder)
