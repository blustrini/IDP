'''
Subprocess class, called by process
'''

def Subprocess():
    #input list of actions in order of stages
    def __init__(self,master,stages):
        #create dictionary that maps stages to actions
        self.actions = {}
        for i in len(self.stages):
            self.actions[i] = self.stages[i]
 
 print('hi')