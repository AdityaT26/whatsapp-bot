import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sys
import pyautogui
import datetime
import re 
import os
import pyautogui as pg
import webbrowser as web
import threading
import pickle
import re

class Var():
    refresh=False
    pswd='<Bot_password_(can be anything)'
    group_id='<Your Whatsapp Group ID' 


pg.FAILSAFE = False
#driver = webdriver.Chrome(executable_path=os.getcwd()+'\\chromedriver.exe')
driver = webdriver.Chrome(executable_path='<Path_to_chrome_driver')
driver.get('https://web.whatsapp.com/accept?code='+Var.group_id)

time.sleep(10)
#pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
print('start')
refresh=False

def getWappMsg(all):

    try:

        s=[]

        htmlcode=(driver.page_source).encode('utf-8')
        soup = BeautifulSoup(htmlcode,features="html.parser")

        x=soup.findAll(['div', 'alt'] , class_ = '_1wlJG')
        for i in x:
            try:
                s.append(i.get_text())
            except:
                pass

        latest=s[len(s)-1]

        if all == False:
            return latest
        else:
            return s
        #_1wlJG
    except:
        print('Fresh Start')
        return ''

def sendMsg(msg):
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(msg)
    sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
    sendbutton.click()

def countdown(t): 
    time.sleep(t)
    Var.refresh=True
    countdown(t)

commands='> .bot ; > .bot.assist:<phrase> -> connects you to google assistant ; > .bot.damn ; > .bot.repeat:<phrase> ; > .bot.repeat@<no_of_times>@<phrase> ; > .bot.refresh ; > .bot.showchat ; > .bot.createList:<list_name> ; > .bot.addToList@<list_name>@<message> ; > .bot.getFromList@<list_name>@ ; > .bot.delList@<list_name>@ ; > .bot.showLists ; > .bot.help '
commands=commands.replace(';', '\n')
threading.Thread(target = lambda: countdown(90))

def sendQuery(query):
    with open('.\\Assistant\\query.txt', 'w', encoding='utf-8') as h:
        print('writing query: ', query)
        h.write(query)

def getResponse():
    try:
        resp=''
        with open('.\\Assistant\\response.txt', 'r', encoding='utf-8') as h:
            resp=h.read()
        return resp
    except:
        print('ERROR')
        import traceback

        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" %ex_value)
        print("Stack trace : %s" %stack_trace)
        return ''

sendQuery('')
with open('.\\Assistant\\response.txt', 'w', encoding='utf-8') as h:
    h.write('')
        
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def listenAssist(msg):
    print('Assistant on')
    if msg.startswith('.bot.assist:'):
        print('bot assist active')
        l=msg.split(':')
        query=''
        try:
            for i in range(1, len(l)):
                query+=l[i]
        except:
            pass
        print(query)
        
        if query!='':
            print('Asking')

            sendQuery(query)
            time.sleep(1)
            sendQuery('')


            resp=''

            while resp=='':
                resp=getResponse()
                pass


            sendQuery('')
            with open('.\\response.txt', 'w+', encoding='utf-8') as h:
                h.write('')
            
            try:
                try:
                    print(resp)
                    if resp!='':
                        sendMsg(deEmojify(resp))
                    else:
                        pass
                except:
                    #sendMsg('Couldn\'t connect with google at the moment')
                    import traceback

                    # Get current system exception
                    ex_type, ex_value, ex_traceback = sys.exc_info()

                    # Extract unformatter stack traces as tuples
                    trace_back = traceback.extract_tb(ex_traceback)

                    # Format stacktrace
                    stack_trace = list()

                    for trace in trace_back:
                        stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

                    print("Exception type : %s " % ex_type.__name__)
                    print("Exception message : %s" %ex_value)
                    print("Stack trace : %s" %stack_trace)
            except:
                #sendMsg('Couldn\'t connect with google at the moment')
                import traceback

                # Get current system exception
                ex_type, ex_value, ex_traceback = sys.exc_info()

                # Extract unformatter stack traces as tuples
                trace_back = traceback.extract_tb(ex_traceback)

                # Format stacktrace
                stack_trace = list()

                for trace in trace_back:
                    stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

                print("Exception type : %s " % ex_type.__name__)
                print("Exception message : %s" %ex_value)
                print("Stack trace : %s" %stack_trace)
                pass
        
