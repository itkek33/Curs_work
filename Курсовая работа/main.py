#Ипортирование библиотек
import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5.uic import loadUi
#Подключение к базе данных 
db = sqlite3.connect("EquipmentRecorder.db")
sql = db.cursor()

#Класс окна авторизации
class Login(QDialog):
    #Функцияя __init__ которая вызывается при вызове самого класса
    def __init__(self):
        super(Login,self).__init__()
        #Открытие ui формы авторизации
        loadUi("log.ui",self)
        
        #Добавление функции для кнопки 
        self.loginpushButton.clicked.connect(self.loginfunction)
        
    def loginfunction(self):
        #Запись в переменные данных из полей для логина и пароля
        login=self.login.text()
        password=self.password.text()
        #sql запрос на проверку есть ли введённые данные в таблице акаунтов администрации
        sql.execute(f"SELECT * FROM login WHERE login = '{login}' AND password = '{password}';")
        #сохраннение после sql запроса
        db.commit() 
        #Проверка на то есть ли введённые данные в таблице, Если нет то нечего не происходит, если же есть
        #то Вызывается класс под окно с меню с переходами на все другие окна
        if sql.fetchone() == None:
            print("Такого акаунта нету")
        else:
            print('Welcome')
            #Вызываем с помощью нажатой кнопки класс меню
            loginpushButton=Menu()
            widget.addWidget(loginpushButton)
            widget.setCurrentIndex(widget.currentIndex()+1)
#Класс окна меню
class Menu(QDialog):
    #Функцияя __init__ которая вызывается при вызове самого класса
    def __init__(self):
        super(Menu,self).__init__()
        #Открытие ui формы меню
        loadUi("menu.ui",self)
        #Добавление функции для кнопок 
        self.menubutton_1.clicked.connect(self.open1)
        self.menubutton_2.clicked.connect(self.open2)
        self.menubutton_3.clicked.connect(self.open3)
        self.menubutton_4.clicked.connect(self.open4)
        self.menubutton_5.clicked.connect(self.open5)
        self.menubutton_6.clicked.connect(self.open6)
        self.menubutton_7.clicked.connect(self.open7)
        self.menubutton_8.clicked.connect(self.open8)
        self.menubutton_9.clicked.connect(self.open9)
    #Функции открытия других форм    
    def open1(self):
        #Вызываем с помощью нажатой кнопки класс который обозначен на данной кнопке
        menubutton_1=Equipment_more_detailed()
        widget.addWidget(menubutton_1)
        widget.setCurrentIndex(widget.currentIndex()+1)
    #Следующие 8 функциий работают так же, но вызывают другие классы которые тоже обозначенны на кнопках
    def open2(self):
        menubutton_2=Main()
        widget.addWidget(menubutton_2)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def open3(self):
        menubutton_3=Broken_equipment()
        widget.addWidget(menubutton_3)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def open4(self):
        menubutton_4=Equipment()
        widget.addWidget(menubutton_4)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def open5(self):
        menubutton_5=Equipment_prevention()
        widget.addWidget(menubutton_5)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def open6(self):
        menubutton_6=Equipmentprevention_will_soon()
        widget.addWidget(menubutton_6)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def open7(self):
        menubutton_7=Place()
        widget.addWidget(menubutton_7)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def open8(self):
        menubutton_8=Type_equipments()
        widget.addWidget(menubutton_8)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def open9(self):
        menubutton_9=Workers()
        widget.addWidget(menubutton_9)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
