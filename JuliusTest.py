import socket
import threading
import wave
import winsound
import xml.etree.ElementTree as ET
import os
import subprocess
import time
import random

import pyaudio

host = '127.0.0.1'  # localhost
port = 10500  # julisuサーバーモードのポート


def main():
    # p = subprocess.Popen(["./run-win-dnn-module.bat"], stdout=subprocess.PIPE, shell=True) # julius起動スクリプトを実行
    # pid = str(p.stdout.read().decode('utf-8')) # juliusのプロセスIDを取得
    # juliusProcess = subprocess.run("run-win-dnn-module.bat", shell=True)

    time.sleep(3)  # 3秒間スリープ
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))  # サーバーモードで起動したjuliusに接続

    res = ''
    startTime = 0
    nextTime = int(random.uniform(10, 20))
    recentlyWord = ''
    message = ''
    while True:
        startTime += 1
        # 音声認識の区切りである「改行+.」がくるまで待つ
        while (res.find('\n.') == -1):
            # Juliusから取得した値を格納していく
            res += client.recv(1024).decode('shift-jis')

        word = ''
        for line in res.split('\n'):
            # Juliusから取得した値から認識文字列の行を探す
            index = line.find('WORD=')
            # 認識文字列があったら...
            if index != -1:
                # 認識文字列部分だけを抜き取る
                line = line[index + 6: line.find('"', index + 6)]
                # 文字列の開始記号以外を格納していく
                if line != '[s]':
                    word = word + line

            # 認識された文字がある場合
            if len(word) != 0:
                # print("word : "+word)
                recentlyWord = word

            # nextTimeを超過した場合
            if startTime >= nextTime:
                print("音声合成 : " + recentlyWord)
                nextTime = nextTime + int(random.uniform(10, 20))
                message = recentlyWord
                audioStartThread = threading.Thread(target=voice, args=(message,))
                audioStartThread.start()

            res = ''
            # print("TIME : " + str(startTime) + "NEXT -> " + str(nextTime))


def voice(message):
    ms = 'ててふぉふぉふぉふぉふぉて'
    # 音声合成
    path = [
        'wsl echo \'',
        message,
        '\' | ',
        'wsl open_jtalk',
        ' -x /var/lib/mecab/dic/open-jtalk/naist-jdic',
        ' -m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice',
        ' -ow /mnt/c/home/OpenJTalk/voice.wav',
        ' -r 1.0',
        ' -a 0.3',
        ' -jf 1.0',
        ' -fm -5.0', ]
    path = ''.join(path)
    result = subprocess.run(path, shell=True)

    #音声再生
    time.sleep(0.1)
    wf = wave.open('C:\\home\\OpenJTalk\\voice.wav', "r")

    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 音声を再生
    chunk = 1024
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    p.terminate()

    print('かきこみしゅうりょう')


if __name__ == "__main__":
    main()
