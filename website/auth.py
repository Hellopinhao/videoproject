import flask
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import note, activity, user, preference, collection, information, browse, rating, btime, watch
from . import db
import pandas as pd
from datetime import datetime, timezone
from datetime import timedelta
import random
from flask_login import login_user, login_required, logout_user, current_user

# test 250110
from flask import session

auth = Blueprint('auth', __name__)
# ytb_data = pd.read_excel("/home/vidRepVer2/.local/videoProject/YouTube videos.xlsx")
# ytb_data = pd.read_excel("/home/vidRepVer2/.local/videoProject/YouTube videos-with tags.xlsx")
ytb_data = pd.read_excel("/root/experiment/videoproject/Douyin_videos.xlsx")
#total_duration = {timedelta(seconds=0)}
total_duration = {}
# status variables
non_res_count1 = {}
non_res_count2 = {}
non_res_count3 = {}
cat1_end = {}
cat2_end = {}
cat3_end = {}
# variables to store the IDs of the all sets
most_pref = {}
second_most_pref = {}
third_most_pref = {}
indiff_list = {}
low_rel = {}
filler = {}
# variables to store path, option, current catogory, and previous videos
path_record = {}
option = {}
current_cat = {}
pre_cat1 = {}
pre_cat2 = {}
pre_cat3 = {}
pre_filler = {}
rec_round = {}
vid_count = {}
non_res_pai_ind = {}
ready_time  = {}
next_time = {}
actual_browsing_time = {}
ind_browsing_time = {}
prev_browsing_time = {}
prev_duration = {}
pause ={}
pause_duration = {}
#new project
exp_group = {}
cat1_first = {}
cat2_first = {}
cat3_first = {}
cat1_sec = {}
cat2_sec = {}
cat3_sec = {}
rnd1_vids = {}
rnd2_vids = {}
cat1_dur = {}
cat2_dur = {}
cat3_dur = {}
cat1_name = {}
cat2_name = {}
cat3_name = {}
cat1_sec_fin  = {}
cat2_sec_fin  = {}
cat3_sec_fin  = {}
count_dic = {}
intro_time ={}
preference_time = {}
preference_time2 = {}
report_time = {}
r1_bt = {}
pct_data = {}
first_playing_time = {}
#parameters to change
non_res_pct = 0.3
non_res_pai = 2
max_count = 30
max_count_no_filler = 30
cat1_num = 15
cat2_num = 9
cat3_num = 6
non_res_sec = 3

# keyerror bug 250108 test!!!
is_first_time = 1

def get_pref(username, rnd):
    # check for preference indication
    username = username
    if rnd  == 0:
        pre_check = preference.query.filter_by(username=username).first()
        if pre_check:
            # load and sort preferences
            dic = {
                "daily_vlog": pre_check.daily_vlog,
                "dressing": pre_check.dressing,
                "fitness": pre_check.fitness,
                "gourmet": pre_check.gourmet,
                "hair_braided": pre_check.hair_braided,
                "homemade_drinks": pre_check.homemade_drinks,
                "kids": pre_check.kids,
                "livehouse": pre_check.livehouse,
                "makeup": pre_check.makeup,
                "painting": pre_check.painting,
                "pets": pre_check.pet,
                "photography": pre_check.photography,
                "popular_science": pre_check.popular_science,
                "scenery": pre_check.scenery,
                "street_snap": pre_check.street_snap}
            sorted_dic = dict(sorted(dic.items(), key=lambda kv: kv[1], reverse= True))
            sorted_pref = list(sorted_dic.keys())
            cat1 = sorted_pref[0]
            cat2 = sorted_pref[1]
            cat3 = sorted_pref[2]



            cat1_name[username] = cat1
            cat2_name[username] = cat2
            cat3_name[username] = cat3
            # test 250118 next line
            session['cat1_name'] = cat1
            session['cat2_name'] = cat2
            session['cat3_name'] = cat3

            # read videos from Youtube video data
            df1 = ytb_data[ytb_data['category'] == cat1]
            df2 = ytb_data[ytb_data['category'] == cat2]
            df3 = ytb_data[ytb_data['category'] == cat3]
            vids1 = df1['id'].to_list()
            vids2 = df2['id'].to_list()
            vids3 = df3['id'].to_list()
            # determine the Top 3 sets, the H set, and the L set, and randomly shuffle the videos
            global most_pref, second_most_pref, third_most_pref, option, current_cat, non_res_pai_ind, rnd1_vids, cat1_first, cat2_first, cat3_first, rnd2_vids
            if sorted_dic[cat1] > sorted_dic[cat2]:
                most_pref[username] = vids1
                if sorted_dic[cat2] > sorted_dic[cat3]:
                    second_most_pref[username] = vids2
                    third_most_pref[username] = vids3
                else:
                    ran_list = [vids2, vids3]
                    random.shuffle(ran_list)
                    second_most_pref[username] = ran_list[0]
                    third_most_pref[username] = ran_list[1]
            elif (sorted_dic[cat1] == sorted_dic[cat2]) and (sorted_dic[cat2] > sorted_dic[cat3]):
                ran_list = [vids1, vids2]
                random.shuffle(ran_list)
                most_pref[username] = ran_list[0]
                second_most_pref[username] = ran_list[1]
                third_most_pref[username] = vids3
            else:
                ran_list = [vids1, vids2, vids3]
                random.shuffle(ran_list)
                most_pref[username] = ran_list[0]
                second_most_pref[username] = ran_list[1]
                third_most_pref[username] = ran_list[2]
            print(most_pref[username])
            print(second_most_pref[username])
            print(third_most_pref[username])
            random.shuffle(most_pref[username])
            random.shuffle(second_most_pref[username])
            random.shuffle(third_most_pref[username])
            global non_res_pai
            non_res_pai_ind[username] = 999
            #first round and second round
            cat1_first[username] = most_pref[username][0:10]
            cat2_first[username] = second_most_pref[username][0:7]
            cat3_first[username] = third_most_pref[username][0:3]
            cat1_sec[username] = most_pref[username][10:]
            cat2_sec[username] = most_pref[username][7:]
            cat3_sec[username] = most_pref[username][3:]
            cat1_sec_fin[username] = cat1_sec[username]
            cat2_sec_fin[username] = cat2_sec[username]
            cat3_sec_fin[username] = cat3_sec[username]
            rnd1_vids[username] = cat1_first[username] + cat2_first[username] + cat3_first[username]
            random.shuffle(rnd1_vids[username])
            # test 250112
            session['rnd1_vids'] = rnd1_vids[username]

            # test 250118 next six lines
            session['cat1_first'] = cat1_first[username]
            session['cat2_first'] = cat2_first[username]
            session['cat3_first'] = cat3_first[username]
            session['cat1_sec_fin'] = cat1_sec_fin[username]
            session['cat2_sec_fin'] = cat2_sec_fin[username]
            session['cat3_sec_fin'] = cat3_sec_fin[username]


            print(rnd1_vids[username])
            rnd2_vids[username] = cat1_sec[username] + cat2_sec[username] + cat3_sec[username]
            # test 250112
            session['rnd2_vids'] = rnd2_vids[username]

        else:
            flash("No preferences indicated!", category="error")
            return redirect(url_for("views.home"))
    else:
        pre_check = preference.query.filter_by(username=username).limit(2)[1]
        if pre_check:
            # load and sort preferences
            dic = {
                "daily_vlog": pre_check.daily_vlog,
                "dressing": pre_check.dressing,
                "fitness": pre_check.fitness,
                "gourmet": pre_check.gourmet,
                "hair_braided": pre_check.hair_braided,
                "homemade_drinks": pre_check.homemade_drinks,
                "kids": pre_check.kids,
                "livehouse": pre_check.livehouse,
                "makeup": pre_check.makeup,
                "painting": pre_check.painting,
                "pets": pre_check.pet,
                "photography": pre_check.photography,
                "popular_science": pre_check.popular_science,
                "scenery": pre_check.scenery,
                "street_snap": pre_check.street_snap}
            sorted_dic = dict(sorted(dic.items(), key=lambda kv: kv[1], reverse=True))
            sorted_pref = list(sorted_dic.keys())
            cat1 = sorted_pref[0]
            cat2 = sorted_pref[1]
            cat3 = sorted_pref[2]
            session['cat1_sec_name'] = cat1
            session['cat2_sec_name'] = cat2
            session['cat3_sec_name'] = cat3
            # read videos from Youtube video data
            df1 = ytb_data[ytb_data['category'] == cat1]
            df2 = ytb_data[ytb_data['category'] == cat2]
            df3 = ytb_data[ytb_data['category'] == cat3]
            vids1 = df1['id'].to_list()
            vids2 = df2['id'].to_list()
            vids3 = df3['id'].to_list()
            vids1_sec = vids1
            vids2_sec = vids2
            vids3_sec = vids3
            if sorted_dic[cat1] > sorted_dic[cat2]:
                most_pref[username] = vids1
                if sorted_dic[cat2] > sorted_dic[cat3]:
                    second_most_pref[username] = vids2
                    third_most_pref[username] = vids3
                else:
                    ran_list = [vids2, vids3]
                    random.shuffle(ran_list)
                    second_most_pref[username] = ran_list[0]
                    third_most_pref[username] = ran_list[1]
            elif (sorted_dic[cat1] == sorted_dic[cat2]) and (sorted_dic[cat2] > sorted_dic[cat3]):
                ran_list = [vids1, vids2]
                random.shuffle(ran_list)
                most_pref[username] = ran_list[0]
                second_most_pref[username] = ran_list[1]
                third_most_pref[username] = vids3
            else:
                ran_list = [vids1, vids2, vids3]
                random.shuffle(ran_list)
                most_pref[username] = ran_list[0]
                second_most_pref[username] = ran_list[1]
                third_most_pref[username] = ran_list[2]
            vids1 = most_pref[username]
            vids2 = second_most_pref[username]
            vids3 = third_most_pref[username]
            #avoid repetition
            # test 250112
            rnd1_vids[username] = session.get('rnd1_vids')
            # test 250112
            rnd2_vids[username] = session.get('rnd2_vids')

            for v in rnd1_vids[username]:
                if v in vids1:
                    vids1.remove(v)
                elif v in vids2:
                    vids2.remove(v)
                elif v in vids3:
                    vids3.remove(v)
            cat1_sec_fin[username] = vids1[0:2]
            cat2_sec_fin[username] = vids2[0:2]
            cat3_sec_fin[username] = vids3[0:2]
            print('video-round2-set1')
            print(cat1_sec_fin)
            print('video-round2-set2')
            print(cat2_sec_fin)
            print('video-round2-set3')
            print(cat3_sec_fin)
            # test 250122
            rnd2_vids[username] = (vids1[0:2] + vids2[0:2] + vids3[0:2])[0:6]
            #rnd2_vids[username] = (vids1[0:2] + vids2[0:2] + vids3[0:2])[0:5]
            random.shuffle(rnd2_vids[username])
            # test 250112
            session['rnd2_vids'] = rnd2_vids[username]
            print('video-list-round2')
            print(rnd2_vids[username])

            # test 250118 next three lines
            session['cat1_sec_fin'] = cat1_sec_fin[username]
            session['cat2_sec_fin'] = cat2_sec_fin[username]
            session['cat3_sec_fin'] = cat3_sec_fin[username]

