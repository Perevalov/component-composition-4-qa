# Repository for the paper "Service Composition in Component-Oriented Question Answering Systems using Petri Nets and Semantic Descriptions"

## Structure

* `data/`: contains the RDF/Turtle data
  * `data/ontology/`: contains the ontology files
  * `data/component-descriptions/`: contains the component descriptions for a subset of the [Qanary components](https://github.com/WDAqua/Qanary-question-answering-components).
* `notebooks/`: contains the Jupyter notebooks used for the experiments
  * `notebooks/snakes-toy-example.ipynb`: just illustrates the usage of the `snakes` library
  * `notebooks/pipeline.ipynb`: contains the step-by-step code for conducting the composition approach
* `scripts/`: contains the common code to be used in the notebooks
  * `scripts/annotations.py`: contains the DTO objects for the annotations
  * `scripts/components.py`: contains the DTO objects for the components descriptions
  * `scripts/functions.py`: provides functions for the composition approach

## How to run

1. Install the dependencies:
   * `pip install -r requirements.txt`
2. Navigate to `notebooks/pipeline.ipynb` and run the Jupyter notebook.
   * All the magic happens directly below the section **"Produce the reachable combinations"**.