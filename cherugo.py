"""切噜语（ちぇる語, Language Cheru）转换

定义:
    W_cheru = '切' ^ `CHERU_SET`+
    切噜词均以'切'开头，可用字符集为`CHERU_SET`

    L_cheru = {W_cheru ∪ `\\W`}*
    切噜语由切噜词与标点符号连接而成
"""

import random
import re
from itertools import zip_longest
import os
from pydub import AudioSegment

from hoshino import Service, util,R
from hoshino.typing import CQEvent
import hoshino

sv = Service('pcr-cherugo', bundle='pcr娱乐', help_='''
[切噜一下] 转换为切噜语
[切噜～♪切啰巴切拉切蹦切蹦] 切噜语翻译
'''.strip())

CHERU_SET = '切卟叮咧哔唎啪啰啵嘭噜噼巴拉蹦铃'
CHERU_DIC = {c: i for i, c in enumerate(CHERU_SET)}
ENCODING = 'gb18030'
rex_split = re.compile(r'\b', re.U)
rex_word = re.compile(r'^\w+$', re.U)
rex_cheru_word: re.Pattern = re.compile(rf'切[{CHERU_SET}]+', re.U)
voice_path = os.path.join(os.path.dirname(__file__), '切噜')
save_path = hoshino.config.RES_DIR + r'\record\cherugo.mp3'
voice_dict = {}

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def word2cheru(w: str) -> str:
    c = ['切']
    for b in w.encode(ENCODING):
        c.append(CHERU_SET[b & 0xf])
        c.append(CHERU_SET[(b >> 4) & 0xf])
    return ''.join(c)


def cheru2word(c: str) -> str:
    if not c[0] == '切' or len(c) < 2:
        return c
    b = []
    for b1, b2 in grouper(c[1:], 2, '切'):
        x = CHERU_DIC.get(b2, 0)
        x = x << 4 | CHERU_DIC.get(b1, 0)
        b.append(x)
    return bytes(b).decode(ENCODING, 'replace')


def str2cheru(s: str) -> str:
    c = []
    for w in rex_split.split(s):
        if rex_word.search(w):
            w = word2cheru(w)
        c.append(w)
    return ''.join(c)

def cheru2str(c: str) -> str:
    return rex_cheru_word.sub(lambda w: cheru2word(w.group()), c)

def load_voice():
    global start_cheru
    start_cheru = AudioSegment.from_mp3(os.path.join(os.path.dirname(__file__), '切噜.mp3'))
    start_db = start_cheru.dBFS
    files = os.listdir(voice_path)
    for voice in files:
        voice_length = len(voice[:-4]) 
        inMP3 = AudioSegment.from_mp3(f'{voice_path}/{voice}')
        inMP3_db = inMP3.dBFS
        db = start_db - inMP3_db
        inMP3 += db 
        if voice_length in voice_dict:
            voice_dict[voice_length].append(inMP3)
        else:
            voice_dict[voice_length] = []
            voice_dict[voice_length].append(inMP3)

async def chueru2voice(text):
    if voice_dict == {}:
        load_voice()
    length = len(text)
    result = length
    voice_list = []
    while result > max(voice_dict):
        voice_len = random.choice(list(voice_dict))
        voice_list.append(random.choice(voice_dict[voice_len]))
        result -= voice_len
    else:
        if result in voice_dict:
            voice_list.append(random.choice(voice_dict[result]))
        else:
            voice_list.append(random.choice(voice_dict[random.choice(list(voice_dict))]))
    outmp3 = start_cheru
    for voice in voice_list:
        outmp3 += voice
    outmp3.export(save_path, format="mp3")
    return R.rec("cherugo.mp3").cqcode

@sv.on_prefix('切噜一下')
async def cherulize(bot, ev: CQEvent):
    
    s = ev.message.extract_plain_text()
    if len(s) > 500:
        await bot.send(ev, '切、切噜太长切不动勒切噜噜...', at_sender=True)
        return
    text = '切噜～♪' + str2cheru(s)
    voice = await chueru2voice(text[5:])
    await bot.send(ev, text)
    await bot.send(ev, voice)
    
@sv.on_prefix('切噜～♪')
async def decherulize(bot, ev: CQEvent):
    s = ev.message.extract_plain_text()
    if len(s) > 1501:
        await bot.send(ev, '切、切噜太长切不动勒切噜噜...', at_sender=True)
        return
    msg = '的切噜噜是：\n' + util.filt_message(cheru2str(s))
    await bot.send(ev, msg, at_sender=True)

@sv.on_prefix('切噜语配音')
async def decherulize_voice(bot, ev: CQEvent):
    s = ev.message.extract_plain_text()
    if len(s) > 1501:
        await bot.send(ev, '切、切噜太长切不动勒切噜噜...', at_sender=True)
        return
    text = '切噜～♪' + str2cheru(s)
    voice = await chueru2voice(text[5:])
    msg = '的切噜噜是：\n' + util.filt_message(text)
    await bot.send(ev, msg, at_sender=True)
    await bot.send(ev, voice)
