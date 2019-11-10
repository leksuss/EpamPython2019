""""

Задание 1

0) Повторение понятий из биологии (ДНК, РНК, нуклеотид, протеин, кодон)

1) Построение статистики по входящим в последовательность ДНК нуклеотидам 
для каждого гена (например: [A - 46, C - 66, G - 23, T - 34])

2) Перевод последовательности ДНК в РНК (окей, Гугл)

3) Перевод последовательности РНК в протеин*


*В папке files вы найдете файл rna_codon_table.txt - 
в нем содержится таблица переводов кодонов РНК в аминокислоту, 
составляющую часть полипептидной цепи белка.


Вход: файл dna.fasta с n-количеством генов

Выход - 3 файла:
 - статистика по количеству нуклеотидов в ДНК
 - последовательность РНК для каждого гена
 - последовательность кодонов для каждого гена

 ** Если вы умеете в matplotlib/seaborn или еще что, 
 welcome за дополнительными баллами за
 гистограммы по нуклеотидной статистике.
 (Не забудьте подписать оси)

P.S. За незакрытый файловый дескриптор - караем штрафным дезе.

"""

# read the file dna.fasta
import os


def translate_from_dna_to_rna(dna):

    '''Перевод последовательности ДНК в РНК'''

    rna = dna.replace('T', 'U')
    return rna


def count_nucleotides(dna):

    '''Построение статистики по входящим в
    последовательность ДНК нуклеотидам длякаждого гена'''

    num_of_nucleotides = {}
    for i in dna:
        if i not in num_of_nucleotides:
            num_of_nucleotides[i] = 0
        num_of_nucleotides[i] += 1
    return num_of_nucleotides


def rna_to_protein_mapping(path_to_file):

    '''Извлекает из файла соответствие RNA<->protein
    Получает путь к файлу, возвращает словарь'''

    path, file = os.path.split(path_to_file)
    rna_to_protein_dict = {}
    with open(os.path.join(path, file)) as file:
        for line in file:
            for item in line.split('   '):
                if item:
                    convert_pair = item.strip().split()
                    rna_to_protein_dict[convert_pair[0]] = convert_pair[1]
    return rna_to_protein_dict


def translate_rna_to_protein(rna, rna_to_protein_map):

    '''Перевод последовательности РНК в протеин'''

    protein = []
    for i in range(0, len(rna), 3):
        rna_block = rna[i:i + 3]
        if rna_block in rna_to_protein_map:
            protein.append(rna_to_protein_map[rna_block])
        else:
            raise Exception("Non-valid RNA!")
    return protein


# file names we are working
files_dir = 'files'
dna_source_file = 'dna.fasta'
rna_codon_map_file = 'rna_codon_table.txt'
dna_stats_res_file = 'dna_stats.txt'
rna_res_file = 'rna.txt'
codon_res_file = 'codon.txt'

# read source dna file
genes = {}
with open(os.path.join(files_dir, dna_source_file)) as file:
    for line in file:
        if line.startswith('>'):
            gene_title = line.strip('>\n')
            genes[gene_title] = ''
        else:
            genes[gene_title] += line.strip()

# calc DNA statistics and write it to the file
with open(os.path.join(files_dir, dna_stats_res_file), 'w') as file:
    for gene_title, gene in genes.items():
        file.write('>' + gene_title + '\n')
        stats = count_nucleotides(gene)
        stats_list = [dna + ' - ' + str(stats[dna]) for dna in sorted(stats)]
        file.write(', '.join(stats_list) + '\n')


