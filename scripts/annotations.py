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
        if len(self.supported_knowledge_graphs) == 0:
            return f"(instance == {self.token_value})"
        else:
            kg_part = 'or '.join([f'kgInstance == \"{kg}\"' for kg in self.supported_knowledge_graphs])
            return f"(instance == {self.token_value} and ({kg_part}))"
    
    def get_input_variables(self):
        if len(self.supported_knowledge_graphs) == 0:
            return [Variable('instance')]
        else:
            return [Variable('instance'), Variable('kgInstance')]
    
    def get_output_variables(self):
        if len(self.supported_knowledge_graphs) == 0:
            return [Variable('instance')]
        else:
            return [Variable('instance'), Variable('kgInstance')]
    
    def get_output_values(self):
        if len(self.supported_knowledge_graphs) == 0:
            return [Value(self.token_value)]
        else:
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
    def __init__(self, **kwargs):
        self.supported_languages = kwargs.get('https://w3id.org/wdaqua/qanary#supportedLanguages', [])

    def get_guard_expression(self):
        lang_part = 'or '.join([f'questionLang == \"{lang}\"' for lang in self.supported_languages])
        return f"({lang_part})"

    def get_input_variables(self):
        return [Variable('questionLang')]
    
    def get_output_variables(self):
        return [Variable('questionLang')]
    
    def get_output_values(self):
        return [Value(self.supported_languages[0])]
 
class AnnotationOfQuestionTranslation:
    token_value = 7
    def __init__(self, **kwargs):
        self.supported_languages = kwargs.get('https://w3id.org/wdaqua/qanary#supportedLanguages', [])

    def get_guard_expression(self):
        lang_part = 'or '.join([f'translatedQuestionLang == \"{lang}\"' for lang in self.supported_languages])
        return f"(translatedQuestion == {self.token_value} and ({lang_part}))"

    def get_input_variables(self):
        return [Variable('translatedQuestion'), Variable('translatedQuestionLang')]
    
    def get_output_variables(self):
        return [Variable('translatedQuestion'), Variable('translatedQuestionLang')] 
    
    def get_output_values(self):
        return [Value(self.token_value), Value(self.supported_languages[0])]

class AnnotationOfSpotInstance:
    token_value = 8
    def __init__(self, **kwargs):
        pass

    def get_guard_expression(self):
        return f"(spotInstance == {self.token_value})"
    
    def get_input_variables(self):
        return [Variable('spotInstance')]
    
    def get_output_variables(self):
        return [Variable('spotInstance')]
    
    def get_output_values(self):
        return [Value(self.token_value)]