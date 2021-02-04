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


client = TextClient(apikey=token)
allowedChannels = ['Whatsapp']

class Wa():
    users={}
    def __init__(self,msg):
        self.msg=msg
        # print(msg)
        self.sname=msg['from']['name']
        self.sno=msg['from']['number']
        self.message=msg['message']['text'].strip()
        self.to=['00'+self.sno[1:]]
        if self.sno not in Wa.users:
            Wa.users[self.sno]={
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
            name=Wa.users[self.sno]['f_name']+" "+Wa.users[self.sno]['l_name']
            purpose=Wa.users[self.sno]['purpose']
            patient=Wa.users[self.sno]['patient']
            user=Wa.users[self.sno]['user']
            # msg=f'*New Customer:*\n*Name:*_{name}_\n*Mobile:*{self.sno}\n*Purpose:*{purpose}\n*Patient:*{patient}\n*Use Hearing Aid:*{user}\n'
            msg=' *New Customer:*\n *Name:* _'+ name+'_\n *Mobile:* '+self.sno+'\n *Purpose:* '+purpose+'\n *Patient:* '+patient+'\n *Use Hearing Aid:* '+user+'\n'
            client.SendSingleMessage(message=msg, from_='HEAR.COM', to=admin,allowedChannels=allowedChannels)

    def createlead(self):
        record= ZCRMRecord.get_instance('Leads')
        # name=Wa.users[self.sno]['name'].split()

        record.set_field_value('First_Name',Wa.users[self.sno]['f_name'])
        record.set_field_value('Last_Name',Wa.users[self.sno]['l_name'])
        record.set_field_value('Mobile',self.sno) 
        record.set_field_value('Lead_Source',"Whatsapp")
        record.set_field_value('Lead_Status',Wa.users[self.sno]['status'])
        if Wa.users[self.sno]['last']!=200:
            record.set_field_value('Purpose',Wa.users[self.sno]['purpose'])
            record.set_field_value('Patient',Wa.users[self.sno]['patient'])
            record.set_field_value('Hearing_user',Wa.users[self.sno]['user'])
        resp=record.create()
        print(resp.status_code," ",resp.code)
    def resetdata(self):
        Wa.users[self.sno]={
                        'last':0,
                        'l_name':'.',
                        'f_name':'.',
                        'status':'New',
                        'purpose':'NA',
                        'user':'NA',
                        'patient':'NA'
                        }

    def processing(self):
        # print(Wa.users)
        # print(self.sname+" : "+self.sno+" "+self.message)
        self.last=Wa.users[self.sno]['last']
        if(self.last==0):            
            client.SendSingleMessage(message=que[0], from_='HEAR.COM', to=self.to,allowedChannels=allowedChannels)
            self.text(1)
            Wa.users[self.sno]['last']=1
            
        elif(self.last==1):
            try:
                nm=self.message.split()
                Wa.users[self.sno]['f_name']=nm[0]
                Wa.users[self.sno]['l_name']=nm[1]
            except:
                self.text(10)
                return
            Wa.users[self.sno]['last']=2
            self.text(2)      
                  
        elif(self.last==2):
            try:
                n=int(self.message)
                if(n==1):
                    # Wa.users[self.sno]['last']=200
                    # self.last=200
                    Wa.users[self.sno]['status']='Existing'
                    self.text(3)                    
                    self.createlead()
                    # print(Wa.users.pop(self.sno))
                    self.resetdata()
                    

                elif n==2:
                    Wa.users[self.sno]['last']=3
                    self.text(5)
                    
                else:
                    self.text(4)
            except:
                self.text(9)  
                      
        elif self.last==3:
            try:
                n=int(self.message)
                if n==1 or n==2:                   
                    Wa.users[self.sno]['last']=4
                    if n==1:
                        Wa.users[self.sno]['purpose']='Hearing Aid Trial'
                    else:
                        Wa.users[self.sno]['purpose']='Book an appointment'
                    self.text(6)
                elif n==3:
                    Wa.users[self.sno]['last']=300
                    self.last=300
                    self.text(8)
                    Wa.users[self.sno]['purpose']='Something else'
                    self.createlead()
                    self.newcustomer()
                    self.resetdata()
                    # del Wa.users[self.sno]
                else:
                    self.text(9)
            except:
                self.text(9)
            
        elif self.last==4:
            try:
                n=int(self.message)
                if n==1 or n==2:
                    Wa.users[self.sno]['last']=5
                    if n==1:
                        Wa.users[self.sno]['patient']='Self'
                    else:
                        Wa.users[self.sno]['patient']='Someone else'
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
                        Wa.users[self.sno]['user']='Yes'
                    else:
                        Wa.users[self.sno]['user']='No'
                       
                    self.createlead()
                    self.newcustomer()
                    self.text(8)
                    #del Wa.users[self.sno]
                    self.resetdata()
 
                else:
                    self.text(9)
            except:
                self.text(9)
        
            
        




        


