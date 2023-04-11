from random import choices
import sqlite3


class data:

    def __init__(self) -> None:
        self.conn = sqlite3.connect("./base/db.db")
        self.cur = self.conn.cursor()

    def get_admin(self, uid):
        data = self.cur.execute("SELECT * FROM users WHERE user_id=:uid", {"uid": uid}).fetchone()
        try:
            res = {"uid": data[0], "status": data[1]}
            return res
        except Exception:
            return None

    def add_admin(self, uid, status):
        self.cur.execute("INSERT INTO users VALUES (:uid, :st)", {"uid": uid, "st": status})
        self.conn.commit()

    def not_adm_exc(self):
        data = self.cur.execute("SELECT * FROM users").fetchall()
        if len(data) == 0:
            return True
        else:
            return False

    def get_resourses(self, status):
        if status == "active":
            data = self.cur.execute("SELECT * FROM resourses WHERE status=:st", {"st": status}).fetchall()
        elif status == "all":
            data = self.cur.execute("SELECT * FROM resourses").fetchall()
        else:
            data = self.cur.execute("SELECT * FROM resourses WHERE status=:st", {"st": status}).fetchall()

        if len(data) == 0:
            return None
        else:
            res = []
            for i in data:
                dd = {"res_id": i[0], "title": i[1], "status": i[2], "uniq_id": i[3]}
                res.append(dd)
            return res

    def update_anu(self, col, data, where):
        req = f"UPDATE resourses SET {col}=:d WHERE {where}"
        self.cur.execute(req, {"d": data})
        self.conn.commit()
        
    def __genstr(self, lenn: int):
        bid = "".join(choices("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890", k=lenn))
        return bid

    def __checkstr(self, genstr: str):
        res = self.cur.execute("SELECT * FROM resourses WHERE uniq=:bb", {"bb": genstr}).fetchone()
        if res:
            return True
        else:
            return False

    def __aller(self, lenn: int=20):
        while True:
            __genstr = self.__genstr(lenn)
            if self.__checkstr(__genstr) == False:
                break
        return __genstr

    def get_channel(self, chId):
        data = self.cur.execute("SELECT * FROM resourses WHERE res_id=:rid", {"rid": chId}).fetchone()
        try:
            res = {"res_id": data[0], "title": data[1], "status": data[2], "uniq_id": data[3]}
            return res
        except Exception:
            return None

    def get_channel_b(self, chId):
        data = self.cur.execute("SELECT * FROM resourses WHERE uniq=:rid", {"rid": chId}).fetchone()
        try:
            res = {"res_id": data[0], "title": data[1], "status": data[2], "uniq_id": data[3]}
            return res
        except Exception:
            return None


    def add_channel(self, chId, title):
        if self.get_channel(chId) == None:
            bid = self.__aller(6)
            self.cur.execute("INSERT INTO resourses VALUES (:rid, :t, :st, :un)", {"rid": chId, "t": title, "st": "disactive", "un": bid})
            self.conn.commit()
            return True
        else:
            return False

    def delete_channel(self, bid):
        self.cur.execute("DELETE FROM resourses WHERE uniq=:rid", {"rid": bid})
        self.conn.commit()

    def sort(self, lst, order):
        order_list = order.split(",")
        kb_list = []
        else_list = []
        text = ""

        for d in lst:
            for k, v in d.items():
                if k == "kb":
                    kb_items = v.split(" - ")
                    if len(kb_items) == 2 and kb_items[1].startswith(("http://", "https://")):
                        kb_list.append({kb_items[0]: kb_items[1]})
                elif k == "text":
                    text += "\n\n"+v
                else:
                    else_list.append({k:v})
        else_list.append({"text": text})

        sorted_lst = sorted(else_list, key=lambda x: order_list.index(list(x.keys())[0]))
        return sorted_lst, kb_list

    def move_element(self, s, element, direction):
        values = s.split(',')
        index = values.index(element)
        if direction == 'down' and index < len(values) - 1:
            new_index = index + 1
        elif direction == 'up' and index > 0:
            new_index = index - 1
        else:
            return s
        values.insert(new_index, values.pop(index))
        return ','.join(values)

    def cut(self, soup, data):
        result = []
        for dictionary in soup:
            key = list(dictionary.keys())[0]
            if key in data:
                result.append(dictionary)
        return result





