#coding=utf-8
#作者：曾祥卫
#时间：2017.04.26
#描述：用例集，调用addssid_business

import unittest
from selenium import webdriver
import sys
from clients.client_access.clientaccess_business import ClientAccessBusiness
from login.login_business import LoginBusiness
from network_group.add_ssid.addssid_business import AddSSIDBusiness
from access_points.aps_business import APSBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
from network_group.networkgroup_business import NGBusiness
from connect.ssh import SSH
from data import data

reload(sys)
sys.setdefaultencoding('utf-8')

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()

class TestAddSSID(unittest.TestCase):
    u"""测试额外ssid的用例集(runtime:10h)"""
    def setUp(self):
        # firefox_profile = webdriver.FirefoxProfile(data_basic['firefox_profile'])
        # self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(data_basic['DUT_web'])
        self.driver.implicitly_wait(60)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])

    #在页面上把AP恢复出厂设置(testlink_ID:773)
    def test_001_factory_reset(self):
        u"""在页面上把AP恢复出厂设置(testlink_ID:773)"""
        #如果登录没有成功，再次使用默认密码登录;如果登录成功则直接退出
        Lg = LoginBusiness(self.driver)
        Lg.login_again()

        tmp = APSBusiness(self.driver)
        #描述：启用无线网卡
        tmp.wlan_enable(data_basic['wlan_pc'])
        #rsyslog服务器准备
        tmp.ready_rsyslog()
        result = tmp.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        assert result,"reset the AP defalut config in webpage,fail!"
        print "reset the AP defalut config in webpage,pass!"

     #添加额外ssid是否能够连接成功(testlink_ID:300_1)
    def test_002_add_ssid(self):
        u"""添加额外ssid是否能够连接成功(testlink_ID:300_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #新建一个额外的ssid
        tmp.new_ssid(data_wireless['add_ssid'],data_wireless['short_wpa'])
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test new Additional SSID,test fail!"
        print "test new Additional SSID,test pass!"

    #enable/disable Additional SSID的正常配置(testlink_ID:300_2)
    def test_003_check_first_en_dis_status(self):
        u"""enable/disable Additional SSID的正常配置(testlink_ID:300_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #enable/disable Additional SSID的正常配置
        result1,result2 = tmp.check_first_en_dis_status()
        assert (result1 == "enableicon") and (result2 == "disableicon"),\
            "check enable/disable additional ssid config,test fail!"
        print "check enable/disable additional ssid config,test pass!"

    #enable/disable Additional SSID的功能验证(testlink_ID:301)
    def test_004_check_en_dis_function(self):
        u"""enable/disable Additional SSID的正常配置(testlink_ID:301)"""
        tmp = AddSSIDBusiness(self.driver)
        #disable状态下，使用无线网卡扫描该ssid
        result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        #enable/disable first Additional SSID
        tmp.en_dis_first()
        #无线连接这个的AP
        result2 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == False) and (data_wireless['add_ssid'] in result2),\
            "check enable/disable additional ssid function,test fail!"
        print "check enable/disable additional ssid function,test pass!"

    #SSID为空的配置验证(testlink_ID:302)
    def test_005_check_blank_ssid(self):
        u"""SSID为空的配置验证(testlink_ID:302)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2 = tmp.check_blank_ssid()
        ##enable/disable first Additional SSID
        tmp.en_dis_first()
        assert result1 and (result2 == "disableicon"),\
            "check blank ssid in additional ssid,test fail!"
        print "check blank ssid in additional ssid,test pass!"

    #英文/数字、英文+数字和ASCII标准符号的 SSID 的正常配置(testlink_ID:303)
    def test_006_check_ssid_config(self):
        u"""英文/数字、英文+数字和ASCII标准符号的 SSID 的正常配置(testlink_ID:303)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2,result3,result4 = tmp.check_ssid_config(data_wireless['letter_ssid'],\
                        data_wireless['digital_ssid'],data_wireless['digital_letter_ssid'],\
                        data_wireless['ascii_ssid'])
        assert (result1 == data_wireless['letter_ssid']) and (result2 == data_wireless['digital_ssid']) \
            and (result3 == data_wireless['digital_letter_ssid']) and (result4 == data_wireless['ascii_ssid']),\
            "check ssid config,test fail!"
        print "check ssid config,test pass!"

    #SSID 对英文的SSID 的支持(testlink_ID:304_1)
    def test_007_check_SSID_letter(self):
        u"""SSID 对英文的SSID 的支持(testlink_ID:304_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['letter_ssid'])
        result = tmp.ssid_scan_result_backup(data_wireless['letter_ssid'],data_basic["wlan_pc"])
        assert result,"Check letter SSID,test fail!"
        print "Check letter SSID,test pass!"

    #SSID 对数字的SSID 的支持(testlink_ID:304_2)
    def test_008_check_SSID_digital(self):
        u"""SSID 对数字的SSID 的支持(testlink_ID:304_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['digital_ssid'])
        result = tmp.ssid_scan_result_backup(data_wireless['digital_ssid'],data_basic["wlan_pc"])
        assert result,"Check digital SSID,test fail!"
        print "Check digital SSID,test pass!"

    #SSID 对英文+数字的SSID 的支持(testlink_ID:304_3)
    def test_009_check_SSID_letter_digital(self):
        u"""SSID 对英文+数字的SSID 的支持(testlink_ID:304_3)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['digital_letter_ssid'])
        result = tmp.ssid_scan_result_backup(data_wireless['digital_letter_ssid'],data_basic["wlan_pc"])
        assert result,"Check letter+digital SSID,test fail!"
        print "Check letter+digital SSID,test pass!"

    #SSID对ASCII的支持(testlink_ID:304_4)
    def test_010_check_SSID_ASCII(self):
        u"""SSID对ASCII的支持(testlink_ID:304_4)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['ascii_ssid'])
        #获取第一个额外ssid的名字
        result = tmp.get_first_ssid_name()
        assert data_wireless['ascii_ssid'] in result,"Check ASCII SSID,test fail!"
        print "Check ASCII SSID,test pass!"

    #中文SSID的正常配置(testlink_ID:305)
    def test_011_check_SSID_CN(self):
        u"""中文SSID的正常配置(testlink_ID:305)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['CN_ssid'])
        #获取第一个额外ssid的名字
        result = tmp.get_first_ssid_name()
        assert data_wireless['CN_ssid'] in result,"Check CN SSID,test fail!"
        print "Check CN SSID,test pass!"

    #特殊符号的SSID配置(testlink_ID:307)
    def test_012_check_SSID_special(self):
        u"""特殊符号的SSID配置(testlink_ID:307)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['special_ssid'])
        #获取第一个额外ssid的名字
        result = tmp.get_first_ssid_name()
        assert data_wireless['special_ssid'] in result,"Check special SSID,test fail!"
        print "Check specail SSID,test pass!"

    #修改已配置的SSID(testlink_ID:308)
    def test_013_change_SSID(self):
        u"""修改已配置的SSID(testlink_ID:308)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid为全英文
        tmp.modify_ssid(data_wireless['letter_ssid'])
        result1 = tmp.connect_WPA_AP(data_wireless['letter_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        #修改第一个额外ssid的ssid为混合
        tmp.modify_ssid(data_wireless['add_ssid'])
        result2 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        assert (data_wireless['letter_ssid'] in result1) and (data_wireless['add_ssid'] in result2),\
            "Check change SSID,test fail!"
        print "Check change SSID,test pass!"

    #验证SSID的字符长度限制(testlink_ID:309)
    def test_014_SSID_max(self):
        u"""验证SSID的字符长度限制(testlink_ID:309)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['long_ssid']+"abc")
        #获取第一个额外ssid的名字
        result1 = tmp.get_first_ssid_name()
        result2 = tmp.connect_WPA_AP(data_wireless['long_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        assert ((data_wireless['long_ssid']+"abc") not in result1) and (data_wireless['long_ssid'] in result1) \
            and ((data_wireless['long_ssid']+"abc") not in result2) and (data_wireless['long_ssid'] in result2),\
            "Check max SSID,test fail!"
        print "Check max SSID,test pass!"

    #Name里含有空格的SSID(testlink_ID:310)
    def test_015_SSID_blank(self):
        u"""Name里含有空格的SSID(testlink_ID:310)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        ssid = data_wireless['letter_ssid']+" "+data_wireless['digital_ssid']
        tmp.modify_ssid(ssid)
        #获取第一个额外ssid的名字
        result1 = tmp.get_first_ssid_name()
        result2 = tmp.connect_WPA_AP(ssid,data_wireless["short_wpa"],\
                                    data_basic['wlan_pc'])
        assert (ssid in result1) and (ssid in result2),"Check SSID contain blank,test fail!"
        print "Check SSID contain blank,test pass!"

    #关闭开启WIFI对连接在SSID无线终端的影响(testlink_ID:311)
    def test_016_disable_enable_wifi(self):
        u"""关闭开启WIFI对连接在SSID无线终端的影响(testlink_ID:311)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['add_ssid'])
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        #enable/disable first Additional SSID
        tmp.en_dis_first()
        result2 = tmp.get_client_cmd_result("iw dev %s link"%data_basic['wlan_pc'])
        #enable/disable first Additional SSID
        tmp.en_dis_first()
        result3 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        assert (data_wireless['add_ssid'] in result1) and ("Not connected" in result2)\
            and (data_wireless['add_ssid'] in result3),"Check client status after disable/enable wifi,test fail!"
        print "Check client status after disable/enable wifi,test pass!"

    #Enable Hide SSID 的配置、功能(testlink_ID:312)
    def test_017_enable_hidden(self):
        u"""测试隐藏无线ssid(testlink_ID:311)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置第一个额外ssid隐藏
        tmp.set_hide_ssid()
        #获取第一个额外ssid的隐藏状态
        result1 = tmp.get_first_hide()
        #无线扫描，无法扫描到
        result2 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        #通过连接隐藏ssid的方法能够连接上该ssid
        result3 = tmp.connect_WPA_hiddenssid_AP(data_wireless['add_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        #断开无线连接
        tmp.disconnect_ap()
        assert (result1 == "enableicon") and (result2 == False) and\
               (data_wireless['add_ssid'] in result3),\
            "test hidden ssid,test fail!"
        print "test hidden ssid,test pass!"

    #重启后测试隐藏无线ssid是否依然生效(testlink_ID:319)
    def test_018_reboot_hidden_SSID(self):
        u"""重启后测试隐藏无线ssid是否依然生效(testlink_ID:319)"""
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        #无线扫描，无法扫描到
        result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        #通过连接隐藏ssid的方法能够连接上该ssid
        result2 = tmp.connect_WPA_hiddenssid_AP(data_wireless['add_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result2,\
            "test hidden ssid after rebootting,test fail!"
        print "test hidden ssid after rebootting,test pass!"

    #Hide 有终端连接的SSID(testlink_ID:313)
    def test_019_hidden_ssid_client_connected(self):
        u"""Hide 有终端连接的SSID(testlink_ID:313)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置取消第一个额外ssid隐藏
        tmp.set_hide_ssid()
        tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless["short_wpa"],data_basic['wlan_pc'])
        #设置第一个额外ssid隐藏
        tmp.set_hide_ssid()
        #通过连接隐藏ssid的方法能够连接上该ssid
        result = tmp.connect_WPA_hiddenssid_AP(data_wireless['add_ssid'],\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,\
            "test hidden ssid if this ssid has been connected,test fail!"
        print "test hidden ssid if this ssid has been connected,test pass!"

    #Hide SSID 的状态下修改SSID(testlink_ID:314)
    def test_020_modify_hidden_ssid(self):
        u"""Hide SSID 的状态下修改SSID(testlink_ID:314)"""
        tmp = AddSSIDBusiness(self.driver)
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['add_ssid']+"02")
        #通过连接隐藏ssid的方法能够连接上该ssid
        result = tmp.connect_WPA_hiddenssid_AP(data_wireless['add_ssid']+"02",\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['add_ssid']+"02") in result,\
            "modify ssid if hidden ssid,test fail!"
        print "modify ssid if hidden ssid,test pass!"

    #关闭、开启WIFI对连接在 Hide SSID 无线终端的影响(testlink_ID:315)
    def test_021_disable_hidden_wifi(self):
        u"""关闭、开启WIFI对连接在 Hide SSID 无线终端的影响(testlink_ID:315)"""
        tmp = AddSSIDBusiness(self.driver)
        #enable/disable first Additional SSID
        tmp.en_dis_first()
        result1 = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['add_ssid']+"02",\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        #enable/disable first Additional SSID
        tmp.en_dis_first()
        result2 = tmp.connect_WPA_hiddenssid_AP(data_wireless['add_ssid']+"02",\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ("Not connected" in result1) and ((data_wireless['add_ssid']+"02") in result2),\
                "test disable/enable wifi on hidden ssid,test fail!"
        print "test disable/enable wifi on hidden ssid,test pass!"

    #Disable Hide SSID 的配置与功能验证(testlink_ID:316)
    def test_022_disable_hidden_ssid(self):
        u"""Disable Hide SSID 的配置与功能验证(testlink_ID:316)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置取消第一个额外ssid隐藏
        tmp.set_hide_ssid()
        #获取第一个额外ssid的隐藏状态
        result1 = tmp.get_first_hide()
        #无线扫描，能够扫描到
        result2 = tmp.ssid_scan_result_backup(data_wireless['add_ssid']+"02",data_basic['wlan_pc'])
        #使用正常连接方式能够连接上
        result3 = tmp.connect_WPA_AP(data_wireless['add_ssid']+"02",\
                data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == "disableicon") and (result2 == True) and\
               ((data_wireless['add_ssid']+"02") in result3),\
                "disable hidden ssid,test fail!"
        print "disable hidden ssid,test pass!"

    #Hide SSID 与 OPEN 加密模式的结合使用验证(testlink_ID:317)
    def test_023_OPEN_hidden_SSID(self):
        u"""Hide SSID 与 OPEN 加密模式的结合使用验证(testlink_ID:317)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置第一个额外ssid隐藏
        tmp.set_hide_ssid()
        #修改第一个额外ssid的ssid
        tmp.modify_ssid(data_wireless['add_ssid'])
        #设置默认网络组无线为非加密
        tmp.wifi_None_encryption()
        result = tmp.connect_NONE_hiddenssid_AP(data_wireless['add_ssid'],data_basic['wlan_pc'])
        #设置默认网络组无线为wpa/wpa2加密
        tmp.wifi_wpa_encryption(3,0,data_wireless['short_wpa'])
        assert data_wireless['add_ssid'] in result,"test OPEN encryption hidden ssid,test fail!"
        print "test OPEN encryption hidden ssid,test pass!"

    #Hide SSID 与 Mac filter 结合使用验证(testlink_ID:318)
    def test_024_mac_filter_hidden_SSID(self):
        u"""Hide SSID 与 Mac filter 结合使用验证(testlink_ID:318)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #添加一个只有一个mac地址的访问列表
        tmp1.add_accesslist_onemac(mac)

        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist()
        #无线连接这个的hidden AP
        result = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #禁用默认网络组的无线过滤
        tmp.disable_macfilter(1)
        #设置取消第一个额外ssid隐藏
        tmp.set_hide_ssid()
        assert 'Not connected' in result,"test mac filter on hidden SSID,test fail!"
        print "test mac filter on hidden SSID,test pass!"

    #AP 2.4G和5G可以同时广播相同SSID
    def test_025_dual_band(self):
        u"""AP 2.4G和5G可以同时广播相同SSID"""
        #确认有两个无线接口
        tmp1 = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = tmp1.ssh_cmd(data_basic['sshUser'],"iwconfig ath2 | grep ESSID")
        result2 = tmp1.ssh_cmd(data_basic['sshUser'],"iwconfig ath3 | grep ESSID")
        assert (data_wireless['add_ssid'] in result1) \
            and (data_wireless['add_ssid'] in result2),"test SSID broadcast of 2.4G and 5G,test fail!"
        print "test SSID broadcast of 2.4G and 5G,test pass!"

    #AP 2.4G和5G BSSID不相同
    def test_026_BSSID(self):
        u"""AP 2.4G和5G BSSID不相同"""
        tmp = SSH(data_basic['DUT_ip'],data_login['all'])
        #取2.4G的BSSID
        BSSID_2g4_tmp = tmp.ssh_cmd(data_basic['sshUser'],"iwconfig ath2 | grep Access")
        BSSID_2g4 = BSSID_2g4_tmp.strip("\n\t")[-21:-4]
        #取5G的BSSID
        BSSID_5g_tmp = tmp.ssh_cmd(data_basic['sshUser'],"iwconfig ath3 | grep Access")
        BSSID_5g = BSSID_5g_tmp.strip("\n\t")[-21:-4]
        print BSSID_2g4,BSSID_5g
        assert BSSID_2g4 != BSSID_5g,"test BSSID of 2.4G and 5G,test fail!"
        print "test BSSID of 2.4G and 5G,test pass!"


    ####################################################################
    ##################以下是加密的测试用例#################################
    ####################################################################
    #测试额外ssid中2.4g的无线加密-为不加密时(testlink_ID:320)
    def test_027_None_encryption(self):
        u"""测试额外ssid中2.4g的无线加密-为不加密时(testlink_ID:320)"""
        #切换2.4G频段
        tmp1 = APSBusiness(self.driver)
        tmp1.change_AP_Freq("2.4GHz")

        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为非加密
        tmp.wifi_None_encryption()
        #无线连接这个非加密的无线
        result = tmp.connect_NONE_AP(data_wireless['add_ssid'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test None encryption of wifi,test fail!"
        print "test None encryption of wifi,test pass!"

    #测试额外ssid中2.4g的无线加密-为5位wep64时(testlink_ID:322_1)
    def test_028_5wep64_encryption(self):
        u"""测试额外ssid中2.4g的无线加密-为5位wep64时(testlink_ID:322_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test 5bits wep64 encryption of wifi,test fail!"
        print "test 5bits wep64 encryption of wifi,test pass!"

    #测试额外ssid中2.4g的无线加密-为10位wep64时(testlink_ID:322_2)
    def test_029_10wep64_encryption(self):
        u"""测试额外ssid中2.4g的无线加密-为10位wep64时(testlink_ID:322_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(0,data_wireless['wep64-10'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['add_ssid'],data_wireless['wep64-10'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test 10bits wep64 encryption of wifi,test fail!"
        print "test 10bits wep64 encryption of wifi,test pass!"

    #2.4g的WEP64bit参数校验1(testlink_ID:324_1)
    def test_030_abnormal1_wep(self):
        u"""2.4g的WEP64bit参数校验1(testlink_ID:324_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep64 abnormal1 encryption,test fail!"
        print "test wep64 abnormal1 encryption,test pass!"

    #2.4g的WEP64bit参数校验2(testlink_ID:324_2)
    def test_031_abnormal2_wep(self):
        u"""2.4g的WEP64bit参数校验2(testlink_ID:324_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep64 abnormal2 encryption,test fail!"
        print "test wep64 abnormal2 encryption,test pass!"

    #测试额外ssid中2.4g的无线加密-为13位wep128时(testlink_ID:323_1)
    def test_032_13wep128_encryption(self):
        u"""测试额外ssid中2.4g的无线加密-为13位wep128时(testlink_ID:323_1)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test 13bits wep128 encryption of wifi,test fail!"
        print "test 13bits wep128 encryption of wifi,test pass!"

    #测试额外ssid中2.4g的无线加密-为26位wep128时(testlink_ID:323_2)
    def test_033_26wep128_encryption(self):
        u"""测试额外ssid中2.4g的无线加密-为26位wep128时(testlink_ID:323_2)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(0,data_wireless['wep128-26'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['add_ssid'],data_wireless['wep128-26'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test 26bits wep128 encryption of wifi,test fail!"
        print "test 26bits wep128 encryption of wifi,test pass!"

    #2.4g的WEP128bit参数校验1(testlink_ID:325_1)
    def test_034_abnormal1_wep(self):
        u"""2.4g的WEP128bit参数校验1(testlink_ID:325_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep128 abnormal1 encryption,test fail!"
        print "test wep128 abnormal1 encryption,test pass!"

    #2.4g的WEP128bit参数校验2(testlink_ID:325_2)
    def test_035_abnormal2_wep(self):
        u"""2.4g的WEP128bit参数校验2(testlink_ID:325_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep128 abnormal2 encryption,test fail!"
        print "test wep128 abnormal2 encryption,test pass!"

    #测试额外ssid中2.4g的无线加密-为wpa/wpa2-AES时(testlink_ID:327)
    def test_036_wpa_mixed_AES_encryption(self):
        u"""测试额外ssid中2.4g的无线加密-为wpa/wpa2-AES时(testlink_ID:327)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa/wpa2-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-AES encryption of wifi,test pass!"


    #2.4g的WPA/WPA2-PSK AES参数校验(testlink_ID:329)
    def test_037_check_AES_arguments(self):
        u"""2.4g的WPA/WPA2-PSK AES参数校验(testlink_ID:329)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check AES arguments,test fail!"
        print "check AES arguments,test pass!"

    #2.4g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:331)
    def test_038_wpa_mixed_AES_max(self):
        u"""2.4g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:331)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check WPA/WPA2-PSK AES max length ,test fail!"
        print "check WPA/WPA2-PSK AES max length,test pass!"

    #测试额外ssid中2.4g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:332)
    def test_039_wpa_mixed_TKIP_encryption(self):
        u"""测试额外ssid中2.4g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:332)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-TKIP的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa/wpa2-TKIP encryption of wifi,test fail!"
        print "test wpa/wpa2-TKIP encryption of wifi,test pass!"

    #2.4g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:334)
    def test_040_check_TKIP_arguments(self):
        u"""2.4g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:334)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check TKIP/AES arguments,test fail!"
        print "check TKIP/AES arguments,test pass!"

    #2.4g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:331)
    def test_041_wpa_mixed_TKIP_AES_max(self):
        u"""2.4g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:331)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check WPA/WPA2-PSK TKIP/AES max length ,test fail!"
        print "check WPA/WPA2-PSK TKIP/AES max length,test pass!"

    #测试额外ssid中2.4g的无线加密-为wpa2-AES时(testlink_ID:337)
    def test_042_wpa2_AES_encryption(self):
        u"""测试额外ssid中2.4g的无线加密-为wpa2-AES时(testlink_ID:337)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"


    #2.4g的wpa2-AES参数校验(testlink_ID:341)
    def test_043_check_WPA2_AES_arguments(self):
        u"""2.4g的wpa2-AES参数校验(testlink_ID:341)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check wpa2-AES arguments,test fail!"
        print "check wpa2-AES arguments,test pass!"

    #2.4g的wpa2-AES 密钥长度限制验证(testlink_ID:346)
    def test_044_wpa2_AES_max(self):
        u"""2.4g的wpa2-AES 密钥长度限制验证(testlink_ID:346)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check wpa2-AES max length ,test fail!"
        print "check wpa2-AES max length,test pass!"

    #测试额外ssid中2.4g的无线加密-为wpa2-TKIP/AES时(testlink_ID:339)
    def test_045_wpa2_TKIP_AES_encryption(self):
        u"""测试额外ssid中2.4g的无线加密-为wpa2-TKIP/AES时(testlink_ID:339)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa2-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-TKIP/AES encryption of wifi,test pass!"


    #2.4g的wpa2-TKIP/AES参数校验(testlink_ID:343)
    def test_046_check_WPA2_TKIP_AES_arguments(self):
        u"""2.4g的wpa2-TKIP/AES参数校验(testlink_ID:343)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check wpa2-TKIP/AESAES arguments,test fail!"
        print "check wpa2-TKIP/AESAES arguments,test pass!"

    #2.4g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:346)
    def test_047_wpa2_TKIP_AES_max(self):
        u"""2.4g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:346)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check wpa2-TKIP/AES max length ,test fail!"
        print "check wpa2-TKIP/AES max length,test pass!"

    #测试额外ssid中2.4g的无线加密-为wpa2-802.1x-TKIP/AES时
    def test_048_wpa2_802_1x_TKIP_AES(self):
        u"""测试额外ssid中2.4g的无线加密-为wpa2-802.1x-TKIP/AES时"""
        tmp = AddSSIDBusiness(self.driver)
        #设置额外ssid无线为wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['add_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa2-802.1x-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-TKIP/AES encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为wpa2-802.1x-AES时
    def test_049_wpa2_802_1x_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa2-802.1x-AES时"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['add_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-AES时
    def test_050_wpa_mixed_802_1x_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-AES时"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(3,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['add_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时
    def test_051_wpa_mixed_802_1x_TKIP_AES(self):
        u"""测试网络组中2.4g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['add_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"


    #测试额外ssid中2.4g的无线加密再次改为wpa2-AES时(testlink_ID:337)
    def test_052_wpa_mixed_AES_encryption(self):
        u"""测试额外ssid中2.4g的无线加密再次改为wpa2-AES时(testlink_ID:337)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"







    #测试额外ssid中5g的无线加密-为不加密时(testlink_ID:320)
    def test_053_None_encryption(self):
        u"""测试额外ssid中5g的无线加密-为不加密时(testlink_ID:320)"""
        #切换5G频段
        tmp1 = APSBusiness(self.driver)
        tmp1.change_AP_Freq("5GHz")

        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为非加密
        tmp.wifi_None_encryption()
        #无线连接这个非加密的无线
        result = tmp.connect_NONE_AP(data_wireless['add_ssid'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test None encryption of wifi,test fail!"
        print "test None encryption of wifi,test pass!"

    #测试额外ssid中5g的无线加密-为5位wep64时(testlink_ID:322_1)
    def test_054_5wep64_encryption(self):
        u"""测试额外ssid中5g的无线加密-为5位wep64时(testlink_ID:322_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test 5bits wep64 encryption of wifi,test fail!"
        print "test 5bits wep64 encryption of wifi,test pass!"

    #测试额外ssid中5g的无线加密-为10位wep64时(testlink_ID:322_2)
    def test_055_10wep64_encryption(self):
        u"""测试额外ssid中5g的无线加密-为10位wep64时(testlink_ID:322_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(0,data_wireless['wep64-10'])
        #无线连接这个wep64的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['add_ssid'],data_wireless['wep64-10'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test 10bits wep64 encryption of wifi,test fail!"
        print "test 10bits wep64 encryption of wifi,test pass!"

    #5g的WEP64bit参数校验1(testlink_ID:324_1)
    def test_056_abnormal1_wep(self):
        u"""5g的WEP64bit参数校验1(testlink_ID:324_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep64 abnormal1 encryption,test fail!"
        print "test wep64 abnormal1 encryption,test pass!"

    #5g的WEP64bit参数校验2(testlink_ID:324_2)
    def test_057_abnormal2_wep(self):
        u"""5g的WEP64bit参数校验2(testlink_ID:324_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep64 abnormal2 encryption,test fail!"
        print "test wep64 abnormal2 encryption,test pass!"

    #测试额外ssid中5g的无线加密-为13位wep128时(testlink_ID:323_1)
    def test_058_13wep128_encryption(self):
        u"""测试额外ssid中5g的无线加密-为13位wep128时(testlink_ID:323_1)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test 13bits wep128 encryption of wifi,test fail!"
        print "test 13bits wep128 encryption of wifi,test pass!"

    #测试额外ssid中5g的无线加密-为26位wep128时(testlink_ID:323_1)
    def test_059_26wep128_encryption(self):
        u"""测试额外ssid中5g的无线加密-为26位wep128时(testlink_ID:323_1)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(0,data_wireless['wep128-26'])
        #无线连接这个wep128的无线
        result = tmp.connect_WEP10_26_AP(data_wireless['add_ssid'],data_wireless['wep128-26'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test 26bits wep128 encryption of wifi,test fail!"
        print "test 26bits wep128 encryption of wifi,test pass!"

    #5g的WEP128bit参数校验1(testlink_ID:325_1)
    def test_060_abnormal1_wep(self):
        u"""5g的WEP128bit参数校验1(testlink_ID:325_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal1_wep'])
        assert result1 and result2,"test wep128 abnormal1 encryption,test fail!"
        print "test wep128 abnormal1 encryption,test pass!"

    #5g的WEP128bit参数校验2(testlink_ID:325_2)
    def test_061_abnormal2_wep(self):
        u"""5g的WEP128bit参数校验2(testlink_ID:325_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #输入异常wep密码，是否有提示
        result1,result2 = tmp.check_abnormal_wep(0,data_wireless['abnormal2_wep'])
        assert result1 and result2,"test wep128 abnormal2 encryption,test fail!"
        print "test wep128 abnormal2 encryption,test pass!"

    #测试额外ssid中5g的无线加密-为wpa/wpa2-AES时(testlink_ID:327)
    def test_062_wpa_mixed_AES_encryption(self):
        u"""测试额外ssid中5g的无线加密-为wpa/wpa2-AES时(testlink_ID:327)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa/wpa2-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-AES encryption of wifi,test pass!"


    #5g的WPA/WPA2-PSK AES参数校验(testlink_ID:329)
    def test_063_check_AES_arguments(self):
        u"""5g的WPA/WPA2-PSK AES参数校验(testlink_ID:329)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check AES arguments,test fail!"
        print "check AES arguments,test pass!"

    #5g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:331)
    def test_064_wpa_mixed_AES_max(self):
        u"""5g的WPA/WPA2-PSK AES 密钥长度限制验证(testlink_ID:331)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check WPA/WPA2-PSK AES max length ,test fail!"
        print "check WPA/WPA2-PSK AES max length,test pass!"

    #测试额外ssid中5g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:332)
    def test_065_wpa_mixed_TKIP_encryption(self):
        u"""测试额外ssid中5g的无线加密-为wpa/wpa2-TKIP/AES时(testlink_ID:332)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa/wpa2-TKIP的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa/wpa2-TKIP encryption of wifi,test fail!"
        print "test wpa/wpa2-TKIP encryption of wifi,test pass!"

    #5g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:334)
    def test_066_check_TKIP_arguments(self):
        u"""5g的WPA/WPA2-PSK TKIP/AES参数校验(testlink_ID:334)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check TKIP/AES arguments,test fail!"
        print "check TKIP/AES arguments,test pass!"

    #5g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:331)
    def test_067_wpa_mixed_TKIP_AES_max(self):
        u"""5g的WPA/WPA2-PSK TKIP/AES 密钥长度限制验证(testlink_ID:331)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check WPA/WPA2-PSK TKIP/AES max length ,test fail!"
        print "check WPA/WPA2-PSK TKIP/AES max length,test pass!"

    #测试额外ssid中5g的无线加密-为wpa2-AES时(testlink_ID:337)
    def test_068_wpa2_AES_encryption(self):
        u"""测试额外ssid中5g的无线加密-为wpa2-AES时(testlink_ID:331)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"


    #5g的wpa2-AES参数校验(testlink_ID:341)
    def test_069_check_WPA2_AES_arguments(self):
        u"""5g的wpa2-AES参数校验(testlink_ID:341)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa/wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check wpa2-AES arguments,test fail!"
        print "check wpa2-AES arguments,test pass!"

    #5g的wpa2-AES 密钥长度限制验证(testlink_ID:346)
    def test_070_wpa2_AES_max(self):
        u"""5g的wpa2-AES 密钥长度限制验证(testlink_ID:346)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check wpa2-AES max length ,test fail!"
        print "check wpa2-AES max length,test pass!"

    #测试额外ssid中5g的无线加密-为wpa2-TKIP/AES时(testlink_ID:339)
    def test_071_wpa2_TKIP_AES_encryption(self):
        u"""测试额外ssid中5g的无线加密-为wpa2-TKIP/AES时(testlink_ID:339)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa2-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-TKIP/AES encryption of wifi,test pass!"


    #5g的wpa2-TKIP/AES参数校验(testlink_ID:343)
    def test_072_check_WPA2_TKIP_AES_arguments(self):
        u"""5g的wpa2-TKIP/AES参数校验(testlink_ID:343)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['all_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['all_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check wpa2-TKIP/AESAES arguments,test fail!"
        print "check wpa2-TKIP/AESAES arguments,test pass!"

    #5g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:346)
    def test_073_wpa2_TKIP_AES_max(self):
        u"""5g的wpa2-TKIP/AES 密钥长度限制验证(testlink_ID:346)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(0,0,data_wireless['long_wpa'])
        #无线连接这个wpa2-TKIP/AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['long_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check wpa2-TKIP/AES max length ,test fail!"
        print "check wpa2-TKIP/AES max length,test pass!"

    #测试额外ssid中5g的无线加密-为wpa2-802.1x-TKIP/AES时
    def test_074_wpa2_802_1x_TKIP_AES(self):
        u"""测试额外ssid中5g的无线加密-为wpa2-802.1x-TKIP/AES时"""
        tmp = AddSSIDBusiness(self.driver)
        #设置额外ssid无线为wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['add_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa2-802.1x-TKIP/AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-TKIP/AES encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为wpa2-802.1x-AES时
    def test_075_wpa2_802_1x_AES(self):
        u"""测试网络组中5g的无线加密-为wpa2-802.1x-AES时"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['add_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为wpa/wpa2-802.1x-AES时
    def test_076_wpa_mixed_802_1x_AES(self):
        u"""测试网络组中5g的无线加密-为wpa/wpa2-802.1x-AES时"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-802.1x-AES
        tmp.wifi_8021x_encryption(3,0,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-AES的无线
        result = tmp.connect_8021x_AP(data_wireless['add_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试网络组中5g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时
    def test_077_wpa_mixed_802_1x_TKIP_AES(self):
        u"""测试网络组中5g的无线加密-为wpa/wpa2-802.1x-TKIP/AES时"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wpa/wpa2-802.1x-TKIP/AES
        tmp.wifi_8021x_encryption(0,1,data_basic['radius_addr'],data_basic['radius_secrect'])
        #无线连接这个wpa/wpa2-802.1x-TKIP/AES的无线
        result = tmp.connect_8021x_AP(data_wireless['add_ssid'],\
                data_basic['radius_usename'],data_basic['radius_password'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test wpa/wpa2-802.1x-AES encryption of wifi,test fail!"
        print "test wpa/wpa2-802.1x-AES encryption of wifi,test pass!"

    #测试额外ssid中5g的无线加密再次改为wpa2-AES时(testlink_ID:337)
    def test_078_wpa_mixed_AES_encryption(self):
        u"""测试额外ssid中5g的无线加密再次改为wpa2-AES时(testlink_ID:337)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #无线连接这个wpa2-AES的无线
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])

        #切换Dual-Band频段
        tmp1 = APSBusiness(self.driver)
        tmp1.change_AP_Freq("Dual-Band")

        assert data_wireless['add_ssid'] in result,"test wpa2-AES encryption of wifi,test fail!"
        print "test wpa2-AES encryption of wifi,test pass!"

    ####################################################################
    ##################以下是Mac Filter的测试用例###########################
    ####################################################################
    #设置额外ssid的无线过滤的白名单,添加本机无线mac地址，并判断无线是否能够连接成功(testlink_ID:362)
    def test_079_mac_whitelist_in(self):
        u"""设置额外ssid的无线过滤的白名单,添加本机无线mac地址，并判断无线是否能够连接成功(testlink_ID:362)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test mac in whitelist,test fail!"
        print "test mac in whitelist,test pass!"

    #设置无线过滤的白名单然后重启ap，并判断无线是否能够连接成功(testlink_ID:369)
    def test_080_reboot_mac_whitelist_in(self):
        u"""设置无线过滤的白名单然后重启ap，并判断无线是否能够连接成功(testlink_ID:369)"""
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test mac in whitelist after reboot ap,test fail!"
        print "test mac in whitelist after reboot ap,test pass!"

    #刷新页面配置，显示是 whitelist 状态
    def test_081_mac_whitelist_display(self):
        u"""刷新页面配置，显示是 whitelist 状态"""
        tmp = AddSSIDBusiness(self.driver)
        #点击网络组菜单，然后在点击额外ssid菜单
        tmp.NG_SSID_menu()
        #获取第一个额外ssid的MAC过滤状态
        result = tmp.get_first_macfilter()
        assert result == (u"白名单" or "Whitelist"),"test mac filter display in whitelist,test fail!"
        print "test mac filter display in whitelist,test pass!"

    #设置额外ssid的无线过滤的白名单,添加随机mac，并判断本机无线是否能够连接成功(testlink_ID:362)
    def test_082_mac_whitelist_out(self):
        u"""设置额外ssid的无线过滤的白名单,添加随机mac，并判断本机无线是否能够连接成功(testlink_ID:362)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取随机mac地址
        random_mac = tmp.randomMAC()
        print random_mac
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert 'Not connected' in result,"test mac out whitelist,test fail!"
        print "test mac out whitelist,test pass!"


    #设置额外ssid的无线过滤的白名单,添加随机小写的mac地址(testlink_ID:362)
    def test_083_lower_mac_whitelist_out(self):
        u"""设置额外ssid的无线过滤的白名单,添加随机小写的mac地址(testlink_ID:362)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取本机无线mac地址
        mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        tmp.edit_accesslist_onemac(mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test lower mac out whitelist,test fail!"
        print "test lower mac out whitelist,test pass!"

    #添加10条mac地址白名单，确认其有效性(testlink_ID:363)
    def test_084_many_mac_whitelist(self):
        u"""添加10条mac地址白名单，确认其有效性(testlink_ID:363)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        tmp = AddSSIDBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，白名单数目
        result1 = tmp.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == 10) and (data_wireless['add_ssid'] in result2),"test many mac_whitelist,test fail!"
        print "test many mac_whitelist,test pass!"

    #删除所有的mac地址白名单，仅保留PC本身的mac，确认其有效性(testlink_ID:359)
    def test_085_del_many_mac_whitelist(self):
        u"""删除所有的mac地址白名单，仅保留PC本身的mac，确认其有效性(testlink_ID:359)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        tmp1 = AddSSIDBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，白名单数目
        result1 = tmp1.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert result1 == 1 and (data_wireless['add_ssid'] in result2),"test del all mac_whitelist,test fail!"
        print "test del all mac_whitelist,test pass!"

    #设置额外ssid的无线过滤的黑名单,添加本机mac地址，并判断无线不能连接成功(testlink_ID:360)
    def test_086_mac_blacklist_in(self):
        u"""设置额外ssid的无线过滤的黑名单,添加本机mad地址，并判断无线不能连接成功(testlink_ID:360)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置额外ssid的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test mac in blacklist,test fail!"
        print "test mac in blacklist,test pass!"

    #刷新页面配置，显示是 blacklist 状态
    def test_087_mac_blacklist_display(self):
        u"""刷新页面配置，显示是 blacklist 状态"""
        tmp = AddSSIDBusiness(self.driver)
        #点击网络组菜单，然后在点击额外ssid菜单
        tmp.NG_SSID_menu()
        #获取第一个额外ssid的MAC过滤状态
        result = tmp.get_first_macfilter()
        assert result == (u"黑名单" or "Blacklist"),"test mac filter display in blacklist,test fail!"
        print "test mac filter display in blacklist,test pass!"

    #设置无线过滤的黑名单然后重启ap，并判断无线是否能够连接成功(testlink_ID:369)
    def test_088_reboot_mac_blacklist_in(self):
        u"""设置无线过滤的黑名单然后重启ap，并判断无线是否能够连接成功(testlink_ID:369)"""
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test mac in blacklist after reboot ap,test fail!"
        print "test mac in blacklist after reboot ap,test pass!"

    #设置额外ssid的无线过滤的黑名单,添加随机mac，并判断本机无线能够连接成功(testlink_ID:362)
    def test_089_mac_blacklist_out(self):
        u"""设置额外ssid的无线过滤的黑名单,添加随机mac，并判断本机无线能够连接成功(testlink_ID:362)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        #取随机mac地址
        random_mac = tmp.randomMAC()
        print random_mac
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test mac out blacklist,test fail!"
        print "test mac out blacklist,test pass!"

    #添加10条mac地址黑名单，确认其有效性(testlink_ID:361)
    def test_090_many_mac_blacklist(self):
        u"""添加10条mac地址黑名单，确认其有效性(testlink_ID:361)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        tmp = AddSSIDBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，黑名单数目
        result1 = tmp.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (result1 == 10) and (data_wireless['add_ssid'] in result2),"test many mac_blacklist,test fail!"
        print "test many mac_blacklist,test pass!"

    #删除所有的mac地址黑名单，仅保留PC本身的mac，确认其有效性(testlink_ID:359)
    def test_091_del_many_mac_blacklist(self):
        u"""删除所有的mac地址黑名单，仅保留PC本身的mac，确认其有效性(testlink_ID:359)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        #取本机无线mac地址
        mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        tmp.edit_accesslist_onemac(mac)

        tmp1 = AddSSIDBusiness(self.driver)
        #登录路由后台，判断mac地址过滤，黑名单数目
        result1 = tmp1.check_mac_list(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        #无线连接这个的AP
        result2 = tmp1.connect_WPA_AP_backup(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert result1 == 1 and ('Not connected' in result2),"test del all mac_blacklist,test fail!"
        print "test del all mac_blacklist,test pass!"

    #禁用mac filter，并判断本机无线能够连接成功(testlink_ID:364)
    def test_092_mac_blacklist_out(self):
        u"""禁用mac filter，并判断本机无线能够连接成功(testlink_ID:364)"""
        #禁用额外ssid的无线过滤
        tmp = AddSSIDBusiness(self.driver)
        tmp.disable_macfilter(1)
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"test mac out blacklist,test fail!"
        print "test mac out blacklist,test pass!"

    #刷新页面配置，显示是 disable 状态
    def test_093_mac_disable_display(self):
        u"""刷新页面配置，显示是 disable 状态"""
        tmp = AddSSIDBusiness(self.driver)
        #点击网络组菜单，然后在点击额外ssid菜单
        tmp.NG_SSID_menu()
        #获取第一个额外ssid的MAC过滤状态
        result = tmp.get_first_macfilter()
        assert result == (u"禁止" or "Disable"),"test mac filter display in disable status,test fail!"
        print "test mac filter display in disable status,test pass!"


    #Blacklist 多zone环境应用功能验证1(testlink_ID:365_1)
    def test_094_check_blacklist_many_addssid1(self):
        u"""Blacklist 多zone环境应用功能验证1(testlink_ID:365_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #新建一个额外的ssid
        tmp.new_ssid(data_wireless['add_ssid']+"2",data_wireless['short_wpa'])
        #有多个额外ssid时，设置第2个额外ssid的无线过滤的黑名单
        tmp.wifi_n_blacklist(2)
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['add_ssid'] in result1) and ('Not connected' in result2),\
            "check blacklist validity in many addssid1,test fail!"
        print "check blacklist validity in many addssid1,test pass!"

    #Blacklist 多zone环境应用功能验证2(testlink_ID:365_2)
    def test_095_check_blacklist_many_addssid2(self):
        u"""Blacklist 多zone环境应用功能验证2(testlink_ID:365_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #有多个额外ssid时，设置第1个额外ssid的无线过滤的黑名单
        tmp.wifi_n_blacklist_backup(1)
        #有多个额外ssid时,禁用第2个的无线过滤
        tmp.disable_macfilter(2)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(data_wireless['add_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ((data_wireless['add_ssid']+"2") in result2),\
            "check blacklist validity in many addssid2,test fail!"
        print "check blacklist validity in many addssid2,test pass!"

    #Blacklist 多zone环境应用功能验证3(testlink_ID:365_3)
    def test_096_check_blacklist_many_addssid3(self):
        u"""Blacklist 多zone环境应用功能验证3(testlink_ID:365_3)"""
        tmp = AddSSIDBusiness(self.driver)
        #有多个额外ssid时，设置第2个额外ssid的无线过滤的黑名单
        tmp.wifi_n_blacklist_backup(2)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ('Not connected' in result2),\
            "check blacklist validity in many addssid3,test fail!"
        print "check blacklist validity in many addssid3,test pass!"

    #Whitelist 多zone环境应用功能验证1(testlink_ID:366_1)
    def test_097_check_Whitelist_many_addssid1(self):
        u"""Whitelist 多zone环境应用功能验证1(testlink_ID:366_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp1.randomMAC()
        tmp1.edit_accesslist_onemac(random_mac)
        tmp = AddSSIDBusiness(self.driver)
        #有多个额外ssid时,禁用第1个的无线过滤
        tmp.disable_macfilter(1)
        #有多个额外ssid时，设置第2个额外ssid的无线过滤的白名单
        tmp.wifi_n_whitelist(2)
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['add_ssid'] in result1) and ('Not connected' in result2),\
            "check whitelist validity in many addssid1,test fail!"
        print "check whitelist validity in many addssid1,test pass!"

    #Whitelist 多zone环境应用功能验证2(testlink_ID:366_2)
    def test_098_check_Whitelist_many_addssid2(self):
        u"""Whitelist 多zone环境应用功能验证2(testlink_ID:366_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #有多个额外ssid时，设置第1个额外ssid的无线过滤的白名单
        tmp.wifi_n_whitelist_backup(1)
        #有多个额外ssid时,禁用第2个的无线过滤
        tmp.disable_macfilter(2)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(data_wireless['add_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ((data_wireless['add_ssid']+"2") in result2),\
            "check whitelist validity in many addssid2,test fail!"
        print "check whitelist validity in many addssid2,test pass!"

    #Whitelist 多zone环境应用功能验证3(testlink_ID:366_3)
    def test_099_check_Whitelist_many_addssid3(self):
        u"""Whitelist 多zone环境应用功能验证3(testlink_ID:366_3)"""
        tmp = AddSSIDBusiness(self.driver)
        #有多个额外ssid时，设置第2个额外ssid的无线过滤的白名单
        tmp.wifi_n_whitelist_backup(2)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ('Not connected' in result2),\
            "check whitelist validity in many addssid3,test fail!"
        print "check whitelist validity in many addssid3,test pass!"

    #Whitelist 多zone环境应用功能验证4(testlink_ID:366_4)
    def test_100_check_Whitelist_many_addssid4(self):
        u"""Whitelist 多zone环境应用功能验证4(testlink_ID:366_4)"""
        tmp = ClientAccessBusiness(self.driver)
        mac = tmp.get_wlan_mac(data_basic["wlan_pc"])
        tmp.edit_accesslist_onemac(mac)
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(data_wireless['add_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['add_ssid'] in result1) and ((data_wireless['add_ssid']+"2") in result2),\
            "check whitelist validity in many addssid4,test fail!"
        print "check whitelist validity in many addssid4,test pass!"

    #Blacklist和whitelist在多zone环境里冲突时的功能验证1(testlink_ID:367_1)
    def test_101_check_mix_many_addssid1(self):
        u"""Blacklist和whitelist在多zone环境里冲突时的功能验证1(testlink_ID:367_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #有多个额外ssid时，设置第1个额外ssid的无线过滤的黑名单
        tmp.wifi_n_blacklist_backup(1)
        result1 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP(data_wireless['add_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert ('Not connected' in result1) and ((data_wireless['add_ssid']+"2") in result2),\
            "check whitelist and blacklist validity in many addssid1,test fail!"
        print "check whitelist and blacklist validity in many addssid1,test pass!"

     #Blacklist和whitelist在多zone环境里冲突时的功能验证2(testlink_ID:367_2)
    def test_102_check_mix_many_addssid2(self):
        u"""Blacklist和whitelist在多zone环境里冲突时的功能验证2(testlink_ID:367_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        tmp.edit_accesslist_onemac(random_mac)
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp.connect_WPA_AP_backup(data_wireless['add_ssid']+"2",\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['add_ssid'] in result1) and ('Not connected' in result2),\
            "check whitelist and blacklist validity in many addssid2,test fail!"
        print "check whitelist and blacklist validity in many addssid2,test pass!"

    #终端的MAC地址在同时配置在 blacklistlist 和whitelist 名单里(testlink_ID:368)
    def test_103_check_mix_sametime_addssid(self):
        u"""Blacklist和whitelist在多zone环境里冲突时的功能验证2"""
        tmp = AddSSIDBusiness(self.driver)
        #删除第二个额外的ssid
        tmp.del_n_ssid(2)
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #禁用第1个的无线过滤
        tmp.disable_macfilter(1)
        assert data_wireless['add_ssid'] in result,\
            "client mac in blacklist and whitelist in the sametime,test fail!"
        print "client mac in blacklist and whitelist in the sametime,test pass!"



    #WEP 64bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:371_1)
    def test_104_wep64_1_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:371_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wep64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WEP64bit,test fail!"
        print "test one mac in blacklist with WEP64bit,test pass!"

    #WEP 64bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:371_2)
    def test_105_wep64_many_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:371_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        result = tmp.connect_WEP_AP_backup(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with WEP64bit,test fail!"
        print "test many mac in blacklist with WEP64bit,test pass!"


    #WEP 64bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:371_3)
    def test_106_wep64_1_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:371_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in blacklist with WEP64bit,test fail!"
        print "test one mac in blacklist with WEP64bit,test pass!"

    #WEP 64bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:371_4)
    def test_107_wep64_many_blacklist(self):
        u"""WEP 64bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:371_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in blacklist with WEP64bit,test fail!"
        print "test many mac in blacklist with WEP64bit,test pass!"

    #WEP 64bit 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:372_1)
    def test_108_wep64_1_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:372_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in whitelist with WEP64bit,test fail!"
        print "test one mac in whitelist with WEP64bit,test pass!"

    #WEP 64bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:372_2)
    def test_109_wep64_many_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:372_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in whitelist with WEP64bit,test fail!"
        print "test many mac in whitelist with WEP64bit,test pass!"

    #WEP 64bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:372_3)
    def test_110_wep64_1_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:372_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with WEP64bit,test fail!"
        print "test one mac in whitelist with WEP64bit,test pass!"

    #WEP 64bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:372_4)
    def test_111_wep64_many_whitelist(self):
        u"""WEP 64bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:372_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['add_ssid'],data_wireless['wep64'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in whitelist with WEP64bit,test fail!"
        print "test many mac in whitelist with WEP64bit,test pass!"


    #WEP 128bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:373_1)
    def test_112_wep128_1_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:373_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为wep128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WEP128bit,test fail!"
        print "test one mac in blacklist with WEP128bit,test pass!"

    #WEP 128bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:373_2)
    def test_113_wep128_many_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:373_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with WEP128bit,test fail!"
        print "test many mac in blacklist with WEP128bit,test pass!"


    #WEP 128bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:373_3)
    def test_114_wep128_1_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:373_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in blacklist with WEP128bit,test fail!"
        print "test one mac in blacklist with WEP128bit,test pass!"

    #WEP 128bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:373_4)
    def test_115_wep128_many_blacklist(self):
        u"""WEP 128bit 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:373_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in blacklist with WEP128bit,test fail!"
        print "test many mac in blacklist with WEP128bit,test pass!"

    #WEP 128bit 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:374_1)
    def test_116_wep128_1_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:374_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in whitelist with WEP128bit,test fail!"
        print "test one mac in whitelist with WEP128bit,test pass!"

    #WEP 128bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:374_2)
    def test_117_wep128_many_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:374_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in whitelist with WEP128bit,test fail!"
        print "test many mac in whitelist with WEP128bit,test pass!"

    #WEP 128bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:374_3)
    def test_118_wep128_1_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:374_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with WEP128bit,test fail!"
        print "test one mac in whitelist with WEP128bit,test pass!"

    #WEP 128bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:374_4)
    def test_119_wep128_many_whitelist(self):
        u"""WEP 128bit 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:374_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WEP_AP_backup(data_wireless['add_ssid'],data_wireless['wep128'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in whitelist with WEP128bit,test fail!"
        print "test many mac in whitelist with WEP128bit,test pass!"


    #WPA 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:375_1)
    def test_120_WPA_1_blacklist(self):
        u"""WPA 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:375_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa/wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WPA,test fail!"
        print "test one mac in blacklist with WPA,test pass!"

    #WPA 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:375_2)
    def test_121_WPA_many_blacklist(self):
        u"""WPA 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:375_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with WPA,test fail!"
        print "test many mac in blacklist with WPA,test pass!"


    #WPA 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:375_3)
    def test_122_WPA_1_blacklist(self):
        u"""WPA 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:375_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in blacklist with WPA,test fail!"
        print "test one mac in blacklist with WPA,test pass!"

    #WPA 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:375_4)
    def test_123_WPA_many_blacklist(self):
        u"""WPA 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:375_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in blacklist with WPA,test fail!"
        print "test many mac in blacklist with WPA,test pass!"

    #WPA 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:376_1)
    def test_124_WPA_1_whitelist(self):
        u"""WPA 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:376_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in whitelist with WPA,test fail!"
        print "test one mac in whitelist with WPA,test pass!"

    #WPA 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:376_2)
    def test_125_WPA_many_whitelist(self):
        u"""WPA 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:376_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in whitelist with WPA,test fail!"
        print "test many mac in whitelist with WPA,test pass!"

    #WPA 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:376_3)
    def test_126_WPA_1_whitelist(self):
        u"""WPA 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:376_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with WPA,test fail!"
        print "test one mac in whitelist with WPA,test pass!"

    #WPA 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:376_4)
    def test_127_WPA_many_whitelist(self):
        u"""WPA 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:376_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in whitelist with WPA,test fail!"
        print "test many mac in whitelist with WPA,test pass!"



    #WPA2 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:377_1)
    def test_128_WPA2_1_blacklist(self):
        u"""WPA2 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:377_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为wpa2-TKIP/AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with WPA2,test fail!"
        print "test one mac in blacklist with WPA2,test pass!"

    #WPA2 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:377_2)
    def test_129_WPA2_many_blacklist(self):
        u"""WPA2 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:377_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with WPA2,test fail!"
        print "test many mac in blacklist with WPA2,test pass!"


    #WPA2 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:377_3)
    def test_130_WPA2_1_blacklist(self):
        u"""WPA2 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:377_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in blacklist with WPA,test fail!"
        print "test one mac in blacklist with WPA,test pass!"

    #WPA2 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:377_4)
    def test_131_WPA2_many_blacklist(self):
        u"""WPA2 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:377_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in blacklist with WPA,test fail!"
        print "test many mac in blacklist with WPA,test pass!"

    #WPA2 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:378_1)
    def test_132_WPA2_1_whitelist(self):
        u"""WPA2 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:378_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in whitelist with WPA2,test fail!"
        print "test one mac in whitelist with WPA2,test pass!"

    #WPA2 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:378_2)
    def test_133_WPA2_many_whitelist(self):
        u"""WPA2 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:378_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in whitelist with WPA2,test fail!"
        print "test many mac in whitelist with WPA2,test pass!"

    #WPA2 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:378_3)
    def test_134_WPA2_1_whitelist(self):
        u"""WPA2 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:378_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with WPA2,test fail!"
        print "test one mac in whitelist with WPA2,test pass!"

    #WPA2 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:378_4)
    def test_135_WPA2_many_whitelist(self):
        u"""WPA2 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:378_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                        data_wireless['short_wpa'],data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in whitelist with WPA2,test fail!"
        print "test many mac in whitelist with WPA2,test pass!"


    #open 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:379_1)
    def test_136_open_1_blacklist(self):
        u"""open 和 blacklist 混合验证1（单客户端）--无线客户端在blacklist里面(testlink_ID:379_1)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        ##设置默认网络组无线为不加密
        tmp.wifi_None_encryption()
        #设置默认网络组的无线过滤的黑名单
        tmp.wifi_blacklist_backup()
        #无线连接这个的AP
        result = tmp.connect_NONE_AP_backup(data_wireless['add_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in blacklist with open,test fail!"
        print "test one mac in blacklist with open,test pass!"

    #open 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:379_2)
    def test_137_open_many_blacklist(self):
        u"""open 和 blacklist 混合验证2（多客户端）--无线客户端在blacklist里面(testlink_ID:379_2)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP_backup(data_wireless['add_ssid'],\
                        data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert 'Not connected' in result,"test many mac in blacklist with open,test fail!"
        print "test many mac in blacklist with open,test pass!"


    #open 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:379_3)
    def test_138_open_1_blacklist(self):
        u"""open 和 blacklist 混合验证3（单客户端）--无线客户端不在blacklist里面(testlink_ID:379_3)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP(data_wireless['add_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in blacklist with open,test fail!"
        print "test one mac in blacklist with open,test pass!"

    #open 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:379_4)
    def test_139_open_many_blacklist(self):
        u"""open 和 blacklist 混合验证4（多客户端）--无线客户端不在blacklist里面(testlink_ID:379_4)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP(data_wireless['add_ssid'],\
                        data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in blacklist with open,test fail!"
        print "test many mac in blacklist with open,test pass!"

    #open 和 whitelist 混合验证1（单客户端）--无线客户端在whitelist里面(testlink_ID:379_5)
    def test_140_open_1_whitelist(self):
        u"""open 和 whitelist 混合验证1（单客户端）--无线客户端在white里面(testlink_ID:379_5)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp1.edit_accesslist_onemac(mac)
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组的无线过滤的白名单
        tmp.wifi_whitelist_backup()
        #无线连接这个的AP
        result = tmp.connect_NONE_AP(data_wireless['add_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert data_wireless['add_ssid'] in result,"test one mac in whitelist with open,test fail!"
        print "test one mac in whitelist with open,test pass!"

    #open 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:379_6)
    def test_141_open_many_whitelist(self):
        u"""open 和 whitelist 混合验证2（多客户端）--无线客户端在whitelist里面(testlink_ID:379_6)"""
        tmp = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP(data_wireless['add_ssid'],\
                        data_basic['wlan_pc'])
        print result
        #编辑第一个mac地址的访问列表--删除所有的mac，只保留第一个mac地址
        tmp.del_accesslist_manymac()
        assert data_wireless['add_ssid'] in result,"test many mac in whitelist with open,test fail!"
        print "test many mac in whitelist with open,test pass!"

    #open 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:379_7)
    def test_142_open_1_whitelist(self):
        u"""open 和 whitelist 混合验证3（单客户端）--无线客户端不在whitelist里面(testlink_ID:379_7)"""
        tmp = ClientAccessBusiness(self.driver)
        #取随机mac地址
        random_mac = tmp.randomMAC()
        #编辑第一个只有一个mac地址的访问列表---只修改mac，不添加
        tmp.edit_accesslist_onemac(random_mac)
        #无线连接这个的AP
        result = tmp.connect_NONE_AP_backup(data_wireless['add_ssid'],\
                        data_basic['wlan_pc'])
        print result
        assert 'Not connected' in result,"test one mac in whitelist with open,test fail!"
        print "test one mac in whitelist with open,test pass!"

    #open 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:379_8)
    def test_143_open_many_whitelist(self):
        u"""open 和 whitelist 混合验证4（多客户端）--无线客户端不在whitelist里面(testlink_ID:379_8)"""
        tmp2 = ClientAccessBusiness(self.driver)
        #编辑第一个mac地址的访问列表---添加n个mac地址，第一个mac地址不修改
        tmp2.edit_accesslist_manymac(9)
        #无线连接这个的AP
        result = tmp2.connect_NONE_AP_backup(data_wireless['add_ssid'],\
                        data_basic['wlan_pc'])
        print result

        #复位AP
        tmp1 = APSBusiness(self.driver)
        tmp1.web_factory_reset(data_basic['DUT_ip'],data_basic['sshUser'],\
                               data_basic['super_defalut_pwd'])
        #新建一个额外的ssid
        tmp = AddSSIDBusiness(self.driver)
        tmp.new_ssid(data_wireless['add_ssid'],data_wireless['short_wpa'])
        ##设置额外的ssid无线为不加密
        tmp.wifi_None_encryption()
        assert 'Not connected' in result,"test many mac in whitelist with open,test fail!"
        print "test many mac in whitelist with open,test pass!"




    #enable client isolation 配置验证(testlink_ID:380_1)
    def test_144_enable_client_isolation2(self):
        u"""enable client isolation 配置验证(testlink_ID:380_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置第1个额外ssid的客户端隔离
        tmp.wifi_n_isolation(1,"radio")
        #获取第一个额外ssid的客户端隔离状态
        result = tmp.get_first_isolation()
        assert result == "enableicon","enable client isolation,test fail!"
        print "enable client isolation,test pass!"

    #disable client isolation 配置验证(testlink_ID:380_2)
    def test_145_disable_client_isolation(self):
        u"""disable client isolation 配置验证(testlink_ID:380_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置第1个额外ssid的客户端不隔离
        tmp.wifi_n_isolation(1,"radio")
        #获取第一个额外ssid的客户端隔离状态
        result = tmp.get_first_isolation()
        assert result == "disableicon","disable client isolation,test fail!"
        print "disable client isolation,test pass!"

    #Gateway MAC Address为空的配置验证(testlink_ID:381)
    def test_146_check_wifi_n_isolation_gateway_mac_blank(self):
        u"""Gateway MAC Address为空的配置验证(testlink_ID:381)"""
        tmp = AddSSIDBusiness(self.driver)
        #配置第n个额外ssid的客户端隔离的网关mac为空的测试
        result1,result2 = tmp.check_wifi_n_isolation_gateway_mac_err(1," ")
        assert (result1 and result2) == True,"check gateway mac is blank,test fail!"
        print "check gateway mac is blank,test pass!"

    #单环境下client isolation功能验证radio--这里只验证后台规则生效(testlink_ID:382_1)
    def test_147_check_isolation_radio(self):
        u"""单环境下client isolation功能验证radio--这里只验证后台规则生效(testlink_ID:382_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #配置第1个额外ssid的客户端隔离的无线模式
        tmp. wifi_n_isolation(1,"radio")
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result1) and ("radio" in result2),\
            "check isolation radio,test fail!"
        print "check isolation radio,test pass!"

    #单环境下client isolation功能验证internet(testlink_ID:382_2)
    def test_148_check_isolation_internet(self):
        u"""单环境下client isolation功能验证internet(testlink_ID:382_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #配置第1个额外ssid的客户端隔离的互联网模式
        tmp. wifi_n_isolation_backup(1,"internet")
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        result3,result4 = tmp.check_isolation(data_wireless['add_ssid'])
        assert ("1" in result1) and ("internet" in result2) and \
               (result3 != 0) and (result4 == 0), \
            "check isolation internet,test fail!"
        print "check isolation internet,test pass!"

    #单环境下client isolation功能验证gatewaymac(testlink_ID:382_3)
    def test_149_check_isolation_gatewaymac(self):
        u"""单环境下client isolation功能验证gatewaymac(testlink_ID:382_3)"""
        tmp = AddSSIDBusiness(self.driver)
        #配置第1个额外ssid的客户端隔离的网关mac模式
        #获取7000的mac地址
        route_mac = tmp.get_router_mac(data_basic['7000_ip'],data_basic['sshUser'],data_login['all'])
        print route_mac
        tmp. wifi_n_isolation_gateway_mac_backup(1,route_mac)
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.gateway_mac")
        result4,result5 = tmp.check_isolation(data_wireless['add_ssid'])
        self.driver.refresh()
        self.driver.implicitly_wait(10)
        #登录AP
        Lg = LoginBusiness(self.driver)
        Lg.login(data_basic['superUser'],data_login['all'])
        #配置第1个额外ssid的客户端隔离的无线模式
        tmp. wifi_n_isolation_backup(1,"radio")
        assert ("1" in result1) and ("gateway_mac" in result2) and (route_mac in result3) and \
            (result4 == 0) and (result5 == 0), \
            "check isolation gateway mac,test fail!"
        print "check isolation gateway mac,test pass!"

    #重启查看client isolation是否依然生效(testlink_ID:383)
    def test_150_check_reboot_isolation(self):
        u"""重启查看client isolation是否依然生效(testlink_ID:383)"""
        tmp = UpgradeBusiness(self.driver)
        tmp.web_reboot(data_basic['DUT_ip'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result1) and ("radio" in result2),\
            "check isolation radio after rebooting,test fail!"
        print "check isolation radio after rebooting,test pass!"

    #多功能混合验证 client isolation + encrypted  (open mode)(testlink_ID:384)
    def test_151_check_open_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (open mode)(testlink_ID:384)"""
        tmp = AddSSIDBusiness(self.driver)
        #无线连接这个的AP
        result1 = tmp.connect_NONE_AP(data_wireless['add_ssid'],\
                        data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['add_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check open encryption and isolation radio,test fail!"
        print "check open encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WEP 64bit  mode)(testlink_ID:385)
    def test_152_check_wep64_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WEP 64bit  mode)(testlink_ID:385)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置wep64加密
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #无线连接这个的AP
        result1 = tmp.connect_WEP_AP(data_wireless['add_ssid'],\
                    data_wireless['wep64'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['add_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wep64bit encryption and isolation radio,test fail!"
        print "check wep64bit encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WEP 128bit  mode)(testlink_ID:386)
    def test_153_check_wep128_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WEP 128bit  mode)(testlink_ID:386)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置wep128加密
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #无线连接这个的AP
        result1 = tmp.connect_WEP_AP(data_wireless['add_ssid'],\
                    data_wireless['wep128'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['add_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wep128bit encryption and isolation radio,test fail!"
        print "check wep128bit encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES mode)(testlink_ID:387)
    def test_154_check_wpa2_mix_AES_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES mode)(testlink_ID:387)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置额外SSID无线为wpa/wpa2-AES
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['add_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2 mix-AES encryption and isolation radio,test fail!"
        print "check wpa2 mix-AES encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES/TKIP mode)(testlink_ID:388)
    def test_155_check_wpa2_mix_AESTKIP_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA/WPA2  AES/TKIP mode)(testlink_ID:388)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置额外SSID无线为wpa/wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['add_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2 mix-AES/TKIP encryption and isolation radio,test fail!"
        print "check wpa2 mix-AES/TKIP encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA2  AES mode)(testlink_ID:389)
    def test_156_check_wpa2_AES_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA2  AES mode)(testlink_ID:389)"""
        tmp = AddSSIDBusiness(self.driver)
        #首先取消客户端隔离的模式
        tmp.cancel_wifi_n_isolation(1)
        ##设置额外SSID无线为wpa2-AES
        tmp.wifi_wpa_encryption(1,1,data_wireless['short_wpa'])
        #再选择客户端隔离的模式
        tmp.cancel_wifi_n_isolation(1)
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['add_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2-AES encryption and isolation radio,test fail!"
        print "check wpa2-AES encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + encrypted  (WPA2  AES/TKIP mode)(testlink_ID:390)
    def test_157_check_wpa2_AESTKIP_isolation(self):
        u"""多功能混合验证 client isolation + encrypted  (WPA2  AES/TKIP mode)(testlink_ID:390)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置额外SSID无线为wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(0,1,data_wireless['short_wpa'])
        #无线连接这个的AP
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['add_ssid'] in result1) and \
               ("1" in result2) and ("radio" in result3),\
                "check wpa2-AES/TKIP encryption and isolation radio,test fail!"
        print "check wpa2-AES/TKIP encryption and isolation radio,test pass!"

    #多功能混合验证 client isolation + hide SSID(testlink_ID:391)
    def test_158_check_hideSSID_isolation(self):
        u"""多功能混合验证 client isolation + hide SSID(testlink_ID:391)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置第一个额外ssid是否隐藏
        tmp.set_hide_ssid()
        result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        #取消第一个额外ssid是否隐藏
        tmp.set_hide_ssid()
        assert (result1 == False) and ("1" in result2) \
                and ("radio" in result3) and (data_wireless['add_ssid'] in result4),\
                "check hide SSID and isolation radio,test fail!"
        print "check hide SSID and isolation radio,test pass!"

    #多功能混合验证 client isolation + mac filter(testlink_ID:392)
    def test_159_check_macfilter_isolation(self):
        u"""多功能混合验证 client isolation + mac filter(testlink_ID:392)"""
        tmp1 = ClientAccessBusiness(self.driver)
        #取本机无线mac地址
        mac = tmp1.get_wlan_mac(data_basic["wlan_pc"])
        #添加一个只有一个mac地址的访问列表
        tmp1.add_accesslist_onemac(mac)

        tmp = AddSSIDBusiness(self.driver)
        tmp.wifi_whitelist()
        result1 = tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert (data_wireless['add_ssid'] in result1) and ("1" in result2) \
                and ("radio" in result3),\
                "check mac filter and isolation radio,test fail!"
        print "check mac filter and isolation radio,test pass!"

    #hide SSID、WPA2、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:403)
    def test_160_WPA2_all_mixed_whitelist(self):
        u"""hide SSID、WPA2、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:403)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置第一个额外ssid是否隐藏
        tmp.set_hide_ssid()
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['add_ssid'] in result4),\
                "check WPA2 in all mixed whitelist,test fail!"
        print "check WPA2 in all mixed whitelist,test pass!"

    #hide SSID、OPEN、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:399)
    def test_161_open_all_mixed_whitelist(self):
        u"""hide SSID、OPEN、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:399)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为不加密
        tmp.wifi_None_encryption()
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_NONE_hiddenssid_AP(data_wireless['add_ssid'],\
                    data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['add_ssid'] in result4),\
                "check OPEN in all mixed whitelist,test fail!"
        print "check OPEN in all mixed whitelist,test pass!"

    #hide SSID、WEP64、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:400)
    def test_162_WEP64_all_mixed_whitelist(self):
        u"""hide SSID、WEP64、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:400)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置额外SSID无线为WEP64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP(data_wireless['add_ssid'],\
                    data_wireless['wep64'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['add_ssid'] in result4),\
                "check WEP64 in all mixed whitelist,test fail!"
        print "check WEP64 in all mixed whitelist,test pass!"

    #hide SSID、WEP128、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:401)
    def test_163_WEP128_all_mixed_whitelist(self):
        u"""hide SSID、WEP128、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:401)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置额外SSID无线为WEP128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP(data_wireless['add_ssid'],\
                    data_wireless['wep128'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['add_ssid'] in result4),\
                "check WEP128 in all mixed whitelist,test fail!"
        print "check WEP128 in all mixed whitelist,test pass!"

    #hide SSID、WPA、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:402)
    def test_164_WPA_all_mixed_whitelist(self):
        u"""hide SSID、WPA、mac filter whitelist、client isolation，验证是否有功能出现异常(testlink_ID:402)"""
        tmp = AddSSIDBusiness(self.driver)
        ##设置额外SSID无线为wpa/wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(1,0,data_wireless['short_wpa'])
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and (data_wireless['add_ssid'] in result4),\
                "check WPA in all mixed whitelist,test fail!"
        print "check WPA in all mixed whitelist,test pass!"

    #hide SSID、WPA、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:397)
    def test_165_WPA_all_mixed_blacklist(self):
        u"""hide SSID、WPA、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:397)"""
        tmp = AddSSIDBusiness(self.driver)
        tmp.wifi_blacklist()
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check WPA in all mixed blacklist,test fail!"
        print "check WPA in all mixed blacklist,test pass!"

    #hide SSID、open、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:394)
    def test_166_open_all_mixed_blacklist(self):
        u"""hide SSID、open、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:394)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置默认网络组无线为不加密
        tmp.wifi_None_encryption()
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_NONE_hiddenssid_AP_backup(data_wireless['add_ssid'],\
                    data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check open in all mixed blacklist,test fail!"
        print "check open in all mixed blacklist,test pass!"

    #hide SSID、wep64、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:395)
    def test_167_wep64_all_mixed_blacklist(self):
        u"""hide SSID、wep64、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:395)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置额外SSID无线为WEP64
        tmp.wifi_wep_encryption(1,data_wireless['wep64'])
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['wep64'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check wep64 in all mixed blacklist,test fail!"
        print "check wep64 in all mixed blacklist,test pass!"

    #hide SSID、wep128、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:396)
    def test_168_wep128_all_mixed_blacklist(self):
        u"""hide SSID、wep128、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:396)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置额外SSID无线为WEP128
        tmp.wifi_wep_encryption(1,data_wireless['wep128'])
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WEP_hiddenssid_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['wep128'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check wep128 in all mixed blacklist,test fail!"
        print "check wep128 in all mixed blacklist,test pass!"

    #hide SSID、wpa2、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:398)
    def test_169_wpa2_all_mixed_blacklist(self):
        u"""hide SSID、wpa2、mac filter blacklist、client isolation，验证是否有功能出现异常(testlink_ID:398)"""
        tmp = AddSSIDBusiness(self.driver)
        #设置额外SSID无线为wpa/wpa2-AES/TKIP
        tmp.wifi_wpa_encryption(2,0,data_wireless['short_wpa'])
        #result1 = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        result4 = tmp.connect_WPA_hiddenssid_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        #禁用第1个的无线过滤
        tmp.disable_macfilter(1)
        #取消第一个额外ssid是否隐藏
        tmp.set_hide_ssid()
        #取消第n个额外ssid的客户端隔离的模式
        tmp.cancel_wifi_n_isolation(1)
        assert ("1" in result2) \
                and ("radio" in result3) and ("Not connected" in result4),\
                "check wpa2 in all mixed blacklist,test fail!"
        print "check wpa2 in all mixed blacklist,test pass!"


    #enableRSSI 配置验证并检查(testlink_ID:414_1)
    def test_170_check_enable_rssi(self):
        u"""enableRSSI 配置验证并检查(testlink_ID:414_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #enableRSSI 配置验证并检查
        result1,result2 = tmp.check_enable_rssi()
        assert result1==result2=="-94","check enable RSSI,test fail!"
        print "check enable RSSI,test pass!"

    #disableRSSI 配置验证并检查(testlink_ID:414_2)
    def test_171_check_disable_rssi(self):
        u"""disableRSSI 配置验证并检查(testlink_ID:414_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #disableRSSI 配置验证并检查
        result1,result2 = tmp.check_disable_rssi()
        assert (result1=="-94") and (result2 == "disableicon"),"check disable RSSI,test fail!"
        print "check disable RSSI,test pass!"

    #enable rssi,Minimum RSSI (dBm)为空格的配置验证(testlink_ID:415_1)
    def test_172_check_min_rssi_blank(self):
        u"""enable rssi,Minimum RSSI (dBm)为空格的配置验证(testlink_ID:415_1)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(" ")
        assert result1 and result2,"enable rssi when min rssi is blank,test fail!"
        print "enable rssi when min rssi is blank,test pass!"

    #disable rssi,Minimum RSSI (dBm)为空的配置验证(testlink_ID:415_2)
    def test_173_check_min_rssi_empty(self):
        u"""disable rssi,Minimum RSSI (dBm)为空的配置验证(testlink_ID:415_2)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2 = tmp.check_disable_min_rssi_error("")
        assert (result1==False) and (result2==False),"disable rssi when min rssi is empty,test fail!"
        print "disable rssi when min rssi is empty,test pass!"

    #在Minimum RSSI (dBm)处输入大于-1的整数(testlink_ID:416_1)
    def test_174_check_min_rssi_more_than_negative1(self):
        u"""在Minimum RSSI (dBm)处输入大于-1的整数(testlink_ID:416_1)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error("0")
        assert result1 and result2,"when min rssi more than nagative 1,test fail!"
        print "when min rssi more than nagative 1,test pass!"

    #在Minimum RSSI (dBm)处输入小于-94的整数(testlink_ID:416_2)
    def test_175_check_min_rssi_less_than_negative94(self):
        u"""在Minimum RSSI (dBm)处输入小于-94的整数(testlink_ID:416_2)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error("-95")
        assert result1 and result2,"when min rssi less than nagative 95,test fail!"
        print "when min rssi less than nagative 95,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:416_3)
    def test_176_check_min_rssi_chinese(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如中文(testlink_ID:416_3)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(data_wireless['CN_ssid'])
        assert result1 and result2,"when min rssi is chinese,test fail!"
        print "when min rssi is chinese,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:416_4)
    def test_177_check_min_rssi_ascii(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如ASCII码(testlink_ID:416_4)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(data_wireless['ascii_ssid'])
        assert result1 and result2,"when min rssi is ascii,test fail!"
        print "when min rssi is ascii,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:416_5)
    def test_178_check_min_rssi_decimals(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如小数(testlink_ID:416_5)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error("-50.5")
        assert result1 and result2,"when min rssi is decimals,test fail!"
        print "when min rssi is decimals,test pass!"

    #在Minimum RSSI (dBm)处输入非法字符如中文、ASCII码、小数和特殊字符等(testlink_ID:416_6)
    def test_179_check_min_rssi_special(self):
        u"""在Minimum RSSI (dBm)处输入非法字符如特殊字符(testlink_ID:416_6)"""
        tmp = AddSSIDBusiness(self.driver)
        result1,result2 = tmp.check_enable_min_rssi_error(data_wireless['special_ssid'])
        assert result1 and result2,"when min rssi is special,test fail!"
        print "when min rssi is special,test pass!"

    #在Minimum RSSI (dBm)处输入-1(testlink_ID:417_1)
    def test_180_check_min_rssi_negative1(self):
        u"""在Minimum RSSI (dBm)处输入-1(testlink_ID:417_1)"""
        tmp = AddSSIDBusiness(self.driver)
        #enableRSSI
        tmp.check_enable_rssi()
        #设置最小RSSI值，并检查是否正确
        result = tmp.check_min_rssi("-1")
        assert result == "-1","when min rssi is -1,test fail!"
        print "when min rssi is -1,test pass!"

    #RSSI功能验证-范围验证-1(testlink_ID:417_2)
    def test_181_check_min_rssi_negative1_validity(self):
        u"""RSSI功能验证-范围验证-1(testlink_ID:417_2)"""
        tmp = AddSSIDBusiness(self.driver)
        tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #在2分钟内每隔2秒检查无线网卡是否一直保持和ap连接
        result = tmp.check_wifi_client_connected_allthetime(data_basic['wlan_pc'])
        assert "Not connected.\n" in result,"check min rssi is -1 validity,test fail!"
        print "check min rssi is -1 validity,test pass!"

    #在Minimum RSSI (dBm)处输入-94(testlink_ID:417_3)
    def test_182_check_min_rssi_negative94(self):
        u"""在Minimum RSSI (dBm)处输入-1(testlink_ID:417_3)"""
        tmp = AddSSIDBusiness(self.driver)
        result = tmp.check_min_rssi("-94")
        assert result == "-94","when min rssi is -94,test fail!"
        print "when min rssi is -94,test pass!"

    #RSSI功能验证-范围验证-94(testlink_ID:417_4)
    def test_183_check_min_rssi_negative94_validity(self):
        u"""RSSI功能验证-范围验证-94(testlink_ID:417_4)"""
        tmp = AddSSIDBusiness(self.driver)
        tmp.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #在2分钟内每隔2秒检查无线网卡是否一直保持和ap连接
        result = tmp.check_wifi_client_connected_allthetime(data_basic['wlan_pc'])
        assert "Not connected.\n" not in result,"check min rssi is -94 validity,test fail!"
        print "check min rssi is -94 validity,test pass!"

    #在Minimum RSSI (dBm)处输入-10(testlink_ID:418_1)
    def test_184_check_min_rssi_negative10(self):
        u"""在Minimum RSSI (dBm)处输入-10(testlink_ID:418_1)"""
        tmp = AddSSIDBusiness(self.driver)
        result = tmp.check_min_rssi("-10")
        assert result == "-10","when min rssi is -10,test fail!"
        print "when min rssi is -10,test pass!"

    #RSSI功能验证-范围验证-10(testlink_ID:418_2)
    def test_185_check_min_rssi_negative10_validity(self):
        u"""RSSI功能验证-范围验证-10(testlink_ID:418_2)"""
        tmp = AddSSIDBusiness(self.driver)
        tmp.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #在2分钟内每隔5秒检查无线网卡是否一直保持和ap连接
        result = tmp.check_wifi_client_connected_allthetime(data_basic['wlan_pc'])
        #disableRSSI 配置验证并检查
        tmp.check_disable_rssi()
        assert "Not connected.\n" in result,"check min rssi is -10 validity,test fail!"
        print "check min rssi is -10 validity,test pass!"

    #Network Group Membership的显示验证1(testlink_ID:421_1)
    def test_186_check_group_membership_display(self):
        u"""Network Group Membership的显示验证1(testlink_ID:421_1)"""
        tmp = NGBusiness(self.driver)
        #点击网络组，添加两个新的网络组
        NG_name = data_ng["NG2_name"]
        NG_ssid = data_ng["NG2_ssid"]
        tmp.new_network_group(NG_name+"-2",NG_ssid+"-2",data_wireless["short_wpa"])
        tmp.new_network_group(NG_name+"-3",NG_ssid+"-3",data_wireless["short_wpa"])
        tmp1 = AddSSIDBusiness(self.driver)
        result1,result2 = tmp1.check_2_3_network_group_membership()
        assert (result1 == (NG_name+"-2")) and (result2 == (NG_name+"-3")),\
            "check group membership display,test fail!"
        print "check group membership display,test pass!"

    #Network Group Membership的显示验证2(testlink_ID:421_2)
    def test_187_check_group_membership_display(self):
        u"""Network Group Membership的显示验证2(testlink_ID:421_2)"""
        tmp = NGBusiness(self.driver)
        #删除所有网络组
        tmp.del_all_NG()
        tmp1 = AddSSIDBusiness(self.driver)
        result1,result2 = tmp1.check_2_3_network_group_membership()
        assert (result1 == False) and (result2 == False),\
            "check group membership display,test fail!"
        print "check group membership display,test pass!"

    #Network Group Membership的显示验证3--默认网络组的组名为group0(testlink_ID:421_3)
    def test_188_check_default_group_membership_display(self):
        u"""Network Group Membership的显示验证3--默认网络组的组名为group0(testlink_ID:421_3)"""
        tmp = AddSSIDBusiness(self.driver)
        result = tmp.check_1_network_group_membership()
        #设置额外SSID无线为不加密
        tmp.wifi_None_encryption()
        assert result == "group0","check group membership display,test fail!"
        print "check group membership display,test pass!"

    #Network Group Membership的功能验证1(testlink_ID:422_1)
    def test_189_check_group_membership_function1(self):
        u"""Network Group Membership的功能验证1(testlink_ID:422_1)"""
        tmp = NGBusiness(self.driver)
        #点击网络组，添加一个新的网络组
        NG_name = data_ng["NG2_name"]
        NG_ssid = data_ng["NG2_ssid"]
        tmp.new_network_group(NG_name+"-2",NG_ssid+"-2",data_wireless["short_wpa"])
        tmp1 = AddSSIDBusiness(self.driver)
        #设置第一个额外ssid的网路组到第2个网络组
        tmp1.set_zone(1)
        result = tmp1.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        assert result == False,"check group membership function1,test fail!"
        print "check group membership function1,test pass!"

    #Network Group Membership的功能验证2(testlink_ID:422_2)
    def test_190_check_group_membership_function2(self):
        u"""Network Group Membership的功能验证2(testlink_ID:422_2)"""
        tmp = APSBusiness(self.driver)
        #将master ap加入第2个网络组2
        tmp.add_master_to_n_NG(2)
        result = tmp.connect_NONE_AP(data_wireless['add_ssid'],\
                    data_basic['wlan_pc'])
        assert data_wireless['add_ssid'] in result,"check group membership function2,test fail!"
        print "check group membership function2,test pass!"

    #Network Group Membership的功能验证3(testlink_ID:422_3)
    def test_191_check_group_membership_function3(self):
        u"""Network Group Membership的功能验证3(testlink_ID:422_3)"""
        tmp = NGBusiness(self.driver)
        #删除所有网络组
        tmp.del_all_NG()
        tmp1 = AddSSIDBusiness(self.driver)
        #点击网络组菜单，然后在点击额外ssid菜单
        tmp1.NG_SSID_menu()
        #检测页面上是否有第一个额外ssid
        result1 = tmp1.check_first_exist()
        result2 = tmp1.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        print "result1 = %s"%result1
        print "result2 = %s"%result2
        tmp = APSBusiness(self.driver)
        #将master ap加入第1个网络组group0
        tmp.add_master_to_n_NG(1)
        assert (result1 == False) and (result2 == False),"check group membership function3,test fail!"
        print "check group membership function3,test pass!"

    #isolation与network group的冲突验证--这里只验证后台规则生效(testlink_ID:423)
    def test_192_isolation_conflict(self):
        u"""isolation与network group的冲突验证--这里只验证后台规则生效(testlink_ID:423)"""
        tmp = AddSSIDBusiness(self.driver)
        #新建一个额外的ssid
        tmp.new_ssid(data_wireless['add_ssid'],data_wireless['short_wpa'])
        #配置第1个额外ssid的客户端隔离的模式
        tmp.wifi_n_isolation(1,"radio")
        ssh = SSH(data_basic['DUT_ip'],data_login['all'])
        result1 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation")
        result2 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.ssid0.isolation_mode")
        result3 = ssh.ssh_cmd(data_basic['sshUser'],"uci show grandstream.zone0.isolation")
        #取消第1个额外ssid的客户端隔离的模式
        tmp.cancel_wifi_n_isolation(1)
        assert ("1" in result1) and ("radio" in result2) and ("1" not in result3),\
            "check isolation conflict,test fail!"
        print "check isolation conflict,test pass!"

    #黑白名单和network group的冲突验证1(testlink_ID:424_1)
    def test_193_blacklist_whitelist_confict1(self):
        u"""黑白名单和network group的冲突验证1(testlink_ID:424_1)"""
        tmp = NGBusiness(self.driver)
        #修改默认网络组的ssid和密码
        tmp.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        tmp.wifi_whitelist()
        tmp1 = AddSSIDBusiness(self.driver)
        #设置第一个额外ssid的无线过滤的黑名单
        tmp1.wifi_blacklist()
        result1 = tmp1.connect_WPA_AP(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp1.connect_WPA_AP_backup(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        assert (data_wireless['all_ssid'] in result1) and \
               ("Not connected" in result2),"check blacklist and whitelist conflict,test fail!"
        print "check blacklist and whitelist conflict,test pass!"

    #黑白名单和network group的冲突验证2(testlink_ID:424_2)
    def test_194_blacklist_whitelist_confict2(self):
        u"""黑白名单和network group的冲突验证2(testlink_ID:424_2)"""
        tmp = NGBusiness(self.driver)
        tmp.wifi_blacklist()
        tmp1 = AddSSIDBusiness(self.driver)
        #设置第一个额外ssid的无线过滤的白名单
        tmp1.wifi_whitelist()
        result1 = tmp1.connect_WPA_AP_backup(data_wireless['all_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        result2 = tmp1.connect_WPA_AP(data_wireless['add_ssid'],\
                    data_wireless['short_wpa'],data_basic['wlan_pc'])
        #禁用group0和第一个额外ssid的mac地址过滤
        tmp.disable_macfilter(1)
        tmp1.disable_macfilter(1)
        assert ("Not connected" in result1) and \
               (data_wireless['add_ssid'] in result2),"check blacklist and whitelist conflict,test fail!"
        print "check blacklist and whitelist conflict,test pass!"

    #additional SSID的创建数量限制(testlink_ID:425)
    def test_195_max_addSSID(self):
        u"""additional SSID的创建数量限制(testlink_ID:425)"""
        tmp = AddSSIDBusiness(self.driver)
        #增加到最大的额外ssid
        result1,result2,result3 = tmp.add_NG_max(data_basic['DUT_ip'],data_basic['sshUser'],\
                       data_login['all'],data_wireless['add_ssid'],\
                       data_wireless['short_wpa'])
        assert result1 and ("='ssid14'" in result2) and ("ath31" in result3),\
            "check max additional ssid number,test fail!"
        print "check max additional ssid number,test pass!"

    #additional SSID属于单个group的创建数量限制(testlink_ID:426)
    def test_196_check_max_group_number(self):
        u"""additional SSID属于单个group的创建数量限制(testlink_ID:426)"""
        tmp = AddSSIDBusiness(self.driver)
        #获取所有group0的网络组，并判断个数
        result = tmp.check_group_number()
        assert result == 15,"The max number of only group creating additional ssid is %s,test fail!"%result
        print "The max number of only group creating additional ssid is %s,test pass!"%result

    #当additional ssid和network group ssid两者总数超过16个时的SSID广播情况(testlink_ID:427_1)
    def test_197_check_sum_addssid_NG(self):
        u"""当additional ssid和network group ssid两者总数超过16个时的SSID广播情况(testlink_ID:427_1)"""
        tmp = NGBusiness(self.driver)
        #点击网络组，添加一个新的网络组时判断是否提示不能添加
        result = tmp.check_tip_new_network_group("%s-2"%data_ng["NG2_name"],\
                    "%s-2"%data_ng["NG2_ssid"],data_wireless["short_wpa"])
        print "result = %s"%result
        assert result,"The sum number of addSSID and Network group isn't 16,test fail!"
        print "The sum number of addSSID and Network group is 16,test pass!"

    #删除所有的additional SSID(testlink_ID:427_2)
    def test_198_del_max_addSSID(self):
        u"""删除所有的additional SSID(testlink_ID:427_2)"""
        tmp = AddSSIDBusiness(self.driver)
        #删除所有网络组
        tmp.del_all_NG()
        #检测页面上是否有第一个额外ssid
        result = tmp.check_first_exist()
        print "result = %s"%result
        #新建一个额外的ssid
        tmp.new_ssid(data_wireless['add_ssid'],data_wireless['short_wpa'])
        assert result == False,"delete max additional ssid number,test fail!"
        print "delete max additional ssid number,test pass!"

    #删除额外ssid后无法扫描(testlink_ID:427_3)
    def test_199_del_add_ssid(self):
        u"""删除额外ssid后无法扫描(testlink_ID:427_3)"""
        tmp = AddSSIDBusiness(self.driver)
        #删除新建一个额外的ssid
        tmp.del_new_ssid()
        #无线扫描这个ssid
        result = tmp.ssid_scan_result(data_wireless['add_ssid'],data_basic['wlan_pc'])
        print result
        #测试完毕，禁用无线网卡，使pc能够上网
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("AddSSID")
        assert result == False,"wifi client can scan the AP after del new Additional SSID,test fail!"
        print "wifi client can't scan the AP after del new Additional SSID,test pass!"



    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
