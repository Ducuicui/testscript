import socket


def testSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    '''
    host = 'www.baidu.com'
    #get host ip
    ip = socket.gethostbyname(host)
    port = 80
    s.connect((ip , port))
    message = "GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n"
    s.send(message)
    reply = s.recv(4096)
    print reply
    s.close()
    '''
    s.bind(('localhost', 8882))
    #10 process wait at last
    s.listen(10)

    while True:
        connection,address = s.accept()
        print 'Connected with ' + address[0] + ':' + str(address[1])
        data = connection.recv(1024)
        connection.send('your input '+data)
        
    connection.close()
    s.close()
    
if __name__ == '__main__':
    testSocket()