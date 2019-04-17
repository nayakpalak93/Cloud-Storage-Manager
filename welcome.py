# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#reference: https://developer.ibm.com/recipes/tutorials/use-python-to-access-your-bluemix-object-storage/

import os
from flask import Flask, jsonify
import swiftclient
import keystoneclient
from flask import Flask, render_template, request, redirect
from flask import flash, request, session, abort, url_for

from simplecrypt import encrypt, decrypt

#from cryptography.fernet import Fernet
#key = Fernet.generate_key() 
#cipher_suite = Fernet(key)

app = Flask(__name__)

auth_url = "https://identity.open.softlayer.com/v3"
password = "cMWD2#(vSRV4QjMx"
project_id = "98307bd2334e451e98e5000a438b382d"
user_id = "39141b0011844c51898db7b084552de3"
region_name = "dallas"

conn = swiftclient.Connection(key=password,
authurl=auth_url,
auth_version='3',
os_options={"project_id": project_id,
"user_id": user_id,
"region_name": region_name})

container_name = 'PalakContainer'

# File name for testing
file_name = 'example_file.txt'

# Create a new container
conn.put_container(container_name)
print "nContainer %s created successfully." % container_name


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route("/upload", methods=['GET','POST'])
def upload():
    file_name = request.files['file_upload'].filename
    content=request.files['file_upload'].read()
    et = encrypt('1234567899999999', content)
    #encoded_text = cipher_suite.encrypt(b"%s" % content)
    #decryptedContent = cipher_suite.decrypt(encoded_text)
    conn.put_object(container_name,file_name,contents=et,content_type='text/plain')
    return '<h3>File Successfully created</h3>'

@app.route("/list", methods=['GET','POST'])
def List():  
	allFiles = ""   
        for container in conn.get_account()[1]:
		print '--->container'
		print container
                for data in conn.get_container(container['name'])[1]:
			print data
                        if not data:
                                allFiles = allFiles + "<i> No files are currently present on Cloud.</i>"
                        else:
                                allFiles = allFiles + "<li>" + 'File: {0}\t Size: {1}\t Date: {2}'.format(data['name'], data['bytes'], data['last_modified']) + "</li><br>"
        return '<h3>The files currently on cloud are </h3><br><br><ol>' + allFiles + '<br><form action="../"><input type="Submit" value="Back to Home Page"></form>'

@app.route("/delete", methods=['GET','POST'])
def delete():
	filename = request.form['filename']
	conn.delete_object(container_name, filename)
	print "nObject %s deleted successfully." % file_name
	return '<h3>The requested file has been deleted</h3>'

@app.route("/download", methods=['GET','POST'])
def download():
	filename = request.form['filedownload']
	obj = conn.get_object(container_name, filename)
	temp = str(obj[1])
	dt = decrypt('1234567899999999', obj[1])
	#decryptedContent = cipher_suite.decrypt(temp)
	f= open("Downloaded.txt","w+")
	f.write(dt)
	return "<h3>The requested file has been downloaded</h3>"

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)