def update(username,cur_cat, cur_id):
    global cat1_end, cat2_end, cat3_end
    # test 250110 next line
    cat1_end[username] = session.get('cat1_end', 0)
    # test 250110 next line
    cat2_end[username] = session.get('cat2_end', 0)

    if cat1_end[username] == 1 and cat2_end[username] == 1:
        return "end"
    if cur_cat == 'cat1':
        # test!!!
        cur_id = int(cur_id)
        # test 250112
        rnd1_vids[username] = session.get('rnd1_vids')

        print("pinhao_debug: update, cur_id:{}, rnd1_vids[username]:{}".format(cur_id, rnd1_vids[username]))
        try:
            cur_index = rnd1_vids[username].index(cur_id)
        except:
            print("error! update, cur_cat:{}, round:{}".format(cur_cat, session.get('rec_round')))
            rnd2_vids[username] = session.get('rnd2_vids')
            cur_index = rnd2_vids[username].index(cur_id)
            if cur_index == len(rnd2_vids[username]) - 1:
                # test 250110 next line
                session['cat2_end'] = 1
                cat2_end[username] = 1
            session['cat1_end'] = 1
            cat1_end[username] = 1
            return 'next'

        if cur_index == len(rnd1_vids[username]) - 1:
            # test 250110 next line
            session['cat1_end'] = 1
            cat1_end[username] = 1
    else:
        # test!!!
        cur_id = int(cur_id)
        # test 250112
        rnd2_vids[username] = session.get('rnd2_vids')

        print("pinhao_debug: update, cur_id:{}, rnd2_vids[username]:{}".format(cur_id, rnd2_vids[username]))
        cur_index = rnd2_vids[username].index(cur_id)
        if cur_index == len(rnd2_vids[username]) - 1:
            # test 250110 next line
            session['cat2_end'] = 1
            cat2_end[username] = 1
    return 'next'

def get_next_id(username,cur_cat,cur_vid):
    global pre_cat1, pre_cat2
    if cur_cat == 'cat1':
        # test 250112
        rnd1_vids[username] = session.get('rnd1_vids')

        print("pinhao_debug: get_next_id, cur_vid:{}, rnd1_vids[username]:{}".format(cur_vid, rnd1_vids[username]))
        try:
            cur_index = rnd1_vids[username].index(cur_vid)
        except:
            print("error! get_next_id, cur_cat:{}, round:{}".format(cur_cat, session.get('rec_round')))
            rnd2_vids[username] = session.get('rnd2_vids')
            cur_index = rnd2_vids[username].index(cur_vid)
            next_id =rnd2_vids[username][cur_index+1]
            if cur_index > 0:
                pre_cat2[username] = cur_vid
            return next_id

        next_id = rnd1_vids[username][cur_index+1]
        if cur_index > 0:
            pre_cat1[username] = cur_vid
        return next_id
    elif cur_cat == 'cat2':
        # test 250112
        rnd2_vids[username] = session.get('rnd2_vids')

        print("pinhao_debug: get_next_id, cur_vid:{}, rnd2_vids[username]:{}".format(cur_vid, rnd2_vids[username]))
        cur_index = rnd2_vids[username].index(cur_vid)
        next_id =rnd2_vids[username][cur_index+1]
        if cur_index > 0:
            pre_cat2[username] = cur_vid
        return next_id

def get_prev_id(username,cur_cat, cur_id):
    global pre_cat1, pre_cat2, pre_cat3, pre_filler
    if cur_cat == 'cat1':
        # test 250112
        rnd1_vids[username] = session.get('rnd1_vids')

        if cur_id in rnd1_vids[username]:
            cur_index = rnd1_vids[username].index(cur_id)
            if cur_index == 0:
                return 'no prev'
            else:
                prev_id = rnd1_vids[username][cur_index-1]
                return prev_id
        else:
            print("error! rnd1 cur_id: {} rnd1_vids: {}", cur_id, rnd1_vids[username])
            return 'no prev'
    elif cur_cat == 'cat2':
        # test 250112
        rnd2_vids[username] = session.get('rnd2_vids')

        if cur_id in rnd2_vids[username]:
            cur_index = rnd2_vids[username].index(cur_id)
            if cur_index == 0:
                return 'no prev'
            else:
                prev_id = rnd2_vids[username][cur_index - 1]
                return prev_id
        else:
            print("error! rnd2 cur_id: {} rnd1_vids: {}", cur_id, rnd2_vids[username])
            return 'no prev'

@auth.route('/track', methods= ['GET', 'POST'])
def track_length():
    print("track start", datetime.now())
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    info = request.get_json()
    id = current_user.id
    # keyerror bug 250108 test!!!
    #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #trans_ip = ip.replace(".", '')
    #num = user.query.filter(user.username.contains(trans_ip)).count()
    #username = trans_ip + str(num)
    username = current_user.username
    # test 250118 next line
    exp_group[username] = session.get('exp_group')

    pct_data[username] = info['pct']
    print("pinhao_debug: pct:{}".format(pct_data[username]))

    print(info['status'])
    if info['pct'] is None:
        return "Null. Do not record."
    if info['status'] == 'playing':
        # test 250111 next line
        session['last_state'] = 0
        pause[username] = session.get('pause')
        if first_playing_time[username] == 0 and info['pct'] < 0.01:
            first_playing_time[username] = datetime.now()
            print("pinhao_debug: first time playing: {}".format(first_playing_time[username]))

        if pause[username] != 0:
            print(info['time'])
            # test 250118 next two lines
            pause_duration[username] = session.get('pause_duration')
            #session['pause_duration'] = pause_duration[username] + (info['time'] - pause[username])/1000
            session['pause_duration'] = pause_duration[username] + (datetime.fromisoformat(datetime.now().isoformat()) - datetime.fromisoformat(pause[username])).total_seconds()
            #pause_duration[username] += (info['time'] - pause[username])/1000
            pause_duration[username] = session['pause_duration']
            # test 250111 next two lines
            session['pause'] = 0
            #pause[username] = session.get('pause')
            pause[username] = 0
            print(pause_duration[username])
        new_act = activity(user_id = id, username = username,ip=ip, video_id=info['id'], percent_watched=info['pct'], group = int(exp_group[username][-1]))
    elif info['status'] == 'paused':
        # test 250111 next two lines
        #session['pause'] = info['time']
        session['last_state'] = 1
        session['pause'] = datetime.now().isoformat()
        pause[username] = session['pause']
        #pause[username] = info['time']
        print(pause[username])
        new_act = activity(user_id=id, username=username, ip=ip, video_id=info['id'], percent_watched=info['pct'], paused = 1, group = int(exp_group[username][-1]))
    else:
        new_act = activity(user_id=id, username=username, ip=ip, video_id=info['id'], percent_watched=info['pct'], finished = 1, group = int(exp_group[username][-1]))

    try:
        db.session.add(new_act)
        db.session.commit()
    except:
        print("Not successful")
    print("track ends", datetime.now())
    return "success!"

