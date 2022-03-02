from .main import app, stats
from .db import insert_post
from bs4 import BeautifulSoup
from langdetect import detect
import fasttext as ft
import requests
import re
import os

model = ft.load_model('./celery_app/model/clarin.kgr10.20.bin')
date_newest = "0"

@app.task(ignore_result=True)
def save_to_db(post):
    if not post:
        return
    insert_post(post)
    print('Saved to db {post}')

@app.task
def vectorize(post):
    if not post:
        return
    post['vector'] = model.get_sentence_vector(post['text']).tolist()

    return post


@app.task(bind=True)
def check_language(self, post):
    lang = detect(post['text'])
    raport_metric_language(lang)
    
    if lang != 'pl':
        self.request.callbacks = None # abort chain
        return
    else:
        return post


@app.task(ignore_result=True)
@stats.timer('wykop_pipeline.request_times')
def scrap_wykop():

    html = requests.get("https://www.wykop.pl/tag/wroclaw/wszystkie").text
    soup = BeautifulSoup(html, "html.parser")
    posts = soup.find("div", {"id": "content"}).find_all("li", {"class": "entry iC"})

    global date_newest
    if date_newest == get_date(posts[0]):
        return

    results = []

    for post in posts[:10]:

        upper_bar = post.find("div", {"class": "author ellipsis"})
        author = upper_bar.find("b").text
        date = upper_bar.find("time")["title"]
        reactions_num = int(upper_bar.find("p", {"class": "vC"})["data-vc"])

        text = post.find("div", {"class": "text"}).find("p").text
        clean_text = re.sub(r"\r|\t|\n", " ", text).strip()

        comments_block = post.find("ul", {"class": "sub"}, recursive=False)

        if comments_block:
            li_list = comments_block.find_all("li", recursive=False)
            comments_num = len(li_list)
            if comments_num > 2:
                more_comments_text = li_list[2].find("a").text
                more_comments_num = re.search("\(.*\)", more_comments_text).group()[
                    1:-1
                ]
                comments_num += int(more_comments_num)
                comments_num -= 1
        else:
            comments_num = 0

        result = {
            "author": author,
            "text": clean_text,
            "date": date,
            "reactions_num": reactions_num,
            "comments_num": comments_num,
        }

        results.append(result)

        (check_language.s(result) | vectorize.s() | save_to_db.s())()

    raport_metric(results)
    date_newest = results[0]['date']


def raport_metric(results):
    comments_num = sum(map(lambda r: r['comments_num'], results))
    reactions_num = sum(map(lambda r: r['reactions_num'], results))
    posts_num = len(results)

    stats.gauge('wykop_pipeline.number_of_posts', posts_num)
    stats.incr('wykop_pipeline.number_of_comments', comments_num)
    stats.incr('wykop_pipeline.number_of_pluses', reactions_num)

def raport_metric_language(lang):
    stats.incr('wykop_pipeline.lang.'+ lang, 1)

def get_date(post):
    upper_bar = post.find("div", {"class": "author ellipsis"})
    date = upper_bar.find("time")["title"]
    return date