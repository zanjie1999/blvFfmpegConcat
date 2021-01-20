# B站缓存视频合并工具 (需要ffmpeg)
# Sparkle 20190623
# v3

import os
import json

videoPath = '.'
ffmpegPath = 'ffmpeg'

listDir = os.listdir(videoPath)
os.chdir(videoPath)
#循环当前目录下的文件夹
for i in listDir:
    if not os.path.isdir(i):
        continue
    
    #进去
    print(i)
    os.chdir(i)
    #定义拼接完成后视频的标题
    vtitle = '../'
    jsonName = 'entry.json'
    isUWP = False
    if 'info.json' in os.listdir('.'):
        jsonName = 'info.json'
        isUWP = True
    with open(jsonName, 'r', encoding='UTF-8') as load_f:
        # loads方法将json格式数据转换为字典（读取文本用此法）
        load_dict = json.load(load_f)
        # print(load_dict)
        if 'ep' in load_dict.keys():
            vtitle += load_dict['ep']['index'].zfill(len(str(len(listDir))))
            vtitle += load_dict['ep']['index_title']
        elif 'page_data' in load_dict.keys():
            vtitle += str(load_dict['page_data']['page']).zfill(len(str(len(listDir))))
            vtitle += load_dict['page_data']['part']
        elif isUWP:
            vtitle += str(load_dict['index']).zfill(len(str(len(listDir))))
            vtitle += load_dict['title']
        else:
            print("找不到json 告辞")
            os._exit()
        load_f.close()
    # 生成拼接ffmpeg拼接用的txt配置
    ffmpegTXT = ''
    # 这是放 blv 的那个目录 按需修改
    videoPath = '.'
    # 新版本采用m4s保存
    isM4s = False
    # 上古视频是flv
    isFlv = False
    for i in os.listdir('.'):
        if os.path.isdir(i):
            videoPath = i
    if videoPath == '.' and not isUWP:
        print("找不到视频目录 告辞")
        os._exit()

    videoPathFile = os.listdir(videoPath)
    videoPathFile.sort(key=lambda x: x.split('.')[0])

    # 循环里面的 blv
    for f in videoPathFile:
        # 如果后缀名为 .blv 那就拼进去
        if f.endswith('.blv'):
            ffmpegTXT += "file '{}/{}'\n".format(videoPath, f)
        elif f.endswith('.m4s'):
            isM4s = True
            break
        elif f.endswith('.flv'):
            isFlv = True
            break

    # 如果目录里有想要的文件 把配置存起来用 ffmpeg 合并视频
    if isFlv:
        cmd = '{} -i {}/000.flv -c copy "{}.mp4"'.format(ffmpegPath, videoPath, vtitle.replace('"', '\\"'))
        print(cmd)
        os.system(cmd)
    elif isM4s:
        cmd = '{} -i {}/video.m4s -i {}/audio.m4s -c copy "{}.mp4"'.format(ffmpegPath, videoPath, videoPath, vtitle.replace('"', '\\"'))
        print(cmd)
        os.system(cmd)
    elif len(ffmpegTXT) > 0:
        with open('ff.txt', 'w', encoding='UTF-8') as f:
            f.write(ffmpegTXT)
            f.close()
            # ffmpeg 拼接视频的命令
            cmd = '{} -f concat -i ff.txt -c copy "{}.mp4"'.format(ffmpegPath, vtitle.replace('"', '\\"'))
            # python调用Shell脚本执行命令
            print(cmd)
            os.system(cmd)
            os.remove('ff.txt')
    #搞完了回到上一级目录
    os.chdir('..')