# -*- coding: utf-8 -*-
# Author: Vladimir Pichugin <vladimir@pichug.in>


class Settings:
    DEBUG = False

    MONGO = ''
    MONGO_DATABASE = ''
    MONGO_COLLECTION = ''

    SCHEDULE_TIME = 60 * 10  # Частота обращений к сайту за расписанием, в секундах.

    DOMAIN = 'https://cbcol.mskobr.ru'
    BLOG_PATH = '/elektronnye_servisy/blog/'
