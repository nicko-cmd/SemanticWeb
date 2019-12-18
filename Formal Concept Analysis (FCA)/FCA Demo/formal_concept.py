from openpyxl import load_workbook
import re


def create_formal_concept(filename, treshold):
    workbook = load_workbook(filename)
    worksheet = workbook['Foglio1']

    dimension = worksheet.calculate_dimension()
    final_object_cell = re.split(':', dimension)[1]

    cells_value = worksheet['B2':final_object_cell]

    # Find the minimum value
    min_value = 1000
    for row in cells_value:
        for cell in row:
            if float(cell.value) < min_value:
                min_value = float(cell.value)

    threshold = 0.9
    # Normalize cells value and apply threshold
    for row in cells_value:
        for cell in row:
            if float(cell.value) - min_value < threshold:
                cell.value = '0'
            else:
                cell.value = '1'

    path = '/data/formal_concepts/'
    formal_concept = path + filename
    workbook.save(formal_concept)

    print('Formal Concept created.')
