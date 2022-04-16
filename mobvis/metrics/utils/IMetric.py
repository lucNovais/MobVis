import pandas as pd

from abc import abstractclassmethod, ABCMeta

class IMetric(metaclass=ABCMeta):
    """Abstract class that defines the implemented metrics patterns and default methods.
       All metrics on the library must inherit from this class and implement its methods.
    """
    @abstractclassmethod
    def __init__(self, **kwargs):
        pass

    @abstractclassmethod
    def extract(self):
        pass
