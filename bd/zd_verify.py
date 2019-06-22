import sys
import time
import requests

if __name__ == '__main__':
	file_path = sys.argv[1]

	verified_domain_list, unverify_domain_list = [],[]
	with open("./domain_unverified/" + file_path, "r") as f:
		unverify_domain_list = f.readlines()

	result_file_name = "./domain_verified/file_"+time.strftime("%Y%m%d%H%M%S", time.localtime())
	with open(result_file_name, "w") as f:
		for ud in unverify_domain_list:
			f.write(ud.strip() + " teste test\n")

	post_url = ""
	
	d = {
		"time": time.time(),
		"id": sys.argv[1],
		"file_url":"http://localhost/domain_verified/" + result_file_name,
		"file_md5": 
	}