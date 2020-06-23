from init.init_imports import Infra



host = "http://10.97.252.12:5000"
url = "/webapi/auth.cgi"
gurl = "{}{}".format(host,url)
param = {
    "api":"SYNO.API.Auth",
    "method":"login",
    "version":"3",
    "account":"admin",
    "passwd":"Password123",
    "format":"cookie",
    "session":"FileStation"
}
data = Infra.get_wr(gurl,param).json()
is_success = data['success']
if is_success:
    data = data['data']
    sid = data['sid']
    print(sid)