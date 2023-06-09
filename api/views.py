from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import *
from .serializers import *
import datetime
from rest_framework.views import APIView
from django.views import View
from .views import *
from django.http import HttpResponse
import json
from django.utils.html import strip_tags
import datetime
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.db.models import F, Q
def remove_html_tags(text):
    """Removes HTML tags from the given text"""
    return strip_tags(text)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def home(request):
    return HttpResponse('Home')
class UserRegistration(APIView):

    def post(self, request, format=None):
        lang = request.data.get('lang_code')
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if lang=="it":
            msg = "Registrazione correttamente eseguita!"
        else:    
            msg = "User Registration  Successfully!"
        return Response({'msg':msg, 'success': "true"}, status=status.HTTP_200_OK)

class UserLoginView(APIView):

    def post(self, request, format=None):
        lang = request.data.get('lang_code')
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile_number = serializer.data.get('mobile_number')
        passwords = '12345'
        users = authenticate(mobile_number=mobile_number, password = passwords)

        if users is not None:
            if users.is_active == 1:
                login(request, users)
               
                if lang=="it":
                    msg = "Accesso correttamente effettuato!"
                else:    
                    msg = "User Login Succesfully...!"
                return Response({ 'msg':msg, 'success': "true", "user_id": users.pk, "surname": users.surname, 'nickname':users.nickname  }, status=status.HTTP_200_OK)
            else:
                if lang=="it":
                    msg = "L'account utente è Dactivate..!"
                else:    
                    msg = "User Account is Dactivate..!"
         
                return Response({'msg':msg , 'success': "true"}, status=status.HTTP_200_OK)     
        if lang=="it":
            msg = "Il numero inserito non risulta registrato. Procedere con la registrazione!"
        else:    
            msg = "Mobile Number Not Registered Please Register Your Mobile Number"
        return Response({"success": "false", "msg":msg  }, status=status.HTTP_200_OK)

class VerifyMobileNumber(APIView):

    def post(self, request):
        lang = request.data.get('lang_code')
        phone_number = request.data.get('phone_number')
        if Users.objects.filter(mobile_number=phone_number).exists():
            if lang=="it":
                msg = "Numero di cellulare verificato..!"
            else:    
                msg = "Mobile Number Verified..!"
            return Response({"msg":msg, "success":"true"})
        else:
            if lang=="it":
                msg = "Il numero inserito non risulta registrato. Procedere con la registrazione!"
            else:    
                msg = "Mobile Number Not registerd..!"
            return Response({"msg":msg,  "success":"false"})
