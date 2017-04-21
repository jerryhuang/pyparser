#!/usr/bin/python

# This is a simple reader for hardware info collection.

import os, sys , csv

sys.path.append("lib");

from commonparser import *
from common import *

if len(sys.argv) > 2:
	logFolderPath = sys.argv[1]
	csvfilename = sys.argv[2]
else:
	exit(0)

logfolderReader = FolderReader()
logfolderReader.GetFolderName(logFolderPath)
sublogfolder = logfolderReader.GetRealFolderName()


# get dmidecode info

dmidecodeInfoReader = DmidecodeReader()
dmidecodeInfoReader.ReadFile(sublogfolder+'/dmidecode')
dmidecodeInfoReader.DataParse()
DmidecodeInfo = dmidecodeInfoReader.GetData()

# put data in table
InfoData = {}
for DmiInfo in DmidecodeInfo:
	if 'InfoName' in DmiInfo.keys():
		if DmiInfo['InfoName'] == "System Information":
			if not 'Platform' in InfoData.keys():
				InfoData['Platform'] = DmiInfo['Version']
			if not 'MTM' in InfoData.keys():
				InfoData['MTM'] = DmiInfo['Product Name']
			if not 'SN' in InfoData.keys():
				InfoData['SN'] = DmiInfo['Serial Number']
		if DmiInfo['InfoName'] == "Processor Information":
			if 'Version' in DmiInfo.keys() and not 'CPU' in InfoData.keys():
				InfoData['CPU'] = DmiInfo['Version']
		if DmiInfo['InfoName'] == "BIOS Information":
			if not 'BIOS' in InfoData.keys():
				InfoData['BIOS'] = DmiInfo['Version']

# get pci info

lspciInfoReader = PciInfoReader()
lspciInfoReader.ReadFile(sublogfolder+'/lspci')
lspciInfoReader.DataParse()
LspciInfo = lspciInfoReader.GetData()

#put data in lspci table
for lspcidata in LspciInfo:
	if 'PciDeviceType' in lspcidata.keys():
		# get graphic info 
		if 'VGA compatible controller' in lspcidata['PciDeviceType']:
			if not 'Graphic' in InfoData.keys():
				InfoData['Graphic'] = lspcidata['PciDevcieName']
			elif not lspcidata['PciDevcieName'] in InfoData['Graphic']:
				InfoData['Graphic'] += '\n+\n' + lspcidata['PciDevcieName']
			if not 'subGraphic' in InfoData.keys():
				InfoData['subGraphic'] = lspcidata['Subsystem']
			elif not lspcidata['Subsystem'] in InfoData['subGraphic']:
				InfoData['subGraphic'] += '\n+\n' + lspcidata['Subsystem']
		if '3D controller' in lspcidata['PciDeviceType']:
			if not 'Graphic' in InfoData.keys():
				InfoData['Graphic'] = lspcidata['PciDevcieName']
			elif not lspcidata['PciDevcieName'] in InfoData['Graphic']:
				InfoData['Graphic'] += '\n+\n' + lspcidata['PciDevcieName']
			if not 'subGraphic' in InfoData.keys() and 'Subsystem' in InfoData.keys():
				InfoData['subGraphic'] = lspcidata['Subsystem']
			elif 'Subsystem' in InfoData.keys() and not lspcidata['Subsystem'] in InfoData['subGraphic']:
				InfoData['subGraphic'] += '\n+\n' + lspcidata['Subsystem']
		if 'Display controller' in lspcidata['PciDeviceType']:
			if not 'Graphic' in InfoData.keys():
				InfoData['Graphic'] = lspcidata['PciDevcieName']
			elif not lspcidata['PciDevcieName'] in InfoData['Graphic']:
				InfoData['Graphic'] += '\n+\n' + lspcidata['PciDevcieName']
			if not 'subGraphic' in InfoData.keys() and 'Subsystem' in InfoData.keys():
				InfoData['subGraphic'] = lspcidata['Subsystem']
			elif 'Subsystem' in InfoData.keys() and not lspcidata['Subsystem'] in InfoData['subGraphic']:
				InfoData['subGraphic'] += '\n+\n' + lspcidata['Subsystem']
		# get Ethernet controller info
		if 'Ethernet controller' in lspcidata['PciDeviceType']:
			if not 'LAN' in InfoData.keys():
				InfoData['LAN'] = lspcidata['PciDevcieName'] + "\nSubsystem: " + lspcidata['Subsystem']
			elif not lspcidata['PciDevcieName'] in InfoData['LAN']:
				InfoData['LAN'] += '\n+\n' + lspcidata['PciDevcieName'] + "\nSubsystem: " + lspcidata['Subsystem']
		# get Audio device info
		if 'Audio device' in lspcidata['PciDeviceType']:
			if not 'Audio' in InfoData.keys():
				InfoData['Audio'] = lspcidata['PciDevcieName']
			elif not lspcidata['PciDevcieName'] in InfoData['Audio']:
				InfoData['Audio'] += '\n+\n' + lspcidata['PciDevcieName']

		# get WLAN info
		if 'Network controller' in lspcidata['PciDeviceType']:
			if not 'WLAN' in InfoData.keys():
				InfoData['WLAN'] = lspcidata['PciDevcieName'] + "\nSubsystem: " + lspcidata['Subsystem']
			elif not lspcidata['PciDevcieName'] in InfoData['WLAN']:
				InfoData['WLAN'] += '\n+\n' + lspcidata['PciDevcieName'] + "\nSubsystem: " + lspcidata['Subsystem']
		# get CardReader and Realtek LAN info 
		if 'Unassigned class' in lspcidata['PciDeviceType']:
			if 'Card Reader' in lspcidata['PciDevcieName']:
				if not 'CardReader' in InfoData.keys():
					InfoData['CardReader'] = lspcidata['PciDevcieName']
				elif not lspcidata['PciDevcieName'] in InfoData['CardReader']:
					InfoData['CardReader'] += '\n+\n' + lspcidata['PciDevcieName']
			elif 'Realtek' in lspcidata['PciDevcieName']:
				if not 'LAN' in InfoData.keys():
					InfoData['LAN'] = lspcidata['PciDevcieName'] + "\nSubsystem: " + lspcidata['Subsystem']
				elif not lspcidata['PciDevcieName'] in InfoData['LAN']:
					InfoData['LAN'] += '\n+\n' + lspcidata['PciDevcieName'] + "\nSubsystem: " + lspcidata['Subsystem']