@auth.route('/signup', methods= ['GET', 'POST'])

def signUp():
    # test 250118 next line
    exp_group[username] = session.get('exp_group')

    if request.method == 'POST':
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        username = request.form.get('username')
        if len(username) >= 1:
            check = user.query.filter_by(username = username).first()
            if check:
                flash("The username has already been taken! Try another.", category="error")
            else:
                new_user = user(username=username, ip = ip, group = int(exp_group[username][-1]))
                db.session.add(new_user)
                db.session.commit()
                check = user.query.filter_by(username=username).first()
                login_user(check, remember=True)
                flash("Account created!", category="success")
                return redirect(url_for('views.home'))
        else:
            flash("Please enter a valid username.", category="error")
    return render_template("signup.html", user = current_user)

@auth.route('/login', methods= ['GET', 'POST'])

def logIn():
    if request.method == 'POST':
        username = request.form.get('username')
        check = user.query.filter_by(username=username).first()
        pre_check = preference.query.filter_by(username=username).first()
        info_check = information.query.filter_by(username=username).first()
        if check:
            flash("Log in successfully!", category="success")
            login_user(check)
            if pre_check:
                if info_check:
                    return redirect(url_for('auth.show_instructions'))
                else:
                    return redirect(url_for('auth.personalInfo'))
            else:
                return redirect(url_for('views.home'))
        else:
            if len(username) >= 1:
                flash("The username does not exist.", category="error")
            else:
                flash("Please enter a username.", category="error")
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logOut():
    logout_user()
    return redirect(url_for('auth.intro'))

