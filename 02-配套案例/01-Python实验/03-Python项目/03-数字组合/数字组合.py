num1  =  input ( '请输入0-9之间任意一个或多个数字：' )
num2  =  input ( '请再次输入0-9之间任意一个或多个数字：' )
def  account(num1,num2):
     print ( "两次输入数字的组合即将开始" )
     list1  =  [(x,y)  for  x  in  num1  for  y  in  num2 ]
     num3  =  []
     for  list2  in  list1:
         print (''.join([ str (x)  for  x  in  list2]))
         num3.append(''.join([ str (x)  for  x  in  list2]))
     print ( "组合完成，共有"  +  str ( len (num3))  +  "对组合！" )
account(num1,num2)