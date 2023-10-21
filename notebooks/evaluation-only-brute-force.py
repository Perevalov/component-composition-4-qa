import os
import sys
import random
from itertools import permutations
from tqdm.notebook import tqdm
from rdflib import Graph, Namespace, RDF
from snakes.nets import *

BATCH_SIZE = 3 * 10 ** 4

# os.chdir("..")

current_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))

# Add the parent directory to module search path
sys.path.append(parent_path)


from scripts.annotations import AnnotationQuestion, AnnotationOfInstance, AnnotationOfRelation, AnnotationOfAnswerSPARQL
from scripts.functions import parse_component, reachable, find_output_annotation_in_combination

data_dir = "./data/"
descriptions_dir = os.path.join(data_dir, "component-descriptions")

# Define the namespaces used in the RDF/Turtle file
QA = Namespace('https://w3id.org/wdaqua/qanary#')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')

combinations_len_list = []
reachable_combinations_len_list = []
pruned_reachable_combinations_len_list = []

n = 10
n_services_per_activity = int(sys.argv[1])
considered_types = ["NED", "REL", "QB"]

def combine_lists(lists):
        """
        Combines the provided list of lists into a list of tuples, where each tuple contains a component combination.
        N = n_1*n_2*...*n_k, where n_i is the length of the i-th list in lists and k is the length of the lists.

        Args:
            lists (_type_): a list of lists of actual components

        Returns:
            list: a list of tuples of actual components (combinations)
        """
        if not lists:
            return []
        elif len(lists) == 1:
            return [(x,) for x in lists[0]]
        else:
            result = []
            for item in lists[0]:
                for subitem in combine_lists(lists[1:]):
                    result.append((item,) + subitem)
            return result

for i in range(n):
    type_files_dict = dict()

    for _type in considered_types:
        type_files_dict[_type] = random.sample([file for file in os.listdir(descriptions_dir) if _type in file], n_services_per_activity)

    description_files = [value for value_list in type_files_dict.values() for value in value_list]

    components = []

    for file in description_files: # iterate over available component descriptions
        # Load the RDF/Turtle file into an rdflib graph
        try:
            g = Graph()
            with open(os.path.join(descriptions_dir, file), 'r') as f:
                g.parse(f, format='turtle')

            # Find the component type
            component_type = [t for t in g.triples((QA[file.replace('.ttl', '')], RDF.type, None))][0][2].toPython()
            # Find the component in the graph
            component_uri = QA[file.replace('.ttl', '')]
            component = parse_component(g, component_uri, component_type)
            components.append(component)
        except Exception as e:
            print(file)
            print(e)

    type_component_dict = {}

    # construct a dictionary mapping component types to actual components that have that type
    for component in components:
        type_component_dict[type(component)] = type_component_dict.get(type(component), []) + [component]

    len_permutations_dict = {}

    # construct a dictionary mapping the length of a permutation to all possible permutations of component types
    for k in range(1, len(type_component_dict.keys()) + 1):
        len_permutations_dict[k] = [p for p in permutations(type_component_dict.keys(), k)]
        
    combinations = []
    for length, abstract_perm in len_permutations_dict.items():
        for perm in abstract_perm:
            component_type_lists = [type_component_dict[component_type] for component_type in perm]
            combinations += combine_lists(component_type_lists)

    combinations_len_list.append(len(combinations))

print("------Results--------")
print((sum(combinations_len_list)/n))