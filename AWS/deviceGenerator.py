# # importing the requests library
import requests
import uuid

# # api-endpoint
for i in range(10):
    device_id = "dev_"+(uuid.uuid4().hex)
    user_id = "usr_"+(uuid.uuid4().hex)
    dev_list = open("E:/aeroasis/Embedded/device_list.txt", 'a')
    dev_list.write(device_id)
    dev_list.write('\n')
    dev_list.close()
    URL = "https://5nwvflntl1.execute-api.us-west-2.amazonaws.com/testing/?device_id=" + \
        device_id+"&device_type=aeroasis_device&user_id="+user_id

    # # defining a params dict for the parameters to be sent to the API
    PARAMS = None

    # # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # # extracting data in json format
    data = r.json()
    print(data)

    # print(data)

    cert = data['body']['certificate']
    priv = data['body']['privateKey']
    device_name = data['body']['thingName']

    fn_c = open("E:/aeroasis/keys/"+device_name+"_cert.pem", 'x')
    fn_c.write(cert)
    fn_c.close()

    fn_p = open("E:/aeroasis/keys/"+device_name+"_private.key", 'x')
    fn_p.write(priv)
    fn_p.close()
