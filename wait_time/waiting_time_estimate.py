import firebase_admin
import random
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
v = []

# "제육볶음", "김치볶음밥", "일반주먹밥", "김치주먹밥", "참치주먹밥", "볼케이노치밥", "스팸마요덮밥", "라면", "오므라이스", "부대찌개", "뚝배기불고기", "돈까스"
di = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
PAST_finish_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 이전 조리 완료 시간 ( ti-1 )

count = 0
cnt = 0

def JongHap_list_insert_count(R_order_food):
    if R_order_food == '제육볶음':
        count = 0
    elif R_order_food == '김치볶음밥':
        count = 1
    elif R_order_food == '일반주먹밥':
        count = 2
    elif R_order_food == '김치주먹밥':
        count = 3
    elif R_order_food == '참치주먹밥':
        count = 4
    elif R_order_food == '볼케이노치밥':
        count = 5
    elif R_order_food == '스팸마요덮밥':
        count = 6
    elif R_order_food == '라면':
        count = 7
    elif R_order_food == '오므라이스':
        count = 8
    elif R_order_food == '부대찌개':
        count = 9
    elif R_order_food == '뚝배기불고기':
        count = 10
    elif R_order_food == '돈까스':
        count = 11
    return count

def Olive_list_insert_count(R_order_food):
    if R_order_food == '제육볶음':
        count = 0
    elif R_order_food == '돈까스김치볶음밥':
        count = 1
    elif R_order_food == '잔치국수':
        count = 2
    elif R_order_food == '돈까스카레덮밥':
        count = 3
    elif R_order_food == '떡국':
        count = 4
    elif R_order_food == '양파돈까스':
        count = 5
    elif R_order_food == '김치볶음밥':
        count = 6
    elif R_order_food == '등심돈까스':
        count = 7
    elif R_order_food == '치즈돈까스':
        count = 8
    elif R_order_food == '카레덮밥':
        count = 9
    elif R_order_food == '김치수제비':
        count = 10
    elif R_order_food == '함박스테이크':
        count = 11
    return count

def Sanyung_list_insert_count(R_order_food):
    if R_order_food == '치즈김밥':
        count = 0
    elif R_order_food == '마요네즈김밥':
        count = 1
    elif R_order_food == '잔치국수':
        count = 2
    elif R_order_food == '제육덮밥':
        count = 3
    elif R_order_food == '갈비탕':
        count = 4
    elif R_order_food == '마파두부':
        count = 5
    elif R_order_food == '김치볶음밥':
        count = 6
    elif R_order_food == '스페셜떡볶이':
        count = 7
    elif R_order_food == '비빔냉면':
        count = 8
    elif R_order_food == '부대찌개':
        count = 9
    elif R_order_food == '물냉면':
        count = 10
    elif R_order_food == '냉모밀':
        count = 11
    return count

def TIP_list_insert_count(R_order_food):
    if R_order_food == '야끼우동':
        count = 0
    elif R_order_food == '짜그리':
        count = 1
    elif R_order_food == '치즈돈까스':
        count = 2
    elif R_order_food == '냉모밀':
        count = 3
    elif R_order_food == '부타동':
        count = 4
    elif R_order_food == '라면':
        count = 5
    elif R_order_food == '마불덮밥':
        count = 6
    elif R_order_food == '컵닭강정':
        count = 7
    elif R_order_food == '김치찌개':
        count = 8
    elif R_order_food == '돈까스김치나베':
        count = 9
    elif R_order_food == '모듬컵밥':
        count = 10
    elif R_order_food == '꼬치어묵우동':
        count = 11
    return count


