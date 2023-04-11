import asyncio
from aiogram.types import Message, CallbackQuery, InputMedia, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import RetryAfter, MessageNotModified
from datetime import datetime
import json

from handlers.states import addRess, post
from kb import Offline, Inline
from base.db import data
from cfg import settings, get_row, update_row
bot = settings()[1]
storage = settings()[0]
db = data()
ofl = Offline()
inl = Inline()


async def start_command(msg: Message):
    uid = msg.from_user.id
    if db.get_admin(uid):
        await bot.send_message(uid, "Меню", reply_markup=inl.start_menu())
    else:
        if db.not_adm_exc():
            db.add_admin(uid, "owner")
            await bot.send_message(uid, "Меню", reply_markup=inl.start_menu())

async def resurses(call: CallbackQuery):
    uid = call.message.chat.id
    msg = call.message.message_id
    data = db.get_resourses("all")
    if data != None:
        for i in data:
            try:
                title = (await bot.get_chat(i['res_id']))['title']
                db.update_anu("title", title, f"uniq='{i['uniq_id']}'")
            except Exception as e:
                await bot.send_message(uid, e)
    text = "Доступные ресурсы"
    try:
        await call.bot.delete_message(uid, msg)
    except Exception:
        pass
    await call.bot.send_message(uid, text, reply_markup=inl.resourses())

async def backer(call: CallbackQuery, state: FSMContext=None):
    uid = call.message.chat.id
    msg = call.message.message_id
    dest = call.data.split("_")[1]
    try:
        await call.bot.delete_message(uid, msg)
    except Exception:
        pass
    if dest == "Main":
        try:
            to_del = (await state.get_data())
            print(to_del)
            try:
                for i in to_del['msg0']:
                    try:
                        await call.bot.delete_message(uid, i)
                    except Exception:
                        pass
            except KeyError:
                pass
        except Exception:
            pass
        try:
            await state.finish()
        except Exception:
            pass
        await start_command(call)
    elif dest == "Res":
        await resurses(call)
    elif dest == "Post":
        await post.msg0.set()
        to_del = (await state.get_data())
        try:
            for i in to_del['msg0']:
                try:
                    await call.bot.delete_message(uid, i)
                except Exception:
                    pass
        except KeyError:
            pass
        await posting2(call, state)
    elif dest == "pre":
        to_del = (await state.get_data())
        print(to_del)
        try:
            for i in to_del['msg0']:
                try:
                    await call.bot.delete_message(uid, i)
                except Exception:
                    pass
        except KeyError:
            pass
        await preview(call, state)

async def addRes(call: CallbackQuery, state: FSMContext):
    uid = call.message.chat.id
    msg = call.message.message_id
    await call.bot.delete_message(uid, msg)
    text = "Шаг 1. Добавьте бота в канал/чат\n"\
           "Шаг 2. Перешлите боту оттуда любое текстовое сообщение"
    mesg = await bot.send_message(uid, text, reply_markup=inl.back_res())
    await addRess.st.set()
    await state.update_data(msg0=mesg.message_id)