@auth.route('/recommend/<optionNum>', methods= ['GET', 'POST'])
@login_required
def recommend(optionNum):
    # test 250110 next line
    username = current_user.username
    # test 250110 next line
    rec_round[username] = session.get('rec_round', 0)
    # test 250110 next two lines
    #current_cat[username] = session.get('current_cat', 'cat1')
    #total_duration[username] = session.get('total_duration')

    # test 250110 next line
    #count_dic[username] = session.get('count_dic', {})
    # test 250118 next line
    exp_group[username] = session.get('exp_group')

    # test 250112 next lines
    cat1_dur[username] = session.get('cat1_dur')
    cat2_dur[username] = session.get('cat2_dur')
    cat3_dur[username] = session.get('cat3_dur')

    global rnd1_vids, rnd2_vids
    if request.method == 'POST':
        print("post start", datetime.now())
        global non_res_count1, non_res_count2, non_res_count3, current_cat, cat1_end, cat2_end, cat3_end, non_res_pai_ind, cat1_sec_fin, cat2_sec_fin, cat3_sec_fin
        # test 250110 next line
        current_cat[username] = session.get('current_cat')
        # test 250110 next line
        cat1_end[username] = session.get('cat1_end', 0)
        # test 250110 next line
        cat2_end[username] = session.get('cat2_end', 0)

        id = current_user.id
        # keyerror bug 250108 test!!!
        #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        #trans_ip = ip.replace(".", '')
        #num = user.query.filter(user.username.contains(trans_ip)).count()
        #username = trans_ip + str(num)
        username = current_user.username
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        cur_id = request.form['mysrc']
        if rec_round[username] == 1:
            cur_total = 20
        elif rec_round[username] == 2:
            cur_total = 6
        if 'next' in request.form.keys():
            print(cat1_dur[username])
            print(cat2_dur[username])
            print(cat3_dur[username])
            pct = float(request.form['next'])
            is_end = update(username, current_cat[username], cur_id)
            # test 250118 next two lines
            session['vid_count'] = session.get('vid_count') + 1
            vid_count[username] = session.get('vid_count')
            #vid_count[username] +=1
            # test 250111 next few lines
            next_time_data = session.get('next_time')
            next_time[username] = datetime.now()
            #time_str_next = next_time_data.get(username)
            print('next time:{}'.format(next_time[username]))

            # test 250118 next two lines
            pause_duration[username] = session.get('pause_duration')
            print('0214 pause_duration')
            print(pause_duration[username])
            if session.get('last_state') == 1:
                try:
                    session['pause_duration'] = pause_duration[username] + (datetime.fromisoformat(datetime.now().isoformat()) - datetime.fromisoformat(pause[username])).total_seconds()
                except:
                    print("error! pause[username]:{}".format(pause[username]))
                pause_duration[username] = session['pause_duration']
            if first_playing_time[username] == 0:
                if pct_data[username] == 0:
                    print("pinhao_debug: pct is 0, set actual_time to 0")
                    actual_time = 0
                else:
                    print("pinhao_debug: compute actual time based on ready time")
                    actual_time = (next_time[username] - ready_time[username]).total_seconds() - pause_duration[username]
            else:
                print("pinhao_debug: compute actual time based on first playing time")
                actual_time = (next_time[username] - first_playing_time[username]).total_seconds() - pause_duration[username]
            
            vedio_id = int(cur_id)
            cur_group_id = int(exp_group[username][-1])
            cur_cat_name = 'null'
            if int(session.get('rec_round')) == 1:
                if vedio_id in session.get('cat1_first'):
                    cur_cat_name = category=session.get('cat1_name')
                elif vedio_id in session.get('cat2_first'):
                    cur_cat_name = category=session.get('cat2_name')
                elif vedio_id in session.get('cat3_first'):
                    cur_cat_name = category=session.get('cat3_name')
            elif int(session.get('rec_round')) == 2:
                if vedio_id in session.get('cat1_sec_fin'):
                    cur_cat_name = category=session.get('cat1_sec_name')
                elif vedio_id in session.get('cat2_sec_fin'):
                    cur_cat_name = category=session.get('cat2_sec_name')
                elif vedio_id in session.get('cat3_sec_fin'):
                    cur_cat_name = category=session.get('cat3_sec_name')
            
            vedio_time = ytb_data[ytb_data['id'] == int(cur_id)]
            vedio_time = float(vedio_time['duration'].to_list()[0])
            watch_percent = actual_time / vedio_time
            watch_record = watch(group_id=cur_group_id, user_id=int(current_user.id), username=current_user.username, category=cur_cat_name, video_id=cur_id, watch_time=actual_time, vedio_time=vedio_time, percent=watch_percent, turn=int(session.get('rec_round')))
            try:
                db.session.add(watch_record)
                db.session.commit()
            except:
                print("error! fail to add watch record")
            print("pinhao_debug: actual_time: {} next_time: {} ready_time: {} pause_duration: {} first_playing_time: {} cur_id: {} cat1_first: {} cur_cat_name:{} turn: {} user_id:{} username:{} group_id:{} vedio_time: {} watch_percent: {}".format(actual_time, next_time[username], ready_time[username], pause_duration[username], first_playing_time[username], cur_id, session.get('cat1_first'), cur_cat_name, session.get('rec_round'), current_user.id, username, cur_group_id, vedio_time, watch_percent))
            ind_browsing_time[username] = actual_time
            # test 250118 next two lines
            actual_browsing_time[username] = session.get('actual_browsing_time')
            session['actual_browsing_time'] = session.get('actual_browsing_time') + actual_time
            actual_browsing_time[username] += actual_time
            # test 250111 next two lines
            session['pause'] = 0
            session['last_state'] = 0
            first_playing_time[username] = 0
            pct_data[username] = 0
            ready_time[username] = datetime.now()
            #pause[username] = session.get('pause')
            pause[username] = 0
            # test 250118 next two lines
            session['pause_duration'] = 0
            #pause_duration[username] = session.get('pause_duration')
            pause_duration[username] = 0
            # test!!!
            cur_id = int(cur_id)
            # test 250118 next line
            path_record[username] = session.get('path_record')

            if not pd.isnull(ytb_data[ytb_data['id'] == cur_id]['Tags'].tolist()[0]):
                tags = ytb_data[ytb_data['id'] == cur_id]['Tags'].tolist()[0].split(', ')
                for t in tags:
                    # test 250110 next few lines
                    count_dic_data = session.get('count_dic')            # 1) 取出最外层
                    user_count_data = count_dic_data.get(username, {})       # 2) 取出该用户的子字典
                    if t not in user_count_data.keys():
                    #if t not in count_dic[username].keys():
                        # test 250110 next few lines
                        #count_dic_data = session.get('count_dic')            # 1) 取出最外层
                        #user_count_data = count_dic_data.get(username)       # 2) 取出该用户的子字典
                        user_count_data[t] = actual_time                         # 3) 写入 actual_time
                        print('count_dic_test1*****572******user_count_data')
                        print(user_count_data)
                        count_dic_data[username] = user_count_data               # 4) 更新大字典
                        print('count_dic_test2*****572******count_dic_data')
                        print(count_dic_data)
                        session['count_dic'] = count_dic_data                    # 存回 session

                        #count_dic[username][t] = actual_time
                    else:
                        # test 250110 next few lines
                        #count_dic_data = session.get('count_dic')            # 1) 取出最外层
                        #user_count_data = count_dic_data.get(username)       # 2) 取出该用户的子字典
                        user_count_data[t] = user_count_data[t] + actual_time                         # 3) 写入 actual_time
                        print('count_dic_test1*****584******user_count_data')
                        print(user_count_data)
                        count_dic_data[username] = user_count_data               # 4) 更新大字典
                        print('count_dic_test2*****584******count_dic_data')
                        print(count_dic_data)
                        session['count_dic'] = count_dic_data                    # 存回 session
                        #count_dic[username][t] = user_count_data[t]

                        #count_dic[username][t] += actual_time

            # test 250118 next three lines
            cat1_first[username] = session.get('cat1_first')
            cat2_first[username] = session.get('cat2_first')
            cat3_first[username] = session.get('cat3_first')
            cat1_sec_fin[username] = session.get('cat1_sec_fin')
            cat2_sec_fin[username] = session.get('cat2_sec_fin')
            cat3_sec_fin[username] = session.get('cat3_sec_fin')

            if cur_id in cat1_first[username]:
                # test 250211 next line
                cat1_dur[username] = session.get('cat1_dur')
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat1 rnd1'+")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
                cat1_dur[username] += actual_time
                # test 250112 next lines
                session['cat1_dur'] = cat1_dur[username]

                #cur_rat.category = 'Ind set'
            elif cur_id in cat2_first[username]:
                # test 250211 next line
                cat2_dur[username] = session.get('cat2_dur')
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat2 rnd1' + ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
                cat2_dur[username] += actual_time
                # test 250112 next lines
                session['cat2_dur'] = cat2_dur[username]

                #cur_rat.category = 'L set'
            elif cur_id in cat3_first[username]:
                # test 250211 next line
                cat3_dur[username] = session.get('cat3_dur')
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat3 rnd1' + ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
                cat3_dur[username] += actual_time
                # test 250112 next lines
                session['cat3_dur'] = cat3_dur[username]

            elif cur_id in cat1_sec_fin[username]:
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat1 rnd2' +  ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
                #cur_rat.category = 'L set'
            elif cur_id in cat2_sec_fin[username]:
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat2 rnd2' +  ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
            elif cur_id in cat3_sec_fin[username]:
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat3 rnd2' +  ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
                '''try:
                    db.session.query(rating).filter(rating.username == username).filter(rating.video_id == cur_id).update({'seconds': actual_time})
                    db.session.commit()
                except:
                    print("did not update!")'''
            # check category status to avoid exhausted categories
            if cat1_end[username] == 0 and cat2_end[username] ==0 :
                pass
            elif cat1_end[username] == 1 and cat2_end[username] ==0 and rec_round[username] == 1:
                print("you should end rnd1!")
                # test 250118 next line
                actual_browsing_time[username] = session.get('actual_browsing_time')
                # test 250118 next two lines
                session['r1_bt'] = actual_browsing_time[username]
                #r1_bt[username] = session.get('r1_bt')
                r1_bt[username] = actual_browsing_time[username]
                # test 250110 next line
                session['current_cat'] = 'cat2'
                current_cat[username] = 'cat2'
                #redirect
                if exp_group[username] == 'Group1':
                    #show risk reminder
                    return redirect(url_for('auth.show_report', content = "r1"))
                elif exp_group[username] == 'Group2':
                    #show nothing
                    return redirect(url_for('auth.proceed'))
                elif exp_group[username] == 'Group3':
                    #show reminder+general report
                    return redirect(url_for('auth.show_report', content = "r3"))
                elif exp_group[username] == 'Group4':
                    #show general report
                    return redirect(url_for('auth.show_report', content = "r4"))
                elif exp_group[username] == 'Group5':
                    #show reminder+detailed report
                    return redirect(url_for('auth.show_report', content = "r5"))
                elif exp_group[username] == 'Group6':
                    #show detailed report
                    return redirect(url_for('auth.show_report', content = "r6"))
            elif cat1_end[username] == 1 and cat2_end[username] ==1:
                is_end = 'end'
            if is_end == 'next':
                # test!!!
                cur_id = int(cur_id)
                next_id = get_next_id(username, current_cat[username], cur_id)
                df_dur = ytb_data[ytb_data['id'] == next_id]
                duration = df_dur['duration'].to_list()[0]
                # test 250110 next few lines
                duration_tem = session.get("total_duration")
                total_duration[username] = timedelta(seconds=float(duration_tem)) + timedelta(seconds=float(duration))
                session['total_duration'] = float(duration_tem) + float(duration)
                #total_duration[username] += timedelta(seconds=float(duration))
                records = note.query.filter_by(video_id=next_id, username = username).all()
                users = []
                coms = []
                likes = 0
                dislikes = 0
                for r in records:
                    if r.comments is not None:
                        users.append(r.username)
                        coms.append(r.comments)
                    elif r.like is not None:
                        likes += 1
                    elif r.dislike is not None:
                        dislikes += 1
                collects = collection.query.filter_by(video_id=next_id, username = username).all()
                len_col = len(collects)
                len_com = len(users)
                print("post ends", datetime.now())
                return render_template('recommendation.html', video_id=next_id, user=current_user,
                                       zip=zip, users=users, coms=coms, len_com=len_com, len_like=likes,
                                       len_dislike=dislikes, len_saved=len_col, cur_count = vid_count[username] + 1, cur_total = cur_total)
            else:
                print("end")
                # test 250110 next two lines
                duration_tem = session.get("total_duration")
                total_duration[username] = timedelta(seconds=float(duration_tem))

                # test 250118 next line
                actual_browsing_time[username] = session.get('actual_browsing_time')
                browsing_time = actual_browsing_time[username]
                brow_tot_ratio = browsing_time/total_duration[username].total_seconds()
                group_num = exp_group[username][-1]
                num = browse.query.filter(browse.code.isnot(None), browse.code.like(group_num+'%')).count() + 1
                num_code = str(num)
                if len(num_code) == 1:
                    code = group_num + "00" + num_code
                elif len(num_code)   == 2:
                    code = group_num + "0" + num_code
                elif len(num_code)   == 3:
                    code = group_num + num_code
                else:
                    code = group_num + num_code
                # test 250118 next line
                path_record[username] = session.get('path_record')
                print(path_record[username])
                print(code)
                new_browse = browse(user_id=id, username=username, ip=ip, browsingTime=browsing_time, \
                                    browsing_to_tot_ratio=brow_tot_ratio, path=path_record[username], \
                                    code = code, group = int(exp_group[username][-1]))
                try:
                    db.session.add(new_browse)
                    db.session.commit()
                except:
                    print("Not successful")
                try:
                    db.session.query(preference).filter(preference.username == username).update({'code': code})
                    db.session.commit()
                except:
                    print("did not update!")
                #flash("The end！", category='success')
                print("post ends", datetime.now())
                return redirect(url_for('auth.end',code = code))
        elif 'prev' in request.form.keys():
            #do prev
            # test 250118 next two lines
            session['vid_count'] = session.get('vid_count') - 1
            vid_count[username] = session.get('vid_count')
            #vid_count[username] -= 1
            # test 250111 next few lines
            #next_time_data = session.get('next_time')
            #time_str_next = next_time_data.get(username)
            #next_time[username] = datetime.fromisoformat(time_str_next)
            next_time[username] = datetime.now()

            # test 250118 next two lines
            # test 250118 next line
            pause_duration[username] = session.get('pause_duration')
            print('0214 pause_duration')
            print(pause_duration[username])
            if session.get('last_state') == 1:
                try:
                    session['pause_duration'] = pause_duration[username] + (datetime.fromisoformat(datetime.now().isoformat()) - datetime.fromisoformat(pause[username])).total_seconds()
                except:
                    print("error! pause[username]:{}".format(pause[username]))
                pause_duration[username] = session['pause_duration']
            
            actual_time = (next_time[username] - ready_time[username]).total_seconds() - pause_duration[username]
            print("pinhao_debug 2: actual_time: {} next_time: {} ready_time: {} pause_duration: {} first_playing_time: {} cur_id: {} cat1_first: {}".format(actual_time, next_time[username], session.get('ready_time'), pause_duration[username], first_playing_time[username], cur_id, session.get('cat1_first')))
            ind_browsing_time[username] = actual_time
            # test 250118 next two lines
            actual_browsing_time[username] = session.get('actual_browsing_time')
            session['actual_browsing_time'] = session.get('actual_browsing_time') + actual_time
            actual_browsing_time[username] += actual_time
            # test 250111 next two lines
            session['pause'] = 0
            #pause[username] = session.get('pause')
            pause[username] = 0
            session['last_state'] = 0
            first_playing_time[username] = 0
            # test 250118 next two lines
            session['pause_duration'] = 0
            #pause_duration[username] = session.get('pause_duration')
            pause_duration[username] = 0
            # test!!!
            cur_id = int(cur_id)
            if not pd.isnull(ytb_data[ytb_data['id'] == cur_id]['Tags'].tolist()[0]):
                tags = ytb_data[ytb_data['id'] == cur_id]['Tags'].tolist()[0].split(', ')
                for t in tags:
                    # test 250110 next few lines
                    count_dic_data = session.get('count_dic')            # 1) 取出最外层
                    user_count_data = count_dic_data.get(username, {})       # 2) 取出该用户的子字典
                    if t not in user_count_data.keys():
                    #if t not in count_dic[username].keys():
                        # test 250110 next few lines
                        #count_dic_data = session.get('count_dic')            # 1) 取出最外层
                        #user_count_data = count_dic_data.get(username)       # 2) 取出该用户的子字典
                        user_count_data[t] = actual_time                         # 3) 写入 actual_time
                        print('count_dic_test1*****822******user_count_data')
                        print(user_count_data)
                        count_dic_data[username] = user_count_data               # 4) 更新大字典
                        print('count_dic_test2*****822******count_dic_data')
                        print(count_dic_data)
                        session['count_dic'] = count_dic_data                    # 存回 session

                        #count_dic[username][t] = actual_time
                    else:
                        # test 250110 next few lines
                        #count_dic_data = session.get('count_dic')            # 1) 取出最外层
                        #user_count_data = count_dic_data.get(username)       # 2) 取出该用户的子字典
                        user_count_data[t] = user_count_data[t] + actual_time                         # 3) 写入 actual_time
                        print('count_dic_test1*****835******user_count_data')
                        print(user_count_data)
                        count_dic_data[username] = user_count_data               # 4) 更新大字典
                        print('count_dic_test2*****835******count_dic_data')
                        print(count_dic_data)
                        session['count_dic'] = count_dic_data                    # 存回 session
                        #count_dic[username][t] = user_count_data[t]

                        #count_dic[username][t] += actual_time

            # test 250118 next three lines
            cat1_first[username] = session.get('cat1_first')
            cat2_first[username] = session.get('cat2_first')
            cat3_first[username] = session.get('cat3_first')
            cat1_sec_fin[username] = session.get('cat1_sec_fin')
            cat2_sec_fin[username] = session.get('cat2_sec_fin')
            cat3_sec_fin[username] = session.get('cat3_sec_fin')

            if cur_id in cat1_first[username]:
                # test 250211 next line
                cat1_dur[username] = session.get('cat1_dur')
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat1 rnd1' + ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
                cat1_dur[username] += actual_time
                # test 250112 next lines
                session['cat1_dur'] = cat1_dur[username]

                # cur_rat.category = 'Ind set'
            elif cur_id in cat2_first[username]:
                # test 250211 next line
                cat2_dur[username] = session.get('cat2_dur')
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat2 rnd1' + ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
                cat2_dur[username] += actual_time
                # test 250112 next lines
                session['cat2_dur'] = cat2_dur[username]

                # cur_rat.category = 'L set'
            elif cur_id in cat3_first[username]:
                # test 250211 next line
                cat3_dur[username] = session.get('cat3_dur')
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat3 rnd1' + ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
                cat3_dur[username] += actual_time
                # test 250112 next lines
                session['cat3_dur'] = cat3_dur[username]

            elif cur_id in cat1_sec_fin[username]:
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat1 rnd2' + ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
                # cur_rat.category = 'L set'
            elif cur_id in cat2_sec_fin[username]:
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat2 rnd2' + ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
            elif cur_id in cat3_sec_fin[username]:
                # test!!!
                cur_id = str(cur_id)
                v_str = '(' + cur_id + "," + 'cat3 rnd2' + ")"
                # test 250118 next two lines
                session['path_record'] = session.get('path_record') + v_str
                #path_record[username] = session.get('path_record')
                path_record[username] += v_str
            # test!!!
            cur_id = int(cur_id)
            prev_id = get_prev_id(username, current_cat[username], cur_id)
            if prev_id != "no prev":
                df_dur = ytb_data[ytb_data['id'] == prev_id]
                duration = df_dur['duration'].to_list()[0]
                # test 250110 next few lines
                duration_tem = session.get("total_duration")
                total_duration[username] = timedelta(seconds=float(duration_tem)) + timedelta(seconds=float(duration))
                session['total_duration'] = float(duration_tem) + float(duration)
                #total_duration[username] += timedelta(seconds=float(duration))
                records = note.query.filter_by(video_id=prev_id, username=username).all()
                users = []
                coms = []
                likes = 0
                dislikes = 0
                for r in records:
                    if r.comments is not None:
                        users.append(r.username)
                        coms.append(r.comments)
                    elif r.like is not None:
                        likes += 1
                    elif r.dislike is not None:
                        dislikes += 1
                collects = collection.query.filter_by(video_id=prev_id, username = username).all()
                len_col = len(collects)
                len_com = len(users)
                print("post ends", datetime.now())
                return render_template('recommendation.html', video_id=prev_id, user=current_user,
                                       zip=zip, users=users, coms=coms, len_com=len_com, len_like=likes,
                                       len_dislike=dislikes, len_saved=len_col, cur_count = vid_count[username] + 1, cur_total = cur_total)
            else:
                records = note.query.filter_by(video_id=cur_id).all()
                collects = collection.query.filter_by(video_id=cur_id, username=username).all()
                users = []
                coms = []
                likes = 0
                dislikes = 0
                for r in records:
                    if r.comments is not None:
                        users.append(r.username)
                        coms.append(r.comments)
                    elif r.like is not None:
                        likes += 1
                    elif r.dislike is not None:
                        dislikes += 1
                len_col = len(collects)
                len_com = len(users)
                print("post ends", datetime.now())
                return render_template('recommendation.html', video_id=cur_id, user=current_user,
                                       zip=zip, users=users, coms=coms, len_com=len_com, len_like=likes,
                                       len_dislike=dislikes, len_saved=len_col, cur_count = 1)
        # test!!!
        cur_id = int(cur_id)
        records = note.query.filter_by(video_id=cur_id).all()
        collects = collection.query.filter_by(video_id=cur_id, username = username).all()
        users = []
        coms = []
        likes = 0
        dislikes = 0
        for r in records:
            if r.comments is not None:
                users.append(r.username)
                coms.append(r.comments)
            elif r.like is not None:
                likes += 1
            elif r.dislike is not None:
                dislikes += 1
        len_col = len(collects)
        len_com = len(users)
        print("post ends", datetime.now())
        return render_template('recommendation.html', video_id=cur_id, user=current_user,
                               zip=zip, users=users,coms=coms, len_com = len_com, len_like = likes,
                               len_dislike = dislikes, len_saved=len_col, cur_count = vid_count[username] + 1, cur_total = cur_total)

    else:
        print("get start", datetime.now())
        global pre_cat1, pre_filler
        # keyerror bug 250108 test!!!
        #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        #trans_ip = ip.replace(".", '')
        #num = user.query.filter(user.username.contains(trans_ip)).count()
        #username = trans_ip + str(num)
        username = current_user.username
        pre_check = preference.query.filter_by(username=username).first()
        # test 250110 next line
        current_cat[username] = session.get('current_cat')
        # test 250110 next line
        session['rec_round'] = session.get('rec_round') + 1
        rec_round[username] += 1
        if rec_round[username] == 1:
            cur_total = 20

        elif rec_round[username] == 2:
            cur_total = 6
        # test 250118 next two lines
        if session.get('r1_bt') != None:
            r1_bt[username] = session.get('r1_bt')
        if username in r1_bt.keys():
            # test 250118 next two lines
            session['actual_browsing_time'] = r1_bt[username]
            #actual_browsing_time[username] = session.get('actual_browsing_time')
            actual_browsing_time[username] = r1_bt[username]
        else:
            # test 250118 next two lines
            session['actual_browsing_time'] = 0
            #actual_browsing_time[username] = session.get('actual_browsing_time')
            actual_browsing_time[username] = 0
        if int(optionNum) == 0:
            non_res_count1[username] = 0
            non_res_count2[username] = 0
            prev_browsing_time[username] = 0
            prev_duration[username] = 0
            # test 250118 next two lines
            session['path_record'] = ''
            #path_record[username] = session.get('path_record')
            path_record[username] = ''
            pre_cat1[username] = ''
            pre_cat2[username] = ''
            # test 250118 next two lines
            session['vid_count'] = 0
            vid_count[username] = session.get('vid_count')
            #vid_count[username] = 0
            # test 250111 next two lines
            session['pause'] = 0
            #pause[username] = session.get('pause')
            pause[username] = 0
            # test 250118 next two lines
            session['pause_duration'] = 0
            #pause_duration[username] = session.get('pause_duration')
            pause_duration[username] = 0
            #newly added
            cat1_dur[username] = 0
            cat2_dur[username] = 0
            cat3_dur[username] = 0
            # test 250112
            session['cat1_dur'] = 0
            session['cat2_dur'] = 0
            session['cat3_dur'] = 0

            if pre_check:
                # test 250112
                rnd1_vids[username] = session.get('rnd1_vids')

                if rnd1_vids[username]:
                    if current_cat[username] == 'cat1':
                        rec = rnd1_vids[username][0]
                    else:
                        rec = filler[username][0]
                        pre_filler[username] = rec
                    df_dur = ytb_data[ytb_data['id'] == rec]
                    duration = df_dur['duration'].to_list()[0]
                    # test 250110 next few lines
                    duration_tem = session.get("total_duration")
                    total_duration[username] = timedelta(seconds=float(duration_tem)) + timedelta(seconds=float(duration))
                    session['total_duration'] = float(duration_tem) + float(duration)
                    #total_duration[username] += timedelta(seconds= float(duration))
                    records = note.query.filter_by(video_id=rec, username = username).all()
                    users = []
                    coms = []
                    likes = 0
                    dislikes = 0
                    for r in records:
                        if r.comments is not None:
                            users.append(r.username)
                            coms.append(r.comments)
                        elif r.like is not None:
                            likes += 1
                        elif r.dislike is not None:
                            dislikes += 1
                    len_com = len(users)
                    collects = collection.query.filter_by(video_id=rec, username = username).all()
                    len_col = len(collects)
                    print("get ends", datetime.now())
                    return render_template('recommendation.html', video_id = rec, user = current_user, zip = zip,
                                           users = users, coms=coms, len_com = len_com, len_like = likes, len_dislike = dislikes, len_saved = len_col, cur_count = 1, cur_total = cur_total)
                else:
                    return "error"
            else:
                flash("No record of preference", category="error")
                return render_template('home.html')
        else:
            # test 250118 next two lines
            session['vid_count'] = 0
            vid_count[username] = session.get('vid_count')
            #vid_count[username] = 0
            # test 250111 next two lines
            session['pause'] = 0
            #pause[username] = session.get('pause')
            pause[username] = 0
            # test 250118 next two lines
            session['pause_duration'] = 0
            #pause_duration[username] = session.get('pause_duration')
            pause_duration[username] = 0
            # newly added
            cat1_dur[username] = 0
            cat2_dur[username] = 0
            cat3_dur[username] = 0
            # test 250112
            session['cat1_dur'] = 0
            session['cat2_dur'] = 0
            session['cat3_dur'] = 0

            # test 250112
            rnd2_vids[username] = session.get('rnd2_vids')

            if rnd2_vids[username]:
                rec = rnd2_vids[username][0]
                df_dur = ytb_data[ytb_data['id'] == rec]
                duration = df_dur['duration'].to_list()[0]
                # test 250110 next few lines
                duration_tem = session.get("total_duration")
                total_duration[username] = timedelta(seconds=float(duration_tem)) + timedelta(seconds=float(duration))
                session['total_duration'] = float(duration_tem) + float(duration)
                #total_duration[username] += timedelta(seconds= float(duration))
                records = note.query.filter_by(video_id=rec, username = username).all()
                users = []
                coms = []
                likes = 0
                dislikes = 0
                for r in records:
                    if r.comments is not None:
                        users.append(r.username)
                        coms.append(r.comments)
                    elif r.like is not None:
                        likes += 1
                    elif r.dislike is not None:
                        dislikes += 1
                len_com = len(users)
                collects = collection.query.filter_by(video_id=rec, username = username).all()
                len_col = len(collects)
                print("get ends", datetime.now())
                return render_template('recommendation.html', video_id = rec, user = current_user, zip = zip,
                                       users = users, coms=coms, len_com = len_com, len_like = likes, len_dislike = dislikes, len_saved = len_col, cur_count = 1, cur_total = cur_total)
            else:
                return "error"
