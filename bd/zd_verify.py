import sys
import time
import requests

if __name__ == '__main__':
	file_path = sys.argv[1]

	verified_domain_list, unverify_domain_list = [],[]
	with open("./domain_unverified/" + file_path, "r") as f:
		unverify_domain_list = f.readlines()

	timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
	result_file_name = "./domain_verified/file_" + timestamp
	with open(result_file_name, "w") as f:
		for ud in unverify_domain_list:
			f.write(ud.strip() + " teste test\n")

	get_file_url = "http://localhost:8888/file"
	file_url = get_file_url + "/file_" + timestamp
	
	d = {
		"time": time.time(),
		"id": sys.argv[1],
		"file_url": file_url,
		"file_md5": "abcd "
	}

	print (file_url)
	print (file_url)
	print (file_url)	
	r = requests.post("http://10.245.146.207", json=d)