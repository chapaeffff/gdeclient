from django.http import HttpResponse
from django.shortcuts import render

import vk

import requests

from .models import *


access_token = 'b4a61bf2e92f709f3997f7863058a52dea5064b82419cf4eaf05bdefa8a2b2a7ab48050d7c48e29cf2863'
session = vk.Session(access_token=access_token)
vk_api = vk.API(session)
v = '5.78'
from time import sleep
import re




search_lines = ['"семейн прав"','неустойка', 'юрист', 'адвокат', 'страховка']#['''"семейное право"'''] # , '"семейное+право"']








def index(request):
    return HttpResponse("Hello, world. You're at the scanner index.")

def search(request, city_id):
    #пусть делает 10 секунд реквестов и останавливается = 30 реквестов
    start_from = 0
    reqs = 0
    portion = 200
    while start_from < 1000: #requests<30 and
        print (reqs)
        for search_line in search_lines:
            r = requests.get('https://api.vk.com/method/newsfeed.search',
                             params={'q': search_line, 'v': v, 'count': portion, 'access_token': access_token, 'start_from':start_from})
            response = r.json()
            sleep(0.33)
            #print(response)

            #searches = vk_api.newsfeed.search(q=search_line, v=v, count=50, start_from = start_from)['items']
            searches = response['response']['items']
            print (start_from)

            start_from+=portion

            if search_line.startswith('"') and search_line.endswith('"'):
                search_line = search_line[1:-1]
            words = search_line.split()

            print (start_from)
            reqs +=1
            for i in range(len(searches)):
                search = searches[i]
                post_id = search['id']
                owner_id = search["owner_id"]
                date = search['date']

                item = search['text']

                if owner_id > 0:
                    user_id = owner_id
                    if not Post.objects.filter(post_owner__user_id=user_id, post_id = post_id).exists(): #если этот пост уже проверялся / (быстрод) либо юзер не из питера

                        #если нет совпадения то не нужен и юзер

                        if (len(words)) > 1:
                            coinc = False
                            re_line = ''
                            for word in words:
                                re_line += word
                                re_line += '.{1,5} '
                            print(re_line)

                            stritem = str(item)
                            stritemlow = stritem.lower()

                            # for line in lines:
                                # result = re.findall(r'\bсемейн.{2,4} \bправ.{1,2}\W', stritemlow)

                            result = re.search(re_line, stritemlow)
                            if result: coinc = True


                        if (len(words)==1) or coinc:
                            user = User.objects.filter(user_id=user_id).first()
                            if not user: #юзера нет в базе
                                print ('no user')
                                user = vk_api.users.get(user_ids=user_id, fields='city', v=v)[0]
                                sleep(0.33)
                                reqs+=1
                                #print (requests)
                                if 'city' in user:
                                    city_id = (user['city']['id'])
                                else:
                                    city_id = 0
                                    #print(owner_id, post_id, city_id)
                                    if city_id == 2:
                                        print ('THERE IS')
                                user, created = User.objects.get_or_create(user_id=user_id,
                                                                           first_name = user['first_name'],
                                                                           last_name = user['last_name'],
                                                                           city_id=city_id)


                            post, created = Post.objects.get_or_create(
                            post_id = post_id, post_owner=user,
                            defaults={'text': search['text'], 'date': search['date'], 'search': search_line})

                            # print (search['text'])

                    #здесь юзер уже точно в базе


                                # video_instance, created = Video.objects.get_or_create(vid=att['video']['id'],
                                #                                                       owner_id=att['video']['owner_id'],
                                #                                                       defaults=video_data_clean)
                                # # print('профиль:', 'http://vk.com/id' + str(uid))
                                # print (search['text'][:200])
                                # print('http://vk.com/wall' + str(search['owner_id']) + '_' + str(search['id']))


    return HttpResponse(" # %s users #2 was updated" %str(reqs))




def results(request, city_id):

    results = Post.objects.filter(post_owner__city_id  = city_id, show = True).exclude(text='').order_by('-date') #
    # lists = List.objects.all()
    return render(request, 'scanner/results.html', {'results': results})
    # print (result)
    #
    # return HttpResponse(" # %s city was listed" %city_id)
