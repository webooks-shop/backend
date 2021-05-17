import urllib.request
import json
import requests
import time
from datetime import datetime
from django.db.models import Avg, Max, Min, Sum, Count
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .models import *
from my_settings import Client_ID, Client_Secret



class FindBookView(View):

    def post(self,request):
        try:
            data = json.loads(request.body)
            book = data['book']
            encText = urllib.parse.quote(book)
            url = "https://openapi.naver.com/v1/search/book?query=" + encText +"&display=10&sort=count"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",Client_ID)
            request.add_header("X-Naver-Client-Secret",Client_Secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                k = response_body.decode('utf-8')
                m = json.loads(k)
                items =[]
                for i in m["items"]:
                    title = i["title"]
                    title = title.replace("<b>","")
                    title = title.replace("</b>","")
                    item ={
                        "title":title,
                        "authors":i["author"],
                        "publisher":i["publisher"],
                        "image":i["image"]
                    }
                    items.append(item)
                    print(items)
                return JsonResponse({"Search_list":items},status=200)
            else:
                print("Error Code:" + rescode)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)


class SaveView(View):
	'''데코레이터 유저인증 변경'''
	def post(self, request):
		data = json.loads(request.body)
		user_id = data['user_id']
		'''책 정보'''
		title = data['title']
		cover_image = data['cover_image']
		author = data['authors']
		publisher = data['publisher']
		
		'''책과 유저 정보'''
		read_time = data['read_time']
		rating = data['rating']
		recommend = data['recommend']

		'''등록되어 있는지 확인하고 없으면 생성'''
		book, _ = Book.objects.get_or_create(
				title = title,
				cover_image = cover_image,
				author = author,
				publisher = publisher
				)
		if Info.objects.filter(book_id = book.id).filter(user_id = user_id):
			Info.objects.filter(book_id = book.id).filter(user_id = user_id).delete()
		Info.objects.create(
				book_id = book.id,
				user_id = user_id,
				rating = rating,
				recommend = recommend
				)
		ReadTime.objects.create(
				book_id = book.id,
				user_id = user_id,
				read_time = read_time
				)
		
		return JsonResponse({"message":"SUCCESS"}, status = 201)


class FilterView(View):
	def get(self,request):
		try:
			group = request.GET.get('group','')
			bf = request.GET.get('bf','')
			
			top = Book.objects.prefetch_related('info_set').annotate(num_books=Count('info')).order_by('-num_books')
			users = User.objects.prefetch_related('info_set').all()
			if group:
				users=users.filter(group=group)
			if bf:
				users=users.filter(bf = bf)
			
			book_list = []
			user_group =[]
			for i in users:
				user_group.append(i.group)
				for j in i.info_set.all():
					book_list.append(j.book_id)
			a = top.filter(id__in=book_list)
			set_user_group = set(user_group)
			user_group=list(set_user_group)
			user_group.sort()
			group={"groups":user_group}
			books=[]
			for qu in a:
				rating=0
				reco=[]
				total=0
				back=0
				for j in qu.info_set.all():
					if j.user.bf ==1 :
						back += 1
					total += 1
					rating += j.rating
					reco.append(j.recommend)
				dict = {
					"book_id":qu.id,
					"title":qu.title,
					"cover_image":qu.cover_image,
					"total":total,
					"back":back,
					"front":total-back,
					"rating":rating/total,
					"recommend":{
						"1":reco.count(1),
						"2":reco.count(2),
						"3":reco.count(3),
						"4":reco.count(4),
						"5":reco.count(5)
					}
				}
				books.append(dict)
			print(books)
			return JsonResponse({"books":books,"groups":user_group},status=200)
		except KeyError as e:
			return HttpResponse({"Message":f"key_error: => {e}"},status = 400)


class MyPageView(View):
	def get(self, request):
		'''데코레이터로 유저인증 변경'''
		user_id = request.GET.get('user','')

		if not user_id:
			return JsonResponse({"message":"not login"},status=400)

		qu = ReadTime.objects.select_related('book').filter(user_id=user_id)
		mybook_list=[]
		for q in qu:
			aa={"title":q.book.title,
				"image":q.book.cover_image,
				"read_time":q.read_time,
				"book_id":q.book.id}
			mybook_list.append(aa)
		my = User.objects.get(id=user_id)
		my_info = {
			"name":my.name,
			"group":my.group,
			"bf":my.bf,
			"image":my.image,
		}
		return JsonResponse({"book":mybook_list,"info":my_info}, status=200)


class UserPageView(View):
	def get(self, request,user_id):
		user_id = user_id
		
		if not user_id:
			return JsonResponse({"message":"해당하는 유저가 없습니다"}, status=400)

		books = ReadTime.objects.select_related('book').filter(user_id=user_id)
		book_list=[]
		for q in books:
			book_info = {
				"title":q.book.title,
				"image":q.book.cover_image,
				"read_time":q.read_time,
				"book_id":q.book.id,
			}
			book_list.append(book_info)
		user = User.objects.get(id=user_id)
		user_info = {
			"name":user.name,
			"group":user.group,
			"bf":user.bf,
			"image":user.image,
		}
		return JsonResponse({"books":book_list,"user_info":user_info}, status=200)
			


class BookDetailView(View):
	def get(self, request,book_id):
		a = Info.objects.select_related('user').filter(book_id=book_id)
		book = Book.objects.get(id=book_id)
		total = a.count()
		back=0
		front=0
		rating=0
		for i in a:
			rating+=i.rating
			if i.user.bf == 1: 
				back += 1
			else:
				front += 1
		dict = {
			"book_id":book.id,
			"title":book.title,
			"cover_image":book.cover_image,
			"author":book.author,
			"publisher":book.publisher,
			"total":total,
			"back":back,
			"front":front,
			"rating":rating/total
		}
		comments = Comment.objects.filter(book_id=book_id)
		if comments:
			comment_list = []
			for comment in comments:
				dic={
					"user_id":comment.user_id,
					"user_name":comment.user.name,
					"user_image":comment.user.image,
					"user_group":comment.user.group,
					"user_bf":comment.user.bf,
					"text":comment.comment,
					"created_at":comment.created_at,
				}
				comment_list.append(dic)
			comment={
				"comment":comment_list
			}
			dict.update(comment)
		return JsonResponse(dict)


class BookCommentView(View):
	'''데코레이터로 유저인증  변경'''
	def post(self, request,book_id):
		data = json.loads(request.body)
		user_id = data['user_id']
		book_id = data['book_id']
		text = data['text']
		

		Comment.objects.create(
				user_id=user_id,
				book_id=book_id,
				comment=text
				)
		return JsonResponse({"message":"SUCCESS"}, status=201)
