#!/usr/bin/python
# -*- coding: utf8 -*-

############ Module #############
from Crypto.Cipher import AES
# from socket import *
from ScanLan import *
import datetime, os, Queue, threading, sqlite3, pickle, base64

############ Global #############
CheckIp = socket(AF_INET, SOCK_DGRAM)
try:
    CheckIp.connect(('google.com', 0))
    IpAddress = CheckIp.getsockname()[0]

except:
    print "[+]Check your internet connection and continue."
    os._exit(1)
OnlineClients = set()
Username = os.environ.get('USERNAME')
Hour = datetime.datetime.now().hour
FullDate = datetime.datetime.now().strftime("%d-%m-%y")
WorkerQueue = Queue.Queue()
WorkingThreads = 64
ThreadSemaphore = threading.Semaphore(1)


############ Class #############

class Commnd(object):
    # Class command
    def __init__(self):
        print "[+]Starting...."

    def Parameters(self):
        # Parameters For encryption.
        secret = "a12a87aAw2351cE58a8s7SqwD2f46eSA"
        self.BLOCK_SIZE = 32
        self.PADDING = '{'
        self.cipher = AES.new(secret)

    def Connect(self, Target):
        # Connect server over socket.
        client = socket(AF_INET, SOCK_STREAM)
        self.client = client
        self.buffer = 2048
        self.client.connect((Target, 7418))
        self.client.settimeout(30)
        self.ipServer = self.Receive_Message()
        self.Write_log('[+]Client connected: {0}.'.format(self.ipServer))
        print '[+] Client connected: {0}.'.format(self.ipServer)
        Message = self.Receive_Message()
        if Message == "Regme": self.Write_In_Db(self.ipServer)
        else: return Message

    def Encryption(self):
        # Encryption text
        pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING
        return lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    def Decryption(self):
        # Decryption text
        return lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(self.PADDING)

    def Write_log(self, Text):
        # writing to log file
        with open("Logs\%s.log" % (FullDate), 'a') as LogsFile:
            data = "%s      %s\n" % (datetime.datetime.now().strftime("%H:%M"), Text)
            LogsFile.write(data)
            LogsFile.close()

    def Send_Message(self, Text):
        # Encryption message and Send message to server
        self.client.send(self.Encryption()(self.cipher, Text))

    def Receive_Message(self):
        # Decryption message and return message to server
        try:
            Message = self.Decryption()(self.cipher, self.client.recv(self.buffer))
        except ValueError:
            return "Something has happened, try again."
        return Message

    def Write_In_Db(self, Data):
        dbConnect = sqlite3.connect('Db\DBCore.db')
        dbConnect.execute("INSERT INTO Clients (`ip`,`status`) VALUES ('%s','%s')" % (Data, "Active"))
        dbConnect.commit()
        dbConnect.close()

    def Close_Socket(self):
        self.client.close()

    def Remove_Agent(self, Client):
        dbConnect = sqlite3.connect('Db\DBCore.db')
        dbConnect.execute("DELETE FROM Clients WHERE ip = '%s';" % (Client))
        dbConnect.commit()
        dbConnect.close()
        self.Close_Socket()

