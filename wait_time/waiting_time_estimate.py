import firebase_admin
import random
import threading
from time import sleep
from firebase_admin import credentials
from firebase_admin import db
from thinkbayes2 import Suite


cred = credentials.Certificate('myKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://graduate-work-462b3.firebaseio.com'
})

JongHap_real_time_track = db.reference('Restaurant_DB/Real_time/JongHap/')
Olive_real_time_track = db.reference('Restaurant_DB/Real_time/Olive/')
Sanyung_real_time_track = db.reference('Restaurant_DB/Real_time/Sanyung/')
TIP_real_time_track = db.reference('Restaurant_DB/Real_time/TIP/')
Menu_track = db.reference('Menu_DB/')
v = []

global PAST_finish_time  # 이전 조리 완료 시간 ( ti-1 )
global count
global cnt
global sample_num
global finish_time

di = []
JongHap_Menu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Olive_Menu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Sanyung_Menu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
TIP_Menu = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def load_menu(restaurant):
    global JongHap_Menu
    global Olive_Menu
    global Sanyung_Menu
    global TIP_Menu

    l_snapshot = Menu_track.child(restaurant + '/').get()
    count_sum = 0
    for R_key in l_snapshot:
        if restaurant == 'JongHap':
            JongHap_Menu[count_sum] = db.reference('Menu_DB/%s/%s/menu_name' % (restaurant, R_key)).get()
        elif restaurant == 'Olive':
            Olive_Menu[count_sum] = db.reference('Menu_DB/%s/%s/menu_name' % (restaurant, R_key)).get()
        elif restaurant == 'Sanyung':
            Sanyung_Menu[count_sum] = db.reference('Menu_DB/%s/%s/menu_name' % (restaurant, R_key)).get()
        elif restaurant == 'TIP':
            TIP_Menu[count_sum] = db.reference('Menu_DB/%s/%s/menu_name' % (restaurant, R_key)).get()

        count_sum += 1


def jonghap_list_insert_count(r_order_food):
    count_sum = 0
    j_count = 0
    for i in range(0, 12):
        if r_order_food == JongHap_Menu[i]:
            j_count = count_sum
        count_sum += 1

    return j_count


def olive_list_insert_count(r_order_food):
    count_sum = 0
    o_count = 0
    for i in range(0, 12):
        if r_order_food == Olive_Menu[i]:
            o_count = count_sum
        count_sum += 1

    return o_count


def sanyung_list_insert_count(r_order_food):
    count_sum = 0
    s_count = 0
    for i in range(0, 12):
        if r_order_food == Sanyung_Menu[i]:
            s_count = count_sum
        count_sum += 1

    return s_count


def tip_list_insert_count(r_order_food):
    count_sum = 0
    t_count = 0
    for i in range(0, 12):
        if r_order_food == TIP_Menu[i]:
            t_count = count_sum
        count_sum += 1

    return t_count


