import numpy as np
import matplotlib.pyplot as plt
data = {}
plt.figure(figsize=(9,6))
# Сбор данных ключ-значение из файла

def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def get_data(data):
    with open('crop1.txt') as f:
        for line in f:
            line_list = line.split()
            if line_list and isDigit(line_list[-1]):
                interface = line_list[0]
                address = float(line_list[-1])
                data[interface] = address
get_data(data)
print(data)

T = 168 #неделя-168 (7 дней * 24 часа), год-8760
t=1
step = 1
M = 0
daytime = 1 # 1 -- день, 0 -- ночь
plt.grid()
M_graph=[]
T_graph=[]
I_graph=[]
CO2_graph=[]

for i in range(1, T+1, step): T_graph.append(i)
while t<=T:
    co2_level = data.get('co2_const') + data.get('co2_ampl') * np.sin(np.pi * 2 * t / 24 + np.pi)
    CO2_graph.append(co2_level)
    I_graph.append(data['Int'])
    R = (((data.get('R_max_t')*np.e**(-((data.get('Temp')-data.get('T_opt'))**2)/(2*data.get('sigma_sq_t')))) *
         (data.get('R_max_h')*np.e**(-((data.get('H_const')-data.get('H_soil'))**2)/(2*data.get('sigma_sq_h')))) *
          (data.get('R_max_i')*data.get('Int')/(data.get('k')+data.get('Int'))) *
         (data.get('R_max_co2')*co2_level/(data.get('k_m')+co2_level))) *
         (data.get('R_max_h')*np.e**(-((data.get('H_const')-data.get('H_air'))**2)/(2*data.get('sigma_sq_h')))))
    M = M + R * step
    M_graph.append(M)
    if t%12 == 0: # смена дня и ночи
        if daytime==1:
            data['Int'] = data.get('Int')/2 #ранее 1(день) --> уменьшаем интенсивность
            daytime=0
        else:
            data['Int'] = data.get('Int')*2 #ранее 0(ночь) --> увеличиваем интенсивность
            daytime=1
    t+=step
plt.plot(T_graph,M_graph, label='M')
plt.plot(T_graph,I_graph, label='Int')
plt.plot(T_graph,CO2_graph, label='Co2')
plt.tight_layout()
plt.legend()
plt.show()
