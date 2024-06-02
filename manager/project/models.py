from django.db import models
from django.contrib.auth.models import User
class MemberType(models.Model):
    name=models.CharField(max_length=40)
    def __str__(self):
        return self.name
class Member(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_active':True,'is_staff':True,'is_superuser':False})
    member_type=models.ForeignKey(MemberType,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)
class Client(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_active':True,'is_staff':False,'is_superuser':False})
    def __str__(self):
        return str(self.user)
class Project(models.Model):
    name=models.CharField(max_length=50,unique=True)
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    cost=models.PositiveIntegerField(default=0)
    deadline=models.DateField(null=True)
    def __str__(self):
        return self.name
class Priority(models.Model):
    name=models.CharField(max_length=30)
    def __str__(self):
        return self.name
class TaskStatus(models.Model):
    name=models.CharField(max_length=40,unique=True)
    def __str__(self):
        return self.name
class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    task_status=models.ForeignKey(TaskStatus,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=30)
    description=models.CharField(max_length=400,null=True)
    deadline=models.DateField(null=True)
    priority=models.ForeignKey(Priority,on_delete=models.CASCADE)
    submited=models.DateTimeField(auto_now=True)
    member=models.ForeignKey(Member,on_delete=models.CASCADE,null=True,blank=True)
    member_type=models.ForeignKey(MemberType,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name
class SubTask(models.Model):
    submited_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    task=models.ForeignKey(Task,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=30)
    description=models.CharField(max_length=400,null=True)
    deadline=models.DateField(null=True)
    priority=models.ForeignKey(Priority,on_delete=models.CASCADE)
    submited=models.DateTimeField(auto_now=True)
    member=models.ForeignKey(Member,on_delete=models.CASCADE,null=True)
    subtask_status=models.ForeignKey(TaskStatus,on_delete=models.CASCADE,null=True)
    member_type=models.ForeignKey(MemberType,on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.name
class TaskComment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    task=models.ForeignKey(Task,on_delete=models.CASCADE)
    comment=models.CharField(max_length=400)
    submited=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)
class SubTaskComment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    task=models.ForeignKey(SubTask,on_delete=models.CASCADE)
    comment=models.CharField(max_length=400)
    submited=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)
