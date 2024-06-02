from django.shortcuts import render,redirect
from django.views import View
from externals import *
from project.models import *
class AddView(View):
    def get(self,request,model):
        model_form,model_object=model2form(model)
        return render(request,'add.html',{'form':model_form})
    def post(self,request,model):
        model_form,model_object=model2form(model)
        posted_data=dict(request.POST)
        del posted_data['csrfmiddlewaretoken']
        data={}
        for key in posted_data:
            final_value=posted_data[key][0]
            if key=='user':
                final_value=request.user
            elif key.endswith('_select'):
                key=key.replace('_select','')
                model_name=key.replace('_','')
                select_model_object=modelname2object(model_name)
                if final_value:
                    final_value=select_model_object.objects.get(id=final_value)
            data[key]=final_value
        model_object.objects.create(**data)
        return redirect(request.path)
class ReadView(View):
    def get(self,request,model):
        model_object=modelname2object(model)
        model_data=model_object.objects.all()
        keys=[]
        values=[]
        get_key=True
        for obj in model_data:
            obj_list = []
            val=[]
            for field in obj._meta.fields:
                if get_key:
                    keys.append(field.name)
                val.append(getattr(obj, field.name))
            get_key=False
            values.append(val)
        return render(request,'read.html',{'keys':keys,'values':values})
class TaskView(View):
    def get(self,request):
        user=request.user
        member=Member.objects.filter(user=request.user)
        member_type=member.member_type
        member_tasks=Task.objects.filter(member=member)
        member_type_tasks=Task.objects.filter(member_type=member_type).exclude(member=member)
        return render(request,'task.html',{'member_tasks':member_tasks,'member_type_tasks':member_type_tasks})
    def post(self,request):
        pass
class AddTaskView(View):
    def get(self,request):
        task_form=model2form('task')[0]
        return render(request,'add_task.html',{'task_form':task_form})
    def post(self,request):
        posted_data=request.POST
        name=posted_data['name']
        description=posted_data['description']
        project=Project.objects.get(id=posted_data['project'])
        deadline=posted_data['deadline']
        priority=Priority.objects.get(id=posted_data['priority'])
        member_type=MemberType.objects.get(id=posted_data['member_type'])
        task_status=TaskStatus.objects.get(name='To Do')
        Task.objects.create(name=name,description=description,user=request.user,project=project,deadline=deadline,priority=priority,member_type=member_type)
        return redirect(request.path)
class AddSubTaskView(View):
    def get(self,request,id):
        task_form=model2form('subtask')[0]
        return render(request,'add_subtask.html',{'task_form':task_form})
    def post(self,request,id):
        posted_data=request.POST
        name=posted_data['name']
        description=posted_data['description']
        task=Task.objects.get(id=id)
        deadline=posted_data['deadline']
        priority=Priority.objects.get(id=posted_data['priority'])
        member_type=MemberType.objects.get(id=posted_data['member_type'])
        task_status=TaskStatus.objects.get(name='To Do')
        SubTask.objects.create(subtask_status=task_status,name=name,description=description,submited_by=request.user,task=task,deadline=deadline,priority=priority,member_type=member_type)
        return redirect(request.path)
class ProjectView(View):
    def get(self,request):
        model_object=modelname2object('project')
        model_data=model_object.objects.all()
        keys=[]
        values=[]
        get_key=True
        for obj in model_data:
            obj_list = []
            val=[]
            for field in obj._meta.fields:
                if get_key:
                    keys.append(field.name)
                val.append(getattr(obj, field.name))
            get_key=False
            values.append(val)
        return render(request,'project.html',{'keys':keys,'values':values})
class ProjectTaskView(View):
    def get(self,request,id):
        user=request.user
        project=Project.objects.get(id=id)
        member=Member.objects.filter(user=user)
        if not member:
            tasks=Task.objects.filter(project=project)
        else:
            print('Memberat')
            tasks=Task.objects.filter(project=project,member_type=member[0].member_type)
        to_do_status=TaskStatus.objects.get(name='To Do')
        in_progress_status=TaskStatus.objects.get(name='In Progress')
        testing_status=TaskStatus.objects.get(name='Testing')
        done_status=TaskStatus.objects.get(name='Done')
        to_do_task=tasks.filter(task_status=to_do_status)
        in_progress_task=tasks.filter(task_status=in_progress_status)
        testing_task=tasks.filter(task_status=testing_status)
        done_task=tasks.filter(task_status=done_status)
        return render(request,'project_task.html',{'to_do_task':to_do_task,'in_progress_task':in_progress_task,'testing_task':testing_task,'done_task':done_task,'id':id})
    def post(self,request,id):
        user=request.user
        posted_data=request.POST
        task_id=posted_data['task_id']
        task=Task.objects.get(id=task_id)
        member_object=Member.objects.filter(user=user)
        if member_object:
            task.member=member_object[0]
            task_status=status_update(task.task_status.name)
            task_status_object=TaskStatus.objects.get(name=task_status)
            task.task_status=task_status_object
            task.save()
        return redirect(request.path)
