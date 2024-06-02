from django.apps import apps
from project.forms import *
def model2form(model):
    model_name=model
    if model_name.find('_')>-1:
        model_name=model.replace('_','')
    app_label='project'
    model=apps.get_model(app_label, model_name)
    model_form=create_model_form(model)
    return model_form,model
def modelname2object(model_name):
    if model_name.find('_')>-1:
        model_name=model.replace('_','')
    app_label='project'
    model=apps.get_model(app_label, model_name)
    return model
def status_update(status):
    switch={'To Do':'In Progress','In Progress':'Testing','Testing':'Done','Done':'Done'}
    return switch[status]
