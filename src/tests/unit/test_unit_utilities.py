#
#  Copyright (c) 2019-2020, ETH Zurich. All rights reserved.
#
#  Please, refer to the LICENSE file in the root directory.
#  SPDX-License-Identifier: BSD-3-Clause
#
import pytest
import requests
import os
from markers import host_environment_test


FIRECREST_IP = os.environ.get("FIRECREST_IP")
if FIRECREST_IP:
	UTILITIES_URL = os.environ.get("FIRECREST_IP") + "/utilities"
else:
    UTILITIES_URL = os.environ.get("UTILITIES_URL")


SERVER_UTILITIES = os.environ.get("SYSTEMS_PUBLIC").split(";")[0]

DATA = [ (SERVER_UTILITIES, 200) , ("someservernotavailable", 400)]  #ls, rename, chmod,chown, file, download,upload
DATA_201 = [ (SERVER_UTILITIES, 201) , ("someservernotavailable", 400)] #mkdir, symlink, 



# Test upload command
@pytest.mark.parametrize("machine, expected_response_code", DATA_201)
def test_upload(machine, expected_response_code, headers):
	data = {"targetPath": "/home/testuser/"}
	files = {'file': ('testsbatch.sh', open('testsbatch.sh', 'rb'))}
	url = "{}/upload".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.post(url, headers=headers, data=data, files=files)
	print(resp.json())
	assert resp.status_code == expected_response_code 


# Test exec file command on remote system
@pytest.mark.parametrize("machine, expected_response_code", DATA)
def test_file_type(machine, expected_response_code, headers):
	url = "{}/file".format(UTILITIES_URL)
	params = {"targetPath": ".bashrc"}
	headers.update({"X-Machine-Name": machine})
	resp = requests.get(url, headers=headers, params=params)
	print(resp.json())
	assert resp.status_code == expected_response_code  
	 

# Helper function to exec chmod
def exec_chmod(machine, headers, data):
	url = "{}/chmod".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.put(url, headers=headers, data=data)
	return resp


# Test chmod with valid arguments 
@pytest.mark.parametrize("machine, expected_response_code", DATA)
def test_chmod_valid_args(machine, expected_response_code, headers):
	data = {"targetPath": "testsbatch.sh", "mode" : "777"}
	resp = exec_chmod(machine, headers, data)
	#print(resp.json())
	assert resp.status_code == expected_response_code  


# Test chmod with invalid arguments 
@pytest.mark.parametrize("machine, expected_response_code", DATA)
def test_chmod_invalid_args(machine, expected_response_code, headers):
	data = {"targetPath": "testsbatch.sh", "mode" : "999"}
	resp = exec_chmod(machine, headers, data)
	print(resp.json())
	assert resp.status_code != 200



# Test chown method 
@pytest.mark.parametrize("machine, expected_response_code", DATA)
def test_chown(machine, expected_response_code, headers):
	data = {"targetPath": "/home/testuser/testsbatch.sh", "owner" : "testuser" , "group": "testuser"}
	url = "{}/chown".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.put(url, headers=headers, data=data)
	print(resp.json())
	assert resp.status_code == expected_response_code  

# Test ls command
@pytest.mark.parametrize("machine, expected_response_code", DATA)
def test_list_directory(machine, expected_response_code, headers):
	params = {"targetPath": "/home/testuser/", "showhidden" : "true"}
	url = "{}/ls".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.get(url, headers=headers, params=params)
	print(resp.json())
	assert resp.status_code == expected_response_code


# Test mkdir command
@pytest.mark.parametrize("machine, expected_response_code", DATA_201)
def test_make_directory(machine, expected_response_code, headers):
	data = {"targetPath": "/home/testuser/samplefolder/samplesubfolder", "p" : "true"}
	url = "{}/mkdir".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.post(url, headers=headers, data=data)
	print(resp.json())
	assert resp.status_code == expected_response_code  


# Test rename command
@pytest.mark.parametrize("machine, expected_response_code", DATA)
def test_rename(machine, expected_response_code, headers):
	data = {"sourcePath": "/home/testuser/samplefolder/", "targetPath" : "/home/testuser/sampleFolder/"}
	url = "{}/rename".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.put(url, headers=headers, data=data)
	print(resp.json())
	assert resp.status_code == expected_response_code  



# Test cp command
@pytest.mark.parametrize("machine, expected_response_code", DATA_201)
def test_copy(machine, expected_response_code, headers):
	data = {"sourcePath": "/home/testuser/sampleFolder", "targetPath" : "/home/testuser/sampleFoldercopy"}
	url = "{}/copy".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.post(url, headers=headers, data=data)
	print(resp.json())
	assert resp.status_code == expected_response_code  


# Test symlink command
@pytest.mark.parametrize("machine, expected_response_code", DATA_201)
def test_symlink(machine, expected_response_code, headers):
	data = {"targetPath": "/home/testuser/testsbatch.sh", "linkPath" : "/home/testuser/sampleFolder/testlink"}
	url = "{}/symlink".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.post(url, headers=headers, data=data)
	print(resp.json())
	print(machine)
	assert resp.status_code == expected_response_code


#  Test rm command: remove sampleFolder
# TODO: test file which doesn't exist (must return 400)
@pytest.mark.parametrize("machine, expected_response_code", [ (SERVER_UTILITIES, 204) , ("someservernotavailable", 400)])
def test_rm(machine, expected_response_code, headers):
	data = {"targetPath": "/home/testuser/sampleFolder/"}
	url = "{}/rm".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.delete(url, headers=headers, data=data)
	#print(resp.json())
	assert resp.status_code == expected_response_code 


# Test download command
@pytest.mark.parametrize("machine, expected_response_code", DATA)
def test_download(machine, expected_response_code, headers):
	params = {"sourcePath": "/home/testuser/testsbatch.sh"}
	url = "{}/download".format(UTILITIES_URL)
	headers.update({"X-Machine-Name": machine})
	resp = requests.get(url, headers=headers, params=params)
	assert resp.status_code == expected_response_code


# Test utilities microservice status
@host_environment_test
def test_status():
	url = "{}/status".format(UTILITIES_URL)
	resp = requests.get(url)
	assert resp.status_code == 200



if __name__ == '__main__':
	pytest.main()
