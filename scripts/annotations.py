from snakes.nets import Variable, Value


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
    
## TODO: finish for other annotations
# qa:AnnotationOfQuestionLanguage 
#         owl:equivalentClass  [ a                   owl:Restriction ;
#                               owl:onProperty      oa:hasBody ;
#                              owl:someValuesFrom  <http://id.loc.gov/vocabulary/iso639-1/>
#                             ] .

# qa:AnnotationOfQuestionTranslation
#        owl:equivalentClass  [ a                   owl:Restriction ;
#                               owl:onProperty      qa:supportedLanguages ;
#                               owl:someValuesFrom  <http://id.loc.gov/vocabulary/iso639-1/>
#                             ] .

## TODO: finish for other annotations

class AnnotationOfClass:
    token_value = 5
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

class AnnotationOfQuestionLanguage:
    token_value = 6