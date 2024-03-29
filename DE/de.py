import numpy as np
import matplotlib.pyplot as plt
import random

class de :

    # 変数宣言
    cr = 0.9 # DEのパラメータ
    fw = 0.5 # DEのパラメータ
    tmax = 1000 # 最大繰り返し回数
    fend = 1e-5 # 終了条件
    xmin = -5 # 乱数生成の範囲(下限)
    xmax = 5 # 乱数生成の範囲(上限)

    # 初期化
    def __init__(self, m, d, func='sphere') :
        self.m = m # 個体数
        self.d = d # 解の次元
        self.func = func # 目的関数の設定
        self.x = (self.xmax - self.xmin) * np.random.rand(m,d) + self.xmin # M個*D次元の配列(位置)
        self.xnew = np.zeros((m,d)) # M個*D次元の配列(新しい位置)
        self.v = np.zeros(d) # D次元の配列(速度)
        self.u = np.zeros(d) # D次元の配列(解候補)
        self.f = np.zeros(m) # 評価関数値
        self.ftmp = 0 # 評価関数値(一時的)
        self.fbest = float('inf') # 最も良い評価関数値
        self.xbest = np.full(d, float('inf')) # 最も良い位置(次元の数だけ存在する)

        # 初期値によるFの計算
        if self.func == 'sphere' :
            self.sphere_f()
        elif self.func == 'rastrigin' :
            self.rastrigin_f()

    def sphere_u(self, xu) :
        f = 0
        for d in range(self.d) :
            xd = xu[d]
            f += xd**2
        return f

    def sphere_f(self) :
        for i in range(self.m) :
            xd = 0
            for j in range(self.d) :
                xd += self.x[i][j]**2
            self.f[i] = xd

    def rastrigin_u(self,xu) :
        f = 0
        for d in range(self.d) :
            xd = ((xu[d]**2) - 10*np.cos(2*np.pi*xu[d]) + 10)
            f += xd
        return f

    def rastrigin_f(self) :
        for i in range(self.m) :
            xd = 0
            for j in range(self.d) :
                xd += ((self.x[i][j]**2) - 10*np.cos(2*np.pi*self.x[i][j]) + 10)
            self.f[i] = xd


    def calc(self) :
        each_fg = [] # 実験用
        for self.stopt in range(1, self.tmax+1) :
            for i in range(self.m) :
                rabc = np.hstack((np.arange(0,i),np.arange(i+1,self.m)))
                a, b, c = np.random.choice(rabc,3,replace=False)
                #for j in range(self.d) :
                self.v = self.x[a] + self.fw*(self.x[b] - self.x[c])

                jr = np.random.randint(0,self.d,1)
                for j in range(self.d) :
                    ri = np.random.rand()
                    if ri < self.cr or j == jr :
                        self.u[j] = self.v[j]
                    else :
                        self.u[j] = self.x[i][j]
                
                # 目的関数
                if self.func == 'sphere' :
                    self.ftmp = self.sphere_u(self.u) # Uの評価関数Ftmpの計算
                elif self.func == 'rastrigin' :
                    self.ftmp = self.rastrigin_u(self.u) # Uの評価関数Ftmpの計算
                
                if self.ftmp < self.f[i] :
                    self.f[i] = self.ftmp
                    self.xnew[i] = self.u
                    if self.ftmp < self.fbest :
                        self.fbest = self.ftmp
                        self.xbest = self.x[i]
                else :
                    self.xnew[i] = self.x[i]
            
            each_fg.append(self.fbest)
            self.x = self.xnew
            if self.fbest < self.fend :
                break
        return each_fg

if __name__ == '__main__' :
    de1 = de(30,5)
    de1.calc()
    print("終了時刻t = " + str(de1.stopt))
    print("解の目的関数値Fg = ", end="")
    print(de1.fbest)