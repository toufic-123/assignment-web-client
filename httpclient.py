#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        
        # parse url using urllib
        parsedUrl = urllib.parse.urlparse(url)
        urlHost = parsedUrl.hostname
        urlPort = parsedUrl.port
        
        # if the port is empty set it to 80 by default
        if urlPort == None:
            urlPort = 80
        
        # return the host and port
        return urlHost,urlPort



    # dont need to touch
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    
    
    def get_code(self, data):
        # get the second parameter
        code = data.split()[1]
        return int(code)

   
   
    def get_headers(self,data):
        # get everything above the body
        splitHeader = data.split("\r\n\r\n")[0]
        return splitHeader

    
    
    def get_body(self, data):
        # get the body
        splitBody = data.split("\r\n\r\n")[1]
        return splitBody
    
    
    
    # dont need to touch
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    
    
    def close(self):
        self.socket.close()
    
    
    # dont need to touch
    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    
    
    def GET(self, url, args=None):
        code = 500
        body = ""

        # get the host and the port from the url
        urlHost, urlPort = self.get_host_port(url)
        # print((urlHost, urlPort))

        # get the path from the url
        urlPath = urllib.parse.urlparse(url).path
        
        # if the path is empty set it to /
        if urlPath == "":
            urlPath = '/'
        
        # connect using the host and port
        self.connect(urlHost, urlPort)

        # make the string to send
        requestStr = f"GET " + urlPath + " HTTP/1.1\r\nHost: " + urlHost + "\r\nConnection: close\r\n\r\n"
        
        # send the string
        self.sendall(requestStr)
        
        # get the response from the socket
        response = self.recvall(self.socket)

        
        # get the code and body from the response
        code = self.get_code(response)
        body = self.get_body(response)
        
        # close the socket
        self.close()
        return HTTPResponse(code, body)

    
    
    def POST(self, url, args=None):
        code = 500
        body = ""
        
        # get the host and the port from the url
        urlHost, urlPort = self.get_host_port(url)
        
        # get the path from the url
        urlPath = urllib.parse.urlparse(url).path
        
        # if the path is empty set it to /
        if urlPath == "":
            urlPath = '/'
        
        # connect using the host and port from url
        self.connect(urlHost, urlPort)

        # begin making the request string to send
        requestStr = f"POST " + urlPath + " HTTP/1.1\r\nHost: " + urlHost + "\r\nAccept: */*\r\nConnection: close\r\nContent-Type: application/x-www-form-urlencoded\r\n"

        # if there is content find the length of the content, otherwise is it length 0
        if args:
            requestStr += "Content-Length: " + str(len(urllib.parse.urlencode(args).encode('utf-8'))) + "\r\n\r\n" + urllib.parse.urlencode(args)
        else:
            requestStr += f"Content-Length: 0 \r\n\r\n"
        
        # send the requestStr
        self.sendall(requestStr)

        # get the response from the socket
        response = self.recvall(self.socket)

        
        # get the code and body from the response
        code = self.get_code(response)
        body = self.get_body(response)
        
        # close the socket
        self.close()
        return HTTPResponse(code, body)
        
        

    
    
    # dont need to touch
    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )


# dont need to touch    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
