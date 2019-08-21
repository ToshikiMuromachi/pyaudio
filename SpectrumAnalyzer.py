# プロット関係のライブラリ

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys

# 音声関係のライブラリ
import pyaudio
import struct
import winsound

# 制御関連
import random
import platform
import threading
import time
import concurrent.futures

np.set_printoptions(threshold=np.inf)


class PlotWindow:
    def __init__(self):
        # マイクインプット設定
        self.CHUNK = 1024  # 1度に読み取る音声のデータ幅
        self.RATE = 44100  # サンプリング周波数 16000->441000
        self.update_seconds = 50  # 更新時間[ms]
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)

        # 音声データの格納場所(プロットデータ)
        self.data = np.zeros(self.CHUNK)
        self.axis = np.fft.fftfreq(len(self.data), d=1.0 / self.RATE)

        # プロット初期設定
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle("SpectrumAnalyzer")
        self.plt = self.win.addPlot()  # プロットのビジュアル関係
        self.plt.setYRange(0, 1500)  # y軸の制限

        # アップデート時間設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_seconds)  # 10msごとにupdateを呼び出し

        # グラフプロット用
        self.pitches = np.zeros(100)

        # 相槌
        self.conflict = 0
        self.conflictFlag = True

        # 時間設定
        self.time = 0  # 経過時間
        self.conflictTime = random.uniform(20, 25)  # 相槌後経過時間

        # ループ回数(デバック用)
        self.loop = 0

    def update(self):
        self.data = np.append(self.data, self.AudioInput())
        if len(self.data) / 1024 > 10:
            self.data = self.data[1024:]
        self.fft_data = self.FFT_AMP(self.data)
        self.axis = np.fft.fftfreq(len(self.data), d=1.0 / self.RATE)
        self.plotData = self.fft_data  # 配列操作用の変数
        self.plotData[self.plotData < 5.0] = 0.0  # 1より振幅が小さいものは捨てる
        self.plotData[self.plotData > 1500.0] = 0.0  # 1500より振幅が小さいものは捨てる
        # print(np.round(data, 2))
        self.datamax = np.argmax(self.plotData)  # FFTされたものの一番大きいものを取り出す
        # print(data[datamax])
        # print(np.round(self.axis[datamax], 2))

        # ピッチをグラフにプロットするために配列を用意する
        self.pitches = np.roll(self.pitches, -1)  # ピッチを左にずらす
        self.nowPitch = abs(self.axis[self.datamax] * 0.8)  # 最新のピッチ。鏡像現象対策で絶対値で出す。fukuno先輩のコードより0.8かけてあげる
        self.pitches[99] = self.nowPitch
        # print(self.nowPitch)
        # print(self.RATE * 1 * self.pitches[99] / data.size) #ピッチ計算最終結果予定
        # print(self.fft_data.index(max(self.fft_data)))
        self.pitchX = np.linspace(0, 99, 100)
        self.plt.plot(x=self.pitchX, y=self.pitches, clear=True)
        # 音を流す [最新のピッチが5個が0の時、開始経過時間、相槌後経過タイマー、無音区間突入後相槌してるかフラグ(TRUEなら相槌可能)]
        if all(self.pitches[94:99]) == 0 and self.time > 50 and self.conflictTime <= 0 and self.conflictFlag:
            self.conflict = int(sum(self.pitches[79:93]) / 20)  # 直近から20個分のピッチを平均する
            print(self.conflict)
            audioThread1 = threading.Thread(target=self.beep, args=(self.conflict + 37, 200))
            audioThread1.start()
            audioThread2 = threading.Thread(target=self.beep, args=(self.conflict + 87, 200))
            audioThread2.start()
            audioThread3 = threading.Thread(target=self.beep, args=(self.conflict + int(random.uniform(137, 187)), 200))
            audioThread3.start()
            audioThread4 = threading.Thread(target=self.beep, args=(self.conflict + int(random.uniform(137, 187)), 200))
            audioThread4.start()
            self.conflictTime = random.uniform(50, 70)
            self.conflictFlag = False
        if all(self.pitches[94:99]) != 0:
            self.conflictFlag = True    # 音を検出したら相槌可能フラグを立ててあげる
        # self.plt.plot(x=self.axis, y=self.fft_data, clear=True)  # symbol="o", symbolPen="y", symbolBrush="b")
        self.time = self.time + 1  # 時間を更新する
        if self.conflictTime > 0:
            self.conflictTime = int(self.conflictTime - 1)  # 相槌経過後タイマーを更新する
        # print(self.time)
        # print(self.conflictTime)

    def AudioInput(self):
        ret = self.stream.read(self.CHUNK)  # 音声の読み取り(バイナリ) CHUNKが大きいとここで時間かかる
        # バイナリ → 数値(int16)に変換
        # 32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
        ret = np.frombuffer(ret, dtype="int16") / 32768.0
        # print(ret)
        return ret

    def FFT_AMP(self, data):
        data = np.hamming(len(data)) * data
        data = np.fft.fft(data)
        data = np.abs(data)
        return data

    def beep(self, freq, dur=100):
        """
            ビープ音を鳴らす.
            @param freq 周波数
            @param dur  継続時間（ms）
        """
        winsound.Beep(freq, dur)


if __name__ == "__main__":
    plotwin = PlotWindow()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
