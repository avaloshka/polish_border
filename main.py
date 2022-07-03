# This is working parsing for polish/belarusian border crossings
import sqlite3
import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
url = 'https://granica.gov.pl/index_wait.php?p=b&v=pl&k=w'
response = requests.get(url, headers=headers)
soup = bs(response.content, 'html.parser')
table = soup.find('table')
# print(table)

rows = soup.find_all('tr')[3:]
kuznica = ['Kuznica']
bobrowniki = ['Bobrowniki']
polowce = ['Polowce']
koroszczyn = ['Koroszczyn (Kukuryki)']
terespol = ['Terespol']
slawatycze = ['Slawatycze']

for row in rows:
    try:
        # Get timings
        kuz = row.findAll('td')[2].text.strip()
        bobr = row.findAll('td')[3].text.strip()
        pol = row.findAll('td')[4].text.strip()
        kor = row.findAll('td')[5].text.strip()
        ter = row.findAll('td')[6].text.strip()
        sla = row.findAll('td')[7].text.strip()
        if kuz == '':
            kuz = '-'
        if bobr == '':
            bobr = '-'
        if pol == '':
            pol = '-'
        if kor == '':
            kor = '-'
        if ter == '':
            ter = '-'
        if sla == '':
            sla = '-'
    except:
        # simple index out of range on iteration 7, but I don't care. I don't need iteration 7
        pass

    kuznica.append(kuz)
    bobrowniki.append(bobr)
    polowce.append(pol)
    koroszczyn.append(kor)
    terespol.append(ter)
    slawatycze.append(sla)


# Agregate all data to list
data = [kuznica, bobrowniki, polowce, koroszczyn, terespol, slawatycze]
# show only 4 rows in any column
data = [item[:4] for item in data]

# CREATE DB AND TABLE

conn = sqlite3.connect('polish.db')
cursor = conn.cursor()

# CREATE DB and TABLE
try:
    cursor.execute("""CREATE TABLE polish
                     ([Пункт] TEXT,
                     [Грузовики] TEXT,
                     [Автобусы] TEXT,
                     [Машины] TEXT)
                     """)
    conn.commit()
except:
    pass

# CLEAN PREVIOUS RECORD SO WE CAN INSERT NEW DATA
cursor.execute(
    "DELETE FROM polish"
)
conn.commit()


# INSERT INTO DB
for item in data:
    cursor.execute(
        '''
        INSERT INTO polish(Пункт, Грузовики, Автобусы, Машины)
        VALUES(?, ?, ?, ?)
        ''',
        item
    )
    conn.commit()

# Print DB
print('Printing Database...')
cursor.execute(
    """
    SELECT * FROM polish
    """
)
print(cursor.fetchall())
data_list = cursor.fetchall()
conn.commit()


# Print DB with pandas
import pandas as pd
df = pd.read_sql_query("SELECT * FROM polish", conn)
print(df)