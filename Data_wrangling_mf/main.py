import os, sys, time
import numpy as np
import csv
from pathlib import Path

# path_to_py - путь к исполняемому файлу *.py без имени файла. Например: C:\Hatzker\Project
path_to_executable_file = os.path.abspath(os.path.dirname(sys.argv[0]))
# paths_to_mf_file - список путей к *.mf файлам с именем файла,
# хранящихся на одном уровне с исполняемым файлом и во всех подкаталогах
paths_to_mf_file = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path_to_executable_file) for f in filenames if os.path.splitext(f)[1] == '.mf']

if not paths_to_mf_file:
    print('Файлы mf не найдены')
    sys.exit()

#
# Список переменных, которые будут считываться с границ inlet, outlet и всех ID
# Здесь присутствуют только общие параметры границ inlet/outlet и ID
list_parameters_in_sections = [
    'Hub_radius',
    'Shroud_radius',
    'Area',
    'Number_of_blades',
    'Rotational_speed',
    'Specific_heat',
    'Specific_heat_ratio',
    'Radial_velocity',
    'Absolute_tangential_velocity',
    'Axial_velocity',
    'Absolute_velocity_magnitude',
    'Meridional_flow_angle',
    'Absolute_blade - to - blade_flow_angle',
    'Absolute_Mach_number',
    'Swirl',
    'Static_pressure',
    'Static_temperature',
    'Density',
    'Absolute_total_pressure',
    'Absolute_total_temperature',
    'Mass_flow'
    ]

# Список параметров режима (map) по границам inlet и outlet
list_map_parameters = [
    'Static_pressure_ratio',
    'Absolute_total_pressure_ratio',
    'Static_temperature_ratio',
    'Absolute_total_temperature_ratio',
    'Isentropic_efficiency',
    'Axial_thrust',
    'Torque',
    'Power'
    ]

# Список параметров injected / extracted
list_param_injector = [
    'Mass_flow',
    'Maximum_Mach_Number',
    'Absolute_Total_temperature',
    'Absolute_Total_pressure'
    ]


# Функция, которая читает mf файл и собирает с него метаданные:
def read_content_mf(path):
    try:
        opened_file = open(path, "r")
        string_from_mf = opened_file.read()
    finally:
        opened_file.close()
    global list_from_mf
    # list_from_mf - список всего контента *.mf файла
    list_from_mf = string_from_mf.split()

    # count_id - количество id
    # place_id - индект id в листе list_from_mf
    # count_injector - количество injected / extracted
    global count_id, place_id, count_injector
    count_id = 0
    place_id = [0, len(list_from_mf)]
    count_injector = 0
    # Проход по списку list_from_mf для определения count_id/place_id/count_injector
    for i in range(len(list_from_mf)):
        if list_from_mf[i] == 'ID':
            count_id += 1
            place_id.insert(len(place_id) - 1, i)
        # Подсчёт количества втеканий в тракт
        if list_from_mf[i] == 'Absolute_Total_pressure':
            count_injector += 1


# Проход по первому mf файлу чтобы определить параметры count_id/place_id/count_injector,
# которые используются для инициализации размеров матриц numpy
read_content_mf(paths_to_mf_file[0])


count_param = len(list_parameters_in_sections)
count_sec = 2 + count_id
count_mf = len(paths_to_mf_file)


# data_header - матрица numpy, содержащая  имя *.run файла из всех *.mf файлов
data_header = np.empty(count_mf, dtype=object)
# data_main - матрица numpy, содержащая все параметры list_parameters_in_sections со всех файлов.
data_main = np.empty((count_param, count_sec, count_mf))
# data_footer - матрица numpy, содержащая все параметры list_map_parameters со всех файлов
data_footer = np.empty((len(list_map_parameters), count_mf))
# Структура  всех матриц представлена картинкой png


count_param_injector = len(list_param_injector)


data_injector_name = np.empty((count_injector, count_mf), dtype=object)
# data_injector_name - матрица numpy, содержащая все имена injected / extracted
data_injector = np.empty((count_param_injector, count_injector, count_mf))
# data_injector - матрица numpy, содержащая все параметры injected / extracted


