from datetime import timedelta, datetime
from tqdm import tqdm
import pytz
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')
g = config.get
from ossapi import *
api = OssapiV2(g('api', 'clientid'), g('api', 'clientsec'))
utc = pytz.UTC
# Definir la api y poner al primer jugador.
# Also, abrir el archivo donde irán los jugadores
api = OssapiV2(g('api', 'clientid'), g('api', 'clientsec'))
c = input("Elige hasta el top del que quieres el nombre \n")
b = 0
if g('method', 'country') == "":
    r = api.ranking("g('method','gamemode')", RankingType.PERFORMANCE)
else:
    r = api.ranking(g('method','gamemode'), RankingType.PERFORMANCE,country=g('method', 'country') )
cursor = r.cursor
players = []
f = open(f"{g('filenames', 'playersoutput')}.txt", "w")
# loop infinito
while 1 == 1:
    i = 0
    d = int(b)/50
    if b < 50:
        if g('method', 'country') == "":
            r = api.ranking(g('method','gamemode'), RankingType.PERFORMANCE)
        else:
            r = api.ranking(g('method','gamemode'), RankingType.PERFORMANCE ,country=g('method', 'country'))
    else:
        if g('method', 'country') == "":
            r = api.ranking(g('method','gamemode'), RankingType.PERFORMANCE, cursor=r.cursor)
        else:
            r = api.ranking(g('method','gamemode'), RankingType.PERFORMANCE,country=g('method', 'country'), cursor=r.cursor)
    while i <= 49:      
        players.append(r.ranking[i].user.id)
        i += 1
        b += 1
        if b-int(c) == 0:
            break
    if b-int(c) == 0:
        break
#output en un archivo con newlines
for item in players:
    f.write("%s\n" % item)
print("Done getting players. Now loading plays.")
# tuve que poner las dos partes en el mismo archivo porque cosas.
# f = archivo con las ids ; o = archivo a donde se envian las plays ; i = contador con overflow en 5
# s = contador de veces de overflow en i, hasta 20 ; a = contador absoluto 
a = 0
d = a/100
done = False
f = open(f"{g('filenames', 'playersoutput')}.txt", "r")
lc = 0
for line in f:
    if line != "\n":
        lc += 1
f.close()
f = open(f"{g('filenames', 'playersoutput')}.txt", "r")
o = open(f"{g('filenames', 'playsoutput')}.txt", "w")
ma = utc.localize(datetime.now()) - timedelta(days=30)
plays = []
for x in tqdm(range(a,lc)):
    i = 0
    s = 0
    ids = f.readline()
    if ids != "":
        b = api.user_scores(ids, "best", False, g('method','gamemode'), 1200, s)[i]
    i = 0
    s = 0
    while 1==1:
        if i >= 50 and s == 0:
            s = 49
            i = 0
        elif s == 49 and i == 50:
            s = 0
            a =+ 1
            break
        while i <= 49:
            b = api.user_scores(ids, "best", False, g('method','gamemode'),1200,s)[i]
            if b.created_at >= ma:
                plays.append(f"Jugado por {b.user.username}, en el {b.created_at}, {b.pp}pp. https://osu.ppy.sh/scores/osu/{b.best_id}") 
            else: pass
            a += 1
            i += 1    
for item in plays:
    o.write("%s\n" % item)
print("Done!")

