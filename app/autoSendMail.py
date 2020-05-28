# -*- coding: utf-8 -*-
import smtplib
# 发送邮件
def autoSendMail(title, content,to_addr=None):
    # 输入Email地址和口令:
    from_addr = 'auto1023193134@163.com'
    password = '1234dhcp'
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.163.com'
    # 输入收件人地址:
    if to_addr == None:
        to_addr = '1023193134@qq.com'
    # 输入内容
    mailb = ["auto send:", content]
    mailh = ["From: " + from_addr, "To: " + to_addr, "Subject: auto send mail:" + title]
    mailmsg = "\r\n\r\n".join(["\r\n".join(mailh), "\r\n".join(mailb)])

    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    server.login(from_addr, password)
    server.sendmail(from_addr, (to_addr), mailmsg)
    server.quit()