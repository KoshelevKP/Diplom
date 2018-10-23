import requests
from urllib.parse import urlencode
import time
import json


def get_id(user_id, token):
    '''
    Функция возвращает id (целое число) пользователя по имени или id пользвателя.
    На вход подается имя ользователя ввиде строки или id.
    Если на входе id не задан строкой функция вернет начальное значение id.
    '''
    if type(user_id) is str:  
        
        flag = False
        
        for letter in user_id: #проверка является ли входная строка числом
            if letter not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                flag = True
        
        if flag: #если входная не является числом            
            params = {
                      'screen_name': user_id,
                      'access_token': token,
                      'v': '5.74'
                     }

            response = requests.get('https://api.vk.com/method/utils.resolveScreenName',params)
            if 'object_id' in response.json()['response']: #Проверка получен ли овет
                user_id = response.json()['response']['object_id']
            else:
                user_id = None
            
            
        else: #если сторка число преобразовать строку в целое  
            user_id = int(user_id) 
        
    return user_id


def get_friends(user_id, token):
    '''
    функция возвращает список id друзей пользователя.
    На вход функции подается id пользователя ввиде целого числа.
    '''
    user_id = get_id(user_id, token)
    if user_id == None:
        return None
    
    params = {
              'user_id': user_id,
              'access_token': token,
              'v': '5.74'
            }
    
    response = requests.get('https://api.vk.com/method/friends.get',params)
    freinds_id = response.json()['response']['items']
    
    return freinds_id


def get_groups(user_id, token):
    '''
    функция возвращает список id групп пользователя.
    На вход функции подается id пользователя ввиде целого числа.
    '''
    user_id = get_id(user_id, token)
    if user_id == None:
        return None
    
    params = {
              'user_id': user_id,
              'access_token': token,
              'v': '5.74'
            }
    
    response = requests.get('https://api.vk.com/method/groups.get',params)
    groups_id = response.json()['response']['items']
    
    return groups_id


def get_groups_user(group_id, token, count, groups_count):
    '''
    функция возвращает список id пользователей состоящих в группе.
    На вход функции подается id группы ввиде целого числа.
    В случае если запрос выдает ошибку функция возвращает None.
    '''
    params = {
              'access_token': token,
              'v': '5.74',
              'group_id': group_id,
              'offset': 0,
              'count': 1000
             }
    
    response = requests.get('https://api.vk.com/method/groups.getMembers',params)
    
    if 'response' in response.json(): #Проверка получен ли списоко пользователей группы
        group_members = response.json()['response']['items']
        user_check = 1000
        user_count = response.json()['response']['count']
    else:
        time.sleep(2)
        print('error get_groups_user')
        response = requests.get('https://api.vk.com/method/groups.getMembers',params)
        if 'response' in response.json(): #Проверка получен ли списоко пользователей группы
            group_members = response.json()['response']['items']
            user_check = 1000
            user_count = response.json()['response']['count']
        else:
            print('error get_groups_user')
            group_members = None
        
    if group_members != None:
        while user_check < user_count:
            params = {
              'access_token': token,
              'v': '5.74',
              'group_id': group_id,
              'offset': user_check,
              'count': 1000
             }
            response = requests.get('https://api.vk.com/method/groups.getMembers',params)
            if 'response' in response.json(): #Проверка получен ли овет    
                group_members += response.json()['response']['items']
                
                flag = True
                
                user_check = len(group_members)
                print(count, '/', groups_count, 'групп проверено', 'получено иноформации о пользователях группы', user_check, '/', response.json()['response']['count'])
            else:
                time.sleep(1)
                if flag == False:
                    user_check += 1000
                flag = False
            
    time.sleep(1)        
    return group_members


def chek_group_for_frends(freinds_id, group_members):
    '''
    Функция проверяет состоят ли подьзоатлеи в группе.
    На вход подаются список id друзей и список id пользователей группы.
    В случае если id из списка друзей не встречается в списке пользователей группы функция возвращает True,
    в противном случе False.
    '''
    
    flag = True
    
    if group_members == None:
        flag = False
    
    if group_members != None:
        for friend in freinds_id:
            if friend in group_members:
                flag = False
                
    return flag
        
 
def get_group_info(group_id, token, members_count):
    '''
    Функция возвращает словарь с информацией о группе.
    На вход подается id группы и количество пользователей в группе.
    Словарь содержит информацию о имени группы, id и количестве пользователей в группе.
    В словаре используются следующие ключи:
        'Name', 'id', 'members_count'.
    '''
    
    params = {
              'access_token': token,
              'v': '5.74',
              'group_id': group_id 
             }
    
    response = requests.get('https://api.vk.com/method/groups.getById',params)

    group_info = {
                  'Name': response.json()['response'][0]['name'],
                  'id': response.json()['response'][0]['id'],
                  'members_count': members_count
                 }
    
    return group_info



def find_groups(user_id, token):
    '''
    Функция осуществляет поиск групп в которых состоит пользователь но при этом в них не сотоят его друзья.
    
    На вход функции подается id пользователя или его имя,
    имя пользователя должно быть ввиде строки,
    id пользователя может быть ввиде целого числа или строки,
    если id записанно ввиде строки в нем не дожно юыть испоьзовано букв.
    Пример использования функции
        find_groups('eshmargunov', token)
        find_groups('171691064', token)
        find_groups(171691064, token).
    
    Функция возвращает список с иформацией о группах в которых состоит пользователь но отсутсвуют его друзья.
        Список сотоит из словарь с информацией о имени группы, id и количестве пользователей в группе.
        В словаре используются следующие ключи:
            'Name', 'id', 'members_count'.
            
    Функция сохраняет полученныю информцию в файл output в формате json.
    
    Функция выводит информацию о количестве проверенных групп.
    '''
    freinds_id = get_friends(user_id, token)
    if freinds_id == None:
        print ('Пользоваьеля с таким id или именем не существует')
        return None
    
    groups_id = get_groups(user_id, token)
    if groups_id == None:
        print ('Пользоваьеля с таким id или именем не существует')
        return None

    groups_alone_id = []
    count = 0
    
    time.sleep(1) #задержка выполнения прогрыммы необходимая из-за ограничения на количестов запрсов API

    for group_id in groups_id:

        group_members = get_groups_user(group_id, token, count, len(groups_id))
    
        if chek_group_for_frends (freinds_id, group_members): #Если друзья не состоят в группе
            group_info =  get_group_info(group_id, token, len(group_members))
            groups_alone_id.append(group_info)
            
        count += 1 #подсчет количества проверенных групп
        print(count, '/', len(groups_id), 'групп проверено')
        
        time.sleep(1) #задержка выполнения прогрыммы необходимая из-за ограничения на количестов запрсов API

    with open("groups.json", "w", encoding="utf-8") as file:
        json.dump(groups_alone_id, file, ensure_ascii=False, indent=2)
        
    return groups_alone_id


token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

#user_id = input('введите id ')
user_id = 'eshmargunov'

find_groups(user_id, token)

