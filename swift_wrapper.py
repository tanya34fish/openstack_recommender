import swiftclient
import os

conn = swiftclient.Connection(
    user=os.environ['OS_USERNAME'],
    key=os.environ['OS_PASSWORD'],
    authurl=os.environ['OS_AUTH_URL'],
    tenant_name="hackthon6",
    auth_version="2.0"
)
def send(container_name,file):
    filename = file.name
    conn.put_object(container_name, filename, contents=file.read())

def upload_from_file(container_name, filename):
    with open(filename, 'r') as my_file:
        conn.put_object(container_name, filename, contents= my_file.read())

def download(container_name, filename):
    obj_tuple = conn.get_object(container_name, filename)
    with open(filename, 'w') as my_file:
        my_file.write(obj_tuple[1])

def updateMetaData(container_name, o, d):
    conn.post_object(container_name, o, headers=d)

def getMetaData(container_name, o):
    return conn.head_object(container_name, o)

def listObjects(container_name):
    return conn.get_container(container_name)[1]
