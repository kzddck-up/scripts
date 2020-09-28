# 本脚本基于python3.7编写，理论适用于所有python3系列
# 更新时间：2020.09.29
# 作者；ck
# 使用说明：将下面的部分数据修改为你的，然后挂在腾讯云函数即可

import requests
import smtplib


######以下为需要修改的信息##########
#1：修改为你的发件邮箱地址,请使用QQ邮箱，其他邮箱请自行修改代码
email='1512403685@qq.com'
#2：发件邮箱的授权码(需开启POP3/IMAP/SMTP)等服务
password_key='tvxergwufcfogcfh'
#3：收件人邮箱，支持多邮箱发送。
# 示例代码take_email= ['1209739382@qq.com','806108998@qq.com']
take_email= ['1209739382@qq.com','806108998@qq.com']
#4：发送邮箱的标题
sendtxt= '京东签到状态'
#5：修改为你的cookie
cookie = '_4SBJCPFL72HWC3FOTQTHFKWI7WQXL3QHYJ67MFWTJK35EU; shshshfp=b15caf769ad32ca7cbdfd24de423a8df; shshshsID=11de7742fafbbb1845c857b66f269ebf_1_1599733010077; __jdv=122270672%7Cdirect%7C-%7Cnone%7C-%7C1599732656305'
#sever酱获取地址，https://sc.ftqq.com，不会可不填写
sever='SCU96331Tbec475a0fd8594f8bf14ba8862539e915ead8cf7a620c'
######以上为需要修改的信息##########



######以下代码切勿进行任何修改######
url = 'http://ckcode.tooo.top:3001?cookie='+cookie
urls = 'http://jd.kzddck.cn:3001?cookie='+cookie

def sendEmail(data):
    from email.mime.text import MIMEText
    from email.header import Header
    from_addr = email
    password = password_key
    to_addr = ','.join(take_email)
    smtp_server = 'smtp.qq.com'
    msg = MIMEText(data, 'plain', 'utf-8')
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(sendtxt)
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr.split(','), msg.as_string())
    # 关闭服务器
    server.quit()

#失败通知
def lose(text):
    requests.get('https://sc.ftqq.com/'+sever+'.send?text=京东签到脚本运行失败&desp=%s' +text)

def run(url):
    try:
        try:
            html = requests.get(url).text
            data = html.replace('<br>', "\n")
            sendEmail(data)
            if 'Cookie失效' in data:
                text = '京东cookie失效，请重新获取'
                lose(text)
        except:
            html = requests.get(urls).text
            data = html.replace('<br>', "\n")
            sendEmail(data)
            if 'Cookie失效' in data:
                text = '京东cookie失效，请重新获取'
                lose(text)
    except:
        text = '网络请求错误'
        lose(text)


def main_handler(event, context):
    return run(url)
if __name__ == '__main__':
    run(url)