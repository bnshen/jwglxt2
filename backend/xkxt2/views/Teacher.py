from flask import Blueprint,request,jsonify
from utils import *
from auths import Auth
Teacher = Blueprint('Teacher', __name__)
from exts import cursor,db,mutex


'''
    GET:获取自己这学期开课信息
'''
@Teacher.route('/courses', methods=['GET', 'POST', 'DELETE'])
def course():
    #鉴权
    payload_or_error = Auth.identify(Auth, request)
    if payload_or_error[0]:
        user_info = payload_or_error[1]['data']
        user_id=user_info['id']
        # print(user_info)
        if not user_info['catagory_name']=="Teacher":
            return jsonify(error_response(403,"没有权限"))
    else:
        return jsonify(error_response(401,payload_or_error[1]))
    if request.method=='GET':
        sql = "select * from ((select OpenC.id,openc_time,openc_address,openc_curnum,openc_maxnum,openc_QA_time,course_no,course_name," \
              "course_credit,course_hour,course_final_exam_precentage,openc_teacher_id,openc_semester_id " \
              "from OpenC  left join Course on openc_course_id=Course.id) A left join Semester on " \
              "A.openc_semester_id=Semester.id) where openc_teacher_id=%s order by semester_name" %user_id
        print(sql)
        try:
            mutex.acquire()
            cursor.execute(sql)
            results = cursor.fetchall()
            mutex.release()
            tmp = []
            for i in results:
                tmp.append(gen_openC_dict(i))
            return jsonify(success_response('查询成功', {'OpenC': tmp}))
        except Exception as e:
            mutex.release()
            print("Error: unable to fetch data")
    return jsonify(error_response(400,'DB发生错误'))

'''
    GET:获取对应课的学生的成绩
    PUT:输入成绩
'''
@Teacher.route('/courses/scores', methods=['GET', 'PUT'])
def scores():
    #鉴权
    payload_or_error = Auth.identify(Auth, request)
    if payload_or_error[0]:
        user_info = payload_or_error[1]['data']
        user_id = user_info['id']
        # print(user_info)
        if not user_info['catagory_name'] == "Teacher":
            return jsonify(error_response(403, "没有权限"))
    else:
        return jsonify(error_response(401, payload_or_error[1]))
    if request.method=='GET':
        openc_id=request.args.get('openc_id',None)
        if not openc_id:
            return jsonify(error_response(400, 'lack of params'))
        sql = "select * from ((select elective_student_id,id,elevtive_regular_grade,elevtive_final_exam_grade,elevtive_total_grade" \
              " from Elective where elective_openc_id = '%s')A " \
              "left join (select student_no,student_name,student_sex,student_grade,student_tel,id from Student) B " \
              "on B.id = A.elective_student_id) "%openc_id
        # print(sql)
        try:
            mutex.acquire()
            cursor.execute(sql)
            results = cursor.fetchall()
            tmp = []
            for i in results:
                tmp.append(gen_scores_dict(i))
            mutex.release()
            return jsonify(success_response('查询成功', {'scores': tmp}))
        except Exception as e:
            mutex.release()
            print(e)

    if  request.method=='PUT':
        _data = request.get_json()
        elective_id_list = _data.get("elective_id", None)
        elevtive_regular_grade_list = _data.get('elevtive_regular_grade', None)
        elevtive_final_exam_grade_list = _data.get('elevtive_final_exam_grade', None)
        if not (elective_id_list and elevtive_regular_grade_list and elevtive_final_exam_grade_list):
            return jsonify(error_response(400, 'lack of params'))
        try:
            mutex.acquire()
            for i in range(len(elective_id_list)):
            #查询该课程是否是自己开的
                sql="select openc_teacher_id from OpenC where id = " \
                    "(SELECT elective_openc_id from Elective where id='%s')"%(elective_id_list[i])
                cursor.execute(sql)
                results = cursor.fetchone()
                # print(results)
                if user_id!=results[0]:
                    mutex.release()
                    return jsonify(error_response(403,'没有权限'))
                sql="UPDATE Elective set elevtive_regular_grade=%s,elevtive_final_exam_grade=%s " \
                    "where id=%s"%(float(elevtive_regular_grade_list[i]),float(elevtive_final_exam_grade_list[i]),float(elective_id_list[i]))
                cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('输入成功'))
        except:
            mutex.release()
            print("Error: unable to fetch data")
    return jsonify(error_response('DB发生错误'))

def gen_openC_dict(OpenC_list):
    info_name=['openc_id','openc_time','openc_address','openc_curnum','openc_maxnum',
               'openc_QA_time','course_no','course_name','course_credit','course_hour','course_final_exam_precentage','semester_name']
    info_dict = dict()
    OpenC_list=OpenC_list[:11]+OpenC_list[14:15]
    # print(OpenC_list)
    for i in range(len(info_name)):
        info_dict[info_name[i]] = OpenC_list[i]

    return info_dict

def gen_scores_dict(scores_list):
    info_name=['elective_id','elevtive_regular_grade','elevtive_final_exam_grade','elevtive_total_grade',
               'student_no', 'student_name', 'student_sex', 'student_grade', 'student_tel']
    info_dict = dict()
    scores_list=scores_list[1:-1]
    print(scores_list)
    for i in range(len(info_name)):
        info_dict[info_name[i]] = scores_list[i]

    return info_dict

