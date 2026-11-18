#!/usr/bin/env python3
"""Generate an Apple Calendar-compatible holiday subscription feed."""
import json
import urllib.request
from datetime import date, timedelta
from pathlib import Path

START_YEAR, END_YEAR = 2026, 2035
OUT = Path(__file__).parent / 'holidays.ics'
SOURCE = 'https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/{year}.json'

def easter(year):
    a=year%19;b=year//100;c=year%100;d=b//4;e=b%4;f=(b+8)//25;g=(b-f+1)//3
    h=(19*a+b-d-g+15)%30;i=c//4;k=c%4;l=(32+2*e+2*i-h-k)%7;m=(a+11*h+22*l)//451
    month=(h+l-7*m+114)//31;day=(h+l-7*m+114)%31+1
    return date(year,month,day)

def nth_weekday(y,m,weekday,n):
    first=date(y,m,1)
    return first+timedelta(days=(weekday-first.weekday())%7+7*(n-1))

def last_weekday(y,m,weekday):
    next_month=date(y+1,1,1) if m==12 else date(y,m+1,1)
    last=next_month-timedelta(days=1)
    return last-timedelta(days=(last.weekday()-weekday)%7)

def international(y):
    return [
        (date(y,2,14),'情人节 · Valentine’s Day'),
        (easter(y),'复活节 · Easter Sunday'),
        (nth_weekday(y,5,6,2),'母亲节 · Mother’s Day'),
        (nth_weekday(y,6,6,3),'父亲节 · Father’s Day'),
        (date(y,10,31),'万圣节 · Halloween'),
        (nth_weekday(y,11,3,4),'感恩节 · Thanksgiving (US)'),
        (date(y,12,24),'平安夜 · Christmas Eve'),
        (date(y,12,25),'圣诞节 · Christmas Day'),
    ]

def chinese(y):
    try:
        req=urllib.request.Request(SOURCE.format(year=y),headers={'User-Agent':'holiday-calendar-generator/1.0'})
        with urllib.request.urlopen(req,timeout=15) as response:
            data=json.load(response)
        days=data.get('days',[])
        result=[]
        for item in days:
            if not isinstance(item.get('isOffDay'),bool): continue
            d=date.fromisoformat(item['date'])
            if d.year!=y:continue
            prefix='休' if item['isOffDay'] else '班'
            name=item.get('name') or '法定节假日调整'
            result.append((d,f'{prefix}｜{name}'))
        print(f'{y}: {len(result)} official holiday/adjustment records')
        return result
    except Exception as exc:
        print(f'{y}: no verified China holiday data available ({exc})')
        return []

def escape(s):
    return str(s).replace('\\','\\\\').replace(';','\\;').replace(',','\\,').replace('\n','\\n')

def fold(line):
    # RFC 5545 folding at 75 octets; don't split UTF-8 characters
    chunks=[];current='';length=0
    for char in line:
        n=len(char.encode('utf-8'))
        if length+n>75:
            chunks.append(current);current=' ';length=1
        current+=char;length+=n
    chunks.append(current)
    return '\r\n'.join(chunks)

def main():
    records={}
    for year in range(START_YEAR,END_YEAR+1):
        for d,name in international(year):records[(d,'global',name)]=None
        for d,name in chinese(year):records[(d,'china',name)]=None
    lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Holiday Calendar//CN and International//ZH','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:Holidays｜节假日','X-WR-TIMEZONE:Asia/Shanghai','REFRESH-INTERVAL;VALUE=DURATION:P1D','X-PUBLISHED-TTL:PT24H']
    for d,kind,name in sorted(records):
        # stable deterministic UID independent of Python hash randomization
        import hashlib
        uid=f'{d:%Y%m%d}-{kind}-{hashlib.sha256(name.encode()).hexdigest()[:16]}@holiday-calendar'
        lines.extend(['BEGIN:VEVENT',f'UID:{uid}','DTSTAMP:20260101T000000Z',f'DTSTART;VALUE=DATE:{d:%Y%m%d}',f'DTEND;VALUE=DATE:{d+timedelta(days=1):%Y%m%d}',f'SUMMARY:{escape(name)}','TRANSP:TRANSPARENT','END:VEVENT'])
    lines.append('END:VCALENDAR')
    OUT.write_bytes(('\r\n'.join(fold(line) for line in lines)+'\r\n').encode('utf-8'))
    print(f'Wrote {OUT} ({len(records)} events)')

if __name__=='__main__':main()
