import os
from requests import Session
from Step import Step

class Load(Step): 
    
    def __init__(self):
        self.setStartTime()
        self.step = "Lo"
        self.paramsFile = 'Load.properties'
        self.logger = 'logLoad'
        self.logFile = self.getRelativeFile(os.getcwd() + '\../logs/Load.log')
        
        

    def startup(self):
        super(Load, self).startup()
        self.startConsensusSubscriber()
    
        
        
    def startConsensusSubscriber(self):
        self.subscriber = self.rC.pubsub()
        self.subscriber.subscribe(self.taskID + "_" + self.step)