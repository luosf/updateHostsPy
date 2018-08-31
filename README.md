updateHosts
============

## 简介

自动从网络下载hosts文件，hosts源由用户设置。
修改自https://github.com/ladder1984/updateHosts
### 运行方法
已经自动添加了hosts源url下载路径。直接运行python updateHosts.py 即可[管理员方式]

### 文件说明

- **config.ini：** 设置参数，包括选择更新源、开启关闭功能。
- **hosts_user_defined.txt：** 可填入自定义hosts内容

### 设置说明
目前可以在config.ini文件中方设置功能。0为不开启，1为开启此功能。目前可设置的功能有：

- not_block_sites 开启后，将注释掉通过127.0.0.1屏蔽的网址
- always_on 开启后，将常驻内存，每小时执行一次更新
 
### 注意事项：

- 如果不确定是否更新成功，可查看hosts文件，Windows系统通常在C:\Windows\System32\drivers\etc下的hosts文件。
- 本软件不提供hosts文件，而是从从用户定义的地址下载hosts，默认提供几个流行的hosts，参见config.ini
- 建议使用前手动备份hosts文件
- Windows用户可能需要授予程序管理员权限：右击python27.exe，选中“属性”，在“兼容性”里勾选“以管理员身份运行此程序”。
- 建议使用Notepad++、Sublime Text编辑文件
- 删除启动项（Windows用户）：删除“启动”文件夹内的快捷方式，“启动”文件夹在开始菜单内


## 运行环境
- 操作系统：Windows、Linux、Mac OS


## 功能描述
- 下载hosts文件并更新本地hosts
- 用户可自定义hosts内容
- 可选的hosts更新源
- 可以选择下载多个hosts文件并合并
- 备份hosts文件
- 可去除屏蔽广告部分
- 可常驻后台，可每小时执行一次
- 分离出单独的配置文件
- 运行时不显示窗口
- 打包成exe文件，无需安装python即可使用
- 可单文件执行updateHosts
- 可添加启动项
- 生成错误日志errorLog.txt
- 待添加


## hosts源
hosts源来源于网络，收录入[someHosts](https://github.com/ladder1984/someHosts)项目，并选取如下hosts：

- simpleu-hosts <https://github.com/vokins/simpleu>
- google-hosts <https://github.com/txthinking/google-hosts>
- GavinHosts <http://blog.crpuer.com/GavinHosts.txt>
- imouto.host <https://github.com/zxdrive/imouto.host>

用户可在config.ini中选择，或者自定义hosts源。


## 其他
- updateHosts项目地址：<https://github.com/ladder1984/updateHosts>
- ChangeLog：<https://github.com/ladder1984/updateHosts/blob/master/ChangeLog.txt>
- 作者：<https://github.com/ladder1984> 博客：<http://www.itoldme.net>
- 欢迎反馈问题和建议，地址：<https://github.com/ladder1984/updateHosts/issues>


