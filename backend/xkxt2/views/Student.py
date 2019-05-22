from flask import Blueprint,request,jsonify
from utils import *
from auths import Auth
Student = Blueprint('Student', __name__)
from exts import cursor,db,mutex
'''
    GET:获取已选课程
    POST:选课
    DELECT:退课
'''
@Student.route('/Elective', methods=['GET', 'POST', 'DELETE'])
def courses():
    payload_or_error = Auth.identify(Auth, request)
    if payload_or_error[0]:
        user_info = payload_or_error[1]['data']
        user_id=user_info['id']
        print(user_info)
        if not (user_info['auth']['catagoty_elective_authority']and user_info['catagory_name']=="Student"):
            return jsonify(error_response(403,"没有权限"))
    else:
        return jsonify(error_response(401,payload_or_error[1]))

    if request.method=='GET':
        sql = "select * from ((select OpenC.id,openc_time,openc_address,openc_curnum,openc_maxnum,openc_available,openc_QA_time,course_no,course_name," \
              "course_credit,course_hour,openc_teacher_id " \
              "from OpenC left join Course on openc_course_id=Course.id " \
              "where openc_semester_id=(select id from Semester where semester_available = true) and " \
              "OpenC.id in (select elective_openc_id from Elective where elective_student_id='%s'))A left join " \
              "(select id,teacher_name from Teacher )B on A.openc_teacher_id=B.id)"%(user_id)
        # print(sql)
        try:
            mutex.acquire()
            cursor.execute(sql)
            results = cursor.fetchall()
            mutex.release()
            tmp = []
            for i in results:
                tmp.append(gen_openC_dict(i))
            return jsonify(success_response('查询成功', {'Elective': tmp}))
        except Exception as e:
            mutex.release()
            print(e)

    ##判断是否可选课
    sql = "select * from Semester where semester_available=true and semester_able=true"
    mutex.acquire()
    cursor.execute(sql)
    result = cursor.fetchone()
    mutex.release()
    if not result:
        return jsonify(error_response(400,'选课时间未到。'))

    openc_id = request.form.get("openc_id", None)
    if not openc_id:
        return jsonify(error_response(400, 'lack of params'))
    if request.method=='POST':
        try:
            sql="select * from OpenC where id ='%s' and openc_curnum<openc_maxnum and openc_available=TRUE "%user_id
            mutex.acquire()
            cursor.execute(sql)
            flag=cursor.fetchone()
            if not flag:
                mutex.release()
                return jsonify(error_response(400,'选课失败，请确定课程处于能被选状态'))


            #查询是否已选此课程
            sql="select course_no from Course where id in (select openc_course_id from OpenC where id in " \
                "(select elective_openc_id from Elective where elective_student_id='%s') " \
                "and openc_semester_id in (select id from Semester where semester_available = true))"%(user_id)
            cursor.execute(sql)
            courses_no_tuple = cursor.fetchall()
            # print(courses_no_tuple)
            sql = "select course_no from Course where id in (select openc_course_id from OpenC where id = %s " \
                  "and openc_semester_id in (select id from Semester where semester_available = true))" % (openc_id)
            cursor.execute(sql)
            courses_no = cursor.fetchone()
            # print(courses_no)
            for i in courses_no_tuple:
                if i[0]==courses_no[0]:
                    mutex.release()
                    return jsonify(error_response(400,'已选此门课程'))

            #选课
            sql="INSERT INTO Elective(elective_student_id,elective_openc_id) values ('%s','%s') "%(user_id,openc_id)
            cursor.execute(sql)
            sql="update OpenC set openc_curnum=openc_curnum+1 where id='%s'"%(openc_id)
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('选课成功'))
        except Exception as e:
            mutex.release()
            print(e)

    if request.method=='DELETE':
        try:
            # 查询是否已选此课程
            sql="SELECT * from Elective left join OpenC on OpenC.id=elective_openc_id where openc_semester_id in (select id from Semester where semester_available = true) " \
                "and elective_student_id = '%s' and elective_openc_id = '%s'"%(user_id,openc_id)
            mutex.acquire()
            cursor.execute(sql)
            results = cursor.fetchone()
            if results==None:
                mutex.release()
                return jsonify(error_response(400,'未选此课程'))

            #退课
            sql="DELETE from Elective where elective_student_id='%s' and elective_openc_id='%s'" %(user_id,openc_id)
            cursor.execute(sql)
            sql = "update OpenC set openc_curnum=openc_curnum-1 where id='%s'" % (openc_id)
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('退课成功'))
        except Exception as e:
            mutex.release()
            print(e)
    return jsonify(error_response(400,'DB发生错误'))




'''
    获取成绩单
'''
@Student.route('/scores', methods=['GET'])
def get_personal_scores():
    payload_or_error = Auth.identify(Auth, request)
    if payload_or_error[0]:
        user_info = payload_or_error[1]['data']
        user_id=user_info['id']
        if not (user_info['auth']['catagory_information_authority'] and user_info['catagory_name']=="Student"):
            return jsonify(error_response(403,"没有权限"))
    else:
        return jsonify(error_response(401,payload_or_error[1]))
    try:
        sql="select course_no,course_name,elevtive_total_grade" \
            " from (((select elective_openc_id,elevtive_total_grade from Elective where elective_student_id='%s') A " \
            "left join OpenC on A.elective_openc_id=OpenC.id)" \
            "left join Course on openc_course_id=Course.id) "%user_id
        print(sql)
        mutex.acquire()
        cursor.execute(sql)
        results = cursor.fetchall()
        tmp=[]
        for i in results:
            tmp.append(gen_scores_dict(i))
        mutex.release()

        return jsonify(success_response('查询成功', {'scores': results}))
    except Exception as e:
        mutex.release()
        print(e)
    return jsonify(error_response(400,'DB发生错误'))



def gen_openC_dict(OpenC_list):
    info_name=['openc_id','openc_time','openc_address','openc_curnum','openc_maxnum','openc_available',
               'openc_QA_time','course_no','course_name','course_credit','course_hour','teacher_id','teacher_name']
    info_dict = dict()
    OpenC_list=OpenC_list[:11]+OpenC_list[12:]
    for i in range(len(info_name)):
        info_dict[info_name[i]] = OpenC_list[i]

    return info_dict


def gen_scores_dict(scores_list):
    info_name = ['course_no','course_name','elevtive_total_grade']
    info_dict = dict()
    for i in range(len(info_name)):
        info_dict[info_name[i]] = scores_list[i]

    return info_dict


