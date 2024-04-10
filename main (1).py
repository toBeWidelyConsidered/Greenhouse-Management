import numpy as np
import matplotlib.pyplot as plt
data = {}
plt.figure(figsize=(9,6))
# Сбор данных ключ-значение из файла
def get_data(data):
    with open('crop1.txt') as f:
        for line in f:
            line_list = line.split()
            if line_list and line_list[-1].isdigit():
                interface = line_list[0]
                address = int(line_list[-1])
                data[interface] = address
get_data(data)
print(data)
"""
def gauss_func(x_opt, sigma_sq, r_max):
    x = np.linspace(0, x_opt*2, 100)
    plt.xlim([0, x_opt*2])
    plt.tight_layout()
    plt.plot(x, r_max*np.e**(-((x-x_opt)**2)/(2*sigma_sq)), color='coral')
def log_func(k, r_max):
    x = np.linspace(0, 50, 100)
    plt.ylim([0, r_max+10])
    plt.tight_layout()
    plt.plot(x, r_max*x/(k+x),color='coral')
def GR_temp():
    plt.subplot(2, 2, 1)
    plt.grid()
    plt.title('Рост растений в зависимости от температуры', fontsize=10)
    plt.xlabel('Температура', fontsize=10)
    plt.ylabel('Рост', fontsize=10)
    gauss_func(data.get('T_opt'),data.get('sigma_sq_t'),data.get('R_max_t'))
def GR_hum():
    plt.subplot(2, 2, 2)
    plt.grid()
    plt.title('Рост растений в зависимости от влажности', fontsize=10)
    plt.xlabel('Влажность', fontsize=10)
    plt.ylabel('Рост', fontsize=10)
    gauss_func(data.get('H_opt'),data.get('sigma_sq_h'),data.get('R_max_h'))
def GR_intens():
    plt.subplot(2, 2, 3)
    plt.grid()
    plt.title('Рост растений в зависимости от интенсивности света', fontsize=10)
    plt.xlabel('Интенсивность', fontsize=10)
    plt.ylabel('Рост', fontsize=10)
    log_func(data.get('k'),data.get('R_max_i'))
    #plt.axhline(y=data.get('R_max_i'), color ="maroon", linestyle ="--")
def GR_co2():
    plt.subplot(2, 2, 4)
    plt.grid()
    plt.title('Рост растений в зависимости от концентрации $Co_2$', fontsize=10)
    plt.xlabel('Концентрация $Co_2$', fontsize=10)
    plt.ylabel('Рост', fontsize=10)
    log_func('k_m','R_max_co2')
GR_temp()
GR_hum()
GR_intens()
GR_co2()"""
#plt.show()
T = 50 #период дней и ночей
t0=0
t=1
count = 0
daytime = 1 # 1 -- день, 0 -- ночь
plt.grid()
M_graph=[]
T_graph=[]
for i in range(T): T_graph.append(i)
while t<=T:
    koef = -1
    R = ((data.get('R_max_t')*np.e**(-((data.get('Temp')-data.get('T_opt'))**2)/(2*data.get('sigma_sq_t')))) *
         (data.get('R_max_h')*np.e**(-((data.get('Temp')-data.get('H_opt'))**2)/(2*data.get('sigma_sq_h')))) *
          (data.get('R_max_i')*data.get('Int')/(data.get('k')+data.get('Int'))) *
         (data.get('R_max_co2')*data.get('Int')/(data.get('k_m')+data.get('co2'))))
    M = R + R * (t-t0)
    M_graph.append(M)
    data['H_opt'] *= (1-0.01*(t-t0))
    data['co2'] = data.get('co2') + koef * data.get('co2') * 0.05
    if count%5 == 0: # смена дня и ночи   5ночь 10день 15ночь 20день
        if daytime==1: data['Int'] = data.get('Int')/2 #ранее 1(день) --> уменьшаем интенсивность
        else: data['Int'] = data.get('Int')*2 #ранее 0(ночь) --> увеличиваем интенсивность
        if count%2==0: daytime=0
        else: daytime=1
        koef *= -1
    count += 1
    t0=t
    t+=1
plt.plot(T_graph,M_graph)
plt.show()
