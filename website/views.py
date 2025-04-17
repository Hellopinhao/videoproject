from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import preference, user
from . import db
views = Blueprint('views', __name__)

@views.route('/pref/<grp>/<rnd>', methods= ['GET', 'POST'])
@login_required
def home(rnd, grp):
    username = current_user.username
    user_grp = user.query.filter_by(username=username).first().group

    #info_check = information.query.filter_by(username=username).first()
    print(request.url_rule)
    print(rnd)
    print(grp)
    print(request.form)
    if request.method == 'POST':
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        id = current_user.id
        new_pref = preference(
            user_id=id,
            username=username,
            ip=ip,
            daily_vlog=request.form['range1'],
            dressing=request.form['range2'],
            fitness=request.form['range3'],
            gourmet=request.form['range4'],
            hair_braided=request.form['range5'],
            homemade_drinks=request.form['range6'],
            kids=request.form['range7'],
            livehouse=request.form['range8'],
            makeup=request.form['range9'],
            painting=request.form['range10'],
            pet=request.form['range11'],
            photography=request.form['range12'],
            popular_science=request.form['range13'],
            scenery=request.form['range14'],
            street_snap=request.form['range15'],
            group = user_grp
            )
        try:
            db.session.add(new_pref)
            db.session.commit()
            flash("您的选择已成功提交!", category="success")
            # flash("Preferences submitted！", category="success")
            print('submitted')
            return redirect(url_for('auth.show_instructions'))
        except:
            print("Not successful")
    else:
        if rnd == '0':
            return render_template("home.html", user = current_user)
        else:
            return render_template("home_sec.html", user=current_user, grp = grp)