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
    info_name=['semester_id','semester_name','semester_available','semester_able']
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
        sql = "select Teacher.id,teacher_no,teacher_name,teacher_sex,teacher_education,department_name,teacher_workaddress" \
              " from Teacher left join Department on department_id=Department.id"
        cursor.execute(sql)
        results=cursor.fetchall()
        tmp = []
        for i in results:
            tmp.append(gen_Teacher_dict1(i))
        return jsonify(success_response(200,tmp))
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

def gen_Teacher_dict1(teacher_list):
    info_name=['teacher_id','teacher_no','teacher_name','teacher_sex','teacher_education','department_name','teacher_workaddress']
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
    info_name=['catagory_id','catagory_name']
    info_dict = dict()
    for i in range(len(info_name)):
        info_dict[info_name[i]] = teacher_list[i]
    return info_dict

