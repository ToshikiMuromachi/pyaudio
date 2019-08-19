# coding: utf-8

import pyxel, pyaudio
import numpy as np


class App:
    def __init__(self):
        pyxel.init(255, 155, fps=60, scale=2, border_width=10, border_color=0x0d0015, caption='Pyxel & PyAudio')
        self.CHUNK = pyxel.width
        self.RATE = 44100
        self.P = pyaudio.PyAudio()
        self.stream = self.P.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, frames_per_buffer=self.CHUNK,
                                  input=True, output=False)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        # 画面を一度クリアする
        pyxel.cls(1)

        input = self.stream.read(self.CHUNK, exception_on_overflow=False)
        # bufferからndarrayに変換
        ndarray = np.frombuffer(input, dtype='int16')
        # 高速フーリエ変換をして時間領域から周波数領域にする
        f = np.fft.fft(ndarray)
        # 値が大きいので1500で割る
        F = (np.abs(f) / 1500).astype(np.int16)

        for i in range(pyxel.width):
            pyxel.line(i, pyxel.height, i, pyxel.height - F[i], 6)


if __name__ == '__main__':
    App()