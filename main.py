import random
import numpy

if __name__ == '__main__':

    class work_day:
        smena_excavator_cl = 0
        smena_bulldozer_cl = 0
        smena_excavator_repair_cl = 0
        smena_bulldozer_repair_cl = 0

        def _init_(self):
            self.smena_excavator_repair_cl = 0
            self.smena_bulldozer_repair_cl = 0
            self.smena_excavator_cl = 0
            self.smena_bulldozer_cl = 0

    obj_work_day = work_day() #объект класса
    list_6 = [] #список, хранящий данные всех прошедших дней для слесаря 6 разряда
    list_36 = []  # список, хранящий данные всех прошедших дней для слесарей 3 и 6 разряда

    # Математические ожидания
    Mx_work_excavator = 4 # мат.ожидание работы, час
    Mx_work_bulldozer = 6
    Mx_repair_excavator = 1
    Mx_repair_bulldozer = 2

    # Финансы
    price_excavator = 500 # прибыль/потери за 1 час
    price_bulldozer = 300

    price_worker6 = 100 # з/п за 1 час
    price_worker36 = 160 # з/п за 1 час
    price_repair = 50 # накладные при починки за 1 час

    fulltime_smena_sec = 16 * 3600
    n = 1000 # кол-во итераций

    for j in range(2):
        # Средние значения за количество дней
        average_smena_excavator = 0  # среднее время работы экскаватора за n дней, сек
        average_smena_bulldozer = 0
        average_smena_excavator_repair = 0  # среднее время починки экскаватора за n дней, сек
        average_smena_bulldozer_repair = 0

        if j == 1:
            Mx_repair_excavator = 0.25
            Mx_repair_bulldozer = 1.5
            price_worker6 = 160  # з/п за 1 час

        for i in range(n):
            smena_excavator = 0 # всё время работы экскаватора за 1 смену, сек
            smena_bulldozer = 0
            smena_excavator_repair = 0  # всё время починки экскаватора за 1 смену, сек
            smena_bulldozer_repair = 0

            rand_value_excavator = int(numpy.random.exponential(Mx_work_excavator) * 3600)  # время работы (до смены статуса)
            if rand_value_excavator >= (fulltime_smena_sec):
                smena_excavator = fulltime_smena_sec
            else:
                smena_excavator += rand_value_excavator   # накапливаем время работы грейдера

            rand_value_bulldozer = int(numpy.random.exponential(Mx_work_bulldozer) * 3600)
            if rand_value_bulldozer >= (fulltime_smena_sec): # если время работы > 16 часов
                smena_bulldozer = fulltime_smena_sec
            else:
                smena_bulldozer += rand_value_bulldozer

            rand_value_repair = 0       # время починки
            status_excavator = 1   # -1 - чинится 0 - простаивает 1 - работает
            status_bulldozer = 1

            point_excavator = 0
            point_bulldozer = 0
            point_excavator = rand_value_excavator    # точка будущего события во времени (определяется до события по циклу)
            point_bulldozer = rand_value_bulldozer

            for t in range(fulltime_smena_sec):

                if t == point_excavator: # произошло событие (смена статуса экскаватора)
                    if status_excavator == 1: # окончание работы
                        if status_bulldozer != -1: # если бульдозер не чинится (слесарь свободен)
                            status_excavator = -1
                            rand_value_repair = int(numpy.random.exponential(Mx_repair_excavator) * 3600) # определяем время починки
                            if (point_excavator + rand_value_repair) < (fulltime_smena_sec):
                                point_excavator += rand_value_repair # определяем точку следующего события: экскаватор починился
                                smena_excavator_repair += rand_value_repair
                            else:
                                point_excavator = fulltime_smena_sec + 1
                                smena_excavator_repair += (fulltime_smena_sec - t)
                        else: # status_bulldozer == -1: # если бульдозер чинится (слесарь занят)
                            status_excavator = 0
                            point_excavator = point_bulldozer # определяем время события: бульдозер сменит статус
                    elif status_excavator == 0: # окончание простоя
                        status_excavator = -1
                        rand_value_repair = int(numpy.random.exponential(Mx_repair_excavator) * 3600)
                        if (point_excavator + rand_value_repair) < (fulltime_smena_sec):
                            point_excavator += rand_value_repair  # определяем время события: экскаватор закончит чиниться
                            smena_excavator_repair += rand_value_repair # накапливаем время починки грейдера
                        else:
                            point_excavator = fulltime_smena_sec + 1
                            smena_excavator_repair += (fulltime_smena_sec - t)
                    else:   # status_excavator == -1 # окончание ремонта
                        status_excavator = 1
                        rand_value_excavator = int(numpy.random.exponential(Mx_work_excavator) * 3600)
                        if (point_excavator + rand_value_excavator) < (fulltime_smena_sec):
                            point_excavator += rand_value_excavator # определяем время события: экскаватор сломается
                            smena_excavator += rand_value_excavator # накапливаем время работы грейдера
                        else:
                            point_excavator = fulltime_smena_sec + 1
                            smena_excavator += (fulltime_smena_sec - t)

                if t == point_bulldozer: # произошло событие (смена статуса бульдозера)
                    if status_bulldozer == 1:
                        if status_excavator != -1:
                            status_bulldozer = -1
                            rand_value_repair = int(numpy.random.exponential(Mx_repair_bulldozer) * 3600)
                            if (point_excavator + rand_value_repair) < (fulltime_smena_sec):
                                point_bulldozer += rand_value_repair
                                smena_bulldozer_repair += rand_value_repair
                            else:
                                point_bulldozer = fulltime_smena_sec + 1
                                smena_bulldozer_repair += (fulltime_smena_sec - t)
                        else: #status_excavator == -1: # если экскаватор чинится
                            status_bulldozer = 0
                            point_bulldozer = point_excavator # определяем время события: когда экскаватор изменит статус
                    elif status_bulldozer == 0:
                        status_bulldozer = -1
                        rand_value_repair = int(numpy.random.exponential(Mx_repair_bulldozer) * 3600)
                        if (point_excavator + rand_value_repair) < (fulltime_smena_sec):
                            point_bulldozer += rand_value_repair # определяем время события: когда бульдозер закончит чиниться
                            smena_bulldozer_repair += rand_value_repair
                        else:
                            point_bulldozer = fulltime_smena_sec + 1
                            smena_bulldozer_repair += (fulltime_smena_sec - t)
                    else:   # status_bulldozer == -1 # окончание ремонта
                        status_bulldozer = 1
                        rand_value_bulldozer = int(numpy.random.exponential(Mx_work_bulldozer) * 3600)
                        if (point_bulldozer + rand_value_bulldozer) < (fulltime_smena_sec):
                            point_bulldozer += rand_value_bulldozer
                            smena_bulldozer += rand_value_bulldozer
                        else:
                            point_bulldozer = fulltime_smena_sec + 1
                            smena_bulldozer += (fulltime_smena_sec - t)

            obj_work_day.smena_excavator_cl = round(smena_excavator / 3600, 2) # заполняем объект
            obj_work_day.smena_bulldozer_cl = round(smena_bulldozer / 3600, 2)
            obj_work_day.smena_excavator_repair_cl = round(smena_excavator_repair / 3600, 2)
            obj_work_day.smena_bulldozer_repair_cl = round(smena_bulldozer_repair / 3600, 2)

            if (j == 0):
                list_6.insert(n, obj_work_day) # сохраняем значения за день в список
            elif (j == 1):
                list_36.insert(n, obj_work_day)

            # добавляем время к накопителю, для подсчета среднего в конце
            average_smena_excavator += smena_excavator # в секундах
            average_smena_bulldozer += smena_bulldozer
            average_smena_excavator_repair += smena_excavator_repair
            average_smena_bulldozer_repair += smena_bulldozer_repair

        average_smena_excavator /= n * 3600 # в часах
        average_smena_bulldozer /= n * 3600
        average_smena_excavator_repair /= n * 3600
        average_smena_bulldozer_repair /= n * 3600

        if j == 0:
            print("\n===================Слесарь 6 разряда=========================")
        else:
            print("\n===================Слесари 3 и 6 разряда=====================")

        print("Среднее время работы, часов:")
        print(" работа экскаватора", round(average_smena_excavator, 2))
        print(" работа бульдозера", round(average_smena_bulldozer, 2))
        print(" починка экскаватора", round(average_smena_excavator_repair, 2))
        print(" починка бульдозера", round(average_smena_bulldozer_repair, 2))

        profit_excavator = average_smena_excavator * price_excavator
        profit_bulldozer = average_smena_bulldozer * price_excavator
        total_profit = profit_excavator + profit_bulldozer
        print("Прибыль от экскаватора, руб:", round(profit_excavator, 2))
        print("Прибыль от бульдозера, руб:", round(profit_bulldozer, 2))

        total_repair_time = average_smena_excavator_repair + average_smena_bulldozer_repair
        print("З/п слесаря, руб:", round(total_repair_time * price_worker6, 2))
        print("Накладные на ремонт, руб:", round(total_repair_time * price_repair, 2))

        print("Итого средняя прибыль, руб:", round(total_profit - total_repair_time * (price_worker6 + price_repair), 2))