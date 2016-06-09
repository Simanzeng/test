#!/usr/local/bin/python
# -*- coding:utf-8 -*-

from Tkinter import *
import tkMessageBox

textlen = 8 #输入框长度

class Application(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
	self.pack()
	self.num = '0' #物品数
	self.cap = '0' #背包容量
	self.i = 0     #物品编号
	self.W = []    #物品重量
	self.V = []    #物品价格
	self.createWidgets()
    
    def createWidgets(self):
        #物品数和背包容量
        self.numberLabel = Label(self, text='物品数:').grid(row = 0)
	self.capacityLabel = Label(self, text=' 背包容量:').grid(row = 0, column = 2)
	self.blank = Label(self, text='      ').grid(row = 0, column = 4)
	self.numberInput = Entry(self, width = textlen)
	self.numberInput.grid(row = 0, column = 1)
	self.capacityInput = Entry(self, width = textlen)
	self.capacityInput.grid(row = 0, column = 3)
        self.Button1 = Button(self, text='确认', command = self.numberConfirm).grid(row = 1, column =3)
	
	#列表
	self.Lb1 = Listbox(self, height = 20, width = 30)
	self.Lb1.insert(1, '%15s%15s%15s'%('物品编号','重量','价值'))
	self.Lb1.grid(row = 0,rowspan = 20, column = 5)
	
	#添加物品重量和价格
	self.goodsLabel = Label(self, text = '添加物品  :').grid(row = 3)
	self.weightLabel = Label(self, text = '重量:').grid(row = 4, column = 0)
	self.priceLabel = Label(self, text = '价格:').grid(row = 4, column = 2)
	self.weightInput = Entry(self, width = textlen)
	self.priceInput = Entry(self, width = textlen)
	self.weightInput.grid(row = 4, column = 1)
	self.priceInput.grid(row = 4, column = 3)
	self.Button2 = Button(self, text='添加',command = self.addGoods).grid(row = 5, column = 3)
        
	#最优值和最优解
	self.blank2 = Label(self, text='  ').grid(row = 6)
	self.Button3 = Button(self, text = '计算', command = self.computeSolution).grid(row = 7)
	self.optimalValueLabel = Label(self, text='最优值:').grid(row = 8)
	self.optimalSolutionLabel = Label(self, text='最优解:').grid(row = 9)
	self.optimalValueOutput = Entry(self, width = textlen)
	self.optimalSolutionOutput = Entry(self, width = textlen*3)
        self.optimalValueOutput.grid(row = 8, column = 1)
	self.optimalSolutionOutput.grid(row = 9, columnspan = 3, column = 1)
    
    #物品数和背包容量确认按钮的响应函数
    def numberConfirm(self):
        self.W = []
	self.V = []
	self.i = 0
	self.num = self.numberInput.get() or '0'
	self.cap = self.capacityInput.get() or '0'
	if self.num == '0' or self.cap == '0':
	    tkMessageBox.showinfo('Message', '物品数量或背包容量为0\n      请重新输入！')
	    return 
	tkMessageBox.showinfo('Message', '物品数： %s\n背包容量：%s\n成功' %(self.num, self.cap))
	self.Lb1.delete(1,20)
	self.weightInput.delete(0,textlen)
	self.priceInput.delete(0,textlen)
	self.optimalValueOutput.delete(0,textlen)
	self.optimalSolutionOutput.delete(0,textlen*3)
	if self.num != '0':
	    Label(self, text='添加物品1:').grid(row =3)
    
    #添加物品重量和价格确认按钮的响应函数
    def addGoods(self):
	if self.num == '0' or self.cap == '0':
	    tkMessageBox.showinfo('Message', '物品数量或背包容量为0\n没实际意义，请重新添加！')
	    return
	if self.i == int(self.num):
	    tkMessageBox.showinfo('Message', '已添加完成，无需再添加')
	    return
	w = self.weightInput.get() or '0'
	v = self.priceInput.get() or '0'
	self.W.append(w)
	self.V.append(v)
	tkMessageBox.showinfo('Message', '添加成功')
	self.i = self.i+1
	if self.i == int(self.num):
	    Label(self, text='   完  成   :  ').grid(row = 3)
	    self.update_idletasks()
	    self.Lb1.insert(self.i+1, '%9s%16s%15s'%(str(self.i), w, v))
	else:
	    Label(self, text='添加物品%s:'%str(self.i+1)).grid(row = 3)
	    self.Lb1.insert(self.i+1, '%9s%16s%15s'%(str(self.i), w, v))
	self.weightInput.delete(0,textlen)
	self.priceInput.delete(0,textlen)
    
    #动态规划法求解0-1背包问题	
    def computeSolution(self):
        if self.num == '0' or self.cap == '0':
	    tkMessageBox.showinfo('Message', '物品数量或背包容量为0\n没实际意义，请重新添加！')
            return
	if self.i != int(self.num):
	    tkMessageBox.showinfo('Message', '未完成物品的输入，请继续输入')
	    return
	res = []
	res=[[-1 for j in range(int(self.cap)+1)] for i in range(int(self.num))]
	for j in range(int(self.cap)+1):
	    if j < int(self.W[int(self.num)-1]):
	        res[int(self.num)-1][j] = 0
	    else:
	        res[int(self.num)-1][j] = int(self.V[int(self.num)-1])
	for i in range(1, int(self.num)-1)[::-1]:
	    for j in range(int(self.cap)+1):
	        res[i][j] = res[i+1][j]
		if j >= int(self.W[i]) and res[i+1][j] < res[i+1][j-int(self.W[i])]+int(self.V[i]):
		    res[i][j] = res[i+1][j-int(self.W[i])] + int(self.V[i])
	if int(self.num) > 1: 
	    res[0][int(self.cap)] = res[1][int(self.cap)]
	    if int(self.cap) >= int(self.W[0])\
	    and res[1][int(self.cap)] < res[1][int(self.cap)-int(self.W[0])] + int(self.V[0]):
	        res[0][int(self.cap)] = res[1][int(self.cap)-int(self.W[0])] + int(self.V[0])
	else:
	    if int(self.W[0]) <= int(self.cap):
	        res[0][int(self.cap)] = int(self.V[0])
            else:
	        res[0][int(self.cap)] = 0
	
        #x=[]
	x = [False for i in range(int(self.num))]
	j = int(self.cap)
	for i in range(1, int(self.num)):
	    if res[i-1][j]!=res[i][j]:
	        x[i-1] = True
		j -= int(self.W[i-1])
	x[int(self.num)-1] = 0
	if res[int(self.num)-1][j] > 0:
	    x[int(self.num)-1] = 1
	self.optimalValueOutput.delete(0,textlen)
	self.optimalSolutionOutput.delete(0,textlen*3)
	self.optimalValueOutput.insert(0, str(res[0][int(self.cap)]))
	for i in range(int(self.num)):
	    if x[i]:
	        self.optimalSolutionOutput.insert(i*2, '1  ')
	    else:
	        self.optimalSolutionOutput.insert(i*2, '0  ')


app = Application()
app.master.title('动态规划法算法求0-1背包问题')
app.mainloop()
