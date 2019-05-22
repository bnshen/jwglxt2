from flask import Blueprint,request,jsonify
from utils import *
Public = Blueprint('Public', __name__)
from exts import cursor,db,mutex

@Public.route('/Semester', methods=['GET'])
def get_Semester():
    sql='select * from Semester'
    cursor.execute(sql)
    results = cursor.fetchall()
    tmp=[]
    for i in results:
        tmp.append(gen_Semester_dict(i))
    return jsonify(success_response(tmp))

def gen_Semester_dict(OpenC_list):
    info_name=['学期id','学期名','是否当前学期','是否可以选课']
    info_dict = dict()
    for i in range(len(info_name)):
        info_dict[info_name[i]] = OpenC_list[i]
    return info_dict

@Public.route('/Department',methods=['GET'])
def get_department():
    department_id=request.args.get('department_id','')+'%'
    sql = "select * from Department where id like '%s'"%department_id
    cursor.execute(sql)
    results = cursor.fetchall()
    tmp = []
    for i in results:
        tmp.append(gen_Department_dict(i))
    return jsonify(success_response(tmp))

def gen_Department_dict(OpenC_list):
    info_name=['department_id','department_no','department_name','department_address','department_tel']
    info_dict = dict()
    for i in range(len(info_name)):
        info_dict[info_name[i]] = OpenC_list[i]
    return info_dict

@Public.route('/Teacher',methods=['GET'])
def get_teacher():
    teacher_id=request.args.get('teacher_id',None)
    if not teacher_id:
        return jsonify(error_response(400,'lack of params'))
    sql = "select teacher_no,teacher_name,teacher_sex,teacher_education,department_name,teacher_workaddress" \
          " from Teacher left join Department on department_id=Department.id where Teacher.id= '%s'"%teacher_id
    # print(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    tmp = []
    for i in results:
        tmp.append(gen_Teacher_dict(i))
    return jsonify(success_response(tmp))

def gen_Teacher_dict(teacher_list):
    info_name=['teacher_no','teacher_name','teacher_sex','teacher_education','department_name','teacher_workaddress']
    info_dict = dict()
    for i in range(len(info_name)):
        info_dict[info_name[i]] = teacher_list[i]
    return info_dict

@Public.route('/Catagory',methods=['GET'])
def get_catagory():
    sql = "select id,catagory_name from Catagory where id in (2,3)"
    # print(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    tmp = []
    for i in results:
        tmp.append(gen_catagory_dict(i))
    return jsonify(success_response(tmp))

def gen_catagory_dict(teacher_list):
    info_name=['类别','类别名']
    info_dict = dict()
    for i in range(len(info_name)):
        info_dict[info_name[i]] = teacher_list[i]
    return info_dict

