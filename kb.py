from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from base.db import data

db = data()

class Offline:

    def __init__(self) -> None:
        self.get_ap = KeyboardButton("Открыть Админ панель")

    def get_AP(self):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(self.get_ap)
        return kb


class Inline:

    def __init__(self) -> None:
        self.res = InlineKeyboardButton("🗂 Ресурсы", callback_data="resourses")
        self.post = InlineKeyboardButton("📫 Рассылка", callback_data="post")
        self.settings = InlineKeyboardButton("⚙️ Настройки", callback_data="settings")
        self.st_on = InlineKeyboardButton("🟢", callback_data="000")
        self.st_of = InlineKeyboardButton("🔴", callback_data="000")
        self.add_res = InlineKeyboardButton("➕ Добавить", callback_data="addRes")

        self.back_Main = InlineKeyboardButton("🏠 На Главную", callback_data="back_Main")
        self.back_Res = InlineKeyboardButton("🔙 Назад", callback_data="back_Res")
        self.back_post = InlineKeyboardButton("🔙 Назад", callback_data="back_Post")
        self.back_pre = InlineKeyboardButton("🔙 Назад", callback_data="back_pre")

        self.get_saved = InlineKeyboardButton("Черновик", callback_data="get_saved")
        self.save = InlineKeyboardButton("📥 Сохранить", callback_data="save")
        self.post_send = InlineKeyboardButton("📫 Отправить", callback_data="post")
        self.pre = InlineKeyboardButton("Предпросмотр", callback_data="no_preview")
        self.change_Ord = InlineKeyboardButton("Изменить порядок", callback_data="changeOrd")


    def start_menu(self):
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(self.res, self.post, self.settings)
        return kb

    def resourses(self):
        kb = InlineKeyboardMarkup(row_width=4)
        data = db.get_resourses("all")
        if data != None:
            sts = {"active": self.st_on, "disactive": self.st_of}
            sts2 = {"active": "Выкл.", "disactive": "Вкл."}
            for i in data:
                kb.row(
                    sts[i['status']],
                    InlineKeyboardButton(i['title'], callback_data="000"),
                    InlineKeyboardButton(sts2[i['status']], callback_data=f"change_{i['uniq_id']}"),
                    InlineKeyboardButton("🗑", callback_data=f"delete_{i['uniq_id']}")
                )
        kb.add(self.add_res)
        kb.add(self.back_Main)
        return kb

    def back_res(self):
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(self.back_Res)
        return kb

    def sett(self):
        kb = InlineKeyboardMarkup(row_width=4)
        with open("./settings.txt", "r") as f:
            dd = f.read()
            timeout = dd.split("_")[0]
            end = dd.split("_")[1]
            threads = dd.split("_")[2]
            f.close()
        endth = {"s": "Сек.", "m": "Мин.", "h": "Ч."}
        kb.add(
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton("⬆️", callback_data="timeout_time_up"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000")
        )
        kb.add(
            InlineKeyboardButton("︎💠", callback_data="000"),
            InlineKeyboardButton(str(timeout), callback_data="000"),
            InlineKeyboardButton(endth[end], callback_data="timeout_time_chend"),
            InlineKeyboardButton("︎💠", callback_data="000")
        )
        kb.add(
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton("⬇️", callback_data="timeout_time_down"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000")
        )
        kb.add(
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton(" ︎ ", callback_data="000"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000")
        )
        kb.add(
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton("⬆️", callback_data="timeout_th_up"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000")
        )
        kb.add(
            InlineKeyboardButton("︎💠", callback_data="000"),
            InlineKeyboardButton(str(threads), callback_data="000"),
            InlineKeyboardButton("︎повторений", callback_data="000"),
            InlineKeyboardButton("︎💠", callback_data="000")
        )
        kb.add(
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton("⬇️", callback_data="timeout_th_down"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000"),
            InlineKeyboardButton("︎ ︎ ", callback_data="000")
        )
        kb.add(self.back_Main)
        return kb

    def posting1(self, **data):
        kb = InlineKeyboardMarkup(row_width=3)
        vals = {"media": "Медиа", "text": "текст", "kb": "кнопки"}
        ignore = ["text", "kb"]
        for k, v in data.items():
            indicator = "🔴"
            if k == "text" and v != "no":
                indicator = "🟢"
            elif k == "kb" and v != "no":
                indicator = "🟢"
            elif k == "media":
                if all((v != "no", str(v) != "[]")):
                    keysa = []
                    for i in v:
                        keysa.extend(i.keys())
                    for item in keysa:
                        if item not in ignore:
                            indicator = "🟢"
            kb.add(
                InlineKeyboardButton(vals[k], callback_data=f"{k}_000"),
                InlineKeyboardButton(indicator, callback_data="000"),
                InlineKeyboardButton("🗑", callback_data=f"delete_{k}")
            )
        kb.add(self.get_saved)
        kb.add(self.pre)
        kb.add(self.back_Main)
        return kb

    def back_post_kb(self):
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(self.back_post)
        return kb

    def send_post(self):
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(self.save, self.change_Ord,self.post_send,self.back_post,self.back_Main)
        return kb
        
    def change_ord(self, order: list):
        kb = InlineKeyboardMarkup(row_width=4)
        nms = {"text":"текст","photo": "фото", "video":"видео","note":"кружок","voice":"гс","audio":"музыка","document":"файл","sticker":"стикер"}
        for i in order:
            kb.add(
                InlineKeyboardButton("💠", callback_data="000"),
                InlineKeyboardButton(nms[i], callback_data="000"),
                InlineKeyboardButton("⬆️", callback_data=f"sett_up_{i}"),
                InlineKeyboardButton("⬇️", callback_data=f"sett_down_{i}")
            )
        kb.add(self.back_pre)
        return kb

    def post_keyb(self, kb_list: list):
        kb = InlineKeyboardMarkup(row_width=1)
        for i in kb_list:
            for k,v in i.items():
                title = k
                url = v
            kb.add(
                InlineKeyboardButton(title, url)
            )
        return kb