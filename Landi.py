import socket
import json
import datetime
import random

################################# INFORMATION ############################

#ProjectName: PyLandi
#Version: 0.1
#Codename: sintia

#This is based on reversed app V-Land Landi, because of i disatisfy of the native app LOL
#########################################################################

class Landi(object):
	def __init__(self,token=None, HP=None, pin=None, memberid=None, fixid=None):
		self.BASE_IP = '43.245.187.254'
		self.BASE_PORT = 8981
		self.logged_in = 0

		Token = self.Gen_Token()

		if str(HP[0:2]) == '08':
			HP = "628" + HP[2:len(HP)]
			print('[WARNING] Gunakan 628xxxx daripada 08xxxxx')

		if token == None:
			rSignup = self.SendCommand('{"data":"newSignUP",\
				"date":"%s",\
				"datefordb":"%s",\
				"nextdata":["89871510011804699452"],\
				"phonenumber":"+%s",\
				"pin":"%s",\
				"tokenid":"%s",\
				"tosendtimer":0,"type":7,"versiapp":0,"vipclass":0}}-}'

				% (self.Now()[1], self.Now()[0], HP, pin, Token)
				)
			print(rSignup)
			if 'blocksignUP#Register failed' in str(rSignup['data']):
				raise Exception("Login Failed, Check Your Number And Pin Correctly")

			if "blocksignUP#Mohon hub. Cust care. Alasan : request token spam !" in str(rSignup['data']):
				raise Exception("Login Failed, Token Spam")

			approve = self.SendCommand('{"data":"approve",\
				"date":"%s",\
				"datefordb":"%s",\
				"memberid" : "%s", \
				"nextdata":["89871510011804699452"],\
				"phonenumber":"+%s",\
				"pin":"%s",\
				"tokenid":"%s",\
				"tosendtimer":0,"type":7,"versiapp":0,"vipclass":0}}-}'

  				% (self.Now()[1], self.Now()[0], rSignup['memberid'], HP, pin, Token)
				)
			print(approve)
			print('################# INFORMATION ################')
			print('PhoneNumber:%s\nMemberid:%s\nFixID:%s\nTokenID:%s\n'
				% (rSignup['phonenumber'], approve['memberid'], approve['fixid'], Token)
				)
			print('Simpan Token ini agar tidak perlu login lagi...\nPenyimpanan akan dilakukan secara otomatis...')
			print('##############################################')

			self.Logins = {"Phone" : str(rSignup['phonenumber']).replace('+',''), "memberid" : approve['memberid'], "fixid" : approve['fixid'], "tokenid" : Token, "pin" : pin}

			sync_ = self.SendCommand('{"date":"%s",\
				"datefordb":"%s",\
				"fixid" : "%s", \
				"memberid" : "%s", \
				"phonenumber":"+%s",\
				"pin":"%s",\
				"tokenid":"%s",\
				"tosendtimer":0,"type":5,"versiapp":0,"vipclass":0}}-}'

				% (self.Now()[1], self.Now()[0], self.Logins['fixid'], self.Logins['memberid'], HP, pin, self.Logins['tokenid'])
				)

			with open('{}.txt'.format(HP), 'w', encoding='utf-8') as f:
				for tipe,Login in self.Logins.items():
					f.write(str(tipe)+":"+str(Login)+"\n")


			if 'logout' in approve['formonitor'].lower(): 
				print('Login Gagal, Coba periksa Akun Anda')
			elif 'register now' in approve['formonitor'].lower():
				print('Login Success')
				self.logged_in = 1
				return self.Logins
			else:
				print('Unknown Error Detected')
				print(approve)
		elif (token or HP or pin) is None:
			raise Exception('Argument Not Enough')
		else:
			self.Logins = {"Phone" : HP, "memberid" : memberid, "fixid" : fixid, "tokenid" : token, "pin" : pin}
			#Sync Product For The First Time To Ensure The Login
			sync_ = self.SendCommand('{"date":"%s",\
				"datefordb":"%s",\
				"fixid" : "%s", \
				"memberid" : "%s", \
				"phonenumber":"+%s",\
				"pin":"%s",\
				"tokenid":"%s",\
				"tosendtimer":0,"type":5,"versiapp":0,"vipclass":0}}-}'

				% (self.Now()[1], self.Now()[0], self.Logins['fixid'], self.Logins['memberid'], HP, pin, self.Logins['tokenid'])
				)
			if 'logout' in str(sync_).lower():
				raise Exception('Sudden Logout Detected... (Please ReLogin)')
			else:
				print('Login Sukses...')
				self.logged_in = 1

	def Gen_Token(self):
		s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
		template = "dKs_HjBupuA:APA91bHJ7JRSyxwedUfrgF_Bumn$-NNih4p89r73UtUg$_m2aSFlxH8Gi-_qzdJg7D1YRXx-2UaYX2JblQcpf0Sh5XGRoKU1ub$ijV-_q59b7FB"
		passlen = 3
		p =  "".join(random.sample(s,passlen))
		return str(template).replace('$', p)

	def Now(self):
		today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		clock = datetime.datetime.now().strftime('%H:%M')
		dates = datetime.datetime.now().strftime('%Y-%m-%d')
		return today,clock,dates

	def SendCommand(self, commands):
		commands = commands.encode('utf-8')
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.BASE_IP, self.BASE_PORT))
		s.send(commands)
		data2 = ''
		while True:
			rData = s.recv(1024)
			if not rData:
				break
			data2 = str(data2) + str(rData.decode('utf-8'))

		if 'force' in str(data2).lower() or 'logout' in str(data2).lower() or 'spam' in str(data2).lower():
			return None

		return json.loads(data2.replace('}}-}', '}'))

	def SendCommand2(self, commands):
		commands = commands.encode('utf-8')
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.BASE_IP, self.BASE_PORT))
		s.send(commands)
		data2 = ''
		while True:
			rData = s.recv(1024)
			#if not rData:
			#	break
			data2 = str(data2) + str(rData.decode('utf-8'))
			print(rData.decode('utf-8'))
		return json.loads(data2.replace('}}-}', '}'))

	def Sync_Product(self):
		sync = self.SendCommand('{"date":"%s",\
			"datefordb":"%s",\
			"fixid":"%s",\
			"memberid":"%s",\
			"phonenumber":"+%s",\
			"pin":"%s",\
			"tokenid":"%s",\
			"tosendtimer":0,"type":5,"versiapp":0,"vipclass":0}}-}'

			% (self.Now()[1], self.Now()[0], 
				self.Logins['fixid'], self.Logins['memberid'], 
				self.Logins['Phone'], self.Logins['pin'], 
				self.Logins['tokenid'])
			)

		if sync is None:
			return None

		return sync['produklink']

	def ss(self):
		trx = self.SendCommand2('''{"TrxQ":"HARGA.ax10.1234",\
			"data":"trxdo",\
			"date":"%s",\
			"datefordb":"%s",\
			"fixid":"%s",\
			"memberid":"%s",\
			"phonenumber":"+%s",\
			"pin":"%s",\
			"tokenid":"%s",\
			"tosendtimer":0,"type":3,"versiapp":0,"vipclass":0}}-}'''
			
			%(self.Now()[1], 
				self.Now()[0], self.Logins['fixid'],
				self.Logins['memberid'], self.Logins['Phone'],
				self.Logins['pin'], self.Logins['tokenid'])
			)

	def GetSaldo(self):
		try:
			Get_Saldo = int((self.GetProfile()['sisasaldo']).replace('.',''))
			return Get_Saldo
		except:
			print('Null')
			return None

	def TrxDo(self, kode,tujuan,server):
		if server not in ['RO','R2','R3','R4','R5','R6','R7','R8','R9','R10']:
			print('[Error] Server Not In List')
			return -2

		try:
			products = self.Sync_Product()
			for product in products:
				if str(kode).upper() == product.split(',')[0]:
					Get_Saldo = int((self.GetProfile()['sisasaldo']).replace('.',''))
					price = int(product.split(',')[1])
					if Get_Saldo < price:
						print('[ERROR] Saldo Tidak Cukup')
						return -3

			trx = self.SendCommand('''{"TrxQ":"%s.%s.%s.%s",\
				"data":"trxdo",\
				"date":"%s",\
				"datefordb":"%s",\
				"fixid":"%s",\
				"memberid":"%s",\
				"phonenumber":"+%s",\
				"pin":"%s",\
				"tokenid":"%s",\
				"tosendtimer":0,"type":3,"versiapp":0,"vipclass":0}}-}'''
				
				%(kode, tujuan, self.Logins['pin'], 
					server, self.Now()[1], 
					self.Now()[0], self.Logins['fixid'],
					self.Logins['memberid'], self.Logins['Phone'],
					self.Logins['pin'], self.Logins['tokenid'])
				)
			if 'approvedtrx' in str(trx['data']).lower():
				UCode = "TRX"+str(self.GetSaldo())+"!"+str(self.Now()[2])+"!"+str(Get_Saldo - price)
				trx_code = {"UCode" : UCode, "Product" : kode, "Tujuan" : tujuan, "Server" : server}

				if self.Find_Trx(UCode) == None:
					print('[ERROR] Transaksi Gagal')
					return -1
				else:
					print('Transaksi Sukses')
					return trx_code
			else:
				print('Traksaksi Gagal')
				return -1
		except:
			print('Transaksi Gagal')
			return -1

	def Find_Trx(self, UCode):
		U_code = UCode.split('!')
		a_saldo = str(U_code[0]).replace('TRX','')
		tgl = U_code[1]
		b_saldo = U_code[2]
		code_msg = {0 : "On Process", 1 : "Success", 2 : "Failed"}
		trx_list = self.History()

		for trx in range(len(trx_list)-1):
			s_saldo = (str(trx_list[trx]['saldoakhir']).replace('Rp ','')).replace('.','')
			t_saldo = (str(trx_list[trx]['saldoawal']).replace('Rp ','')).replace('.','')
			
			if (s_saldo == b_saldo) and (t_saldo == a_saldo) and (tgl in str(trx_list[trx]['datetime'])) and (str(trx_list[trx]['jenis']) == 'Transaksi'):
				try:
					print(trx_list[trx])
					R_trx = {"UCode": UCode, "datetime" : trx_list[trx]['datetime'], "Product" : trx_list[trx]['kodeproduk'], 
							"Tujuan" : trx_list[trx]['nomortujuan'], "SaldoAwal" : trx_list[trx]['saldoawal'], 
							"SaldoAkhir" : trx_list[trx]['saldoakhir'], "HaPokok" : trx_list[trx]['nominal'],
							 "SN" : trx_list[trx]['sn'], "Ket" : trx_list[trx]['ket'], 
							 "Status" : str(trx_list[trx]['statustrx']), "Description" : code_msg[int(trx_list[trx]['statustrx'])]}
					if R_trx["Status"] == '1':
						print('[Sukses] Transaksi Sukses')
					elif R_trx['Status'] == '0':
						print('[Proses] Transaksi Dalam Proses')
					else:
						print('Transaksi Gagal')
						print("Status:", R_trx['Status'])
					return json.loads(json.dumps(R_trx))
				except:
					return None
		return None

	def History(self):
		H_trx = self.SendCommand('{"data":"first",\
			"date":"%s",\
			"datefordb":"%s",\
			"fixid":"%s",\
			"memberid":"%s",\
			"phonenumber":"+%s",\
			"pin":"%s",\
			"tokenid":"%s",\
			"tosendtimer":0,"type":2,"versiapp":0,"vipclass":0}}-}'

			% 	(self.Now()[1], self.Now()[0],
				 self.Logins['fixid'], self.Logins['memberid'],
				 self.Logins['Phone'], self.Logins['pin'],
				 self.Logins['tokenid'])
			)
		if H_trx is not None:
			for i in H_trx['dataHistories']:
				i['UCode'] = "TRX"+str((i['saldoawal']).replace('Rp ','')).replace('.','')+"!"+str(i['datetime'].split(' ')[0])+"!"+str((i['saldoakhir']).replace('Rp ','')).replace('.', '')

		return None if H_trx is None else json.loads(json.dumps(H_trx['dataHistories']))

	def GetProfile(self):
		profile = self.SendCommand('{"date":"%s",\
			"datefordb":"%s",\
			"fixid":"%s",\
			"memberid":"%s",\
			"phonenumber":"+%s",\
			"pin":"%s",\
			"tokenid":"%s",\
			"tosendtimer":0,"type":0,"versiapp":0,"vipclass":0}}-}'

			% (self.Now()[1], self.Now()[0],
					self.Logins['fixid'], self.Logins['memberid'],
					self.Logins['Phone'], self.Logins['pin'],
					self.Logins['tokenid'])

			)
		return None if profile is None else json.loads(json.dumps(profile['profile']))

if __name__ == '__main__':

	#Debugging Purpose Only

	Landi = Landi(token='token', HP='Phone', pin='pin', memberid='memberid', fixid='fixid')
	
	#trx = Landi.TrxDo('S20', '9676575476589089078978978797978', 'R2')

	#print(Landi.ss())
	#print(trx)
	#print(Landi.Find_Trx('TRX188475!2019-07-09!167875'))

	import time
	while 1:
		print(Landi.GetProfile())
		time.sleep(4)