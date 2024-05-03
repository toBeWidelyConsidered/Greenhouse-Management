import numpy as np
import matplotlib.pyplot as plt

data = {}


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


# Функции
def gauss_func(x_opt, sigma_sq, x_const):
    return np.e ** (-((x_const - x_opt) ** 2) / (2 * sigma_sq))


def GR_temp():
    return gauss_func(data['T_opt'], data['sigma_sq_t'], data['Temp'])


def GR_H_soil():
    return gauss_func(data['H_soil'], data['sigma_sq_h'], data['H_const'])


def GR_H_air():
    return gauss_func(data['H_air'], data['sigma_sq_h'], data['H_const'])


def GR_Int():
    return data['Int'] / (data['k'] + data['Int']) + alpha


def get_co2_level(t):
    return data.get('co2_const') + data.get('co2_ampl') * np.sin(np.pi * 2 * t / 24 + np.pi)


def get_co2_level2(t, co2_level):
    if t % 72 == 0:  # каждый 3ий день
        return co2_level * 1.75
    elif t % 120 == 0:
        return co2_level * 0.5  # каждый 5 день
    else:
        return co2_level


def get_co2_level3(t, daytime, control):
    if t % 12 == 1 and daytime == 1:
        return data.get('co2_const') + data.get('co2_ampl') * np.sin(np.pi * 2 * t / 24 + np.pi) + control
    elif t % 12 == 11 and daytime == 1:
        return data.get('co2_const') + data.get('co2_ampl') * np.sin(np.pi * 2 * t / 24 + np.pi) - control
    else:
        return data.get('co2_const') + data.get('co2_ampl') * np.sin(np.pi * 2 * t / 24 + np.pi)


def GR_co2(co2_level):
    return co2_level / (data['k_m'] + co2_level)


def get_R(co2_level):
    return data['R_max'] * (GR_temp() * GR_H_soil() * GR_H_air() * GR_Int() * GR_co2(co2_level))


def get_R2(co2_level):
    return data['R_max'] * (GR_temp() + GR_H_soil() + GR_H_air() + GR_Int() + GR_co2(co2_level))


def get_R3(co2_level):
    return data['R_max'] * (GR_temp() * GR_H_soil() * GR_H_air() + GR_Int() * GR_co2(co2_level))


def show_graph():
    plt.figure(figsize=(9, 6))
    plt.subplot(2, 2, 1)
    plt.grid()
    plt.plot(T_graph, M_graph, label='M', color='coral')
    plt.xlabel('Период прогнозирования T, ч', fontsize=10)
    plt.tight_layout()
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.grid()
    plt.plot(T_graph, R_graph, label='R', color='coral')
    plt.xlabel('Период прогнозирования T, ч', fontsize=10)
    plt.tight_layout()
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.grid()
    plt.plot(T_graph, I_graph, label='Int', color='coral')
    plt.xlabel('Период прогнозирования T, ч', fontsize=10)
    plt.tight_layout()
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.grid()
    plt.plot(T_graph, CO2_graph, label='Co2', color='coral')
    plt.xlabel('Период прогнозирования T, ч', fontsize=10)
    plt.tight_layout()
    plt.legend()
    plt.show()


def Time_period():
    print("Введите количество дней прогноза: ", end='')
    T = int(input())
    return T * 24  # неделя-168 (7 дней * 24 часа), год-8760


T = Time_period()
t = 1
step = 1
M = 0
co2_level = data['co2_const']
daytime = 1  # 1 -- день, 0 -- ночь
alpha = 0.01
control = 100

M_graph = []
T_graph = []
I_graph = []
R_graph = []
CO2_graph = []
const_int = data['Int']

for i in range(1, T + 1, step): T_graph.append(i)
while t <= T:
    co2_level = get_co2_level(t)
    CO2_graph.append(co2_level)
    I_graph.append(data['Int'])
    R = get_R(co2_level)
    R_graph.append(R)
    M = M + R * step
    M_graph.append(M)
    if t % 12 == 0:  # смена дня и ночи
        if daytime == 1:
            data['Int'] = 0  # ранее 1(день) --> уменьшаем интенсивность (выключаем свет)
            daytime = 0
        else:
            data['Int'] = const_int  # ранее 0(ночь) --> увеличиваем интенсивность (включаем свет)
            daytime = 1
    t += step
show_graph()
