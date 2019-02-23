import random
import math

player_cnt = int(input('Enter number of players: '))
if player_cnt < 5:
    print('Unfortunately, you can\'t play with less than 5 people :(')

assassin_cnt = math.floor(1 + (player_cnt - 5) / 4)
police_cnt = math.floor(1 + (player_cnt - 5) / 5)
suicidal_cnt = 1
doctor_cnt = 1 + (player_cnt >= 10)
mutilator_cnt = 1 + (player_cnt >= 10)
potato_cnt = player_cnt - assassin_cnt - police_cnt - suicidal_cnt - doctor_cnt - mutilator_cnt

role_list = []
for i in range(assassin_cnt):
    role_list.append('assassin')

for i in range(police_cnt):
    role_list.append('policeman')

role_list.append('suicidal dude')

for i in range(doctor_cnt):
    role_list.append('doctor')

for i in range(mutilator_cnt):
    role_list.append('mutilator')

for i in range(potato_cnt):
    role_list.append('townie')

random.shuffle(role_list)

player_roles = {}
for i in range(player_cnt):
    curr_name = input('Please enter your name: ')
    while (curr_name in player_roles):
        curr_name = input('Someone has already claimed your name! Please choose another name: ')

    rand_index = random.randint(0, len(role_list) - 1)
    player_roles[curr_name] = role_list.pop(rand_index);

# TODO: (Lulu) Make a UI so that everyone can find out their roles kthxbye