@auth.route('/options', methods= ['GET', 'POST'])
@login_required
def options():
    # test!!!
    # keyerror bug 250108 test!!!
    #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #trans_ip = ip.replace(".", '')
    #num = user.query.filter(user.username.contains(trans_ip)).count()
    #username = trans_ip + str(num)
    username = current_user.username
    #username = str(current_user.username)
    # test 250110 next line
    rec_round[username] = session.get('rec_round', 0)
    # test 250110 next line
    option[username] = session.get('option', 'option1')
    # test 250110 next line
    current_cat[username] = session.get('current_cat', 'cat1')

    if username in option.keys():
        get_pref(username, rec_round[username])
    if request.method == 'POST':
        id = current_user.id
        # keyerror bug 250108 test!!!
        #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        #trans_ip = ip.replace(".", '')
        #num = user.query.filter(user.username.contains(trans_ip)).count()
        #username = trans_ip + str(num)
        username = current_user.username
        opt = request.form['opt']
        print(opt)
        # test 250110 next line
        session['option'] = ''
        option[username] = ''
        # test 240110 next line
        session['current_cat'] = 'cat1'
        current_cat[username] = 'cat1'
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        get_pref(username, opt, 1)
        return redirect(url_for('auth.recommend', optionNum=option[username][-1]))
    #return render_template("options.html", user = current_user)
    #if is_first_time == 1:
    #    rec_round[username] = 0
    #    return redirect(url_for('auth.recommend', optionNum=0))
    #else:
    return redirect(url_for('auth.recommend', optionNum=rec_round[username]))