async def getCH(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    mesg = (await state.get_data())['msg0']
    try:
        ch__ = await bot.get_chat(msg['forward_from_chat']['id'])
        chid = ch__['id']
        title = ch__['title']
        r = db.add_channel(chid, title)
        if r == True:
            await bot.delete_message(uid, mesg)
            await bot.delete_message(uid, msg.message_id)
            await bot.send_message(uid, f"Канал <b>{title}</b> был успешно добавлен", reply_markup=inl.resourses())
            await state.finish()
        else:
            await bot.send_message(uid, "Этот канал уже был добавлен")
    except Exception as e:
        await bot.send_message(uid, e)

async def change_status(call: CallbackQuery):
    uid = call.message.chat.id
    msg = call.message.message_id
    chid = call.data.split("_")[1]
    dd = db.get_channel_b(chid)
    sts = {"active": "disactive", "disactive": "active"}
    db.update_anu("status", sts[dd['status']], f"uniq='{dd['uniq_id']}'")
    try:
        await call.bot.edit_message_reply_markup(uid, msg, reply_markup=inl.resourses())
    except Exception as e:
        await bot.send_message(uid, e)

async def delete(call: CallbackQuery):
    uid = call.message.chat.id
    msg = call.message.message_id
    chid = call.data.split("_")[1]
    db.delete_channel(chid)
    try:
        await call.answer("Удалено успешно", True)
        await call.bot.edit_message_reply_markup(uid, msg, reply_markup=inl.resourses())
    except Exception:
        pass

async def settings(call: CallbackQuery):
    uid = call.message.chat.id
    msg = call.message.message_id
    text = "Делай че хочешь"
    await call.bot.delete_message(uid, msg)
    await call.bot.send_message(uid, text, reply_markup=inl.sett())

async def ch_sett(call: CallbackQuery):
    uid = call.message.chat.id
    msg = call.message.message_id
    data = call.data.split("_")
    with open("./settings.txt", "r") as f:
        soup = f.read()
        timeout = int(soup.split("_")[0])
        end = soup.split("_")[1]
        rounds = int(soup.split("_")[2])
        f.close()
    with open("./settings.txt", "w+") as f:
        if data[1] == "time":
            to = data[2]
            if to == "up":
                if int(timeout) == 100:
                    timeout = 10
                else:
                    timeout += 10
            elif to == "chend":
                endth0 = {"s": "m", "m": "h", "h": "s"}
                end = endth0[end]
            else:
                if int(timeout) == 0:
                    timeout = 100
                else:
                    timeout -= 10
        else:
            to = data[2]
            if to == "up":
                if int(rounds) == 100:
                    rounds = 1
                else:
                    rounds += 1
            else:
                if int(rounds) == 1:
                    rounds = 100
                else:
                    rounds -= 1
        f.write(f"{timeout}_{end}_{rounds}")
        f.close()
        await call.bot.edit_message_reply_markup(uid, msg, reply_markup=inl.sett())

async def posting(call: CallbackQuery, state: FSMContext):
    uid = call.message.chat.id
    msg = call.message.message_id
    text = "рассылка"
    try:
        await call.bot.delete_message(uid, msg)
    except Exception:
        pass
    mesg = await call.bot.send_message(uid, text, reply_markup=inl.posting1(media="no", text="no", kb="no"))
    await post.msg0.set()
    await state.update_data(media="no", text="no", kb="no")

async def posting2(call: CallbackQuery, state: FSMContext):
    uid = call.message.chat.id
    text = "рассылка"
    datas = (await state.get_data())
    await call.bot.send_message(uid, text, reply_markup=inl.posting1(media=datas['media'], text=datas['text'], kb=datas['kb']))

async def get_saved(call: CallbackQuery, state: FSMContext):
    uid = call.message.chat.id
    msg = call.message.message_id
    saved = json.loads((get_row()[1]).replace("'",'"'))
    print(saved)
    text = "no"
    kb = "no"
    for i in saved:
        for k,v in i.items():
            if k == "text":
                text = "yes"
            elif k == "kb":
                kb = "yes"
    await state.update_data(media=saved, text=text, kb=kb)
    await call.answer("Черновик загружен", True)
    datas = (await state.get_data())
    try:
        await call.bot.edit_message_reply_markup(uid, msg, reply_markup=inl.posting1(media=datas['media'], text=datas['text'], kb=datas['kb']))
    except MessageNotModified:
        pass

async def choosing(call: CallbackQuery, state: FSMContext):
    uid = call.message.chat.id
    msg = call.message.message_id
    to = call.data.split("_")[0]
    dest = call.data.split("_")[1]
    if to == "delete":
        if dest == "media":
            dat = await state.get_data()
            await state.update_data(media=db.cut(dat['media'], ["text","kb"]))
            dat = await state.get_data()
            try:
                await call.bot.edit_message_reply_markup(uid, msg, reply_markup=inl.posting1(media=dat["media"], text=dat['text'], kb=dat['kb']))
            except MessageNotModified:
                pass
        if dest == "text":
            await state.update_data(text="no")
            dat = await state.get_data()
            await state.update_data(media=db.cut(dat['media'], ["photo","video","voice","note","sticker","audio","document","kb"]))
            dat = await state.get_data()
            try:
                await call.bot.edit_message_reply_markup(uid, msg, reply_markup=inl.posting1(media=dat["media"], text=dat['text'], kb=dat['kb']))
            except MessageNotModified:
                pass
        if dest == "kb":
            await state.update_data(kb="no")
            dat = await state.get_data()
            await state.update_data(media=db.cut(dat['media'], ["photo","video","voice","note","sticker","audio","document","text"]))
            dat = await state.get_data()
            try:
                await call.bot.edit_message_reply_markup(uid, msg, reply_markup=inl.posting1(media=dat["media"], text=dat['text'], kb=dat['kb']))
            except MessageNotModified:
                pass
    else:
        if to == "media":
            await post.media.set()
            await call.bot.delete_message(uid, msg)
            await call.bot.send_message(uid, "Отправляйте медиа либо нажмите на кнопки", reply_markup=inl.back_post_kb())
        elif to == "text":
            await post.text.set()
            await call.bot.delete_message(uid, msg)
            await call.bot.send_message(uid, "Отправляйте текста либо нажмите на кнопки", reply_markup=inl.back_post_kb())
        elif to == "kb":
            await post.kb.set()
            await call.bot.delete_message(uid, msg)
            await call.bot.send_message(uid, "введите клавиатуру в формате\n<code>текст - ссылка</code>", reply_markup=inl.back_post_kb())
        elif to == "no":
            await preview(call, state)

async def post_text(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    text = msg.text
    mesg = msg.message_id
    st_text = (await state.get_data())['media']
    print(await state.get_data(), "post_text")
    if st_text == "no":
        st_text = []
    st_text.append({"text": text})
    await state.update_data(media=st_text)
    await state.update_data(text="yes")
    await bot.delete_message(uid, mesg)

async def post_photo(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    photo = msg.photo[-1].file_id
    mesg = msg.message_id
    st_media = (await state.get_data())['media']
    if st_media == "no":
        st_media = []
    st_media.append({"photo": photo})
    await state.update_data(media=st_media)
    await bot.delete_message(uid, mesg)

async def post_video(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    video = msg['video']['file_id']
    mesg = msg.message_id
    st_media = (await state.get_data())['media']
    if st_media == "no":
        st_media = []
    st_media.append({"video": video})
    await state.update_data(media=st_media)
    await bot.delete_message(uid, mesg)

async def post_note(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    note = msg['video_note']['file_id']
    mesg = msg.message_id
    st_media = (await state.get_data())['media']
    if st_media == "no":
        st_media = []
    st_media.append({"note": note})
    await state.update_data(media=st_media)
    await bot.delete_message(uid, mesg)

async def post_voice(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    voice = msg['voice']['file_id']
    mesg = msg.message_id
    st_media = (await state.get_data())['media']
    if st_media == "no":
        st_media = []
    st_media.append({"voice": voice})
    await state.update_data(media=st_media)
    await bot.delete_message(uid, mesg)

async def post_audio(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    audio = msg['audio']['file_id']
    mesg = msg.message_id
    st_media = (await state.get_data())['media']
    if st_media == "no":
        st_media = []
    st_media.append({"audio": audio})
    await state.update_data(media=st_media)
    await bot.delete_message(uid, mesg)

async def post_doc(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    doc = msg['document']['file_id']
    mesg = msg.message_id
    st_media = (await state.get_data())['media']
    if st_media == "no":
        st_media = []
    st_media.append({"document": doc})
    await state.update_data(media=st_media)
    await bot.delete_message(uid, mesg)

async def post_sticker(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    stick = msg.sticker.file_id
    mesg = msg.message_id
    st_media = (await state.get_data())['media']
    if st_media == "no":
        st_media = []
    st_media.append({"sticker": stick})
    await state.update_data(media=st_media)
    await bot.delete_message(uid, mesg)

async def post_kb(msg: Message, state: FSMContext):
    uid = msg.from_user.id
    text = msg.text.split("\n")
    mesg = msg.message_id
    st_text = (await state.get_data())['media']
    if st_text == "no":
        st_text = []
    for i in text:
        st_text.append({"kb": i})
    await state.update_data(media=st_text)
    await state.update_data(kb="yes")
    await bot.delete_message(uid, mesg)

async def preview(call: CallbackQuery, state: FSMContext):
    uid = call.message.chat.id
    msg = call.message.message_id
    data = (await state.get_data())['media']
    to_del = []
    if isinstance(data, list) and all(isinstance(item, dict) for item in data) and any(key != "kb" for item in data for key in item.keys()):
        order = get_row()[0]
        so = db.sort(data, order)
        sortd = so[0]
        kb = so[1]
        while True:
            try:
                mesg = await call.bot.send_message(uid, "Вот так выглядит рассылка:")
                to_del.append(mesg.message_id)
                break
            except RetryAfter as e:
                await asyncio.sleep(e.timeout)
        for i in sortd:
            for k,v in i.items():
                typ = k
                file_id = v
            if typ == "text":
                while True:
                    try:
                        mesg = await call.bot.send_message(uid, file_id)
                        to_del.append(mesg.message_id)
                        break
                    except RetryAfter as e:
                        await asyncio.sleep(e.timeout)
            elif typ == "photo":
                while True:
                    try:
                        mesg = await call.bot.send_photo(uid, file_id)
                        to_del.append(mesg.message_id)
                        break
                    except RetryAfter as e:
                        await asyncio.sleep(e.timeout)
            elif typ == "video":
                while True:
                    try:
                        mesg = await call.bot.send_video(uid, file_id)
                        to_del.append(mesg.message_id)
                        break
                    except RetryAfter as e:
                        await asyncio.sleep(e.timeout)
            elif typ == "note":
                while True:
                    try:
                        mesg = await call.bot.send_video_note(uid, file_id)
                        to_del.append(mesg.message_id)
                        break
                    except RetryAfter as e:
                        await asyncio.sleep(e.timeout)
            elif typ == "voice":
                while True:
                    try:
                        mesg = await call.bot.send_voice(uid, file_id)
                        to_del.append(mesg.message_id)
                        break
                    except RetryAfter as e:
                        await asyncio.sleep(e.timeout)
            elif typ == "audio":
                while True:
                    try:
                        mesg = await call.bot.send_audio(uid, file_id)
                        to_del.append(mesg.message_id)
                        break
                    except RetryAfter as e:
                        await asyncio.sleep(e.timeout)
            elif typ == "document":
                while True:
                    try:
                        mesg = await call.bot.send_audio(uid, file_id)
                        to_del.append(mesg.message_id)
                        break
                    except RetryAfter as e:
                        await asyncio.sleep(e.timeout)
            elif typ == "sticker":
                while True:
                    try:
                        mesg = await call.bot.send_sticker(uid, file_id)
                        to_del.append(mesg.message_id)
                        break
                    except RetryAfter as e:
                        await asyncio.sleep(e.timeout)
        await state.update_data(msg0=to_del)
        text = "<b>Предпросмотр</b>\n\n"\
            "<i>Добавленная клавиатура:</i>\n"
        if len(kb) < 1:
            text += "<i>Нет</i>\n"
        else:
            for i in kb:
                for k,v in i.items():
                    title = k
                    url = v
                text += f"<i>{title} - {url}</i>\n"
        text += "\n<b>Взаимодействуй с кнопками:</b>"
        try:
            await call.bot.delete_message(uid, msg)
        except Exception:
            pass
        while True:
            try:
                await call.bot.send_message(uid, text, reply_markup=inl.send_post(), disable_web_page_preview=True)
                break
            except RetryAfter as e:
                await asyncio.sleep(e.timeout)
        await post.settigs.set()
    elif data == "no":
        await call.answer("Вы не добавили ничего...\nЧто мне отправлять?", True)
    else:
        await call.answer("Нельзя отправить только кнопки", True)

async def save_post(call: CallbackQuery, state: FSMContext):
    data = (await state.get_data())['media']
    update_row(last_post=data)
    await call.answer("Черновик сохранен", True)

async def change_ord(call: CallbackQuery, state: FSMContext):
    uid = call.message.chat.id
    msg = call.message.message_id
    text = "Настройки порядка постинга:"
    to_del = (await state.get_data())['msg0']
    for i in to_del:
        try:
            await call.bot.delete_message(uid, i)
        except Exception:
            pass
    await call.bot.delete_message(uid, msg)
    await call.bot.send_message(uid, text, reply_markup=inl.change_ord(get_row()[0].split(",")))

async def change_ord2(call: CallbackQuery, state: FSMContext):
    uid = call.message.chat.id
    msg = call.message.message_id
    dest = call.data.split("_")[1]
    el = call.data.split("_")[2]
    data = db.move_element(get_row()[0], el, dest)
    update_row(row1=data)
    try:
        await call.bot.edit_message_reply_markup(uid, msg, reply_markup=inl.change_ord(data.split(",")))
    except MessageNotModified:
        pass

async def posting3(call: CallbackQuery, state: FSMContext):
    uid = call.message.chat.id
    msg = call.message.message_id
    to_del = (await state.get_data())['msg0']
    data = (await state.get_data())['media']
    order = get_row()[0]
    so = db.sort(data, order)
    sortd = so[0]
    usr_kb = inl.post_keyb(so[1])
    for i in to_del:
        try:
            await call.bot.delete_message(uid, i)
        except Exception:
            pass
    with open("./settings.txt", "r") as f:
        soup = f.read()
        timeout = int(soup.split("_")[0])
        end = soup.split("_")[1]
        rounds = int(soup.split("_")[2])
        f.close()
    to = db.get_resourses("active")
    r = 0
    status = "Рассылка..."
    wait = "0"
    text = "Идет рассылка"
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("📊 Статус", callback_data="000"), InlineKeyboardButton("🔄 Круг", callback_data="000"), InlineKeyboardButton("⏳ Ожидание", callback_data="000")
    )
    kb.add(
        InlineKeyboardButton(status, callback_data="000"),  InlineKeyboardButton(str(r)+"/"+str(rounds), callback_data="000"),  InlineKeyboardButton(str(wait)+"/"+str(timeout), callback_data="000")
    )
    await state.finish()
    await call.bot.delete_message(uid, msg)
    meg = await call.bot.send_message(uid, text, reply_markup=kb)
    await start_command(call)
    for anu in range(rounds):
        r += 1
        mesg = meg.message_id
        for chat in to:
            d = 0
            chatid = chat['res_id']
            for i in sortd:
                l = len(sortd)
                d += 1
                for k,v in i.items():
                    typ = k
                    file_id = v
                if typ == "text":
                    while True:
                        try:
                            if d < l:
                                await call.bot.send_message(chatid, file_id)
                            else:
                                await call.bot.send_message(chatid, file_id, reply_markup=usr_kb)
                            break
                        except RetryAfter as e:
                            await asyncio.sleep(e.timeout)
                elif typ == "photo":
                    while True:
                        try:
                            if d < l:
                                await call.bot.send_photo(chatid, file_id)
                            else:
                                await call.bot.send_photo(chatid, file_id, reply_markup=usr_kb)
                            break
                        except RetryAfter as e:
                            await asyncio.sleep(e.timeout)
                elif typ == "video":
                    while True:
                        try:
                            if d < l:
                                await call.bot.send_video(chatid, file_id)
                            else:
                                await call.bot.send_video(chatid, file_id, reply_markup=usr_kb)
                            break
                        except RetryAfter as e:
                            await asyncio.sleep(e.timeout)
                elif typ == "note":
                    while True:
                        try:
                            if d < l:
                                await call.bot.send_video_note(chatid, file_id)
                            else:
                                await call.bot.send_video_note(chatid, file_id, reply_markup=usr_kb)
                            break
                        except RetryAfter as e:
                            await asyncio.sleep(e.timeout)
                elif typ == "voice":
                    while True:
                        try:
                            if d < l:
                                await call.bot.send_voice(chatid, file_id)
                            else:
                                await call.bot.send_voice(chatid, file_id, reply_markup=usr_kb)
                            break
                        except RetryAfter as e:
                            await asyncio.sleep(e.timeout)
                elif typ == "audio":
                    while True:
                        try:
                            if d < l:
                                await call.bot.send_audio(chatid, file_id)
                            else:
                                await call.bot.send_audio(chatid, file_id, reply_markup=usr_kb)
                            break
                        except RetryAfter as e:
                            await asyncio.sleep(e.timeout)
                elif typ == "document":
                    while True:
                        try:
                            if d < l:
                                await call.bot.send_audio(chatid, file_id)
                            else:
                                await call.bot.send_audio(chatid, file_id, reply_markup=usr_kb)
                            break
                        except RetryAfter as e:
                            await asyncio.sleep(e.timeout)
                elif typ == "sticker":
                    while True:
                        try:
                            if d < l:
                                await call.bot.send_sticker(chatid, file_id)
                            else:
                                await call.bot.send_sticker(chatid, file_id, reply_markup=usr_kb)
                            break
                        except RetryAfter as e:
                            await asyncio.sleep(e.timeout)
        kb = InlineKeyboardMarkup(row_width=3)
        kb.add(
            InlineKeyboardButton("📊 Статус", callback_data="000"), InlineKeyboardButton("🔄 Круг", callback_data="000"), InlineKeyboardButton("⏳ Ожидание", callback_data="000")
        )
        kb.add(
            InlineKeyboardButton(status, callback_data="000"),  InlineKeyboardButton(str(r)+"/"+str(rounds), callback_data="000"),  InlineKeyboardButton(str(wait)+"/"+str(timeout), callback_data="000")
        )
        if timeout != 0:
            if end == "s":
                sleep = timeout
            elif end == "m":
                sleep = timeout*60
            elif end == "h":
                sleep = timeout*60*60
            for i in range(sleep+1):
                endth = sleep-i
                h = endth//3600
                mins = (endth%3600)//60
                secs = endth%60
                timer_str = ""
                if h > 0:
                    timer_str += f"{h}h "
                if mins > 0 or h > 0:
                    timer_str += f"{mins}m "
                timer_str += f"{secs}s"
                wait = timer_str
                try:
                    kb = InlineKeyboardMarkup(row_width=3)
                    kb.add(
                        InlineKeyboardButton("📊 Статус", callback_data="000"), InlineKeyboardButton("🔄 Круг", callback_data="000"), InlineKeyboardButton("⏳ Ожидание", callback_data="000")
                    )
                    kb.add(
                        InlineKeyboardButton(status, callback_data="000"),  InlineKeyboardButton(str(r)+"/"+str(rounds), callback_data="000"),  InlineKeyboardButton(str(wait)+"/"+str(timeout), callback_data="000")
                    )
                    await call.bot.edit_message_reply_markup(uid, mesg, reply_markup=kb)
                except MessageNotModified:
                    pass
                await asyncio.sleep(1)
        try:
            await call.bot.edit_message_reply_markup(uid, mesg, reply_markup=kb)
        except MessageNotModified:
            pass
    await call.bot.edit_message_text(f"Рассылка завершена\nКругов:{str(rounds)}", uid, mesg)
    
    