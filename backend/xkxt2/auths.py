import jwt, datetime, time
from settings import config
from utils import *
from exts import cursor,mutex
import datetime as dt
class Auth():
    @staticmethod
    def encode_auth_token(catagory_name,id,auth_dict):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2),
                'iat': datetime.datetime.utcnow(),
                'iss': 'DB XKXT',
                'data': {
                    'catagory_name': catagory_name,
                    'id':id,
                    'auth': auth_dict
                }
            }

            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:string
        :return: dict|string payload|error
        """
        try:
            payload = jwt.decode(auth_token, config.SECRET_KEY, leeway=datetime.timedelta(seconds=600))
            # 取消过期时间验证
            # payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': False})
            if ('data' in payload):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'


    def authenticate(self, user_id, PWSD):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param email:string
        :param password:string
        :return: dict
        """

        sql = "SELECT * FROM User where user_name='%s' and user_password='%s'" % (user_id, PWSD)
        try:
            mutex.acquire()
            cursor.execute(sql)
            results = cursor.fetchone()
            if results:
                sql = "SELECT * FROM Catagory where id='%s'"%(results[1])
                cursor.execute(sql)
                auth_results = cursor.fetchone()
                auth_dict=gen_auth_dict(auth_results[3:])
                print(auth_dict)
                catagory_name=auth_results[1]

                if catagory_name in ['Student','Teacher']:
                    sql = "SELECT * FROM %s left join (select id,department_name from Department) A " \
                          "on A.id=%s.department_id where %s.id='%s'"%(catagory_name,catagory_name,catagory_name,results[2])
                    print(sql)
                    cursor.execute(sql)
                    user_info_list=cursor.fetchone()
                    if catagory_name=="Student":
                        user_info_dict=gen_stu_info_dict(user_info_list[1:])
                    elif catagory_name=="Teacher":
                        user_info_dict=gen_teacher_info_dict(user_info_list[1:])
                else:
                    sql = "SELECT administor_no,administor_name,administor_sex FROM %s where id='%s'" % (
                          catagory_name, results[2])
                    print(sql)
                    cursor.execute(sql)
                    user_info_list = cursor.fetchone()
                    user_info_dict = gen_admin_info_dict(user_info_list)
                token=self.encode_auth_token(catagory_name,results[2],auth_dict)
                mutex.release()
                return success_response('登陆成功', {'token':token.decode(),'user_info':user_info_dict,'catagory_name':catagory_name})
            else:
                mutex.release()
        except Exception as e:
            mutex.release()
            print(e)
        return error_response(400,'登陆失败')



    def identify(self, request):
        """
        用户鉴权
        :return: dict
        """
        auth_token = request.headers.get('Authorization',None)
        if auth_token:
            payload_or_error = self.decode_auth_token(auth_token)
            if not isinstance(payload_or_error, str):
                return True,payload_or_error
            else:
                return False,"token错误"
        else:
            return False,'没有提供认证token'

def gen_auth_dict(auth_list):
    auth_name=['catagoty_authority_authority','catagoty_user_authority','catagoty_semester_authority',
               'catagoty_course_authority','catagoty_elective_authority','catagoty_grade_authority',
               'catagory_information_authority']
    auth_dict=dict()
    for i in range(len(auth_name)):
        auth_dict[auth_name[i]]=auth_list[i]

    return auth_dict

def gen_admin_info_dict(info_list):
    info_name=['administor_no','administor_name','administor_sex']
    info_dict=dict()
    for i in range(len(info_name)):
        info_dict[info_name[i]] = info_list[i]
    # print(info_dict)
    return info_dict

def gen_stu_info_dict(info_list):
    info_name=['student_no','student_name','student_sex','student_grade',
               'student_class','student_birthtime',
               'student_birthaddress','student_tel','student_user_id',
               'department_id','department_name']
    info_list=info_list[:8]+info_list[9:]
    info_dict=dict()
    for i in range(len(info_name)):
        if info_name[i]=='student_birthtime':
            info_dict[info_name[i]] = info_list[i].strftime("%Y-%m-%d")
            continue
        info_dict[info_name[i]] = info_list[i]
    # print(info_dict)
    return info_dict

def gen_teacher_info_dict(info_list):
    info_name=['teacher_no','teacher_name','teacher_sex','teacher_birthtime','teacher_education',
               'teacher_salary','teacher_department_id','teacher_workaddress','teacher_user_id']
    info_dict = dict()
    for i in range(len(info_name)):
        if info_name[i]=='teacher_birthtime':
            info_dict[info_name[i]] = info_list[i].strftime("%Y-%m-%d")
            continue
        info_dict[info_name[i]] = info_list[i]

    return info_dict


