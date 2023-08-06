from dataclasses import dataclass


@dataclass
class Dataset:
    '''Works with the sklearn data generators parameters manipulation
    to measure the impact on metrics.'''

    random_state: int = 137

    def data_generator(self, generator, param, list_value):
        '''Generates features and targets for the set of parameters.'''
        
        for v in list_value:
            d_param = dict()
            d_param['random_state'] = self.random_state
            d_param[param] = v
            X, y = generator(**d_param)
            
            yield X, y