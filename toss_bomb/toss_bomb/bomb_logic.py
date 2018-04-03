'''
Created on 4. 8. 2017

@author: dmarkov004
'''

import threading
import time
import random
import tg_interface


class bomb(threading.Thread):
    '''
    set up bomb time (hardcoded first)
    check the left time
    send message when time is over
    '''
    def __init__(self, duration_sup, duration_inf, UserList, chat_id, interval=1):
        # init the thread
        threading.Thread.__init__(self)
        self.interval = interval  # seconds
        # initial value
        self.value=random.randint(int(float(duration_sup)),int(float(duration_inf)))
        self.chat_id=chat_id
        self.UserList=UserList
        # controls the while loop in method run
        self.alive = False
    
    
    def run(self):
        '''
        this will run in its own thread via self.start()
        '''
        self.alive = True
        while self.alive:
            time.sleep(self.interval)
            # update count value
            self.value =self.value - self.interval
            if self.value<0:
                self.value=0
                self.alive=False
                
                text_to_send_finish="_____GAME_____"+chr(10)+"_____OV.ER_____"
                for user in self.UserList:
                    if self.chat_id == user[3]:
                        text_to_send="You've been killed, take a shot and relax"
                        looser=user[0].__str__() 
                        tg_interface.sendMessage(int(user[3]), text_to_send)
                        tg_interface.sendMessage(int(user[3]), text_to_send_finish)
                for user in self.UserList:
                    if self.chat_id != user[3]:
                        text_to_send="You've survived. "+looser+" is killed." +chr(10)+"Take another chance!"
                        tg_interface.sendMessage(int(user[3]), text_to_send)
                        tg_interface.sendMessage(int(user[3]), text_to_send_finish)
                

    def updatevictim(self, victim_chat_id):
        self.chat_id=victim_chat_id
    
    def isbombalive(self):
        return self.alive
    
    def getcurrentvictim(self):
        return self.chat_id
    
    def updatetime(self, time_s):
        if self.alive:
            self.value=self.value+int(float(time_s))
    
    def peek(self):
        '''
        return the current value
        '''
        return self.value
    
    #def finish(self):
    #    '''
    #    close the thread, return final value
    #    '''
    #    # stop the while loop in method run
    #    self.alive = False
    #    return self.value