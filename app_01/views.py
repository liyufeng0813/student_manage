from django.shortcuts import render, redirect, HttpResponse
from django import views
from app_01 import models
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
import json
import os

from tools.pagination import PagerHelper


class Login(views.View):

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {'message': ''})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        c = models.Manager.objects.filter(username=username, password=password).count()
        if c != 0:
            request.session['is_login'] = True
            request.session['username'] = username
            request.session.set_expiry(0)
            return redirect('/index')
        return render(request, 'login.html', {'message': '用户名或密码错误！'})


def logout(request):
    request.session.clear()
    return redirect('/login')


def register(request):
    if request.method == "GET":
        return render(request, 'register.html', {'message': ''})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '' or models.Manager.objects.filter(username=username).count() !=0:
            return render(request, 'register.html', {'message': '用户名或者密码错误！'})
        else:
            models.Manager.objects.create(username=username, password=password)
            return render(request, 'register.html', {'message': '注册成功！'})
    else:
        return redirect('/index')


def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return inner


@auth
def index(request):
    username = request.session.get('username')
    if request.method == 'GET':
        return render(request, 'index.html', {'username': username})
    else:
        return redirect('/index')


@csrf_exempt
@auth
def classes(request):
    context = {}
    if request.method == 'GET':
        total_count = models.Classes.objects.all().count()
        pager_helper = PagerHelper(request, total_count, '/classes', 10)
        data = models.Classes.objects.all().order_by('id')[pager_helper.db_start:pager_helper.db_end]
        context['data'] = data
        pager = pager_helper.pager_str()
        context['pager'] = mark_safe(pager)
        username = request.session.get('username')
        context['username'] = username
        return render(request, 'classes.html', context)
    elif request.method == 'POST':
        resopnse_dict = {'status': True, 'message': None, 'data': None}
        caption = request.POST.get('caption', None)
        if caption is not None and models.Classes.objects.filter(caption=caption).count() == 0:
            obj = models.Classes.objects.create(caption=caption)
            resopnse_dict['message'] = '班级添加成功！'
            resopnse_dict['data'] = {'id': obj.id, 'caption': obj.caption}
        else:
            resopnse_dict['status'] = False
            resopnse_dict['message'] = '班级名不能为空，且该班级名已被占用！'
        return HttpResponse(json.dumps(resopnse_dict))
    else:
        return redirect('/index')


@csrf_exempt
@auth
def edit_classes(request):
    if request.method == 'GET':
        return redirect('/classes')
    elif request.method == 'POST':
        response_dic = {'status': True, 'message': None, 'data': None}
        caption = request.POST.get('caption')
        id = request.POST.get('id')
        if models.Classes.objects.filter(caption=caption).count() == 0:
            models.Classes.objects.filter(id=id).update(caption=caption)
            return HttpResponse(json.dumps(response_dic))
        else:
            response_dic['status'] = False
            response_dic['message'] = '用户名重复或不可为空！'
        return HttpResponse(json.dumps(response_dic))
    else:
        return redirect('/index')


@auth
def remove_classes(request):
    if request.method == 'GET':
        return redirect('/classes')
    elif request.method == 'POST':
        nid = request.POST.get('id')
        models.Classes.objects.filter(id=nid).delete()
        return HttpResponse('ok')
    else:
        return redirect('/index')


@csrf_exempt
@auth
def classes_add(request):
    message = ""
    if request.method == 'GET':
        return render(request, 'classes_add.html', {'message': message})
    elif request.method == 'POST':
        caption = request.POST.get('caption', None)
        if caption is not None and models.Classes.objects.filter(caption=caption).count() == 0:
            models.Classes.objects.create(caption=caption)
            return redirect('/classes')
        else:
            message = '班级名不可为空，或者班级名重复！'
            return render(request, 'classes_add.html', {'message': message})
    else:
        return redirect('/index')


@auth
def student(request):
    if request.method == 'GET':
        context = {}
        total_count = models.Student.objects.all().count()
        pager_helper = PagerHelper(request, total_count, '/student', 10)
        student_info = models.Student.objects.all().order_by('id')[pager_helper.db_start:pager_helper.db_end]
        context['student_info'] = student_info
        pager = pager_helper.pager_str()
        context['pager'] = mark_safe(pager)
        username = request.session.get('username')
        context['username'] = username
        class_info = models.Classes.objects.all()
        context['class_info'] = class_info
        return render(request, 'student.html', context)
    else:
        return redirect('/index')


def ValidateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@auth
def student_form_add(request):
    context = {}
    if request.method == 'GET':
        context['message'] = ''
        classes_data = models.Classes.objects.all()
        context['classes_data'] = classes_data
        return render(request, 'student_form_add.html', context)
    elif request.method == 'POST':
        name = request.POST.get('student_name', '').strip()
        email = request.POST.get('student_email', '').strip()
        cls_id = int(request.POST.get('cls'))
        c = models.Student.objects.filter(email=email).count()
        if name and email and ValidateEmail(email) and c == 0 and cls_id != 0:
            cls = models.Classes.objects.get(id=cls_id)
            models.Student.objects.create(name=name, email=email, cls=cls)
            return redirect('/student')
        else:
            return render(request, 'student_form_add.html', {'message': '选择一个班级、名字和邮箱不可为空或者邮箱存在或者邮箱格式不正确！'})
    else:
        return redirect('/index')


@auth
def student_ajax_add(request):
    if request.method == 'POST':
        response = {'status': True, 'message': '', 'data': ''}
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        cls = int(request.POST.get('cls'))
        c = models.Student.objects.filter(email=email).count()
        if name and ValidateEmail(email) and c == 0 and cls != 0:
            models.Student.objects.create(name=name, email=email, cls_id=cls)
            return HttpResponse(json.dumps(response))
        else:
            response['status'] = False
            response['message'] = '请正确输入姓名和邮箱地址以及选择班级，邮箱不可重复注册！'
            return HttpResponse(json.dumps(response))
    else:
        return redirect('/index')


@auth
def student_edit(request):
    if request.method == 'POST':
        response = {'status': True, 'message': '', 'data': ''}
        id = request.POST.get('id')
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        cls = int(request.POST.get('cls'))
        EMAIL = models.Student.objects.get(id=id).email
        if ValidateEmail(email):
            if EMAIL != email:
                c = models.Student.objects.filter(email=email).count()
                if c != 0:
                    response['status'] = False
                    response['message'] = '邮箱重复,请换个邮箱！'
                    return HttpResponse(json.dumps(response))
                else:
                    models.Student.objects.filter(id=id).update(name=name, email=email, cls_id=cls)
                    return HttpResponse(json.dumps(response))
            else:
                models.Student.objects.filter(id=id).update(name=name, email=email, cls_id=cls)
                return HttpResponse(json.dumps(response))
        else:
            response['status'] = False
            response['message'] = '输入规范的邮箱地址！'
            return HttpResponse(json.dumps(response))
    else:
        return redirect('/index')


@auth
def student_delete(request):
    if request.method == 'POST':
        response = {'status': True, 'message': '', 'data': ''}
        id = request.POST.get('id')
        models.Student.objects.filter(id=id).delete()
        return HttpResponse(json.dumps(response))
    else:
        return redirect('/index')


@auth
def student_detail(request):
    if request.method == 'GET':
        context = {}
        username = request.session.get('username')
        context['username'] = username
        sid = request.GET.get('sid', 0)
        if sid == 0:
            return redirect('/student')
        else:
            student_detail_info = models.Student.objects.get(id=sid)
            context['student_detail_info'] = student_detail_info
            return render(request, 'student_detail.html', context)
    else:
        return redirect('/index')



@auth
def teacher(request):
    if request.method == 'GET':
        context = {}
        username = request.session.get('username')
        context['username'] = username
        # 方式一: 模板渲染时要查数据库很多次，会降低性能。
        # teacher_info = models.Teacher.objects.all()
        # context['teacher_info'] = teacher_info
        #方式二： 对象的方式
        # class Node:
        #     def __init__(self, nid, name):
        #         self.nid = nid
        #         self.name = name
        #         self.cls_list = []
        #方式三：传字典，用values把值全取出来，做好处理传到模板渲染，这样对数据库的操作少。
        # teacher_list = models.Teacher.objects.filter(id__in=models.Teacher.objects.filter(id__in=range(5))).values('id', 'name', 'email', 'cls__id', 'cls__caption')
        teacher_list = models.Teacher.objects.filter(id__in=models.Teacher.objects.all()).values('id', 'name', 'email', 'cls__id', 'cls__caption')
        teacher_dict = {}
        for item in teacher_list:
            if item['id'] in teacher_dict:
                if item['cls__id']:
                    teacher_dict[item['id']]['cls_list'].append(
                        {'cls__id': item['cls__id'], 'cls__caption': item['cls__caption']})
            else:
                if item['cls__id']:
                    temp = [
                        {'cls__id': item['cls__id'], 'cls__caption': item['cls__caption']},
                    ]
                else:
                    temp = []
                teacher_dict[item['id']] = {
                    'nid': item['id'],
                    'name': item['name'],
                    'email': item['email'],
                    'cls_list': temp
                }
        context['teacher_dict'] = teacher_dict
        return render(request, 'teacher.html', context)


