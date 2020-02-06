from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import viewsets
from .models import EmailUser
from .serializers import EmailUserSerializer, CreateEmailUserSerializer
from .permissions import BaseUserPermission
from rest_framework.permissions import IsAuthenticated, AllowAny

# class EmailUserViewSet(viewsets.ModelViewSet):

#     serializer_class = EmailUserSerializer
#     permission_classes = (IsAuthenticated, )
#     queryset = EmailUser.objects.all()

#     def get_queryset(self):
#         q = self.queryset
#         print(q)

#         if 'email' in self.request.query_params:
#             return q.filter(email=self.request.query_params['email'])
#         return q.all()

#     def check_registered(self, request):


class CreateEmailUserViewSet(viewsets.ModelViewSet):

    serializer_class = CreateEmailUserSerializer
    permission_classes = (AllowAny, )
    queryset = EmailUser.objects.all()

    def get_queryset(self):
        q = self.queryset
        return q.all()

    def create(self, validated_data):

        if 'is_social' in self.request.data:
            print("self.request.data", self.request.data)
            try:
                user = EmailUser.objects.get(email=self.request.data['email'])
                print("user in def create() try block   ", user)
                print("\n")
                print("JsonResponse in try ", JsonResponse)
                return JsonResponse({
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_seller': user.is_seller,
                    'is_buyer': user.is_buyer,
                    'token': user.auth_token.key,
                    'validated_at': user.validated_at
                })
            except Exception as e:
                user = self.create_user_api(validated_data)
                user.is_social = True
                user.validated_at = datetime.datetime.now()
                user.save()
                return Response(
                    data={
                        'id': user.id,
                        'token': user.auth_token.key,
                        'email': user.email,
                        'is_seller': user.is_seller,
                        'is_buyer': user.is_buyer,
                        'validated_at': user.validated_at
                    })
        else:
            print("else part ")
            user = self.create_user_api(validated_data)
            print("user ", user)
            if user == False:
                user = EmailUser.objects.filter(
                    email=self.request.data['email'])
                if user:
                    return Response(
                        data={'result': 'Email id is already exist.'})
            return Response(
                data={
                    'id': user.id,
                    'token': user.auth_token.key,
                    'email': user.email,
                    'is_seller': user.is_seller,
                    'is_buyer': user.is_buyer,
                    'validated_at': user.validated_at
                })

    def create_user_api(self, validated_data):
        serializer = serializers.CreateEmailUserSerializer(
            data=self.request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return False
        user = serializer.save()
        user.set_password(self.request.data['password'])
        user.country_id = user.company_country_id
        user.save()
        if user.is_seller == True:
            user.is_seller_approved = True
            user.save()
        crate_notification_user = FCMDevice.objects.create(
            registration_id=123444,
            device_id=122323,
            user_id=user.id,
            type='abc')
        self.send_registration_email()
        return user

    def send_registration_email(self):
        plaintext = get_template('registration_confirmation.txt')
        htmly = get_template('registration_confirmation.html')

        d = {'email': self.request.user}

        subject, from_email, to = 'Welcome', settings.DEFAULT_FROM_EMAIL, str(
            self.request.data['email'])
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
