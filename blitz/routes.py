from datetime import datetime
from blitz import app, db, bcrypt, mail
from flask import render_template, redirect, url_for, flash
from blitz.tasks import Get_data
from blitz.Utils import check
from blitz.forms import Comment_Form , registration_Form, Login_Form, Choice_Form
from blitz.models import Article, Comment, User, Exchange_rate, Covid
from flask_login import current_user, login_user , logout_user, login_required
from flask_mail import Message



@app.route("/")
def home():
    now = datetime.utcnow()
    #if now.strftime("%H%M") =="0000" or   now.strftime("%H%M") =="0600" or now.strftime("%H%M") =="1200" or now.strftime("%H%M") =="1800":
    Get_data.delay()
    hearld = Article.query.filter_by(source="THE Herald").order_by(Article.date.desc()).paginate(per_page=5)
    h_metro = Article.query.filter_by(source="H-Metro").order_by(Article.date.desc()).paginate(per_page=5)
    daily_news = Article.query.filter_by(source="Daily News").order_by(Article.date.desc()).paginate(per_page=5)
    the_zim = Article.query.filter_by(source="The Zimbabwean").order_by(Article.date.desc()).paginate(per_page=5)
    news_day = Article.query.filter_by(source="NewsDay").order_by(Article.date.desc()).paginate(per_page=5)
    return render_template("home.html", hearld=hearld, h_metro=h_metro, daily_news=daily_news, the_zim=the_zim ,news_day=news_day )


@app.route("/<article_id>", methods=["GET", 'POST'])
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    form = Comment_Form()
    if form.validate_on_submit():
        print("submited")
        comment = Comment(content=form.content.data,  article_post=article_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view_article',article_id=article_id ))
    comments = Comment.query.filter_by(article_post=article_id)
    return render_template("article_view.html", form=form, article=article, comments=comments)


@app.route("/registration", methods=["GET", 'POST'])
def registration():
    form = registration_Form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(Username= form.username.data ,Email= form.email.data , password=hashed_password)
        db.session.add(user)
        db.session.commit()
        if form.check.data:
            print("hello")
        flash(f"your account has been created")
        return redirect(url_for("home"))
    return render_template("registration_form.html", form=form)


@app.route("/Log in", methods=["GET", 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Login_Form()
    if form.validate_on_submit():
        print("submitted")
        user = User.query.filter_by(Username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"you have logged in")
            return redirect(url_for("home"))
        else:
            flash(f"unsuccesfull login ", "danger")
    return render_template("login.html", form=form)


@login_required
@app.route("/account",  methods=["GET", 'POST'])
def account():
     form = Choice_Form()
     if form.validate_on_submit():
        follow = Followers()
        if form.hearld.data:
             f1 = follow(user_id=current_user, article_source=("THE Herald"))
             db.session.add(f1)
        if form.Hmetro.data:
            f2 = follow(user_id=current_user, article_source=("H-Metro"))
            db.session.add(f2)
        if form.Dailynews.data:
            f3 = follow(user_id=current_user, article_source=("Daily News"))
            db.session.add(f3)
        if form.The_Zimbabwean.data:
            f4 = follow(user_id=current_user, article_source=("The Zimbabwean"))
            db.session.add(f4)
        if form.NewsDay.data:
            f5 = follow(user_id=current_user, article_source=("NewsDay"))
            db.session.add(f5)

     return render_template('account.html', form=form)


@app.route("/logout", methods=["GET", 'POST'])
def Logout():
    logout_user()
    return ('home.html')


@app.route("/more/<article_source>", methods=["GET", 'POST'])
def View_more(article_source):
    source = Article.query.filter_by(source=article_source).order_by(Article.date.desc()).paginate(per_page=20)
    return render_template('view_more.html', source=source, a=article_source)


@app.route("/exchange rate", methods=["GET", 'POST'])
def Exchange():
    zimrates = Exchange_rate.query.filter_by(name="zimrates").order_by(Exchange_rate.date.desc()).first()
    OMIR =  Exchange_rate.query.filter_by(name="OMIR").order_by(Exchange_rate.date.desc()).first()
    interbank =  Exchange_rate.query.filter_by(name="interbank").order_by(Exchange_rate.date.desc()).first()
    zimrates_bond =  Exchange_rate.query.filter_by(name="zimrates_bond").order_by(Exchange_rate.date.desc()).first()
    return render_template("Exchange.html", zimrates=zimrates, OMIR=OMIR,  interbank=interbank,  zimrates_bond=zimrates_bond)


@app.route("/covid 19 rates", methods=["GET", 'POST'])
def Covid_19():
    source = Covid.query.order_by(Covid.date.desc()).first()
    return render_template("Covid_19.html", s=source)




@app.route("/email", methods=["GET", 'POST'])
def test():
        msg = Message("hello",
                  sender="mugandiwaraymond@gmail.com",
                  recipients =["raymondnigel@live.com"])
        msg.body="test maybe it will work or maybe not"
        mail.send(msg)
        return "sent"
