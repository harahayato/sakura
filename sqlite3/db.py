import os
import sqlite3

#DBファイル作成
base_dir = os.path.dirname(__file__)
database = os.path.join(base_dir, 'data.splite')

#SQL
#接続
conn = sqlite3.connect(database)
print('コネクションの接続')
print()
#カーソル
cur = conn.cursor()
#テーブル削除SQL
drop_sql = '''
    DROP TABLE IF EXISTS items;
'''
cur.execute(drop_sql)
print('(|)対象テーブルがあれば削除')
#テーブル作成SQL
create_sql = '''
    CREATE TABLE users (
        user_id STRING UNIQUE NOT NULL,
        user_name STRING NOT NULL,
        user_partner_name STRING NOT NULL
    )
'''
cur.execute(create_sql)
print('(2)テーブル作成')
#データ登録SQL
insert_sql = '''
    INSERT INTO users (user_id, user_name, user_partner_name) VALUES(?, ?, ?)
'''

insert_data_list = [
    ('example@gmail.com', 'はやと', '女の子')
]
cur.executemany(insert_sql, insert_data_list)
conn.commit()
print('(3)データ登録：実行')
#データ参照（全件）SQL
select_all_sql = '''
    SELECT * FROM users
'''
cur.execute(select_all_sql)
print('(4)------------全件取得：実行-------------')
data = cur.fetchall()
print(data)
#データ参照（1件）SQL
select_one_sql = '''
    SELECT * FROM users WHERE user_id = ?
'''
user_id = 'example@gmial.com'
cur.execute(select_one_sql, (user_id,))
print('(5)-------------１件取得：実行--------------')
data= cur.fetchone()
print(data)
#データ更新SQL
update_sql = '''
    UPDATE users SET user_partner_name=? WHERE user_id = ?
'''
user_partner_name = '女の子２'
user_id = 'example@gmail.com'
cur.execute(update_sql, (user_partner_name, user_id))
print('(6)---------------データ更新：実行--------------')
conn.commit()
cur.execute(select_one_sql, (user_id,))
data = cur.fetchone()
print('確認のため１件取得：実行', data)
#データ削除SQL
delete_sql = '''
    DELETE FROM users WHERE user_id = ?
'''
id = 'example@gmail.com'
cur.execute(delete_sql, (user_id,))
conn.commit()
print('(7)-------------データ削除：実行---------------')
cur.execute(select_all_sql)
data = cur.fetchall()
print('確認のため全件取得；実行', data)
#閉じる
conn.close()
print()
print('コネクションを閉じる')