#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from tkinter import *
import threading,time,copy,os
#全局变量
lock = threading.Lock() #进程锁
tables = []             #网络上的路由表的集合
table_new = []          #更新后的路由表的集合
                        #通过这两个表的交换赋值来更新
luyou_wrong = '--'      #故障的表的名字（默认一次只能故障一个路由）
#每次更新控件显示的字符串
str_send = ''           #发送了自己路由表的信息
str_update = ''         #更新了自己路由表的信息

def time_now():#用于获得当前时间
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

def main():#主函数
    def add(data,tables):#由用户添加每个路由器的初始路由表
        if tables:
            flag = False
            for i in range(len(tables)):
                if data[0] == tables[i][0]:
                    if [data[1],data[2],data[3]] in tables[i][1]:
                        string = '路由器%s中已有该表项（目标地址：%s,距离：%d，下一跳：%s）' % (data[0],data[1],data[2],data[3])
                    else:
                        tables[i][1].append([data[1],data[2],data[3]])                        
                        string = '向路由器%s添加了表项（目标地址：%s,距离：%d，下一跳：%s）' % (data[0],data[1],data[2],data[3])
                    flag = True
                    break
            if not flag:
                tables.append([data[0],[[data[1],data[2],data[3]]]])
                string = '添加了%s路由器\n向%s路由器添加了表项（目标地址：%s,距离：%d，下一跳：%s）' % (data[0],data[0],data[1],data[2],data[3])
        else:
            tables.append([data[0],[[data[1],data[2],data[3]]]])
            string = '添加了%s路由器\n向%s路由器添加了表项（目标地址：%s,距离：%d，下一跳：%s）' % (data[0],data[0],data[1],data[2],data[3])
        log(string)
        return tables

    def send(table):#向相邻网络发送自己的路由表
        string = table[0] + '向相邻路由发送了自己的路由表 '
        global str_send
        str_send += time_now() + '\n' + string + '\n'


    def update(table,tables,table_new):#更新自己的路由表
        global str_update
        table = copy.deepcopy(table)
        tables = copy.deepcopy(tables)
        #找出相邻的路由，并且得到更新表
        tar = []
        for i in table[1]:
            if i[1]==1:
                tar.append(i[0])                
        tables.remove(table)
        tables_n = copy.deepcopy(tables)
        for each in tables:
            flag = False
            for t in each[1]:
                if t[0] in tar and t[1] == 1:
                    flag = True
                    break
                else:
                    pass
            if not flag:
                tables_n.remove(each)
        #开始更新        
        for each in tables_n:
            str_update += '\n' + time_now() + '\n路由器%s收到了来自%s的更新表\n' % (table[0],each[0])
        table_n = copy.deepcopy(table)
        for each in tables_n:
            n = each[0]
            for tu in each[1]:
                tu[1] += 1
                if tu[1] == 17:
                    tu[1] = 16
                tu[2] = n
                f = False
                for t in table_n[1]:  
                    if t[0] == tu[0]:#如果目标网络相同
                        if t[2] == n:#如果下一跳相同
                            table_n[1][table_n[1].index(t)] = tu
                            str_update += '\n' + time_now() + '\n路由器%s从路由器%s更新了表项:\n（目标地址：%s,距离：%d，下一跳：%s）——>\n（目标地址：%s,距离：%d，下一跳：%s）\n' % (table[0],n,t[0],t[1],t[2],tu[0],tu[1],tu[2])
                        else:#下一跳不同
                            if (tu[1] < t[1] and t[1] != 16) or tu[1] == 16:
                                table_n[1][table_n[1].index(t)] = tu
                                str_update += '\n' + time_now() + '\n路由器%s从路由器%s更新了表项:\n（目标地址：%s,距离：%d，下一跳：%s）——>\n（目标地址：%s,距离：%d，下一跳：%s）\n' % (table[0],n,t[0],t[1],t[2],tu[0],tu[1],tu[2])
                        f = True
                        break
                if not f:
                    table_n[1].append(tu)
                    str_update += '\n' + time_now() + '\n路由器%s从路由器%s添加了新的表项:\n（目标地址：%s,距离：%d，下一跳：%s）\n' % (table[0],n,tu[0],tu[1],tu[2])
        #故障处理
        for i in table_n[1]:
            if i[0] == luyou_wrong and i[1] == 1:
                i[1] = 16
        lock.acquire()
        table_new.append(table_n)
        lock.release()

    def threads(tables,table_new):#多线程发送和更新，做到每一个路由器同时发送和更新(设置接收信息的时间为1s)
        global str_send
        global str_update
        str_send = ''
        str_update = ''
        threadpool_1 = []
        for each in tables:
            th = threading.Thread(target= send, args= (each,))
            threadpool_1.append(th)
        for th in threadpool_1:
            th.start()
        for th in threadpool_1:
            threading.Thread.join(th)
        t2.config(state = NORMAL)
        t2.insert(INSERT,'--------------------------------------------------\n发送情况：\n')
        t2.insert(INSERT,str_send)
        t2.see(END)
        t2.config(state = DISABLED)
        time.sleep(1)
        threadpool_2 = []
        for each in tables:
            th = threading.Thread(target= update, args= (each,tables,table_new))
            threadpool_2.append(th)
        for th in threadpool_2:
            th.start()
        for th in threadpool_2:
            threading.Thread.join(th)
        t2.config(state = NORMAL)
        t2.insert(INSERT,'--------------------------------------------------\n更新情况：\n')
        t2.insert(INSERT,str_update)
        t2.see(END)
        t2.config(state = DISABLED)
        return table_new

    def log(string):#更新日志的函数
        string = time_now() + '\n' + string + '\n'
        t2.config(state = NORMAL)
        t2.insert(INSERT,string)
        t2.see(END)
        t2.config(state = DISABLED)

    def show_add(tables):#用户添加初始路由表时更新路由信息
        string = ''
        string += '--------------------------------------------------\n'
        string += '更新时间：' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())) + '\n'
        for each in tables:
            string += '路由器' + each[0]+':\n'
            for i in range(len(each[1])):
                string += '('+str(i+1) + ')' + ' 目标网络：'+ each[1][i][0] + '  距离：'+ str(each[1][i][1]) + '  下一跳：' + each[1][i][2] + '\n'            
        t1.config(state = NORMAL)
        t1.delete(1.0,END)  
        t1.insert(INSERT,string)
        t1.see(END)
        t1.config(state = DISABLED)

    def show_up(tables):#每次更新路由表时更新路由信息
        string = ''
        string += '--------------------------------------------------\n'
        string += '更新时间：' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())) + '\n'
        for each in tables:
            string += '路由器' + each[0]+':\n'
            for i in range(len(each[1])):
                string += '('+str(i+1) + ')' + ' 目标网络：'+ each[1][i][0] + '  距离：'+ str(each[1][i][1]) + '  下一跳：' + each[1][i][2] + '\n'            
        t1.config(state = NORMAL)
        t1.insert(INSERT,string)
        t1.see(END)
        t1.config(state = DISABLED)

    #控件的callback函数
    def add_callback(tables):#添加按钮
        distance = e_distance.get()
        if distance.isdigit():
            name = e_name.get()
            net_tar = e_net_tar.get() 
            next_ = e_next_.get()
            if name != '' and net_tar != '' and distance != '':
                distance = int(distance)
                if distance>=1 and distance<=16:
                    data = [name,net_tar,distance,next_]
                    tables = add(data,tables)
                    show_add(tables)
                else:
                    messagebox.showinfo('警告','距离应当为1-16的整数!')
            else:
                messagebox.showinfo('警告','路由器名称,目标网络和距离不能为空！')
        else:
            messagebox.showinfo('警告','距离应当为1-16的整数!')

    def update_callback(tables,table_new):#更新按钮
        table_new.clear()
        tables_n = threads(tables,table_new)
        tables.clear()
        tables.extend(tables_n)
        show_up(tables)
        return tables

    def wrong_callback(tables):#故障按钮
        global luyou_wrong
        name_w = e_name_w.get()
        if name_w == '':
            messagebox.showinfo('警告','故障网络名称不能为空！')
        else:
            luyou_wrong = name_w
            messagebox.showinfo('通知','网络%s已设置为故障！' % name_w)
            t2.config(state = NORMAL)
            t2.insert(INSERT, '网络%s故障！' % name_w)
            t2.see(END)
            t2.config(state = DISABLED)

    def save_info_callback():#保存路由信息
        if not t1.get(1.0,END).isspace():
            file = filedialog.asksaveasfilename(defaultextension = '.txt', filetypes = [('txt,TXT','.txt'),('ALL','.*')])
            os.chdir(os.path.dirname(file))
            f = open(os.path.basename(file),'w')
            f.write(t1.get(1.0,END))
            f.close()
            messagebox.showinfo('通知','路由表信息已保存在%s中!' % file)
        else:
            messagebox.showinfo('警告','路由表信息为空!')

    def save_log_callback():#保存日志信息
        if not t2.get(1.0,END).isspace():
            file = filedialog.asksaveasfilename(defaultextension = '.txt', filetypes = [('txt,TXT','.txt'),('ALL','.*')])
            os.chdir(os.path.dirname(file))
            f = open(os.path.basename(file),'w')
            f.write(t2.get(1.0,END))
            f.close()
            messagebox.showinfo('通知','日志信息已保存在%s中!' % file)
        else:
            messagebox.showinfo('警告','路由表信息为空!')

    #GUI界面
    root = Tk()
    root.title('基于距离向量算法的路由协议的实现')
    #左边的输入框
    m_l = PanedWindow(showhandle = True, sashrelief = SUNKEN)
    m_l.pack(fill = BOTH, expand = 1, padx = 10, pady = 10)

    frame_l = LabelFrame(m_l, text = '输入路由信息：', font = 18, padx = 5, pady = 5)
    frame_l.pack(padx = 10, pady = 10)
    Label(frame_l, text = '路由器名称：', font = 16).grid(row = 0, column = 0, sticky = W, pady = 5)
    Label(frame_l, text = '目的网络：', font = 16).grid(row = 1, column = 0, sticky = W, pady = 5)
    Label(frame_l, text = '距离：', font = 16).grid(row = 2, column = 0, sticky = W, pady = 5)
    Label(frame_l, text = '下一跳：', font = 16).grid(row = 3, column = 0, sticky = W, pady = 5)

    e_name = Entry(frame_l, justify = CENTER)
    e_name.grid(row = 0, column = 1)
    e_net_tar = Entry(frame_l, justify = CENTER)
    e_net_tar.grid(row = 1, column = 1)
    e_distance = Entry(frame_l, justify = CENTER)
    e_distance.grid(row = 2, column = 1)
    e_next_ = Entry(frame_l, justify = CENTER)
    e_next_.grid(row = 3, column = 1)
    b_add = Button(frame_l, text = '添加', font = 18, command = lambda : add_callback(tables), padx = 20, pady = 5)
    b_add.grid(row = 4, column = 0, pady = 5)
    b_start = Button(frame_l, text = '更新', font = 18, command = lambda : update_callback(tables,table_new), padx = 20, pady = 5)
    b_start.grid(row = 4, column = 1, pady = 5)

    Label(frame_l, text = '', font = 16).grid(row = 5, column = 0, sticky = W, pady = 5)
    Label(frame_l, text = '模拟网络故障：', font = 18).grid(row = 6, column = 0, sticky = W, pady = 5)
    Label(frame_l, text = '故障网络名称：', font = 16).grid(row = 7, column = 0, sticky = W, pady = 5)
    e_name_w = Entry(frame_l, justify = CENTER)
    e_name_w.grid(row = 7, column = 1)
    b_w = Button(frame_l, text = '故障', font = 18, command = lambda : wrong_callback(tables), padx = 20, pady = 5)
    b_w.grid(row = 8, column = 0, pady = 5, columnspan = 2)

    Label(frame_l, text = '', font = 16).grid(row = 9, column = 0, sticky = W, pady = 5)
    Label(frame_l, text = '保存信息：', font = 18).grid(row = 10, column = 0, sticky = W, pady = 5)
    b_save_info = Button(frame_l, text = '保存路由表', font = 16, command = save_info_callback, padx = 10, pady = 5)
    b_save_info.grid(row = 11, column = 0, pady = 5)
    b_save_log = Button(frame_l, text = '保存日志', font = 16, command = save_log_callback, padx = 10, pady = 5)
    b_save_log.grid(row = 11, column = 1, pady = 5)


    #右边的信息和log
    m_r = PanedWindow(orient = VERTICAL, showhandle = True, sashrelief = SUNKEN)
    frame1 = LabelFrame(m_r, text = '路由表信息：', font = 16, padx = 5, pady = 5)
    frame1.pack(padx = 10, pady = 10)
    sb1 = Scrollbar(frame1)
    sb1.pack(side = RIGHT, fill = Y)
    t1 = Text(frame1, width = 60, height = 20, font = 16, state = DISABLED, yscrollcommand = sb1.set)
    t1.pack(side = LEFT, fill = BOTH)
    sb1.config(command = t1.yview)
    m_r.add(frame1)

    frame2 = LabelFrame(m_r, text = '日志信息：', font = 16, padx = 5, pady = 5)
    frame2.pack(padx = 10, pady = 10)
    sb2 = Scrollbar(frame2)
    sb2.pack(side = RIGHT, fill = Y)
    t2 = Text(frame2, width = 60, height = 15, font = 16, state = DISABLED, yscrollcommand = sb2.set)
    t2.pack(side = LEFT, fill = BOTH)
    sb2.config(command = t2.yview)
    m_r.add(frame2)

    m_l.add(frame_l)
    m_l.add(m_r)
    mainloop()


if __name__=='__main__':
    main()