class calculate(Suite):
    cal = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

    mixes = {
        cal[0]: dict(p1=2, p2=3, p3=1, p4=4, p5=2, p6=1, p7=0, p8=1, p9=8, p10=2, p11=1, p12=7),
        cal[1]: dict(p1=3, p2=6, p3=7, p4=1, p5=7, p6=1, p7=9, p8=9, p9=1, p10=2, p11=2, p12=1),
        cal[2]: dict(p1=2, p2=4, p3=3, p4=1, p5=2, p6=1, p7=3, p8=1, p9=11, p10=12, p11=1, p12=10),
        cal[3]: dict(p1=1, p2=0, p3=2, p4=5, p5=3, p6=8, p7=6, p8=4, p9=1, p10=9, p11=11, p12=7),
        cal[4]: dict(p1=1, p2=2, p3=0, p4=3, p5=1, p6=5, p7=1, p8=1, p9=2, p10=10, p11=1, p12=9),
        cal[5]: dict(p1=1, p2=1, p3=1, p4=2, p5=7, p6=3, p7=11, p8=8, p9=5, p10=3, p11=6, p12=1),
        cal[6]: dict(p1=10, p2=10, p13=4, p4=4, p5=1, p6=6, p7=7, p8=15, p9=11, p10=13, p11=4, p12=5),
        cal[7]: dict(p1=12, p2=13, p3=4, p4=0, p5=2, p6=3, p7=7, p8=6, p9=5, p10=11, p11=8, p12=7),
        cal[8]: dict(p1=1, p2=4, p3=6, p4=7, p5=11, p6=16, p7=5, p8=5, p9=12, p10=10, p11=11, p12=1),
        cal[9]: dict(p1=0, p2=0, p3=16, p4=5, p5=4, p6=13, p7=10, p8=12, p9=10, p10=14, p11=15, p12=12),
        cal[10]: dict(p1=6, p2=7, p3=11, p4=14, p5=12, p6=11, p7=0, p8=15, p9=11, p10=7, p11=8, p12=5),
        cal[11]: dict(p1=2, p2=6, p3=6, p4=4, p5=4, p6=6, p7=6, p8=4, p9=1, p10=6, p11=5, p12=6),
        cal[12]: dict(p1=3, p2=7, p3=7, p4=8, p5=8, p6=9, p7=4, p8=1, p9=6, p10=4, p11=7, p12=4),
        cal[13]: dict(p1=4, p2=8, p3=6, p4=6, p5=6, p6=7, p7=8, p8=0, p9=7, p10=6, p11=5, p12=6),
        cal[14]: dict(p1=5, p2=6, p3=9, p4=9, p5=4, p6=4, p7=3, p8=8, p9=5, p10=5, p11=4, p12=4),
        cal[15]: dict(p1=2, p2=3, p3=6, p4=6, p5=6, p6=2, p7=8, p8=0, p9=7, p10=6, p11=9, p12=6),
        cal[16]: dict(p1=1, p2=2, p3=9, p4=9, p5=4, p6=4, p7=3, p8=8, p9=6, p10=5, p11=4, p12=1)
    }

    def Likelihood(self, data, hypo):
        mix = self.mixes[hypo]
        like = mix[data]
        return like


hypos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

