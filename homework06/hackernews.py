from bottle import redirect, request, route, run, template  # type: ignore
from sqlalchemy.orm import load_only  # type: ignore

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    news = s.query(News).filter(News.id == request.query.id).one()
    news.label = request.query.label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    current_news = get_news("https://news.ycombinator.com/newest")
    existing_news = s.query(News).options(load_only("title", "author")).all()
    existing_t_a = [(news.title, news.author) for news in existing_news]
    for news in current_news:
        if (news["title"], news["author"]) not in existing_t_a:
            news_add = News(
                title=news["title"],
                author=news["author"],
                url=news["url"],
                comments=news["comments"],
                points=news["points"],
            )
            s.add(news_add)
    s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    train_news = s.query(News).filter(News.label != None).all()
    x_train = [row.title for row in train_news]
    y_train = [row.label for row in train_news]
    classifier.fit(x_train, y_train)
    test_news = s.query(News).filter(News.label == None).all()
    x = [row.title for row in test_news]
    labels = classifier.predict(x)
    good = [test_news[i] for i in range(len(test_news)) if labels[i] == "good"]
    maybe = [test_news[i] for i in range(len(test_news)) if labels[i] == "maybe"]
    never = [test_news[i] for i in range(len(test_news)) if labels[i] == "never"]
    return template("news", {"good": good, "never": never, "maybe": maybe})


if __name__ == "__main__":
    s = session()
    classifier = NaiveBayesClassifier()
    marked_news = s.query(News).filter(News.label != None).all()
    x_train = [row.title for row in marked_news]
    y_train = [row.label for row in marked_news]
    classifier.fit(x_train, y_train)

    run(host="localhost", port=8080)
