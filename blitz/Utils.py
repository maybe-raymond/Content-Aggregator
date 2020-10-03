from blitz.models import Article, User, Followers
from sqlalchemy import and_

def check(s):
    data = Article.query.filter_by(source= s).all()
    return data

def get_Followers(id):
    follow =[]
    p = Followers.query.filter_by(user_id=id.id)
    for n in p:
        follow.append(n.article_source)
    return follow

def all_news(follow):
    m = 0
    p1 = Article.query.filter_by(source=follow[0])
    follow.pop(0)
    for k,v in list(enumerate(follow)):
        p2 = Article.query.filter_by(source=follow[k])
        m = p1.union(p2)
    return m
