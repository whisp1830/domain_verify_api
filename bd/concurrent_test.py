import os
for i in range(100):
	os.system("nohup python mono.py 3000%s baidu_%s.txt &"%(i+1,i+1))
