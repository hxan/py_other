
import commands
import threading
import socket
import sys
commands.getoutput('camera_turn_run.sh')
def todo():
    print( commands.getoutput('/AIR/record_run.sh') )
def todo_cmav(*data):
    commands.getoutput('/AIR/cmav_run.sh '+data[1]+' '
                           +data[2]+' '+data[3]+' '
                           +data[4]+' '
                           +data[5]
                                  ) 
def todo_camera(*datas):
     print( commands.getoutput('/AIR/camera_run.sh '+datas[1]+' '+datas[2]
                             +' '+datas[3]+' '+datas[4]+' '
                          +datas[5]+' '+datas[6]   
                                 )    
             )


skt=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
skt.bind((sys.argv[1],6060))
#commands.getstatusoutput("/a.sh "+'1212' ) 
print("OK")

while True: 
    data,addr=skt.recvfrom(1024)
    if data[0]=='1': #camera_run
        c=threading.Thread(target=todo_camera,args=data.split())
        c.setDaemon(True)
        c.start()
       # print( commands.getoutput('/AIR/camera_run.sh '+data.split()[1]+' '+data.split()[2]
       #                      +' '+data.split()[3]+' '+data.split()[4]+' '
       #                   +data.split()[5]+' '+data.split()[6]   
        #                         )    
#             )
        print('/AIR/camera_run.sh '+data.split()[1]+' '+data.split()[2]
                             +' '+data.split()[3]+' '+data.split()[4]+' '
                          +data.split()[5]+' '+data.split()[6])
    elif data[0]=='2': #cmav_run
        m=threading.Thread(target=todo_cmav,args=data.split())
        m.setDaemon(True)
        m.start()
        print("cmav_run is running")
#	commands.getoutput('/AIR/cmav_run.sh '+data.split()[1]+' '
  #                         +data.split()[2]+' '+data.split()[3]+' '
    #                       +data.split()[4]+' '
      #                     +data.split()[5]
       #                           ) 
              
        print("hoe")
        print('/AIR/cmav_run.sh '+data.split()[1]+' '
                           +data.split()[2]+' '+data.split()[3]+' '
                           +data.split()[4]+' '
                           +data.split()[5])
    
    elif data[0]=='3': #record_run
        print('/AIR/record_run.sh')
        t=threading.Thread(target=todo)
        t.setDaemon(True)
        t.start() 
    
    elif data[0]=='4': #vpn
        print('zerotier-cli join '+data.split()[1])
        print ( commands.getoutput('zerotier-cli join '+data.split()[1])  )
    elif data[0]=='5': #turn.sh
       # print('/AIR/turn.sh '+data.split()[1]+' '+data.split()[2])
       # print( commands.getoutput('/AIR/turn.sh '+data.split()[1]+' '+data.split()[2] ) ) 
        print('echo P1-12='+str( int( data.split()[1] )+138 )+'> /dev/servoblaster')
        print('echo P1-16='+str( int( data.split()[2] )+143 )+'> /dev/servoblaster')
        commands.getoutput( 'echo P1-12='+str( int( data.split()[1] )+138 )+'> /dev/servoblaster')
        commands.getoutput( 'echo P1-16='+str( int( data.split()[2] )+138 )+'> /dev/servoblaster')
    elif data[0]=='6': #network print
        print('/AIR/network.sh')
        rst=commands.getoutput('/AIR/network.sh')
        skt.sendto(rst,addr)
    elif data[0]=='7': #get cpu temp
        print('/AIR/get_temp.sh')
        rst=commands.getoutput('/AIR/get_temp.sh')
        skt.sendto(rst,addr)
    elif data[0]=='8': # ras model
        print('cat  /proc/device-tree/model')
        rst=commands.getoutput('cat  /proc/device-tree/model')
        skt.sendto(rst,addr)
    elif data[0]=='9': #camera stop
        print('/AIR/camera_stop.sh')
        print ( commands.getoutput('/AIR/camera_stop.sh') )

    elif data[0]=='a': #cmav_stop
        print('/AIR/cmav_stop.sh')
        print ( commands.getoutput('/AIR/cmav_stop.sh') )
    elif data[0]=='b':
        print('/AIR/record_stop.sh')
        print( commands.getoutput('/AIR/record_stop.sh') ) 
    elif data[0]=='c':
        print('zerotier-cli leave '+data.split()[1])
        print( commands.getoutput('zerotier-cli leave '+data.split()[1])  )    
    elif data[0]=='p':#cpu temp
        print('/AIR/get_temp.sh')
        print( commands.getoutput('/AIR/get_temp.sh') )
        cpu_data=str( commands.getoutput('/AIR/get_temp.sh') )
        send_data=bytes(cpu_data)
        skt.sendto(send_data,addr)

    print(data.split())

