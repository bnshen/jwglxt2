from flask import Blueprint,request,jsonify
from utils import *
from auths import Auth
Admin = Blueprint('Admin', __name__)
from exts import cursor,db,mutex
import datetime

'''
    GET:获取user信息
    POST:增加user
    DELETE:删除user
'''
@Admin.route('/userinfo',methods=['GET','POST','DELETE'])
def student_info():
    #鉴权
    payload_or_error = Auth.identify(Auth, request)
    if payload_or_error[0]:
        user_info = payload_or_error[1]['data']
        user_id = user_info['id']
        # print(user_info)
        if not user_info['catagory_name'] == "Administrator":
            return jsonify(error_response(403, "没有权限"))
    else:
        return jsonify(error_response(401, payload_or_error[1]))
    # 学号工号模糊查询
    if request.method=='GET':
        catagory_name = request.args.get('catagory_name', None)
        no = request.args.get('no', '')+'%'
        if not catagory_name and catagory_name not in ['Student','Teacher']:
            catagory_name='Student'
        if catagory_name=='Student':
            name='student_no'
        else:
            name='teacher_no'
        sql = "SELECT * FROM %s left join (select id,department_name from Department) A " \
              "on A.id=%s.department_id where %s.%s like '%s'" % (catagory_name, catagory_name, catagory_name,name, no)
        print(sql)
        try:
            mutex.acquire()
            cursor.execute(sql)
            results = cursor.fetchall()
            tmp=[]
            if catagory_name == "Student":
                for i in results:
                    user_info_dict = gen_stu_info_dict(i[1:])
                    tmp.append(user_info_dict)
            elif catagory_name == "Teacher":
                for i in results:
                    user_info_dict = gen_teacher_info_dict(i[1:])
                    tmp.append(user_info_dict)
            # print(tmp)
            mutex.release()
            return jsonify(success_response('查询成功', {'userinfo': tmp}))
        except Exception as e:
            mutex.release()
            print(e)
        return jsonify(error_response(400,'发生错误'))

    #新增教师学生
    if request.method == 'POST':
        catagory_id=int(request.form.get('catagory_id'))
        if not catagory_id:
            return jsonify(error_response(400,'lack of params'))
        elif catagory_id==2:#插入教师信息
            teacher_no = request.form.get("teacher_no", '')
            teacher_name = request.form.get("teacher_name", '')
            teacher_sex = request.form.get("teacher_sex", '')
            teacher_birthtime = request.form.get("teacher_birthtime", '')#形如1998-1-1
            teacher_education = request.form.get("teacher_education", '')
            teacher_salary = request.form.get("teacher_salary", '')
            department_id = request.form.get("department_id", '')
            teacher_workaddress = request.form.get("teacher_workaddress", '')
            password = request.form.get("password", '')

            try:
                # 查询是否有此工号
                sql = "SELECT * from Teacher where teacher_no='%s'" % teacher_no
                mutex.acquire()
                cursor.execute(sql)
                results = cursor.fetchone()
                if results != None:
                    return jsonify(error_response('400', '工号已存在'))
                sql = "INSERT INTO Teacher(teacher_no,teacher_name,teacher_sex,teacher_birthtime,teacher_education,teacher_salary,department_id,teacher_workaddress) " \
                      "values ('%s','%s','%s','%s','%s','%s','%s','%s') " % (
                    teacher_no, teacher_name, teacher_sex, teacher_birthtime,
                    teacher_education, teacher_salary,department_id,teacher_workaddress)
                print(sql)
                cursor.execute(sql)
                sql="insert into User(user_catagoty_id, user_catagoty_id_class_id, user_name, user_password) " \
                    "value ('%s','%s','%s','%s')"%(catagory_id,cursor.lastrowid,teacher_no,password)
                cursor.execute(sql)
                db.commit()
                mutex.release()
                return jsonify(success_response('新增成功'))
            except Exception as e:
                mutex.release()
                print(e)
        elif catagory_id==3:
            student_no = request.form.get("student_no", '')
            student_name = request.form.get('student_sex', '')
            student_sex = request.form.get('student_sex', '')
            student_grade = request.form.get('student_grade', '')
            student_class = request.form.get('student_class', '')
            student_birthtime = request.form.get('student_birthtime', '')
            student_birthaddress = request.form.get('student_birthaddress', '')
            student_tel = request.form.get('student_tel', '')
            department_id = request.form.get('department_id', '')
            password = request.form.get('password', '')

            try:
                # 查询是否有此工号
                sql = "SELECT * from Student where student_no='%s'" % student_no
                mutex.acquire()
                cursor.execute(sql)
                results = cursor.fetchone()
                if results != None:
                    return jsonify(error_response('400', '学号已存在'))
                sql = "INSERT INTO Student(student_no,student_name,student_sex,student_grade,student_class,student_birthtime," \
                      "student_birthaddress,student_tel,department_id) " \
                      "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (
                    student_no, student_name, student_sex, student_grade,
                    student_class, student_birthtime,student_birthaddress,student_tel,department_id)
                print(sql)
                cursor.execute(sql)
                sql="insert into User(user_catagoty_id, user_catagoty_id_class_id, user_name, user_password) " \
                    "value ('%s','%s','%s','%s')"%(catagory_id,cursor.lastrowid,student_no,password)
                cursor.execute(sql)
                db.commit()
                mutex.release()
                return jsonify(success_response('新增成功'))
            except Exception as e:
                mutex.release()
                print(e)
        else:
            return jsonify(error_response(400,'error params'))

    #删除用户
    if request.method == 'DELETE':
        no = request.form.get("no", None)
        catagory_id = request.form.get("catagory_id", None)
        if not (no and catagory_id):
            return jsonify(error_response(400,'lack of params'))
        try:
            if catagory_id==2:
                sql = "DELETE from Teacher where teacher_no='%s' " % no
            else:
                sql=  "DELETE from Student where student_no='%s' " % no
            mutex.acquire()
            cursor.execute(sql)
            sql="delete from User where user_name='%s'"%no
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('删除成功'))
        except Exception as e:
            mutex.release()
            print(e)
    return jsonify(error_response(400,'DB发生错误'))

