import time;  # 引入time模块
ticks = time.time()
print ("当前时间戳为:", ticks)


import time
# 格式化成2018-12-8 15:26:39形式
print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 
 
# 格式化成Sat Dec 08 15:26:26 2018形式
print (time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())) 
  
# 将格式字符串转换为时间戳
a = "Sat Dec 08 15:26:26 2018"
print (time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y")))
