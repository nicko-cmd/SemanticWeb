from openpyxl import load_workbook
from concepts import Context
import os
import csv
import re


def build_lattice(filename):
    filecsv = 'dataset.csv'
    attributes, cells = load_attributes_object(filename)
    create_csv_file(filecsv, attributes, cells)
    create_lattice_file(filecsv, filename)

    print('Lattice builted.')


def load_attributes_object(filename):
    workbook = load_workbook(filename)
    worksheet = workbook['Foglio1']

    dimension = worksheet.calculate_dimension()
    final_object_cell = re.split(':', dimension)[1]
    final_attribute_cell = re.findall('[A-Z]+', final_object_cell)[0] + '1'

    attributes = worksheet['A1':final_attribute_cell]
    cells = worksheet['A2':final_object_cell]

    return attributes, cells


def create_csv_file(filecsv, attributes, cells):
    row_list, l = [], []

    for attr in attributes[0]:
        l.append(attr.value)

    row_list.append(l)

    for row in cells:
        l = []
        l.append(row[0].value)
        for i in range(1, len(row)):
            l.append('X') if str(row[i].value) == '1' else l.append('')
        row_list.append(l)

    with open(filecsv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)


def create_lattice_file(filecsv, filename):
    lat = Context.fromfile(filecsv, frmat='csv').lattice
    os.remove(filecsv)

    path = '/data/lattices'
    filename = path + filename.replace('.xlsx', '.txt')

    with open(filename, 'w') as fp:
        fp.write(str(lat))

    # View lattice liake a graph
    # c.graphviz(filename="exampleLattice",view=True)
    # print('Lattice graph created')