@auth.route('/personalInfo', methods= ['GET', 'POST'])
@login_required
def personalInfo():
    if request.method == 'POST':
        # check for past personal information record
        # keyerror bug 250108 test!!!
        #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        #trans_ip = ip.replace(".", '')
        #num = user.query.filter(user.username.contains(trans_ip)).count()
        #username = trans_ip + str(num)
        username = current_user.username
        # test 250118 next line
        exp_group[username] = session.get('exp_group')

        pre_check = information.query.filter_by(username=username).first()
        if pre_check:
            flash("You have entered your information before!", category="error")
            return redirect(url_for('auth.options'))
        else:
            # if no record found
            id = current_user.id
            age = request.form['age']
            if 'gender' in request.form.keys():
                gender = request.form['gender']
            else:
                gender = ''
            if 'duration' in request.form.keys():
                duration = request.form['duration']
            else:
                duration = ''
            if age != '' and gender!= '' and duration != '':
                ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                new_info = information(user_id = id, username = username,ip=ip, age=age, gender=gender, duration=duration, group = int(exp_group[username][-1]))
                try:
                    db.session.add(new_info)
                    db.session.commit()
                    flash("Personal information submitted!", category="success")
                    return redirect(url_for('auth.show_instructions'))
                except:
                    print("Not successful")
            else:
                if age == '':
                    flash("Please enter your age!", category="error")
                if gender == '':
                    flash("Please choose your gender!", category="error")
                if duration == '':
                    flash("Please choose how long you spend on Douyin every day!", category="error")
                return render_template("personalInfo.html", user=current_user)

    #return render_template("personalInfo.html", user = current_user)
    return redirect(url_for('auth.options'))

@auth.route('/instructions', methods= ['GET', 'POST'])
@login_required
def show_instructions():
    '''if (rec_round > 0) or (request.method == "POST"):
        return redirect(url_for('auth.options'))
    else:
        return render_template("instructions.html", user = current_user)'''
    return redirect(url_for('auth.options'))

@auth.route('/end/<code>', methods= ['GET', 'POST'])
@login_required
def end(code):
    logout_user()
    return render_template("end.html", user = current_user, code=code)

