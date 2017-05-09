# 19.HomeControlCenterBBGW
this is a web running on BBGW 

![你好](https://raw.githubusercontent.com/Lee-Kevin/19.HomeControlCenterBBGW/master/images/1.png)

## Set the App as default start

1. Move the homecontrol file to the /etc/inid.d/ directory.
2. Set the script as the excute script.
```shell
chmod +x homecontrol
```
3. set the app as default start app by running:
 ```shell
 insserv -v -d /etc/init.d/homecontrol
 ```
 
 or by running this
 
 ```shell
 update-rc.d assistant defaults
 ```
