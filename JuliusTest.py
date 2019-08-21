import socket
import xml.etree.ElementTree as ET
import os
import subprocess
import time

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
    while True:
        # 音声認識の区切りである「改行+.」がくるまで待つ
        print("にんしきちゅう")
        while (res.find('\n.') == -1):
            # Juliusから取得した値を格納していく
            res += client.recv(1024).decode('shift-jis')
            #print("ニンシキ  :  " + res)

        word = ''
        for line in res.split('\n'):
            # Juliusから取得した値から認識文字列の行を探す
            index = line.find('WORD=')
            print('OK')
            # 認識文字列があったら...
            if index != -1:
                # 認識文字列部分だけを抜き取る
                line = line[index + 6: line.find('"', index + 6)]
                # 文字列の開始記号以外を格納していく
                if line != '[s]':
                    word = word + line

            # 「かめら」という文字列を認識したら...
            if word == 'かめら':
                print("かめら！！")
            print("word : "+word)
            res = ''


if __name__ == "__main__":
    main()
