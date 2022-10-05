#Moduleのインポート
import glob
import cv2
import numpy as np
import os
import shutil
import datetime

#定数指定
width = 868
height = 1212
input = 'input'
artifact = 'artifact'
output = 'output'
i = 1

#関数作成
def listup_files(path):
    yield [os.path.abspath(p) for p in glob.glob(path)]
def get_now():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    return now.strftime('%Y%m%d%H%M')

#中間ファイル作成(cv2が日本語名を含むファイルを読み込めないため)
for filename in os.listdir(input):
    if filename.endswith('.jpg'):
        shutil.copyfile(input + '\\' + filename, artifact  + '\\' + str(i) + '.jpg')
        i += 1

#artifactフォルダ内のJPGファイルを取得する。
files = glob.glob(os.path.abspath(artifact) + '\\*.jpg')
files.sort()

#タイル状に60枚のポケモンカードを連結する。
img = cv2.imread(files[0])
height, width, channels = img.shape
tile = np.zeros((height * 6, width * 10, channels), dtype = np.uint8)
for i in range(6):
    for j in range(10):
        index = i * 10 + j
        tile[i * height:(i + 1) * height, j * width:(j + 1) * width] = cv2.resize(cv2.imread(files[index]), dsize=(width,height))

#8K規格に収まるサイズに縮尺し、動画化する。
result = cv2.resize(tile,dsize=(5156,4320))
out = cv2.VideoWriter(output + '\\deck_' +str(get_now()) + '.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 1.0, (result.shape[1],result.shape[0]),True)
out.write(result)
out.release()
