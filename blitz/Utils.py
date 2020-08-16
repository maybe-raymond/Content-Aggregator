from blitz.models import Article

def check(s):
    data = Article.query.filter_by(source= s).all()
    return data
