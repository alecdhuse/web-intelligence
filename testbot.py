import socket
import sys

def main():
    import sys
    
    server = "irc.cluenet.org"
    port = 6667
    channel = "#cluebotng"
    nickname = "ss_intel"
    first_ping = False
    
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
    print "connecting to:"+server
    
    irc.connect((server, port))                                                         #connects to the server
    irc.send("NICK "+ nickname +"\n") #sets nick
    irc.send("USER "+ nickname + " 0 * :Test bot\n")
    irc.send("msg nickserv identify qdue9911\r\n")    #auth

    while 1:    #puts it in a loop
       text=irc.recv(2040)  #receive the text
       print text   #print text to console

       if text.find('PING') != -1:                          #check if 'PING' is found
           irc.send('PONG ' + text.split() [1] + '\r\n') #returnes 'PONG' back to the server (prevents pinging out!)
           if first_ping == False:
                first_ping = True
                irc.send("JOIN "+ channel +"\n")        #join the chan
                
if __name__ == "__main__":
    main()
