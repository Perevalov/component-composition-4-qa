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

def create_nets_batch(combinations: list):
        nets = []

        for combination in combinations: # a single combination refers to a single petri net
            n = PetriNet(' --> '.join(str(c) for c in combination))
            
            n.add_place(Place('questionPlace', [1, 'http://id.loc.gov/vocabulary/iso639-1/en'])) # assume english question on start

            for component in combination:
                place_name = str(component) + 'Place'
                transition_name = str(component) + 'Transition'
                n.add_place(Place(place_name, []))
                n.add_transition(Transition(name=transition_name, guard=Expression(' and '.join([a.get_guard_expression() for a in component.input_annotations]))))
                
            prev_variables = []
            for i in range(len(combination)):
                input_variables = list(set([v for ia in combination[i].input_annotations for v in ia.get_input_variables()]))
                input_variables = [v for v in prev_variables if v not in input_variables and type(v) != Value] + input_variables # add those prev_variables that are not in input_variables
                output_values = list(set([v for oa in combination[i].output_annotations for v in oa.get_output_values()]))
                
                n.add_input(n.place()[i].name, n.transition()[i].name, MultiArc(input_variables))
                n.add_output(n.place()[i + 1].name, n.transition()[i].name, MultiArc(input_variables + output_values))
                
                output_variables = list(set([v for oa in combination[i].output_annotations for v in oa.get_output_variables()]))
                prev_variables = input_variables + output_variables

            nets.append(n)
        
        return nets

def prune_reachable(combinations):
    comb_size_dict = dict()
    for comb in combinations:
        size = len(str(comb).split(" --> "))
        comb_size_dict[str(comb)] = size

    _min = min(list(comb_size_dict.values()))

    filtered_dict = {key: value for key, value in comb_size_dict.items() if value == _min}
    return list(filtered_dict.keys())

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

    reachable_combinations = []
    for i in tqdm(range(0, len(combinations), BATCH_SIZE)): # we use a batch size to avoid memory issues
        if i + BATCH_SIZE > len(combinations):
            nets = create_nets_batch(combinations[i:])
        else:
            nets = create_nets_batch(combinations[i:i + BATCH_SIZE])
        
        for i in tqdm(range(len(nets))):
            annotation = AnnotationOfAnswerSPARQL # search for this as a produced token in the net
            if find_output_annotation_in_combination(annotation, combinations[i]): # theoretical possibility that the annotation is in the combination
                if reachable(nets[i], annotation.token_value):
                    print(nets[i], "Success!")
                    reachable_combinations.append(nets[i])
                else:
                    print(nets[i], "Failure!")
        
        del nets

    combinations_len_list.append(len(combinations))
    reachable_combinations_len_list.append(len(reachable_combinations))
    # pruned_reachable_combinations_len_list.append(len(prune_reachable(reachable_combinations)))

print("------Results--------")
print((sum(combinations_len_list)/n))
print((sum(reachable_combinations_len_list)/n))
# print((sum(pruned_reachable_combinations_len_list)/n))