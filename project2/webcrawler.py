#!/usr/bin/python

__author__ = 'steven'

import socket
import BeautifulSoup
import re
import urlparse
import sys


# get session id
def get_session(source):
    pattern = re.compile(r'sessionid\s*=\s*(\w+)')
    pat_search = pattern.search(source)
    if pat_search != None:
        return pat_search.group(1)

# get csrftoken
def get_token(source):
    pattern = re.compile(r'csrftoken\s*=\s*(\w+)')
    pat_search = pattern.search(source)
    if pat_search != None:
        return pat_search.group(1)

# http get
def http_get_content():
    hostname = 'cs5700sp15.ccs.neu.edu'
    port = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.send('GET /accounts/login/?next=/fakebook/ HTTP/1.0\r\n\r\n')
    msg_recv = s.recv(8192)
    s.close()
    return msg_recv

def http_post_content(sessionid, csrftoken, username, password):
    hostname = 'cs5700sp15.ccs.neu.edu'
    port = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))

    header = 'POST /accounts/login/?next=/fakebook/ HTTP/1.0\r\n'
    header += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
    header += 'Accept-Encoding: gzip, deflate\r\n'
    header += 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6\r\n'
    header += 'Cache-Control:max-age=0\r\n'
    header += 'Connection:keep-alive\r\n'
    header += 'Content-Length: 95\r\n'
    header += 'Content-Type: application/x-www-form-urlencoded\r\n'
    header += 'Cookie: ' + 'csrftoken=' + csrftoken + '; ' + 'sessionid=' + sessionid + '\r\n'
    header += 'Origin: http://cs5700sp15.ccs.neu.edu\r\n'
    header += 'Refer: http://cs5700sp15.ccs.neu.edu/accounts/login/?next=/fakebook/\r\n'
    header += 'User-Agent: HTTPTool/1.0\r\n'
    header += '\r\n'
    data = 'username' + '=' + username + '&' + 'password' + '=' + password + '&' + 'csrfmiddlewaretoken' + '=' + csrftoken + '&' + 'next=\fakebook' + '\r\n\r\n'
    s.send(header + data)
    msg_recv_new = s.recv(8192)
    s.close()
    return msg_recv_new

def get_html_text(url, sessionid):
    # get the home page
    hostname = 'cs5700sp15.ccs.neu.edu'
    port = 80
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    header = 'GET ' + url + ' HTTP/1.0\r\nCookie: sessionid=' + sessionid + '\r\n\r\n'
    s.send(header)
    msg_recv = s.recv(8192)
    s.close()
    return msg_recv

def get_url(str):
    index = str.find('/fakebook/')
    return str[index:]


# spider begin
def crawler(sessionid):
    FLAGS = []
    urls = ['http://cs5700sp15.ccs.neu.edu/fakebook/']
    visited = ['http://cs5700sp15.ccs.neu.edu/fakebook/', 'http://www.northeastern.edu', 'http://www.ccs.neu.edu/home/choffnes/']

    while len(urls) > 0:
        html_content = get_html_text(get_url(urls[0]), sessionid)
        soup = BeautifulSoup.BeautifulSoup(html_content)
        urls.pop(0)
        print len(urls)
        for tag in soup.findAll('a', href=True):
            for flag in soup.findAll('h2', {'class': 'secret_flag', 'style': 'color:red'}):
                if flag.string not in FLAGS:
                    FLAGS.append(flag.string)
            if tag.get('href')[0] == '/':
                temp = 'http://cs5700sp15.ccs.neu.edu' + tag.get('href')
                if temp not in visited:
                    urls.append(temp)
                    visited.append(temp)

    return FLAGS


if (len(sys.argv) != 3):
    print 'the number of parameters is not correct, please enter again'
else:
    USERNAME = sys.argv[1]
    PASSWORD = sys.argv[2]

#USERNAME = '001725635'
#PASSWORD = 'CEU6WOYL'

msg = http_get_content()
SESSIONID = get_session(msg)
CSRFTOKEN = get_token(msg)
msg_new = http_post_content(SESSIONID, CSRFTOKEN, USERNAME, PASSWORD)
SESSIONID_NEW = get_session(msg_new)
print crawler(SESSIONID_NEW)
