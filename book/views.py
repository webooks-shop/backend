import urllib.request
import json
import requests
import time

from datetime import datetime
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
            url = "https://openapi.naver.com/v1/search/book?query=" + encText +"&display=7&sort=count"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",Client_ID)
            request.add_header("X-Naver-Client-Secret",Client_Secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                k = response_body.decode('utf-8')
                print(type(k))
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
                return HttpResponse(items)
            else:
                print("Error Code:" + rescode)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)

