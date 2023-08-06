import inspect
import json
import os
import time
from Step import Step
import pandas as pd

class Transform(Step):
    def __init__(self):
        self.setStartTime()
        self.step = "Tr"
        self.paramsFile = 'Transform.properties'
        self.logger = 'logTransform'
        self.logFile = self.getRelativeFile(os.getcwd() + '\../logs/Transform.log')


    def startup(self):
        super(Transform, self).startup()
        # self.taskID = self.taskID
        # self.taskExecutionID  = self.taskExecutionID 
        # self.consensusID = self.consensusID
        # self.consensusExecutionID = self.consensusExecutionID
        # self.rC = self.rC
        self.startTrSubscriber()

    #message subscriber
    def startTrSubscriber(self):
        self.subscriber = self.rC.pubsub()
        self.subscriber.subscribe(self.taskID + "_" + "Ex")


    #  client need to define transformExData or doWorkAndHandoff inside client transform
    # def doWorkAndHandoff(self):
    #     self.transformExData()


    #function is available for microbatching of  redisSortedSet
    def microBatchProcessRedisSortedSet(self):
        try:
            datalength = self.rC.zcard(self.taskID)
            print('Total records on start',datalength)
            arrayToHoldData=[]
            start = True
            while start:
                self.setStartTime()
                self.setTaskExecutionID()
                
                currentTime =round(time.time() * 1000)
                rangeStart = 0
                rangeEnd = int(self.params["batchSize"].data)
                # while  len(arrayToHoldData) < int(self.params["batchSize"].data) + 1:
                while  True:
                    now = round(time.time() * 1000)
                    datafromRedis = self.rC.zrevrange(self.taskID, rangeStart, rangeEnd, withscores=False)
                    for i in datafromRedis:
                        arrayToHoldData.append(i)
                        rangeStart = rangeStart + 1
                        
                    if len(arrayToHoldData) >= (int(self.params["batchSize"].data) + 1):
                        self.logInfo(self.step, "Batch size reached " + str(len(arrayToHoldData)))
                        break

                    if ((int((now - currentTime)) > int(self.params["batchDuration"].data)) and (len(arrayToHoldData) > 0)):
                        self.logInfo(self.step, "Batch Duration completed, size is " + str(len(arrayToHoldData)))
                        break
                    else:
                        time.sleep(0.2)     

                df = pd.DataFrame(arrayToHoldData)
                
                self.handOff(self.step, df.to_json() )
                
                for item in arrayToHoldData:
                    self.rC.zrem(self.taskID, str(item))    

                arrayToHoldData.clear()
        except Exception as error:
            print("Error in microBatchProcessRedisSortedSet")
            self.logError(self.step, str(error))