'''
    GET:获取开课信息
    POST:开课
    DELETE:删课
'''
@Admin.route('/openc',methods=['GET','POST','DELETE'])
def openc():
    #鉴权
    payload_or_error = Auth.identify(Auth, request)
    if payload_or_error[0]:
        user_info = payload_or_error[1]['data']
        user_id = user_info['id']
        # print(user_info)
        if not user_info['catagory_name'] == "Administrator":
            return jsonify(error_response(403, "没有权限"))
    else:
        return jsonify(error_response(401, payload_or_error[1]))


    if request.method=='POST':
        course_id = request.form.get("course_id", None)
        teacher_id = request.form.get('teacher_id', '')
        openc_time = request.form.get('openc_time', '')
        openc_address = request.form.get('openc_address','')
        openc_maxnum = int(request.form.get('openc_maxnum', ''))
        openc_QA_time = request.form.get('openc_QA_time', '')
        openc_QA_address = request.form.get('openc_QA_address', '')

        try:
            mutex.acquire()
            # 获取当前学期id
            sql="SELECT id from Semester where semester_available=TRUE "
            cursor.execute(sql)
            semester_id = cursor.fetchone()[0]

            #开课
            sql="INSERT INTO OpenC(openc_course_id, openc_semester_id, openc_teacher_id, " \
                "openc_time,openc_address,openc_curnum, openc_maxnum, openc_available," \
                " openc_QA_time, openc_QA_address) values ('%s','%s','%s','%s','%s',%s,%s,'%s','%s','%s') "\
                %(course_id,semester_id,teacher_id,openc_time,openc_address,0,openc_maxnum,1,openc_QA_time,openc_QA_address)
            print(sql)
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('开课成功'))
        except Exception as e:
            mutex.release()
            print(e)

    if request.method=='DELETE':
        openc_id = request.form.get("openc_id", None)
        try:
            #删课
            sql="select * from Elective where elective_openc_id='%s'"%openc_id
            mutex.acquire()
            cursor.execute(sql)
            results = cursor.fetchone()
            if results:
                mutex.release()
                return jsonify(error_response('400', '存在已选此课的学生无法删除'))
            sql="DELETE from OpenC where id='%s'" %openc_id
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('删课成功'))
        except Exception as e:
            mutex.release()
            print(e)
    return jsonify(error_response(400,'DB发生错误'))

'''
    GET:获取开课信息
    POST:开课
    DELETE:删课
'''
@Admin.route('/courses',methods=['GET','POST','DELETE'])
def course():
    #鉴权
    payload_or_error = Auth.identify(Auth, request)
    if payload_or_error[0]:
        user_info = payload_or_error[1]['data']
        user_id = user_info['id']
        # print(user_info)
        if not user_info['catagory_name'] == "Administrator":
            return jsonify(error_response(403, "没有权限"))
    else:
        return jsonify(error_response(401, payload_or_error[1]))

    # 获取course
    if request.method == 'GET':
        course_no = request.args.get('course_no', '') + '%'
        try:
            mutex.acquire()
            sql = "select id,course_name,course_credit,course_hour,course_final_exam_precentage,course_catagory,course_no from Course where course_no like '%s'" % (
                course_no)
            cursor.execute(sql)
            results = cursor.fetchall()
            tmp = []
            for i in results:
                tmp.append(gen_course_info_dict(i))
            mutex.release()
            return jsonify(success_response('查询成功', {'courseinfo': tmp}))
        except Exception as e:
            mutex.release()
            print(e)

    if request.method == 'POST':
        course_no = request.form.get('course_no', '')
        course_name = request.form.get('course_name', '')
        course_credit = request.form.get('course_credit', '')
        course_hour = request.form.get('course_hour', '')
        department_id = request.form.get('department_id', '')
        course_final_exam_precentage = request.form.get('course_final_exam_precentage', '')
        course_grade = request.form.get('course_grade', '')
        course_catagory = request.form.get('course_catagory', '')
        try:
            mutex.acquire()
            sql = "select * from Course where course_no = '%s'" % (course_no)
            cursor.execute(sql)
            results = cursor.fetchone()
            if results:
                mutex.release()
                return jsonify(error_response('400', '课程号已存在'))
            sql = "insert into Course(course_name, course_credit, course_hour, course_department_id, " \
                  "course_final_exam_precentage, course_grade, course_catagory, course_no) " \
                  "values ('%s','%s','%s','%s','%s','%s','%s','%s')"\
                  %(course_name,course_credit,course_hour,department_id,course_final_exam_precentage,course_grade,course_catagory,course_no)
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('增加course成功'))
        except Exception as e:
            mutex.release()
            print(e)
    if request.method=="DELETE":
        course_id = request.form.get('course_id', '')
        try:
            mutex.acquire()
            sql = "select * from OpenC where openc_course_id = '%s'" % (course_id)
            cursor.execute(sql)
            results = cursor.fetchone()
            if results:
                mutex.release()
                return jsonify(error_response('400', '存在openc，该course不能删除'))
            sql = "delete from Course where id ='%s'"%course_id
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('删除course成功'))
        except Exception as e:
            mutex.release()
            print(e)
    return jsonify(error_response(400,'DB发生错误'))