class Calculate(Suite):
    cal = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

    mixes1 = {
        cal[0]: dict(p1=2, p2=3, p3=1, p4=4, p5=2, p6=1, p7=0, p8=1, p9=8, p10=2, p11=1, p12=7),
        cal[1]: dict(p1=3, p2=6, p3=7, p4=1, p5=7, p6=1, p7=9, p8=9, p9=1, p10=2, p11=2, p12=1),
        cal[2]: dict(p1=2, p2=4, p3=3, p4=1, p5=2, p6=1, p7=3, p8=1, p9=11, p10=12, p11=1, p12=10),
        cal[3]: dict(p1=1, p2=1, p3=2, p4=5, p5=3, p6=8, p7=6, p8=4, p9=1, p10=9, p11=11, p12=7),
        cal[4]: dict(p1=1, p2=2, p3=1, p4=3, p5=1, p6=5, p7=1, p8=1, p9=2, p10=10, p11=1, p12=9),
        cal[5]: dict(p1=1, p2=1, p3=1, p4=2, p5=7, p6=3, p7=11, p8=8, p9=5, p10=3, p11=6, p12=1),
        cal[6]: dict(p1=10, p2=10, p3=4, p4=4, p5=1, p6=6, p7=7, p8=15, p9=11, p10=13, p11=4, p12=5),
        cal[7]: dict(p1=12, p2=13, p3=4, p4=0, p5=2, p6=3, p7=7, p8=6, p9=5, p10=11, p11=8, p12=7),
        cal[8]: dict(p1=1, p2=4, p3=6, p4=7, p5=11, p6=16, p7=5, p8=5, p9=12, p10=10, p11=11, p12=1),
        cal[9]: dict(p1=0, p2=0, p3=16, p4=5, p5=4, p6=12, p7=10, p8=11, p9=10, p10=14, p11=13, p12=12),
        cal[10]: dict(p1=6, p2=7, p3=3, p4=1, p5=7, p6=2, p7=0, p8=5, p9=9, p10=7, p11=8, p12=5),
        cal[11]: dict(p1=2, p2=6, p3=6, p4=4, p5=4, p6=6, p7=6, p8=4, p9=1, p10=6, p11=5, p12=6),
        cal[12]: dict(p1=3, p2=7, p3=7, p4=8, p5=8, p6=9, p7=4, p8=1, p9=6, p10=4, p11=7, p12=4),
        cal[13]: dict(p1=4, p2=8, p3=6, p4=6, p5=6, p6=7, p7=8, p8=0, p9=7, p10=6, p11=5, p12=6),
        cal[14]: dict(p1=5, p2=6, p3=4, p4=2, p5=4, p6=4, p7=3, p8=8, p9=5, p10=5, p11=4, p12=4),
        cal[15]: dict(p1=2, p2=3, p3=6, p4=6, p5=6, p6=2, p7=8, p8=0, p9=7, p10=6, p11=9, p12=6),
        cal[16]: dict(p1=1, p2=2, p3=5, p4=1, p5=4, p6=4, p7=3, p8=8, p9=6, p10=5, p11=4, p12=1)
    }

    mixes2 = {
        cal[0]: dict(p1=2, p2=3, p3=1, p4=4, p5=2, p6=1, p7=0, p8=1, p9=8, p10=2, p11=1, p12=7),
        cal[1]: dict(p1=3, p2=6, p3=7, p4=1, p5=7, p6=1, p7=9, p8=9, p9=1, p10=2, p11=2, p12=1),
        cal[2]: dict(p1=2, p2=4, p3=3, p4=1, p5=2, p6=1, p7=3, p8=1, p9=11, p10=12, p11=1, p12=10),
        cal[3]: dict(p1=1, p2=0, p3=2, p4=5, p5=3, p6=8, p7=6, p8=4, p9=1, p10=9, p11=11, p12=7),
        cal[4]: dict(p1=1, p2=2, p3=0, p4=3, p5=1, p6=5, p7=1, p8=1, p9=2, p10=10, p11=1, p12=9),
        cal[5]: dict(p1=1, p2=1, p3=1, p4=2, p5=7, p6=3, p7=11, p8=8, p9=5, p10=3, p11=6, p12=1),
        cal[6]: dict(p1=10, p2=10, p3=4, p4=4, p5=1, p6=6, p7=7, p8=15, p9=11, p10=13, p11=4, p12=5),
        cal[7]: dict(p1=12, p2=13, p3=4, p4=0, p5=2, p6=3, p7=7, p8=6, p9=5, p10=11, p11=8, p12=7),
        cal[8]: dict(p1=1, p2=4, p3=6, p4=7, p5=11, p6=16, p7=5, p8=5, p9=12, p10=10, p11=11, p12=1),
        cal[9]: dict(p1=0, p2=0, p3=16, p4=5, p5=4, p6=12, p7=10, p8=11, p9=10, p10=14, p11=13, p12=12),
        cal[10]: dict(p1=6, p2=7, p3=3, p4=1, p5=7, p6=2, p7=0, p8=5, p9=9, p10=7, p11=8, p12=5),
        cal[11]: dict(p1=2, p2=6, p3=6, p4=4, p5=4, p6=6, p7=6, p8=4, p9=1, p10=6, p11=5, p12=6),
        cal[12]: dict(p1=3, p2=7, p3=7, p4=8, p5=8, p6=9, p7=4, p8=1, p9=6, p10=4, p11=7, p12=4),
        cal[13]: dict(p1=4, p2=8, p3=6, p4=6, p5=6, p6=7, p7=8, p8=0, p9=7, p10=6, p11=5, p12=6),
        cal[14]: dict(p1=5, p2=6, p3=9, p4=9, p5=4, p6=4, p7=3, p8=8, p9=5, p10=5, p11=4, p12=4),
        cal[15]: dict(p1=2, p2=3, p3=6, p4=6, p5=6, p6=2, p7=8, p8=0, p9=7, p10=6, p11=9, p12=6),
        cal[16]: dict(p1=1, p2=2, p3=9, p4=9, p5=4, p6=4, p7=3, p8=8, p9=6, p10=5, p11=4, p12=1)
    }

    mixes3 = {
        cal[0]: dict(p1=2, p2=3, p3=1, p4=4, p5=2, p6=1, p7=0, p8=1, p9=8, p10=2, p11=1, p12=7),
        cal[1]: dict(p1=3, p2=6, p3=7, p4=1, p5=7, p6=1, p7=9, p8=9, p9=1, p10=2, p11=2, p12=1),
        cal[2]: dict(p1=2, p2=4, p3=3, p4=1, p5=2, p6=1, p7=3, p8=1, p9=11, p10=12, p11=1, p12=10),
        cal[3]: dict(p1=1, p2=0, p3=2, p4=5, p5=3, p6=8, p7=6, p8=4, p9=1, p10=9, p11=11, p12=7),
        cal[4]: dict(p1=1, p2=2, p3=0, p4=3, p5=1, p6=5, p7=1, p8=1, p9=2, p10=10, p11=1, p12=9),
        cal[5]: dict(p1=1, p2=1, p3=1, p4=2, p5=7, p6=3, p7=11, p8=8, p9=5, p10=3, p11=6, p12=1),
        cal[6]: dict(p1=10, p2=10, p3=4, p4=4, p5=1, p6=6, p7=7, p8=15, p9=11, p10=13, p11=4, p12=5),
        cal[7]: dict(p1=12, p2=13, p3=4, p4=0, p5=2, p6=3, p7=7, p8=6, p9=5, p10=11, p11=8, p12=7),
        cal[8]: dict(p1=1, p2=4, p3=6, p4=7, p5=11, p6=16, p7=5, p8=5, p9=12, p10=10, p11=11, p12=1),
        cal[9]: dict(p1=0, p2=0, p3=16, p4=5, p5=4, p6=12, p7=10, p8=11, p9=10, p10=14, p11=13, p12=12),
        cal[10]: dict(p1=6, p2=7, p3=3, p4=1, p5=7, p6=2, p7=0, p8=5, p9=9, p10=7, p11=8, p12=5),
        cal[11]: dict(p1=2, p2=6, p3=6, p4=4, p5=4, p6=6, p7=6, p8=4, p9=1, p10=6, p11=5, p12=6),
        cal[12]: dict(p1=3, p2=7, p3=7, p4=8, p5=8, p6=9, p7=4, p8=1, p9=6, p10=4, p11=7, p12=4),
        cal[13]: dict(p1=4, p2=8, p3=6, p4=6, p5=6, p6=7, p7=8, p8=0, p9=7, p10=6, p11=5, p12=6),
        cal[14]: dict(p1=5, p2=6, p3=9, p4=9, p5=4, p6=4, p7=3, p8=8, p9=5, p10=5, p11=4, p12=4),
        cal[15]: dict(p1=2, p2=3, p3=6, p4=6, p5=6, p6=2, p7=8, p8=0, p9=7, p10=6, p11=9, p12=6),
        cal[16]: dict(p1=1, p2=2, p3=9, p4=9, p5=4, p6=4, p7=3, p8=8, p9=6, p10=5, p11=4, p12=1)
    }

    mixes4 = {
        cal[0]: dict(p1=2, p2=3, p3=1, p4=4, p5=2, p6=1, p7=0, p8=1, p9=8, p10=2, p11=1, p12=7),
        cal[1]: dict(p1=3, p2=6, p3=7, p4=1, p5=7, p6=1, p7=9, p8=9, p9=1, p10=2, p11=2, p12=1),
        cal[2]: dict(p1=2, p2=4, p3=3, p4=1, p5=2, p6=1, p7=3, p8=1, p9=11, p10=12, p11=1, p12=10),
        cal[3]: dict(p1=1, p2=0, p3=2, p4=5, p5=3, p6=8, p7=6, p8=4, p9=1, p10=9, p11=11, p12=7),
        cal[4]: dict(p1=1, p2=2, p3=0, p4=3, p5=1, p6=5, p7=1, p8=1, p9=2, p10=10, p11=1, p12=9),
        cal[5]: dict(p1=1, p2=1, p3=1, p4=2, p5=7, p6=3, p7=11, p8=8, p9=5, p10=3, p11=6, p12=1),
        cal[6]: dict(p1=10, p2=10, p3=4, p4=4, p5=1, p6=6, p7=7, p8=15, p9=11, p10=13, p11=4, p12=5),
        cal[7]: dict(p1=12, p2=13, p3=4, p4=0, p5=2, p6=3, p7=7, p8=6, p9=5, p10=11, p11=8, p12=7),
        cal[8]: dict(p1=1, p2=4, p3=6, p4=7, p5=11, p6=16, p7=5, p8=5, p9=12, p10=10, p11=11, p12=1),
        cal[9]: dict(p1=0, p2=0, p3=16, p4=5, p5=4, p6=12, p7=10, p8=11, p9=10, p10=14, p11=13, p12=12),
        cal[10]: dict(p1=6, p2=7, p3=3, p4=1, p5=7, p6=2, p7=0, p8=5, p9=9, p10=7, p11=8, p12=5),
        cal[11]: dict(p1=2, p2=6, p3=6, p4=4, p5=4, p6=6, p7=6, p8=4, p9=1, p10=6, p11=5, p12=6),
        cal[12]: dict(p1=3, p2=7, p3=7, p4=8, p5=8, p6=9, p7=4, p8=1, p9=6, p10=4, p11=7, p12=4),
        cal[13]: dict(p1=4, p2=8, p3=6, p4=6, p5=6, p6=7, p7=8, p8=0, p9=7, p10=6, p11=5, p12=6),
        cal[14]: dict(p1=5, p2=6, p3=9, p4=9, p5=4, p6=4, p7=3, p8=8, p9=5, p10=5, p11=4, p12=4),
        cal[15]: dict(p1=2, p2=3, p3=6, p4=6, p5=6, p6=2, p7=8, p8=0, p9=7, p10=6, p11=9, p12=6),
        cal[16]: dict(p1=1, p2=2, p3=9, p4=9, p5=4, p6=4, p7=3, p8=8, p9=6, p10=5, p11=4, p12=1)
    }

    def Likelihood(self, data, hypo):
        if sample_num == 1:
            mix = self.mixes1[hypo]
        elif sample_num == 2:
            mix = self.mixes2[hypo]
        elif sample_num == 3:
            mix = self.mixes3[hypo]
        elif sample_num == 4:
            mix = self.mixes4[hypo]

        like = mix[data]
        return like


