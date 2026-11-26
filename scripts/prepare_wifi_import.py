import hashlib
import json
import math
from pathlib import Path

rows=json.loads(Path('rtk-wifi-original.json').read_text(encoding='utf-8-sig'))
points=[]
seen=set()
for n,row in enumerate(rows,1):
    lat,lon=map(float,row['GPS координаты'].split())
    if not math.isfinite(lat+lon) or not (55<=lat<=61 and 39<=lon<=49):
        raise ValueError('Check coordinates in source row {}'.format(n))
    address=row['Адрес размещения'].strip()
    if not address:
        raise ValueError('Missing address in source row {}'.format(n))
    key=(address,lat,lon)
    if key in seen:
        raise ValueError('Duplicate station in source row {}'.format(n))
    seen.add(key)
    identity=hashlib.sha256((row['Уникальный идентификатор ФИАС']+'|'+address+'|'+str(lat)+'|'+str(lon)).encode()).hexdigest()[:24]
    points.append(dict(id='rtk-'+identity,name='Wi-Fi Ростелеком — '+row['Населенный пункт'].strip(),
                       address=address,latitude=lat,longitude=lon,ssid='',password='',
                       comment='Источник: реестр Ростелекома, предоставлен Депцифры 25.11.2026. '+
                       'Муниципальный округ: '+row['Муниципальный округ']+'. Тип линии: '+row['Тип линии связи']+
                       '. ФИАС: '+row['Уникальный идентификатор ФИАС']+'. SSID и параметры доступа в источнике не указаны.'))
Path('rtk-wifi-import.json').write_text(json.dumps(points,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared {} source points; coordinates and duplicate records checked.'.format(len(points)))
