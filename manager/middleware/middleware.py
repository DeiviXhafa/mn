from django.http import JsonResponse
import json
from authentication.models import *
from externals import *
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
class UserAuthenticationMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        self.user=''
        self.valid_paths=['/robots.txt','/enterprise/login','/favicon.png','/testing','/','/authentication/','/favicon.ico','/privacy-policy','/ads.txt']
    def __call__(self,request):
        if check_link(request.path,self.valid_paths) and request.method=='POST':
            print(request.path)
            json_data=json.loads(request.body)
            if 'linker' in json_data:
                print('Json Data',json_data)
                linker=json_data['linker']
                if '=' in linker:
                    linker=linker[linker.find('ui=')+3:].split(' ')[0].replace(';','')
                if linker.startswith('bew'):
                    request.is_web=True
                    request.is_mobile=False
                else:
                    request.is_mobile=True
                    request.is_web=False
                print('Linkeri',linker)
                user=Users.objects.filter(linker=linker)
                print(user)
                if user:
                    request.user=user[0]
                    self.user=user[0]
                else:
                    self.user=None
                request.linker=linker
            else:
                print('Hereee')
                session_id=json_data.get('sessionid')
                if session_id:
                    session=Session.objects.get(session_key=session_id)
                    user_id=session.get_decoded().get('_auth_user_id')
                    user=User.objects.using('enterprise').get(pk=user_id)
                    print(user)
                    request.user=user
                    self.user=user
        response=self.get_response(request)
        return response
    def process_view(self,request,view_func,view_args,view_kwargs):
        if check_link(request.path,self.valid_paths):
            if not self.user and request.method=='POST':
                return JsonResponse({})
