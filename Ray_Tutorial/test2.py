import ray
import time
import numpy as np

# 启动Ray.
ray.init()
#定义remote函数
@ray.remote
def sleep1(n):
    time.sleep(n)

#程序开始时的时间
time_start=time.time()

result_ids = []
i = 0
while i<100:
        #异步执行remote函数
    sleep1.remote(i)
    i = i+1
    print(i)    
#程序结束时系统时间
time_end=time.time()
#两者相减
print('totally cost',time_end-time_start)