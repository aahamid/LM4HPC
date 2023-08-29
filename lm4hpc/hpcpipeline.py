import json
import os
from .pipeline_openmp_question_answering import openmp_question_answering
from .pipeline_codebase_question_answering import codebase_question_answering
from .pipeline_similarity_checking import similarity_checking

def hpcpipelines(task: str, model: str, **kwargs) -> callable:
    """
    Returns a function for the specified task and model.

    Parameters:
        task (str): The task to perform. Options are 'openmp_question_answering', 'similarity_checking', and 'codebase_question_answering'.
        model (str): The model to use for the task.
        **kwargs: Additional keyword arguments.

    Returns:
        callable: A function that takes the appropriate parameters for the specified task and returns the result.

    Raises:
        ValueError: If the task or model is not valid.
    """
    # Read the configuration file
    with open(os.path.join(os.path.dirname(__file__), 'config.json')) as f:
        config = json.load(f)
    
    # Check if the task is valid
    if task not in config:
        raise ValueError('Unknown task: {}'.format(task))
    
    # Check if the model is valid for the task
    if model not in config[task]['models']:
        raise ValueError('Invalid model for {}: {}'.format(task, model))
    
    # Get the default parameters for the model
    default_parameters = config[task]['default_parameters'][model]
    
    # Update the default parameters with the user-specified parameters
    parameters = {**default_parameters, **kwargs}
    
    if task == 'openmp_question_answering':
        return lambda question: openmp_question_answering(model, question, **parameters)
    elif task == 'similarity_checking':
        return lambda code1, code2: similarity_checking(model, code1, code2, **parameters)
    elif task == 'codebase_question_answering':
        return lambda question: codebase_question_answering(model, question, **parameters)
