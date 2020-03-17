import tkinter as tk
from spider import getarticle
import tkinter.messagebox


window = tk.Tk()    # 创建窗口对象
window.title("百度文库提取器")
# window.update()
scnWidth, scnHeight = window.maxsize()
appWidth1 = scnWidth/6
appHeight1 = scnHeight/6
appWidth2 = scnWidth/3
appHeight2 = scnHeight/1.5
# print(appHeight2)
window.geometry("%dx%d+%d+%d"%(appWidth1, appHeight1, scnWidth/2-appWidth1/2, scnHeight/2-appHeight1/2))   # 设置窗口大小并居中


pagenum = tk.StringVar()    # 将label标签的内容设置为字符类型，将pagenum显示在标签上

readnum = 1                 # 记录当前所在页
mes = []                    # 存放文档内容


def extract():
    global mes
    global readnum
    mes.clear()
    readnum = 1
    link = url.get()
    # print(link)
    window.geometry("%dx%d+%d+%d" % (appWidth2, appHeight2, scnWidth/2-appWidth2/2, scnHeight/2-appHeight2/2))   # 设置窗口大小并居中
    url.pack_forget()
    button.pack_forget()
    article.pack()
    # article.insert('insert', "加载中...")
    mes = getarticle(link)
    totalnum = len(mes)
    article.delete('1.0', 'end')
    article.insert('insert', mes[0])
    page.place(x=int(appWidth2/2-20), y=int(appHeight2*0.92))
    pagenum.set("第1/" + str(totalnum) + "页")
    lastPage.place(x=int(appWidth2/2-100), y=int(appHeight2*0.925))
    nextPage.place(x=int(appWidth2/2+50), y=int(appHeight2*0.925))
    back.place(x=int(appWidth2/2+250), y=int(appHeight2*0.925))


def clear():
    window.geometry("%dx%d+%d+%d"%(appWidth1, appHeight1, scnWidth/2-appWidth1/2, scnHeight/2-appHeight1/2))   # 设置窗口大小并居中
    page.pack_forget()
    lastPage.pack_forget()
    nextPage.pack_forget()
    article.pack_forget()
    url.pack(pady=40)
    button.pack()


def next():
    global readnum
    global mes
    if readnum >= len(mes):
        return
    article.delete('1.0', 'end')
    article.insert('insert', mes[readnum])
    readnum = readnum + 1
    pagenum.set("第" + str(readnum) + "/" + str(len(mes)) + "页")


def last():
    global readnum
    if readnum <= 1:
        return
    article.delete('1.0', 'end')
    article.insert('insert', mes[readnum-2])
    readnum = readnum - 1
    pagenum.set("第" + str(readnum) + "/" + str(len(mes)) + "页")


article = tk.Text(window, width=int(appWidth2/10), height=int(appHeight2/18.5), font=('Arial', 11))

url = tk.Entry(window, width=35, show=None, font=('Arial', 9))   # 地址框

button = tk.Button(window, text='提取文章', font=('Arial', 12), width=10, height=1, command=extract)

page = tk.Label(window, textvariable=pagenum, text='页码', font=('Arial', 10), height=2)

nextPage = tk.Button(window, text='下一页', font=('Arial', 12), width=5, height=1, command=next)
lastPage = tk.Button(window, text='上一页', font=('Arial', 12), width=5, height=1, command=last)

back = tk.Button(window, text='返回', font=('Arial', 12), width=4, height=1, command=clear)

url.pack(pady=40)
button.pack()

tkinter.messagebox.showinfo(title='使用说明', message='将文章地址复制的文本框中，点击提取文章（此版本仅限百度文库中doc、txt文章）\n本软件仅供学习交流请勿用于非法用途，如需下载文档请支持正版')  # 提示信息对话窗


window.mainloop()