@auth
def teacher_form_add(request):
    context = {}
    if request.method == 'GET':
        class_info = models.Classes.objects.values('id', 'caption')
        context['class_info'] = class_info
        return render(request, 'teacher_form_add.html', context)
    elif request.method == 'POST':
        message = ""
        context['message'] = message
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        cls = request.POST.getlist('cls[]')
        c = models.Teacher.objects.filter(email=email).count()
        if name and ValidateEmail(email) and c==0:
            obj = models.Teacher.objects.create(name=name, email=email)
            obj.cls.add(*cls)
            return redirect('/teacher')
        else:
            message = '姓名和邮箱不可为空，邮箱不可重复！'
            context['message'] = message
            return render(request, 'teacher_form_add.html', context)
    else:
        return redirect('/index')


@auth
def teacher_form_edit(request, tid):
    context = {}
    if request.method == 'GET':
        teacher_info = models.Teacher.objects.filter(id=tid)[0]
        context['teacher_info'] = teacher_info
        class_all_info = models.Classes.objects.all()
        context['class_all_info'] = class_all_info
        class_id = models.Teacher.objects.filter(id=tid).values('cls__id')
        # 方式一：通过循环
        # class_id_list = []
        # for temp in class_id:
        #     class_id_list.append(temp.get('cls__id'))
        # 方式二：通过zip函数
        # class_id = models.Teacher.objects.filter(id=tid).values_list('cls__id')
        # class_id_tuple = list(zip(*class_id))[0]
        # 方式三：通过列表生成式
        class_id_list = [temp.get('cls__id') for temp in class_id]
        context['class_id_list'] = class_id_list
        return render(request, 'teacher_form_edit.html', context)
    elif request.method == 'POST':
        nid = request.POST.get('id')
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        cls = request.POST.getlist('cls[]')
        EMAIL = models.Teacher.objects.filter(id=nid)[0].email
        if EMAIL == email:
            if name:
                obj = models.Teacher.objects.filter(id=nid)
                obj.update(name=name, email=email)
                obj[0].cls.set(cls)
                return redirect('/teacher')
            else:
                context['message'] = '名字不可为空！'
                return render(request, 'teacher_form_edit.html', context)
        else:
            c = models.Teacher.objects.filter(email=email).count()
            if c == 0 and name and ValidateEmail(email):
                obj = models.Teacher.objects.create(name=name, email=email)
                obj.cls.set(cls)
                return redirect('/teacher')
            else:
                context['message'] = '用户名和邮箱不可为空且邮箱不可以重复！'
                return render(request, 'teacher_form_edit.html', context)
    else:
        return redirect('/teacher')


@auth
def teacher_ajax_delete(request):
    if request.method == 'POST':
        tid = request.POST.get('id')
        models.Teacher.objects.filter(id=tid).delete()
        return redirect('/teacher')
    else:
        return redirect('/index')


@auth
def upload(request):
    context = {}
    if request.method == 'GET':
        img_list = models.Img.objects.all().values('id', 'path')
        context['img_list'] = img_list
        return render(request, 'upload.html', context)
    elif request.method == 'POST':
        user = request.POST.get('user')
        file = request.FILES.get('file')
        file_path = os.path.join('static', 'upload', file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        models.Img.objects.create(path=file_path)
        return redirect('/upload')


@csrf_exempt
@auth
def upload_ajax(request):
    context = {}
    if request.method == 'GET':
        img_list = models.Img.objects.all().values('id', 'path')
        context['img_list'] = img_list
        return render(request, 'upload_ajax.html', context)
    elif request.method == 'POST':
        file = request.FILES.get('file')
        file_path = os.path.join('static', 'upload', file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        models.Img.objects.create(path=file_path)
        response = {'status': True, 'path': file_path}
        return HttpResponse(json.dumps(response))