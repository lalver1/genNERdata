"""
Generate NER data

"""

from dataclasses import dataclass
from numpy import random
from faker import Faker
import json
import sys

def load_sequences(filename):
    """Load JSON NE sequences.

    :param filename: Name of JSON file to load
    :type filename: String
    :return: Deserialized JSON object
    :rtype: Dictionary
    """

    with open(filename, "r") as read_file:
        data = json.load(read_file)
    return data


def count_sequences(data):
    """Count the number of JSON NE sequences.
    
    :param data: Dictionary of NE sequences
    :type data: Dictionary
    :return: Number of NE sequences
    :rtype: Integer
    """

    count = 0
    try:
        for value in data.items():
            if isinstance(value, list):
                count += len(value)
    except:
        print('Invalid NE sequences format') 
    return count


def gen_data(sequence,N):
    """Generate spaCy training data.
    
    :param sequence: NE sequence
    :type data: List
    :return: spaCy training data
    :rtype: List of tuples
    """

    fake = Faker()
    train_data =[]
    for _ in range(N):
        entities = []    
        for (offset, s) in enumerate(sequence):    
                if s['p'] is None:
                    try:
                        value = eval(s['value'])
                    except:
                        value = s['value']            
                else:
                    value = random.choice(s['value'], 1, p=s['p']).item(0)                
                if offset == 0:
                    start = 0
                    end = len(value)
                else:
                    start = entities[offset-1]['end']
                    end = start + len(value)
                label = s['label']
                entities.append({'value': value, 'start': start, 'end': end, 'label': label})
        data = (''.join([str(e['value']) for e in entities]),{'entities': [(e['start'],e['end'],e['label']) for e in entities if e['label'] is not None]})    
        train_data.append(data)
    
    return train_data

def main():
    """Entry point.

    """
        
    sequences = load_sequences(sys.argv[1])
    training_data = []
    for (offset, seq) in enumerate(sequences['ne-sequences']):
        training_data.append(gen_data(seq['ne-sequence'],5))
    for (offset, seq) in enumerate(sequences['ne-sequences']):
        print(training_data[offset])
    

if __name__ == "__main__":
    main()