class CondVar:
    myTurn = 0

    def __init__(self):
        pass


def bayes_inner_fnc(res_name):
    global di
    global PAST_finish_time  # 이전 조리 완료 시간 ( ti-1 )
    global count
    global cnt
    global sample_num
    global finish_time

    if res_name == 'JongHap':
        r_snapshot = JongHap_real_time_track.get()
    elif res_name == 'Olive':
        r_snapshot = Olive_real_time_track.get()
    elif res_name == 'Sanyung':
        r_snapshot = Sanyung_real_time_track.get()
    elif res_name == 'TIP':
        r_snapshot = TIP_real_time_track.get()

    load_menu(res_name)


    if r_snapshot is None:
        print('대기중 메뉴 없음')
        db.reference('Waiting_time_DB/%s/Waiting_time' % res_name).set(str(0))
    else:
        di = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        PAST_finish_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 이전 조리 완료 시간 ( ti-1 )
        count = 0
        cnt = 0
        sample_num = 1

        for R_key in r_snapshot:
            if v is None:
                break
            else:
                # 결제 음식
                r_order_food = db.reference('Restaurant_DB/Real_time/%s/%s/order_food' % (res_name, R_key)).get()
                v.append(r_order_food)

        for R_key in r_snapshot:
            if v is None:
                break

            # 결제 음식
            r_order_food = db.reference('Restaurant_DB/Real_time/%s/%s/order_food' % (res_name, R_key)).get()

            print(v)
            if res_name == 'JongHap':
                count = jonghap_list_insert_count(r_order_food)
            elif res_name == 'Olive':
                count = olive_list_insert_count(r_order_food)
            elif res_name == 'Sanyung':
                count = sanyung_list_insert_count(r_order_food)
            elif res_name == 'TIP':
                count = tip_list_insert_count(r_order_food)

            # 결제 시간 ( pi )
            r_pay_time = db.reference('Restaurant_DB/Real_time/%s/%s/pay_time' % (res_name, R_key)).get()
            finish_time = random.randint(3, 10)
            pre_finish_time = int(r_pay_time) + finish_time  # 현재 조리 완료 시간 ( ti )
            if PAST_finish_time[count] > int(r_pay_time):
                di[count] = pre_finish_time - PAST_finish_time[count]
                if di[count] < 0:
                    di[count] = pre_finish_time - int(r_pay_time)
            else:
                di[count] = pre_finish_time - int(r_pay_time)

            PAST_finish_time[count] = pre_finish_time

            del v[0]

            pmf = Calculate(hypos)
            pmf.Normalize()
            pmf.Update('p%d' % (count + 1))

            max_num = 0

            for hypo, prob in pmf.Items():
                if prob >= max_num:
                    max_num = prob
                    end_hypo = hypo

            if cnt == 0:
                cnt += int(end_hypo)
            elif int(end_hypo) > 3:
                cnt += int(end_hypo) - 3  # 동시에 조리를 할 경우를 상정하여 조금씩 대기시간 차감
            else:
                cnt += int(end_hypo) - 1

            print(end_hypo, max_num)

            print('================================================')

        db.reference('Waiting_time_DB/%s/Waiting_time' % res_name).set(str(cnt))


