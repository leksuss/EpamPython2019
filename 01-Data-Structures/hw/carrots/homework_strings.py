import os


def translate_from_dna_to_rna(dna):

    """Convert DNA to RNA"""

    rna = dna.replace('T', 'U')
    return rna


def count_nucleotides(dna):

    """Count nucleotides in DNA"""

    num_of_nucleotides = {}
    for i in dna:
        if i not in num_of_nucleotides:
            num_of_nucleotides[i] = 0
        num_of_nucleotides[i] += 1
    return num_of_nucleotides


def rna_to_protein_mapping(path_to_file):

    """Extract from file RNA<->protein mapping and return dict"""

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

    """Convert RNA to protein"""

    protein = []
    for i in range(0, len(rna), 3):
        rna_block = rna[i:i + 3]
        if rna_block in rna_to_protein_map:
            protein.append(rna_to_protein_map[rna_block])
        else:
            print('Non-valid RNA! Position:', i, 'block:', rna_block)
    return protein


# file names we are working
files_dir = 'files/'
dna_source_file = 'dna.fasta'
rna_codon_map_file = 'rna_codon_table.txt'
dna_stats_res_file = 'dna_stats.txt'
rna_res_file = 'rna.txt'
codon_res_file = 'protein.txt'

# read source dna file
genes = {}
with open(os.path.join(files_dir, dna_source_file)) as file:
    for line in file:
        if line.startswith('>'):
            gene_title = line.strip('>\n')
            genes[gene_title] = ''
        else:
            genes[gene_title] += line.strip()
if len(genes):
    print(f'Data from file "{dna_source_file}" loaded sucessfuly')
else:
    print('No genes was found :(')
    exit()

# calc DNA statistics and write it to the file
with open(os.path.join(files_dir, dna_stats_res_file), 'w') as file:
    for gene_title, gene in genes.items():
        file.write('>' + gene_title + '\n')
        stats = count_nucleotides(gene)
        stats_list = [dna + ' - ' + str(stats[dna]) for dna in sorted(stats)]
        file.write(', '.join(stats_list) + '\n')
if os.path.getsize(os.path.join(files_dir, dna_stats_res_file)) != 0:
    print(f'DNA statistics has been written to "{dna_stats_res_file}" file')

# convert DNA to RNA write result to the file
with open(os.path.join(files_dir, rna_res_file), 'w') as file:
    for gene_title, gene in genes.items():
        file.write('>[RNA] ' + gene_title + '\n')
        file.write(translate_from_dna_to_rna(gene) + '\n')
if os.path.getsize(os.path.join(files_dir, rna_res_file)) != 0:
    print(f'DNA has been converted to RNA & written to "{rna_res_file}" file')

# convert RNA to protein and write result to the file
with open(os.path.join(files_dir, codon_res_file), 'w') as file:
    rna_protein = rna_to_protein_mapping(files_dir + rna_codon_map_file)
    for gene_title, gene in genes.items():
        file.write('>[protein] ' + gene_title + '\n')
        rna = translate_from_dna_to_rna(gene)
        file.write(''.join(translate_rna_to_protein(rna, rna_protein)) + '\n')
if os.path.getsize(os.path.join(files_dir, rna_res_file)) != 0:
    print(f'DNA has been converted to RNA & written to "{rna_res_file}" file')