# get lsusb info

lsusbInfoReader = UsbInfoReader()
lsusbInfoReader.ReadFile(sublogfolder+'/lsusb')
lsusbInfoReader.DataParse()
lsusbInfo = lsusbInfoReader.GetData()

# put data in table
for usbInfo in lsusbInfo:
	if 'UsbDevcieName' in usbInfo.keys():
		# get bluetooth info
		if 'Device Descriptor' in usbInfo.keys() and 'Bluetooth' in usbInfo['Device Descriptor']:
			if not 'Bluetooth' in InfoData.keys():
				InfoData['Bluetooth'] = usbInfo['UsbDevcieName']
		# get camera info
		if 'Device Descriptor' in usbInfo.keys() and 'Integrated Camera' in usbInfo['Device Descriptor']:
			if not 'Camera' in InfoData.keys():
				InfoData['Camera'] = usbInfo['UsbDevcieName']
			elif not usbInfo['UsbDevcieName'] in InfoData['Camera']:
				InfoData['Camera'] += usbInfo['UsbDevcieName']
		# get Fingerprint Reader info
		if 'Device Descriptor' in usbInfo.keys() and 'Validity Sensors' in usbInfo['Device Descriptor']:
			if not 'Fingerprint' in InfoData.keys():
				InfoData['Fingerprint'] = usbInfo['UsbDevcieName']
		# get TouchScreen info
		if 'Device Descriptor' in usbInfo.keys() and 'ouch' in usbInfo['Device Descriptor']:
			if not 'TouchScreen' in InfoData.keys():
				InfoData['TouchScreen'] = usbInfo['UsbDevcieName']
#print InfoData.keys()

printInfo = []
printInfo.append('RoW')
printInfo.append(' ')
printInfo.append('Lenovo')
printInfo.append('LCFC')
if 'Platform' in InfoData.keys():
	printInfo.append(InfoData['Platform'])
else:
	printInfo.append(' ')
printInfo.append(' ')
printInfo.append(' ')
printInfo.append(' ')
printInfo.append(' ')
printInfo.append('Notebook')
if 'SN' in InfoData.keys():
	printInfo.append(InfoData['SN'])
else:
	printInfo.append(' ')
if 'MTM' in InfoData.keys():
	printInfo.append(InfoData['MTM'])
else:
	printInfo.append(' ')

if 'BIOS' in InfoData.keys():
	printInfo.append(InfoData['BIOS'])
else:
	printInfo.append(' ')
printInfo.append(' ')
printInfo.append(' ')
printInfo.append(' ')
if 'CPU' in InfoData.keys():
	printInfo.append(InfoData['CPU'])
else:
	printInfo.append(' ')
if 'Graphic' in InfoData.keys():
	printInfo.append(InfoData['Graphic'])
else:
	printInfo.append(' ')
if 'subGraphic' in InfoData.keys():
	printInfo.append(InfoData['subGraphic'])
else:
	printInfo.append(' ')

if 'Audio' in InfoData.keys():
	printInfo.append(InfoData['Audio'])
else:
	printInfo.append(' ')
printInfo.append(' ')
printInfo.append(' ')
if 'LAN' in InfoData.keys():
	printInfo.append(InfoData['LAN'])
else:
	printInfo.append(' ')
printInfo.append(' ')
printInfo.append(' ')
printInfo.append(' ')
if 'WLAN' in InfoData.keys():
	printInfo.append(InfoData['WLAN'])
else:
	printInfo.append(' ')

printInfo.append(' ')
printInfo.append(' ')

if 'Bluetooth' in InfoData.keys():
	printInfo.append(InfoData['Bluetooth'])
else:
	printInfo.append(' ')

printInfo.append(' ')
printInfo.append(' ')

if 'Camera' in InfoData.keys():
	printInfo.append(InfoData['Camera'])
else:
	printInfo.append(' ')
if 'CardReader' in InfoData.keys():
	printInfo.append(InfoData['CardReader'])
else:
	printInfo.append(' ')

if 'Fingerprint' in InfoData.keys():
	printInfo.append(InfoData['Fingerprint'])
else:
	printInfo.append(' ')

printInfo.append(' ')

if 'TouchScreen' in InfoData.keys():
	printInfo.append(InfoData['TouchScreen'])
else:
	printInfo.append(' ')

#print printInfo
 

csvfullfilename = 'csv/' + csvfilename

if not os.path.exists(csvfullfilename):

	with open(csvfullfilename, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile,dialect='excel')
		for x in printInfo:
			spamwriter.writerow([x,])



