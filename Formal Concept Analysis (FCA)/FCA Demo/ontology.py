from collections import defaultdict
from collections import OrderedDict
from types import new_class
import re

from owlready2 import *

related = 0
implies = 0


def create_ontology(lattice, rules):
    """create an ontology from a lattice and add information from
    the association rules.

    Arguments:
        lattice (str): The lattice's file name
        rules (str): The association rules' file name
    """
    conf_th = 0.5
    concepts = {}

    # inizialitation
    ontology = get_ontology("http://example.org/data")

    intents = get_intents(lattice)

    for k in intents.keys():
        attributes = intents[k]
        for attr in attributes:
            flag = False
            if k == 1:
                create_concept(ontology, concepts, attr)
            else:
                for j in range(k+1, len(intents)+1):
                    if j in intents.keys():
                        for attr1 in intents[j]:
                            if sublist(attr, attr1):
                                flag = True
                                create_concept(ontology, concepts, attr)
                                diff = difference(attr1, attr)
                                # create ObjectProperty attr -> diff
                                create_object_property(ontology, concepts, attr, diff)
                        if flag:
                            break
                if k == 2 and not flag:
                    concept1 = f"['{attr[0]}']"
                    concept2 = f"['{attr[1]}']"
                    create_object_property(ontology, concepts, concept1, concept2)

    with open(rules, 'r') as fp:
        for rule in fp:
            conf, left, right = get_info(rule)
            if conf >= conf_th:
                create_implies_property(ontology, concepts, conf, left, right)

    file = '/data/ontology/' + lattice.replace('txt', 'owl')
    ontology.save(file="datasetOntology.owl", format="rdfxml")
    print('Created ontology.')


def create_concept(onto, concepts, attributes):
    """Create concept into ontology.

    Arguments:
        onto (): The ontology
        concepts (dict): A dict with concepts
        attributes (list): A list with attributes.
    """
    key = str(attributes)
    with onto:
        if key != "[]" and key not in concepts:
            concepts[key] = new_class(class_name(attributes), (Thing,))


def create_object_property(onto, concepts, c1, c2):
    """Create an Object Property into ontology.

    An Object Property relates two concept

    Arguments:
        onto (): The ontology
        concepts (dict): A dict with concepts
        c1 (list): The key of the first concept
        c2 (list): The key of the second concept
    """
    global related

    with onto:
        create_concept(onto, concepts, c2)
        C1 = concepts[str(c1)]
        C2 = concepts[str(c2)]

        # create Object Property
        property_name = 'isRelated' + str(related)
        property = type(property_name, (ObjectProperty,), {"domain": [C1], "range": [C2]})
        related += 1
        #create Inverse Property
        inverse_property_name = 'isRelated' + str(related)
        type(inverse_property_name, (ObjectProperty,), {"domain": [C2], "range": [C1],"inverse_property":property})
        related += 1


def create_implies_property(onto, concepts, conf, c1, c2):
    """Create an Implies Property into ontology.

    An Implies Property relates two concept through a level of confidence;
    this is taken from the association rules

    Arguments:
        onto (): The ontology
        concepts (dict): A dict with concepts
        conf (str): The level of confidence
        c1 (list): The key of the first concept
        c2 (list): The key of the second concept
    """
    global implies
    with onto:
        create_concept(onto, concepts, c1)
        create_concept(onto, concepts, c2)

        C1 = concepts[str(c1)]
        C2 = concepts[str(c2)]

        # create Implies Property
        label = f'Confidence: {conf}'
        property_name = 'Implies' + str(implies)
        type(property_name, (ObjectProperty,), {"domain": [C1], "range": [C2], "label": label})
        implies += 1


def get_intents(filename):
    """Get intents from the lattice.

    Return an ordere map of intents (k: #intents, v: list)

    Arguments:
        filename (str): Lattice's file (.txt)
    Returns:
        intents (OrderedDict): A dict with intents
    """
    map = defaultdict(list)
    regex = "(?<=\\[).+?(?=\\])"

    with open(filename, 'r') as fp:
        lines = fp.readlines()

    lines_to_read = len(lines) - 1
    # first and last lines are useless
    for i in range(2, lines_to_read):
        # find intent
        tmp = re.findall(regex, lines[i])[0].split(' ')
        map[len(tmp)].append(tmp)
    return OrderedDict(sorted(map.items()))


def get_info(rule):
    """Get info from association rule.

    The format of a rule is:
        [attributesA] => [attributesB] (conf: x)

    Arguments:
        rule (str): A association rule

    Returns:
        conf (str): The value of connfidence
        left (str): A list with 'attributesA'
        right (str): A list with 'attributesB'
    """
    rconf, rattr = "[0-9.]+", "\\[.*?\\]"
    conf = float(findall(rconf, rule)[0])
    attr = findall(rattr, rule)
    left = attr[0].replace(" ", "")
    right = attr[1].replace(" ", "")

    return conf, left, right


def class_name(list):
    """Create a name from a list

    Arguments:
        list (list): A list with strings
    Returns:
        name (str)
    """
    if type(list) is str:
        return list.replace('\'', '').replace('[', '').replace(']', '')
    else:
        name = ""
        end = list[len(list)-1]
        for l in list:
            if l == end:
                name = name + l
            else:
                name = name + l + ","
        return name


def sublist(lst1, lst2):
    """Returns True if all the element of the list1 
    are contained in the list2, False otherwise.

    Arguments:
        list1 (list): The first list
        list2 (list): The second list
    """
    for el in lst1:
        if el not in lst2:
            return False
    return True


def difference(lst1, lst2):
    """Subtract element of the first list from the second.

    Arguments:
        list1 (list): The first list
        list2 (list): The second list
    Returns:
        diff (list): The remaining elements
    """
    diff = []
    for i in lst1:
        if i not in lst2:
            diff.append(i)
    return diff
