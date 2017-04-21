
import os
class FolderReader(object):

	def __init__(self):
		self.folderName = ""
		self.SubFolderName = ""

	def GetFolderName(self,folderName):
		self.folderName = folderName

	def GetSubFolderName(self):
		if not os.path.exists(self.folderName + "/tmp"):
			return False
		folderlist = os.listdir(self.folderName + "/tmp")
		for x in folderlist:
			if 'sutton' in x:
				return x
		return False

	def CheckFilesExist(self):
		self.SubFolderName = self.GetSubFolderName()
		if self.SubFolderName:
			if not os.path.exists(self.folderName + "/tmp/" + self.SubFolderName + "/dmidecode"):
				return False
			if not os.path.exists(self.folderName + "/tmp/" + self.SubFolderName + "/lspci"):
				return False
			if not os.path.exists(self.folderName + "/tmp/" + self.SubFolderName + "/lsusb"):
				return False
			if not os.path.exists(self.folderName + "/tmp/" + self.SubFolderName + "/build-info-log"):
				return False
			if not os.path.exists(self.folderName + "/tmp/" + self.SubFolderName + "/running_dmesg"):
				return False
			return True
		return False

	def GetRealFolderName(self):
		if self.CheckFilesExist():
			return self.folderName + "/tmp/" + self.SubFolderName

