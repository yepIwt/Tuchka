import os

class withfolder(object):

	__slots__ = ('local','tree_local','start')
	
	def __init__(self,dir):
		self.start = os.getcwd()
		self.local = dir
		try:
			os.chdir(self.local)
		except:
			raise FileNotFoundError('Can\'t find this dir')
	
	def move(self,where):  #Never use that
		if where == 'back':
			os.chdir(self.start)
		if where == 'home':
			os.chdir(self.local)

	def download_folder(self,objected):
		self.move('home')
		os.mkdir(self.wee('name', objected))
		os.chdir(self.wee('name', objected))

	def maketree(self,dir=None):
		if not dir:
			dir = self.local
		tmp = []
		for elem in os.walk(dir):
			tmp.append(elem)
		return tmp

	def check_folders_from_cloud(self,netfolders):
		tree = self.maketree()
		gotcha = list(set(set(tree[0][1]) ^ set(self.wee('name2',netfolders))))
		for caught in gotcha:
			if caught in tree[0][1]:
				print('There is no',caught,'in cloud')
				print('Wanna create that on cloud?(y/n)')
				if input() == 'y':
					self.new_folder(str(caught))
			else:
				print('There is no',caught,'in local machine') ## working if u add in cfgs
				print('Wanna donwload this?(y/n)')
				if input() == 'y':
					self.download_folder(caught)

	def check_files_from_cloud(self,netfolders:list): #First you have to sync folder
		tree = self.maketree()
		for folder in tree[0][1]:
			for i in range(len(netfolders)):
				if folder == self.wee('name',netfolders[i]): #Нашли папку
					for gotcha in list(set(set(os.listdir(folder)) ^ set(self.wee('files',netfolders[i])))):
						if gotcha in netfolders[i][1]:
							print(gotcha,'in', folder, '- add,but only in internet')
						else:
							print(gotcha, 'in', folder, '-add, but only in local')
