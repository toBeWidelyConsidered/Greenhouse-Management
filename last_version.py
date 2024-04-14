import numpy as np
import matplotlib.pyplot as plt

data = {}
plt.figure(figsize=(9, 6))


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
def gauss_func(x_opt, sigma_sq, r_max, x_const):
    return r_max * np.e ** (-((x_const - x_opt) ** 2) / (2 * sigma_sq))


def GR_temp():
    return gauss_func(data['T_opt'], data['sigma_sq_t'], data['R_max_t'], data['Temp'])


def GR_H_soil():
    return gauss_func(data['H_soil'], data['sigma_sq_h'], data['R_max_h'], data['H_const'])


def GR_H_air():
    return gauss_func(data['H_air'], data['sigma_sq_h'], data['R_max_h'], data['H_const'])


def GR_Int():
    return data['R_max_i'] * data['Int'] / (data['k'] + data['Int'])


def GR_co2(co2_level):
    return data['R_max_co2'] * co2_level / (data['k_m'] + co2_level)


def show_graph():
    plt.grid()
    plt.plot(T_graph, M_graph, label='M')
    plt.plot(T_graph, I_graph, label='Int')
    plt.plot(T_graph, CO2_graph, label='Co2')
    plt.xlabel('Период прогнозирования T, сек', fontsize=10)
    plt.tight_layout()
    plt.legend()
    plt.show()


def Time_period():
    print("Введите количество дней прогноза:")
    T = int(input())
    return T * 24  # неделя-168 (7 дней * 24 часа), год-8760


T = Time_period()
t = 1
step = 1
M = 0
daytime = 1  # 1 -- день, 0 -- ночь

M_graph = []
T_graph = []
I_graph = []
CO2_graph = []

for i in range(1, T + 1, step): T_graph.append(i)
while t <= T:
    co2_level = data.get('co2_const') + data.get('co2_ampl') * np.sin(np.pi * 2 * t / 24 + np.pi)
    CO2_graph.append(co2_level)
    I_graph.append(data['Int'])
    R = GR_temp() * GR_H_soil() * GR_H_air() * GR_Int() * GR_co2(co2_level)
    M = M + R * step
    M_graph.append(M)
    if t % 12 == 0:  # смена дня и ночи
        if daytime == 1:
            data['Int'] /= 2  # ранее 1(день) --> уменьшаем интенсивность
            daytime = 0
        else:
            data['Int'] *= 2  # ранее 0(ночь) --> увеличиваем интенсивность
            daytime = 1
    t += step
show_graph()
