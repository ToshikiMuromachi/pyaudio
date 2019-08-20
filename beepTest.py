import platform
import sys


def beep(freq, dur=100):
    """
        ビープ音を鳴らす.
        @param freq 周波数
        @param dur  継続時間（ms）
    """
    if platform.system() == "Windows":
        # Windowsの場合は、winsoundというPython標準ライブラリを使います.
        import winsound
        winsound.Beep(freq, dur)
    else:
        # Macの場合には、Macに標準インストールされたplayコマンドを使います.
        import os
        os.system('play -n synth %s sin %s' % (dur / 1000, freq))


# 2000Hzで500ms秒鳴らす
beep(2000, 500)
# ド
beep(523, 100)
# レ
beep(587, 100)
# ミ
beep(659, 100)
# ファ
beep(698, 100)
# ソ
beep(784, 100)
# ラ
beep(880, 100)
# シ
beep(932, 100)
# ド
beep(523, 100)

sys.exit()
