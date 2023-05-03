from snakes.nets import Variable, Value
from rdflib import RDF


class AnnotationQuestion:
    token_value = 1
    def __init__(self, **kwargs):
        self.supported_languages = kwargs.get('https://w3id.org/wdaqua/qanary#supportedLanguages', [])

    def get_guard_expression(self):
        lang_part = 'or '.join([f'questionLang == \"{lang}\"' for lang in self.supported_languages])
        return f"(question == {self.token_value} and ({lang_part}))"

    def get_input_variables(self):
        return [Variable('question'), Variable('questionLang')]
    
class AnnotationOfInstance:
    token_value = 2
    def __init__(self, **kwargs):
        self.supported_knowledge_graphs = kwargs.get('https://w3id.org/wdaqua/qanary#supportedKnowledgeGraphs', [])

    def get_guard_expression(self):
        kg_part = 'or '.join([f'kgInstance == \"{kg}\"' for kg in self.supported_knowledge_graphs])
        return f"(instance == {self.token_value} and ({kg_part}))"
    
    def get_input_variables(self):
        return [Variable('instance'), Variable('kgInstance')]
    
    def get_output_variables(self):
        return [Variable('instance'), Variable('kgInstance')]
    
    def get_output_values(self):
        return [Value(self.token_value), Value(self.supported_knowledge_graphs[0])] # we assume that for the output annotation we only have one kg

class AnnotationOfRelation:
    token_value = 3
    def __init__(self, **kwargs):
        self.supported_knowledge_graphs = kwargs.get('https://w3id.org/wdaqua/qanary#supportedKnowledgeGraphs', [])

    def get_guard_expression(self):
        kg_part = 'or '.join([f'kgRelation == \"{kg}\"' for kg in self.supported_knowledge_graphs])
        return f"(relation == {self.token_value} and ({kg_part}))"
    
    def get_input_variables(self):
        return [Variable('relation'), Variable('kgRelation')]
    
    def get_output_variables(self):
        return [Variable('relation'), Variable('kgRelation')]
    
    def get_output_values(self):
        return [Value(self.token_value), Value(self.supported_knowledge_graphs[0])] # we assume that for the output annotation we only have one kg

class AnnotationOfAnswerSPARQL:
    token_value = 4
    def __init__(self, **kwargs):
        self.supported_knowledge_graphs = kwargs.get('https://w3id.org/wdaqua/qanary#supportedKnowledgeGraphs', [])

    def get_guard_expression(self):
        # used for input annotations
        kg_part = 'or '.join([f'kgAnswerSparql == \"{kg}\"' for kg in self.supported_knowledge_graphs])
        return f"(answer == {self.token_value} and ({kg_part}))"
    
    def get_input_variables(self):
        return [Variable('answerSparql'), Variable('kgAnswerSparql')]
    
    def get_output_variables(self):
        return [Variable('answerSparql'), Variable('kgAnswerSparql')]
    
    def get_output_values(self):
        return [Value(self.token_value), Value(self.supported_knowledge_graphs[0])] # we assume that for the output annotation we only have one kg

class Component:
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponent'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        self.uri = uri
        self.comment = comment
        self.label = label
        self.input_annotations = input_annotations
        self.output_annotations = output_annotations
        
    def __str__(self) -> str:
        value = self.uri.replace('https://w3id.org/wdaqua/qanary/', '')
        return f'{value}'
    
    def __repr__(self) -> str:
        value = self.uri.replace('https://w3id.org/wdaqua/qanary/', '')
        return f'{value}'

# TODO: define all compoenent types NER, NED, QB, etc.
class ComponentNER(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentNER'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentNED(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentNED'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentREL(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentREL'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentQB(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentQB'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

type_class_dict = {
    ComponentNER.uri_type: ComponentNER,
    ComponentNED.uri_type: ComponentNED,
    ComponentREL.uri_type: ComponentREL,
    ComponentQB.uri_type: ComponentQB    
}

component_query = """
    SELECT DISTINCT ?comment ?label WHERE {{
        <{component_uri}> rdfs:comment ?comment .
        <{component_uri}> rdfs:label ?label .
    }}
    LIMIT 1
"""

in_annotations_query = """
    SELECT DISTINCT ?Annotations ?AnnotationsProperty ?AnnotationsValue WHERE {{
        <{component_uri}> qa:hasInputAnnotations ?Annotations .
        ?Annotations ?AnnotationsProperty ?AnnotationsValue .
    }}
"""

out_annotations_query = """
    SELECT DISTINCT ?Annotations ?AnnotationsProperty ?AnnotationsValue WHERE {{
        <{component_uri}> qa:hasOutputAnnotations ?Annotations .
        ?Annotations ?AnnotationsProperty ?AnnotationsValue .
    }}
"""

def parse_annotations(query_results):
    annotation_value = {}
    # Extract the values from the query results
    for row in query_results:
        annotation_value[row.Annotations.toPython()] = annotation_value.get(row.Annotations.toPython(), {})
        annotation_value[row.Annotations.toPython()][row.AnnotationsProperty.toPython()] = annotation_value[row.Annotations.toPython()].get(row.AnnotationsProperty.toPython(), [])
        annotation_value[row.Annotations.toPython()][row.AnnotationsProperty.toPython()] = annotation_value[row.Annotations.toPython()][row.AnnotationsProperty.toPython()] + [row.AnnotationsValue.toPython()]
        
    annotations = []
    for annotation, value in annotation_value.items():
        if 'https://w3id.org/wdaqua/qanary#AnnotationOfInstance' in value[RDF.type.toPython()]:
            annotations.append(AnnotationOfInstance(**value))
        elif 'https://w3id.org/wdaqua/qanary#AnnotationOfRelation' in value[RDF.type.toPython()]:
            annotations.append(AnnotationOfRelation(**value))
        elif 'https://w3id.org/wdaqua/qanary#AnnotationQuestion' in value[RDF.type.toPython()]:
            annotations.append(AnnotationQuestion(**value))
        elif 'https://w3id.org/wdaqua/qanary#AnnotationOfAnswerSPARQL' in value[RDF.type.toPython()]:
            annotations.append(AnnotationOfAnswerSPARQL(**value))
    
    return annotations

def parse_component(graph, component_uri, component_type):
    input_results = graph.query(in_annotations_query.format(component_uri=component_uri))
    output_results = graph.query(out_annotations_query.format(component_uri=component_uri))
    component_results = graph.query(component_query.format(component_uri=component_uri))

    input_annotations = parse_annotations(input_results)
    output_annotations = parse_annotations(output_results)

    for row in component_results:
        return type_class_dict[component_type](uri=component_uri, comment=row.comment.toPython(), label=row.label.toPython(), input_annotations=input_annotations, output_annotations=output_annotations)
    
def reachable(n, marking_value):
    for transition in n.transition():
        modes = transition.modes() # get variable substitutions
        if len(modes) == 0: # deadlock
            return False
        
        transition.fire(modes[0]) # fire the transition

        for t in n.get_marking().keys():
            if marking_value in n.get_marking()[t].items(): # if the desired token is in the marking
                return True
    
    return False
