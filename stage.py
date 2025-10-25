import os
import sqlite3
import sys
from tabulate import tabulate

def update_rows(cur,con,all_fields_in_table): #обновление по условию
    field = ""
    while field not in all_fields_in_table:
        field = input("Введите поле, в котором будут изменены все изначения на заданное: ").strip()
        
    value = input("Введите значение, которое будет записано во все строки столбца {}: ".format(field)).strip()
    sql = "UPDATE reportMPEI SET {} =?".format(field)
    cur.executemany(sql,value)
    con.commit()
    print("Операция завершена")

def delete_row(cur,con): #удаление строки
    subject_id = input("Введите код дисциплины для удаления строк из БД: ").strip()
    date_attestation = input("Введите дату аттестации для удаления строк из БД: ").strip()
    acction = input("Внимание строка с кодом дисциплины {} и датой аттестации {} будет удалена, продолжить ? ДА/НЕТ ".format(subject_id,date_attestation)).strip()
    if acction != "ДА":
        print("Удаление отменено!")
        return
    
    sql = "DELETE FROM reportMPEI WHERE subjectId=? AND dateAttestation=?"
    cur.execute(sql, (subject_id, date_attestation))
    con.commit()
    print("Строка удалена")
    return

def field_choice(cur,con,all_fields_in_table): #извлечение по условию 
    name_field = ""
    while name_field not in all_fields_in_table:
        name_field = input("Выбирете одно из полей таблицы reportMPEI: ").strip()
        
    set_operators = ("=", "!=",  "<", ">", "<=",  ">=")
    print("Доступные операторы: ",set_operators)
    operator = ""
    while operator not in set_operators:
        operator = input("Введите необходимый оператор для задания условия по значениям поля {}: ".format(name_field)).strip()
        
    value = input("Введите числовое значние для применения оператора '{}' ".format(operator)).strip()
    sql = "SELECT * FROM reportMPEI WHERE {}?".format(name_field+operator)
    cur.execute(sql,(value,))
    con.commit()
    getData = cur.fetchall()
    print(tabulate(getData, headers=[all_fields_in_table[i] for i in range (len(all_fields_in_table))], tablefmt="grid"))

def add_new_row(cur,con): #добавление новой строки
    push_to_table=[]; dano=[]
    dano.append(input('Код дисциплины по учебному плану=').strip())
    dano.append(input('Название дисциплины=').strip())
    dano.append(input('Номер семестра с аттестацией по дисциплине=').strip())
    dano.append(input('Тип аттестации (экзамен/зачет)=').strip())
    dano.append(input('Дата аттестации=').strip())
    dano.append(input('ФИО преподавателя, проводившего аттестацию=').strip())
    dano.append(input('Должность преподавателя=').strip())
    dano.append(input('Полученная оценка=').strip())
    dano.append(input('Дата занесения/обновления записи=').strip())
    push_to_table.append(tuple(dano))
    sql="""INSERT INTO reportMPEI (subjectId,subject,semestrNumber,typeAttestation,dateAttestation,fioTeacher,
                                                postTeacher,markGet,updateDate) VALUES (?,?,?,?,?,?,?,?,?)"""
    cur.executemany(sql,push_to_table)
    con.commit()
    print("Вставка осуществлена!")

def save_all_database_in_file(cur): # сохранение в файл 
    name = input("Введите имя файла для сохранения содержимиого таблицы reportMPEI: ")
    file=open('{}'.format(name),'w')
    cur.execute("PRAGMA table_info(reportMPEI);")
    columns = [column[1] for column in cur.fetchall()]
    file.write(str(columns)+'\n')
    sql = 'SELECT * FROM reportMPEI;'
    data = cur.execute(sql).fetchall()
    file.write(str(data)+'\n')
    file.close()
    print("Файл сохранен")
    
def view_all_current_table(columns,cur,all_fields_in_table): #просмотр всех полей
    sql = 'SELECT * FROM reportMPEI'
    data = cur.execute(sql).fetchall()
    print(tabulate(data, headers=[all_fields_in_table[i] for i in range (len(all_fields_in_table))], tablefmt="grid"))
    return

def start(cur,con):
    print("Список имен полей таблицы reportMPEI".center(80))
    cur.execute("PRAGMA table_info(reportMPEI)")
    columns = cur.fetchall()
    all_fields_in_table = []
    for i in columns:
        all_fields_in_table.append(i[1])
        print("Поле - ",i[1])
        
    while True:
        print("Меню".center(80))
        print("Введите 1 для отображение текущего содержимого таблицы БД на экране в ввде таблицы")
        print("Введите 2 для сохранения текущего содержимого таблицы БД в текстовый файл")
        print("Введите 3 для отображения содержимого какого-либо поля БД с заданием логического выражения по значениям")
        print("Введите 4 для удаления строки из базы данных по коду дисциплины и дате аттестации")
        print("Введите 5 для замены значений во всех строках в указанном поле на заданное значение")
        print("Введите 6 для добавления новой строки")
        print("Введите 7 для вывода списка имен БД")
        print("Введите 8 для завершения работы программы")
        tab = (input("Выберите номер необходимого действия \t"))

        match tab:
            case "1":
                view_all_current_table(columns,cur,all_fields_in_table)
            case "2":
                save_all_database_in_file(cur)
            case "3":
                field_choice(cur,con,all_fields_in_table)
            case "4":
                delete_row(cur,con)
            case "5":
                update_rows(cur,con,all_fields_in_table)
            case "6":
                add_new_row(cur,con)
            case "7":
                for i in range (len(all_fields_in_table)):
                    print("Поле - ",all_fields_in_table[i]) 
            case "8":
                print("Завршение работы программы")
                return
            
def main():
    #работа с БД
    print("Здравствуйте, эта программа работает с таблицей reportMPEI, проверяю есть ли данная таблица в директории\n")
    path_folder = os.getcwd()
    path_to_file = os.path.join(path_folder, "db_step3.sqlite")
    
    if not(os.path.isfile(path_to_file)):
        print("В рабочей директории не обнаружен файл db_step3.sqlite. Попробуйте сменить директорию и запустить программу заново")
        return

    print("Таблица reportMPEI найдена, запускаю программу!\n")
    con = sqlite3.connect('db_step3.sqlite')
    cur = con.cursor()
    start(cur,con)
    cur.close()
    con.close()
    print("Работа программы завршена")

