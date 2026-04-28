# encoding: utf-8
from tools.log import log


class WorkFlow(object):
    """
    插件调度的进程池
    """
    pluginNames = []

    # 具体干活的worker 集合
    taskFuncs = dict()

    # 退出具体干活的worker 集合
    taskexitFuncs = dict()

    # worker 任务参数
    taskArges = dict()
    
    @staticmethod
    def registBus(pluginName, taskFunc, taskArges, taskexitFunc):
        """
        注册插件到工作流调度总线
        :param pluginName: 插件全局唯一的名称
        :param taskFunc: worker 具体干活的
        :param taskQueue: 任务队列(任务参数)
        :param taskexitFunc: 任务退出函数
        :return:
        """
        if not pluginName in WorkFlow.pluginNames:
            WorkFlow.taskFuncs[pluginName] = taskFunc
            WorkFlow.taskArges[pluginName] = taskArges
            WorkFlow.taskexitFuncs[pluginName] = taskexitFunc
            log.info("registered plugin: {} is successfully".format(pluginName))
            WorkFlow.pluginNames.append(pluginName)
        else:
            log.info("The plugin {} task already exists, please do not register again".format(pluginName))

    def __init__(self):
        pass
    
    def busStart(self):
        """
        启动所有已经注册的插件线进程
        :return:
        """
        count = len(WorkFlow.taskFuncs.keys())
        if count == 0:
            return
        from concurrent.futures import ProcessPoolExecutor
        pool = ProcessPoolExecutor(count)
        for k, func in WorkFlow.taskFuncs.items():
            taskArgs = WorkFlow.taskArges[k]
            pool.submit(func, *taskArgs)
            log.info("task:{} Submitted to the process pool".format(k))
        WorkFlow.taskFuncs.clear()
        WorkFlow.taskArges.clear()
    
    def onExit(self):
        """
        调用将所有已经注册的插件的退出函数，并关闭插件的输入、输出队列
        :return:
        """
        for k, exitfunc in WorkFlow.taskexitFuncs.items():
            exitfunc()
            log.info("task:{} Finished running".format(k))
            
    def plugin_exit(self, plugin_name):
        if plugin_name in WorkFlow.pluginNames:
            exitFunc = WorkFlow.taskexitFuncs[plugin_name]
            exitFunc()
            WorkFlow.taskexitFuncs.pop(plugin_name)
            log.info("插件{}已经正确的退出了".format(plugin_name))
            WorkFlow.pluginNames.remove(plugin_name)
        else:
            log.info(plugin_name)


workFlow = WorkFlow()
