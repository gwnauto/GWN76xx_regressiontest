#coding=utf-8
#作者：蒋甜
#时间：2018.03.29
#描述：用例集，调用bandwidth_business
import unittest,time
from system_settings.mesh.mesh_business import MeshBusiness
from selenium import webdriver
import sys
from clients.client_access.clientaccess_business import ClientAccessBusiness
from login.login_business import LoginBusiness
from setupwizard.setupwizard_business import SWBusiness
from ssid.ssid_business import SSIDBusiness
from access_points.aps_business import APSBusiness
from system_settings.maintenance.upgrade.upgrade_business import UpgradeBusiness
# from network_group.networkgroup_business import NGBusiness
from connect.ssh import SSH
from data import data
from captive_portal.captiveportal_business import CPBusiness
from network_group.networkgroup_business import NGBusiness
from bandwidth.bandwidth_business import BandwidthBusiness

reload(sys)
sys.setdefaultencoding('utf-8')

data_basic = data.data_basic()
data_login = data.data_login()
data_wireless = data.data_wireless()
data_ng = data.data_networkgroup()
data_AP = data.data_AP()
data_bandwidth = data.data_bandwidth()

class TestBandwidth(unittest.TestCase):
    u"""测试ssid的用例集(runtime:10h)"""
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

    #检查带宽规则列表,保存按钮生效
    def test_002_check_bandwidth_rule(self):
        u"""检查带宽规则列表(testlink_ID:566,577)"""
        tmp = BandwidthBusiness(self.driver)
        #添加一条带宽规则
        tmp.add_bandwidth_rule_up_downstream(data_bandwidth['upstream'],data_bandwidth['downstream'])
        #判断该带宽规则是否添加成功
        result = tmp.check_edit_button(1)
        self.assertTrue(result)

    #检查开启带宽规则
    def test_003_check_bandwidth_enabled(self):
        u"""检查开启带宽规则(testlink_ID:567)"""
        tmp = BandwidthBusiness(self.driver)
        #检查带宽规则界面第一条规则的状态是否为开启
        result = tmp.check_n_bandwidth_enable_dis(1)
        self.assertTrue(result)

    #检查关闭带宽规则
    def test_004_check_bandwidth_disabled(self):
        u"""检查关闭带宽规则(testlink_ID:568)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.bandwidth_rule_enadle_dis(1)
        #检查带宽规则界面第一条规则的状态是否为开启
        result = tmp.check_n_bandwidth_enable_dis(1)
        self.assertFalse(result)

    #all按钮
    def test_005_check_all_button(self):
        u"""all按钮(testlink_ID:569)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp1.new_ssid(data_wireless['all_ssid']+"2",data_wireless["short_wpa"])
        result = tmp.check_all()
        self.assertNotIn(False,result)

    #none按钮
    def test_006_check_none_button(self):
        u"""none按钮(testlink_ID:570)"""
        tmp = BandwidthBusiness(self.driver)
        result = tmp.check_none()
        self.assertNotIn(True,result)

    #ssid检测,检测带宽规则界面显示默认的ssid
    def test_007_check_ssid(self):
        u"""ssid检测_01,检测带宽规则界面显示默认的ssid(testlink_ID:571_01)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1= SWBusiness(self.driver)
        ssid = tmp1.default_ssid(data_AP['master:mac'])
        result = tmp.check_ssid_in_bandwidth(ssid)
        self.assertTrue(result)

    #ssid检测_02,检测带宽规则界面显示修改后的ssid
    def test_008_check_ssid(self):
        u"""ssid检测_02,检测带宽规则界面显示修改后的ssid(testlink_ID:571_02)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp1.change_wifi_ssid_key(data_wireless['all_ssid'],data_wireless["short_wpa"])
        result = tmp.check_ssid_in_bandwidth(data_wireless['all_ssid'])
        self.assertTrue(result)

    #ssid检测_03,检测带宽规则界面显示新增的ssid
    def test_009_check_ssid(self):
        u"""ssid检测_03,检测带宽规则界面显示新增的ssid(testlink_ID:571_03)"""
        tmp = BandwidthBusiness(self.driver)
        #删除界面的带宽规则
        tmp.del_bandwidth_rule()
        #新增一条带宽规则
        tmp.add_bandwidth_rule_up_downstream(data_bandwidth['upstream'],data_bandwidth['downstream'])
        #检查带宽规则是否存在
        result = tmp.check_ssid_in_bandwidth(data_wireless['all_ssid']+"2")
        self.assertTrue(result)

    #ssid检测_03,删除ssid ,检测带宽规则界面删除该规则
    def test_010_check_ssid(self):
        u"""ssid检测_04,删除ssid ,检测带宽规则界面删除该规则(testlink_ID:571_04)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        #删除ssid
        tmp1.del_n_ssid(2)
        #检查带宽规则是否存在
        result = tmp.check_ssid_in_bandwidth(data_wireless['all_ssid']+"2")
        self.assertFalse(result)

    #约束范围:all
    def test_011_check_all_range(self):
        u"""约束范围:all(testlink_ID:572)"""
        tmp = BandwidthBusiness(self.driver)
        #检查范围为all时，带宽规则界面是否显示为all
        result = tmp.bandwidth_range(1)
        self.assertEqual("All",result)

    #约束范围MAC_01（输入正确格式的mac地址，并且都是小写的地址）
    def test_012_check_mac_range(self):
        u"""约束范围MAC_01，小写的地址(testlink_ID:573_01)"""
        tmp = BandwidthBusiness(self.driver)
        #删除之前的规则
        tmp.del_bandwidth_rule()
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        mac1 = mac.upper()
        #添加mac规则，填入小写的地址
        tmp.add_bandwidth_rule_range_mac('MAC',mac,data_bandwidth['upstream'],data_bandwidth['downstream'])
        result = tmp.check_mac_ip_range(mac1,1)
        self.assertTrue(result)

    #约束范围MAC_02（输入正确格式的mac地址，并且都是大写的地址）
    def test_013_check_mac_range(self):
        u"""约束范围MAC_02，大写的地址(testlink_ID:573_02)"""
        tmp = BandwidthBusiness(self.driver)
        #删除之前的规则
        tmp.del_bandwidth_rule()
        mac = tmp.get_wlan_mac(data_basic['wlan_pc']).upper()
        #添加mac规则，填入小写的地址
        tmp.add_bandwidth_rule_range_mac('MAC',mac,data_bandwidth['upstream'],data_bandwidth['downstream'])
        result = tmp.check_mac_ip_range(mac,1)
        self.assertTrue(result)

    #约束范围MAC_03（输入正确格式的mac地址，大写加小写）
    def test_014_check_mac_range(self):
        u"""约束范围MAC_03，大写加小写的地址(testlink_ID:573_03)"""
        tmp = BandwidthBusiness(self.driver)
        #删除之前的规则
        tmp.del_bandwidth_rule()
        mac = data_bandwidth['upper_small'].upper()
        #添加mac规则，填入大写加小写混合
        tmp.add_bandwidth_rule_range_mac('MAC',data_bandwidth['upper_small'],data_bandwidth['upstream'],data_bandwidth['downstream'])
        result = tmp.check_mac_ip_range(mac,1)
        self.assertTrue(result)

    #约束范围MAC_04（输入错误的格式xx-xx-xx-xx-xx-xx）
    def test_015_check_mac_range(self):
        u"""约束范围MAC_04，输入错误的格式xx-xx-xx-xx-xx-xx(testlink_ID:573_04)"""
        tmp = BandwidthBusiness(self.driver)
        #填入错误格式的mac
        result,result1 = tmp.add_bandwidth_rule_range_error_mac('MAC',data_bandwidth['err_mac1'])
        self.assertTrue(result)
        self.assertTrue(result1)

    #约束范围MAC_05（输入错误的格式xxxxxxxxxxxx）
    def test_016_check_mac_range(self):
        u"""约束范围MAC_05，输入错误的格式xxxxxxxxxxxx(testlink_ID:573_05)"""
        tmp = BandwidthBusiness(self.driver)
        #填入错误格式的mac
        result,result1 = tmp.add_bandwidth_rule_range_error_mac('MAC',data_bandwidth['err_mac2'])
        self.assertTrue(result)
        self.assertTrue(result1)

    #约束范围MAC_06（输入错误的长度）
    def test_018_check_mac_range(self):
        u"""约束范围MAC_06，输入错误的长度(testlink_ID:573_06)"""
        tmp = BandwidthBusiness(self.driver)
        #填入错误格式的mac
        result,result1 = tmp.add_bandwidth_rule_range_error_mac('MAC',data_bandwidth['err_mac3'])
        self.assertTrue(result)
        self.assertTrue(result1)

    #约束范围MAC_07（输入错误的长度）
    def test_019_check_mac_range(self):
        u"""约束范围MAC_07，输入非法字符(testlink_ID:573_07)"""
        tmp = BandwidthBusiness(self.driver)
        #填入错误格式的mac
        result,result1 = tmp.add_bandwidth_rule_range_error_mac('MAC',data_bandwidth['err_mac4'])
        self.assertTrue(result)
        self.assertTrue(result1)

    #约束范围MAC_08（输入mac为空）
    def test_020_check_mac_range(self):
        u"""约束范围MAC_08，输入非法字符(testlink_ID:573_08)"""
        tmp = BandwidthBusiness(self.driver)
        #填入错误格式的mac
        result,result1 = tmp.add_bandwidth_rule_range_error_mac('MAC',"")
        self.assertTrue(result)
        self.assertTrue(result1)

       #约束范围IP_01（输入合法的主机ip）
    def test_021_check_ip_range(self):
        u"""约束范围IP_01,输入合法的ip(testlink_ID:574_01)"""
        tmp = BandwidthBusiness(self.driver)
        #编辑带宽规则，填入合法的ip
        tmp.edit_bandwidth_ip_rule(1,"IP Address",data_bandwidth['host_ip'])
        result = tmp.check_mac_ip_range(data_bandwidth['host_ip'],1)
        self.assertTrue(result)

    #约束范围IP_02（输入合法的带掩码ip）
    def test_022_check_ip_range(self):
        u"""约束范围IP_02,输入合法的带掩码ip(testlink_ID:574_02)"""
        tmp = BandwidthBusiness(self.driver)
        #编辑带宽规则，填入网段ip
        tmp.edit_bandwidth_ip_rule(1,"IP Address",data_bandwidth['ip'])
        result = tmp.check_mac_ip_range(data_bandwidth['ip'],1)
        self.assertTrue(result)

    #约束范围IP_03（输入错误的ip）
    def test_023_check_ip_range(self):
        u"""约束范围IP_03,输入错误的ip(testlink_ID:574_03)"""
        tmp = BandwidthBusiness(self.driver)
        #填入错误的ip,查看是否有错误提示
        result,result1 = tmp.edit_bandwidth_ip_rule_error(1,data_bandwidth['error_ip'])
        self.assertTrue(result)
        self.assertTrue(result1)

     #上游速率输入框检查(负数,大于1000)
    def test_024_check_upstream(self):
        u"""上游速率输入框检查:负数,大于1000(testlink_ID:575_01)"""
        tmp = BandwidthBusiness(self.driver)
        #检查上游速率框输入负数
        result,result1 = tmp.edit_bandwidth_upstream_error(1,data_bandwidth['upstream_neg'])
        #检查上游速率框输入大于1000
        result2,result3 = tmp.edit_bandwidth_upstream_error(1,data_bandwidth['upstream_big'])
        self.assertTrue(result)
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)

    #上游速率输入框单位为kbps
    def test_025_check_upstream(self):
        u"""上游速率输入框单位为kbps(testlink_ID:575_02)"""
        tmp = BandwidthBusiness(self.driver)
        #修改上游速率单位为kbps,检查输入速率为大于1000000
        result,result1 = tmp.edit_upstream_unit_error(1,data_bandwidth['upstream_more'],"k")
        self.assertTrue(result)
        self.assertTrue(result1)

     #上游速率输入框检查(字母,特殊字符)
    def test_026_check_upstream(self):
        u"""上游速率输入框检查:字母,特殊字符(testlink_ID:575_03)"""
        tmp = BandwidthBusiness(self.driver)
        ##上游速率输入框检查输入字母
        result,result1 = tmp.edit_bandwidth_upstream_error(1,data_bandwidth['upstream_letter'])
        #上游速率输入框检查输入特殊字符
        result2,result3 = tmp.edit_bandwidth_upstream_error(1,data_bandwidth['upstream_chara'])
        self.assertTrue(result)
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)

      #下游速率输入框检查(负数，大于1000)
    def test_027_check_downstream(self):
        u"""下游速率输入框检查(testlink_ID:576_01)"""
        tmp = BandwidthBusiness(self.driver)
        #判断输入异常值是否会有错误提示，负数
        result,result1 = tmp.edit_bandwidth_downstream_error(1,data_bandwidth['downstream_neg'])
        #判断输入异常值是否会有错误提示，大于1000
        result2,result3 = tmp.edit_bandwidth_downstream_error(1,data_bandwidth['downstream_big'])
        self.assertTrue(result)
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)

    #下游速率输入框单位为kbps
    def test_028_check_downstream(self):
        u"""下游速率输入框单位为kbps(testlink_ID:576_02)"""
        tmp = BandwidthBusiness(self.driver)
        #修改上游速率单位为kbps,检查输入速率为大于1000000(超过范围)
        result,result1 = tmp.edit_downstream_unit_error(1,data_bandwidth['downstream_more'],"k")
        self.assertTrue(result)
        self.assertTrue(result1)

     #下游速率输入框检查(字母,特殊字符)
    def test_029_check_downstream(self):
        u"""下游速率输入框检查:字母,特殊字符(testlink_ID:576_03)"""
        tmp = BandwidthBusiness(self.driver)
        #下游速率输入框检查输入字母
        result,result1 = tmp.edit_bandwidth_upstream_error(1,data_bandwidth['downstream_letter'])
        #下游速率输入框检查输入特殊字符
        result2,result3 = tmp.edit_bandwidth_upstream_error(1,data_bandwidth['downstream_chara'])
        self.assertTrue(result)
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)

    #检查取消按钮
    def test_030_cancle_button(self):
        u"""检查取消按钮(testlink_ID:578)"""
        tmp = BandwidthBusiness(self.driver)
        #删除界面的带宽规则
        tmp.del_bandwidth_rule_save()
        #新增一条带宽规则，不保存
        tmp.add_bandwidth_rule_cancel(data_bandwidth['upstream'],data_bandwidth['downstream'])
        result = tmp.check_bandwidth_n(1)
        self.assertFalse(result)

    #修改配置
    def test_031_edit_bandwidth(self):
        u"""修改配置(testlink_ID:579)"""
        tmp = BandwidthBusiness(self.driver)
        #新增一条带宽规则
        tmp.add_bandwidth_rule_up_downstream(data_bandwidth['upstream'],data_bandwidth['downstream'])
        #修改这条规则的上游速率，并检查是否修改成功
        tmp.edit_bandwidth_up(1,data_bandwidth['upstream_edit'])
        result = tmp.check_upstream(1,data_bandwidth['upstream_edit'])
        self.assertTrue(result)

    #删除规则
    def test_032_delete_rule(self):
        u"""修改配置(testlink_ID:580)"""
        tmp = BandwidthBusiness(self.driver)
        #删除界面的带宽规则
        tmp.del_bandwidth_rule_save()
        result = tmp.check_bandwidth_n(1)
        self.assertFalse(result)

    #删除ssid后，创建的ssid规则消失
    def test_033_delete_ssid(self):
        u"""删除ssid后，创建的ssid规则消失(testlink_ID:581)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp1.new_ssid(data_wireless['all_ssid']+"2",data_wireless["short_wpa"])
        #新建一条全选的带宽规则
        tmp.add_bandwidth_rule_up_downstream(data_bandwidth['upstream'],data_bandwidth['downstream'])
        #删除新增的ssid
        tmp1.del_all_NG()
        time.sleep(5)
        result = tmp.check_bandwidth_n(2)
        self.assertFalse(result)

    #删除ssid后，创建的mac规则消失
    def test_034_delete_ssid_mac(self):
        u"""删除ssid后，创建的mac规则消失(testlink_ID:582)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp1.new_ssid(data_wireless['all_ssid']+"2",data_wireless["short_wpa"])
        #新建一条范围为mac的带宽规则
        tmp.del_bandwidth_rule()
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        tmp.add_bandwidth_rule_range_mac('MAC',mac,data_bandwidth['upstream'],data_bandwidth['downstream'])
        #删除新增的ssid
        tmp1.del_all_NG()
        result = tmp.check_bandwidth_n(2)
        self.assertFalse(result)

    #删除ssid后，创建的ip规则消失
    def test_035_delete_ssid_ip(self):
        u"""删除ssid后，创建的ip规则消失(testlink_ID:583)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp1.new_ssid(data_wireless['all_ssid']+"2",data_wireless["short_wpa"])
        #新建一条范围为ip的带宽规则
        tmp.del_bandwidth_rule()
        tmp.add_bandwidth_ip_rule("IP Address",data_bandwidth['host_ip'],data_bandwidth['upstream'],data_bandwidth['downstream'])
        #删除新增的ssid
        tmp1.del_all_NG()
        result = tmp.check_bandwidth_n(2)
        self.assertFalse(result)

    #创建规则后，重启配置不丢失
    def test_036_bandwidth_reboot(self):
        u"""创建规则后，重启配置不丢失(testlink_ID:584)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp2 = LoginBusiness(self.driver)
        #重启ap
        tmp1.reboot_router(data_basic['DUT_ip'],data_basic['sshUser'],data_login['all'])
        time.sleep(300)
        tmp2.refresh_login_ap()
        #检查带宽规则是否还存在
        result = tmp.check_bandwidth_n(1)
        self.assertTrue(result)

    #验证all规则上下行带宽生效kbps
    def test_037_bandwidth_kbps(self):
        u"""验证all规则上下行带宽生效kbps(testlink_ID:586)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #新增一条单位kbps的带宽规则
        tmp.add_bandwidth_rule_up_downstream_unit(data_bandwidth['upstream_k'],data_bandwidth['downstream_k'],"k")
        #获取上下行速率值
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #验证all规则上下行带宽生效Mbps,且未开启vlan
    def test_038_bandwidth_Mbps(self):
        u"""验证all规则上下行带宽生效Mbps,且未开启vlan(testlink_ID:587)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #新增一条单位mbps的带宽规则
        tmp.add_bandwidth_rule_up_downstream(data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #获取上下行速率值
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #验证all规则上行带宽生效，下行带宽不受限制
    def test_039_bandwidth_upstream(self):
        u"""验证all规则上行带宽生效，下行带宽不受限制(testlink_ID:588)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #新增一条规则只限制上行速率
        tmp.add_bandwidth_rule_upstream(data_bandwidth['upstream_less'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        #检查上行速率被限制，下行速率没有限制
        self.assertGreater(result1,2)
        self.assertLessEqual(result2,1)

    #验证all规则下行带宽生效，上行带宽不受限制
    def test_040_bandwidth_downstream(self):
        u"""验证all规则下行带宽生效，上行带宽不受限制(testlink_ID:589)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #新增一条规则只限制下行速率
        tmp.add_bandwidth_rule_downstream(data_bandwidth['downstream_less'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result1-1)
        #检查下行速率被限制，上行速率没有限制
        self.assertGreater(result,2)
        self.assertLessEqual(result2,1)

    #验证all规则+开启vlan的ssid规则生效
    def test_041_bandwidth_vlan(self):
        u"""验证all规则+开启vlan的ssid规则生效(testlink_ID:591)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp2 = LoginBusiness(self.driver)
        tmp3 = NGBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #在ssid中新建一个带vlan的ssid
        tmp1.new_vlan_ssid_device(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],"2")
        #在7000中新建一个ssid,设置vlan为2,开启DHCP
        tmp3.mixed_7000_new_NG()
        #重新登录ap
        tmp2.refresh_login_ap()
        #新增加带vlan的ssid的带宽规则
        tmp.add_bandwidth_rule_up_downstream(data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #检查带宽速率是否被限制
        result = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #验证all规则+未开启vlan的ssid规则，终端连接到开vlan的ssid规则，速率不受限制
    def test_042_bandwidth_vlan(self):
        u"""验证all规则+未开启vlan的ssid规则，终端连接到开vlan的ssid规则，速率不受限制(testlink_ID:590)"""
        tmp = BandwidthBusiness(self.driver)
        #删除上一条限制带vlan ssid的带宽规则
        tmp.del_special_bandwidth_ssid(2)
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        self.assertGreater(result,5)
        self.assertGreater(result1,5)

    #验证mac规则+开启vlan的ssid规则生效
    def test_043_mac_bandwidth_vlan(self):
        u"""验证mac规则+开启vlan的ssid规则生效(testlink_ID:598)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #新增mac规则
        tmp.add_bandwidth_rule_range_mac('MAC',mac,data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #获取带vlan ssid的上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        #检查速率是否被限制
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #设置mac+未开启vlan的ssid规则，终端连接开启vlan的ssid，速率不被限制
    def test_044_mac_bandwidth(self):
        u"""设置mac+未开启vlan的ssid规则，终端连接开启vlan的ssid，速率不被限制(testlink_ID:596)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #设置mac+未开启vlan的ssid规则
        tmp.add_bandwidth_rule_range_mac_ssid('MAC',mac,data_bandwidth['upstream'],data_bandwidth['downstream'],1)
        #获得上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        #检查是否不被限制
        self.assertGreater(result,5)
        self.assertGreater(result1,5)

    #验证ip规则+开启vlan的ssid规则生效
    def test_045_ip_bandwidth_vlan(self):
        u"""验证ip规则+开启vlan的ssid规则生效(testlink_ID:611)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #新增ip规则+开启vlan的ssid 的带宽规则
        tmp.add_bandwidth_ip_rule("IP Address",data_bandwidth['ip_vlan'],data_bandwidth['upstream'],data_bandwidth['downstream'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-10)
        result3 = abs(result1-10)
        #检查速率限制情况
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #验证mac规则上下行生效 kbps
    def test_046_mac_bandwidth_up_downstream(self):
        u"""验证mac规则上下行生效 kbps(testlink_ID:592)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #删除ssid
        tmp1.del_all_NG()
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #新增速为1000kbps的带宽规则，并填入无线网卡的mac
        tmp.add_bandwidth_rule_range_mac_unit('MAC',mac,data_bandwidth['upstream_k'],data_bandwidth['downstream_k'],"k")
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        #检查限制情况
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

      #验证mac规则上下行生效 mbps,无线终端mac地址规则生效
    def test_047_mac_bandwidth_up_downstream(self):
        u"""验证mac规则上下行生效 mbps(testlink_ID:593,600)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #新增速为10mbps的带宽规则，并填入无线网卡的mac
        tmp.add_bandwidth_rule_range_mac('MAC',mac,data_bandwidth['upstream'],data_bandwidth['downstream'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-10)
        result3 = abs(result1-10)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #验证mac规则上行带宽生效，下行带宽不受限制
    def test_048_bandwidth_upstream_mac(self):
        u"""验证mac规则上行带宽生效，下行带宽不受限制(testlink_ID:594)"""
        tmp = BandwidthBusiness(self.driver)
        #编辑带宽规则为只限制上行速率
        tmp.edit_bandwidth_up(1,data_bandwidth['upstream_less'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        #检查上行速率被限制，下行速率不被限制
        self.assertGreater(result1,2)
        self.assertLessEqual(result2,1)

    #验证mac规则下行带宽生效，上行带宽不受限制
    def test_049_bandwidth_downstream_mac(self):
        u"""验证mac规则下行带宽生效，上行带宽不受限制(testlink_ID:595)"""
        tmp = BandwidthBusiness(self.driver)
        #编辑带宽规则为只限制下行速率
        tmp.edit_bandwidth_down(1,data_bandwidth['downstream_less'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        #检查下行速率被限制，上行速率不被限制
        self.assertGreater(result1,2)
        self.assertLessEqual(result2,1)

    #验证mac规则，设置非终端连接的mac,速率不受限制
    def test_050_bandwidth_mac(self):
        u"""验证mac规则，设置非终端连接的mac,速率不受限制(testlink_ID:597)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #新增mac规则，设置非终端连接的mac
        tmp.add_bandwidth_rule_range_mac('MAC',data_bandwidth['case-sensitive'],data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        #检查上下行速率是否不被限制
        self.assertGreater(result,5)
        self.assertGreater(result1,5)

    #一个mac关联到多个不同vlan的ssid规则生效
    def test_051_bandwidth_lan_mac(self):
        u"""一个mac关联到多个不同vlan的ssid规则生效(testlink_ID:603)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #新建一个带vlan的ssid,并将设备加入
        tmp1.new_vlan_ssid_device(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],"2")
        mac = tmp.get_wlan_mac(data_basic['wlan_pc'])
        #新增mac规则，ssid0+ssid1
        tmp.add_bandwidth_rule_range_mac('MAC',mac,data_bandwidth['upstream'],data_bandwidth['downstream'])
        #分别获得其上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result3 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result4 = abs(result-10)
        result5 = abs(result1-10)
        result6 = abs(result2-10)
        result7 = abs(result3-10)
        #检查速率限制情况
        self.assertLessEqual(result4,1)
        self.assertLessEqual(result5,1)
        self.assertLessEqual(result6,1)
        self.assertLessEqual(result7,1)

    #mac规则修改后，新规则生效
    def test_052_bandwidth_edit_mac_rule(self):
        u"""mac规则修改后，新规则生效(testlink_ID:604)"""
        tmp = BandwidthBusiness(self.driver)
        #修改带vlan的ssid的带宽限制数值
        tmp.edit_bandwidth_up_downstream(1,data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        #检查速率是否为修改后的速率
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #删除mac规则后，速率将不被限制
    def test_053_bandwidth_del_mac_rule(self):
        u"""删除mac规则后，速率将不被限制(testlink_ID:605)"""
        tmp = BandwidthBusiness(self.driver)
        #删除mac规则
        tmp.del_bandwidth_rule_save()
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        #检查速率是否不受限制
        self.assertGreater(result,5)
        self.assertGreater(result1,5)

    #单个ip规则生效
    def test_054_ip_host_rule(self):
        u"""单个ip规则生效(testlink_ID:606)"""
        tmp = BandwidthBusiness(self.driver)
        ip = tmp.get_ip_after_connect(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        #设置主机 ip的带宽规则
        tmp.add_bandwidth_ip_rule("IP Address",ip,data_bandwidth['upstream'],data_bandwidth['downstream'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-10)
        result3 = abs(result1-10)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #ip网段规则生效
    def test_055_ip_rule(self):
        u"""ip网段规则生效(testlink_ID:607)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #设置网段ip的带宽限制规则
        tmp.add_bandwidth_ip_rule("IP Address",data_bandwidth['ip_rule'],data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #ip+未开启vlan的ssid规则生效
    def test_056_group0_ip_rule(self):
        u"""ip+未开启vlan的ssid规则生效(testlink_ID:609)"""
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        #删除ssid
        tmp1.del_all_NG()
        #删除带宽规则
        tmp.del_bandwidth_rule()
        #添加ssid0的带宽规则
        tmp.add_bandwidth_ip_rule("IP Address",data_bandwidth['ip_rule'],data_bandwidth['upstream'],data_bandwidth['downstream'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-10)
        result3 = abs(result1-10)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #ip+ssid,未设置的ip连接到ssid速率不做限制
    def test_057_unset_ip_bandwidth(self):
        u"""ip+ssid,未设置的ip连接到ssid速率不做限制(testlink_ID:610)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #未设置的ip规则速率限制
        tmp.add_bandwidth_ip_rule("IP Address",data_bandwidth['host_ip'],data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #获取上下行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        self.assertGreater(result,5)
        self.assertGreater(result1,5)

    #ip+最小上行带宽规则生效
    def test_058_ip_min_upstream(self):
        u"""ip+最小上行带宽规则生效(testlink_ID:612)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #设置ip规则为1mbps
        ip = tmp.get_ip_after_connect(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'])
        #设置主机 ip的带宽规则
        tmp.add_bandwidth_ip_rule("IP Address",ip,data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #获取上行速率
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = abs(result-1)
        self.assertLessEqual(result1,1)

    #ip+最小下行带宽规则生效
    def test_059_ip_min_downstream(self):
        u"""ip+最小下行带宽规则生效(testlink_ID:613)"""
        tmp = BandwidthBusiness(self.driver)
        #获取上行速率
        result = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = abs(result-1)
        self.assertLessEqual(result1,1)

    #创建多条ip规则都生效
    def test_060_mutil_ip_rule_01(self):
        u"""创建多条ip规则都生效(testlink_ID:615_01)"""
        #在ssid中新建一个带vlan的ssid
        tmp = BandwidthBusiness(self.driver)
        tmp1 = SSIDBusiness(self.driver)
        tmp.del_bandwidth_rule()
        tmp1.new_vlan_ssid_device(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],"2")
        #设置group0的带宽规则
        tmp.add_bandwidth_ip_rule("IP Address",data_bandwidth['ip_rule'],data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #设置group1的带宽规则
        tmp.add_bandwidth_ip_rule("IP Address",data_bandwidth['ip_vlan'],data_bandwidth['upstream'],data_bandwidth['downstream'])
        #分别连接并判断group0/group1的带宽限制生效
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #创建多条ip规则都生效
    def test_061_mutil_ip_rule_02(self):
        u"""创建多条ip规则都生效(testlink_ID:615_02)"""
        #在ssid中新建一个带vlan的ssid
        tmp = BandwidthBusiness(self.driver)
        result = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-10)
        result3 = abs(result1-10)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #ip规则修改后，新规则生效
    def test_062_edit_ip_rule(self):
        u"""ip规则修改后，新规则生效(testlink_ID:616)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.edit_bandwidth_up_downstream(4,data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #分别连接并判断group0带宽修改后限制生效
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #删除ip规则，客户端速率不受影响
    def test_063_del_ip_rule(self):
        u"""删除ip规则，客户端速率不受影响(testlink_ID:618)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        self.assertGreater(result,10)
        self.assertGreater(result1,10)

    #多个ssid规则生效
    def test_064_singe_ssid_rule(self):
        u"""多个ssid规则生效(testlink_ID:620)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.add_bandwidth_rule_up_downstream(data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #分别连接并判断group0/group1的带宽限制生效
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result3 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        self.assertGreater(result,5)
        self.assertGreater(result1,5)
        self.assertGreater(result2,5)
        self.assertGreater(result3,5)

    #开启vlan的ssid生效
    def test_065_vlan_ssid(self):
        u"""开启vlan的ssid生效(testlink_ID:624)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #新增一条带宽规则，选择带vlan的ssid
        tmp.add_bandwidth_rule_range_select_ssid(2,data_bandwidth['upstream'],data_bandwidth['downstream'])
         #分别连接并判断group1的带宽限制生效
        result = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-10)
        result3 = abs(result1-10)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #ssid+最小上行带宽生效
    def test_066_all_min_upstream(self):
        u"""ssid+最小上行带宽生效(testlink_ID:621)"""
        tmp = BandwidthBusiness(self.driver)
        tmp.del_bandwidth_rule()
        #新增一条带宽规则，ssid1
        tmp.add_bandwidth_rule_up_downstream(data_bandwidth['upstream_less'],data_bandwidth['downstream_less'])
        #分别连接并判断group1的带宽限制生效
        result = tmp.check_upstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-1)
        result3 = abs(result1-1)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #ssid+最小上行带宽生效
    def test_067_all_min_downstream(self):
        u"""ssid+最小上行带宽生效(testlink_ID:622)"""
        tmp = BandwidthBusiness(self.driver)
        #分别连接并判断group1的带宽限制生效
        result = tmp.check_downstream_iperf(data_wireless['all_ssid']+"2",data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = abs(result-1)
        self.assertLessEqual(result1,1)

    #不开vlan的ssid生效
    def test_068_no_vlan_ssid(self):
        u"""不开vlan的ssid生效(testlink_ID:623)"""
        tmp = BandwidthBusiness(self.driver)
          #分别连接并判断group0的带宽限制生效
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-10)
        result3 = abs(result1-10)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    #开启vlan的ssid规则生效
    def test_069_vlan_ssid(self):
        u"""开启vlan的ssid规则生效(testlink_ID:624)"""
        tmp = BandwidthBusiness(self.driver)
          #分别连接并判断group0的带宽限制生效
        result = tmp.check_upstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result1 = tmp.check_downstream_iperf(data_wireless['all_ssid'],data_wireless["short_wpa"],data_basic['wlan_pc'],data_basic['lan_pc'])
        result2 = abs(result-10)
        result3 = abs(result1-10)
        self.assertLessEqual(result2,1)
        self.assertLessEqual(result3,1)

    def test_10002_ending(self):
         #测试完毕，禁用无线网卡，使pc能够上网
        tmp = BandwidthBusiness(self.driver)
        tmp.dhcp_release_wlan(data_basic['wlan_pc'])
        tmp.wlan_disable(data_basic['wlan_pc'])
        #rsyslog服务器完成工作
        tmp.finish_rsyslog("Bandwidth")

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