@auth.route('/feedback', methods= ['GET', 'POST'])
def feedback():
    id = current_user.id
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    info = request.get_json()
    # keyerror bug 250108 test!!!
    #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #trans_ip = ip.replace(".", '')
    #num = user.query.filter(user.username.contains(trans_ip)).count()
    #username = trans_ip + str(num)
    username = current_user.username
    # test 250118 next line
    exp_group[username] = session.get('exp_group')

    v_id = info['id']
    print(v_id)
    print(username)
    if info['type'] == 'like':
        print("i am here")
        if info['status'] == "rgb(0, 0, 0)":
            records = note.query.filter_by(video_id=v_id, username=username).all()
            print("filtered!")
            duplicate = 0
            code = "rgb(37, 110, 229)"
            for r in records:
                if r.like is not None:
                    duplicate = 1
                    break
            if duplicate == 0:
                like = 1
                new_like = note(user_id=id, username=username, ip=ip, video_id=v_id, like=like, group = int(exp_group[username][-1]))
                try:
                    db.session.add(new_like)
                    db.session.commit()
                    print("committed!")
                except:
                    print("Not successful")
        else:
            note.query.filter_by(video_id=v_id, username=username, like=1).delete()
            print("cancel")
            code = "rgb(0, 0, 0)"
        all_rec = note.query.filter_by(video_id=v_id).all()
        likes = 0
        for r in all_rec:
            if r.like is not None:
                likes += 1
        print("likes", likes)
        return jsonify({"code": code, "num_code" :str(likes)})
    elif info['type'] == 'dislike':
        if info['status'] == "rgb(0, 0, 0)":
            records = note.query.filter_by(video_id=v_id, username=username).all()
            duplicate = 0
            code = "rgb(37, 110, 229)"
            for r in records:
                if r.dislike is not None:
                    duplicate = 1
                    break
            if duplicate == 0:
                dislike = 1
                new_dislike = note(user_id=id, username=username, ip=ip, video_id=v_id, dislike=dislike, group = int(exp_group[username][-1]))
                try:
                    db.session.add(new_dislike)
                    db.session.commit()
                except:
                    print("Not successful")
        else:
            note.query.filter_by(video_id=v_id, username=username, dislike=1).delete()
            print("cancel")
            code = "rgb(0, 0, 0)"
        all_rec = note.query.filter_by(video_id=v_id).all()
        dislikes = 0
        for r in all_rec:
            if r.dislike is not None:
                dislikes += 1
        return jsonify({"code": code, "num_code" :str(dislikes)})
    elif info['type'] == 'save':
        if info['status'] == "rgb(0, 0, 0)":
            duplicate = collection.query.filter_by(video_id=v_id, username=username).first()
            code = "rgb(37, 110, 229)"
            if duplicate:
                pass
            else:
                new_col = collection(user_id=id, username=username, ip=ip, video_id=v_id, group = int(exp_group[username][-1]))
                try:
                    db.session.add(new_col)
                    db.session.commit()
                except:
                    print("Not successful")
        else:
            collection.query.filter_by(video_id=v_id, username=username).delete()
            print("cancel")
            code = "rgb(0, 0, 0)"
        all_rec = collection.query.filter_by(video_id=v_id).all()
        return jsonify({"code": code, "num_code" :str(len(all_rec))})
    else:
        comments = info['comment']
        new_comments = note(user_id=id, username=username, ip=ip, video_id=v_id, comments=comments, group = int(exp_group[username][-1]))
        try:
            db.session.add(new_comments)
            db.session.commit()
        except:
            print("Not successful")
        all_rec = note.query.filter_by(video_id=v_id).all()
        num_com = 0
        for r in all_rec:
            if r.comments is not None:
                num_com += 1
        return flask.jsonify(username=username, comment = comments, len_com = str(num_com))

@auth.route('/rating', methods= ['GET', 'POST'])
def rate():
    # test 250110 next line
    rec_round[username] = session.get('rec_round', 0)
    # test 250118 next line
    exp_group[username] = session.get('exp_group')

    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    info = request.get_json()
    id = current_user.id
    # keyerror bug 250108 test!!!
    #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #trans_ip = ip.replace(".", '')
    #num = user.query.filter(user.username.contains(trans_ip)).count()
    #username = trans_ip + str(num)
    username = current_user.username
    v_id = info['id']
    rel = info['rating']
    if rel is None:
        return "No rating"
    duplicate = rating.query.filter_by(username=username, video_id=v_id).first()
    if duplicate:
        pass
    else:
        new_rat = rating(user_id=id, username=username, ip=ip, video_id=v_id, relevance = rel, round_num = rec_round[username], group = int(exp_group[username][-1]))
        try:
            db.session.add(new_rat)
            db.session.commit()
        except:
            print("Not successful")
    print(info)
    return "success!"

@auth.route('/intro', methods= ['GET', 'POST'])

def intro():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    trans_ip = ip.replace(".", '')
    num = user.query.filter(user.username.contains(trans_ip)).count()
    username = trans_ip + str(num)
    new_user = user(username=username, ip=ip)
    db.session.add(new_user)
    db.session.commit()
    check = user.query.filter_by(username=username).first()
    login_user(check, remember=True)
    if request.method == 'POST':
        pre_check = preference.query.filter_by(username=username).first()
        info_check = information.query.filter_by(username=username).first()
        if pre_check:
            if info_check:
                return redirect(url_for('auth.show_instructions'))
            else:
                return redirect(url_for('auth.personalInfo'))
        else:
            return redirect(url_for('views.home'))
        return redirect(url_for('views.home'))
    return render_template("intro.html", user = current_user)

@auth.route('/ready', methods= ['GET', 'POST'])
def record_ready():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    info = request.get_json()
    id = current_user.id
    # keyerror bug 250108 test!!!
    #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #trans_ip = ip.replace(".", '')
    #num = user.query.filter(user.username.contains(trans_ip)).count()
    #username = trans_ip + str(num)
    username = current_user.username
    # test 250110 next line
    current_cat[username] = session.get('current_cat', 'cat1')
    # test 250118 next line
    exp_group[username] = session.get('exp_group')

    print('*****************ready*************')
    print(info['status'])
    if info['status'] == 'ready':
        # test 250118 next three lines
        session['ready_time'] = datetime.now()

        ready_time[username] = datetime.now()
        print("record ready", ready_time[username])
    elif info['status'] == 'pageReady':
        if info['page'] == 'intro':
            trans_ip = ip.replace(".", '')
            num = user.query.filter(user.username.contains(trans_ip)).count()
            username = trans_ip + str(num)
            print('1st username', username)
            #intro_time[username] = datetime.now()
            # test 250111 next few lines
            intro_time_data = session.get('intro_time', {})
            intro_time_data[username] = datetime.now().isoformat()
            session['intro_time'] = intro_time_data
        # keyerror bug 250108 test!!!
        #elif info['page'] == 'pre1':
        #    preference_time[username] = datetime.now()
        elif info['page'] == 'pre' and current_cat[username] == 'cat1':
            #preference_time[username] = datetime.now()
            # test 250111 next few lines
            preference_time_data = session.get('preference_time', {})
            preference_time_data[username] = datetime.now().isoformat()
            session['preference_time'] = preference_time_data

        elif info['page'] == 'report':
            #report_time[username] = datetime.now()
            # test 250111 next few lines
            report_time_data = session.get('report_time', {})
            report_time_data[username] = datetime.now().isoformat()
            session['report_time'] = report_time_data

        else:
            #preference_time2[username] = datetime.now()
            # test 250111 next few lines
            preference_time_data2 = session.get('preference_time2', {})
            preference_time_data2[username] = datetime.now().isoformat()
            session['preference_time2'] = preference_time_data2
    elif info['status'] == 'end':
        add_on = ''
        if info['page'] == 'intro':
            id+=1
            trans_ip = ip.replace(".", '')
            num = user.query.filter(user.username.contains(trans_ip)).count()
            username = trans_ip + str(num)
            print('2nd username', username)
            # test 250111 next few lines
            intro_time_data = session.get('intro_time')
            time_str_intro = intro_time_data.get(username)
            if time_str_intro:
                dt_intro = datetime.fromisoformat(time_str_intro)
                sec_diff = (datetime.now() - dt_intro).total_seconds()
            #if username in intro_time.keys():
            #    sec_diff = (datetime.now() - intro_time[username]).total_seconds()
            else:
                sec_diff = -1
        # keyerror bug 250108 test!!!
        #elif info['page'] == 'pre1':
        #    sec_diff = (datetime.now() - preference_time[username]).total_seconds()
        #elif info['page'] == 'pre' and current_cat[username] == 'cat1':
        #    if username not in current_cat:
        #        sec_diff = (datetime.now() - preference_time[username]).total_seconds()
        #    elif current_cat[username] == 'cat1':
        #        sec_diff = (datetime.now() - preference_time[username]).total_seconds()
        elif info['page'] == 'pre' and current_cat[username] == 'cat1':
            #sec_diff = (datetime.now() - preference_time[username]).total_seconds()
            # test 250111
            preference_time_data = session.get('preference_time')
            time_str = preference_time_data.get(username)
            dt = datetime.fromisoformat(time_str)
            sec_diff = (datetime.now() - dt).total_seconds()
        elif info['page'] == 'report':
            #sec_diff = (datetime.now() - report_time[username]).total_seconds()
            # test 250111 next few lines
            report_time_data = session.get('report_time')
            time_str_report = report_time_data.get(username)
            try:
                dt_report = datetime.fromisoformat(time_str_report)
                sec_diff = (datetime.now() - dt_report).total_seconds()
            except:
                print("error! time_str_report:{}".format(time_str_report))
                sec_diff = 0

        else:
            #sec_diff = (datetime.now() - preference_time2[username]).total_seconds()
            add_on = '2'
            # test 250111 next few lines
            preference_time_data2 = session.get('preference_time2')
            time_str2 = preference_time_data2.get(username)
            dt2 = datetime.fromisoformat(time_str2)
            sec_diff = (datetime.now() - dt2).total_seconds()
        if sec_diff > 0 and 'page' in info.keys() and username in exp_group.keys():
            print('can write')
            new_btime = btime(user_id=id, username=username, ip=ip, page = info['page']+add_on, seconds = sec_diff, group = int(exp_group[username][-1]))
            try:
                db.session.add(new_btime)
                db.session.commit()
            except:
                print("Not successful")
    # test 250214 pause_duration的跳过的那一段会被计时。
    else:
        next_time[username] = datetime.now()
        # test 250111 next few lines
        next_time_data = {}
        next_time_data[username] = datetime.now().isoformat()
        session['next_time'] = next_time_data


        click_time = datetime.fromtimestamp(info['time']/1000)
        print('click time', click_time)
        print('next time', next_time[username])
        # # test 250111 next line
        # pause[username] = session.get('pause')
        # print('0214')
        # print(pause[username])

        # if pause[username] != 0:
        #     print(info['time'])
        #     # test 250118 next two lines
        #     pause_duration[username] = session.get('pause_duration')
        #     session['pause_duration'] = pause_duration[username] + (info['time'] - pause[username]) / 1000
        #     pause_duration[username] += (info['time'] - pause[username]) / 1000
        #     # test 250111 next two lines
        #     session['pause'] = 0
        #     #pause[username] = session.get('pause')
        #     pause[username] = 0
        #     print(pause_duration[username])
        print("record next", next_time[username])
        if info['status'] == 'prev' and (get_prev_id(username, current_cat[username], info['id']) == 'no prev'):
            print("no prev!")
            return "none"
    return "success!"

