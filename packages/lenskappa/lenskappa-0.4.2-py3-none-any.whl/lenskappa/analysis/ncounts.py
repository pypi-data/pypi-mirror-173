from lenskappa.analysis.analysis import LenskappaAnalysis
from lenskappa.output import csvOutput




class NumberCountsAnalysis(LenskappaAnalysis):


    def __init__(self, *args, **kwargs):
        self.setup()

    def setup(self, *args, **kwargs):
        pass

    def get_step(self, *args, **kwargs):
        """
        Performs a single step in the analysis.        
        """
        pass