class Main(Commnd):
    # Class Maibn function
    def __init__(self):
        self.OnlineClients = OnlineClients
        self.Parameters()
        if 5 <= Hour <= 12: print "[+]Good morning %s."   % (Username)
        elif 13 <= Hour <= 18:print "[+]Good afternoon %s." % (Username)
        elif 19 <= Hour <= 22:
            print "[+]Good evening %s." % (Username)
        else:
            print "[+]Good night %s." % (Username)
        self.Write_log("[+]Starting ...")
        Clients = self.Choose_Client()
        self.Write_log("[+]Have a %s client online." % (len(self.OnlineClients)))
        self.Write_log("[+]selected %s from %s client online." % (len(Clients), len(self.OnlineClients)))
        self.What_to_do()

    def Get_Data_DB(self):
        # Get all data from db.
        dbConnect = sqlite3.connect('Db\DBCore.db')
        clientIpList = dbConnect.execute("SELECT ip FROM Clients")
        self.clientIpList = clientIpList.fetchall()
        dbConnect.close()
        return self.clientIpList

    def Check_Online(self, MyQueue, MySempahore):
        # Checks online clients
        self.OnlineClients = set()
        while True:
            Data = MyQueue.get()
            Data = str(Data[0])
            if "TTL" in os.popen("ping -n 1 %s" % (Data)).read():
                with MySempahore:
                    self.OnlineClients.add(Data)
            MyQueue.task_done()
            return self.OnlineClients

    def Choose_Client(self):
        IpClient = set()
        # Select Clients from online list
        print "[+]Checking Online clients ..."
        for i in range(WorkingThreads):
            t = threading.Thread(target=self.Check_Online, args=(WorkerQueue, ThreadSemaphore,))
            t.setDaemon(True)
            t.start()

        for client in self.Get_Data_DB():
            WorkerQueue.put(client)
        WorkerQueue.join()

        print "\n[+]Have %s client online." % (len(self.OnlineClients))
        for i in range(0, len(self.OnlineClients)):
            print "%d%s %s" % (i + 1, ")", list(self.OnlineClients)[i])
        print "\nSelect from the menu: \n" \
              "  (num)    -     for one client.\n" \
              "  (1-%s)    -     for range client.\n" \
              "  (A)      -     for all client.\n" \
              "Exmple: 1, 1-%s, A" % (len(self.OnlineClients), len(self.OnlineClients))
        while True:
            try:
                choose_client = (raw_input(" > ").lower()).split(",")
                for select in choose_client:
                    if "-" in select:
                        select = [int(n) for n in select.split("-")]
                        for index in range(select[0] - 1, select[1]):
                            IpClient.add(list(self.OnlineClients)[index])
                    elif "a" in select:
                        for index in range(len(self.OnlineClients)):
                            IpClient.add(list(self.OnlineClients)[index])
                    else:
                        IpClient.add(list(self.OnlineClients)[int(select) - 1])
                self.IpClient = IpClient
                return self.IpClient
                break
            except IndexError:
                print "[+]Client not found in a list, please try again."
                continue
            except ValueError:
                print "[+]Something was wrong, please try again."
                continue

    def What_to_do(self):
        # Tasks
        isFiresTime = True
        while True:
            if isFiresTime == True:
                ProgramList = ""
                print "Ok, you selected %s client, What you want to do with them (choose 1 action)?" % (len(self.IpClient))
            print "1) Run a command."
            print "2) Get a list of all programs installed on computer."
            print "3) Scan lan to search new clients (Take 1 minute)."
            if len(self.IpClient) == 1:
                print "4) Remove a client."
            else:
                print "4) Remove all clients."
            print "b) Back to select another clients."
            print "q) Exit."
            UserInput = (raw_input(" > ")).lower()
            if UserInput == "1":
                isFiresTime = False
                command = raw_input("[+]Send a command: >> ").lower()
                for Client in self.IpClient:
                    try:
                        self.Connect(Client)
                        self.Send_Message(command)
                        self.Write_log("[+]Send command %s to the: %s" % (command, Client))
                        print "From %s:\n%s" % (self.ipServer, self.Receive_Message())
                    except error, e:
                        print e
                        continue
                    self.Close_Socket()
            elif UserInput == "2":
                isFiresTime = False
                for Client in self.IpClient:
                    try:
                        self.Connect(Client)
                        self.Send_Message("programlist")
                        self.Write_log("[+]Send command %s to the: %s" % ("programlist", Client))
                    except error, e:
                        print e
                        continue
                    while True:
                        Data = self.Receive_Message()
                        ProgramList += Data
                        if "close" in Data:
                            break
                            self.client.close()
                    ProgramList = (pickle.loads(ProgramList))[0]
                    with open("Reports\%s_Program_Install.txt" % (self.ipServer), "w")as file:
                        file.write("The program install for %s\n" % (self.ipServer))
                        file.write("%s\n" % (("-") * 30))
                        for program in ProgramList:
                            try:
                                str(file.write("%s\n" % (program)))
                            except UnicodeEncodeError:
                                continue
                        file.close()
                    print "[+]The reports was save in '%s\Reports\%s_Program_Install.txt" % (os.getcwd(), self.ipServer)
                    self.Write_log("[+]The reports was save in '%s\Reports\%s_Program_Install.txt" % (os.getcwd(), Client))
            elif UserInput == "3":
                isFiresTime = False
                Result = Scanports().Scan(IpAddress)
                if Result == "y":
                    isFiresTime = True
                    self.Choose_Client()
            elif UserInput == "4":
                isFiresTime = False
                for delete in self.IpClient:
                    self.Connect(delete)
                    self.Send_Message("remove_agent")
                    self.Remove_Agent(delete)
                    print "[+]The client %s remove from DB\n" % (delete)
                    self.Write_log("[+]The client %s remove from DB" % (delete))
                    self.Choose_Client()
            elif UserInput == "b":
                isFiresTime = True
                self.Choose_Client()
            elif UserInput == "q":
                os._exit(0)
            else:
                isFiresTime = False
                print "[+]You need select one option, select again"

############ Start program#############
if __name__ == '__main__':
    Main()