for n_path, path in enumerate(paths_to_mf_file):
    read_content_mf(path)
    n_inj = 0
    for k in range(place_id[0], place_id[1]):

        # Заполнение data_header
        if list_from_mf[k] == 'PROJECT' and list_from_mf[k+1] == 'NAME':
            data_header[n_path] = list_from_mf[k + 3]

        # Заполнение data_main данными с границы inlet и outlet
        if list_from_mf[k] == 'Hub_radius':
            data_main[0][0][n_path] = float(list_from_mf[k + 1])
            data_main[0][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Shroud_radius':
            data_main[1][0][n_path] = float(list_from_mf[k + 1])
            data_main[1][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Area':
            data_main[2][0][n_path] = float(list_from_mf[k + 1])
            data_main[2][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Number_of_blades':
            data_main[3][0][n_path] = float(list_from_mf[k + 1])
            data_main[3][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Rotational_speed':
            data_main[4][0][n_path] = float(list_from_mf[k + 1])
            data_main[4][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Specific_heat':
            data_main[5][0][n_path] = float(list_from_mf[k + 2])
            data_main[5][-1][n_path] = float(list_from_mf[k + 3])
            continue

        if list_from_mf[k] == 'Specific_heat_ratio':
            data_main[6][0][n_path] = float(list_from_mf[k + 1])
            data_main[6][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Radial_velocity':
            data_main[7][0][n_path] = float(list_from_mf[k + 1])
            data_main[7][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Absolute_tangential_velocity':
            data_main[8][0][n_path] = float(list_from_mf[k + 1])
            data_main[8][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Axial_velocity':
            data_main[9][0][n_path] = float(list_from_mf[k + 1])
            data_main[9][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Absolute_velocity_magnitude':
            data_main[10][0][n_path] = float(list_from_mf[k + 1])
            data_main[10][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Meridional_flow_angle':
            data_main[11][0][n_path] = float(list_from_mf[k + 1])
            data_main[11][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Absolute_blade-to-blade_flow_angle':
            data_main[12][0][n_path] = float(list_from_mf[k + 1])
            data_main[12][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Absolute_Mach_number':
            data_main[13][0][n_path] = float(list_from_mf[k + 1])
            data_main[13][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Swirl':
            data_main[14][0][n_path] = float(list_from_mf[k + 1])
            data_main[14][-1][n_path] = float(list_from_mf[k + 2])
            continue


        if list_from_mf[k] == 'Static_pressure':
            data_main[15][0][n_path] = float(list_from_mf[k + 1])
            data_main[15][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Static_temperature':
            data_main[16][0][n_path] = float(list_from_mf[k + 1])
            data_main[16][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Density':
            data_main[17][0][n_path] = float(list_from_mf[k + 1])
            data_main[17][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Absolute_total_pressure':
            data_main[18][0][n_path] = float(list_from_mf[k + 1])
            data_main[18][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Absolute_total_temperature':
            data_main[19][0][n_path] = float(list_from_mf[k + 1])
            data_main[19][-1][n_path] = float(list_from_mf[k + 2])
            continue

        if list_from_mf[k] == 'Mass_flow' and list_from_mf[k + 4] == 'Absolute_Mass_flow':
            data_main[20][0][n_path] = float(list_from_mf[k + 1])
            data_main[20][-1][n_path] = float(list_from_mf[k + 2])
            continue

        # Заполнение data_footer
        if list_from_mf[k] == 'Static_pressure_ratio':
            data_footer[0][n_path] = float(list_from_mf[k + 1])
        if list_from_mf[k] == 'Absolute_total_pressure_ratio':
            data_footer[1][n_path] = float(list_from_mf[k + 1])
        if list_from_mf[k] == 'Static_temperature_ratio':
            data_footer[2][n_path] = float(list_from_mf[k + 1])
        if list_from_mf[k] == 'Absolute_total_temperature_ratio':
            data_footer[3][n_path] = float(list_from_mf[k + 1])
        if list_from_mf[k] == 'Isentropic_efficiency':
            data_footer[4][n_path] = float(list_from_mf[k + 1])
        if list_from_mf[k] == 'Axial_thrust':
            data_footer[5][n_path] = float(list_from_mf[k + 1])
        if list_from_mf[k] == 'Torque':
            data_footer[6][n_path] = float(list_from_mf[k + 1])
        if list_from_mf[k] == 'Power':
            data_footer[7][n_path] = float(list_from_mf[k + 1])



        # Заполнение data_injector
        if list_from_mf[k] == 'Absolute_Total_pressure':  # отличается от 'Absolute_total_pressure'
            data_injector_name[n_inj][n_path] = list_from_mf[k - 7]
            data_injector[0][n_inj][n_path] = float(list_from_mf[k - 5])
            data_injector[1][n_inj][n_path] = float(list_from_mf[k - 3])
            data_injector[2][n_inj][n_path] = float(list_from_mf[k - 1])
            data_injector[3][n_inj][n_path] = float(list_from_mf[k + 1])
            n_inj += 1


    # заполнение data_main данными с сечений ID
    for i in range(0, count_id):
        for k in range(place_id[i + 1], place_id[i + 2]):
            if list_from_mf[k] == 'Hub_radius':
                data_main[0][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Shroud_radius':
                data_main[1][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Area':
                data_main[2][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Number_of_blades':
                data_main[3][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Rotational_speed':
                data_main[4][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Specific_heat':
                data_main[5][i + 1][n_path] = float(list_from_mf[k + 2])
            if list_from_mf[k] == 'Specific_heat_ratio':
                data_main[6][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Radial_velocity':
                data_main[7][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Absolute_tangential_velocity':
                data_main[8][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Axial_velocity':
                data_main[9][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Absolute_velocity_magnitude':
                data_main[10][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Meridional_flow_angle':
                data_main[11][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Absolute_blade-to-blade_flow_angle':
                data_main[12][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Absolute_Mach_number':
                data_main[13][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Swirl':
                data_main[14][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Static_pressure':
                data_main[15][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Static_temperature':
                data_main[16][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Density':
                data_main[17][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Absolute_total_pressure':
                data_main[18][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Absolute_total_temperature':
                data_main[19][i + 1][n_path] = float(list_from_mf[k + 1])
            if list_from_mf[k] == 'Mass_flow' and list_from_mf[k-1] == '---------':
                data_main[20][i + 1][n_path] = float(list_from_mf[k + 1])


# сохранение матриц в файл csv
with open(path_to_executable_file + r'\res.csv', 'w') as writr_res_file:
    object_res_file_csv = csv.writer(writr_res_file, delimiter=';', lineterminator='\r')

    # запись пути к run файлу, путей к mf файлам и их имён
    rr = ['path to run ']
    rr.extend(data_header)
    object_res_file_csv.writerow(rr)

    rr = ['path to mf ']
    rr.extend(paths_to_mf_file)
    object_res_file_csv.writerow(rr)

    rr = ['name mf ']
    rrr = [Path(x).stem for x in paths_to_mf_file]
    rr.extend(rrr)
    object_res_file_csv.writerow(rr)

    rr = ['Дата создания']
    rrr = [time.ctime(os.path.getmtime(x))for x in paths_to_mf_file]
    rr.extend(rrr)
    object_res_file_csv.writerow(rr)

    rr = ['Дата изменения']
    rrr = [time.ctime(os.path.getctime(x)) for x in paths_to_mf_file]
    rr.extend(rrr)
    object_res_file_csv.writerow(rr)


    # запись содержимого сечений (Inlet, Outlet, ID)
    for sec in range(count_sec):
        writr_res_file.write('\n' + 'section ' + str(sec) + '\n')
        for param in range(count_param):
            rr = (data_main[param, sec, :].tolist())
            rr.insert(0, list_parameters_in_sections[param])
            object_res_file_csv.writerow(rr)


    # запись интегральных параметров
    writr_res_file.write('\n' + 'footer' + '\n')
    for param in range(len(list_map_parameters)):
        rr = (data_footer[param, :].tolist())
        rr.insert(0, list_map_parameters[param])
        object_res_file_csv.writerow(rr)

    # Запись injected / extracted
    if count_injector: writr_res_file.write('\n' + 'DETAIL OF MASS FLOW THROUGH COOLING/BLEED' + '\n')
    for inj in range(count_injector):
        writr_res_file.write('\n' + 'name_inj ' + str(inj) + '\n')
        rr = data_injector_name[inj, :].tolist()
        rr.insert(0, '')
        object_res_file_csv.writerow(rr)
        for param in range(count_param_injector):
            rr = (data_injector[param, inj, :].tolist())
            rr.insert(0, list_param_injector[param])
            object_res_file_csv.writerow(rr)


# Команда на открытие csv файле
os.startfile(path_to_executable_file + r'\res.csv')
#


# if __name__ == '__main__':


