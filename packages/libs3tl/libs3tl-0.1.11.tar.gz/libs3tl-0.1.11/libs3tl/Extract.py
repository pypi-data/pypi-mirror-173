import os
from requests import Request, Session
from libs3tl import Step
import websocket


class Extract(Step.Step):
    def __init__(self):
        self.setStartTime()
        self.step = "Ex"
        self.paramsFile = 'Extract.properties'
        self.logger = 'logExtract'
        self.logFile =self.getRelativeFile(os.getcwd() +'\../logs/Extract.log') 

    def startup(self):
        return super().startup()

    def doWork(self):
        pass

    def storeToRedisSortedSet(self, key, score, data):
        jsonObj ={}
        jsonObj[str(data)] = score
        self.rC.zadd(key, jsonObj)

    def onmessage(self, ws, message):
        pass
    
    def onerror(self, ws, error):
        pass
    
    def onclose(self, ws, close_status_code, close_msg):
        pass
    
    def onopen(self, ws):
        pass
    
    def startWs(self):
        websocket.enableTrace(False)
        socket = f""+ self.params["wsURL"].data + ""
        ws = websocket.WebSocketApp(socket,
                             on_message=self.onmessage,
                                on_error=self.onerror,
                                on_close=self.onclose,
                                on_open=self.onopen)
        ws.run_forever()

   
