from datetime import datetime
from blitz import app, db, mail
from flask import render_template, redirect, url_for, flash, request
from blitz.tasks import Get_data
import os
from blitz.Utils import check
from blitz.forms import registration_Form, Choice_Form
from blitz.models import Article, User, Exchange_rate, Covid, Followers
from blitz.Utils import  get_Followers, all_news
from flask_mail import Message
from sqlalchemy import and_


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


@app.route("/newsletter/registration", methods=["GET", 'POST'])
def registration():
    form = registration_Form()
    if form.validate_on_submit():
        user = User(Email= form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f"you have been added to the newsletter")
        return redirect(url_for("account", email=form.email.data))
    return render_template("registration_form.html", form=form)



@app.route("/newsletter/Choice",  methods=["GET", 'POST'])
def account():
     form = Choice_Form()
     if form.validate_on_submit():
        email = request.args.get("email")
        p = User.query.filter_by(Email= email).first()
        if form.hearld.data:
             f1 = Followers(user_id=p.id, article_source="THE Herald")
             db.session.add(f1)
        if form.Hmetro.data:
            f2 = Followers(user_id=p.id, article_source= "H-Metro")
            db.session.add(f2)
        if form.Dailynews.data:
            f3 = Followers(user_id=p.id, article_source= "Daily News")
            db.session.add(f3)
        if form.The_Zimbabwean.data:
            f4 = Followers(user_id=p.id, article_source= "The Zimbabwean")
            db.session.add(f4)
        if form.NewsDay.data:
            f5 = Followers(user_id=p.id, article_source= "NewsDay" )
            db.session.add(f5)
        db.session.commit()
        return redirect(url_for("Thank_you"))
     return render_template('account.html', form=form)



@app.route("/more/<article_source>", methods=["GET", 'POST'])
def View_more(article_source):
    source = Article.query.filter_by(source=article_source).order_by(Article.date.desc()).paginate(per_page=20)
    return render_template('view_more.html', source=source, a=article_source)


@app.route("/thank you", methods=["GET", 'POST'])
def Thank_you():
    return render_template('thanks.html')



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
def send_email():
    user = User.query.all()
    with mail.connect() as conn:
        for i in user:
            if Followers.query.filter_by(user_id=i.id).first():
                c = get_Followers(i)
                all = all_news(c)
                subject = f"These are all the great News stories you have missed this week"
                message = render_template("Email.html", news=all)
                msg = Message(recipients =[i.Email],
                              sender=os.environ.get('address'),
                              html=message, subject=subject)
                conn.send(msg)
    return f"sent"

@app.route("/hello")
def test_email():
    hearld = Article.query.filter(and_(Article.source=="THE Herald",Article.source=="H-Metro",Article.source=="Daily News",Article.source=="The Zimbabwean")).order_by(Article.date.desc()).limit(5).all()
    #h_metro = Article.query.filter_by(source="H-Metro").order_by(Article.date.desc())
    #daily_news = Article.query.filter_by(source="Daily News").order_by(Article.date.desc())
    #the_zim = Article.query.filter_by(source="The Zimbabwean").order_by(Article.date.desc())
    #news_day = Article.query.filter_by(source="NewsDay").order_by(Article.date.desc())
    #p1 = hearld.union_all(h_metro, daily_news, the_zim, news_day)
    return render_template("h.html", news=hearld)
