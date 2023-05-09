from rdflib import RDF
from scripts.annotations import AnnotationOfInstance, AnnotationOfRelation, AnnotationQuestion, AnnotationOfAnswerSPARQL
from scripts.components import type_class_dict


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
    """Parse the annotations from the query results

    Args:
        query_results (generator object): a list of query results item.Annotations, item.AnnotationsProperty

    Returns:
        list: a list of annotations
    """
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
        # TODO: add other annotation types
    
    return annotations

def parse_component(graph, component_uri, component_type):
    """Parse the annotations from the query results

    Args:
        graph (rdflib.Graph): a graph based on an RDF/TTL description of the component
        component_uri (str): the URI of the component
        component_type (Component): the type of the component

    Returns:
        Component: an instantiated component
    """
    input_results = graph.query(in_annotations_query.format(component_uri=component_uri))
    output_results = graph.query(out_annotations_query.format(component_uri=component_uri))
    component_results = graph.query(component_query.format(component_uri=component_uri))

    input_annotations = parse_annotations(input_results)
    output_annotations = parse_annotations(output_results)

    for row in component_results:
        return type_class_dict[component_type](uri=component_uri, comment=row.comment.toPython(), label=row.label.toPython(), input_annotations=input_annotations, output_annotations=output_annotations)
    
def reachable(n, marking_value):
    # TODO: if there is no place that is supposed to have the marking_value, then return False
    for transition in n.transition():
        modes = transition.modes() # get variable substitutions
        if len(modes) == 0: # deadlock
            return False
        
        transition.fire(modes[0]) # fire the transition

        for t in n.get_marking().keys():
            if marking_value in n.get_marking()[t].items(): # if the desired token is in the marking
                return True
    
    return False

def find_output_annotation_in_combination(annotation, combination):
    """
    Finds the component that contains the provided annotation in the provided combination.

    Args:
        annotation (Annotation): the annotation to find
        combination (tuple): the combination to search in

    Returns:
        Component: the component that contains the annotation
    """
    for component in combination:
        output_annotation_types = [type(oa) for oa in component.output_annotations]
        if annotation in output_annotation_types:
            return component
    return None