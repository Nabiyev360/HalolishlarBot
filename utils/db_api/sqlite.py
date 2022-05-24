import sqlite3
from datetime import datetime


path = 'data/main.db'

def create_table():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS botConfig (
            ann_price VARCHAR(50),
            ann_price_uzs VARCHAR (50),
            tarif1 VARCHAR(100),
            tarif2 VARCHAR(100),
            tarif3 VARCHAR(100),
            price1 VARCHAR(50),
            price2 VARCHAR(50),
            price3 VARCHAR(50),
            price1uzs VARCHAR(50),
            price2uzs VARCHAR(50),
            price3uzs VARCHAR(50),
            qiwi_wallet TEXT,
            uzcard_num TEXT,
            avtopost VARCHAR(50),
            post_interval INTEGER(3)
    )""")
    conn.commit()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER(50),
            full_name VARCHAR(100),
            username VARCHAR(100),
            is_admin VARCHAR(50),
            last_post_date VARCHAR(100),
            joined_date VARCHAR(100),
            joined_month VARCHAR(8),
            joined_year VARCHAR(4)
    )""")
    conn.commit()
    c.execute("""CREATE TABLE IF NOT EXISTS posts (
            ann_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ann_type VARCHAR(50),
            is_checked VARCHAR(100),
            ann_date VARCHAR(20),
            ann_month VARCHAR(8),
            ann_year VARCHAR(4)
    )""")
    conn.commit()
    conn.close()


def add_user(user_id, fullname, username = None):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    if not c.fetchone():
        sql_query = f"INSERT INTO users VALUES (?,?,?,?,?,?,?,?)"
        today = datetime.now()
        new_data = (user_id, fullname, username, None, None, f'{today:%Y-%m-%d}', f'{today:%Y-%m}', f'{today:%Y}')
        c.execute(sql_query, new_data)
        conn.commit()
    conn.close()


def add_admin(user_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    try:
        c.execute(f"SELECT full_name, is_admin FROM users WHERE user_id = '{user_id}'")
        full_name, is_admin = c.fetchone()
        if is_admin == '1':
            c.execute(f"UPDATE users SET is_admin = False WHERE user_id={user_id}")
            conn.commit()
            return f"{full_name} adminlar ro'yxatidan o'chirildi."
        else:
            c.execute(f"UPDATE users SET is_admin = True WHERE user_id={user_id}")
            conn.commit()
            return f"{full_name} admin qilib tayinlandi✅"
    except:
        return f"Admin qilmoqchi bo'lgan odamingiz bot foydalanuvchisi bo'lishi kerak! (Botga kamida 1 ta /start bosgan bo'lishi kerak)"
    conn.close()



def get_admins(data = 'user_id'):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT {data} FROM users WHERE is_admin = True")
    return c.fetchall()



def get_adv_prices():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT tarif1, tarif2, tarif3, price1, price2, price3, price1uzs, price2uzs, price3uzs FROM botConfig")
    return c.fetchone()


def get_one(param_name):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT {param_name} FROM botConfig")
    return c.fetchone()[0]


def update_value(param_name, value):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"UPDATE botConfig SET {param_name} = '{value}'")
    conn.commit()
    conn.close()


def get_users_id():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM users")
    all_ids = c.fetchall()
    return all_ids


def update_interval(user_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT post_interval FROM botConfig")
    interval = c.fetchone()[0]
    today = datetime.now()
    c.execute(f"UPDATE users SET last_post_date = '{today:%Y-%m-%d}' WHERE user_id= {user_id}")
    conn.commit()
    conn.close()


def check_interval(user_id):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"SELECT post_interval FROM botConfig")
    interval = c.fetchone()[0]
    c.execute(f"SELECT last_post_date FROM users WHERE user_id= {user_id}")
    # c.fetchone() None holati uchun alohida yozishga erinib try except qilganman
    try:
        last_date = c.fetchone()[0]
        today = datetime.today()
        differ = today - datetime.strptime(last_date, '%Y-%m-%d')
        differ_days = int(differ.days)
        left_days = str(interval-differ_days)

        if differ_days >= interval:
            return True
        else:
            return interval, left_days
    except:
        return True



# POSTS QUERIES
def add_ann(ann_type, avtopost=None):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    today = datetime.now()
    sql_query = f"INSERT INTO posts VALUES (?,?,?,?,?,?)"
    new_data = (None, ann_type, avtopost, f'{today:%Y-%m-%d}', f'{today:%Y-%m}', f'{today:%Y}')
    c.execute(sql_query, new_data)
    conn.commit()

    c.execute(f"SELECT ann_id FROM posts ORDER BY ann_id DESC")
    ann_id = c.fetchone()[0]
    conn.close()
    return ann_id


def check_ann(ann_id, result):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(f"UPDATE posts SET is_checked = {result} WHERE ann_id = {ann_id}")
    conn.commit()
    conn.close()




