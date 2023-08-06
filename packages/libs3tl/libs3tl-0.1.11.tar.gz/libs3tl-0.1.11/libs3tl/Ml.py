import os
from libs3tl import Step
import json
import pandas as pd




class Ml(Step.Step):
    def __init__(self):
        self.setStartTime()
        self.step = "Ml"
        self.paramsFile = 'ML.properties'
        self.logger = 'logMl'
        self.logFile = self.getRelativeFile(os.getcwd() +'\../logs/Ml.log')

    def startup(self):
        super(Ml, self).startup()
        self.taskExecutionID = None
        self.startMLSubscriber()
        
    def startMLSubscriber(self):
        self.subscriber = self.rC.pubsub()
        self.subscriber.subscribe(self.taskID + "_" + "Tr")

    
            

    
    def computeML(self,msg):
        pass   
                
    def setpicklename(self,name):
        pass

    def getpicklename(self):
        pass

 