class AddProjectTaskView(View):
    def get(self,request,id):
        task_form=model2form('task')[0]
        return render(request,'add_project_task.html',{'task_form':task_form,'id':id})
    def post(self,request,id):
        posted_data=request.POST
        name=posted_data['name']
        description=posted_data['description']
        project=Project.objects.get(id=id)
        deadline=posted_data['deadline']
        priority=Priority.objects.get(id=posted_data['priority'])
        member_type=MemberType.objects.get(id=posted_data['member_type'])
        task_status=TaskStatus.objects.get(name='To Do')
        Task.objects.create(task_status=task_status,name=name,description=description,user=request.user,project=project,deadline=deadline,priority=priority,member_type=member_type)
        return redirect(request.path)
class SubTaskView(View):
    def get(self,request,task_id):
        user=request.user
        member=Member.objects.filter(user=user)
        task=Task.objects.get(id=task_id)
        if not member:
            subtask=SubTask.objects.filter(task=task)
        else:
            subtask=SubTask.objects.filter(task=task,member_type=member[0].member_type)
        to_do_status=TaskStatus.objects.get(name='To Do')
        in_progress_status=TaskStatus.objects.get(name='In Progress')
        testing_status=TaskStatus.objects.get(name='Testing')
        done_status=TaskStatus.objects.get(name='Done')
        to_do_task=subtask.filter(subtask_status=to_do_status)
        in_progress_task=subtask.filter(subtask_status=in_progress_status)
        testing_task=subtask.filter(subtask_status=testing_status)
        done_task=subtask.filter(subtask_status=done_status)
        return render(request,'project_subtask.html',{'to_do_task':to_do_task,'in_progress_task':in_progress_task,'testing_task':testing_task,'done_task':done_task,'id':task_id})
    def post(self,request,task_id):
        user=request.user
        posted_data=request.POST
        task=SubTask.objects.get(id=task_id)
        member_object=Member.objects.get(user=user)
        task.member=member_object
        task_status=status_update(task.task_status.name)
        task_status_object=TaskStatus.objects.get(name=task_status)
        task.subtask_status=task_status_object
        task.save()
        return redirect(request.path)
class SubTaskIDView(View):
    def get(self,request,id):
        subtask_object=SubTask.objects.get(id=id)
        sub_task_comment=SubTaskComment.objects.filter(task=subtask_object)
        return render(request,'subtask_view.property.html',{'sub_task_comment':sub_task_comment,'subtask':subtask_object})
    def post(self,request,id):
        posted_data=request.POST
        user=request.user
        task=SubTask.objects.get(id=id)
        comment=posted_data['comment']
        SubTaskComment.objects.create(user=user,task=task,comment=comment)
        return redirect(request.path)
class TaskIDView(View):
    def get(self,request,id):
        task_object=Task.objects.get(id=id)
        task_comment=TaskComment.objects.filter(task=task_object)
        return render(request,'task_view.property.html',{'task_comment':task_comment,'task':task_object})
    def post(self,request,id):
        posted_data=request.POST
        user=request.user
        task=Task.objects.get(id=id)
        comment=posted_data['comment']
        TaskComment.objects.create(user=user,task=task,comment=comment)
        return redirect(request.path)
class EditSubTaskView(View):
    def get(self,request,id):
        subtask=SubTask.objects.get(id=id)
        priorities=Priority.objects.all()
        member_types=MemberType.objects.all()
        return render(request,'edit_subtask.html',{'subtask':subtask,'priorities':priorities,'member_types':member_types})
    def post(self,request,id):
        posted_data=request.POST
        name=posted_data['name']
        description=posted_data['description']
        task=SubTask.objects.get(id=id)
        deadline=posted_data['deadline']
        priority=Priority.objects.get(id=posted_data['priority'])
        member_type=MemberType.objects.get(id=posted_data['member_type'])
        task_status=TaskStatus.objects.get(name='To Do')
        SubTask.save(subtask_status=task_status,name=name,description=description,submited_by=request.user,deadline=deadline,priority=priority,member_type=member_type)
        return redirect(request.path)
