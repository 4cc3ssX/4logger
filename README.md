# 4logger
This python script that will record all the log and send to system administrator (with socket module). Note: Run this script as root for working properly. Thanks

  	cd /path/to/file
	python3 4logger.py [HOST]:[PORT] -> python3 4logger.py 0.0.0.0:5050
  
if u wanna run it in silently and in background execute that by nohup

 	nohup python3 4logger.py 0.0.0.0:5050 > /dev/null 2>&1 &
