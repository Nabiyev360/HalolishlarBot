import sqlite3


path = 'data/main.db'

def create_table():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS botConfig (
            ann_price VARCHAR(50),
            tarif1 VARCHAR(100),
            tarif2 VARCHAR(100),
            tarif3 VARCHAR(100),
            price1 VARCHAR(50),
            price2 VARCHAR(50),
            price3 VARCHAR(50),
            qiwi_wallet TEXT,
            uzcard_num TEXT,
            avtopost VARCHAR(50),
            post_interval INTEGER(3)
    )""")


def get_adv_prices():
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT tarif1, tarif2, tarif3, price1, price2, price3 FROM botConfig")
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
