import sys
import time
import hashlib
import requests


#param: dest url, request id

def get_file_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == '__main__':
	file_path = sys.argv[1]

	verified_domain_list, unverify_domain_list = [],[]
	with open("./unverified_domain/" + file_path, "r") as f:
		unverify_domain_list = f.readlines()

	timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
	result_file_name = "./verified_domain/file_" + timestamp
	with open(result_file_name, "w") as f:
		for ud in unverify_domain_list:
			f.write(ud.strip() + " teste test\n")

	get_file_url = "http://localhost:8888/file"
	file_url = get_file_url + "/file_" + timestamp
	file_md5 = get_file_md5(result_file_name)
	
	d = {
		"time": time.time(),
		"id": sys.argv[1],
		"file_url": file_url,
		"file_md5": file_md5
	}

	print d
	print d
	r = requests.post("http://10.245.146.207", json=d)