@Admin.route('/semesters',methods=['POST','PUT','DELETE'])
def semester():
    #鉴权
    payload_or_error = Auth.identify(Auth, request)
    if payload_or_error[0]:
        user_info = payload_or_error[1]['data']
        user_id = user_info['id']
        # print(user_info)
        if not user_info['catagory_name'] == "Administrator":
            return jsonify(error_response(403, "没有权限"))
    else:
        return jsonify(error_response(401, payload_or_error[1]))

    if request.method=='POST':
        semester_name=request.form.get('semester_name',None)
        if not semester_name:
            return jsonify(error_response(400,'lack of params'))
        try:
            mutex.acquire()
            sql = "insert into Semester(semester_name, semester_available,semester_able)values ('%s',0,0)" % (semester_name)
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('增加semester成功'))
        except Exception as e:
            mutex.release()
            print(e)

    if request.method=='PUT':
        semester_id=request.form.get('semester_id',None)
        semester_name=request.form.get('semester_name','')
        semester_available=request.form.get('semester_available',0)
        semester_able=request.form.get('semester_able',0)

        if not semester_id:
            return jsonify(error_response(400,'lack of params'))
        try:
            mutex.acquire()
            sql = "update Semester set semester_name='%s',semester_available=%s,semester_able=%s where id=%s" % (semester_name,semester_available,semester_able,semester_id)
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('修改semester成功'))
        except Exception as e:
            mutex.release()
            print(e)

    if request.method=='DELETE':
        semester_id=request.form.get('semester_id',None)
        if not semester_id:
            return jsonify(error_response(400,'lack of params'))
        try:
            sql = "select * from OpenC where openc_semester_id = '%s'" % (int(semester_id))

            mutex.acquire()
            cursor.execute(sql)
            results = cursor.fetchone()
            if results:
                mutex.release()
                return jsonify(error_response('400', '存在openc，该semester不能删除'))
            sql = "delete from Semester where id='%s'" % (semester_id)
            cursor.execute(sql)
            db.commit()
            mutex.release()
            return jsonify(success_response('删除semester成功'))
        except Exception as e:
            mutex.release()
            print(e)
    return jsonify(error_response(400,'DB发生错误'))








def gen_stu_info_dict(info_list):
   # info_name=['student_no','student_name','student_sex','student_grade',
   #            'student_class','student_birthtime',
   #            'student_birthaddress','student_tel','student_user_id',
   #            'department_id','department_name']

    info_name=['学号','姓名','性别','入学年份',
            '班级','出生日期',
            '出生地','电话','user_id',
            '院系号','院系名']
    info_list=info_list[:8]+info_list[9:]
    info_dict=dict()
    for i in range(len(info_name)):
        if info_name[i]=='student_birthtime':
            info_dict[info_name[i]] = info_list[i].strftime("%Y-%m-%d")
            continue
        info_dict[info_name[i]] = info_list[i]
    print(info_dict)
    info_dict['catagory_id']=3
    return info_dict

def gen_teacher_info_dict(info_list):
    info_name=['教师号','教师名','性别','出生日期','学历',
               '薪资','院系号','办公室','教师登录名']
    info_dict = dict()
    for i in range(len(info_name)):
        if info_name[i]=='teacher_birthtime':
            info_dict[info_name[i]] = info_list[i].strftime("%Y-%m-%d")
            continue
        info_dict[info_name[i]] = info_list[i]
    info_dict['catagory_id']=2

    return info_dict

def gen_course_info_dict(info_list):
    info_name=['课程id','课程名','学分','学时','期末占比','类别','课程号']
    info_dict = dict()
    for i in range(len(info_name)):
        info_dict[info_name[i]] = info_list[i]
    return info_dict
