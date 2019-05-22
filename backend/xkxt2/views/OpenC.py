from flask import Blueprint,request,jsonify
from utils import *

C = Blueprint('OpenC', __name__)
from exts import cursor,mutex
'''
    GET:按条件检索所有课程
'''
@C.route('/query',methods=['GET'])
def query():
    if request.method=='GET':
        course_no=request.args.get('course_no','')+'%'
        course_name=request.args.get('course_name','')+'%'
        teacher_no=request.args.get('teacher_no','')+'%'
        teacher_name=request.args.get('teacher_name','')+'%'
        course_credit = request.args.get('course_credit', '')+'%'
        sql = "select OpenC.id,openc_time,openc_address,openc_curnum,openc_maxnum,openc_available,openc_QA_time,course_no,course_name," \
              "course_credit,course_hour " \
              "from OpenC left join Course on openc_course_id=Course.id " \
              "where openc_semester_id=(select id from Semester where semester_available = true) " \
              "and course_credit like '%s' "\
              "and openc_teacher_id in (select id from Teacher where teacher_no like '%s' and teacher_name like '%s')" \
              "and openc_course_id in (select id from Course where course_no like '%s' and course_name like '%s') " \
            %(course_credit,teacher_no,teacher_name,course_no,course_name)
        print(sql)
        try:
            # 执行SQL语句
            mutex.acquire()
            cursor.execute(sql)
            mutex.release()

            # 获取所有记录列表
            results = cursor.fetchall()
            tmp=[]
            for i in results:
                tmp.append(gen_openC_dict(i))
            return jsonify(success_response('查询成功', {'OpenC': tmp}))
        except:
            mutex.release()
            print("Error: unable to fetch data")
        return jsonify(error_response(400,'发生错误'))

def gen_openC_dict(OpenC_list):
    info_name=['开课id','开课时间','开课地点','当前人数','最大人数','是否可选',
               '答疑时间','课程号','课程名','学分','课时']
    info_dict = dict()
    for i in range(len(info_name)):
        info_dict[info_name[i]] = OpenC_list[i]

    return info_dict
