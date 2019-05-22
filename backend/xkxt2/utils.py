def error_response(status,msg,data = None):
    if data is None:
        data={}
    temp = {'status':status,'msg':msg,'data':data}
    return temp

def success_response(msg,data = None):
    if data is None:
        data={}
    temp = {'status':200,'msg':msg,'data':data}
    return temp
