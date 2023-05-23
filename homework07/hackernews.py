import sqlite3

from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route("/news")
def news_list() -> str:
    sess = session()
    rows = sess.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label() -> None:
    sess = session()
    id = request.query.get("id")
    label = request.query.get("label")

    item = sess.query(News).get(id)
    if item is not None:  # Check if item is not None
        item.label = label
        sess.commit()

    redirect("/news")


@route("/update")
def update_news() -> None:
    sess = session()
    news = get_news("https://news.ycombinator.com/newest")

    for element in news:
        title = element.get("title")
        if title is not None:
            if not list(sess.query(News).filter(News.title == title)):
                title = element.get("title", "-")
                author = element.get("author", "-")
                comments = element.get("comments", 0)
                points = element.get("points", 0)
                url = element.get("url", "")
                new_el = News(title=title, author=author, url=url, comments=comments, points=points)
                sess.add(new_el)

    sess.commit()


@route("/classify")
def classify_news() -> None:
    pass


@route("/recommendations")
def recommendations() -> str:
    sess = session()
    news = sess.query(News).filter(News.label == "good").all()

    return template("recs", rows=news)


@route("/")
def index() -> None:
    redirect("/news")


if __name__ == "__main__":
    run(host="localhost", port=8080)
