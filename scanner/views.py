from django.http import HttpResponse
from django.shortcuts import render

import vk

from .models import *


access_token = 'b4a61bf2e92f709f3997f7863058a52dea5064b82419cf4eaf05bdefa8a2b2a7ab48050d7c48e29cf2863'
session = vk.Session(access_token=access_token)
vk_api = vk.API(session)
v = '5.78'
from time import sleep
search_lines = ['неустойка']#, '"семейное+право"']







def index(request):
    return HttpResponse("Hello, world. You're at the scanner index.")

def search(request, city_id):
    for search_line in search_lines:
        searches = vk_api.newsfeed.search(q=search_line, v=v, count=100, start_from = 0)['items']
        sleep(0.33)
        requests = 0
        for i in range(100):
            search = searches[i]
            post_id = search['id']
            owner_id = search["owner_id"]

            if owner_id > 0:
                user_id = owner_id
                if not Post.objects.filter(post_owner__user_id=user_id, post_id = post_id).exists(): #если этот пост уже проверялся / (быстрод) либо юзер не из питера

                    user = vk_api.users.get(user_ids=user_id, fields='city', v=v)[0]
                    requests+=1
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
                        defaults={'text': search['text']})


                            # video_instance, created = Video.objects.get_or_create(vid=att['video']['id'],
                            #                                                       owner_id=att['video']['owner_id'],
                            #                                                       defaults=video_data_clean)
                            # # print('профиль:', 'http://vk.com/id' + str(uid))
                            # print (search['text'][:200])
                            # print('http://vk.com/wall' + str(search['owner_id']) + '_' + str(search['id']))
                    sleep(0.33)
    return HttpResponse(" # %s posts was updated" %str(requests))




def results(request, city_id):

    results = Post.objects.filter(post_owner__city_id  = 2)
    # lists = List.objects.all()
    return render(request, 'scanner/results.html', {'results': results})
    # print (result)
    #
    # return HttpResponse(" # %s city was listed" %city_id)
