# Khandytool
## How to use it

1.Download and install, old version could get from pip, but new version which oversize for pypi, should download source and build, it added some jmeter run function)
```
pip install khandytool
```
2.Run in the code
```
from core.bladeTest import interactive
interactive.run(8999) #you can change the port if you like

add command line to support command quick start, you need:
$ pip install khandytool
run command:
$ toolrun
this will start some module, detail you need run toolrun -help for check
$ toolrun --module=all

```
3.Or run in the command line 
```
python -m core.bladeTest.interactive #will open 8999 port to contain the application

```

## Purpose 
- Base one daily work, build the test tools,finnaly generate one platform. it wraped some other packages, will continue add.

## Main functions
1. blade chaose executer(may have problem by install by pip and run; but ok in deply by source)
which have two models to execute ChaoseBlade command in the remote server
2. transfer xmind testcase to excel testcase(some formated restrict xmind)
3. transfer swagger url to jmeter scripts
using some opensource packge to complish this
4. transfer har file to jmeter scripts
5. fake data generation base on faker
6. kafka message sender and getter with fileter
7. mqtt message sender and getter with basic filter  
- others code snips, can add into automation testing  
- get data from jmesh  
- get fack data  
- generate test case from xmind  
- get sha1 password  
- http request send and validate  
- time counter wraper  
- multi list to single list  
- mysql operations to quick execute sql  
- redis operations to quick read or write data to it  
- kafka operations to send or get data from target topic  
- mqtt operations to send to receive data from server  


## Todo list
- add har2locust or other protocol sender... 
- add some general validate function in the automation testing, like datatype validate,response validate,callback function ...
- add some wrapped function about auto test framework, like pytest or behave 
- deploy jmeter agent to distribute server or docker warapped agent
- retry function in the auto test framework
- mock server will base one config and generate some data
- email sender and reciever
- socket sender and reciever under some fix config
- config parser for ini, yml, xml, json csv format
- quick process data with numpy or matplotlib

## Functions snapshots:
### mainPage:
<!-- ![avatar][mainPage] -->
![mainPage](1.png)
### xmind:
![xmind](2.png)
### blade
![blade](3.png)
### jmeter
![jmeter](4.png)
### mqtt
![mqtt](5.png)
### dataGen
![dataGen](6.png)

