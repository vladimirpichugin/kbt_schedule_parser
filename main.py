# -*- coding: utf-8 -*-
# Author: Vladimir Pichugin <vladimir@pichug.in>
import time
import threading

from utils import *

logger = init_logger()
logger.info("Initializing..")

try:
    logger.info("Initializing storage..")
    storage = Storage(Settings.MONGO, Settings.MONGO_DATABASE, Settings.MONGO_COLLECTION)
    logger.debug(f"MongoDB Server version: {storage.mongo_client.server_info()['version']}")
except Exception as e:
    logger.error('Storage crashed', exc_info=True)
    raise RuntimeError from e


def run_threaded(name, func):
    job_thread = threading.Thread(target=func)
    job_thread.setName(f'{name}Thread')
    job_thread.start()


def schedule_parser():
    try:
        t = Settings.SCHEDULE_TIME
        g = CollegeScheduleGrabber(Settings.DOMAIN, Settings.BLOG_PATH)

        while True:
            try:
                today = datetime.datetime.today()
                today = today.replace(hour=0, minute=0, second=0, microsecond=0)

                articles = g.parse_articles()

                if not articles:
                    time.sleep(t)
                    continue

                articles = CollegeScheduleAbc.get_articles(articles)

                for article in articles:
                    article_date = article.get('date')
                    article_path = article.get('link')

                    if not article_date:
                        continue

                    if article_date >= today:
                        article_groups = g.parse_article(article_path)
                        article['data'] = article_groups
                        storage.save_schedule(article)
            except:
                logger.error('Exception in schedule parser loop', exc_info=True)

            time.sleep(t)
    except:
        logger.error('Schedule parser loop crashed', exc_info=True)