def get_stats(time_select= 'all'):
    conn = sqlite3.connect(path)
    c = conn.cursor()

    today = datetime.now()
    this_month = 'today:%Y-%m'
    this_year = 'today:%Y'


    if time_select == 'all':            
        c.execute(f"SELECT COUNT() FROM posts")
        total_anns = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE is_checked = True")
        check_anns = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='vacancy'")
        total_vac = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='vacancy' AND is_checked = True")
        check_vac = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='service'")
        total_ser = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='service' AND is_checked = True")
        check_ser = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='resume'")
        total_res = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='resume' AND is_checked = True")
        check_res = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='adver'")
        total_rek = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='adver' AND is_checked = True")
        check_rek = c.fetchone()[0]
        c.execute("SELECT COUNT() FROM users")
        users_count = c.fetchone()[0]
        
        return total_anns, total_vac, total_ser, total_res, total_rek, check_anns, check_vac, check_ser, check_res, check_rek, users_count


    elif time_select == 'day':            
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_date='{today:%Y-%m-%d}'")
        today_anns = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='vacancy' AND ann_date='{today:%Y-%m-%d}'")
        today_vac = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='service' AND ann_date='{today:%Y-%m-%d}'")
        today_ser = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='resume' AND ann_date='{today:%Y-%m-%d}'")
        today_res = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='adver' AND ann_date='{today:%Y-%m-%d}'")
        today_rek = c.fetchone()[0]

        c.execute(f"SELECT COUNT() FROM posts WHERE is_checked = True AND ann_date='{today:%Y-%m-%d}'")
        check_anns = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='vacancy' AND is_checked = True AND ann_date='{today:%Y-%m-%d}'")
        check_vac = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='service' AND is_checked = True AND ann_date='{today:%Y-%m-%d}'")
        check_ser = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='resume' AND is_checked = True AND ann_date='{today:%Y-%m-%d}'")
        check_res = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='adver' AND is_checked = True AND ann_date='{today:%Y-%m-%d}'")
        check_rek = c.fetchone()[0]

        c.execute(f"SELECT COUNT() FROM users WHERE joined_date='{today:%Y-%m-%d}'")
        users_count = c.fetchone()[0]
        
        return today_anns, today_vac, today_ser, today_res, today_rek, check_anns, check_vac, check_ser, check_res, check_rek, users_count


    elif time_select == 'month':
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_month='{today:%Y-%m}'")
        month_anns = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='vacancy' AND ann_month='{today:%Y-%m}'")
        month_vac = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='service' AND ann_month='{today:%Y-%m}'")
        month_ser = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='resume' AND ann_month='{today:%Y-%m}'")
        month_res = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='adver' AND ann_month='{today:%Y-%m}'")
        month_rek = c.fetchone()[0]

        c.execute(f"SELECT COUNT() FROM posts WHERE is_checked = True AND ann_month='{today:%Y-%m}'")
        check_anns = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='vacancy' AND is_checked = True AND ann_month='{today:%Y-%m}'")
        check_vac = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='service' AND is_checked = True AND ann_month='{today:%Y-%m}'")
        check_ser = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='resume' AND is_checked = True AND ann_month='{today:%Y-%m}'")
        check_res = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='adver' AND is_checked = True AND ann_month='{today:%Y-%m}'")
        check_rek = c.fetchone()[0]

        c.execute(f"SELECT COUNT() FROM users WHERE joined_month='{today:%Y-%m}'")
        users_count = c.fetchone()[0]
        
        return month_anns, month_vac, month_ser, month_res, month_rek, check_anns, check_vac, check_ser, check_res, check_rek, users_count

    elif time_select == 'year':            
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_year='{today:%Y}'")
        year_anns = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='vacancy' AND ann_year='{today:%Y}'")
        year_vac = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='service' AND ann_year='{today:%Y}'")
        year_ser = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='resume' AND ann_year='{today:%Y}'")
        year_res = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='adver' AND ann_year='{today:%Y}'")
        year_rek = c.fetchone()[0]

        c.execute(f"SELECT COUNT() FROM posts WHERE is_checked = True AND ann_year='{today:%Y}'")
        check_anns = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='vacancy' AND is_checked = True AND ann_year='{today:%Y}'")
        check_vac = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='service' AND is_checked = True AND ann_year='{today:%Y}'")
        check_ser = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='resume' AND is_checked = True AND ann_year='{today:%Y}'")
        check_res = c.fetchone()[0]
        c.execute(f"SELECT COUNT() FROM posts WHERE ann_type='adver' AND is_checked = True AND ann_year='{today:%Y}'")
        check_rek = c.fetchone()[0]
        
        c.execute(f"SELECT COUNT() FROM users WHERE joined_year='{today:%Y}'")
        users_count = c.fetchone()[0]

        return year_anns, year_vac, year_ser, year_res, year_rek, check_anns, check_vac, check_ser, check_res, check_rek, users_count