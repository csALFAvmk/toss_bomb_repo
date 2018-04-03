'''
Created on 21. 7. 2017

@author: dmarkov004
'''
# encoding: utf8

import time
import tg_interface
import bomb_logic
import ConvertMath
#import requirements


def main():
    while True:
        command = tg_interface.getCommand()
        if None != command:
            my_chat_id=tg_interface.getChatId()#'289795148'#
            #my_username=tg_interface.getUserName()
            FirstUserName=tg_interface.getFirstName()
            #text_to_send="Not a valid command."+chr(10)+"Use /help, dumbass."
            text_to_send=""
            victim_text_to_send=""
            victim_chat_id=""
            
            
            if "help" == command:            
                text_to_send="The game is simple. Toss a bomb to your friends. Make them bombed make them drunk."+chr(10)+chr(10)+"Use /start_bomb to start"
            
            
            if "start_bomb" in command:
                'default values'
                duration_sup=50
                duration_inf=150
                'parse input command'
                if " " in command:
                    index_space=command.find(" ")
                    substring_to_parse=command[index_space+1:]
                    if " " in substring_to_parse:
                        index_space=substring_to_parse.find(" ")
                        duration_sup=substring_to_parse[0:index_space].__str__()
                        duration_inf=substring_to_parse[index_space+1:].__str__()
                    
                if ConvertMath.IsNature(duration_sup) and ConvertMath.IsNature(duration_inf):
                    if (float(duration_sup)<10 or float(duration_inf)>2000 or float(duration_sup)>=float(duration_inf)):
                        text_to_send="Duration must be between 10 and 2000 seconds. Bottom limit show be less than top."
                    else:
                        try: 
                            bomb
                        except NameError:
                            UserList=tg_interface.getBotUserList()
                            bomb=bomb_logic.bomb(duration_sup=duration_sup, duration_inf=duration_inf, UserList=UserList, chat_id=my_chat_id)
                            bomb.start()
                            offset=tg_interface.getCurrentOffset()+1000
                            tg_interface.setOffset(offset.__str__())
                            bomb_time=bomb.peek().__str__()[0:]#[0:bomb_time+3]
                            text_to_send ="Time set up to : " + bomb_time +" seconds."+chr(10)+"Use /send_bomb to pass it."
                        else:
                            if bomb.isbombalive():
                                text_to_send="Haha 2 bombs in one time? No way!" + chr(10)+"Wait for your doom!"
                            else:
                                UserList=tg_interface.getBotUserList()
                                bomb=bomb_logic.bomb(duration_sup=duration_sup, duration_inf=duration_inf, UserList=UserList, chat_id=my_chat_id)
                                bomb.start()
                                bomb_time=bomb.peek().__str__()[0:]#[0:bomb_time+3]
                                text_to_send ="Time set up to : " + bomb_time +" seconds."+chr(10)+"Use /send_bomb to pass it."
                else:
                    text_to_send="Worng format, seconds, dude, seconds. Like that:"+chr(10)+"/start_bomb 10 2000"
    
            
            if "check_bomb" == command:
                try:
                    bomb
                except NameError:
                    text_to_send = "No bomb has been set up. Please use /start_bomb min_time max_time command"
                else:
                    if not bomb.isbombalive():
                        text_to_send = "No bomb has been set up. Please use /start_bomb min_time max_time command"
                    else:
                        if bomb.getcurrentvictim()==my_chat_id:
                            bomb_time=bomb.peek().__str__()[0:]#[0:bomb_time+3]
                            text_to_send ="Time to boooom: " + bomb_time+ " seconds"
                        else:
                            text_to_send ="You have no bomb. How can you know the time?"
                
                
            if 'send_bomb' == command:
                try: 
                    bomb
                except NameError:
                    text_to_send = "No bomb has been set up. Please use /start_bomb min_time max_time command"
                    victim_text_to_send=""
                else:
                    if not bomb.isbombalive():
                        text_to_send = "No bomb has been set up. Please use /start_bomb min_time max_time command"
                    else:
                        if bomb.getcurrentvictim()==my_chat_id:
                            text_to_send=""
                            for user in UserList:
                                if user[3] != my_chat_id:
                                    text_to_send="/"+ user[0]+chr(10)+text_to_send
                            bomb_time=bomb.peek().__str__()
                            if not text_to_send:
                                text_to_send="It seems that noone besides you play this game."+chr(10)+"Dude, you are fucked..."+chr(10)+"Don't drink alone too much."
                            else:
                                text_to_send="You have "+bomb_time+" seconds." +chr(10)+"Whom do you want to pass bomb?"+chr(10)+text_to_send
                        else:
                            text_to_send="You cannot send something that you don't have, can you?"
    
            
            try:
                bomb
            except NameError:
                if not text_to_send:
                    text_to_send = "No bomb has been set up. Use /start_bomb min_time max_time command"
                    victim_text_to_send=""
            else:
                if not bomb.isbombalive():
                    text_to_send = "No bomb has been set up. Use /start_bomb min_time max_time command"
                    victim_text_to_send=""
                else:
                    if my_chat_id == bomb.getcurrentvictim():
                        for user in UserList:
                            if user[0]==command:
                                victim_chat_id=user[3]
                                bomb_time=bomb.peek().__str__()
                                bomb.updatevictim(victim_chat_id)
                                bomb.updatetime(7)
                                victim_text_to_send=FirstUserName + " has bombed you, you have "+bomb_time+" seconds"+chr(10)+"/send_bomb"+chr(10)+"/check_bomb"
                                text_to_send="You have bombed buster!" +chr(10)+ user[0]+" has "+bomb_time+" seconds to pray."
                    else:
                        if not text_to_send:
                            for user in UserList:
                                if bomb.getcurrentvictim() == user[3]:
                                    victim_name=user[0].__str__()
                            text_to_send="Who do you want to cheet on? Wait for "+victim_name.__str__()+"'s mercy!"
                
            'send final message'
            if not text_to_send:
                text_to_send="Not a valid command."+chr(10)+"Use /help, dumbass."
            tg_interface.sendMessage(my_chat_id, text_to_send)
            if victim_chat_id and victim_text_to_send:
                tg_interface.sendMessage(victim_chat_id, victim_text_to_send)
            
            #resetUpdate_id()
        time.sleep(1)
if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()