# -*- coding: utf-8 -*-
from concurrent.futures import ProcessPoolExecutor, as_completed


# 多进程，适用于cpu密集操作型任务，进程数依赖于cpu内核数，建议process_num不超过4
class MyProcessPool():
    def __init__(self, my_func, my_list, process_num=None,other_args=None):
        self.my_func = my_func
        self.my_list = my_list
        self.other_args = other_args
        self.result = []
        if process_num:
            self.process_num = process_num
        else:
            self.process_num = 2  # 默认进程数为2

    def start(self):
        with ProcessPoolExecutor(max_workers=self.process_num) as executor:
            if self.other_args != None:
                try:
                    all_task = [executor.submit(self.my_func,(test.strip()),(self.other_args)) for test in self.my_list]
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
                if data:
                    self.result.append(data)
                    if data == None:
                        pass
                    else:
                        self.result.append(data)



# def test_func(test,other_args):
#     print('get http://t00ls.net/{}'.format(test))
#     print('{} is {}'.format(test,other_args))
#
# test_list = str(range(1,9))
# process_num = 2
# other_args = 'sucess'
# myProcess = MyProcessPool(test_func,test_list,process_num=process_num,other_args=other_args)
# myProcess.start()