class UserProfileUpdateView(APIView):
    
    def post(self, request, format=None):
    
        user_id = request.data.get('id') 
        lang = request.data.get('lang_code')
        user_id = user_id if user_id is not None else "00"
        try:
            data = Users.objects.get(id=user_id)
            serializer = UpdateUserProfileSerializer(data)
            if lang=="it":
                msg = "Dettaglio profili utente!"
            else:    
                msg = "User  Profiles Details"
            return Response({'success': 'true', 'msg':msg, "data": serializer.data}, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            pass
    def put(self, request, format=None):
        user_id = request.data.get('id')
        lang = request.data.get('lang_code')

        if user_id:
            data = Users.objects.get(pk=user_id)
            data.email = request.data.get('email')
            image_url = request.data.get('image_url')
            
            if image_url:
                data.image_url = image_url
                full_name =request.data.get('full_name')
                name_parts = full_name.split(' ')
                if len(name_parts) > 0:
                    data.surname = name_parts[0]
                if len(name_parts) > 1:
                    nickname_parts = name_parts[1:]
                    data.name = ' '.join(nickname_parts) if len(nickname_parts) > 1 else nickname_parts[0]
                if len(name_parts) > 1:
                    nickname_parts = name_parts[1:]
                    data.nickname = ' '.join(nickname_parts) if len(nickname_parts) > 1 else nickname_parts[0]
                    
                    data.save()
                    if lang=="it":
                        msg = "Profilo correttamente aggiornato!"
                    else:    
                        msg = "User Profile Updated Successfully..!"
                    return Response({'success': 'true', 'msg':msg}, status=status.HTTP_200_OK)
            else:
                users = Users.objects.filter(pk=user_id)
                data = Users.objects.get(pk=user_id)
                for user in users:
                    data.image_url = user.image_url
                    full_name =request.data.get('full_name')
                    name_parts = full_name.split(' ')
                    if len(name_parts) > 0:
                        data.surname = name_parts[0]
                    if len(name_parts) > 1:
                        nickname_parts = name_parts[1:]
                        data.name = ' '.join(nickname_parts) if len(nickname_parts) > 1 else nickname_parts[0]
                    if len(name_parts) > 1:
                        nickname_parts = name_parts[1:]
                        data.nickname = ' '.join(nickname_parts) if len(nickname_parts) > 1 else nickname_parts[0]
                        
                        data.save()
                    if lang=="it":
                        msg = "Profilo correttamente aggiornato!"
                    else:    
                        msg = "User Profile Updated Successfully..!"
                    return Response({'success': 'true', 'msg':msg}, status=status.HTTP_200_OK)
        if lang=="it":
            msg = "Record utente non trovato...!"
        else:    
            msg = "User Record Not Found...!"
        return Response({'success': 'false', 'msg':msg }, status=status.HTTP_200_OK)

class ListCategories( APIView):

    def post(self, request):
        lang = request.data.get('lang_code')
        user_id = request.data.get('user_id')
        data = Categories.objects.filter(parent_id = None).all()
        serializers = ListsCategoriesSerializer(data, many=True, context={"user":user_id})
        if lang=="it":
            msg = "Categorie Elenchi Dettagli"
        else:    
            msg = "Categories Lists Details"
        return Response({"success": "true", "msg":msg, "data": serializers.data}, status=status.HTTP_200_OK)
class ListSubCategories(APIView):
    
    def post(self, request):
        lang = request.data.get('lang_code')
        category_id = request.data.get('category_id')
        user_id = request.data.get('user_id')
        data = Categories.objects.filter(parent_id=category_id)
        if data.count() != 0:
            response = [] 
            for data in data:
                follows = FavouriteCategories.objects.filter(category_id=data.pk, user_id = user_id)
                if follows:
                    follows =  1
                else: 
                    follows =  0
                res = {
                    'id':data.pk,
                    'image_url':data.image_url, 
                    'title':data.title, 
                    'follows':follows,
                    'created_at':data.created_at
                }   
                response.append(res)
            if lang=="it":
                msg = "Sottocategorie Elenchi Dettagli"
            else:    
                msg = "Sub Categories Lists Details"
            return Response({"success": "true", "msg":msg, "data":response}, status=status.HTTP_200_OK)
        else:
            if lang=="it":
                msg = "Nessuna sottocategoria trovata per la categoria specificata"
            else:    
                msg = "No sub categories found for the given category."
            return Response({"success": "false", "msg":msg }, status=status.HTTP_200_OK)
class ListsCalendario(APIView):

    def post(self, request):
        lang = request.data.get('lang_code')
        stagione = request.data.get('stagione')
        data = Calendario.objects.filter(stagione=stagione)
        for cl in data:
            casa = Squadre.objects.get(title=cl.casa)
            trasferta = Squadre.objects.get(title=cl.trasferta)
        serializers = CalendarioDetailsSerializer(data, many=True, context={'casa_image':casa.image_url, 'trasferta_image':trasferta.image_url})
        if lang=="it":
            msg = "Calendario Liste Dettagli"
        else:    
            msg = "Calendario Lists Details."
        return Response({"success": "true", "msg":msg, "data": serializers.data}, status=status.HTTP_200_OK)
class ListsGiocatori(APIView):

    def post(self, request):
        data = Giocatori.objects.all()
        lang = request.data.get('lang_code')
        serializers = GiocatoriDetailsSerializer(data, many=True)
        if lang=="it":
            msg = "Giocatori Liste Dettagli"
        else:    
            msg = "Giocatori Lists Details."
        return Response({"success": "true", "msg":msg, "data": serializers.data}, status=status.HTTP_200_OK)
class ListsSquadre(APIView):
    def post(self, request):
        lang = request.data.get('lang_code')
        response = []
        if lang=="it":
            tems = { 'title': "Tutte" }
            response.append(tems)
        else:
            tems = { 'title': "All Teams" }
            response.append(tems)  
        data = Squadre.objects.all()
        serializer = SquadreSerializer(data, many=True)
        response += serializer.data
  
        if lang == "it":
            msg = "Squadre Liste Dettagli"
        else:    
            msg = "Squadre Lists Details"
        return Response({"success": "true", "msg":msg, "data": response}, status=status.HTTP_200_OK)

# class PostLists(APIView):

#     def post(self, request):
#         lang = request.data.get('lang_code')
#         post = Posts.objects.all()
#         total_posts = post.count()
#         user_id = request.data.get('user_id')
#         now = datetime.datetime.now()
#         today_date = now.strftime("%Y-%m-%d")
#         if Users.objects.filter(id=user_id).exists():
#             fav_cat = FavouriteCategories.objects.filter(user_id=user_id)
#             results = []
#             if fav_cat:
#                 for fv in fav_cat:
#                     data = Posts.objects.filter( category_id=fv.category_id, active=1,  end_date__gte=today_date ).order_by('-start_date')
#                     cat_title = ''
#                     page = request.data.get('page')
#                     paginator = Paginator(data, 5)
#                     post_lists = paginator.get_page(page)
#                     for post in post_lists:
#                         reactions = PostReact.objects.filter(post_id=post.pk).values('reaction').annotate(count=Count('reaction')).order_by('-count')
#                         max_reaction = reactions[0]['reaction'] if reactions else 10
#                         if Categories.objects.filter(id=post.category_id).exists():
#                             cat_obj = Categories.objects.get(id=post.category_id)
#                             cat_title = cat_obj.title 
#                         post_react = PostReact.objects.filter(post_id=post.pk)
#                         total_react = post_react.count()
#                         total_love = PostReact.objects.filter(post_id=post.pk, reaction=max_reaction).count()
#                         max_react_value = 0
#                         if total_love!=0:
#                             max_react_value = int((total_love*100)/total_react)
#                         else:
#                             max_react_value = 0
#                         title = strip_tags(post.title).replace('&nbsp;', ' ')
#                         html_string = post.description
#                         cleaned_string = strip_tags(html_string).replace('&nbsp;', ' ')
#                         html_about = post.about
#                         cleaned_string_about = strip_tags(html_about).replace('&nbsp;', ' ')
#                         res = {
#                             'id': post.pk,
#                             'max_react_value':max_react_value,
#                             'max_reaction': max_reaction,
#                             'totalPercentage': total_react,
#                             'guid': post.guid,
#                             'provider_profile_id': post.provider_profile_id,
#                             'category_id': post.category_id,
#                             'title': _(post.title), 
#                             'description': _(cleaned_string), 
#                             'about': _(cleaned_string_about), 
#                             'address': post.address,
#                             'start_date': post.start_date,
#                             'end_date': post.end_date,
#                             'image_url': post.image_url,
#                             'link': post.link,
#                             'data': post.data,
#                             'video': post.video,
#                             'created_at': post.created_at,
#                             'updated_at': post.updated_at,
#                             'active': post.active,
#                             "cat_title": _(cat_title), 
#                         }
#                         results.append(res)
#                 if lang == "it":
#                     msg = "Elenchi record di notizie...!"
#                 else:    
#                     msg = "News Record Lists...!"
#                 sorted_data = sorted(results, key=lambda x: x['start_date'], reverse=True)
#                 return Response({"success": "true", "msg": msg, 'total_posts':total_posts, "data":sorted_data}, status=status.HTTP_200_OK)
#             if lang == "it":
#                 msg = "Notizie Record non trovati...!"
#             else:    
#                 msg = "News Records Not Found...!"
#             return Response({"success": "false", "msg":msg}, status=status.HTTP_200_OK)

#         else:
#             post = Posts.objects.all()
#             total_posts = post.count()
#             data = Posts.objects.filter(active=1,  end_date__gte=today_date).exclude(category_id=90).order_by('-start_date')
#             paginator = Paginator(data, 10) # 5 is the number of items per page
#             page = request.data.get('page') # get the current page number from query parameters
#             post_lists = paginator.get_page(page)
#             results = []
#             cat_title = ''
#             for post in post_lists:
#                 reactions = PostReact.objects.filter(post_id=post.pk).values('reaction').annotate(count=Count('reaction')).order_by('-count')
#                 max_reaction = reactions[0]['reaction'] if reactions else 10
#                 if Categories.objects.filter(id=post.category_id).exists():
#                     cat_obj = Categories.objects.filter(id=post.category_id).exclude(title='E-SPORTS')
#                     for c in cat_obj:
#                         cat_title = c.title
#                 post_react = PostReact.objects.filter(post_id=post.pk)
#                 total_react = post_react.count()
#                 total_love = PostReact.objects.filter(post_id=post.pk, reaction=max_reaction).count()
#                 max_react_value = 0
#                 if total_love!=0:
#                     max_react_value = int((total_love*100)/total_react)
#                 else:
#                     max_react_value = 0
#                 html_string = post.description
#                 cleaned_string = strip_tags(html_string).replace('&nbsp;', ' ')
#                 html_about = post.about
#                 cleaned_string_about = strip_tags(html_about).replace('&nbsp;', ' ')
#                 res = {
#                     'id':post.pk, 'max_react_value':max_react_value,  'max_reaction':max_reaction, 'totalPercentage':total_react,  'guid':post.guid, 'provider_profile_id':post.provider_profile_id, 'category_id':post.category_id, 'title':post.title, 'description':cleaned_string, 'about':cleaned_string_about, 'address':post.address, 'start_date':post.start_date, 'end_date':post.end_date,  'image_url':post.image_url, 'link':post.link, 'data':post.data, 'video':post.video,  'created_at':post.created_at, 'updated_at':post.updated_at, 'active':post.active,  "cat_title":cat_title
#                 }
#                 results.append(res)
#             if lang == "it":
#                 msg = "Elenchi record di notizie...!"
#             else:    
#                 msg = "News Record Lists...!"
#             return Response({"success": "true", "msg":msg,  'total_posts':total_posts, "data":results}, status=status.HTTP_200_OK)
class PostDetails(APIView):

    def post(self, request):
        lang = request.data.get('lang_code')
        user_id = request.data.get('user_id')
        post_id = request.data.get('id')
        if user_id is not None and Users.objects.filter(pk=user_id).exists():
            user = Users.objects.get(pk=user_id)
            data = Posts.objects.get(id=post_id)
            data_obj = Posts.objects.get(id=post_id)
            cat_obj = Categories.objects.get(id=data_obj.category_id)
            cat_title = cat_obj.title
            if FavouriteEvents.objects.filter(user=user, event_id=data_obj.pk ).exists():
                saved = 1
            else:
                saved = 0
            html_string = data.about
            soup = BeautifulSoup(html_string, 'html.parser')
            cleaned_content = soup.get_text()
            res = {
            'id':data.pk, 
            'guid':data.guid, 
            "saved":saved,
            "cat_title":cat_title,
            'provider_profile_id':data.provider_profile_id, 
            'category_id':data.category_id, 
            'title':data.title, 
            'description':data.description, 
            'about':cleaned_content,
            'address':data.address, 
            'start_date':data.start_date, 
            'end_date':data.end_date, 
            'image_url':data.image_url, 
            'link':data.link, 'data':data.data, 
            'video':data.video, 
            'created_at':data.created_at, 
            'updated_at':data.updated_at, 
            'active':data.active   
            }
            if lang == "it":
                msg = "Posta Dettagli"
            else:    
                msg = "Post Details"
            return Response({"success":"true", "msg": msg, "data": res}, status=status.HTTP_200_OK)
        else:
            data = Posts.objects.get(id=post_id)
            cat_obj = Categories.objects.get(id=data.category_id)
            cat_title = cat_obj.title
            html_string = data.about
            soup = BeautifulSoup(html_string, 'html.parser')
            cleaned_content = soup.get_text()
            res = {
            'id':data.pk, 
            'guid':data.guid, 
            'cat_title':cat_title,
            'provider_profile_id':data.provider_profile_id, 
            'category_id':data.category_id, 
            'title':data.title, 
            'description':data.description, 
            'about':cleaned_content,
            'address':data.address, 
            'start_date':data.start_date, 
            'end_date':data.end_date, 
            'image_url':data.image_url, 
            'link':data.link, 'data':data.data, 
            'video':data.video, 
            'created_at':data.created_at, 
            'updated_at':data.updated_at, 
            'active':data.active   
            }
            if lang == "it":
                msg = "Posta Dettagli"
            else:    
                msg = "Post Details"
            return Response({"success":"true", "msg": msg, "data": res}, status=status.HTTP_200_OK)
class SimilarPost(APIView):
    def post(self, request):
        lang = request.data.get('lang_code')
        post_id = request.data.get('id')
        if Posts.objects.filter(pk=post_id):
            data = Posts.objects.get(id=post_id)
            now = datetime.datetime.now()
            today_date = now.strftime("%Y-%m-%d")
            data = Posts.objects.filter(category_id=data.category_id, active=1).exclude(id=post_id).order_by('-id')
            response = []
            for post in data:
                title = strip_tags(post.title)
                res = {
                    'id':post.pk,   'guid':post.guid, 'provider_profile_id':post.provider_profile_id, 'category_id':post.category_id, 'title':title, 'address':post.address, 'start_date':post.start_date, 'end_date':post.end_date,  'image_url':post.image_url, 'link':post.link, 'data':post.data, 'video':post.video,  'created_at':post.created_at, 'updated_at':post.updated_at, 'active':post.active, 
                    }
                response.append(res)
            if lang == "it":
                msg = "Elenchi di post simili"
            else:    
                msg = "Similar Post Lists"
            return Response({"success": "true", "msg": msg, "data":response}, status=status.HTTP_200_OK)
        else:
            if lang == "it":
                msg = "Inserimento non trovato...!"
            else:    
                msg = "Record Not Found...!"
            return Response({"success": "true", "msg":msg, }, status=status.HTTP_200_OK)
    
class PostComment(APIView):

    def post(self, request, format=None):
        lang = request.data.get('lang_code')
        serializer = PostCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if lang == "it":
            msg = "Messaggio correttamente postato!"
        else:    
            msg = "User Comment Message Sent  Successfully!"
        return Response({'msg':msg, 'success': "true"}, status=status.HTTP_200_OK)

class RecentPostComments(APIView):

    def post(self, request):
        post= request.data.get('id')
        lang = request.data.get('lang_code')
        post_comment = Ratings.objects.filter(post_id=post, is_online=1 ).order_by('-id')[:2]
        if post_comment.count() !=0:
            comments = []
            for comment in post_comment:
                user_obj = comment.user 
                my_date_string = str(comment.created_at)
                my_date = datetime.datetime.fromisoformat(my_date_string).date()
                formatted_date = my_date.strftime("%d %b, %Y")
                comt = {
                    'id':comment.pk,
                    'review':comment.review,
                    'surname':user_obj.surname,
                    'nickname': user_obj.nickname ,
                    'user_image':user_obj.image_url.url,
                    'created_at':formatted_date,
                }
                comments.append(comt)
            if lang == "it":
                msg = "Post recente Commento Elenco dei messaggi Dettagli!"
            else:    
                msg = "Recent Post  Comment Message Lists Details!"
            return Response({'msg':msg, 'success': "true", "data":comments}, status=status.HTTP_200_OK)
        else:
            if lang == "it":
                msg = "Messaggio di commento non trovato!"
            else:    
                msg = "Comment Message Not Found !"
            return Response({'msg':msg, 'success': "false", }, status=status.HTTP_200_OK)
        
class PostAllComments(APIView):

    def post(self, request):
        post= request.data.get('id')
        lang = request.data.get('lang_code')
        post_comment = Ratings.objects.filter(post_id=post, is_online=1).order_by('-id')
        if post_comment.count() !=0:
            comments = []
            for comment in post_comment:
                user_obj = comment.user
                my_date_string = str(comment.created_at)
                my_date = datetime.datetime.fromisoformat(my_date_string).date()
                formatted_date = my_date.strftime("%d %b, %Y")
                comt = {
                    'id':comment.pk,
                    'review':comment.review,
                    'surname':user_obj.surname,
                    'nickname': user_obj.nickname ,
                    'user_image':user_obj.image_url.url,
                    'created_at':formatted_date
                }
                comments.append(comt)
            if lang == "it":
                msg = "Post recente Commento Elenco dei messaggi Dettagli!"
            else:    
                msg = "Recent Post  Comment Message Lists Details!"
            return Response({'msg': msg, 'success': "true", "data":comments}, status=status.HTTP_200_OK)
        else:
            if lang == "it":
                msg = "Messaggio di commento non trovato!"
            else:    
                msg = "Comment Message Not Found !"
            return Response({'msg': msg, 'success': "false", }, status=status.HTTP_200_OK)
        
class  EventsList(APIView):
    def post(self, request):
        lang = request.data.get('lang_code')
        now = datetime.datetime.now()
        today_date = now.strftime("%Y-%m-%d")
        post = Posts.objects.all()
        total_posts = post.count()
        data = Posts.objects.filter(active=1, category_id=90,start_date__lte=today_date, end_date__gte=today_date ).order_by("-id")
        results = []
        cat_title = ''
        for post in data:
            reactions = PostReact.objects.filter(post_id=post.pk).values('reaction').annotate(count=Count('reaction')).order_by('-count')
            max_reaction = reactions[0]['reaction'] if reactions else 10
            if Categories.objects.filter(id=post.category_id).exists():
                cat_obj = Categories.objects.filter(id=post.category_id)
                for c in cat_obj:
                    cat_title = c.title
            post_react = PostReact.objects.filter(post_id=post.pk)
            total_react = post_react.count()
            description  = post.description 
            if description is not None:
                soup = BeautifulSoup(description, 'html.parser')
                description = soup.get_text()
            else:
                soup = "<p> <p>"
                soup = BeautifulSoup(soup, 'html.parser')
                description = soup.get_text()
            html_about = post.about
            if html_about is not None:
                soup = BeautifulSoup(html_about, 'html.parser')
                about = soup.get_text()
            else:
                soup = "<p> <p>"
                soup = BeautifulSoup(soup, 'html.parser')
                about = soup.get_text()
            res = {
                'id':post.pk, 'max_reaction':max_reaction, 'totalPercentage':total_react,  'guid':post.guid, 'provider_profile_id':post.provider_profile_id, 'category_id':post.category_id, 'title':post.title, 'description':description, 'about':about, 'address':post.address, 'start_date':post.start_date, 'end_date':post.end_date,  'image_url':post.image_url, 'link':post.link, 'data':post.data, 'video':post.video,  'created_at':post.created_at, 'updated_at':post.updated_at, 'active':post.active,  "cat_title":cat_title
                }
            results.append(res)
        if lang == "it":
            msg = "Elenchi record di notizie...!"
        else:    
            msg = "News Record Lists...!"
        return Response({"success": "true", "msg":msg, 'total_posts':total_posts, "data":results}, status=status.HTTP_200_OK)
class LatestEventsCarouselImageLists(APIView):

    def post(self, request):
        lang = request.data.get('lang_code')
        data = Events.objects.all().order_by("-id")[:4]
        serializers = CarouselSerializer(data, many=True)
        if lang == "it":
            msg = "Ultimi elenchi di eventi"
        else:    
            msg = "Latest Events Lists"
        return Response({"success": "true", "msg": msg, "data": serializers.data}, status=status.HTTP_200_OK)
class LatestNewsCarouselImageLists(APIView):
    
    def post(self, request):
        lang = request.data.get('lang_code')
        data = Posts.objects.all().order_by("-id")[:4]
        response = []
        for post in data:
            if Categories.objects.filter(id=post.category_id).exists():
                cat_obj = Categories.objects.get(id=post.category_id)
                res = {
                    'id':post.pk,  
                    'image_url':post.image_url, 
                    'title':post.title,
                    "sub_title":cat_obj.title
                }
                response.append(res)
        if lang == "it":
            msg = "Ultimi elenchi di eventi"
        else:    
            msg = "Latest Events Lists"
        return Response({"success": "true", "msg":msg, "data": response}, status=status.HTTP_200_OK)
class EventCoverImages(APIView):

    def post(self, request):
        lang = request.data.get('lang_code')
        data = TblPostCover.objects.all()
        serializers = TblPostCoverListsSerializer(data, many=True)
        if lang == "it":
            msg = "Immagini di copertina dell'evento Elenca i dettagli"
        else:    
            msg = "Event Cover Images Lists Details"
        return Response({"success": "true", "msg":msg, "data": serializers.data}, status=status.HTTP_200_OK)
class ContactUs(APIView):

    def post(self, request, format=None):
        mobile_number = request.data.get('mobile_number')
        message = request.data.get('message')
        lang = request.data.get('lang_code')
        if Users.objects.filter(mobile_number=mobile_number).exists():
            user = Users.objects.get(mobile_number=mobile_number)
            Supports.objects.create(name=user.surname, email=user.email, message=message, is_read=0)
            if lang == "it":
                msg = "Messaggio correttamente inviato! Sarai ricontattato il prima possibile."
            else:    
                msg = "Your Feedback Message Submit  Successfully!"
            return Response({'msg':msg, 'success': "true"}, status=status.HTTP_200_OK)
        else:
            Supports.objects.create(name='anonymous', email=mobile_number, message=message, is_read=0)
            if lang == "it":
                msg = "Messaggio correttamente inviato! Sarai ricontattato il prima possibile."
            else:    
                msg = "Your Feedback Message Submit  Successfully!"
            return Response({'msg':msg , 'success': "true"}, status=status.HTTP_200_OK)

class CategoryDetails(APIView):

    def post(self, request):
        Category_id = request.data.get('id')
        lang = request.data.get('lang_code')
        if Category_id :
            data = Categories.objects.get(id=Category_id)
            serializers = CategoryDetailsSerializer(data)
            if lang == "it":
                msg = "Categoria Dettagli"
            else:    
                msg = "Category  Details"
            return Response({"success": "true", "msg":msg , "data": serializers.data}, status=status.HTTP_200_OK)
        else:
            if lang == "it":
                msg = "ID categoria richiesto!"
            else:    
                msg = "Category  Id Required!"
            return Response({"success": "true", "msg":msg }, status=status.HTTP_200_OK)
    
class E_SportDetails(APIView):

    def post(self, request):
        event_id = request.data.get('event_id')
        lang = request.data.get('lang_code')
        if event_id :
            data = Events.objects.filter(id=event_id)
            serializers = EsportDetailsSerializer(data, many=True)
            if lang == "it":
                msg = "Dettagli sulla categoria E-Sport"
            else:    
                msg = "E-Sport Category  Details"
            return Response({"success": "true", "msg":msg , "data": serializers.data}, status=status.HTTP_200_OK)
        else:
            if lang == "it":
                msg = "ID categoria e-sport richiesto!"
            else:    
                msg = "E-Sport Category  Id Required!"
            return Response({"success": "true", "msg":msg , }, status=status.HTTP_200_OK)
        
class FantacalcioSeasonsLists(APIView):

    def post(self, request):
        lang = request.data.get('lang_code')
        GIOCATORI = ""
        CALENDARIO = "" 
        SQUADRE = ""
        if lang =="it":
            GIOCATORI = "GIOCATORI"
            CALENDARIO = "CALENDARIO" 
            SQUADRE = "SQUADRE"
        else : 
            GIOCATORI = "PLAYERS"
            CALENDARIO = "CALENDAR" 
            SQUADRE = "TEAMS"
        giocatori_image = "/media/player.png"   
        celendrio_image = "/media/celender.png"
        squadre_image = "/media/team.png"
        data = FcSeasons.objects.all()
        response = []
        for data in data:
            res = { 'id':data.pk, 
                    'code_id':data.code_id,  
                    'synced':data.synced, 
                    'image_url':data.image_url, 
                    'season_api':data.season_api, 
                    'title':data.title, 
                    'image_url':data.image_url, 
                    'bg_color_rgba':data.bg_color_rgba, 
                    'app_bg_color_rgba':data.app_bg_color_rgba, 
                    'GIOCATORI':GIOCATORI,
                    'giocatori_image':giocatori_image, 
                    'SQUADRE':SQUADRE, 
                    'celendrio_image':celendrio_image, 
                    'CALENDARIO':CALENDARIO, 
                    'squadre_image':squadre_image, 
                    'created_at':data.created_at, 
                    'updated_at':data.updated_at 
                    } 
            response.append(res)
        if lang == "it":
            msg = "Dettagli delle liste stagionali"
        else:    
            msg = "Season Lists Details"
        return Response({"success": "true", "msg":msg , "data": response}, status=status.HTTP_200_OK)
class SearchRecoard(APIView):

    def post(self, request):
        search = request.data.get('search')
        lang = request.data.get('lang_code')

        if search is not None:
            if FcPlayers.objects.filter(first_name=search).exists():
                search_data = FcPlayers.objects.filter(first_name=search)
                teams_details = Squadre.objects.filter(title=search)
                player = []
                for d in search_data:
                    player_details = FcPlayers.objects.filter(code_id=d.code_id) 
                    for h in player_details:
                        url = h.image_url
                        base_url = "http://138.201.86.170/sportal/gestionale/"
                        img_url = base_url+url
                        plys = FcPlayerStats.objects.filter(player_code_id=h.code_id).first()
                        season = plys.season_code
                        res = { 
                            'player':"player",
                            'code_id':h.code_id,
                            'first_name':h.first_name, 
                            'last_name':h.last_name, 
                            'birth_date':h.birth_date, 
                            'team_name':plys.r_name,
                            'role':plys.pr_role,
                            'image_url':img_url,
                            "season_title":season.title,
                            "season_image":season.image_url,
                            "season_code_id":season.code_id
                        }
                        player.append(res)
                for teams in teams_details:
                    team = {
                        'player':"team",
                        "code_id":0,
                        'first_name':teams.title,
                        'last_name':"" ,
                        'birth_date':"",
                        'team_name':teams.title,
                        'role':0,
                        'image_url':teams.image_url,
                        "season_title":season.title,
                        "season_image":season.image_url,
                        "season_code_id":season.code_id
                        
                    }
                    player.append(team)
                if lang == "it":
                    msg = "Cerca i dettagli dei record"
                else:    
                    msg = "Search Records   Details"
                return Response({"success": "true", "msg":msg ,"search":"players", "data": player}, status=status.HTTP_200_OK)
                
            elif Squadre.objects.filter(title=search).exists():
                search_data = Squadre.objects.filter(title=search)
                teams = []
                season = FcSeasons.objects.filter().first()
                for d in search_data:
                    teams_details = Squadre.objects.filter(title=d.title)
                    for h in teams_details:
                        res = {
                            'id':h.pk, 
                            'title':h.title, 
                            'team_image_url':h.image_url,
                            "season_title":season.title,
                            "season_image":season.image_url,
                            "season_code_id":season.code_id
                        }
                        teams.append(res)
                    if lang == "it":
                        msg = "Cerca i dettagli dei record"
                    else:    
                        msg = "Search Records   Details"
                    return Response({"success": "true", "msg":msg , "search":"teams", "data":teams}, status=status.HTTP_200_OK)
            else:
                if lang == "it":
                    msg = "Nessun risultato travato!"
                else:    
                    msg = "Search Record Not Found...!"
                return Response({"success": "false", "msg":msg ,}, status=status.HTTP_200_OK)
        if lang == "it":
            msg = "campi di ricerca Obbligatorio...!"
        else:    
            msg = "search fields Required...!"
        return Response({"success": "false", "msg":msg ,}, status=status.HTTP_200_OK)
class Follow_Category(APIView):

    def post(self, request):
        category = request.data.get('category_id')
        user = request.data.get('user_id')
        lang = request.data.get('lang_code')
        if FavouriteCategories.objects.filter(user_id=user, category_id=category).exists():
            data = Categories.objects.get(id=category)
            sub_category = Categories.objects.filter(parent_id=data.pk)
            for sub_cat in sub_category:
                FavouriteCategories.objects.filter(user_id=user, category_id=sub_cat.pk).delete()
            FavouriteCategories.objects.filter(user_id=user, category_id=category).delete()
            if lang == "it":
                msg = "Categoria Smetti di seguire con successo...!!"
            else:    
                msg = "Category Unfollow  Successfully...!!"
            return Response({"success": "true", "msg":msg ,"follow":"0"}, status=status.HTTP_200_OK)
        else:
            sub = Categories.objects.filter(parent_id=category)
            for fv in sub:
                FavouriteCategories.objects.create(user_id=user, category_id=fv.pk)
            FavouriteCategories.objects.create(user_id=user, category_id=category)
            if lang == "it":
                msg = "Categoria con successo...!!"
            else:    
                msg = "Category  Successfully...!!"
            return Response({"success": "true", "msg":msg ,"follow":"1"}, status=status.HTTP_200_OK)
class Follow_Sub_Category(APIView):
    def post(self, request):
        category_id = request.data.get('category_id')
        user_id = request.data.get("user_id")
        lang = request.data.get('lang_code')

        if category_id or user_id is not None:
            if FavouriteCategories.objects.filter(user_id=user_id, category_id=category_id).exists():
                FavouriteCategories.objects.get(user_id=user_id, category_id=category_id).delete()
                if lang == "it":
                    msg = "Sottocategoria Smetti di seguire con successo...!!"
                else:    
                    msg = "Sub Category Unfollow  Successfully...!! "
                return Response({"success": "true", "msg":msg ,"follows":"0"}, status=status.HTTP_200_OK)
            else:
                FavouriteCategories.objects.create(user_id=user_id, category_id=category_id)
                if lang == "it":
                    msg = "Sottocategoria Seguito con successo...!!"
                else:    
                    msg = "Sub Category Following Successfully...!!"
                return Response({"success": "true", "msg":msg ,"follows":"1"}, status=status.HTTP_200_OK)
        else: 
            if lang == "it":
                msg = "È richiesta la sottocategoria o l'ID utente...!"
            else:    
                msg = "Sub category or User  id is required...!"
            return Response({"success": "false", "msg": msg }, status=status.HTTP_200_OK)
class FavouriteEventsView(APIView):

    def post(self, request):
        event_id = request.data.get('event_id')
        user_id = request.data.get('user_id')
        lang = request.data.get('lang_code')
        if FavouriteEvents.objects.filter(user_id=user_id, event_id=event_id).exists():
            FavouriteEvents.objects.filter(user_id=user_id, event_id=event_id).delete()
            if lang == "it":
                msg = "News correttamente rimossa!"
            else:    
                msg = "News successfully removed!"
            return Response({"success": "true", "msg": msg,}, status=status.HTTP_200_OK)
        else:
            FavouriteEvents.objects.create(user_id=user_id, event_id=event_id)
            if lang == "it":
                msg = "News aggiunta alla lista dei preferiti!"
            else:    
                msg = " News Add In  Favourite News lists Successfully...!!"
            return Response({"success": "true", "msg":msg }, status=status.HTTP_200_OK)

class UserFavouriteEventsLists(APIView):
    def post(self,  request):
        
        user_id = request.data.get("user_id")
        lang = request.data.get('lang_code')
        event = []
        if FavouriteEvents.objects.filter(user_id=user_id).exists():
            favourite_events = FavouriteEvents.objects.filter(user_id=user_id)
            for fav_events in favourite_events:
                data = Posts.objects.filter(id=fav_events.event_id).order_by()
                cat_title = ''
                for post in data:
                    reactions = PostReact.objects.filter(post_id=post.pk).values('reaction').annotate(count=Count('reaction')).order_by('-count')
                    max_reaction = reactions[0]['reaction'] if reactions else 10
                    post_react = PostReact.objects.filter(post_id=post.pk)
                    total_react = post_react.count()
                    total_love = PostReact.objects.filter(post_id=post.pk, reaction=max_reaction).count()
                    max_react_value = 0
                    if total_love!=0:
                        max_react_value = int((total_love*100)/total_react)
                    else:
                        max_react_value = 0
                    reactions = PostReact.objects.filter(post_id=post.pk).values('reaction').annotate(count=Count('reaction')).order_by('-count')
                    max_reaction = reactions[0]['reaction'] if reactions else 10
                    if Categories.objects.filter(id=post.category_id).exists():
                        cat_obj = Categories.objects.get(id=post.category_id)
                        cat_title = cat_obj.title
                    post_react = PostReact.objects.filter(post_id=post.pk)
                    total_react = post_react.count()
                    html_string = post.description
                    cleaned_string = remove_html_tags(html_string)
                    html_about = post.about
                    cleaned_string_about = remove_html_tags(html_about)
                    res = {
                        'id':post.pk, 'max_react_value':max_react_value, 'max_reaction':max_reaction, 'totalPercentage':total_react,  'guid':post.guid, 'provider_profile_id':post.provider_profile_id, 'category_id':post.category_id, 'title':post.title, 'description':cleaned_string, 'about':cleaned_string_about, 'address':post.address, 'start_date':post.start_date, 'end_date':post.end_date,  'image_url':post.image_url, 'link':post.link, 'data':post.data, 'video':post.video,  'created_at':post.created_at, 'updated_at':post.updated_at, 'active':post.active,  "cat_title":cat_title
                    }
                    event.append(res)
            if lang == "it":
                msg = "Post Liste Dettagli"
            else:    
                msg = "Post Lists Details"
            return Response({"success": "true", "msg": msg, "data":event}, status=status.HTTP_200_OK)
        if lang == "it":
            msg = "Nessun dato presente!"
        else:    
            msg = "Record Not Found...!"
        return Response({"success": "false", "msg":msg , }, status=status.HTTP_200_OK)
class PostReactView(APIView):

    def post(self, request):
        lang = request.data.get('lang_code')
        serializer = PostReactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.data['user_id']
        post_id = request.data['post_id']
        reaction = request.data['reaction']
        if reaction==1 or reaction==0 or reaction==2  or reaction==3 or reaction==4:
            if PostReact.objects.filter(user_id=user_id, post_id=post_id ):
                react_update = PostReact.objects.get(user_id=user_id, post_id=post_id ) 
                react_update.reaction=reaction
                react_update.save()
                if lang == "it":
                    msg = "Posta l'aggiornamento della reazione con successo!"
                else:    
                    msg = "Post Reaction Update Successfully!"
                return Response({'msg':msg , 'success': "true"}, status=status.HTTP_200_OK)
            else:   
                PostReact.objects.create(user_id=user_id, post_id=post_id, reaction=reaction )
                if lang == "it":
                    msg = "Post reazione aggiunta con successo!"
                else:    
                    msg = "Post Reaction add Successfully!"
                return Response({'msg':msg , 'success': "true"}, status=status.HTTP_200_OK)
        if lang == "it":
            msg = "Valore post reazione non corrispondente ...!!"
        else:    
            msg = "Post Reaction Value Not Match ...!!"
        return Response({'msg':msg , 'success': "true"}, status=status.HTTP_200_OK)

class PostReactDetails(APIView):

    def post(self, request):
        post_id = request.data.get('post_id')
        user_id = request.data.get('user_id')
        lang = request.data.get('lang_code')
        data = PostReact.objects.filter(post_id=post_id)
        total_react = data.count()
        total_love = PostReact.objects.filter(post_id=post_id, reaction=0).count()
        total_lol = PostReact.objects.filter(post_id=post_id, reaction=1).count()
        total_wow = PostReact.objects.filter(post_id=post_id, reaction=2).count()
        total_sad = PostReact.objects.filter(post_id=post_id, reaction=3).count()
        total_huhh = PostReact.objects.filter(post_id=post_id, reaction=4).count()
        if total_love!=0:
            total_love_percentage = int((total_love*100)/total_react)
        else:
            total_love_percentage = 0
        if total_lol!=0:
            total_lol_percentage = int((total_lol*100)/total_react)
        else:
            total_lol_percentage = 0
        if  total_wow!=0:
            total_wow_percentage = int((total_wow*100)/total_react)
        else:
            total_wow_percentage = 0
        if total_sad!=0:
            total_sad_percentage = int((total_sad*100)/total_react)
        else:
            total_sad_percentage=0
        if total_huhh!=0:
            total_huhh_percentage = int((total_huhh*100)/total_react)
        else:
            total_huhh_percentage = 0
        total_love_percentage = total_love_percentage
        if PostReact.objects.filter(post_id=post_id, user_id= user_id).exists():
            user_reaction = PostReact.objects.get(post_id=post_id, user_id= user_id)
            user_post_reaction = user_reaction.reaction
        else:    
            user_post_reaction=20
        if lang == "it":
            msg = "Valore post reazione non corrispondente ...!!"
        else:    
            msg = "Post Reaction Value Not Match ...!!"
        return Response({"success": "true", "msg":msg, 'user_post_reaction':user_post_reaction, "total_react":total_react, "total_love_percentage":total_love_percentage, "total_lol_percentage":total_lol_percentage,'total_wow_percentage':total_wow_percentage, 'total_sad_percentage':total_sad_percentage, 'total_huhh_percentage':total_huhh_percentage, }, status=status.HTTP_200_OK)

ROLES = {
    'it': {
        0: _('Tutti'),
        1: _('Portiere'),
        2: _('Difensore'),
        3: _('Centrocampista'), 
        5: _('Attaccante')
    },
    'en': {
        0: _('All Roles'),
        1: _('Goalkeeper'),
        2: _('Defender'),
        3: _('Midfielder'),
        5: _('Forward')
    }
}
class RoleListsView(APIView):
    def post(self, request):
        lang = request.data.get('lang_code')
        if lang == "it":
            msg = "Elenco dei ruoli Dettagli"
        else :    
            msg = "Role lists Details"
        if lang in ROLES:
            data = [{'id': id, 'role_name': ROLES[lang][id]} for id in ROLES[lang]]
            return Response({"success": "true", "msg": _(msg), 'data':data }, status=status.HTTP_200_OK)
        else:
            return Response({"success": "false", "msg": _("Invalid language code")}, status=status.HTTP_400_BAD_REQUEST)
    
class GiocateoriLists(APIView):
    def post(self, request):
        role = request.data.get('role')

        team = request.data.get('team')
        lang = request.data.get('lang_code')

        fc_seasons_code_id = request.data.get('code_id')
        if FcSeasons.objects.filter(code_id=fc_seasons_code_id).exists():
            
            if role == 0  and team == team in ["All Teams", "Tutte"] :
                
                data = FcPlayerStats.objects.filter(season_code=fc_seasons_code_id,turn_code_id=360 ).order_by('p_last_name').distinct()
                serializers = GiocatoriRecordsLists(data, many=True)
                if lang == "it":
                    msg = "Giocatori Records Liste...!"
                else :    
                    msg = "Giocatori Records Lists...!"
                return Response({"success":"true", "msg":msg, "data":serializers.data}, status=status.HTTP_200_OK)
            
            elif role == 0 and team == team:
                
                data = FcPlayerStats.objects.filter(season_code=fc_seasons_code_id, r_name=team,turn_code_id=360 ).order_by('p_last_name').distinct()
                serializers = GiocatoriRecordsLists(data, many=True)
                if lang == "it":
                    msg = "Giocateori Records Liste...!"
                else :    
                    msg = "Giocatori Records  Lists...!"
                return Response({"success":"true", "msg":msg, "data":serializers.data}, status=status.HTTP_200_OK)
            
            elif role == role and team in ["All Teams", "Tutte"]: 
                  
                data = FcPlayerStats.objects.filter(season_code=fc_seasons_code_id, pr_role=role, turn_code_id=360).order_by('p_last_name')
                serializers = GiocatoriRecordsLists(data, many=True)
                if lang == "it":
                    msg = "Giocateori Records Liste...!"
                else :    
                    msg = "Giocatori Records Lists...!"
                return Response({"success":"true", "msg":msg , "data":serializers.data}, status=status.HTTP_200_OK)
            
            elif role == role and team == team:
                   
                data = FcPlayerStats.objects.filter(season_code=fc_seasons_code_id, pr_role=role, r_name=team, turn_code_id=360).order_by('p_last_name')
                serializers = GiocatoriRecordsLists(data, many=True)
                if lang == "it":
                    msg = "Giocateori Records Liste...!"
                else :    
                    msg = "Giocatori Records Lists...!"
                return Response({"success":"true", "msg":msg , "data":serializers.data}, status=status.HTTP_200_OK)
            
            else: 
                if lang == "it":
                    msg = "Campi di ruolo o di squadra richiesti..!"
                else :    
                    msg = "Role  or Team  fileds Required..!"
                return Response({"success":"true", "msg":msg }, status=status.HTTP_200_OK)
        if lang == "it":
            msg = "Inserimento non trovato...!"
        else :    
            msg = "Record not found...!"
        return Response({"success":"false", "msg":msg }, status=status.HTTP_200_OK)
    
class PlayerStatus(APIView):
    def post(self, request):
        player_code = request.data.get("player_code_id")
        lang = request.data.get('lang_code')
        player = FcPlayerStats.objects.filter(player_code_id=player_code)
        turn = 1
        if player:
            respone = []
            for xyz in player:
                obj = xyz.season_match_code
                match_team = FcSeasonMatches.objects.filter(code_id=obj.code_id)
                for match in match_team:
                    code = match.turn_code
                    home = FcTeams.objects.get(code_id=match.realteam_id_home)
                    away = FcTeams.objects.get(code_id=match.realteam_id_away)
                    
                    matchs = {
                        'code_id':match.code_id,
                        'turn':turn,
                        'turn_code':code.code_id,
                        'match_date':match.match_date,
                        'home_team_name':home.title,
                        'realteam_id_home':home.image_url,
                        'home_bg_color_rgba':home.bg_color_rgba,
                        'home_app_bg_color_rgba':home.app_bg_color_rgba,
                        'away_team_name':away.title, 
                        'realteam_id_away':away.image_url, 
                        'away_bg_color_rgba':away.bg_color_rgba,
                        'away_app_bg_color_rgba':away.app_bg_color_rgba,
                        'home_score':match.home_score,
                        'away_score':match.away_score,
                        'match_status':match.match_status,
                        'match_timer':match.match_timer,
                    }
                    respone.append(matchs)
                    turn = turn+1
            if lang == "it":
                msg = "Squadre Turni liste...!"
            else :    
                msg = "Teams Turns lists ...!"
            return Response({"success": "true", "msg":msg  , "data":respone}, status=status.HTTP_200_OK)
        if lang == "it":
            msg = "Inserimento non trovato..!"
        else :    
            msg = "Record Not Found..!"
        return Response({"success": "true", "msg": msg }, status=status.HTTP_200_OK)

class TurnsRecordsDetails(APIView):
    def post(self, request):
        player_code_id = request.data.get("player_code_id")
        turn_code_id = request.data.get("turn_code_id")
        lang = request.data.get('lang_code')

        if FcPlayerStats.objects.filter(player_code_id=player_code_id, turn_code_id=turn_code_id).exists():
            data = FcPlayerStats.objects.get(player_code_id=player_code_id, turn_code_id=turn_code_id)
            if data.pr_role == 1:
                pns_goal = str(data.pns_lost_goal) if data.pns_lost_goal is not None else "0"
            else:
                pns_goal = str(data.pns_goal_full) if data.pns_goal_full is not None else "0"
            pns_played = str(data.pns_played) if data.pns_played is not None else "0"
            pi_overall_season_index = str(data.pi_overall_season_index) if data.pi_overall_season_index is not None else "0"
            p_lineup_rating = str(data.p_lineup_rating) if data.p_lineup_rating is not None else "0"
            pns_assist = str(data.pns_assist) if data.pns_assist is not None else "0"
            pns_yellow_card = str(data.pns_yellow_card) if data.pns_yellow_card is not None else "0"
            pns_sub_in = str(data.pns_sub_in) if data.pns_sub_in is not None else "0"
            pl_predicted_note = str(data.pl_predicted_note) if data.pl_predicted_note is not None else "0"

            pns_goal_subout = str(data.pns_goal_subout) if data.pns_goal_subout is not None else "0"
            pns_penalty_saved = ""
            pns_penalty_failed = ""
            if data.pr_role == 1:
                pns_penalty_saved = str(data.pns_penalty_saved) if data.pns_penalty_saved is not None else "0"

            else:    
                pns_penalty_failed = str(data.pns_penalty_failed) if data.pns_penalty_failed is not None else "0"
                pns_penalty_saved = str(data.pns_penalty_saved) if data.pns_penalty_saved is not None else "0"
                
            
            pi_expected_penalty = str(data.pi_expected_penalty) if data.pi_expected_penalty is not None else "0"
            pns_note_win = str(data.pns_note_win) if data.pns_note_win is not None else "0"
            pns_note_lose = str(data.pns_note_lose) if data.pns_note_lose is not None else "0"
            pns_note_last5 = str(data.pns_note_last5) if data.pns_note_last5 is not None else "0"
            pns_score_last5 = str(data.pns_score_last5) if data.pns_score_last5 is not None else "0"
            pns_note = str(data.pns_note) if data.pns_note is not None else "0"
            pr_role = str(data.pr_role) if data.pr_role is not None else "0"
            r_name = str(data.r_name) if data.r_name is not None else "0"
            p_url_xs = str(data.p_url_xs) if data.p_url_xs is not None else "0"
            pl_predicted_note = str(data.pl_predicted_note) if data.pl_predicted_note is not None else "0"
            pns_goal_full = str(data.pns_goal_full) if data.pns_goal_full is not None else "0"
            pi_match_played_perc = str(data.pi_match_played_perc) if data.pi_match_played_perc is not None else "0"
            response = {
                'id':str(data.pk),  
                'player_code_id':str(data.player_code_id) , 
                'turn_code_id':str(data.turn_code_id),  
                'pns_played':pns_played, 
                'pns_goal':pns_goal, 
                'pi_overall_season_index':pi_overall_season_index, 
                'p_lineup_rating':p_lineup_rating, 
                'pns_assist':pns_assist, 
                'pns_yellow_card':pns_yellow_card, 
                'pns_played_draw':pns_sub_in, 
                'pl_predicted_note':pl_predicted_note, 
                'pns_goal_subout':pns_goal_subout, 
                'pns_penalty_saved':pns_penalty_saved ,
                'pns_penalty_failed':pns_penalty_failed, 
                'pi_expected_penalty':pi_expected_penalty, 
                'pns_note_win':pns_note_win, 
                'pns_note_lose':pns_note_lose,
                'pns_note_last5':pns_note_last5, 
                'pns_score_last5':pns_score_last5, 
                'pns_note':pns_note, 
                'pr_role':pr_role, 
                'r_name':r_name, 
                'p_url_xs':p_url_xs, 
                'pl_predicted_note':pl_predicted_note, 
                'pns_goal_full':pns_goal_full, 
                'pi_match_played_perc':pi_match_played_perc
            }   
            if lang=="it":
                msg = "Turns Records Dettagli ...!"
            else :    
                msg = "Turns Records Details ...!"
            return Response({"success": "true", "msg":msg  , "data":response}, status=status.HTTP_200_OK)
        if lang=="it":
            msg = "Record non trovati ...!"
        else :    
            msg = "Records Not Found ...!"
        return Response({"success": "false", "msg":msg }, status=status.HTTP_200_OK)
class FcSeasonSquadreLists(APIView):
    def post(self, request):
        season_id = request.data.get('code_id')
        lang = request.data.get('lang_code')
        if FcSeasonTeams.objects.filter(season_code=season_id).exists():
            teams = FcSeasonTeams.objects.filter(season_code=season_id)
            result = []
            for t in teams:
                data = FcTeams.objects.filter(code_id=t.team_code_id).order_by('title')
                for team in data:
                    res = {
                        'id':team.pk,
                        'title': team.title,
                        'code_id':team.code_id,
                        'image_url':team.image_url
                    }
                    result.append(res)
            result = sorted(result, key=lambda x: x['title'])  # sort the result list by title
            if lang == "it":
                msg = "Liste squadre per stagione...!"
            else :    
                msg = "Teams Lists By Season ...!"
            return Response({"success": "true", "msg":msg ,"data":result}, status=status.HTTP_200_OK)
        else:
            if lang == "it":
                msg = "Inserimento non trovato..!"
            else :    
                msg = " Record Not Found..!"
            return Response({"success": "false", "msg":msg,})
class SeasonTeamsPlayers(APIView):
    def post(self, request):
        team_code_id = request.data.get('code_id')
        lang = request.data.get('lang_code')

        teams = FcPlayerStats.objects.filter(team_code_id=team_code_id)
        plys = []
        for team in teams:
            players = FcPlayers.objects.filter(code_id=team.player_code_id)
            for ply in players:
                p = {
                    'first_name':ply.first_name,
                    'last_name':ply.last_name, 
                    'birth_date':ply.birth_date, 
                    'code_role':ply.code_role, 
                    'image_url':ply.image_url, 
                    'main_role':ply.main_role, 
                    'code_id':ply.code_id,
                }
                plys.append(p)
        if lang == "it":
            msg = "Elenchi dei record dei giocatori per squadra ...!"
        else :    
            msg = "Players Records Lists By Team ...!"
        return Response({"success": "true", "msg":msg , "data":plys}, status=status.HTTP_200_OK)

class AllTurnsLists(APIView):
    def post(self, request):
        lang = request.data.get('lang_code')
        response = []
        a = 1
        data = FcTurns.objects.all()
        for turns in data:
            turn = {
                "turn": a,
                "code_id":turns.code_id
            }
            response.append(turn)
            a = a+1
        if lang == "it":
            msg = "Tutti gli elenchi di giri ...!"
        else :    
            msg = "All Turns Lists...!"
        return Response({"success": "true", "msg":msg , "data":response}, status=status.HTTP_200_OK)
        
class CelenderLists(APIView):
    def post(self, request):
        turn = request.data.get('turn')
        team = request.data.get('team')
        lang = request.data.get('lang_code')

        fc_seasons_code_id = request.data.get('season_code_id')
        now = datetime.datetime.now()
        today_date = now.strftime("%Y-%m-%d")
        tomorrow_date = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_date = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if FcSeasons.objects.filter(code_id=fc_seasons_code_id).exists():
            if turn == 0 and team == team in [ "All Teams", "Tutte"]:
                data = FcPlayerStats.objects.filter(season_code=fc_seasons_code_id)[:3]
                if data:
                    respone = []
                    for xyz in data:
                        obj = xyz.season_match_code
                        match_team = FcSeasonMatches.objects.filter(code_id=obj.code_id)[:3]
                        for match in match_team:
                            home = FcTeams.objects.get(code_id=match.realteam_id_home)
                            away = FcTeams.objects.get(code_id=match.realteam_id_away)
                            matchs = {
                                'code_id':match.code_id,
                                'match_date':match.match_date,
                                'home_team_name':home.title,
                                'realteam_id_home':home.image_url,
                                'away_team_name':away.title, 
                                'realteam_id_away':away.image_url, 
                                'home_score':match.home_score,
                                'away_score':match.away_score,
                                'match_status':match.match_status,
                                'match_timer':match.match_timer,
                            }
                            respone.append(matchs)
                    if lang == "it":
                        msg = "Squadre Turni liste...!"
                    else :    
                        msg = "Teams Turns lists ...!"
                    return Response({"success": "true", "msg":msg  , "data":respone}, status=status.HTTP_200_OK)
                if lang == "it":
                    msg = "Inserimento non trovato ...!"
                else:    
                    msg = "Record Not Found ...!"
                return Response({"success": "true", "msg":msg }, status=status.HTTP_200_OK)
            elif turn == 0 and team == team:
                data = FcTeams.objects.get(title=team)
                match_team = FcSeasonMatches.objects.filter(realteam_id_home=data.code_id) or  FcSeasonMatches.objects.filter(realteam_id_away=data.code_id)
                respone = []
                for match in match_team:
                    home = FcTeams.objects.get(code_id=match.realteam_id_home)
                    away = FcTeams.objects.get(code_id=match.realteam_id_away) 
                    matchs = {
                                'code_id':match.code_id,
                                'match_date':match.match_date,
                                'home_team_name':home.title,
                                'realteam_id_home':home.image_url,
                                'away_team_name':away.title, 
                                'realteam_id_away':away.image_url, 
                                'home_score':match.home_score,
                                'away_score':match.away_score,
                                'match_status':match.match_status,
                                'match_timer':match.match_timer,
                            }
                    respone.append(matchs)
                if lang == "it":
                    msg = "Le squadre trasformano le liste dei record...!!"
                else :    
                    msg = "Teams Turns Records  Lists...!"
                return Response({"success": "true", "msg":msg , "data":respone}, status=status.HTTP_200_OK)
            elif turn == turn and team == team in ["All Teams","Tutte"]:
                played = 0
                query = "SELECT * FROM `fc_season_matches` WHERE date(match_date)=%s AND turn_code_id=%s AND played=%s ORDER BY match_date DESC;"
                match_team = FcSeasonMatches.objects.raw(query, [today_date, turn, played])
                today_match = []
                for match in match_team:
                    home = FcTeams.objects.get(code_id=match.realteam_id_home)
                    away = FcTeams.objects.get(code_id=match.realteam_id_away)
                    matchs = {
                                'code_id':match.code_id, 
                                'match_date':match.match_date,
                                'home_team_name':home.title,
                                'realteam_id_home':home.image_url,
                                'away_team_name':away.title, 
                                'realteam_id_away':away.image_url, 
                                'home_score':match.home_score,
                                'away_score':match.away_score,
                                'match_status':match.match_status,
                                'match_timer':match.match_timer,
                            }
                    today_match.append(matchs)
                match_team = FcSeasonMatches.objects.filter(turn_code_id=turn, played="1")
                recent_match = []
                for match in match_team:
                    home = FcTeams.objects.get(code_id=match.realteam_id_home)
                    away = FcTeams.objects.get(code_id=match.realteam_id_away)
                    matchs = {
                                'code_id':match.code_id,
                                'match_date':match.match_date,
                                'home_team_name':home.title,
                                'realteam_id_home':home.image_url,
                                'away_team_name':away.title, 
                                'realteam_id_away':away.image_url, 
                                'home_score':match.home_score,
                                'away_score':match.away_score,
                                'match_status':match.match_status,
                                'match_timer':match.match_timer,
                            }
                    recent_match.append(matchs)
                played = 0    
                query = "SELECT * FROM `fc_season_matches` WHERE played=%s AND turn_code_id=%s ORDER BY match_date DESC;"
                match_team = FcSeasonMatches.objects.raw(query, [played, turn])
                coming_match = []
                for match in match_team:
                    home = FcTeams.objects.get(code_id = match.realteam_id_home)
                    away = FcTeams.objects.get(code_id = match.realteam_id_away)
                    matchs = {
                                'code_id':match.code_id,
                                'match_date':match.match_date,
                                'home_team_name':home.title,
                                'realteam_id_home':home.image_url,
                                'away_team_name':away.title, 
                                'realteam_id_away':away.image_url, 
                                'home_score':match.home_score,
                                'away_score':match.away_score,
                                'match_status':match.match_status,
                                'match_timer':match.match_timer,
                            }
                    coming_match.append(matchs)
                if lang == "it":
                    msg = "Squadre Turni liste...!"
                else :    
                    msg = "Teams Turns lists ...!"
                return Response({"success": "true", "msg":msg  , "today_match":today_match, 'recent_match':recent_match, 'coming_match':coming_match}, status=status.HTTP_200_OK)
      
            elif turn == turn and team == team:

                team = FcTeams.objects.get(title = team)
                turn = FcTurns.objects.get(code_id = turn)   
                match = FcSeasonMatches.objects.filter(turn_code = turn.code_id,realteam_id_home = team.code_id ) | FcSeasonMatches.objects.filter(turn_code=turn.code_id,realteam_id_away=team.code_id ) 
                for match in  match:
                    home = FcTeams.objects.get(code_id=match.realteam_id_home)
                    away = FcTeams.objects.get(code_id=match.realteam_id_away)
                    respone = []
                    matchs = {
                        'code_id':match.code_id,
                        'match_date':match.match_date,
                        'home_team_name':home.title,
                        'realteam_id_home':home.image_url,
                        'away_team_name':away.title, 
                        'realteam_id_away':away.image_url, 
                        'home_score':match.home_score,
                        'away_score':match.away_score,
                        'match_status':match.match_status,
                        'match_timer':match.match_timer,
                        }
                    respone.append(matchs)
                    return Response({"success":"true", "msg":"Turns  Records by Turns And Teams...!", "today_match":respone}, status=status.HTTP_200_OK)
                if lang == "it":
                    msg = "Inserimento non trovato...! "
                else:    
                    msg = "Record not found...! "
                return Response({"success":"false", "msg":msg}, status=status.HTTP_200_OK)
        if lang == "it":
            msg = "Inserimento non trovato...! "
        else:    
            msg = "Record not found...! "
        return Response({"success":"false", "msg":msg}, status=status.HTTP_200_OK)

class Welcome_Screen(APIView):
    def post(self, request):
        welcome_data = WelcomeScreen.objects.filter().first()
        if welcome_data:
            welcome = {
                'heading':welcome_data.heading,
                'description':welcome_data.description, 
                }
            return Response({"success":"true", "msg":"Welcome","data":welcome }, status=status.HTTP_200_OK)
        return Response({"success":"false", "msg":"Record not found...! "}, status=status.HTTP_200_OK)

class Fantacalcio_Image(APIView):
    def post(self, request):
        fant_img = FantacalcioImages.objects.all()
        lang = request.data.get('lang_code')

        response = []
        for data in fant_img:
            res = {
                'heading':data.heading,
                'image_url':data.image_url.url
                }
            response.append(res)
        if lang == "it":
            msg = "Fantacalcio "
        else:    
            msg = "Fantasy football "
        return Response({"success":"true", "msg":msg,"data":response }, status=status.HTTP_200_OK)
class InfomationSettings(APIView):
    def post(self, request):
        lang = request.data.get('lang_code')
        data = Settings.objects.get(key='reg_details')
        response = {
                'key':data.key,
                'value':remove_html_tags(data.value).replace('&nbsp;', ' ')
                }
        if lang == "it":
            msg = "Impostazioni Informazioni Dettagli"
        else:    
            msg = "Settings Information Details "
        return Response({"success":"true", "msg":msg ,"data":response }, status=status.HTTP_200_OK)
class WelcomeScreenss(APIView):

    def post(self, request):
        data  = Introductions.objects.filter(active=1)
        lang = request.data.get('lang_code')
        if data:
            serializers = WelcomeScreenSerializer(data, many=True)
            if lang == "it":
                msg = "Benvenuta"
            else:    
                msg = "Welcome"
            return Response({"success":"true", "msg":msg,"data":serializers.data }, status=status.HTTP_200_OK)
        else:
            if lang == "it":
                msg = "Inserimento non trovato..!"
            else:    
                msg = "Record Not Found..!"
            return Response({"success":"false", "msg":msg }, status=status.HTTP_200_OK)

########  Web View Page Views ############
class About_Us_Page(View):
    def get(self, request):
        
        data = Settings.objects.get(key='about_us')
        soup = BeautifulSoup(data.value, 'html.parser')
        content = soup.get_text()
        return render(request, 'about_us_page.html', {"data":content})

class Privacy_Policy_Page(View):

    def get(self, request):
        data = Settings.objects.get(key='privacy_policy')
        soup = BeautifulSoup(data.value, 'html.parser')
        content = soup.get_text()
        return render(request, 'privacy_policy.html', {"data":content})
class TermsConditionsPage(View):

    def get(self, request):
        data = Settings.objects.get(key='terms')
        soup = BeautifulSoup(data.value, 'html.parser')
        content = soup.get_text()
        return render(request, 'terms_conditions.html', {"data":content})

# def updateplayerImages():
#         data = FcPlayers.objects.all()
#         for d in data:
#             k = FcPlayerStats.objects.filter(player_code_id=d.code_id).all()
#             k.update(p_url_xs=d.image_url)

class PostLists(APIView):

    def post(self, request):
        lang = request.data.get('lang_code')
        post = Posts.objects.all()
        total_posts = post.count()
        user_id = request.data.get('user_id')
        now = datetime.datetime.now()
        today_date = now.strftime("%Y-%m-%d")
        if Users.objects.filter(id=user_id).exists():
            data = Posts.objects.filter(
            category_id__in=FavouriteCategories.objects.filter(user_id=user_id).order_by('-id').values('category_id') ,
            active=1,
            end_date__gte=today_date
                ).order_by('-start_date')      
            cat_title = ''
            results = []
            if data:
                page = request.data.get('page')
                paginator = Paginator(data, 10)
                post_lists = paginator.get_page(page)
                for post in post_lists:
                    if Categories.objects.filter(id=post.category_id).exists():
                        cat_obj = Categories.objects.get(id=post.category_id)
                        cat_title = cat_obj.title 
                    reactions = PostReact.objects.filter(post_id=post.pk).values('reaction').annotate(count=Count('reaction')).order_by('-count')
                    max_reaction = reactions[0]['reaction'] if reactions else 10    
                    post_react = PostReact.objects.filter(post_id=post.pk)
                    total_react = post_react.count()
                    total_love = PostReact.objects.filter(post_id=post.pk, reaction=max_reaction).count()
                    
                    max_react_value = 0
                    if total_love!=0:
                        max_react_value = int((total_love*100)/total_react)
                    else:
                        max_react_value = 0
                    title = strip_tags(post.title).replace('&nbsp;', ' ')
                    html_string = post.description
                    cleaned_string = strip_tags(html_string).replace('&nbsp;', ' ')
                    html_about = post.about
                    cleaned_string_about = strip_tags(html_about).replace('&nbsp;', '')
                    res = {
                        'id': post.pk,
                        'max_react_value':max_react_value,
                        'max_reaction': max_reaction,
                        'totalPercentage': total_react,
                        'guid': post.guid,
                        'provider_profile_id': post.provider_profile_id,
                        'category_id': post.category_id,
                        'title': _(post.title), 
                        'description': _(cleaned_string), 
                        'about': _(cleaned_string_about), 
                        'address': post.address,
                        'start_date': post.start_date,
                        'end_date': post.end_date,
                        'image_url': post.image_url,
                        'link': post.link,
                        'data': post.data,
                        'video': post.video,
                        'created_at': post.created_at,
                        'updated_at': post.updated_at,
                        'active': post.active,
                        "cat_title": _(cat_title), 
                        }
                    results.append(res)
                if lang == "it":
                    msg = "Elenchi record di notizie...!"
                else:    
                    msg = "News Record Lists...!"    
                return Response({"success": "true", "msg": msg, 'total_posts':total_posts, "data":results}, status=status.HTTP_200_OK)
            if lang == "it":
                msg = "Notizie Record non trovati...!"
            else:    
                msg = "News Records Not Found...!"
            return Response({"success": "false", "msg":msg}, status=status.HTTP_200_OK)
        else:
            post = Posts.objects.all()
            total_posts = post.count()
            data = Posts.objects.filter(active=1,  end_date__gte=today_date).exclude(category_id=90).order_by('-start_date')
            paginator = Paginator(data, 10) # 10 is the number of items per page
            page = request.data.get('page') # get the current page number from query parameters
            post_lists = paginator.get_page(page)
            results = []
            cat_title = ''
            for post in post_lists:
                reactions = PostReact.objects.filter(post_id=post.pk).values('reaction').annotate(count=Count('reaction')).order_by('-count')
                max_reaction = reactions[0]['reaction'] if reactions else 10
                if Categories.objects.filter(id=post.category_id).exists():
                    cat_obj = Categories.objects.filter(id=post.category_id).exclude(title='E-SPORTS')
                    for c in cat_obj:
                        cat_title = c.title
                post_react = PostReact.objects.filter(post_id=post.pk)
                total_react = post_react.count()
                total_love = PostReact.objects.filter(post_id=post.pk, reaction=max_reaction).count()
                max_react_value = 0
                if total_love!=0:
                    max_react_value = int((total_love*100)/total_react)
                else:
                    max_react_value = 0
                html_string = post.description
                cleaned_string = strip_tags(html_string).replace('&nbsp;', ' ')
                html_about = post.about
                cleaned_string_about = strip_tags(html_about).replace('&nbsp;', ' ')
                res = {
                    'id':post.pk, 'max_react_value':max_react_value,  'max_reaction':max_reaction, 'totalPercentage':total_react,  'guid':post.guid, 'provider_profile_id':post.provider_profile_id, 'category_id':post.category_id, 'title':post.title, 'description':cleaned_string, 'about':cleaned_string_about, 'address':post.address, 'start_date':post.start_date, 'end_date':post.end_date,  'image_url':post.image_url, 'link':post.link, 'data':post.data, 'video':post.video,  'created_at':post.created_at, 'updated_at':post.updated_at, 'active':post.active,  "cat_title":cat_title
                }
                results.append(res)
            if lang == "it":
                msg = "Elenchi record di notizie...!"
            else:    
                msg = "News Record Lists...!"
            return Response({"success": "true", "msg":msg,  'total_posts':total_posts, "data":results}, status=status.HTTP_200_OK)