#Класс окна Оборудование детально       
class Equipment_more_detailed(QDialog):
    #Функцияя __init__ которая вызывается при вызове самого класса
    def __init__(self):
        super(Equipment_more_detailed,self).__init__()
        #Открытие ui формы меню
        loadUi("Equipment_more_detailed.ui",self)
        #Добавление функции для кнопок 
        self.InnerButton.clicked.connect(self.insert_staff)
        self.OpenButton.clicked.connect(self.open_file)
        self.DeleteButton.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.hub.clicked.connect(self.menu)
        self.conn = None
    #переменная для реализации не более одного срабатывания добавления колонок в выподающий список
    test = False
    #функция открытия и визуального отображения таблицы
    def open_file(self):
        try:
            #добавление соеденения с базой данных 
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            #запрос на вывод всех данных из таблицы
            data = cur.execute("select * from Equipment_more_detailed")
            #занесение в переменные количество строк и столбцов для будущего нормального отображения данных
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        #обработчик ошибок
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        #задание параметров с помощью ранее созданных переменных
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        #проверка в первый ли раз добавляются колоноки в выподающий список
        if Equipment_more_detailed.test == False:
            self.cbColNames.addItems(col_name)
            Equipment_more_detailed.test = True
        #добавление построчно через цикл данные в окно вывода таблицы
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        
    #функция обновления вывода данных 
    #она добавленна в многих функциях в конце для отображения изменения в таблице сразу как она измениться 
    def update_tableWidget(self, query="select * from Equipment_more_detailed"):
        try:
            #добавление соеденения в переменную и добавление запроса в переменную
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        #обработчик ошибок
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        #добавление построчно через цикл данные в окно вывода таблицы
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        
    #функция добавления строк в таблицу
    def insert_staff(self):
        try:
            #добавление в переменную соеденение с базой данных
            cur = self.conn.cursor()
            #запрос на добавление в талицу данных и как данные берутся значения из полей ввода которые 
            #находятся на форме
            cur.execute(f"""insert into Equipment_more_detailed(type_equipment, name, maker, price, service_life, guarantee, start_of_operation)
            values('{self.wrt1.text()}', '{self.wrt2.text()}', '{self.wrt3.text()}', '{self.wrt4.text()}', '{self.wrt5.text()}', '{self.wrt6.text()}', '{self.wrt7.text()}')""")
            #сохранение изменений
            db.commit()
            self.conn.commit()
            #закрытие соеденение с базой данных
            cur.close()
        #обработчик ошибок
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_tableWidget()
    #функция удаления данных из таблицы
    def delete_staff(self):
        #занесение в переменные данных о выбранной строке которую нужно удалить
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            #соеденение с базой данных
            cur = self.conn.cursor()
            #запрос на удаление где удаление происходит по id выбранного элемента администратором 
            cur.execute(f"delete from Equipment_more_detailed where id = {num}")
            #сохранение изменений
            self.conn.commit()
            #закрытие соеденения с базой данных
            cur.close()
        #обработчик ошибок
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_tableWidget()
    #функция поиска по выбранному столбцу
    def find_for_val(self):
        #запись в переменные текста по которому происходит поиск и запись выбранного элемента из 
        #выподающего списка
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        #запрос на вывод данных по выбранному элементу с прописынным значением из поля ввода
        self.update_tableWidget(f"select * from Equipment_more_detailed where {col} like '{val}'")
    #функция вызова меню с переходами на все другие окна
    def menu(self):
        #вызов класса меню
        hub=Menu()
        widget.addWidget(hub)
        widget.setCurrentIndex(widget.currentIndex()+1)

      