@auth.route('/welcome/<group>', methods= ['GET', 'POST'])

def welcome(group):
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    trans_ip = ip.replace(".", '')
    num = user.query.filter(user.username.contains(trans_ip)).count()
    username = trans_ip + str(num)
    exp_group[username] = group
    print('***********welcome**********' + username)
    new_user = user(username=username, ip=ip, group = int(exp_group[username][-1]))
    db.session.add(new_user)
    db.session.commit()
    check = user.query.filter_by(username=username).first()
    login_user(check, remember=True)

    # test 250110
    session['username'] = username
    session['exp_group'] = group      # 原先 exp_group[username] = group
    session['option'] = 'option1'     # 原先 option[username] = 'option1'
    session['rec_round'] = 0         # 原先 rec_round[username] = 0
    session['current_cat'] = 'cat1'   # 原先 current_cat[username] = 'cat1'
    session['total_duration'] = 0     # 或者存成 int 秒数，而不是 timedelta
    session['cat1_end'] = 0
    session['cat2_end'] = 0
    session['count_dic'] = {}
    session['last_state'] = 0
    #rec_round[username] = session.get('rec_round', 0)

    option[username] = 'option1'
    rec_round[username] = 0
    current_cat[username] = 'cat1'
    total_duration[username] = timedelta(seconds=0)
    cat1_end[username] = 0
    cat2_end[username] = 0
    pct_data[username] = 0
    first_playing_time[username] = 0
    #count_dic[username] = {}
    if request.method == 'POST':
        pre_check = preference.query.filter_by(username=username).first()
        info_check = information.query.filter_by(username=username).first()
        if pre_check:
            return redirect(url_for('auth.show_instructions'))
        else:
            return redirect(url_for('views.home', rnd = rec_round[username], grp = exp_group[username][-1]))
        return redirect(url_for('views.home', rnd = rec_round[username], grp = exp_group[username][-1]))
    return render_template("intro.html", user = current_user)


@auth.route('/report/<content>', methods= ['GET', 'POST'])

def show_report(content):
    is_first_time = 0
    # keyerror bug 250108 test!!!
    #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #trans_ip = ip.replace(".", '')
    #num = user.query.filter(user.username.contains(trans_ip)).count()
    #username = trans_ip + str(num)

    username = current_user.username

    # test 250110 next line
    rec_round[username] = session.get('rec_round', 0)
    # test 250110 next line
    count_dic = session.get('count_dic')
    print('count_dic 250119')
    print(count_dic)
    # test 250112 next lines
    cat1_dur[username] = session.get('cat1_dur')
    cat2_dur[username] = session.get('cat2_dur')
    cat3_dur[username] = session.get('cat3_dur')
    # test 250118 next line
    exp_group[username] = session.get('exp_group')

    if request.method == 'POST':
        return redirect(url_for('views.home', rnd = rec_round[username], grp = exp_group[username][-1]))
    report_type = content
    tot_time = cat1_dur[username] + cat2_dur[username] + cat3_dur[username]
    sorted_count_dic = dict(sorted(count_dic[username].items(), key=lambda kv: kv[1], reverse=True))
    sorted_words = list(sorted_count_dic.keys())
    print('sorted words')
    print(sorted_words)

    category_mapping = {
        "daily_vlog": "日常生活记录（vlog）",
        "dressing": "服装穿搭",
        "fitness": "健身锻炼",
        "gourmet": "美食烹饪",
        "hair_braided": "发型",
        "homemade_drinks": "自制饮料",
        "kids": "孩童",
        "livehouse": "音乐现场",
        "makeup": "化妆",
        "painting": "绘画",
        "pets": "宠物",
        "photography": "摄影摄像",
        "popular_science": "科学知识",
        "scenery": "自然风光",
        "street_snap": "街拍"
    }

    # test 250118 next three lines
    cat1_name[username] = session.get('cat1_name')
    cat2_name[username] = session.get('cat2_name')
    cat3_name[username] = session.get('cat3_name')

    # 替换 cat1, cat2, cat3 为中文类别名称
    cat1_encoded = category_mapping.get(cat1_name[username])  # 如果没有找到对应映射，则保留原名
    cat2_encoded = category_mapping.get(cat2_name[username])
    cat3_encoded = category_mapping.get(cat3_name[username])

    # test
    tot_min, spe_seconds = divmod(int(tot_time), 60)
    return render_template("report_new.html", user = current_user, cat1 = cat1_encoded, cat1_time = "{:.2f}".format(cat1_dur[username]), \
                           cat2 = cat2_encoded, cat2_time = "{:.2f}".format(cat2_dur[username]), cat3 = cat3_encoded, cat3_time = "{:.2f}".format(cat3_dur[username]), \
                           cat1_per = "{:.2f}".format(cat1_dur[username]/tot_time*100), \
                           cat2_per = "{:.2f}".format(cat2_dur[username]/tot_time*100), \
                           cat3_per = "{:.2f}".format(cat3_dur[username]/tot_time*100), tot_min = tot_min, spe_seconds = spe_seconds, report_type = report_type, \
                           w1 = sorted_words[0], w2 = sorted_words[1],w3 = sorted_words[2], w4 = sorted_words[3],w5 = sorted_words[4])

@auth.route('/proceed', methods= ['GET', 'POST'])
@login_required
def proceed():
    # keyerror bug 250108 test!!!
    #ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #trans_ip = ip.replace(".", '')
    #num = user.query.filter(user.username.contains(trans_ip)).count()
    #username = trans_ip + str(num)

    username = current_user.username

    # test 250110 next line
    rec_round[username] = session.get('rec_round', 0)
    # test 250118 next line
    exp_group[username] = session.get('exp_group')

    if request.method == "POST":
        return redirect(url_for('views.home', rnd = rec_round[username], grp = exp_group[username][-1]))
    else:
        return render_template("proceed.html", user = current_user)


@auth.route('/test/<videoid>', methods= ['GET', 'POST'])
def recommend_test(videoid):
    return render_template('recommendation_test.html', video_id=videoid, user=current_user, zip=zip,
                           users=[], coms=[], len_com=1, len_like=1, len_dislike=1,
                           len_saved=1)

@auth.route('/rtest', methods= ['GET', 'POST'])
def test_rep():
    return render_template('report_new.html', cat1 = 'v1', cat1_time = "{:.2f}".format(17.997), \
                           cat2 = 'v2', cat2_time = "{:.2f}".format(30.66), cat3 = 'v3', cat3_time = "{:.2f}".format(40.67), \
                           tot_min = "{:.2f}".format(800/60), report_type = 'r5', \
                           w1 = 'w1', w2 = 'w2',w3 = 'w3', w4 =' sorted_words[3]',w5 = 'sorted_words[4]')

@auth.route('/instructions_refer', methods= ['GET', 'POST'])
@login_required
def show_instructions2():
    '''if (rec_round > 0) or (request.method == "POST"):
        return redirect(url_for('auth.options'))
    else:
        return render_template("instructions.html", user = current_user)'''
    return render_template("instructions.html", user = current_user)