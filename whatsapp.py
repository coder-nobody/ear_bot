# db
from zcrmsdk import ZCRMRestClient,ZCRMRecord,ZCRMModule,ZCRMUser
import pickle
from quest import *
from TextClient import TextClient


r=open("cf","rb")
config=pickle.load(r)
r.close()
admin=['00918210740791']

r=open("cred","rb")
token=pickle.load(r)[0]
r.close()

ZCRMRestClient.initialize(config)
db={
        'last':0,
        'l_name':'.',
        'f_name':'.',
        'status':'New',
        'purpose':'NA',
        'user':'NA',
        'patient':'NA'
    }

users={}
client = TextClient(apikey=token)
allowedChannels = ['Whatsapp']

class Wa():
    def __init__(self,msg):
        self.msg=msg
        # print(msg)
        self.sname=msg['from']['name']
        self.sno=msg['from']['number']
        self.message=msg['message']['text'].strip()
        self.to=['00'+self.sno[1:]]
        if self.sno not in users:
            users[self.sno]={
                            'last':0,
                            'l_name':'.',
                            'f_name':'.',
                            'status':'New',
                            'purpose':'NA',
                            'user':'NA',
                            'patient':'NA'
                            }


    def text(self,num):
        client.SendSingleMessage(message=que[num], from_='HEAR.COM', to=self.to,allowedChannels=allowedChannels)
    def newcustomer(self):
            name=users[self.sno]['f_name']+" "+users[self.sno]['l_name']
            purpose=users[self.sno]['purpose']
            patient=users[self.sno]['patient']
            user=users[self.sno]['user']
            # msg=f'*New Customer:*\n*Name:*_{name}_\n*Mobile:*{self.sno}\n*Purpose:*{purpose}\n*Patient:*{patient}\n*Use Hearing Aid:*{user}\n'
            msg=' *New Customer:*\n *Name:* _'+ name+'_\n *Mobile:* '+self.sno+'\n *Purpose:* '+purpose+'\n *Patient:* '+patient+'\n *Use Hearing Aid:* '+user+'\n'
            client.SendSingleMessage(message=msg, from_='HEAR.COM', to=admin,allowedChannels=allowedChannels)

    def createlead(self):
        record= ZCRMRecord.get_instance('Leads')
        # name=users[self.sno]['name'].split()

        record.set_field_value('First_Name',users[self.sno]['f_name'])
        record.set_field_value('Last_Name',users[self.sno]['l_name'])
        record.set_field_value('Mobile',self.sno) 
        record.set_field_value('Lead_Source',"Whatsapp")
        record.set_field_value('Lead_Status',users[self.sno]['status'])
        if users[self.sno]['last']!=200:
            record.set_field_value('Purpose',users[self.sno]['purpose'])
            record.set_field_value('Patient',users[self.sno]['patient'])
            record.set_field_value('Hearing_user',users[self.sno]['user'])
        resp=record.create()
        print(resp.status_code," ",resp.code)
    def resetdata(self):
        users[self.sno]={
                        'last':0,
                        'l_name':'.',
                        'f_name':'.',
                        'status':'New',
                        'purpose':'NA',
                        'user':'NA',
                        'patient':'NA'
                        }

    def processing(self):
        # print(users)
        # print(self.sname+" : "+self.sno+" "+self.message)
        self.last=users[self.sno]['last']
        if(self.last==0):            
            client.SendSingleMessage(message=que[0], from_='HEAR.COM', to=self.to,allowedChannels=allowedChannels)
            self.text(1)
            users[self.sno]['last']=1
            
        elif(self.last==1):
            try:
                nm=self.message.split()
                users[self.sno]['f_name']=nm[0]
                users[self.sno]['l_name']=nm[1]
            except:
                self.text(10)
                return
            users[self.sno]['last']=2
            self.text(2)      
                  
        elif(self.last==2):
            try:
                n=int(self.message)
                if(n==1):
                    # users[self.sno]['last']=200
                    # self.last=200
                    users[self.sno]['status']='Existing'
                    self.text(3)                    
                    self.createlead()
                    # print(users.pop(self.sno))
                    self.resetdata()
                    

                elif n==2:
                    users[self.sno]['last']=3
                    self.text(5)
                    
                else:
                    self.text(4)
            except:
                self.text(9)  
                      
        elif self.last==3:
            try:
                n=int(self.message)
                if n==1 or n==2:                   
                    users[self.sno]['last']=4
                    if n==1:
                        users[self.sno]['purpose']='Hearing Aid Trial'
                    else:
                        users[self.sno]['purpose']='Book an appointment'
                    self.text(6)
                elif n==3:
                    users[self.sno]['last']=300
                    self.last=300
                    self.text(8)
                    users[self.sno]['purpose']='Something else'
                    self.createlead()
                    self.newcustomer()
                    self.resetdata()
                    # del users[self.sno]
                else:
                    self.text(9)
            except:
                self.text(9)
            
        elif self.last==4:
            try:
                n=int(self.message)
                if n==1 or n==2:
                    users[self.sno]['last']=5
                    if n==1:
                        users[self.sno]['patient']='Self'
                    else:
                        users[self.sno]['patient']='Someone else'
                    self.text(7)                
                else:
                    self.text(9)
            except:
                self.text(9)
            
        elif self.last==5:
            try:
                n=int(self.message)
                if n==1 or n==2:
                    if n==1:
                        users[self.sno]['user']='Yes'
                    else:
                        users[self.sno]['user']='No'
                       
                    self.createlead()
                    self.newcustomer()
                    self.text(8)
                    #del users[self.sno]
                    self.resetdata()
 
                else:
                    self.text(9)
            except:
                self.text(9)
        
            
        




        


