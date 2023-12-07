# LLM Assistant for Terarium Workflow

This is a research directory containing a proof of concept for an llm-assistant for the terarium workflow screen.
It currently has a cli interface and there is a good amount of work to do to convert it to a production feature.

We will most likely want to use beaker.

## To Do (necessary and aspirational):
- [ ] add more information on terrarium
            # Generate edges - Example Request:
            # Add Calibration - Example Request: 
            # Modify Calibration - Example Request: 
            # Delete Calibration - Example Request: 
- [ ] add more information on workflow dict to prompt - 
    # Model Node Dictionaries will be in the following format:
    # {'id': (str) , 'workflowId': (str) Id of the workflow the node is in, 'operationType': 'ModelOperation', 'displayName': 'Model', 'x': (int) x location of node on screen, 'y': (int) y location of node on screen, 'state': {'modelId': terarium data service id of the model, 'modelConfigurationIds': list of terarium data service model config ids associated with this model in the workflow}, 'inputs': empty list, there are no inputs to a model node, 'outputs': list of dictionaries of model config[{'id': '0e7634fa-3db5-422a-af1c-9b04431aaca2', 'type': 'modelConfigId', 'label': 'Default config', 'value': ['37d81396-c399-4e05-9d00-0c5d94b9d939'], 'status': 'not connected'}
- [ ] Add editing existing simulations and calibrations as tools
- [ ] add more information on order of operations in Terarium. - 
    Some typical workflows that a user will want to perform in Terarium are: \n
    1.Search for then add a model to the workflow. To do this you 
    information about order of operations in Terarium (you need this to do that, ...)
- [ ] Increase speed
- [ ] add terarium documentation as ref docs for agent?
- [ ] add ability to access provenance docs?
- [ ] consolidate some tools to reduce prompt size
- [ ] add ability to modify more objects in tds

- [ ] Attempt just giving apis and docs to agent as a simpler,more generic approach
- [ ] change x,y locations where nodes are created?
- [ ] look up old action traces as examples to shove in based on context?

- [ ] have planning of tool use at start?
- [ ] add autocomplete on stop typing..?
- [ ] add actions to history or somehow save so they can be accessed via cli? (may already have this in beaker..)
- [ ] add finetuning?
- [ ] add automated user testing/bug hunting using an llm?