while True:

    time.sleep(0.05)
    msg=getWappMsg(all=False)
    print(msg)

    if(msg=='.bot'):
        print(msg)
        sendMsg('Hello, bot here!')

    if msg.startswith('.bot.assist:'):
        threading.Thread(target=lambda:listenAssist(msg)).start()
        sendMsg('processing')

    elif(msg=='.bot.sing'):
        sendMsg('Lalalalalalalala!!!')

    elif(msg=='.bot.damn'):
        sendMsg('Bruh')

    elif(msg.startswith('.bot.repeat:')):
        try:
            msg=msg[12: len(msg)]
            sendMsg(msg)
        except:
            sendMsg('there should be someting after \'.bot.repeat:\'')
            sendMsg('and the starting should not be an emoji(just yet)')

    elif(msg.startswith('.bot.repeat@')):
        try:
            l=msg.split('@')
            times=None
            try:
                times=int(l[1])
                if not(times>=0 and times<=20):
                    times=None
                    sendMsg('Repetition times should be from 0 to 20')
            except:
                sendMsg('Integers only, like from 0-20')
            m=''
            for i in range(2, len(l)):
                m+=l[i]
            if times!=None:
                for i in range(times):
                    sendMsg(m)
        except:
            sendMsg('there should be someting after \'.bot.repeat@\'')
            sendMsg('and the starting should not be an emoji(just yet)')
            import traceback

            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %stack_trace)
            sendMsg('there should be someting after \'.bot.addToList@:\'')
            sendMsg('and the starting should not be an emoji(just yet)')

    elif(msg=='.bot.refresh'):
        sendMsg('Bot refresh')
        sendMsg('Last msg: '+msg)

    elif(msg=='.bot.showchat'):
        sendMsg(getWappMsg(all=True))

    elif(msg.startswith('.bot.createList:')):
        try:
            lName=msg.split(':')
            h=open(os.getcwd()+'\\Lists\\'+lName[1]+Var.group_id+'.txt', 'w+')
            h.close()
        except:
            sendMsg('there should be someting after \'.bot.createList:\'')
            sendMsg('and the starting should not be an emoji(just yet)')

    elif(msg.startswith('.bot.addToList@')):
        try:
            l=msg.split('@')
            if(len(l)>=2):
                lName=l[1]
                
                lists=os.listdir(os.getcwd()+'\\Lists\\')
                exists=False
                for i in lists:
                    if i.count(lName)>0 and i.count(Var.group_id)>0:
                        exists=True
                        break
                
                if exists:
                    r=''
                    h=open(os.getcwd()+'\\Lists\\'+lName+Var.group_id+'.txt', 'r')
                    r=h.read()
                    h.close()
                    h=open(os.getcwd()+'\\Lists\\'+lName+Var.group_id+'.txt', 'w')
                    h.write(r+' ')
                    for i in range(2, len(l)):
                        h.write(l[i]+'\n')
                    h.close()
                    
                    sendMsg('Added to list '+lName)
                else:
                    sendMsg(lName+ ' does not exist')

            else:
                sendMsg('there should be someting after \'.bot.addToList@\'')
                sendMsg('and the starting should not be an emoji(just yet)')

        except:
            sendMsg('ERROR')
            import traceback

            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %stack_trace)
            sendMsg('there should be someting after \'.bot.addToList@:\'')
            sendMsg('and the starting should not be an emoji(just yet)')

    elif(msg.startswith('.bot.delList@')):
        try:
            l=msg.split('@')
            if(len(l)>=2):
                lName=l[1]
                
                lists=os.listdir(os.getcwd()+'\\Lists\\')
                exists=False
                for i in lists:
                    if i.count(lName)>0 and i.count(Var.group_id)>0:
                        exists=True
                        break
                if exists:
                    os.remove(os.getcwd()+'\\Lists\\'+lName+Var.group_id+'.txt')
                    
                    sendMsg('Deleted list '+lName)
                else:
                    sendMsg(lName+ ' does not exist')

            else:
                sendMsg('there should be someting after \'.bot.addToList@\'')
                sendMsg('and the starting should not be an emoji(just yet)')

        except:
            sendMsg('ERROR')
            import traceback

            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %stack_trace)
            sendMsg('there should be someting after \'.bot.addToList@:\'')
            sendMsg('and the starting should not be an emoji(just yet)')

    elif(msg.startswith('.bot.getFromList@')):
        try:
            l=msg.split('@')
            if(len(l)>=1 ):
                lName=l[1]

                lists=os.listdir(os.getcwd()+'\\Lists\\')
                exists=False
                for i in lists:
                    if i.count(lName)>0 and i.count(Var.group_id)>0:
                        exists=True
                        break
                
                if exists:
                    r=''
                    h=open(os.getcwd()+'\\Lists\\'+lName+Var.group_id+'.txt', 'r')
                    r=h.read()
                    h.close()

                    if r!='':
                        print(r)
                        if r.endswith('\n'):
                            r=r[0: len(r)-1]
                        sendMsg(r)
                    else:
                        sendMsg(lName+' list is empty')
                
                else:
                    sendMsg(lName+ ' does not exist')

            else:
                sendMsg('there should be someting after \'.bot.getFromList@\'')
                sendMsg('and the starting should not be an emoji(just yet)')

        except:
            sendMsg('ERROR')
            import traceback

            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %stack_trace)
            sendMsg('there should be someting after \'.bot.getFromList@:\'')
            sendMsg('and the starting should not be an emoji(just yet)')

    elif(msg=='.bot.showLists'):
        try:
            t=''
            temp=os.listdir(os.getcwd()+'\\Lists\\')
            for i in temp:
                if i.count(Var.group_id)>0:
                    t=i.replace(Var.group_id, '')
                
                if t!='':
                    sendMsg(t)
            
            if t=='':
                sendMsg('oops you don\'t have a list, type .bot.createList:<list_name> to create one')
                break
        except:
            sendMsg('Hol up, An error occured')
            import traceback

            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %stack_trace)
            sendMsg('there should be someting after \'.bot.addToList@:\'')
            sendMsg('and the starting should not be an emoji(just yet)')

    elif msg=='.bot.help':
        sendMsg(commands)

    elif msg=='.bot.stop':
        sendMsg('Enter password')
        msg=getWappMsg(all=False)
        while msg=='Enter password':
            msg=getWappMsg(all=False)
        if msg==Var.pswd:
            sendMsg('Ending Session')
            os._exit(0)

    if Var.refresh:
        sendMsg('Bot refresh')
        sendMsg('Last msg: '+msg)
        Var.refresh=False
    
'''elif(msg=='.bot.showcode'):
        h=open('code.txt', 'r')
        m=h.read()
        sendMsg(m)'''