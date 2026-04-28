import time
i = 0
while True:
    print(i)
    i = i+1
    time.sleep(1)
    if i == 5:
        continue
print("over")