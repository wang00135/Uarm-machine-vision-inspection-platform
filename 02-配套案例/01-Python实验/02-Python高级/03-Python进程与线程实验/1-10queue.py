from multiprocessing import Process, Queue
import os, time, random


# 写数据进程执行的代码：
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())


# 读数据进程执行的代码：
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)


if __name__ == '__main__':
    # 父进程创建出Queue，并传给各个子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入队列
    pw.start()
    # 启动子进程pr，读取队列
    pr.start()
    # 等待pw进程结束
    pw.join()
    # pr进程死循环，无法等待，只能强行终止;
    pr.terminate()
