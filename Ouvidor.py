# -*- coding: utf-8 -*-

import librtmp
import subprocess
import os
from threading import Thread
from datetime import datetime
from lib.database import database

def converter(inname,outname):
    cmd = cmd = 'ffmpeg -i %s %s' %(inname,outname)
    comm = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    STDOUT, STDERR = comm.communicate()
    audio_to_text(outname)
    os.remove(inname)

def audio_to_text(outname):
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.WavFile(outname) as source:
        audio = r.record(source)
    try:
        command = r.recognize_google(audio,language='pt_BR')
        if not command.isspace():
            report(now,command.encode('utf-8'))
            log = '%s>>>%s\n' %(now,command.encode('utf-8'))
            report(log)
    except Exception as e:
        print str(e)
    os.remove(outname)

def report(now,phrase):
    db = database().create()
    db.log.insert(date=now[0],time=now[1],phrase=phrase)
    db.commit()

def connection():
    conn = librtmp.RTMP("rtmp://evp.mm.uol.com.br/educadora_cps/_definst_/educadora_cps")
    conn.connect()
    stream = conn.create_stream()
    return stream

total = 0
idname = 0
conn = 0

while 1:
    if conn == 0:
        stream = connection()
        conn = 1

    now = [datetime.now().strftime('%Y/%m/%d'),datetime.now().strftime('%H:%M:%S')]
    inname = 'data/input/%d.flv' % idname
    outname = 'data/output/%d.wav' % idname
    f = open(inname,'ab')
    data = stream.read(1024 * 1024)
    total += len(data)
    f.write(data)

    if total >= 100000:
        conn = 0
        total = 0
        idname += 1
        data = ''
        f.close()
        stream.close()
        t = Thread(target=converter, args=(inname,outname))
        t.start()
