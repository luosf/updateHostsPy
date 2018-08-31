#coding=utf8
# reload sys
# import urllib2 #python 27
import sys,io
import urllib.request as urllib2
import urllib
import platform
import datetime
import time
import re
import os
from io import StringIO
import shutil
import configparser
import sys
import socket

config_path = 'config.ini'
# default setting
hosts_folder = ""
hosts_location = hosts_folder + "hosts"

source_list = ['https://raw.githubusercontent.com/vokins/simpleu/master/hosts']

not_block_sites = 0
always_on = 0
# default setting

errorLog = open('errorLog.txt', 'a')

# 错误信息
def get_cur_info():
	return (sys._getframe().f_back.f_code.co_name)

# 结束 
def exit_this():
	errorLog.close()
	sys.exit()

# 检查是否可上网（baidu）
def check_connection():
	sleep_seconds = 1200
	i = 0
	for i in range(sleep_seconds):
		try:
			socket.gethostbyname("www.baidu.com")
			break
		except socket.gaierror:
			time.sleep(1)
	if i == sleep_seconds - 1:
		exit_this()

# 检查系统 获取host在系统中的路径 
def check_system():
	global hosts_folder
	global hosts_location
	if platform.system() == 'Windows':
		hosts_folder = os.environ['SYSTEMROOT'] + "\\System32\\drivers\\etc\\"
	elif platform.system() == 'Linux' or platform.system() == 'Darwin':
		hosts_folder = "/etc/"
	else:
		exit_this()
	hosts_location = hosts_folder + "hosts"

# 读config文件 获取host source 和 配置
def get_config():
	global source_list
	global not_block_sites
	global always_on
	print("config path:"+config_path)
	if os.path.exists('config.ini'):
		print("config path Ok")
		try:
			print("config Open..")
			# # 清除Windows记事本自动添加的BOM
			with open(config_path,'rb') as f:
				content = f.read().decode('utf-8-sig').encode('utf8').decode('utf8')

			print('config open, Ok')
			# config = configparser.ConfigParser()
			config=configparser.RawConfigParser()
			# config.read('config.ini',encoding='utf8')
			config.readfp(StringIO(content))
			print('source_select..')
			source_list_key = config.options('source_select')

			source_list=[]
			for i in range(len(source_list_key)):
				source_list.append(config.get('source_select', source_list_key[i]))

			
			source_list_key = config.options('source_github')
			for i in range(len(source_list_key)):
				sourceurl=config.get('source_github', source_list_key[i])
				sourceurl=sourceurl.replace("https://github.com/",'https://raw.githubusercontent.com/')
				sourceurl=sourceurl.replace("/blob/","/")
				source_list.append(sourceurl)

			print("source list:\n",(source_list))

			not_block_sites = config.get("function", "not_block_sites")
			always_on = config.get("function", "always_on")
		except BaseException as e:
			print(e)
			errorLog.write(
				str(datetime.datetime.now()) + '\n' + 'function:' + get_cur_info() + '\nerror:' + str(e) + '\n\n')
			exit_this()

# 备份原始host文件
def backup_hosts():
	try:
		if (not os.path.isfile(hosts_folder + 'backup_hosts_original_by_updateHosts')) and \
				os.path.isfile(hosts_folder + 'hosts'):
			shutil.copy(hosts_folder + 'hosts', hosts_folder + 'backup_hosts_original_by_updateHosts')# 将 原host内的txt 复制到 backup_hosts_original_by_updateHosts
			print("backup origin host, Ok")

		if os.path.isfile(hosts_folder + 'hosts'):
			shutil.copy(hosts_folder + 'hosts', hosts_folder + 'backup_hosts_last_by_updateHosts')

	except BaseException as e:
		errorLog.write(
			str(datetime.datetime.now()) + '\n' + 'function:' + get_cur_info() + '\nerror:' + str(e) + '\n\n')
		exit_this()

# 下载host源到 hosts_from_web
def download_hosts():
	# print(source_list)
	hosts_from_web = open("hosts_from_web", "a")
	for x in source_list:
		try:
			data = urllib2.urlopen(x,timeout=2000)
			print("success get:"+ x)
		except BaseException as e:
			print("erros in:"+ x)
			print(e.code)
			continue
		hosts_from_web.write("# FOME: "+x)
		hosts_from_web.write(data.read().decode('gbk','ignore').encode('utf8').decode('utf8'))

# 将更新的host源，生成host文件
def process_hosts():
	try:
		hosts_content = open('hosts', 'w')
		# 来自网页的host源
		file_from_web = open('hosts_from_web')
		hosts_from_web = file_from_web.read()
		
		#用户自定义的host 源
		file_user_defined = open('hosts_user_defined.txt',encoding='utf8')
		hosts_user_defined = file_user_defined.read()
	
		hosts_content.write('#hosts_user_defined\n')
		hosts_content.write(hosts_user_defined)
		hosts_content.write('\n#hosts_user_defined\n')
		
		#更新来自网页的host源        
		hosts_content.write('\n\n#hosts_by_hostsUpdate\n\n')
		if not_block_sites is "1":
			hosts_from_web = re.sub("127.0.0.1", "#not_block_sites", hosts_from_web)
		else:
			hosts_from_web = "127.0.0.1 localhost\n\n" + hosts_from_web 

		hosts_content.write(hosts_from_web)
		hosts_content.write('\n#hosts_by_hostsUpdate')
		print(4)

		hosts_content.close()
		file_from_web.close()

		file_user_defined.close()
		os.remove('hosts_from_web')

	except BaseException as e:
		print(e)
		errorLog.write(
			str(datetime.datetime.now()) + '\n' + 'function:' + get_cur_info() + '\nerror:' + str(e) + '\n\n')
		exit_this()

# 将更新的host源 替换系统的host源
def move_hosts():
	try:
		#删除源host
		os.remove(hosts_location)
		shutil.move("hosts", hosts_location)
	except BaseException as e:
		errorLog.write(
			str(datetime.datetime.now()) + '\n' + 'function:' + get_cur_info() + '\nerror:' + str(e) + '\n\n')
		exit_this()


def main():
	print('connection..')
	check_connection()
	print('connection: Ok \n')

	print("host..")
	check_system()
	print("host..:"+hosts_location+' \n')

	print("config..")
	get_config()
	print("config Ok \n")

	print("backup_hosts..")
	backup_hosts()
	print("backup_host Ok \n")

	print("download_hosts..")
	download_hosts()
	print("download_hosts Ok \n")
	
	print("process_hosts..")
	process_hosts()
	print("process_hosts Ok")

	print("move_hosts..")
	move_hosts()
	print("move_hosts Ok")

	#刷新dns buf
	os.system('ipconfig /flushdns')
	print("dns freshed")
	
	
	errorLog.close()


if __name__ == '__main__':
	main()

if always_on == "1":
	while 1:
		time.sleep(3600)
		main()
