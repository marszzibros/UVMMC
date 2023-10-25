import time

start = time.time()

time.sleep(1)

end = time.time()
print(end - start)
print(int(12.111 // 1))
# 4200 / 3600  = 1.16 hours for gpu
# 42870 / 3600 = 11.9 hours for gpu