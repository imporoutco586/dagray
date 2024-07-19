import ray


@ray.remote(num_cpus=2, resources={'resources1': 1})
def func1():
    return 1


@ray.remote(num_cpus=0.5)
def func2():
    return 1

# 设置需要的自定义资源
@ray.remote(resources={'custom_parallelism': 1})
def func3():
    return 1

if __name__ == '__main__':
    ray.init()
    while 1:
        res1 = func1.remote()
        res2 = func2.remote()
        res3 = func3.remote()
    print(ray.get(res1))
    print(ray.get(res2))
    print(ray.get(res3))