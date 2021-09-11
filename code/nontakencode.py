
"""def playfunc():
    '''[隐藏播放图标] 当点击播放图标时， 隐藏播放图标与按钮
    '''
    # label实现视频容器
    image_cover = Image.open('A://tkinter//code/bg.png')
    image_playcover= ImageTk.PhotoImage(image=image_cover)
    label_video = tk.Label(win_main, width=600, height=400, bd=1, bg='white')
    label_video.place(x=0,y=0)
    string_filepath = filedialog.askopenfilename() # 打开窗口选择目标视频
    btn_play.place_forget() # 隐藏播放按钮
    video_tobeplayed = cv2.VideoCapture(string_filepath) # 打开目标视频
    int_waittime = int(1000/video_tobeplayed.get(5))
    int_movietime = int((video_tobeplayed.get(7)/video_tobeplayed.get(5))/60)
    bar_playscale = tk.Scale(win_main, from_=0, to=int_movietime, length=1000, orient=tk.HORIZONTAL, resolution=0.1, 
        showvalue=1, bd=0, cursor='hand2', tickinterval=int_movietime/20) 
    bar_playscale.place(x=0, y=540)
    while video_tobeplayed.isOpened(): # 当视频正常打开时
        ret, image_frame = video_tobeplayed.read() # 读取视频帧
        if ret == True: # 当成功读取时
            image_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGBA) # 修改颜色空间 
            image_tobeplayed = Image.fromarray(image_frame).resize((540,360)) # 将cv2读取的图像转换为Image,并修改大小
            imageTk_tobeplayed = ImageTk.PhotoImage(image=image_tobeplayed) # 转换为imagetk
            label_video.configure(image=imageTk_tobeplayed) # 使用configure方法将label更新为最新待播放图像
            label_video.image = imageTk_tobeplayed # 更新
            label_video.update() # 更新
            cv2.waitKey(int_waittime)
        else:
            break
"""
