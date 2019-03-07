import time
from task import *

class Park(Task):
    def __init__(self,Dim):
        #initialise super object
        super().__init__(Dim)
        #name
        self.name = 'Park'