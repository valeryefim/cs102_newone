import sqlite3

from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    sess = session()
    rows = sess.query(News).filter(News.label == None).limit(50).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    sess = session()
    id = request.query["id"]
    label = request.query["label"]

    item = sess.query(News).get(id)
    item.label = label
    sess.commit()

    redirect("/news")


@route("/update")
def update_news():
    sess = session()
    offset = int(request.query.get("offset", 0))
    limit = 50

    news_count = sess.query(News).count()
    rows = sess.query(News).offset(offset).limit(limit).all()

    if offset >= news_count:
        news = get_news("https://news.ycombinator.com/newest")

        for element in news:
            title = element.get("title", "-")
            if not sess.query(News).filter(News.title == title).first():
                author = element.get("author", "-")
                comments = element.get("comments", 0)
                points = element.get("points", 0)
                url = element.get("url", "")
                new_el = News(title=title, author=author, url=url, comments=comments, points=points)
                sess.add(new_el)

        sess.commit()
        rows = sess.query(News).offset(offset).limit(limit).all()

    redirect("/news")


@route("/classify")
def classify_news():
    sess = session()
    train = sess.query(News).filter(News.label != None).all()
    x = [i.title for i in train]
    y = [i.label for i in train]
    bayes.fit(x, y)
    news = sess.query(News).filter(News.label == None).all()
    X = [i.title for i in news]
    y = bayes.predict(X)
    for i in range(len(news)):
        news[i].label = y[i]
    sess.commit()
    return sorted(news, key=lambda x: x.label)


@route("/recommendations")
def recommendations():
    sess = session()
    news = sess.query(News).filter(News.label == "good").all()

    return template("recs", rows=news)


@route("/")
def index():
    redirect("/news")


if __name__ == "__main__":
    run(host="localhost", port=8080)