def delete_inner_fnc(res_name):
    global count
    global finish_time
    global di

    if res_name == 'JongHap':
        r_snapshot = JongHap_real_time_track.get()
    elif res_name == 'Olive':
        r_snapshot = Olive_real_time_track.get()
    elif res_name == 'Sanyung':
        r_snapshot = Sanyung_real_time_track.get()
    elif res_name == 'TIP':
        r_snapshot = TIP_real_time_track.get()

    if r_snapshot is None:
        print('대기중 메뉴 없음')
    else:
        once = 0

        for R_key in r_snapshot:
            if once >= 1:
                break
            else:
                db.reference('Restaurant_DB/Real_time/%s/%s' % (res_name, R_key)).delete()  # 결제 음식
                once += 1

                r_order_food = db.reference('Restaurant_DB/Real_time/%s/%s/order_food' % (res_name, R_key)).get()
                bayes_instance = Calculate()
                print(count)

                if res_name == 'JongHap':
                    count = jonghap_list_insert_count(r_order_food)
                    bayes_instance.mixes1['%d' % di[count]]['p%d' % (count + 1)] += 1
                elif res_name == 'Olive':
                    count = olive_list_insert_count(r_order_food)
                    bayes_instance.mixes2['%d' % di[count]]['p%d' % (count + 1)] += 1
                elif res_name == 'Sanyung':
                    count = sanyung_list_insert_count(r_order_food)
                    bayes_instance.mixes3['%d' % di[count]]['p%d' % (count + 1)] += 1
                elif res_name == 'TIP':
                    count = tip_list_insert_count(r_order_food)
                    bayes_instance.mixes4['%d' % di[count]]['p%d' % (count + 1)] += 1


def bayes_thrd(i_cond, i_turn):
    while True:
        sleep(3)
        
        i_cond.acquire()  # mutex_lock

        bayes_inner_fnc('JongHap')
        bayes_inner_fnc('Olive')
        bayes_inner_fnc('Sanyung')
        bayes_inner_fnc('TIP')

        i_turn.myTurn = 1


        i_cond.notifyAll()  # notify to all consumers
        i_cond.release()  # mutex_unlock


def delete_order(i_cond, i_turn):
    global finish_time

    while True:
        finish_time = random.randint(3, 10)

        sleep(10)

        i_cond.acquire()  # mutex_lock

        delete_inner_fnc('JongHap')
        delete_inner_fnc('Olive')
        delete_inner_fnc('Sanyung')
        delete_inner_fnc('TIP')

        i_turn.myTurn = 1

        i_cond.notifyAll()  # notify to all consumers
        i_cond.release()  # mutex_unlock


hypos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

cond = threading.Condition()
turn = CondVar()

th1 = threading.Thread(target=bayes_thrd, args=(cond, turn))
th2 = threading.Thread(target=delete_order, args=(cond, turn))
th1.start()
th2.start()
