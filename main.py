import os
import sys
import csv
import datetime
from design import *
from tf_recognizer import *
from PyQt5 import QtCore, QtGui, QtWidgets

class BLPR(QtWidgets.QMainWindow):
    data_for_export = []  # Список данных для экспорта
    image_path_global = []  # Список путей к изображениям
    loaded_list_of_nums = []
    
    def __init__(self): # Функция инициализации
        super(BLPR, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.clear_button.clicked.connect(self.clear_legacy)
        self.ui.recognize_num_button.clicked.connect(self.recognize_num)
        self.ui.export_data_button.clicked.connect(self.export_data)
        self.ui.base_of_nums_button.clicked.connect(self.base_of_nums)
        
    def clear_legacy(self): # Функция очистки всей программы
        self.ui.image_place.setPixmap(QtGui.QPixmap(""))
        self.ui.history_legacy.setPlainText("") 
        self.data_for_export = []
        self.loaded_list_of_nums = []
        
    def recognize_num(self): # Функция распознавания номерного знака
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть файл", os.path.join(os.path.expanduser('~'), 'Desktop'), "Форматы изображений (*.jpg *.png *.bmp *.tiff)") # Выбор изображения для дальнейшего распознавания
        if file_name == "":
            QtWidgets.QMessageBox.warning(self, "Предупреждение", self.tr("Вы не выбрали изображение для распознавания!")) # Всплывающее окно предупреждения, если пользователь не выбрал изображение для распознавания
        else:
            detected_num = tf_recognizer_func([file_name])  # Распознавание номера, в виде обращения к функции из файла компилятора модели нейронной сети
            time = datetime.datetime.now().time()  # Получение текущего времени
            self.ui.image_place.setPixmap(QtGui.QPixmap(file_name))  # Отображение выбранного изображения
            current_date = str(datetime.date.today())  # Получение текущей даты
            current_time = time.strftime('%H:%M:%S')  # Получение текущего времени в формате чч:мм:сс
            self.data_for_export.append({"Дата":current_date, "Время":current_time, "Номер":detected_num})  # Добавление данных в список для экспорта
            if self.ui.history_legacy.toPlainText() == "":
                self.ui.history_legacy.insertPlainText(current_date + " " + current_time + " " + detected_num) # Отображает данные в виде: даты, времени, номера в поле с иторией распознаваний
            else:
                self.ui.history_legacy.insertPlainText("\n" + current_date + " " + current_time + " " + detected_num)
            if detected_num in self.loaded_list_of_nums and self.loaded_list_of_nums != []:
                QtWidgets.QMessageBox.information(self, "Информация", self.tr("Данный номер числится в базе. Можно пропускать!"))
            elif detected_num not in self.loaded_list_of_nums and self.loaded_list_of_nums != []:
                QtWidgets.QMessageBox.information(self, "Информация", self.tr("Данный номер не числится в базе."))
            
    def export_data(self): # Экспортируем накопившиеся данные в csv таблицу
        export_path = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить CSV файл", os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), "CSV (*.csv)") # Выбор пути экспорта данных
        if export_path[0] == "":
            QtWidgets.QMessageBox.warning(self, "Предупреждение", self.tr("Вы не выбрали путь для экспорта данных!")) # Всплывающее окно предупреждения, если пользователь не выбрал путь для экспорта данных
        else:
            with open(export_path[0], "w", newline='', encoding='Windows-1251') as csv_file:
                writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=["Дата", "Время", "Номер"])
                writer.writeheader()
                for data in self.data_for_export:
                    writer.writerow(data)
            QtWidgets.QMessageBox.information(self, "Информация", self.tr("Файл был успешно экспортирован!")) # Всплывающее окно

    def base_of_nums(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Загрузить базу с номерами", os.path.join(os.path.expanduser('~'), 'Desktop'), "Формат (*.csv)")
        if file_name == "":
            QtWidgets.QMessageBox.warning(self, "Предупреждение", self.tr("Вы не выбрали базу номеров для импорта!"))
        else:
            with open(file_name, "r") as base_of_nums_file:
                self.loaded_list_of_nums = [nums.strip() for nums in base_of_nums_file]
            QtWidgets.QMessageBox.information(self, "Информация", self.tr("Файл с базой номеров был успешно импортирован!"))
            
if __name__ == "__main__": #Запуск
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MyApp = BLPR()
    MyApp.show()
    sys.exit(app.exec_())
