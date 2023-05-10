class Component:
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponent'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        self.uri = uri
        self.comment = comment
        self.label = label
        self.input_annotations = input_annotations
        self.output_annotations = output_annotations
        
    def __str__(self) -> str:
        value = self.uri.replace('https://w3id.org/wdaqua/qanary#', '')
        return f'{value}'
    
    def __repr__(self) -> str:
        value = self.uri.replace('https://w3id.org/wdaqua/qanary#', '')
        return f'{value}'

class ComponentNER(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentNER'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentNED(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentNED'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentNERD(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentNERD'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentREL(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentREL'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentRD(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentRD'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentQBE(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentQBE'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentQE(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentQE'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentQB(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentQB'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentMT(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentMT'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentLD(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentLD'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentCLS(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentCLS'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

class ComponentASR(Component):
    uri_type = 'https://w3id.org/wdaqua/qanary#QanaryComponentASR'
    def __init__(self, uri: str, comment: str, label: str, input_annotations: list, output_annotations: list):
        super().__init__(uri, comment, label, input_annotations, output_annotations)

type_class_dict = {
    ComponentNER.uri_type: ComponentNER,
    ComponentNED.uri_type: ComponentNED,
    ComponentNERD.uri_type: ComponentNERD,
    ComponentREL.uri_type: ComponentREL,
    ComponentRD.uri_type: ComponentRD,
    ComponentQB.uri_type: ComponentQB,
    ComponentQE.uri_type: ComponentQE,
    ComponentQBE.uri_type: ComponentQBE,
    ComponentMT.uri_type: ComponentMT,
    ComponentLD.uri_type: ComponentLD,
    ComponentCLS.uri_type: ComponentCLS,
    ComponentASR.uri_type: ComponentASR
}