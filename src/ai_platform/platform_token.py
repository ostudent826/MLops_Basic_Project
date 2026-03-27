import math

def basicEstimator(text):
    return math.ceil(len(text) / 4)

def tokenCounter(response):
    return { 'input_tokens': response.usage.input_tokens , 'output_tokens': response.usage.output_tokens}
    
