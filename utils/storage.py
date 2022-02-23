# -*- coding: utf-8 -*-
# Author: Vladimir Pichugin <vladimir@pichug.in>
import pymongo
import datetime

from .data import *
from .helpers import init_logger


logger = init_logger()


class Storage:
    def __init__(self, connect, database, collection):
        self.mongo_client = pymongo.MongoClient(connect, authSource='admin')
        self.db = self.mongo_client.get_database(database)
        self.schedule = self.db.get_collection(collection)

    def get_schedule(self, date: datetime.datetime):
        key = date.strftime('%d-%m-%y')

        data = self.get_data(self.schedule, key)
        if not data:
            return None

        schedule = ScheduleArticle(data)

        return schedule

    def save_schedule(self, schedule: ScheduleArticle) -> bool:
        _id = schedule['date'].strftime('%d-%m-%y')
        schedule['_id'] = _id

        if not schedule.changed:
            logger.debug(f'Schedule <{_id}> already saved, data not changed.')
            return True

        schedule['timestamp'] = int(datetime.datetime.now().timestamp())

        save_result = self.save_data(self.schedule, _id, schedule)
        if save_result:
            logger.debug(f'Schedule <{_id}> saved, result: {save_result}')
            return True

        logger.error(f'Schedule <{_id}> not saved, result: {save_result}')

        return False

    @staticmethod
    def get_data(c: pymongo.collection.Collection, value, name="_id"):
        data = c.find_one({name: value})

        if data:
            return SDict(data)

        return None

    @staticmethod
    def save_data(c: pymongo.collection.Collection, value, data: SDict, name="_id"):
        if c.find_one({name: value}):
            operation = c.update_one({name: value}, {"$set": data})
            result = operation.raw_result if operation else None
        else:
            operation = c.insert_one(data)
            result = operation.inserted_id if operation else None

        return result
