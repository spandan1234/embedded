# # importing the requests library
# import requests

# # api-endpoint


# # defining a params dict for the parameters to be sent to the API
# PARAMS = None

# # sending get request and saving the response as response object
# r = requests.get(url = URL, params = PARAMS)

# # extracting data in json format
# data = r.json()
# print(data)

# print(data)

cert = data['body']['certificate']
priv = data['body']['privateKey']
device_name = data['body']['thingName']

fn_c = open(device_name+"_cert.pem", 'x')
fn_c.write(cert)
fn_c.close()


fn_p = open(device_name+"_private.key", 'x')
fn_p.write(priv)
fn_p.close()
