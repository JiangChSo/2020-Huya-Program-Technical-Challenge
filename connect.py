from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse
import json
from   search_from_csv import   search_from_csv

curdir = path.dirname(path.realpath(__file__))
sep = '/'

# MIME-TYPE
mimedic = [
    ('.html', 'text/html'),
    ('.htm', 'text/html'),
    ('.js', 'application/javascript'),
    ('.css', 'text/css'),
    ('.json', 'application/json'),
    ('.png', 'image/png'),
    ('.jpg', 'image/jpeg'),
    ('.gif', 'image/gif'),
    ('.txt', 'text/plain'),
    ('.avi', 'video/x-msvideo'),
]
def aa():
    print('aaa')

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

        sendReply = False
        print(self.path)
        querypath = urlparse(self.path)
        filepath, query = querypath.path, querypath.query
        if filepath.endswith('/'):
            filepath += 'index.html'
        filename, fileext = path.splitext(filepath)
        for e in mimedic:
            if e[0] == fileext:
                mimetype = e[1]
                sendReply = True

        if sendReply == True:
            try:
                with open(path.realpath(curdir + sep + filepath), 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        datas = self.rfile.read(int(self.headers['content-length']))
        s = datas.decode()
        s = s[10:-7]
        
        print(s)
        #search_result = search_from_csv(string=s, load='weibocut.csv')
        search_result1 = search_from_csv(string=s, load='hupucut.csv')
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(search_result).encode())
 
def run():
    port = 8080
    print('starting server, port', port)
    # Server settings
    server_address = ('172.16.0.17', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()


# import socket
# # from search_from_csv import search_from_csv
# host = socket.gethostname()
# print(host)
# ip_port = ('10.170.9.40', 8080)
# back_log = 5
# buffer_size = 1024
# ser = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   # 套接字类型AF_INET, socket.SOCK_STREAM   tcp协议，基于流式的协议
# # ser.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#
# ser.bind(ip_port)  #  写哪个ip就要运行在哪台机器上
# # 设置半连接池
# ser.listen(back_log)  # 最多可以连接多少个客户端
# while 1:
#     # 阻塞等待，创建连接
#     con,address = ser.accept()  # 在这个位置进行等待，监听端口号
#     while 1:
#         try:
#             # 接受套接字的大小，怎么发就怎么收
#             msg = con.recv(buffer_size)
#             if msg.decode('utf-8') == '1':
#                 # 断开连接
#                 con.close()
#             print('服务器收到消息',msg.decode('utf-8'))
#             # print(search_from_csv(msg.decode('utf-8'), load='weibocut.csv'))
#             con.sendall('aaa')
#         except Exception as e:
#             break
# ser.close()
