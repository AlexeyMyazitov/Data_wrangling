import os, sys
import socket
import csv
path_to_executable_file = os.path.abspath(os.path.dirname(sys.argv[0]))
paths_to_read_file = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path_to_executable_file) for f in filenames if os.path.splitext(f)[1] == '.qualityReport']
hostname = socket.gethostname()

if not paths_to_read_file:
    print('Файлы mf не найдены')
    sys.exit()
if len(paths_to_read_file) > 1:
    print('Найдено больше одного файла')
    sys.exit()

def read_content(path):
    try:
        opened_file = open(path, "r")
        string_content= opened_file.read()
    finally:
        opened_file.close()

    return(string_content)

string_content = read_content(paths_to_read_file[0])
list_content = string_content.split()

main_data = []
row_names = []
number_of_main_blade =[]
number_of_layers = []
current_number_row: int = 0
print(list_content)

name_param =[
            "Имя",
            "Количество узлов",
            "Количество уровней сеточной модели",
            "Минимальный угол скошенности",
            "Средний угол скошенности",
            "Максимальный коэффициент роста в меридиональной плоскости",
            "Средний коэффициент роста в меридиональной плоскости",
            "Максимальное соотношение сторон",
            "Среднее соотношение сторон",
            "Максимальный коэффициент роста в 3D",
            "Средний коэффициент роста в 3D",
            "Среднее расстояние до стенки"
            "Количество слоёв сетки межлопаточного канала"
            "Количество лопаток в венце"
            ]

for n_key, key in enumerate(list_content):
    # условие на чтение метрик всей сетки

    if key == 'AUTOGRID' and list_content[n_key + 1] == 'version':
        autogrid_version = list_content[n_key + 2]

    if key == 'TEMPLATE' and list_content[n_key + 1] == 'FILE':
        template_file = list_content[n_key + 3]

    if key == 'NUMBER' and list_content[n_key + 1] == 'OF'  and list_content[n_key + 2]== 'ROWS':
        number_of_rows = list_content[n_key + 3]

    if key == 'ROW' and list_content[n_key + 1] == 'NAME:':
        row_names.append(list_content[n_key + 2])
        number_of_main_blade.append(list_content[n_key + 7])
        number_of_layers.append(list_content[n_key + 20])



    if (key == 'Number'
            and list_content[n_key+1] == 'of'
            and list_content[n_key+2] == 'Points'
            and list_content[n_key+6] == 'grid'
            and list_content[n_key-6] == "Entire"):

        main_data.append([])
        main_data[current_number_row].append('Вся сетка')  # Имя ряда
        main_data[current_number_row].append(list_content[n_key + 3]) # Количество узлов
        main_data[current_number_row].append(list_content[n_key + 8]) # Количество уровней сеточной модели
        main_data[current_number_row].append(list_content[n_key + 12]) # Минимальный угол скошенности
        main_data[current_number_row].append(list_content[n_key + 20]) # Средний угол скошенности
        main_data[current_number_row].append(list_content[n_key + 45]) # Максимальный коэффициент роста в меридиональной плоскости
        main_data[current_number_row].append(list_content[n_key + 50])  # Средний коэффициент роста в меридиональной плоскости
        main_data[current_number_row].append(list_content[n_key + 58])  # Максимальное соотношение сторон
        main_data[current_number_row].append(list_content[n_key + 62])  # Среднее соотношение сторон
        main_data[current_number_row].append(list_content[n_key + 70])  # Максимальный коэффициент роста в 3D
        main_data[current_number_row].append(list_content[n_key + 74])  # Средний коэффициент роста в 3D
        main_data[current_number_row].append(list_content[n_key + 89])  # Среднее расстояние до стенки
        current_number_row += 1

    if (key == 'Number'
            and list_content[n_key+1] == 'of'
            and list_content[n_key+2] == 'Points'
            and list_content[n_key+6] == 'grid'
            and list_content[n_key-6] != "Entire"):


        main_data.append([])
        main_data[current_number_row].append(row_names[current_number_row-1])  # Имя ряда
        main_data[current_number_row].append(list_content[n_key + 3]) # Количество узлов
        main_data[current_number_row].append(list_content[n_key + 8]) # Количество уровней сеточной модели
        main_data[current_number_row].append(list_content[n_key + 12]) # Минимальный угол скошенности
        main_data[current_number_row].append(list_content[n_key + 20]) # Средний угол скошенности
        main_data[current_number_row].append(list_content[n_key + 58]) # Максимальный коэффициент роста в меридиональной плоскости
        main_data[current_number_row].append(list_content[n_key + 63])  # Средний коэффициент роста в меридиональной плоскости
        main_data[current_number_row].append(list_content[n_key + 78])  # Максимальное соотношение сторон
        main_data[current_number_row].append(list_content[n_key + 82])  # Среднее соотношение сторон
        main_data[current_number_row].append(list_content[n_key + 96])  # Максимальный коэффициент роста в 3D
        main_data[current_number_row].append(list_content[n_key + 100])  # Средний коэффициент роста в 3D
        main_data[current_number_row].append(list_content[n_key + 121])  # Среднее расстояние до стенки
        current_number_row += 1


print(main_data)


with open(path_to_executable_file + r'\res.csv', 'w') as writr_res_file:
    object_res_file_csv = csv.writer(writr_res_file, delimiter=';', lineterminator='\r')
    # rr = ['1', '2', '\r' , '3']
    # rr2 = ['1', '2', '3']
    # object_res_file_csv.writerow(rr)
    # object_res_file_csv.writerow(rr2)
    # writr_res_file.write('\n' + 'section ' + str(1) + ';' + ';' + '2'+'\n'+'\n')

    object_res_file_csv.writerow(['Версия AutoGrid', autogrid_version])
    object_res_file_csv.writerow(['Имя компьютера', hostname])
    object_res_file_csv.writerow(['Путь к шаблону *.trb', template_file])

    for n_par, par in enumerate(name_param):
        row = [par]
        row_par = []
        for n_blade, blade in enumerate(main_data):
            row_par = main_data[n_blade][n_par]
            row.append(row_par)
        object_res_file_csv.writerow(row)

os.startfile(path_to_executable_file + r'\res.csv')