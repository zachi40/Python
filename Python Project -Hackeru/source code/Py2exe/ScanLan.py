from socket import *
import os, threading, Queue, sqlite3, sys

############ Global #############
CheckIp = socket(AF_INET, SOCK_DGRAM)
ThreadSemaphore = threading.Semaphore(1)
WorkerQueue = Queue.Queue()
WorkingThreads = 64
Client_Ports = set()

############ Class #############
class Scanports(object):
    def __init__(self):
        pass

    def Db(self,Data):
        dbConnect = sqlite3.connect('Db\DBCore.db')
        dbConnect.execute("INSERT INTO Clients (`ip`,`status`) VALUES ('%s','%s')" % (Data, "Active"))
        dbConnect.commit()
        dbConnect.close()

    def scan_port(self,port_num, host):
        print "Checking %s ..."%(host)
        s = socket()
        setdefaulttimeout(2)
        try:
            s = s.connect((host, port_num))
            Client_Ports.add(host)
        except Exception:
            pass

    def ping(self, MyQueue, MySempahore):
        while True:
            Data = MyQueue.get()
            if "TTL" in os.popen("ping -n 1 %s" % (Data)).read():
                with MySempahore:
                    self.scan_port(7418, Data)
            MyQueue.task_done()

    def Scan(self, IpAddress):
        IpAddress_split = [int(n) for n in IpAddress.split(".")]
        print "Checking active client ..."
        for i in range(WorkingThreads):
            t = threading.Thread(target=self.ping, args=(WorkerQueue, ThreadSemaphore,))
            t.setDaemon(True)
            t.start()

        for i in range(255):
            try:
                WorkerQueue.put("%d.%d.%d.%d" % (IpAddress_split[0], IpAddress_split[1], IpAddress_split[2], i))
            except:
                print "the ip address is not a valid."
                sys.exit('error message')
                #os._exit(1)
        WorkerQueue.join()

        #######Add to db########
        if len(Client_Ports) > 1:
            question = raw_input("Found %d client with the port open.\nYou want to add them to the db? " % (len(Client_Ports))).lower()
            if question == "y":
                for client in Client_Ports:
                    self.Db(client)
                return "y"
        elif len(Client_Ports) == 1:
            question = raw_input("Found %d client with the port open.\nYou want to add them to the db? " % (len(Client_Ports))).lower()
            if question == "y":
                self.Db(Client_Ports[0])
                return "y"
        else:
            print "No found any client"

if __name__ == '__main__':
    try:
        Scanports().Scan(sys.argv[1])
    except:
        print "use %s\Scanlan [Your IP Address]"%(os.getcwd())