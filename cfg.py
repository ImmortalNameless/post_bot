from configparser import ConfigParser
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
import logging as l

def get_token():
    conf = ConfigParser()
    conf.read("./cfg.ini")
    token = conf['tg']['token']
    return token

def get_row():
    conf = ConfigParser()
    conf.read("./rowid.ini")
    token = conf['rows']['row1']
    post = conf['rows']['last_post']
    return token, post

def update_row(**data):
    conf = ConfigParser()
    conf.read("./rowid.ini")
    for k,v in data.items():
        conf.set("rows", k,str(v))
        with open("./rowid.ini", "w") as conff:
            conf.write(conff)
            conff.close()

def settings():
    """
    returns:
        storage = arg[0]\n
        bot = arg[1]\n
        dp = arg[2]
    """
    l.basicConfig(format=u'%(filename)s запущен',
                    level=l.INFO)
    storage = MemoryStorage()
    bot = Bot(get_token(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())
    return storage, bot, dp