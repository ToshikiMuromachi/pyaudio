import subprocess
import sys

# result = subprocess.run('wsl ls -l', shell=True)

message = 'こ　こ　これからもどうぞよろしくお願いします'
path = [
    'wsl echo \'',
    message,
    '\' | ',
    'wsl open_jtalk',
    ' -x /var/lib/mecab/dic/open-jtalk/naist-jdic',
    ' -m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice',
    ' -ow /mnt/c/home/OpenJTalk/test.wav',
    ' -r 1.0',
    ' -a 0.3',
    ' -jf 1.0',
    ' -fm -5.0', ]
path = ''.join(path)
print(path)
result = subprocess.run(path, shell=True)

sys.exit()
