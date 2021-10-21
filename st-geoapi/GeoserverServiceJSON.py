import requests

headers = {'Content-Type': 'application/json'}
auth = None
urlHttp = None


class GeoserverServiceJSON:
    def __init__(self, url, user, password):
        global auth
        global urlHttp
        auth = (user, password)
        urlHttp = url

    def postRequest(self, url, data):
        return requests.post(url, headers=headers, auth=auth, data=data)

    def getRequest(self, url):
        return requests.get(url, headers=headers, auth=auth)
