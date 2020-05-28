import os

from lib.file.file_Class import readFile,writeFile,getRemoveDupFile
from conf.conf import base_root

class PathPayload:
    #wordsFile:通用单词的文件
    # keyWords：额外添加的关键词列表，如ctf，flag等
    #Extension_AddList：需要扫描的后缀名列表
    #Extension_DelList：不需要扫描的后缀名列表
    def __init__(self,wordsFile=None,keyWords=None,Extension_AddList=None,Extension_DelList=None):
        # print(wordsFile)
        if wordsFile == None:
            self.wordsFile = '{}payload/dict/common-words.txt'
        else:
            self.wordsFile = wordsFile

        if keyWords == None:
            self.keyWords = []
        else:
            self.keyWords = keyWords

        if Extension_AddList == None:
            self.Extension_AddList = ['html','js']
        else:
            self.Extension_AddList = Extension_AddList

        if Extension_DelList == None:
            self.Extension_DelList = []
        else:
            self.Extension_DelList = Extension_DelList

        self.cachePath_txt = '{}payload/cache/path_payload.txt'.format(base_root)
        self.cacheFile_txt = '{}payload/cache/file_payload.txt'.format(base_root)


    #清理缓存文件
    def clearCacheTxt(self):
        try:
            os.remove(self.cachePath_txt)
            # os.remove('{}.rd'.format(self.cachePath_txt))
            os.remove(self.cacheFile_txt)
            # os.remove('{}.rd'.format(self.cacheFile_txt))
        except:
            pass

    #生成后缀名
    def getExtensionList(self):
        extensionList = set(self.Extension_AddList) - set(self.Extension_DelList)
        return list(extensionList)

    #创建缓存路径的txt文档
    def creatCachePathPayload(self):
        self.clearCacheTxt()
        extensionList = self.getExtensionList()

        #创建path缓存文件
        try:
            for fileName in readFile(self.wordsFile):
                writeFile(self.cachePath_txt, '{}\n'.format(fileName.strip()))
            for fileName in self.keyWords:
                writeFile(self.cachePath_txt, '{}\n'.format(fileName))
        except Exception as e:
            print(e)
            pass

        #创建file缓存文件
        try:
            for fileName in readFile(self.wordsFile):
                for exten in extensionList:
                    writeFile(self.cacheFile_txt, '{}.{}\n'.format(fileName.strip(), exten.strip()))
            for fileName in self.keyWords:
                for exten in extensionList:
                    writeFile(self.cacheFile_txt, '{}.{}\n'.format(fileName.strip(), exten.strip()))
        except Exception as e:
            print(e)
            pass

        getRemoveDupFile(self.cachePath_txt)
        getRemoveDupFile(self.cacheFile_txt)
        self.clearCacheTxt()
        os.system('mv {} {}'.format(self.cachePath_txt+'.rd',self.cachePath_txt))
        os.system('mv {} {}'.format(self.cacheFile_txt + '.rd', self.cacheFile_txt))

# if __name__=="__main__":
#     test_file = '{}payload/dict/common-words.txt'.format(base_root)
#     test = PathPayload(test_file)
#     test.creatCachePathPayload()
