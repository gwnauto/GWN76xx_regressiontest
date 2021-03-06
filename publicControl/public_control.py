#coding:utf-8
#描述：公用控制层代码，包括页面共有元素的获取和设置，为基础类
#作者：曾祥卫
#时间：2017.03.10

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import uuid,random,sys
import subprocess,time,pexpect,codecs
import locale
from connect.ssh import SSH
from data import data

data_basic = data.data_basic()
data_login = data.data_login()
data_AP = data.data_AP()

class PublicControl:
    def __init__(self,driver):
        self.driver = driver

    #描述:点击页面主菜单
    #输入:en英文名,chn中文名
    #输出:None
    def menu_css(self,chn,en):
        self.driver.implicitly_wait(20)
        try:
            time.sleep(3)
            first = self.driver.find_element_by_link_text(chn)
            #找到一级菜单，并点击
            first.click()
            self.driver.implicitly_wait(20)
            time.sleep(8)
            print "click ap menu %s successfully!"%chn
        except:
            second = self.driver.find_element_by_link_text(en)
            #找到一级菜单，并点击
            second.click()
            self.driver.implicitly_wait(20)
            time.sleep(8)
            print "click ap menu %s successfully!"%en

    #登录web页面获取DUT的hostname
    def get_DUT_hostname(self):
        try:
            self.driver.implicitly_wait(20)
            element = self.driver.find_element_by_id("hostname")
            result = element.text
            print result
            return result
        except Exception as e:
            raise Exception("webpage has not found 'get_DUT_hostname' element! The reason is %s"%e)



    ###################################################
    #以下是弹出窗口的页面操作
    ###################################################
    #弹出窗口中，点击应用
    def apply_backup(self):
        try:
            time.sleep(5)
            element = self.driver.find_element_by_id("tip-apply")
            element.click()
            self.driver.implicitly_wait(20)
            time.sleep(27)
            #以下检查设备服务状态的窗口是否显示，显示就循环等待5s继续检查，不显示就跳出,持续10分钟
            service_status_element = self.driver.find_element_by_id("service_status_span")
            WebDriverWait(self.driver,720,5).until_not(lambda x:service_status_element.is_displayed())
        except Exception as e:
            raise Exception("webpage has not found 'apply' element! The reason is %s"%e)

     #弹出窗口中，点击应用
    def apply_backup2(self):
        try:
            time.sleep(5)
            element = self.driver.find_element_by_id("tip-apply")
            if element.is_displayed():
                element.click()
                self.driver.implicitly_wait(20)
                time.sleep(27)
            #以下检查设备服务状态的窗口是否显示，显示就循环等待5s继续检查，不显示就跳出,持续10分钟
            service_status_element = self.driver.find_element_by_id("service_status_span")
            WebDriverWait(self.driver,720,5).until_not(lambda x:service_status_element.is_displayed())
        except Exception as e:
            raise Exception("webpage has not found 'apply' element! The reason is %s"%e)


    #弹出窗口中，点击应用
    def apply_backup3(self):
        try:
            time.sleep(5)
            element = self.driver.find_element_by_id("tip-apply")
            print "-----------rick.zeng apply debug:1.the apply button has been found!-----------"
            try:
                element.is_displayed()
            except:
                print "-----------rick.zeng apply debug:2.the displayed attribute of apply hasn't been found!-----------"
                self.driver.refresh()
                time.sleep(30)
            finally:
                if element.is_displayed():
                    element.click()
                    self.driver.implicitly_wait(20)
                    time.sleep(27)
                    print "-----------rick.zeng apply debug:3.apply is displayed, and click apply successfully!-----------"
                else:
                    print "-----------rick.zeng apply debug:4.apply isn't displayed, don't need to click!-----------"
            print "-----------rick.zeng apply debug:5.go in intelligent wait!-----------"
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_id("service_status_span"))
            print "-----------rick.zeng apply debug:6.status element is exist-----------"
            service_status_element = self.driver.find_element_by_id("service_status_span")
            WebDriverWait(self.driver,720,5).until_not(lambda x:service_status_element.is_displayed())
            print "-----------rick.zeng apply debug:7.intelligent wait is finished!-----------"
        except Exception as e:
            raise Exception("webpage has not found 'apply' element! The reason is %s"%e)

    #弹出窗口中，点击应用
    def apply(self):
        try:
            time.sleep(3)
            WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_id("tip-apply"))
            print "-----------rick.zeng apply debug:1.the apply button has been found!-----------"
            element = self.driver.find_element_by_id("tip-apply")
            if element.is_displayed():
                element.click()
                self.driver.implicitly_wait(20)
                time.sleep(27)
                print "-----------rick.zeng apply debug:2.apply is displayed, and click apply successfully!-----------"
            else:
                print "-----------rick.zeng apply debug:3.apply isn't displayed, don't need to click!-----------"
            print "-----------rick.zeng apply debug:4.go in intelligent wait!-----------"
            try:
                WebDriverWait(self.driver,120,5).until(lambda x:self.driver.find_element_by_id("service_status_span"))
                print "-----------rick.zeng apply debug:5.status element is exist-----------"
                service_status_element = self.driver.find_element_by_id("service_status_span")
                WebDriverWait(self.driver,720,5).until_not(lambda x:service_status_element.is_displayed())
                print "-----------rick.zeng apply debug:6.intelligent wait is finished!-----------"
            except:
                print "-----------rick.zeng apply debug:7.can't find status dispaly attribute and refresh webpage to login ap!-----------"
                time.sleep(180)
                self.driver.get(data_basic['DUT_web'])
                self.driver.implicitly_wait(60)
                self.driver.refresh()
                self.driver.implicitly_wait(60)
                #登录AP
                self.driver.find_element_by_id("username").send_keys(data_basic['superUser'])
                self.driver.find_element_by_id("password").send_keys(data_login['all'])
                self.driver.find_element_by_id("loginbtn").click()
        except Exception as e:
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            png = "error_apply_%s.png"%str(current_time)
            self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
            raise Exception("webpage has not found 'apply' element! The reason is %s"%e)


    #弹出窗口中，点击撤销
    def cancel(self):
        try:
            element = self.driver.find_element_by_id("tip-revert")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'cancel' element! The reason is %s"%e)


    ###################################################
    #以下是弹出提示窗口的页面操作
    ###################################################
    #弹出的提示窗口中，点击确认
    def notice_ok_backup(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
        except Exception as e:
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            png = "error_notick_%s.png"%str(current_time)
            self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
            raise Exception("webpage has not found 'notice_ok' element! The reason is %s"%e)

    #弹出的提示窗口中，点击确认
    def notice_ok(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-primary']")
            element.click()
            self.driver.implicitly_wait(10)
            time.sleep(5)
        except Exception as e:
            current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
            png = "error_notick_%s.png"%str(current_time)
            self.driver.get_screenshot_as_file("./data/testresultdata/"+png)
            raise Exception("webpage has not found 'notice_ok' element! The reason is %s"%e)


    #弹出的提示窗口中，点击确认
    def notice_cancel_backup(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-cancel")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'notice_cancel' element! The reason is %s"%e)

    #弹出的提示窗口中，点击确认
    def notice_cancel(self):
        try:
            self.driver.implicitly_wait(10)
            element = self.driver.find_element_by_xpath(".//div[@class='modal-footer']//button[@class='btn btn-cancel']")
            element.click()
            self.driver.implicitly_wait(10)
        except Exception as e:
            raise Exception("webpage has not found 'notice_cancel' element! The reason is %s"%e)




    ###################################################
    #以下是PC端操作
    ###################################################

    #描述：Client端在终端输入命令,命令结果返回给函数
    #输入：self,cmd-client在终端输入的命令
    #输出：output-在终端显示的结果
    def get_client_cmd_result(self,cmd):
        try:
            #Client端在终端输入命令,命令结果返回给函数
            result = subprocess.check_output(cmd,shell=True)
            print "Input cmd %s in PC successfully!"%cmd
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("input command in PC fail! The reason is %s"%e)

    #描述:获取本地mac地址
    #输入:无
    #输出:mac-字符串类型，本地mac
    def get_localmac(self):
        try:
            tmp = uuid.UUID(int=uuid.getnode()).hex[-12:]
            mac = ":".join([tmp[e:e+2] for e in range(0,11,2)])
            return mac
        except Exception,e:
            raise Exception("get local mac address fail! The reason is %s"%e)

    #描述：获取本地无线mac地址
    #输入：wlan：本机无线接口名
    #输出：本机的无线mac地址
    def get_wlan_mac(self,wlan):
        try:
            tmp1 = PublicControl.get_client_cmd_result(self,'ifconfig %s'%wlan)
            tmp2 = tmp1.split('\n')
            tmp3 = tmp2[0]
            #tmp4 = tmp3.strip(" ")
            result =tmp3[-19:-2]
            print result
            return result
        except Exception,e:
            raise Exception("get wlan mac fail! The reason is %s"%e)

    #描述:mac地址去冒号
    #输入:无
    #输出:mac-字符串类型
    def mac_drop(self,mac):
        try:
            tmp = mac.split(":")
            tmp1 = ''.join(tmp)
            print tmp1
            return tmp1
        except Exception,e:
            raise Exception("mac drop : fail! The reason is %s"%e)

    #描述：获取本地IP
    #输入：eth：本机网卡接口名
    #输出：本机的IP地址
    def get_localIp(self,eth):
        try:
            language = locale.getdefaultlocale()#获取系统语言
            result1 = PublicControl.get_client_cmd_result(self,'ifconfig %s'%eth)
            result2 = result1.split('inet')
            result = result2[1].split(" ")
            if 'en_US' in language:
                ip =  result[1].strip('addr:')
            else:
                ip =  result[1].strip('地址:')
            print ip
            return ip
        except Exception,e:
            raise Exception("get local ip fail! The reason is %s"%e)

    #描述:ping IP地址
    #输入:str-ip地址或域名
    #输出:ping结果0或非0
    def get_ping(self,str):
        try:
            ping = "ping %s -c 3"%str
            result = subprocess.call(ping,shell=True)
            print "the result of ping %s is %s"%(str,result)
            return result
        except Exception,e:
            raise Exception("ping ip address fail! The reason is %s"%e)

    #描述:用以在后台判断某个进程在不在
    #输入:某个进程
    #输出:True-存在，反之
    def ssh_ps(self,host,user,pwd,process):
        try:
            i =0
            while(i<5):
                ssh = SSH(host,pwd)
                result = ssh.ssh_cmd(user,"ps")
                if process in result:
                    return True
                time.sleep(20)
                i+=1
            return False
        except Exception,e:
            raise Exception("judge the process in AP fail! The reason is %s"%e)


    #描述：禁用网卡,然后再启用网卡
    #输入：self
    #输出：None
    def networkcard_disable_enable(self):
        try:
            d = data.data_basic()
            #禁用eth0网卡
            down = pexpect.spawn('sudo ifconfig %s down'%d['lan_pc'],timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(15)

            #启用eth0网卡
            up = pexpect.spawn('sudo ifconfig %s up'%d['lan_pc'],timeout=5)
            up.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            up.sendline(d["PC_pwd"])
            time.sleep(15)
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("disable/enable eth of PC fail! The reason is %s"%e)

    #描述：本机PC上,替换代测的新旧固件，然后开启tftp&http&https&rsyslog服务
    #输入：self
    #输出：None
    def replace_FW(self):
        try:
            d = data.data_basic()
            #首先改变拷贝过来的新固件的用户组，路径默认在~/FW/7610_FW/
            #subprocess.call('echo %s |sudo -S chown test:test ~/FW/7610_FW/new/*'%d["PC_pwd"],shell=True)
            #subprocess.call('echo %s |sudo -S chown test:test ~/FW/7610_FW/old/*'%d["PC_pwd"],shell=True)
            #删除old,new文件夹里面的旧固件
            subprocess.call('echo %s |sudo -S rm ~/tftp/old/* /var/www/html/old/*'%d["PC_pwd"],shell=True)
            subprocess.call('echo %s |sudo -S rm ~/tftp/new/* /var/www/html/new/*'%d["PC_pwd"],shell=True)


            #将最新固件拷贝到new目录下
            subprocess.call('cp ~/FW/7610_FW/new/* ~/tftp/new/',shell=True)
            subprocess.call('echo %s |sudo -S cp ~/FW/7610_FW/new/* /var/www/html/new/'%d["PC_pwd"],shell=True)
            #将旧固件拷贝到old目录下
            subprocess.call('cp ~/FW/7610_FW/old/* ~/tftp/old/',shell=True)
            subprocess.call('echo %s |sudo -S cp ~/FW/7610_FW/old/* /var/www/html/old/'%d["PC_pwd"],shell=True)

            #重启tftp 和http,rsyslog服务器
            subprocess.call('echo %s |sudo -S /etc/init.d/tftpd-hpa restart'%d["PC_pwd"],shell=True)
            subprocess.call('echo %s |sudo -S /etc/init.d/apache2 restart'%d["PC_pwd"],shell=True)
            subprocess.call('echo %s |sudo -S /etc/init.d/rsyslog restart'%d["PC_pwd"],shell=True)
            print "replace FW and start tftp&http&https&rsyslog service successfully!"
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("replace_FW and start tftp&http&https&rsyslog service fail! The reason is %s"%e)


    #描述：通过ssh登录路由后台,输入reboot重启路由,并等待60s
    #输入：self
    #输出：None
    def reboot_router(self,host,user,pwd):
        try:
            #在路由器中输入reboot
            ssh = SSH(host,pwd)
            ssh.ssh_cmd(user,"reboot")
            #time.sleep(180)
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("input reboot after login AP fail! The reason is %s"%e)

    #描述：通过ssh登录路由后台，取出路由当前的版本号
    #输入：self
    #输出：路由当前的版本号
    def get_router_version(self,host,user,pwd):
        try:
            #在路由器中输入cat /tmp/gs_version
            ssh = SSH(host,pwd)
            result = ssh.ssh_cmd(user,"cat /tmp/gs_version")
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("get_router_version fail! The reason is %s"%e)


    #描述：通过ssh登录路由后台，取出路由的mac地址
    #输入：self
    #输出：路由的mac地址
    def get_router_mac(self,host,user,pwd):
        try:
            #在路由器后台
            ssh = SSH(host,pwd)
            result1 = ssh.ssh_cmd(user,"ifconfig eth0 | grep HWaddr")
            result = result1[-21:-4]
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("get_router_mac fail! The reason is %s"%e)


    #取随机mac
    def randomMAC(self):
        try:
            mac = [ 0x00, 0x0c,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
            return ':'.join(map(lambda x: "%02x" % x, mac))
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("get random MAC fail! The reason is %s"%e)

    #取随机ip地址
    def randomip(self):
        try:
            a = random.randint(1,254)
            b = random.randint(1,254)
            c = random.randint(1,254)
            d = random.randint(1,254)
            ip = '%s.%s.%s.%s'%(a,b,c,d)
            return ip
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("get random IP address fail! The reason is %s"%e)



    ###################################################
    #以下是无线网卡的控制方法
    ###################################################

    #描述：禁用无线网卡
    #输入：pinself
    #输出：None
    def wlan_disable(self,wlan):
        try:
            d = data.data_basic()
            #禁用无线网卡
            down = pexpect.spawn('sudo ifconfig %s down'%wlan,timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(15)
            print "Disable %s successfully!"%wlan
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("disable wlan of PC fail! The reason is %s"%e)

    #描述：启用无线网卡
    def wlan_enable(self,wlan):
        try:
            d = data.data_basic()
            #启用无线网卡
            up = pexpect.spawn('sudo ifconfig %s up'%wlan,timeout=5)
            up.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            up.sendline(d["PC_pwd"])
            time.sleep(15)
            print "Enable %s successfully!"%wlan
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("enable wlan of PC fail! The reason is %s"%e)

    #描述：扫描无线信号,返回扫描的结果-----备用,不准
    def ssid_scan_backup(self,ssid,wlan):
        try:
            #输入命令进行无线ssid扫描
            result = subprocess.check_output('iwlist %s scanning | grep %s'%(wlan,ssid),shell=True)
            f = open('./data/testresultdata/ssidScanResult.txt','a')
            f.write(result)
            f.close()
            print result
            return result
        #捕捉异常并打印异常信息
        except:
            return False

    #描述：扫描无线信号,返回扫描的结果
    def ssid_scan(self,ssid,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #通过wpa_cli命令来断开已连接的无线网络
            PublicControl.disconnect_ap(self)
            time.sleep(20)
            while True:
                #输入命令进行无线ssid扫描
                result = subprocess.check_output('echo %s |sudo -S iw dev %s scan | grep %s'%(d['PC_pwd'],wlan,ssid),shell=True)
                time.sleep(30)
                if "command failed" in result:
                    print "command failed,scan AP again!"
                    PublicControl.get_client_cmd_result(self,"echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"])
                    time.sleep(60)
                    continue
                f = open('./data/testresultdata/ssidScanResult.txt','a')
                f.write(result)
                f.close()
                print "scan AP has finished!"
                print result
                return result
        #捕捉异常并打印异常信息
        except :
            print "scan AP no result"
            return "scan AP no result!"

    #描述：连接AP后，验证AP的加密类型
    def check_AP_encryption(self):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #输入命令进行无线ssid扫描
            result = PublicControl.get_client_cmd_result(self,\
                'echo %s |sudo -S iwlist %s wpakeys'%(d['PC_pwd'],d['wlan_pc']))
            #print result
            return result
        #捕捉异常并打印异常信息
        except:
            return False


    #描述：扫描无线信号,判断是否能够扫描到AP的SSID
    #输入：指定的无线ssid,无线网卡接口名wlan
    #输出：扫描的结果 如下：
    def ssid_scan_result(self,ssid,wlan):
        result = PublicControl.ssid_scan(self,ssid,wlan)
        #获取无线SSID
        ssid1 = result.strip('	SSID: ')
        print ssid1
        if ssid in ssid1:
            print "scan AP successfully!"
            return True
        else:
            print "scan AP failed!"
            return False

    #描述：扫描无线信号,判断是否能够扫描到AP的SSID--备份
    #输入：指定的无线ssid,无线网卡接口名wlan
    #输出：扫描的结果 如下：
    def ssid_scan_result_backup(self,ssid,wlan):
        for i in range(3):
            result = PublicControl.ssid_scan(self,ssid,wlan)
            #获取无线SSID
            ssid1 = result.strip('	SSID: ')
            if ssid in ssid1:
                print "scan AP successfully!"
                return True
            time.sleep(60)
        print "scan AP failed!"
        return False

    #描述：通过wpa_cli命令来连接不加密的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名
    #输出：输入命令返回的结果
    def connect_NONE_AP(self,ssid,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                'remove_network 0'
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                print 'add_network'
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print ESSID
                child.sendline(ESSID)
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                print 'set_network 0 key_mgmt NONE'
                #禁用无线网络id为0网络
                child.expect('>')
                child.sendline('disable_network 0')
                print 'disable_network 0'
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print 'enable_network 0'
                time.sleep(10)
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print 'quit'
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True)
                if "Not connected" in result1:
                    print "Connect AP failed,wait 60s and try again the times:%s"%(i+1)
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    d_login = data.data_login()
                    ssh = SSH(d['DUT_ip'],d_login['all'])
                    ssh.ssh_cmd(d['sshUser'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print "Connect AP successfully!"
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of NONE encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接不加密的无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名
    #输出：输入命令返回的结果
    def connect_NONE_AP_backup(self,ssid,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            print 'remove_network 0'
            #增加无线网络id为0的配置
            child.expect('>')
            child.sendline('add_network')
            print 'add_network'
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print ESSID
            child.sendline(ESSID)
            #设置无线网络id为0的加密为非加密
            child.expect('>')
            child.sendline('set_network 0 key_mgmt NONE')
            print 'set_network 0 key_mgmt NONE'
            #禁用无线网络id为0网络
            child.expect('>')
            child.sendline('disable_network 0')
            print 'disable_network 0'
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            print 'enable_network 0'
            time.sleep(10)
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            print 'quit'
            #退出wpa_cli交互模式
            child.close(force=True)
            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of NONE encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print 'remove_network 0'
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                print 'add_network'
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print ESSID
                child.sendline(ESSID)
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                print 'set_network 0 key_mgmt NONE'
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 wep_key0 \"%s\"'%str(password)
                print key
                child.sendline(key)
                child.expect('>')
                child.sendline('set_network 0 wep_tx_keyidx 0')
                print 'set_network 0 wep_tx_keyidx 0'
                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print 'select_network 0'
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print 'enable_network 0'
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print 'quit'
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True)
                if "Not connected" in result1:
                    print "Connect AP failed,wait 60s and try again the times:%s"%(i+1)
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    d_login = data.data_login()
                    ssh = SSH(d['DUT_ip'],d_login['all'])
                    ssh.ssh_cmd(d['sshUser'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print "Connect AP successfully!"
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WEP encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP的无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP_AP_backup(self,ssid,password,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            print 'remove_network 0'
            #增加无线网络id为0的配置
            child.expect('>')
            child.sendline('add_network')
            print 'add_network'
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print ESSID
            child.sendline(ESSID)
            #设置无线网络id为0的加密为非加密
            child.expect('>')
            child.sendline('set_network 0 key_mgmt NONE')
            print 'set_network 0 key_mgmt NONE'
            #设置无线网络id为0的密码
            child.expect('>')
            key = 'set_network 0 wep_key0 \"%s\"'%str(password)
            print key
            child.sendline(key)
            child.expect('>')
            child.sendline('set_network 0 wep_tx_keyidx 0')
            print 'set_network 0 wep_tx_keyidx 0'
            #选择无线网络id为0网络
            child.expect('>')
            child.sendline('select_network 0')
            print 'select_network 0'
            time.sleep(10)
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            print 'enable_network 0'
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            print 'quit'
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WEP encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP-10位或26位的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP10_26_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print 'remove_network 0'
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                print 'add_network'
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print ESSID
                child.sendline(ESSID)
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                print 'set_network 0 key_mgmt NONE'
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 wep_key0 %s'%str(password)
                print key
                child.sendline(key)
                child.expect('>')
                child.sendline('set_network 0 wep_tx_keyidx 0')
                print 'set_network 0 wep_tx_keyidx 0'
                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print 'select_network 0'
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print 'enable_network 0'
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print 'quit'
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True)
                if "Not connected" in result1:
                    print "Connect AP failed,wait 60s and try again the times:%s"%(i+1)
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    d_login = data.data_login()
                    ssh = SSH(d['DUT_ip'],d_login['all'])
                    ssh.ssh_cmd(d['sshUser'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print "Connect AP successfully!"
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WEP encryption fail! The reason is %s"%e)


    #描述：通过wpa_cli命令来连接WPA的无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_WPA_AP_backup(self,ssid,password,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            print 'remove_network 0'
            #增加无线网络id为0 的配置
            child.expect('>')
            child.sendline('add_network')
            print 'add_network'
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print ESSID
            child.sendline(ESSID)
            #设置无线网络id为0的密码
            child.expect('>')
            key = 'set_network 0 psk \"%s\"'%str(password)
            print key
            child.sendline(key)

            #选择无线网络id为0网络
            child.expect('>')
            child.sendline('select_network 0')
            print 'select_network 0'
            time.sleep(10)
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            print 'enable_network 0'
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            print 'quit'
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WPA encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WPA的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_WPA_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print 'remove_network 0'
                #增加无线网络id为0 的配置
                child.expect('>')
                child.sendline('add_network')
                print 'add_network'
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print ESSID
                child.sendline(ESSID)
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 psk \"%s\"'%str(password)
                print key
                child.sendline(key)

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print 'select_network 0'
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print 'enable_network 0'
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print 'quit'
                #退出wpa_cli交互模式
                child.close(force=True)
                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True)
                if "Not connected" in result1:
                    print "Connect AP failed,wait 60s and try again the times:%s"%(i+1)
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    d_login = data.data_login()
                    ssh = SSH(d['DUT_ip'],d_login['all'])
                    ssh.ssh_cmd(d['sshUser'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print "Connect AP successfully!"
                    break
            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WPA encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接802.1x的无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_8021x_AP(self,ssid,username,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print 'remove_network 0'
                #增加无线网络id为0 的配置
                child.expect('>')
                child.sendline('add_network')
                print 'add_network'
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print ESSID
                child.sendline(ESSID)

                child.expect('>')
                print 'set_network 0 key_mgmt WPA-EAP'
                child.sendline('set_network 0 key_mgmt WPA-EAP')
                child.expect('>')
                print 'set_network 0 eap PEAP'
                child.sendline('set_network 0 eap PEAP')
                child.expect('>')
                #输入用户名
                Uname = 'set_network 0 identity \"%s\"'%str(username)
                print Uname
                child.sendline(Uname)
                child.expect('>')
                #输入密码
                PW = 'set_network 0 password \"%s\"'%str(password)
                print PW
                child.sendline(PW)
                child.expect('>')

                print 'set_network 0 eapol_flags 0'
                child.sendline('set_network 0 eapol_flags 0')

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print 'select_network 0'
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print 'enable_network 0'
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print 'quit'
                #退出wpa_cli交互模式
                child.close(force=True)
                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True)
                if "Not connected" in result1:
                    print "Connect AP failed,wait 60s and try again the times:%s"%(i+1)
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    d_login = data.data_login()
                    ssh = SSH(d['DUT_ip'],d_login['all'])
                    ssh.ssh_cmd(d['sshUser'],"iwconfig")
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print "Connect AP successfully!"
                    break
            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result

        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WPA 802.1x encryption fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接802.1x的无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_8021x_AP_backup(self,ssid,username,password,wlan):
        try:
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                print 'remove_network 0'
                #增加无线网络id为0 的配置
                child.expect('>')
                child.sendline('add_network')
                print 'add_network'
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print ESSID
                child.sendline(ESSID)

                child.expect('>')
                print 'set_network 0 key_mgmt WPA-EAP'
                child.sendline('set_network 0 key_mgmt WPA-EAP')
                child.expect('>')
                print 'set_network 0 eap PEAP'
                child.sendline('set_network 0 eap PEAP')
                child.expect('>')
                #输入用户名
                Uname = 'set_network 0 identity \"%s\"'%str(username)
                print Uname
                child.sendline(Uname)
                child.expect('>')
                #输入密码
                PW = 'set_network 0 password \"%s\"'%str(password)
                print PW
                child.sendline(PW)
                child.expect('>')

                print 'set_network 0 eapol_flags 0'
                child.sendline('set_network 0 eapol_flags 0')

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                print 'select_network 0'
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                print 'enable_network 0'
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                print 'quit'
                #退出wpa_cli交互模式
                child.close(force=True)
                #判断是否连接AP成功
                result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
                print result
                return result

        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WPA 802.1x encryption fail! The reason is %s"%e)


    #描述：通过wpa_cli命令来断开已连接的无线网络
    def disconnect_ap(self):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            #退出wpa_cli
            child.expect('>')
            time.sleep(2)
            child.sendline('quit')
            #退出wpa_cli交互模式
            child.close(force=True)
            print "disconnect ap successfully!"
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("disconnect ap fail! The reason is %s"%e)


    #描述：通过wpa_cli命令来连接不加密的隐藏无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名
    #输出：输入命令返回的结果
    def connect_NONE_hiddenssid_AP(self,ssid,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print ESSID
                child.sendline(ESSID)
                #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
                child.expect('>')
                print 'set_network 0 scan_ssid 1'
                child.sendline('set_network 0 scan_ssid 1')
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                #禁用无线网络id为0网络
                child.expect('>')
                child.sendline('disable_network 0')
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                time.sleep(10)
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True)
                if "Not connected" in result1:
                    print "Connect AP failed,wait 60s and try again the times:%s"%(i+1)
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print "Connect hide AP successfully!"
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of NONE encryption and hiddenssid fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接不加密的隐藏无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名
    #输出：输入命令返回的结果
    def connect_NONE_hiddenssid_AP_backup(self,ssid,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            #增加无线网络id为0的配置
            child.expect('>')
            child.sendline('add_network')
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print ESSID
            child.sendline(ESSID)
            #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
            child.expect('>')
            print 'set_network 0 scan_ssid 1'
            child.sendline('set_network 0 scan_ssid 1')
            #设置无线网络id为0的加密为非加密
            child.expect('>')
            child.sendline('set_network 0 key_mgmt NONE')
            #禁用无线网络id为0网络
            child.expect('>')
            child.sendline('disable_network 0')
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            time.sleep(10)
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of NONE encryption and hiddenssid fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP的隐藏无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP_hiddenssid_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                #增加无线网络id为0的配置
                child.expect('>')
                child.sendline('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print ESSID
                child.sendline(ESSID)
                #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
                child.expect('>')
                print 'set_network 0 scan_ssid 1'
                child.sendline('set_network 0 scan_ssid 1')
                #设置无线网络id为0的加密为非加密
                child.expect('>')
                child.sendline('set_network 0 key_mgmt NONE')
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 wep_key0 \"%s\"'%str(password)
                print key
                child.sendline(key)
                child.expect('>')
                child.sendline('set_network 0 wep_tx_keyidx 0')

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True)
                if "Not connected" in result1:
                    print "Connect AP failed,wait 60s and try again the times:%s"%(i+1)
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print "Connect hide AP successfully!"
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WEP encryption and hiddenssid fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WEP的隐藏无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wep的密码
    #输出：输入命令返回的结果
    def connect_WEP_hiddenssid_AP_backup(self,ssid,password,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            #增加无线网络id为0的配置
            child.expect('>')
            child.sendline('add_network')
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print ESSID
            child.sendline(ESSID)
            #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
            child.expect('>')
            print 'set_network 0 scan_ssid 1'
            child.sendline('set_network 0 scan_ssid 1')
            #设置无线网络id为0的加密为非加密
            child.expect('>')
            child.sendline('set_network 0 key_mgmt NONE')
            #设置无线网络id为0的密码
            child.expect('>')
            key = 'set_network 0 wep_key0 \"%s\"'%str(password)
            print key
            child.sendline(key)
            child.expect('>')
            child.sendline('set_network 0 wep_tx_keyidx 0')

            #选择无线网络id为0网络
            child.expect('>')
            child.sendline('select_network 0')
            time.sleep(10)
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WEP encryption and hiddenssid fail! The reason is %s"%e)


    #描述：通过wpa_cli命令来连接WPA的隐藏无线网络
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_WPA_hiddenssid_AP(self,ssid,password,wlan):
        try:
            for i in range(3):
                #获取测试主机密码
                d = data.data_basic()
                #进入wpa_cli的配置命令
                child = pexpect.spawn('sudo wpa_cli',timeout=5)
                child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
                child.sendline(d['PC_pwd'])
                time.sleep(5)

                #删除无线网络id为0的配置
                child.expect('>')
                child.sendline('remove_network 0')
                #增加无线网络id为0 的配置
                child.expect('>')
                child.sendline('add_network')
                #设置无线网络id为0的无线ssid
                child.expect('>')
                ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
                print ESSID
                child.sendline(ESSID)
                #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
                child.expect('>')
                print 'set_network 0 scan_ssid 1'
                child.sendline('set_network 0 scan_ssid 1')
                #设置无线网络id为0的密码
                child.expect('>')
                key = 'set_network 0 psk \"%s\"'%str(password)
                print key
                child.sendline(key)

                #选择无线网络id为0网络
                child.expect('>')
                child.sendline('select_network 0')
                time.sleep(10)
                #启用无线网络id为0网络
                child.expect('>')
                child.sendline('enable_network 0')
                #退出wpa_cli
                child.expect('>')
                time.sleep(20)
                child.sendline('quit')
                #退出wpa_cli交互模式
                child.close(force=True)

                #判断是否连接AP成功
                result1 = subprocess.check_output("iw dev %s link"%wlan,shell=True)
                if "Not connected" in result1:
                    print "Connect AP failed,wait 60s and try again the times:%s"%(i+1)
                    #断开已连接的无线网络
                    PublicControl.disconnect_ap(self)
                    #disable/enable 无线网卡
                    PublicControl.wlan_disable(self,wlan)
                    PublicControl.wlan_enable(self,wlan)
                    PublicControl.ssid_scan_result(self,ssid,wlan)
                    subprocess.call("echo %s |sudo -S /etc/init.d/network-manager restart"%d["PC_pwd"],shell=True)
                    time.sleep(60)
                else:
                    print "Connect hide AP successfully!"
                    break

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WPA encryption and hiddenssid fail! The reason is %s"%e)

    #描述：通过wpa_cli命令来连接WPA的隐藏无线网络--备份
    #输入：ssid:需要连接的无线网络的ssid,wlan:无线网卡的接口名,password:wpa的密码
    #输出：输入命令返回的结果
    def connect_WPA_hiddenssid_AP_backup(self,ssid,password,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #进入wpa_cli的配置命令
            child = pexpect.spawn('sudo wpa_cli',timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            time.sleep(5)

            #删除无线网络id为0的配置
            child.expect('>')
            child.sendline('remove_network 0')
            #增加无线网络id为0 的配置
            child.expect('>')
            child.sendline('add_network')
            #设置无线网络id为0的无线ssid
            child.expect('>')
            ESSID = 'set_network 0 ssid \"%s\"'%str(ssid)
            print ESSID
            child.sendline(ESSID)
            #设置无线网络id为0的ssid进行特定扫描，即隐藏的ssid
            child.expect('>')
            print 'set_network 0 scan_ssid 1'
            child.sendline('set_network 0 scan_ssid 1')
            #设置无线网络id为0的密码
            child.expect('>')
            key = 'set_network 0 psk \"%s\"'%str(password)
            print key
            child.sendline(key)

            #选择无线网络id为0网络
            child.expect('>')
            child.sendline('select_network 0')
            time.sleep(10)
            #启用无线网络id为0网络
            child.expect('>')
            child.sendline('enable_network 0')
            #退出wpa_cli
            child.expect('>')
            time.sleep(20)
            child.sendline('quit')
            #退出wpa_cli交互模式
            child.close(force=True)

            #判断是否连接AP成功
            result = subprocess.check_output("iw dev %s link"%wlan,shell=True)
            print result
            return result
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("connect AP of WPA encryption and hiddenssid fail! The reason is %s"%e)


    #描述：使无线网卡获取IP地址
    #输入：wlan:无线网卡的接口名
    #输出：无
    def dhcp_wlan(self,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #输入无线网卡获取IP地址的命令
            down = pexpect.spawn('sudo dhclient %s'%wlan,timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(30)
            print "renew %s ip successfully!"%wlan
        except Exception,e:
            raise Exception("dhcp wlan ip address fail! The reason is %s"%e)

    #描述：使无线网卡释放IP地址
    #输入：wlan:无线网卡的接口名
    #输出：无
    def dhcp_release_wlan(self,wlan):
        try:
            #获取测试主机密码
            d = data.data_basic()
            #输入无线网卡获取IP地址的命令
            down = pexpect.spawn('sudo dhclient -r %s'%wlan,timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(10)
            subprocess.call('echo %s |sudo -S /etc/init.d/network-manager force-reload'%d["PC_pwd"],shell=True)
            time.sleep(20)
            print "release %s ip successfully!"%wlan
        except Exception,e:
            raise Exception("dhcp release wlan ip address fail! The reason is %s"%e)

    #判断使用无线网卡能够连接上ssid,并正常使用
    def connect_DHCP_WPA_AP(self,ssid,password,wlan):
        result = PublicControl.connect_WPA_AP(self,ssid,password,wlan)
        if "Not connected" not in result:
            PublicControl.dhcp_wlan(self,wlan)
            print ssid
            return result
        else:
            print "wifi card hasn't connected AP! "
            return result

    #使用无线网卡连接上AP后，取出该AP的频率值
    def connected_AP_Freq(self,ssid,password,wlan):
        a = PublicControl.connect_WPA_AP(self,ssid,password,wlan)
        if "Not connected" not in a:
            b = a.split("\n\t")
            d = b[-8].strip("freq: ")
            print int(d)
            return int(d)
        else:
            print "wifi card hasn't connected AP! "

    #使用无线网卡连接上AP后，取出该AP的linkspeed
    def connected_AP_linkspeed(self,ssid,password,wlan):
        a = PublicControl.connect_WPA_AP(self,ssid,password,wlan)
        if "Not connected" not in a:
            b = a.split("\n\t")
            c = b[-4].split(" ")
            d = float(c[2])
            print int(d)
            return int(d)
        else:
            print "wifi card hasn't connected AP! "

    #扫描双频的AP，扫描5次，当扫描到有两个相同SSID时就退出，没有就返回None
    def scan_dual_band_same_SSID(self,ssid,wlan):
        for i in range(5):
            tmp = PublicControl.ssid_scan(self,ssid,wlan)
            tmp1 = tmp.split("\n\t")
            result = len(tmp1)
            print result
            if result == 2:
                print "wifi card can scan two same SSID!"
                return result
            print "wifi card can't scan two same SSID,wait 60s and go on..."
            time.sleep(60)
        print "scan 5 times,wifi card can't scan two same SSID!"


    #rsyslog服务器准备
    def ready_rsyslog(self):
        d = data.data_basic()
        d_login = data.data_login()
        subprocess.call('echo %s |sudo -S rm -rf /var/log/%s.log'%(d["PC_pwd"],d['DUT_ip']),shell=True)
        #重启rsyslog服务器
        subprocess.call('echo %s |sudo -S /etc/init.d/rsyslog restart'%d["PC_pwd"],shell=True)
        #删除AP中的core文件
        PublicControl.del_AP_core_file(self,d['DUT_ip'],d['sshUser'],d_login['all'])
        PublicControl.del_slave_ap_core_file(self,data_basic['slave_ip1'],d['sshUser'])
        PublicControl.del_slave_ap_core_file(self,data_basic['slave_ip2'],d['sshUser'])
        print "Delete core file of AP and ready rsyslog service successfully!"
        #将ap恢复出厂设置
        PublicControl.set_ap_factory(self,d['slave_ip1'])
        PublicControl.set_ap_factory(self,d['slave_ip2'])
        time.sleep(180)
        print "set slave ap factory successfully!"

    #rsyslog服务器完成工作
    def finish_rsyslog(self,cases):
        d = data.data_basic()
        d_login = data.data_login()
        #将该用例集的syslog拷贝到./data/log,并根据用例集重命名
        subprocess.call('echo %s |sudo -S cp /var/log/%s.log \
        ./data/log/syslog_%s.log'%(d["PC_pwd"],d['DUT_ip'],cases),shell=True)
        if PublicControl.check_AP_core_file(self,d['DUT_ip'],d['sshUser'],d_login['all']):
            #将core file从AP中拷出，并传到/data/core中
            PublicControl.cp_core_file(self,d['DUT_ip'],d['sshUser'],d_login['all'],cases)
        if PublicControl.check_slave_AP_core_file(self,data_basic['slave_ip1'],d['sshUser']):
            PublicControl.cp_slave_core_file(self,data_basic['slave_ip1'],d['sshUser'],cases)
        if PublicControl.check_slave_AP_core_file(self,data_basic['slave_ip2'],d['sshUser']):
            PublicControl.cp_slave_core_file(self,data_basic['slave_ip2'],d['sshUser'],cases)
        print "Copy syslog of cases: %s successfully! "%cases

    #判断AP中是否有core文件,有则返回True,没有则返回False
    def check_AP_core_file(self,host,user,pwd):
        #在路由器中输入ls /data/core
        ssh = SSH(host,pwd)
        result = ssh.ssh_cmd(user,"ls /data/core")
        if "GWN" in result:
            print "AP has core file!"
            return True
        else:
            print "AP hasn't core file!"
            return False

    #判断slave AP中是否有core文件,有则返回True,没有则返回False
    def check_slave_AP_core_file(self,host,user):
        #在路由器中输入ls /data/core
        result = PublicControl.check_ap_factory(self,host)
        if result:
            pwd = data_basic['super_defalut_pwd']
        else:
            pwd = data_login['all']
        ssh = SSH(host,pwd)
        result1 = ssh.ssh_cmd(user,"ls /data/core")
        if "GWN" in result1:
            print "AP has core file!"
            return True
        else:
            print "AP hasn't core file!"
            return False

    #删除AP中的core文件
    def del_AP_core_file(self,host,user,pwd):
        #在路由器中输入rm -rf /data/core/*
        ssh = SSH(host,pwd)
        ssh.ssh_cmd(user,"rm -rf /data/core/*")
        ssh.ssh_cmd(user,"rm -rf core_file.tgz")
        print "Delete core file of AP successfully!"

    #删除slave ap的core file
    def del_slave_ap_core_file(self,host,user):
        #删除slave中的core file
        result = PublicControl.check_ap_factory(self,host)
        if result == True:
            PublicControl.del_AP_core_file(self,host,user,data_basic['super_defalut_pwd'])
        else:
            PublicControl.del_AP_core_file(self,host,user,data_login['all'])

    #将core file从AP中拷出，并传到/data/core中
    def cp_core_file(self,host,user,pwd,cases):
        d = data.data_basic()
        #在路由器中输入打包并传到PC的tftp服务器中
        ssh = SSH(host,pwd)
        core_file_time = ssh.ssh_cmd(user,"ls -lh /data/core/")
        print "The core file time of AP is %s"%core_file_time
        current_time = ssh.ssh_cmd(user,"date")
        print "The current time of AP is %s"%current_time
        PC_time = PublicControl.get_client_cmd_result(self,"date")
        print "The current time of test PC is %s"%PC_time
        ssh.ssh_cmd(user,"tar cvzf core_file.tgz /data/core/")
        #传到tftp服务器中
        pc_ip = PublicControl.get_localIp(self,d['lan_pc'])
        ssh.ssh_cmd(user,"tftp -p -l core_file.tgz %s"%pc_ip)
        #从tftp中拷贝到/data/core中
        subprocess.call('mv ~/tftp/core_file.tgz ./data/core_file/core_file_%s.tgz'%cases,shell=True)
        print "Copy core file from AP successfully!"

        #将core file从AP中拷出，并传到/data/core中
    def cp_slave_core_file(self,host,user,cases):
        result = PublicControl.check_ap_factory(self,host)
        if result:
            pwd = data_basic['super_defalut_pwd']
        else:
            pwd = data_login['all']
        d = data.data_basic()
        #在路由器中输入打包并传到PC的tftp服务器中
        ssh = SSH(host,pwd)
        core_file_time = ssh.ssh_cmd(user,"ls -lh /data/core/")
        print "The core file time of AP is %s"%core_file_time
        current_time = ssh.ssh_cmd(user,"date")
        print "The current time of AP is %s"%current_time
        PC_time = PublicControl.get_client_cmd_result(self,"date")
        print "The current time of test PC is %s"%PC_time
        ssh.ssh_cmd(user,"tar cvzf core_file.tgz /data/core/")
        print "1"
        #传到tftp服务器中
        pc_ip = PublicControl.get_localIp(self,d['lan_pc'])
        ssh.ssh_cmd(user,"tftp -p -l core_file.tgz %s"%pc_ip)
        #从tftp中拷贝到/data/core中
        subprocess.call('mv ~/tftp/core_file.tgz ./data/core_file/core_file_%s.tgz'%cases,shell=True)
        print "Copy core file from AP successfully!"

    #描述：登录ftp后ftp上传文件
    def ftp_put(self,putfilename):
        d = data.data_basic()
        #使用spawn构造一个函数，生成一个spawn类的对象
        child = pexpect.spawn('ftp %s'%d['ftp_server'],timeout=5)
        #期望具有提示输入用户名的字符出现
        index = child.expect(["(?i)Unknown host", "(?i)Name", pexpect.EOF, pexpect.TIMEOUT])
        #匹配到了"(?i)Name"，表明接下来要输入用户名
        if index != 0 :
            #输入用户名
            child.sendline(d['ftp_name'])
            #期望具体有提示输入密码的字符出现
            child.expect(["(?i)Password", pexpect.EOF, pexpect.TIMEOUT])
            child.sendline(d['ftp_pwd'])
            #期望登录成功并出现'ftp>'的字符出现
            index = child.expect( ['ftp>', 'Login incorrect', 'Service not available',pexpect.EOF, pexpect.TIMEOUT])
            #匹配到了'ftp>'，则表示登录ftp成功
            if index == 0:
                print u'恭喜！ftp登录成功'
                # 发送 'bin'+ 换行符给子程序，表示接下来使用二进制模式来传输文件.
                child.sendline("bin")
                child.expect('>')
                child.sendline("cd %s"%d['ftp_dir'])
                print u'正在上传文件...'
                #输入上传文件的命令
                child.sendline('put %s'%putfilename)
                time.sleep(180)
                #期望下载成功后，出现 'Transfer complete*ftp>'的字符
                index = child.expect( ['ftp>', pexpect.EOF, pexpect.TIMEOUT] )
                #没有匹配到'*ftp>'的字符，表示EOF或超时，打印超时并退出
                if index != 0:
                    print u"上传文件时出现EOF或超时"
                    #强制退出
                    child.close(force=True)
                #匹配到了 '*ftp>'，表明上传文件成功，打印成功信息.
                print u'成功上传文件%s'%putfilename

                #输入 'bye'，结束 ftp session.
                child.sendline("bye")
                print u'传输文件完成，程序退出！'

            #匹配到了'Login incorrect'，则表示登录ftp失败，用户名或密码错误
            elif index == 1:
                print u"登录ftp失败，用户名或密码错误!程序退出"
                child.close(force=True)

            #匹配到其他值（'Service not available',pexpect.EOF, pexpect.TIMEOUT），则表示登录ftp失败.
            else:
                print u"登录ftp失败，服务器不可用或ftp命令退出或超时!程序退出"
                child.close(force=True)

        #匹配到了"(?i)Unknown host"，则表示主机未知
        elif index == 1 :
            print u"没有找到ftp主机!程序退出"
            child.close(force=True)

        #匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出
        else:
            print u"连接ftp时出现EOF或超时"
            child.close(force=True)

    #描述：登录ftp后ftp下载文件
    def ftp_get(self,putfilename):
        d = data.data_basic()
        #使用spawn构造一个函数，生成一个spawn类的对象
        child = pexpect.spawn('ftp %s'%d['ftp_server'],timeout=5)
        #期望具有提示输入用户名的字符出现
        index = child.expect(["(?i)Unknown host", "(?i)Name", pexpect.EOF, pexpect.TIMEOUT])
        #匹配到了"(?i)Name"，表明接下来要输入用户名
        if index != 0 :
            #输入用户名
            child.sendline(d['ftp_name'])
            #期望具体有提示输入密码的字符出现
            child.expect(["(?i)Password", pexpect.EOF, pexpect.TIMEOUT])
            child.sendline(d['ftp_pwd'])
            #期望登录成功并出现'ftp>'的字符出现
            index = child.expect( ['ftp>', 'Login incorrect', 'Service not available',pexpect.EOF, pexpect.TIMEOUT])
            #匹配到了'ftp>'，则表示登录ftp成功
            if index == 0:
                print u'恭喜！ftp登录成功'
                # 发送 'bin'+ 换行符给子程序，表示接下来使用二进制模式来传输文件.
                child.sendline("bin")
                child.expect('>')
                child.sendline("cd %s"%d['ftp_dir'])
                print u'正在下载文件...'
                #输入上传文件的命令
                child.sendline('get %s'%putfilename)
                time.sleep(180)
                #期望下载成功后，出现 'Transfer complete*ftp>'的字符
                index = child.expect( ['ftp>', pexpect.EOF, pexpect.TIMEOUT] )
                #没有匹配到'*ftp>'的字符，表示EOF或超时，打印超时并退出
                if index != 0:
                    print u"上传文件时出现EOF或超时"
                    #强制退出
                    child.close(force=True)
                #匹配到了 '*ftp>'，表明上传文件成功，打印成功信息.
                print u'成功下载文件%s'%putfilename

                #输入 'bye'，结束 ftp session.
                child.sendline("bye")
                print u'传输文件完成，程序退出！'

            #匹配到了'Login incorrect'，则表示登录ftp失败，用户名或密码错误
            elif index == 1:
                print u"登录ftp失败，用户名或密码错误!程序退出"
                child.close(force=True)

            #匹配到其他值（'Service not available',pexpect.EOF, pexpect.TIMEOUT），则表示登录ftp失败.
            else:
                print u"登录ftp失败，服务器不可用或ftp命令退出或超时!程序退出"
                child.close(force=True)

        #匹配到了"(?i)Unknown host"，则表示主机未知
        elif index == 1 :
            print u"没有找到ftp主机!程序退出"
            child.close(force=True)

        #匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出
        else:
            print u"连接ftp时出现EOF或超时"
            child.close(force=True)

    #移动resolv.conf到/etc/目录下
    def move_resolv(self):
        d = data.data_basic()
        subprocess.call('echo %s |sudo -S cp ./data/resolv.conf /etc/'%(d["PC_pwd"]),shell=True)
        time.sleep(10)
        print "move resolv.conf to /etc/ successfully!"


    #判断并等待直到slave ap已经在可解除配对的状态
    def enable_unpair_slave_ap(self,slave_ip):
        try:
            while True:
                #在路由器中输入netstat -ant
                ssh = SSH(data_basic['DUT_ip'],data_login['all'])
                result = ssh.ssh_cmd(data_basic['sshUser'],"netstat -ant | grep %s"%slave_ip)
                if ("TIME_WAIT" not in result) and ("ESTABLISHED" in result):
                    break
                time.sleep(30)
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("check slave ap can been unpair fail! The reason is %s"%e)

    #将ap恢复出厂设置
    def set_ap_factory(self,ip):
        try:
            #在路由器中输入netstat -ant
            ssh = SSH(ip,data_login['all'])
            ssh.ssh_cmd(data_basic['sshUser'],"ubus call controller.icc factory_reset")
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("set ap factory fail! The reason is %s"%e)

    #作者:蒋甜

    #给无线网卡固定ip
    #wlan为无线网卡名，ip为要设置的固定ip
    def set_client_ip(self,ip):
        try:
            d = data.data_basic()
         #使用spawn构造一个函数，生成一个spawn类的对象
         #将要设置的无线网卡名和固定ip拼接成一个字符串
            child = pexpect.spawn('sudo ifconfig %s %s'%(d['wlan_pc'],ip),timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            print(u'设置固定ip成功')
            time.sleep(5)
        except Exception,e:
            raise Exception("set PC ip fail! The reason is %s"%e)


    #取消给无线网卡固定ip
    def remove_client_ip(self):
        try:
            d = data.data_basic()
         #使用spawn构造一个函数，生成一个spawn类的对象
            child = pexpect.spawn('sudo dhclient -r %s'%d['wlan_pc'],timeout=5)
            child.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            child.sendline(d['PC_pwd'])
            print(u'移除设置固定ip成功')
            time.sleep(5)
        except Exception,e:
            raise Exception("remove PC ip fail! The reason is %s"%e)

    #描述：禁用网卡
    #输入：self
    #输出：None
    def networkcard_disable(self):
        try:
            d = data.data_basic()
            #禁用eth0网卡
            down = pexpect.spawn('sudo ifconfig %s down'%d['lan_pc'],timeout=5)
            down.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            down.sendline(d["PC_pwd"])
            time.sleep(15)
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("disable eth of PC fail! The reason is %s"%e)

    #描述：启用网卡
    #输入：self
    #输出：None
    def networkcard_enable(self):
        try:
            d = data.data_basic()
            #启用eth0网卡
            up = pexpect.spawn('sudo ifconfig %s up'%d['lan_pc'],timeout=5)
            up.expect([':',pexpect.TIMEOUT,pexpect.EOF])
            up.sendline(d["PC_pwd"])
            time.sleep(15)
        #捕捉异常并打印异常信息
        except Exception,e:
            raise Exception("enable eth of PC fail! The reason is %s"%e)

    #判断ap是否是恢复
    def check_ap_factory(self,ip):
        while True:
            ping1 = self.get_ping(ip)
            if ping1 == 0:
                break
            time.sleep(60)
        ssh = SSH(ip,data_basic['super_defalut_pwd'])
        admin_pwd = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.general.admin_password")
        if "='admin'" in admin_pwd:
            print "true"
            return True
        else:
            print "false"
            return False


    #抓图方法
    def get_picture(self,picture_name):
        current_time = time.strftime('%m%d%H%M',time.localtime(time.time()))
        png = "error_%s_%s.png"%(picture_name,str(current_time))
        self.driver.get_screenshot_as_file("./data/testresultdata/"+png)

