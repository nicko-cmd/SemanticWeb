from formal_concept import create_formal_concept
from lattice import build_lattice
from rules import generate_rules
from ontology import create_ontology

if __name__ == "__main__":
    path_data = '/data/datasets/'
    path_form = '/data/formal_concepts/'
    path_latt = '/data/lattices/'
    path_rule = '/data/rules/'
    filename = 'example.xlsx'

    dataset = path_data + filename
    formal_concept = path_form + filename
    lattice = path_latt + filename.replace('xlsx', 'txt')
    rules = path_rule + filename.replace('xlsx', 'txt')

    create_formal_concept(dataset, treshold=0.9)
    build_lattice(formal_concept)
    generate_rules(formal_concept)
    create_ontology(lattice, rules)
