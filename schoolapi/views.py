from django.shortcuts import redirect

from .serializers import StudentDetails, StudentSerializerMain
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from .models import Student,Teacher,Principal,User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.response import Response
from .serializers import TeacherSerializerMain, TeacherDetails,PrincipalDetails,\
    PrincipalSerializerMain
from django.conf import settings
from django.core.mail import send_mail
from uuid import uuid4

class Teacher_List_view(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherDetails
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer_class = TeacherSerializerMain(data=data)

        if serializer_class.is_valid():
            teacher = serializer_class.save(serializer_class.data)
            new_mail = data['email']
            my_token = Token.objects.create(user=teacher.user)

            send_after_registration(new_mail, my_token)
            return Response(TeacherDetails(teacher).data, status=200)
        else:
            return Response(serializer_class.errors)

    def partial_update(self, request, *args, **kwargs):
        teacher_obj=self.get_queryset()[0]
        data=request.data
        if "first_name" in data:
            teacher_obj.user.first_name = data["first_name"]
        if "last_name" in data:
            teacher_obj.user.last_name = data["last_name"]
        if "primary_subject" in data:
            teacher_obj.primary_subject = data["primary_subject"]
        if "secondary_subject" in data:
            teacher_obj.secondary_subject = data["secondary_subject"]
        teacher_obj.save()
        return Response(TeacherDetails(teacher_obj).data, status=200)

    def destroy(self,request,*args,**kwargs):
        teacher_obj = self.get_queryset()[0]
        teacher_obj.user.delete()
        return Response("deleted")

class Student_List_view(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentDetails
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        print(data["email"])
        serializer_class = StudentSerializerMain(data=data)

        if serializer_class.is_valid():
            new_mail=data['email']
            student = serializer_class.save(serializer_class.data)
            new_mail = data['email']
            my_token=Token.objects.create(user=student.user)

            send_after_registration(new_mail, my_token)

            return Response(StudentDetails(student).data, status=200)
        else:
            return Response(serializer_class.errors)

    def partial_update(self, request, *args, **kwargs):
        student_obj=self.get_queryset()[0]
        data=request.data
        if "first_name" in data:
            student_obj.user.first_name = data["first_name"]
        if "last_name" in data:
            student_obj.user.last_name = data["last_name"]
        if "roll_no" in data:
            student_obj.roll_no = data["roll_no"]
        if "city" in data:
            student_obj.city= data["city"]
        student_obj.save()
        return Response(StudentDetails(student_obj).data, status=200)

    def destroy(self,request,*args,**kwargs):
        student_obj = self.get_queryset()[0]
        student_obj.user.is_active = False
        student_obj.user.delete()
        return Response("deleted")


class Principal_List_view(viewsets.ModelViewSet):
    queryset = Principal.objects.all()
    serializer_class = PrincipalDetails
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer_class = PrincipalSerializerMain(data=data)
        if serializer_class.is_valid():
            principal = serializer_class.save(serializer_class.data)
            new_mail = data['email']
            my_token = Token.objects.create(user=principal.user)

            send_after_registration(new_mail, my_token)
            return Response(PrincipalDetails(principal).data, status=200)
        else:
            return Response(serializer_class.errors)

    def partial_update(self, request, *args, **kwargs):
        principal_obj=self.get_queryset()[0]
        data=request.data
        if "first_name" in data:
            principal_obj.user.first_name = data["first_name"]
        if "last_name" in data:
            principal_obj.user.last_name = data["last_name"]
        principal_obj.save()
        return Response(PrincipalDetails(principal_obj).data, status=200)

    def destroy(self,request,*args,**kwargs):
        principal_obj = self.get_queryset()[0]
        principal_obj.user.delete()
        return Response("deleted")


def send_after_registration(email,token):
    subject = "your account need to be verified"
    message = f'click the link to verify your account http://127.0.0.1:8000/app/verify/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    return send_mail(subject,message,email_from,recipient_list,fail_silently=False,)

def verify(request,token):
    print(type(token),"------token type----")
    user_obj=Token.objects.get(key=token).user
    print(user_obj,"verify object--------0----------")
    if user_obj:
        user_obj.is_active = True
        user_obj.save()
        return Response ("User verified")
    else:
        return Response("user is not verified")