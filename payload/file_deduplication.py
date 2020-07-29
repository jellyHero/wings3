from lib.code.deduplication import deduplication_list
from conf.conf import base_root
from lib.file.file_Class import readFile,writeFile


def file_dedu(target_file,result_file):
    test = readFile(target_file)
    test = deduplication_list(test)
    for i in test:
        writeFile(result_file,i)

if __name__ == '__main__':
    target_file = '{}payload/fuzz/all_fuzz.txt'.format(base_root)
    result_file = '{}payload/fuzz/all_fuzz1.txt'.format(base_root)
    file_dedu(target_file,result_file)