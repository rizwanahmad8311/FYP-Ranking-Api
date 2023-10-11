from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from . import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Project, Project_Category, Project_Reviews, User_Activation
from django.contrib.auth.hashers import make_password
# For Date and Time
from datetime import datetime , timedelta

# For 32 characters uuid
import uuid

# Current Server Time
def current_server_time(hours):
    current_time = datetime.now()
    future_time = current_time + timedelta(hours=hours)
    # future_time = future_time.strftime("%m-%d-%Y, %H:%M:%S")
    return future_time

# @api_view(['POST'])
# def signup_custom(request):
#     serializer = serializers.UserSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data['email']
#         u = email.replace('@kfueit.edu.pk', '')
#         username = u.lower()
#         if email.endswith("@kfueit.edu.pk"):
#             already = User(email=email)
#             if already.isExists():
#                 return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 email_uuid = str(uuid.uuid4())
#                 serializer.save(uuid=email_uuid, username=username)
#                 sent = sendmail_verification_link(
#                     serializer.validated_data['firstname'], serializer.validated_data['lastname'], username, email_uuid, serializer.validated_data['password'], email)

#                 return Response({'msg': 'Account created successfully.We have sent you an email Please verify it'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'Please Provide Correct University email'}, status=status.HTTP_400_BAD_REQUEST)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        u = email.replace('@kfueit.edu.pk', '')
        username = u.lower()
        if email.endswith("@kfueit.edu.pk"):
            try:
                User.objects.get(username=username)
                re = True
            except:
                re = False
            if re:
                return Response({'error': 'User Already Exists on provided email'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    email=email,
                    username=username,
                    password=serializer.validated_data['password']
                )
                email_uuid = str(uuid.uuid4())
                user_activation = User_Activation(uuid=email_uuid, user=user)
                user_activation.register()
                sent = sendmail_verification_link(
                    user.first_name, user.last_name, user.username, email_uuid, serializer.validated_data['password'], user.email)
                return Response({'success': 'Account has been created successfully Please check your email'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Please Provide Correct University email'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def sendmail_verification_link(firstname, lastname, username, email_uuid, password, email):
    sent = False

    from email.message import EmailMessage
    import ssl
    import smtplib
    # Authentication
    sender_email = "fypranking@gmail.com"
    sender_email_password = 'hspbqxkbpwabjvhx'
    receiver_email = email
    subject = "FYPR email confirmation"
    body = f"""Dear {firstname} {lastname}
       \nWe are happy to inform you that your FYPR(FYP RANKING) Account has been created Successfully.
       \n\nYour Logins are:
       \n Username: {username}
       \n Password:{password}
       \n\nTo avoid Login issues.
       \nPlease confirm your email address by clicking the link given below.
       \n http://fypranking.pythonanywhere.com/email-confirmation/{email_uuid}
       \n\nHow to login?
       \n\nPlease follow the following steps to access the FYP Ranking Dashboard.
       \n• Head over to FYPR App
       \n• Enter your username and password mentioned above.
       \n\nNote: If you are having trouble while loging into your account, contact us at fypranking+accountissue@gmail.com .
       \n\n Best regards,
       \nFYPR Team
       """
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, sender_email_password)
        smtp.sendmail(sender_email, receiver_email, em.as_string())
        sent = True
    return sent


def email_confirmation(request, uuid):
    try:
        user = User_Activation.objects.get(uuid=uuid)
        result = True
    except:
        result = False
    if result:
        if user.active:
            return render(request, 'email_confirmation.html', {'msg': 'Your Email has already been confirmed. Thanks!'})
        User_Activation.objects.filter(uuid=uuid).update(active=True)
        return render(request, 'email_confirmation.html', {'msg': 'Congratulations!Your Email has been confirmed.'})
    else:
        return render(request, 'email_confirmation.html', {'msg': 'Invalid link!'})


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        is_user_active = User_Activation.objects.get(user=user.id)
        if is_user_active.active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Please verify your email first.Instructions are in email sent to you'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'username or password is incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def send_verification_link_again(request):
    email = request.data.get('email')
    if email is not None:
        try:
            user = User.objects.get(email=email)
            re = True
        except:
            re = False
        if re:
            email_uuid = User_Activation.objects.get(user=user.id)
            sent = sendmail_verification_link_again(
                user.first_name, user.last_name, email_uuid.uuid, user.email)
            return Response({'msg': 'Link for email confirmation has been sent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Account does not exists'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Email is required!'}, status=status.HTTP_401_UNAUTHORIZED)


def sendmail_verification_link_again(firstname, lastname, email_uuid, email):
    sent = False

    from email.message import EmailMessage
    import ssl
    import smtplib
    # Authentication
    sender_email = "fypranking@gmail.com"
    sender_email_password = 'hspbqxkbpwabjvhx'
    receiver_email = email
    subject = "FYPR email confirmation"
    body = f"""Dear {firstname} {lastname}
       \nYou are requested for your FYPR(FYP RANKING) Account email confirmation link.
       \n\nHere is the Link.
       \n http://fypranking.pythonanywhere.com/email-confirmation/{email_uuid}
       \n\nHow to login?
       \n\nPlease follow the following steps to access the FYP Ranking Dashboard.
       \n• Head over to FYPR App
       \n• Enter your username and password.
       \n\nNote: If you are having trouble while loging into your account, contact us at fypranking+accountissue@gmail.com .
       \n\nBest regards,
       \nFYPR Team
       """
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, sender_email_password)
        smtp.sendmail(sender_email, receiver_email, em.as_string())
        sent = True
    return sent




@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    serializer = serializers.UserProfileSerializer(request.user, data=request.data)
    password = request.data.get('password')
    if password:
        password = make_password(password)
        User.objects.filter(pk=request.user.id).update(password=password)
        return Response({'success':'Password has been Updated'}, status=status.HTTP_200_OK)
    else:
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'Profile has been Updated','data':serializer.data}, status=status.HTTP_200_OK)
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# All Projects and Reviews without login
@api_view(['GET'])
def all_projects(request):
    projects = Project.objects.filter(status=True).all()
    if len(projects) < 1:
        return Response({'msg': 'No Projects'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = serializers.GetProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def all_reviews(request, pk):
    project_reviews = Project_Reviews.objects.filter(project_id=pk).all()
    if len(project_reviews) < 1:
        return Response({'msg': 'No Reviews'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = serializers.GetProjectReviewsSerializer(
            project_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Project Upload
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_projects(request):
    projects = Project.objects.filter(user_id=request.user)
    if len(projects) < 1:
        return Response({'msg': 'No Projects Uploaded'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = serializers.GetProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    projects = Project.objects.filter(user_id=request.user)
    if len(projects) < 1:
        project_category_id = request.data.get('project_category_id')
        if project_category_id is None:
            return Response({'error': f'{project_category_id}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.ProjectSerializer(data=request.data)
            try:
                p_cat_id = Project_Category.objects.get(id=project_category_id)
                r = True
            except:
                r = False

            server_time = current_server_time(5)
            if r:
                if serializer.is_valid():
                    serializer.save(user_id=request.user, project_category_id=p_cat_id,
                                    created_at=server_time, updated_at=server_time)
                    return Response({'success':'Project uploaded successfully'}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        latest_project = Project.objects.filter(
            user_id=request.user).order_by('-id')[0]
        if latest_project.status:
            project_category_id = request.data.get('project_category_id')
            if project_category_id is None:
                return Response({'error': 'Select Project Category'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = serializers.ProjectSerializer(data=request.data)
                try:
                    p_cat_id = Project_Category.objects.get(
                        id=project_category_id)
                    r = True
                except:
                    r = False
                server_time = current_server_time(5)
                if r:
                    if serializer.is_valid():
                        serializer.save(user_id=request.user, project_category_id=p_cat_id,
                                        created_at=server_time, updated_at=server_time)
                        return Response({'success':'Project uploaded successfully'}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': "Category does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Wait for your Previous Project to be approved!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_project(request, pk):
    project_category_id = request.data.get('project_category_id')
    server_time = current_server_time(5)
    if project_category_id is None:
        return Response({'error': 'Select Project Category'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            project = Project.objects.get(pk=pk, user_id=request.user)
            r = True
        except:
            r = False
        if r:
            try:
                p_cat_id = Project_Category.objects.get(id=project_category_id)
                result_cat = True
            except:
                result_cat = False
            if result_cat:
                serializer = serializers.ProjectSerializer(
                    project, data=request.data)
                if serializer.is_valid():
                    serializer.save(project_category_id=p_cat_id,
                                    updated_at=server_time, status=False)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Project Category does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, pk):
    try:
        project = Project.objects.get(pk=pk, user_id=request.user)
        project.delete()
        return Response({'success': 'Project Has Been Deleted'},status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({'error': 'Project does not exist'},status=status.HTTP_400_BAD_REQUEST)






# Project Reviews
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reviews(request, pid):
    project_reviews = Project_Reviews.objects.filter(
        user_id=request.user, project_id=pid)
    if len(project_reviews) < 1:
        return Response({'msg': 'No Reviews'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = serializers.GetProjectReviewsSerializer(
            project_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pid):
    serializer = serializers.ProjectReviewsSerializer(data=request.data)
    server_time = current_server_time(5)
    try:
        project_id = Project.objects.get(pk=pid)
        r = True
    except:
        r = False
    if r:
        if serializer.is_valid():
            try:
                Project_Reviews.objects.get(project_id=pid,user_id=request.user.id)
                return Response({'error':'You have already reviewed'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                serializer.save(user_id=request.user, project_id=project_id,
                                feedback_date=server_time, feedback_update_date=server_time)
                return Response({'success':'Your review has been submitted','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Project does not exist','errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Project does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_review(request, rid):
    serializer = serializers.ProjectReviewsSerializer(data=request.data)
    server_time = current_server_time(5)
    try:
        review = Project_Reviews.objects.get(pk=rid, user_id=request.user)
        r = True
    except:
        r = False
    if r:
        serializer = serializers.ProjectReviewsSerializer(
            review, data=request.data)
        if serializer.is_valid():
            serializer.save(feedback_update_date=server_time)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Review does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, rid):
    try:
        review = Project_Reviews.objects.get(pk=rid, user_id=request.user)
        review.delete()
        return Response({'success':'Review has been deleted'},status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({'error':'Review does not exist'},status=status.HTTP_204_NO_CONTENT)



# Projects by category
@api_view(['GET'])
def projects_by_category(request,pk):
    projects = Project.objects.filter(status=True,project_category_id=pk).all()
    if len(projects) < 1:
        return Response({'msg': 'No Projects'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = serializers.GetProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category(request):
    categories = Project_Category.objects.all()
    serializer = serializers.CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)