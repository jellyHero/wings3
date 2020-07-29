# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor,as_completed

#多线程，适用于IO密集操作型任务，如网络请求,默认线程数为8
class MyThreadPool():
    def __init__(self, my_func, my_list, thread_num=None,other_args=None):
        self.my_func = my_func
        self.my_list = my_list
        self.other_args = other_args
        self.result = []
        if thread_num:
            self.thread_num = thread_num
        else:
            self.thread_num = 8 #默认线程数为8

    def start(self):
        with ThreadPoolExecutor(max_workers=self.thread_num) as executor:
            if self.other_args != None:
                try:
                    all_task = [executor.submit(self.my_func, (test.strip()),(self.other_args)) for test in self.my_list]
                except:
                    all_task = [executor.submit(self.my_func, (test), (self.other_args)) for test in self.my_list]
            else:
                try:
                    all_task = [executor.submit(self.my_func, (test.strip())) for test in self.my_list]
                except:
                    all_task = [executor.submit(self.my_func, (test)) for test in self.my_list]
            for future in as_completed(all_task):
                # pass
                data = future.result()
                if data == None:
                    pass
                else:
                    self.result.append(data)

# def test_func(test,other_args):
#     print('get http://t00ls.net/{}'.format(test))
#     print('{} is {}'.format(test,other_args))
#
# test_list = range(1,9)
# thread_num = 8
# other_args = 'sucess'
# MyThread = MyThreadPool(test_func,test_list,thread_num=thread_num,other_args=other_args)
# MyThread.start()