while True:

    JongHap_R_snapshot = JongHap_real_time_track.get()


    di = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    PAST_finish_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 이전 조리 완료 시간 ( ti-1 )
    count = 0
    cnt = 0

    for R_key in JongHap_R_snapshot:
        if v is None:
            break
        else:
            R_order_food = db.reference('Restaurant_DB/Real_time/JongHap/%s/order_food' % R_key).get()  # 결제 음식
            v.append(R_order_food)

    for R_key in JongHap_R_snapshot:
        if v is None:
            break

        R_order_food = db.reference('Restaurant_DB/Real_time/JongHap/%s/order_food' % R_key).get()  # 결제 음식

        print(v)
        count = JongHap_list_insert_count(R_order_food)
        R_pay_time = db.reference('Restaurant_DB/Real_time/JongHap/%s/pay_time' % R_key).get()  # 결제 시간 ( pi )
        PRE_finish_time = int(R_pay_time) + random.randint(3, 10)  # 현재 조리 완료 시간 ( ti )


        if PAST_finish_time[count] > int(R_pay_time):
            di[count] = PRE_finish_time - PAST_finish_time[count]
            if di[count] < 0:
                di[count] = PRE_finish_time - int(R_pay_time)
            else:
                di[count] = PRE_finish_time - int(R_pay_time)

        PAST_finish_time[count] = PRE_finish_time

        del v[0]

        pmf = calculate(hypos)
        pmf.Normalize()
        pmf.Update('p%d' % (count + 1))

        max_num = 0

        for hypo, prob in pmf.Items():
            if prob >= max_num:
                max_num = prob
                end_hypo = hypo

        cnt += int(end_hypo)
        print(end_hypo, max_num)

        # mixes[cal[count]]['p%d' % (di[count] + 1)] += 1
        print('================================================')


    db.reference('Waiting_time_DB/JongHap/Waiting_time').set(str(cnt))


    ################################################################################################################################

    Olive_R_snapshot = Olive_real_time_track.get()

    di = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    PAST_finish_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 이전 조리 완료 시간 ( ti-1 )
    count = 0
    cnt = 0

    for R_key in Olive_R_snapshot:
        if v is None:
            break
        else:
            R_order_food = db.reference('Restaurant_DB/Real_time/Olive/%s/order_food' % R_key).get()  # 결제 음식
            v.append(R_order_food)

    for R_key in Olive_R_snapshot:
        if v is None:
            break

        R_order_food = db.reference('Restaurant_DB/Real_time/Olive/%s/order_food' % R_key).get()  # 결제 음식

        print(v)
        count = Olive_list_insert_count(R_order_food)
        R_pay_time = db.reference('Restaurant_DB/Real_time/Olive/%s/pay_time' % R_key).get()  # 결제 시간 ( pi )
        PRE_finish_time = int(R_pay_time) + random.randint(3, 10)  # 현재 조리 완료 시간 ( ti )


        if PAST_finish_time[count] > int(R_pay_time):
            di[count] = PRE_finish_time - PAST_finish_time[count]
            if di[count] < 0:
                di[count] = PRE_finish_time - int(R_pay_time)
            else:
                di[count] = PRE_finish_time - int(R_pay_time)

        PAST_finish_time[count] = PRE_finish_time

        del v[0]

        pmf = calculate(hypos)
        pmf.Normalize()
        pmf.Update('p%d' % (count + 1))

        max_num = 0

        for hypo, prob in pmf.Items():
            if prob >= max_num:
                max_num = prob
                end_hypo = hypo

        cnt += int(end_hypo)
        print(end_hypo, max_num)

        # mixes[cal[count]]['p%d' % (di[count] + 1)] += 1
        print('================================================')


    db.reference('Waiting_time_DB/Olive/Waiting_time').set(str(cnt))


    ################################################################################################################################

    Sanyung_R_snapshot = Sanyung_real_time_track.get()

    di = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    PAST_finish_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 이전 조리 완료 시간 ( ti-1 )
    count = 0
    cnt = 0

    for R_key in Sanyung_R_snapshot:
        if v is None:
            break
        else:
            R_order_food = db.reference('Restaurant_DB/Real_time/Sanyung/%s/order_food' % R_key).get()  # 결제 음식
            v.append(R_order_food)

    for R_key in Sanyung_R_snapshot:
        if v is None:
            break

        R_order_food = db.reference('Restaurant_DB/Real_time/Sanyung/%s/order_food' % R_key).get()  # 결제 음식

        print(v)
        count = Sanyung_list_insert_count(R_order_food)
        R_pay_time = db.reference('Restaurant_DB/Real_time/Sanyung/%s/pay_time' % R_key).get()  # 결제 시간 ( pi )
        PRE_finish_time = int(R_pay_time) + random.randint(3, 10)  # 현재 조리 완료 시간 ( ti )


        if PAST_finish_time[count] > int(R_pay_time):
            di[count] = PRE_finish_time - PAST_finish_time[count]
            if di[count] < 0:
                di[count] = PRE_finish_time - int(R_pay_time)
            else:
                di[count] = PRE_finish_time - int(R_pay_time)

        PAST_finish_time[count] = PRE_finish_time

        del v[0]

        pmf = calculate(hypos)
        pmf.Normalize()
        pmf.Update('p%d' % (count + 1))

        max_num = 0

        for hypo, prob in pmf.Items():
            if prob >= max_num:
                max_num = prob
                end_hypo = hypo

        cnt += int(end_hypo)
        print(end_hypo, max_num)

        # mixes[cal[count]]['p%d' % (di[count] + 1)] += 1
        print('================================================')


    db.reference('Waiting_time_DB/Sanyung/Waiting_time').set(str(cnt))


    ################################################################################################################################

    TIP_R_snapshot = TIP_real_time_track.get()

    di = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    PAST_finish_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 이전 조리 완료 시간 ( ti-1 )
    count = 0
    cnt = 0

    for R_key in TIP_R_snapshot:
        if v is None:
            break
        else:
            R_order_food = db.reference('Restaurant_DB/Real_time/TIP/%s/order_food' % R_key).get()  # 결제 음식
            v.append(R_order_food)

    for R_key in TIP_R_snapshot:
        if v is None:
            break

        R_order_food = db.reference('Restaurant_DB/Real_time/TIP/%s/order_food' % R_key).get()  # 결제 음식

        print(v)
        count = TIP_list_insert_count(R_order_food)
        R_pay_time = db.reference('Restaurant_DB/Real_time/TIP/%s/pay_time' % R_key).get()  # 결제 시간 ( pi )
        PRE_finish_time = int(R_pay_time) + random.randint(3, 10)  # 현재 조리 완료 시간 ( ti )


        if PAST_finish_time[count] > int(R_pay_time):
            di[count] = PRE_finish_time - PAST_finish_time[count]
            if di[count] < 0:
                di[count] = PRE_finish_time - int(R_pay_time)
            else:
                di[count] = PRE_finish_time - int(R_pay_time)

        PAST_finish_time[count] = PRE_finish_time

        del v[0]

        pmf = calculate(hypos)
        pmf.Normalize()
        pmf.Update('p%d' % (count + 1))

        max_num = 0

        for hypo, prob in pmf.Items():
            if prob >= max_num:
                max_num = prob
                end_hypo = hypo

        cnt += int(end_hypo)
        print(end_hypo, max_num)

        # mixes[cal[count]]['p%d' % (di[count] + 1)] += 1
        print('================================================')


    db.reference('Waiting_time_DB/Tip/Waiting_time').set(str(cnt))

    sleep(10)

    ## n = input()
    ## if n =='':
        ## print('프로그램 종료')
        ## break
