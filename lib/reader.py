# Reader is for file reading and simple parsing.

import os

class Reader(object):

    def __init__(self):
        self.filename =  None
        self.stream = None
        self.eof = True
        self.buffer = u""
        self.paragraphs = []
        self.useful_contents = []
        self.final_data = []
        self.split_tag = "\t"
        self.print_onetime_flag = False

    def print_log_onetime(self,log_content):
        if not self.print_onetime_flag:
            print log_content
            self.print_onetime_flag = True

    def find_str_tag_num_start(self,str):
        count = 0
        new_str = str[:]
        while new_str.startswith(self.split_tag):
            new_str = new_str[len(self.split_tag):]
            count = count +1
        return count

    def ReadFile(self,filename):
        if os.path.exists(filename):
            self.filename = filename
            with open(self.filename) as file:
                self.stream = file.read()

    def ParagraphSplit(self):
        if self.stream:
            contents = self.stream.split('\n\n')
            self.paragraphs = [content for content in contents if content]

    def GetUsefulContents(self):
        self.useful_contents = self.paragraphs[:]

    def SpecialFilter(self,sentences):
        return sentences,{}

    def ParagraphParse(self,paragraph_content):
        if paragraph_content:
            new_paragraph_content,SpecialFilterData = self.SpecialFilter(paragraph_content)

            if  SpecialFilterData:
                new_info_dict = SpecialFilterData
            else:
                new_info_dict = {}

            content_sentences = new_paragraph_content.split('\n')
            info_list = []
            across_rows_flag = False
            for  sentence in content_sentences:
                if self.find_str_tag_num_start(sentence) == 1:
                    across_rows_flag = False
                if sentence.endswith(':'):
                    across_rows_flag = True
                if not across_rows_flag or sentence.endswith(':'):
                    if sentence.find(':'):
                        pointer = sentence.find(':')
                        name = sentence[:pointer].strip('\t').strip(' ')
                        value = sentence[pointer+1:].lstrip(' ')
                        info_dict = {'name':name,'value':value}
                        info_list.append(info_dict)
                else:
                    info_dict = info_list[len(info_list)-1]
                    info_dict['value'] = info_dict['value']+sentence

            for info in info_list:
                new_info_dict[info['name']] = info['value']
            return new_info_dict
        else:
            return {}

    def  DataParse(self):
        self.ParagraphSplit()
        self.GetUsefulContents()
        for useful_content in self.useful_contents:
            info_dict = self.ParagraphParse(useful_content)
            self.final_data.append(info_dict)

    def GetData(self):
        self.DataParse()
        return self.final_data


class DmidecodeReader(Reader):

    def __init__(self):
        Reader.__init__(self)

    def GetUsefulContents(self):
        if self.paragraphs and len(self.paragraphs) >2:
            para_counts = len(self.paragraphs)
            self.useful_contents = [self.paragraphs[i] for i in range(1,para_counts-1)]

    def SpecialFilter(self,sentences):
        count = 2
        SpecialFilterData = {}
        while count > 0:
            if sentences.find('\n'):
                if count == 2:
                    SpecialFilterData['HandleDMIInfo'] = sentences[:sentences.find('\n')]
                if count == 1:
                    SpecialFilterData['InfoName'] = sentences[:sentences.find('\n')]
                sentences = sentences[sentences.find('\n')+1:]
            count = count-1
        return sentences,SpecialFilterData

class PciInfoReader(Reader):

    def __init__(self):
        Reader.__init__(self)

    def DeviceNameParser(self,sentence):
        # 00:1d.0 PCI bridge [0604]: Intel Corporation Device [8086:9d18] (rev f1) (prog-if 00 [Normal decode])
        DeviceNameInfo = {}
        sentence = sentence[sentence.find(' '):].strip(' ')
        if sentence.find(':'):
            TypeWords = sentence[:sentence.find(':')]
            DeviceName = sentence[sentence.find(':')+1:].strip(' ')
            if TypeWords.find(' '):
                TypeWords = TypeWords[TypeWords.find(' '):].strip(' ')
            if TypeWords.find('['):
                TypeWords = TypeWords[:TypeWords.find('[')].strip(' ')
            DeviceNameInfo['PciDeviceType'] = TypeWords
            DeviceNameInfo['PciDevcieName'] = DeviceName
        return DeviceNameInfo

    def SpecialFilter(self,sentences):
        count = 1
        SpecialFilterData = {}
        while count > 0:
            if sentences.find('\n'):
                SpecialFilterData = self.DeviceNameParser(sentences[:sentences.find('\n')])
                sentences = sentences[sentences.find('\n')+1:]
            count = count-1
        return sentences,SpecialFilterData

class UsbInfoReader(Reader):

    def __init__(self):
        Reader.__init__(self)

    def DeviceNameParser(self,sentence):
        # Bus 002 Device 002: ID 0781:5581 SanDisk Corp. 
        DeviceNameInfo = {}
        if sentence.find(':'):
            DeviceName = sentence[sentence.find(':')+1:].strip(' ')
            DeviceNameInfo['UsbDevcieName'] = DeviceName
        return DeviceNameInfo

    def SpecialFilter(self,sentences):
        count = 1
        SpecialFilterData = {}
        sentences = sentences.strip('\n')
        while count > 0:
            if sentences.find('\n'):
                SpecialFilterData = self.DeviceNameParser(sentences[:sentences.find('\n')])
                sentences = sentences[sentences.find('\n')+1:]
            count = count-1
        return sentences,SpecialFilterData


a = UsbInfoReader()
a.ReadFile('./lsusb')
a.DataParse()
b = a.GetData()
print b[0].keys()

'''a = PciInfoReader()
a.ReadFile('./lspci')
a.DataParse()
b = a.GetData()
print b[0].keys()
'''