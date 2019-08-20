import subprocess
import sys

#result = subprocess.run('wsl ls -l', shell=True)

result = subprocess.run('wsl echo \'こ　ここんばんは\' | wsl open_jtalk -x /var/lib/mecab/dic/open-jtalk/naist-jdic -m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -r 1.0 -ow /mnt/c/home/OpenJTalk/test.wav -a 0.3 -jf 1.0 -fm -5.0', shell=True)

sys.exit()