class Main(QDialog):
    def __init__(self):
        super(Main,self).__init__()
        loadUi("main.ui",self)
        self.InnerButton.clicked.connect(self.insert_staff)
        self.OpenButton.clicked.connect(self.open_file)
        self.DeleteButton.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.hub.clicked.connect(self.menu)
        self.conn = None

    test = False
    def open_file(self):
        try:
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from main")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        if Main.test == False:
            self.cbColNames.addItems(col_name)
            Main.test = True
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def update_tableWidget(self, query="select * from main"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def insert_staff(self):

        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into main(id_Equipment, id_worcer, place)
            values('{self.wrt1.text()}', '{self.wrt2.text()}', '{self.wrt3.text()}')""")
            db.commit()
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_tableWidget()

    def delete_staff(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from main where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_tableWidget()
    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_tableWidget(f"select * from main where {col} like '{val}'")

    def menu(self):
        hub=Menu()
        widget.addWidget(hub)
        widget.setCurrentIndex(widget.currentIndex()+1)
#класс сломанного оборудования
class Broken_equipment(QDialog):
    def __init__(self):
        super(Broken_equipment,self).__init__()
        #Открытие ui формы сломанного оборудования
        loadUi("broken_equipment.ui",self)
        #добавление кнопкам функции
        self.InnerButton.clicked.connect(self.insert_staff)
        self.OpenButton.clicked.connect(self.open_file)
        self.DeleteButton.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.hub.clicked.connect(self.menu)
        self.conn = None
    #переменная для реализации не более одного срабатывания добавления колонок в выподающий список
    test = False
    def open_file(self):
        #тут используется сразу несколько sql запросов из-за чего нужно после каждого запроса закрывать 
        #и заново открывать соединение с бд
        try:
            #соеденение с базой данных
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            #sql запрос на вывод гарантии для дальнейшей её проверки 
            gurantee = cur.execute("""select guarantee from  Equipment_more_detailed INNER JOIN broken_equipment on broken_equipment.id_equipment = Equipment_more_detailed.id  where broken_equipment.id_equipment = Equipment_more_detailed.id ;""")
            string1 = ( [ row[0] for row in gurantee.fetchall() ] )
            for i in range(len(string1)):
                #соеденение с базой данных
                self.conn = sqlite3.connect('EquipmentRecorder.db')
                cur = self.conn.cursor()
                #запрос на обновление атрибута
                cur.execute(f"""UPDATE broken_equipment set works_guarantee = "нет"  FROM Equipment_more_detailed where DATETIME(start_of_operation, '+{string1[i]} month') < CURRENT_TIMESTAMP AND Equipment_more_detailed.id= broken_equipment.id_equipment And (select ROW_NUMBER() OVER() from broken_equipment) ={i+1};""")
                #сохранение изменений и закрытие подключения к бд, и открытие этого соединения 
                self.conn.commit()
                self.conn.close()
                #соеденение с базой данных
                self.conn = sqlite3.connect('EquipmentRecorder.db')
                cur = self.conn.cursor()
                #запрос на обновление атрибута
                cur.execute(f"""UPDATE broken_equipment set works_guarantee = "есть"  FROM Equipment_more_detailed where DATETIME(start_of_operation, '+{string1[i]} month') > CURRENT_TIMESTAMP AND Equipment_more_detailed.id= broken_equipment.id_equipment And  (select ROW_NUMBER() OVER() from broken_equipment) ={i+1} ;""")
                #сохранение изменений и закрытие подключения к бд, и открытие этого соединения 
                self.conn.commit()
                self.conn.close()
            #соеденение с базой данных
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            #вывод всех данных из таблицы
            cur.execute("""SELECT * FROM broken_equipment;""")
            col_name = [description[0] for description in cur.description]
            data_rows = cur.fetchall()
            #сохранение изменений и закрытие подключения к бд
            self.conn.commit()
            self.conn.close()
            self.tableWidget.setRowCount(0)
            #вывод с помощью цикла всех значений запроса
            for i, row in enumerate(data_rows):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.setHorizontalHeaderLabels(col_name)
            self.tableWidget.resizeColumnsToContents()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        finally:
            #закрытие соеденения к базе данных 
            self.conn.close()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        #условие которое даёт возможность только 1 раз добавить элементы в выподающий список
        if Broken_equipment.test == False:
            self.cbColNames.addItems(col_name)
            Broken_equipment.test = True
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def update_tableWidget(self, query="select * from broken_equipment"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def insert_staff(self):

        try:
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            cur.execute(f"""insert into broken_equipment(type_equipment, id_equipment, data_breakdown)
            values('{self.wrt1.text()}', '{self.wrt2.text()}', '{self.wrt3.text()}')""")
            self.conn.commit()
            self.conn.close()
            
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_tableWidget()

    def delete_staff(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            cur.execute(f"delete from broken_equipment where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_tableWidget()
    def find_for_val(self):
        self.conn = sqlite3.connect('EquipmentRecorder.db')
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_tableWidget(f"select * from broken_equipment where {col} like '{val}'")

    def menu(self):
        hub=Menu()
        widget.addWidget(hub)
        widget.setCurrentIndex(widget.currentIndex()+1)
      
class Equipment(QDialog):
    def __init__(self):
        super(Equipment,self).__init__()
        loadUi("equipment.ui",self)
        self.InnerButton.clicked.connect(self.insert_staff)
        self.OpenButton.clicked.connect(self.open_file)
        self.DeleteButton.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.hub.clicked.connect(self.menu)
        self.conn = None
    
    test = False
    def open_file(self):
        try:
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from equipment")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        if Equipment.test == False:
            self.cbColNames.addItems(col_name)
            Equipment.test = True
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def update_tableWidget(self, query="select * from equipment"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def insert_staff(self):

        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into equipment(id_screen, Id_keyboard, id_mouse, id_computer, id_additional)
            values('{self.wrt1.text()}', '{self.wrt2.text()}', '{self.wrt3.text()}', '{self.wrt4.text()}', '{self.wrt5.text()}')""")
            db.commit()
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_tableWidget()

    def delete_staff(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from equipment where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_tableWidget()
    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_tableWidget(f"select * from equipment where {col} like '{val}'")

    def menu(self):
        hub=Menu()
        widget.addWidget(hub)
        widget.setCurrentIndex(widget.currentIndex()+1)
#Класс оборудования с истекшим сроком эксплуатации
class Equipment_prevention(QDialog):
    def __init__(self):
        super(Equipment_prevention,self).__init__()
        #Открытие ui окна оборудования с истекшим сроком эксплуатации
        loadUi("equipment_prevention.ui",self)
        #Добавление кнопкам функции
        self.OpenButton.clicked.connect(self.open_file)
        self.pbFind.clicked.connect(self.find_for_val)
        self.hub.clicked.connect(self.menu)
        self.conn = None
    #переменная для проверки вызывалась ли функции вывода 
    test = False
    def open_file(self):
        #полностью отсутствуют функции добавление,удаления данных так как это делается автоматически
        try:
            #соеденение с базой данных
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            #запрос на удаление всех данных из таблицы
            cur.execute("DELETE FROM equipment_prevention;")
            #сохранение и закрытие соеденения
            self.conn.commit()
            self.conn.close()
            #соеденение с базой данных
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            #запрос на вывод срока эксплуатации из таблицы оборудование детально
            service_life = cur.execute("""select service_life from  Equipment_more_detailed ;""")
            #создание масива из переменной service_life(масив из всех сроков эксплуатации )
            string1 = ( [ row[0] for row in service_life.fetchall() ] )
            #цикл на добавление всех оборудований с истёкшим сроком эксплуатации
            for i in range(len(string1)):
                #соеденение с базой данных
                self.conn = sqlite3.connect('EquipmentRecorder.db')
                cur = self.conn.cursor()
                #запрос на добавление оборудования, где истёк срок эксплуатации
                cur.execute(f"INSERT INTO equipment_prevention( type_equipment ,id_equipment,start_of_operation,service_life) SELECT type_equipment, id, start_of_operation, service_life from Equipment_more_detailed where DATETIME(start_of_operation, '+{string1[i]} month') < CURRENT_TIMESTAMP And  (select ROW_NUMBER() OVER() from broken_equipment) ={i+1} ;")
                #сохранение и закрытие соеденения с бд 
                self.conn.commit()
                self.conn.close()
            #соеденение с бд
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            #запрос на вывод всех данных из таблицы
            cur.execute("""SELECT * FROM equipment_prevention;""")
            col_name = [description[0] for description in cur.description]
            data_rows = cur.fetchall()
            self.conn.close()
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(data_rows):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.setHorizontalHeaderLabels(col_name)
            self.tableWidget.resizeColumnsToContents()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        finally:
            self.conn.close()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        if Equipment_prevention.test == False:
            self.cbColNames.addItems(col_name)
            Equipment_prevention.test = True
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
    def update_tableWidget(self, query="select * from equipment_prevention"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents() 
    def find_for_val(self):
        self.conn = sqlite3.connect('EquipmentRecorder.db')
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_tableWidget(f"select * from equipment_prevention where {col} like '{val}'")


    def menu(self):
        self.conn.close
        hub=Menu()
        widget.addWidget(hub)
        widget.setCurrentIndex(widget.currentIndex()+1)
 
class Equipmentprevention_will_soon(QDialog):
    def __init__(self):
        super(Equipmentprevention_will_soon,self).__init__()
        loadUi("equipmentprevention_will_soon.ui",self)
        db = sqlite3.connect("EquipmentRecorder.db")
        sql = db.cursor()
        self.OpenButton.clicked.connect(self.open_file)
        self.pbFind.clicked.connect(self.find_for_val)
        self.hub.clicked.connect(self.menu)
        self.conn = None

    test = False
    def open_file(self):
        try:
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            cur.execute("DELETE FROM equipmentprevention_will_soon;")
            self.conn.commit()
            self.conn.close()
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            gurantee = cur.execute("""select service_life from  Equipment_more_detailed ;""")
            string1 = ( [ row[0] for row in gurantee.fetchall() ] )
            for i in range(len(string1)):
                self.conn = sqlite3.connect('EquipmentRecorder.db')
                cur = self.conn.cursor()
                cur.execute(f"INSERT INTO equipmentprevention_will_soon(type_equipment, id_equipment, start_of_operation, service_life, Days_end_life) SELECT type_equipment, id, start_of_operation, service_life, ROUND(julianday(DATETIME(start_of_operation, '+{string1[i]} month')) - julianday('now')) FROM Equipment_more_detailed WHERE DATETIME(start_of_operation, '+{string1[i]} month') > CURRENT_TIMESTAMP And  (select ROW_NUMBER() OVER() from broken_equipment) ={i+1};")
                self.conn.commit()
                self.conn.close()
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            cur.execute("""SELECT * FROM equipmentprevention_will_soon ORDER BY Days_end_life;""")
            col_name = [description[0] for description in cur.description]
            data_rows = cur.fetchall()
            self.conn.close()
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(data_rows):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.setHorizontalHeaderLabels(col_name)
            self.tableWidget.resizeColumnsToContents()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        finally:
            self.conn.close()
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        if Equipmentprevention_will_soon.test == False:
            self.cbColNames.addItems(col_name)
            Equipmentprevention_will_soon.test = True
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
    def update_tableWidget(self, query="select * from equipmentprevention_will_soon"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents() 
    def find_for_val(self):
        self.conn = sqlite3.connect('EquipmentRecorder.db')
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_tableWidget(f"select * from equipmentprevention_will_soon where {col} like '{val}'")


    def menu(self):
        self.conn.close
        hub=Menu()
        widget.addWidget(hub)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Place(QDialog):
    def __init__(self):
        super(Place,self).__init__()
        loadUi("place.ui",self)
        self.InnerButton.clicked.connect(self.insert_staff)
        self.OpenButton.clicked.connect(self.open_file)
        self.DeleteButton.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.hub.clicked.connect(self.menu)
        self.conn = None
    test = False
    def open_file(self):
        try:
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from place")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        if Place.test == False:
            self.cbColNames.addItems(col_name)
            Place.test = True
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def update_tableWidget(self, query="select * from place"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def insert_staff(self):

        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into place(name)
            values('{self.wrt1.text()}')""")
            db.commit()
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_tableWidget()

    def delete_staff(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from place where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_tableWidget()
    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_tableWidget(f"select * from place where {col} like '{val}'")

    def menu(self):
        hub=Menu()
        widget.addWidget(hub)
        widget.setCurrentIndex(widget.currentIndex()+1)
class Type_equipments(QDialog):
    def __init__(self):
        super(Type_equipments,self).__init__()
        loadUi("type_equipments.ui",self)
        self.InnerButton.clicked.connect(self.insert_staff)
        self.OpenButton.clicked.connect(self.open_file)
        self.DeleteButton.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.hub.clicked.connect(self.menu)
        self.conn = None
    test = False
    def open_file(self):
        try:
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from type_equipments")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        if Type_equipments.test == False:
            self.cbColNames.addItems(col_name)
            Type_equipments.test = True
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def update_tableWidget(self, query="select * from type_equipments"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def insert_staff(self):

        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into type_equipments(name)
            values('{self.wrt1.text()}')""")
            db.commit()
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_tableWidget()

    def delete_staff(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from type_equipments where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_tableWidget()
    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_tableWidget(f"select * from type_equipments where {col} like '{val}'")

    def menu(self):
        hub=Menu()
        widget.addWidget(hub)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Workers(QDialog):
    def __init__(self):
        super(Workers,self).__init__()
        loadUi("workers.ui",self)
        self.InnerButton.clicked.connect(self.insert_staff)
        self.OpenButton.clicked.connect(self.open_file)
        self.DeleteButton.clicked.connect(self.delete_staff)
        self.pbFind.clicked.connect(self.find_for_val)
        self.hub.clicked.connect(self.menu)
        self.conn = None
    test = False
    def open_file(self):
        try:
            self.conn = sqlite3.connect('EquipmentRecorder.db')
            cur = self.conn.cursor()
            data = cur.execute("select * from workers")
            col_name = [i[0] for i in data.description]
            data_rows = data.fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        self.tableWidget.setRowCount(0)
        if Workers.test == False:
            self.cbColNames.addItems(col_name)
            Workers.test = True
        for i, row in enumerate(data_rows):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def update_tableWidget(self, query="select * from workers"):
        try:
            cur = self.conn.cursor()
            data = cur.execute(query).fetchall()
        except Exception as e:
            print(f"Проблемы с подключением к БД. {e}")
            return e
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        

    def insert_staff(self):

        try:
            cur = self.conn.cursor()
            cur.execute(f"""insert into workers(First_name, Last_name, Patronymic, post)
            values('{self.wrt1.text()}', '{self.wrt2.text()}', '{self.wrt3.text()}', '{self.wrt4.text()}')""")
            db.commit()
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение1: {e}")
            return e
        self.update_tableWidget()

    def delete_staff(self):
        row = self.tableWidget.currentRow()
        num = self.tableWidget.item(row, 0).text()
        try:
            cur = self.conn.cursor()
            cur.execute(f"delete from workers where id = {num}")
            self.conn.commit()
            cur.close()
        except Exception as e:
            print(f"Исключение: {e}")
            return e
        self.update_tableWidget()
    def find_for_val(self):
        val = self.leFind.text()
        col = self.cbColNames.itemText(self.cbColNames.currentIndex())
        self.update_tableWidget(f"select * from workers where {col} like '{val}'")

    def menu(self):
        hub=Menu()
        widget.addWidget(hub)
        widget.setCurrentIndex(widget.currentIndex()+1)






app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(500)
widget.setFixedHeight(500)
widget.show()
app.exec_()