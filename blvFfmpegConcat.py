# B站缓存视频合并工具 (需要ffmpeg)
# Sparkle 20190623

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
    with open('entry.json', 'r', encoding='UTF-8') as load_f:
        # loads方法将json格式数据转换为字典（读取文本用此法）
        load_dict = json.load(load_f)
        # print(load_dict)
        if 'ep' in load_dict.keys():
            vtitle += load_dict['ep']['index'].zfill(len(str(len(listDir)))) + load_dict['ep']['index_title']
        else:
            vtitle += str(load_dict['page_data']['page']).zfill(len(str(len(listDir)))) + load_dict['page_data']['part']
        load_f.close()
    # 生成拼接ffmpeg拼接用的txt配置
    ffmpegTXT = ''
    # 这是放 blv 的那个目录 按需修改
    videoPath = ''
    for i in os.listdir('.'):
        if os.path.isdir(i):
            videoPath = i
    if videoPath == '' :
        print("找不到视频目录 告辞")
        os._exit()

    # 循环里面的 blv
    for blv in os.listdir(videoPath):
        # 如果后缀名为 .blv 那就拼进去
        if blv.endswith('.blv'):
            ffmpegTXT += "file '{}/{}'\n".format(videoPath, blv)

    # 如果目录里有想要的文件 把配置存起来用 ffmpeg 合并视频
    if len(ffmpegTXT) > 0:
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