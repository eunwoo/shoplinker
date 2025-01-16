from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QTreeWidgetItem, QListWidgetItem, QFileDialog, QTableWidgetItem, QAbstractScrollArea, QComboBox, QAbstractItemView, QItemDelegate, QStyledItemDelegate, QLabel, QMessageBox
from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool, Qt, QSortFilterProxyModel
from PySide6.QtGui import QScreen, QPixmap, QIcon
from main_window import Ui_MainWindow
from textout import clearScreen, print_logo
from web_fetch import WEBManipulator
import os
import sys
import configparser
import cryptocode
import traceback
import pickle
import re
import pandas as pd
import xlrd
import winsound as sd
import openpyxl
from collections import OrderedDict
from webdriver_manager.chrome import ChromeDriverManager

PROGRAM_TITLE = '샵링커 카테고리 작업'
VERSION = '0.0.7'
# 11번가 카테고리 가져오기 에러 수정

MADE_BY = "LEW"
ENCRYPT_KEY = "fhfkekjrh2@hdjs"

store_list = ['스마트스토어', '쿠팡', '지마켓', '11번가', '옥션', '카페24']
my_category_column = ['키워드', '스마트스토어키워드','쿠팡키워드', '지마켓키워드', '11번가키워드', '옥션키워드', '카페24키워드', '스마트스토어', '쿠팡', '지마켓', '11번가', '옥션', '카페24']
table_header = ['고객사대분류코드', '고객사대분류명'] + my_category_column
table_header1 = ['고객사대분류코드', '고객사대분류명'] + my_category_column[7:14]
table_header2 = my_category_column[0:7]

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)
    ret = Signal(int)
    retMsg = Signal(str)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        print(self.kwargs)

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['ret_callback'] = self.signals.ret
        self.kwargs['regMsg_callback'] = self.signals.retMsg

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class WrongEasywinnerCode(Exception):
    "잘못된 이지위너 코드입니다"
    pass

class QTableWidgetDisabledItem(QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        print('createEditor')
        # item = QLabel(parent)
        # item.setReadOnly(True)
        # return item
        return None

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setText(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

def beepsound():
    sd.PlaySound("SystemExit", sd.SND_ALIAS)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f'{PROGRAM_TITLE} {VERSION} ■■■■ 만든이 {MADE_BY}')
        self.tabWidget.setCurrentIndex(0)
        self.comboBox.clear()
        self.comboBox.addItems(['스마트스토어','쿠팡','지마켓', '11번가', '옥션', '카페24'])

        # Load the image
        pixmap = QPixmap("shoplinker_logo.png")  # Replace with your actual image path

        # Create an icon from the image
        icon = QIcon(pixmap)

        # Set the icon on the button
        self.pushButton_20.setIcon(icon)

        # Optionally, set the icon size
        self.pushButton_20.setIconSize(pixmap.rect().size())

        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(self.get_category_thread_run)
        self.pushButton_2.clicked.connect(self.save)
        self.pushButton_3.clicked.connect(self.load)
        self.pushButton_4.clicked.connect(self.expand_all)
        self.pushButton_5.clicked.connect(self.test)
        self.pushButton_6.clicked.connect(self.pause_handler)
        self.pushButton_7.clicked.connect(self.search)
        self.pushButton_8.clicked.connect(self.save_category_match)
        self.pushButton_9.clicked.connect(self.get_first_category_thread_run)
        self.pushButton_10.clicked.connect(self.open_file)
        self.pushButton_11.clicked.connect(self.delete_all)
        self.pushButton_12.clicked.connect(self.collapse_all)
        self.pushButton_13.clicked.connect(self.select_data_folder)
        self.pushButton_14.clicked.connect(self.open_data_folder)
        self.pushButton_15.clicked.connect(self.select_easywinner_excel)
        self.pushButton_16.clicked.connect(self.open_easywinner_excel)
        self.pushButton_17.clicked.connect(self.search_keyword_reset)
        self.pushButton_18.clicked.connect(self.delete_my_category_selected_row)
        self.pushButton_19.clicked.connect(self.delete_my_category_all)
        self.pushButton_20.clicked.connect(self.register_thread_run)
        self.pushButton_21.clicked.connect(self.delete_search_result)
        self.pushButton_22.clicked.connect(self.delete_matched_category_one_mall_in_search_tab)
        self.pushButton_23.clicked.connect(self.register_my_category_selected_thread_run)
        self.pushButton_24.clicked.connect(self.search_keyword)
        self.pushButton_25.clicked.connect(self.ascending_order)
        self.pushButton_26.clicked.connect(self.register_my_category_all_thread_run)
        self.pushButton_27.clicked.connect(self.delete_my_category_selected_cell)
        self.lineEdit_3.returnPressed.connect(self.search_enter)
        self.lineEdit_6.returnPressed.connect(self.search_keyword)
        self.listWidget.itemSelectionChanged.connect(self.list_level1_click)
        self.listWidget_2.itemSelectionChanged.connect(self.list_level2_click)
        self.listWidget_3.itemSelectionChanged.connect(self.list_level3_click)
        self.listWidget_4.itemSelectionChanged.connect(self.list_level4_click)
        self.listWidget_5.itemSelectionChanged.connect(self.list_level5_click)
        self.listWidget_6.itemSelectionChanged.connect(self.list_level6_click)
        self.listWidget_7.itemSelectionChanged.connect(self.list_level7_click)
        self.listWidget_8.itemSelectionChanged.connect(self.list_level8_click)
        self.listWidget_11.itemSelectionChanged.connect(self.search_result_select_smartstore)
        self.listWidget_12.itemSelectionChanged.connect(self.search_result_select_coupang)
        self.listWidget_13.itemSelectionChanged.connect(self.search_result_select_gmarket)
        self.listWidget_10.itemSelectionChanged.connect(self.search_result_select_11st)
        self.listWidget_14.itemSelectionChanged.connect(self.search_result_select_auction)
        self.listWidget_15.itemSelectionChanged.connect(self.search_result_select_interpark)
        self.comboBox.currentTextChanged.connect(self.category_maker_changed)
        self.checkBox.toggled.connect(self.easywinner_code_show_toggle)

        self.pause = {'state':False}
        self.save_my_category_enabled = True

        # 내 카테고리
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(15)
        self.tableWidget.setHorizontalHeaderLabels(table_header)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for idx in range(15):
            if idx >= 2 and idx <= 8:# 키워드는 편집 가능
                continue
            self.tableWidget.setItemDelegateForColumn(idx, QTableWidgetDisabledItem(self.tableWidget))
        self.tableWidget.itemChanged.connect(self.tableWidget_itemchanged)

        # 검색탭 매칭 테이블1 (카테고리)
        self.tableWidget_2.setRowCount(1)
        self.tableWidget_2.setColumnCount(8)
        self.tableWidget_2.setHorizontalHeaderLabels(table_header1)
        self.tableWidget_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.comboBox_code = QComboBox()
        self.tableWidget_2.setCellWidget(0, 0, self.comboBox_code)
        # self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for idx in range(8):
            self.tableWidget_2.setItemDelegateForColumn(idx, QTableWidgetDisabledItem(self.tableWidget_2))
        self.tableWidget_2.itemChanged.connect(self.tableWidget_2_itemchanged)
        horizontalHeader = self.tableWidget_2.horizontalHeader()
        # resize the first column to 100 pixels
        horizontalHeader.resizeSection(0, 200)
        self.comboBox_code.currentTextChanged.connect(self.search_selected_code_changed)

        # 검색탭 매칭 테이블2 (키워드)
        self.tableWidget_3.setRowCount(1)
        self.tableWidget_3.setColumnCount(7)
        self.tableWidget_3.setHorizontalHeaderLabels(table_header2)
        self.tableWidget_3.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.threadpool = QThreadPool()

        self.my_category = pd.DataFrame()
        self.my_category_with_code = pd.DataFrame()
        self.category = {}
        self.my_category_selected = {}
        self.df_easywinner = pd.DataFrame()

        # load config
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='UTF-8')
        try:
            self.lineEdit.setText(config['DEFAULT']['id'])
            self.lineEdit_2.setText(cryptocode.decrypt(config['DEFAULT']['password'], ENCRYPT_KEY))
            self.lineEdit_4.setText(config['DEFAULT']['data_folder'])
            self.lineEdit_5.setText(config['DEFAULT']['easywinner_excel'])
            self.lineEdit_7.setText(config['DEFAULT']['loading_wait_time'])
            # rect = self.geometry()
            # self.setGeometry(rect.left, rect.top, int(config['DEFAULT']['width']), int(config['DEFAULT']['height']))
            self.resize(int(config['DEFAULT']['width']), int(config['DEFAULT']['height']))
            if config['DEFAULT']['easywinner_code_show_all'] == '1':
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
        except Exception as e:
            print('exception when loading config')
            print(e)
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_7.setText('4')

        driver_path = ChromeDriverManager().install()
        print(driver_path)
        print(os.path.dirname(driver_path).split("\\"))
        self.label_13.setText(os.path.dirname(driver_path).split("\\")[-2])

        self.load()
        self.easywinner_code_show_toggle()

    def tableWidget_itemchanged(self, item):
        if item.column() >= 2 and item.column() <= 8:
            column_name = self.tableWidget.horizontalHeaderItem(item.column()).text()
            category_code = self.tableWidget.item(item.row(), 0).text()
            self.my_category.loc[category_code,column_name] = self.tableWidget.item(item.row(), item.column()).text()
            self.my_category_with_code.loc[category_code,column_name] = self.tableWidget.item(item.row(), item.column()).text()
            if self.save_my_category_enabled:
                self.save_my_category_to_file()
            self.easywinner_code_show_toggle()

    def tableWidget_2_itemchanged(self, item):
        # print('tableWidget_2_itemchanged')
        # print(item.row(), item.column())
        # print(item.text())
        pass

    def delete_my_category_selected_row(self):
        print('delete_my_category_selected_row')
        selected_rows = []
        for item in self.tableWidget.selectedIndexes():
            if item.row() not in selected_rows:
                selected_rows.append(item.row())
        for row in reversed(selected_rows):
            code = self.tableWidget.item(row, 0).text()
            self.tableWidget.removeRow(row)
            self.my_category_with_code.drop(code, inplace=True)
            self.my_category.drop(code, inplace=True)
        self.save_my_category_to_file()
        self.easywinner_code_show_toggle()

    def delete_my_category_selected_cell(self):
        for item in self.tableWidget.selectedIndexes():
            code = self.tableWidget.item(item.row(), 0).text()
            self.tableWidget.takeItem(item.row(), item.column())
            column_name = self.tableWidget.horizontalHeaderItem(item.column()).text()
            self.my_category_with_code.loc[code][column_name] = ''
            self.my_category.loc[code][column_name] = ''
        self.save_my_category_to_file()
        self.easywinner_code_show_toggle()

    def delete_my_category_all(self):
        msgBox = QMessageBox()
        msgBox.setText("전체 삭제를 진행할까요?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msgBox.exec()
        if ret == QMessageBox.Ok:
            self.my_category = pd.DataFrame(columns=my_category_column)
            self.my_category_with_code = pd.DataFrame(columns=my_category_column)
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(table_header)
            self.save_my_category_to_file()

    def delete_search_result(self):
        self.listWidget_11.clear()
        self.listWidget_12.clear()
        self.listWidget_13.clear()
        self.listWidget_10.clear()
        self.listWidget_14.clear()
        self.listWidget_15.clear()

    def search_keyword(self):
        print('search_keyword')
        filter_text = self.lineEdit_6.text()
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(i, j)
                match = filter_text.lower() not in item.text().lower()
                self.tableWidget.setRowHidden(i, match)
                if not match:
                    break
    
    def search_keyword_reset(self):
        print('search_keyword_reset')
        self.lineEdit_6.setText('')
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHidden(i, False)

    def ascending_order(self):
        print('ascending_order')
        self.tableWidget.sortItems(self.tableWidget.currentColumn(), Qt.AscendingOrder)

    def easywinner_code_show_toggle(self):
        # print('easywinner_code_show_toggle')
        try:
            if self.checkBox.isChecked():
                category_code = []
                for code in self.df_easywinner.index.tolist():
                    category_code.append(str(code))
                self.comboBox_code.clear()
                self.comboBox_code.addItems(category_code)
                self.comboBox_code.setCurrentIndex(0)
            else:
                category_code = []
                for code in self.df_easywinner.index.tolist():
                    if code not in self.my_category.index:
                        category_code.append(str(code))
                self.comboBox_code.clear()
                self.comboBox_code.addItems(category_code)
                self.comboBox_code.setCurrentIndex(0)
            self.tableWidget_2.resizeColumnsToContents()
            horizontalHeader = self.tableWidget_2.horizontalHeader()
            horizontalHeader.resizeSection(0, 200)
        except AttributeError as e:
            print(e)
            print('AttributeError')



    def select_easywinner_excel(self):
        dlg = QFileDialog()
        name, filter = dlg.getOpenFileName(self)
        if name:
            self.lineEdit_5.setText(name)

    def select_data_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.lineEdit_4.setText(folder)

    def open_easywinner_excel(self):
        os.system('start excel.exe "%s"' % (self.lineEdit_5.text(), ))

    def open_data_folder(self):
        path = self.lineEdit_4.text()
        path = os.path.realpath(path)
        os.startfile(path)

    def load_easywinner_excel(self):
        filename = self.lineEdit_5.text()
        try:
            wb = xlrd.open_workbook(filename, ignore_workbook_corruption=True, formatting_info=True)
            self.df_easywinner = pd.read_excel(wb, index_col=4)
            self.df_easywinner = self.df_easywinner.fillna('')
            if '고객사' not in self.category:
                self.category['고객사'] = {}
            for index, row in self.df_easywinner.iterrows():
                self.category['고객사'][row['대분류명']] = {}
            self.easywinner_code_show_toggle()

        except FileNotFoundError:
            print('이지위너 엑셀 파일 설정안됨. 이지위너 엑셀 파일을 설정해주시기 바랍니다.')

    def search_selected_code_changed(self):
        # print('search_selected_code_changed', self.comboBox_code.count())
        if self.comboBox_code.count() == 0:
            return
        code = self.comboBox_code.currentText()
        if code == '':
            return

        easywinner = QTableWidgetItem(self.df_easywinner.loc[code]['대분류명'])
        keyword = OrderedDict()
        storeTableItem = OrderedDict()
        if code in self.my_category_with_code.index:
            item_str = self.my_category.loc[code]['키워드']
            keyword['공통'] = QTableWidgetItem(item_str)

            for store in store_list:
                item_str = self.my_category.loc[code][f'{store}키워드']
                keyword[store] = QTableWidgetItem(str(item_str))

                item_str = self.search_result_selected_string_format(self.my_category.loc[code][store])
                storeTableItem[store] = QTableWidgetItem(item_str)
                self.my_category_selected[store] = self.my_category_with_code.loc[code][store]
        else:
            keyword['공통'] = QTableWidgetItem('')
            for store in store_list:
                self.my_category_selected[store] = ''
                keyword[store] = QTableWidgetItem('')
                storeTableItem[store] = QTableWidgetItem('')
        self.tableWidget_2.setItem(0, 1, easywinner)

        for idx, (store, item) in enumerate(storeTableItem.items()):
            self.tableWidget_2.setItem(0, idx+2, item)
        for idx, (store, item) in enumerate(keyword.items()):
            self.tableWidget_3.setItem(0, idx, item)

        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_3.resizeColumnsToContents()


    def load_my_category(self):
        filename = self.lineEdit_4.text() + '/my_category.xlsx'
        print(f'load_my_category: {filename}')
        try:
            self.my_category = pd.read_excel(filename, sheet_name='Sheet1', index_col=0, dtype={'키워드': str, '스마트스토어키워드': str, '쿠팡키워드': str, '지마켓키워드': str, '11번가키워드': str, '옥션키워드': str, '인터파크키워드': str})
            self.my_category = self.my_category[~self.my_category.index.duplicated(keep='first')]
            self.my_category = self.my_category.fillna('')
            self.my_category.index = self.my_category.index.map(str)
            # self.my_category.drop(['Unnamed: 0'], axis = 1, inplace = True)

            self.my_category_with_code = pd.read_excel(filename, sheet_name='Sheet2', index_col=0, dtype={'키워드': str, '스마트스토어키워드': str, '쿠팡키워드': str, '지마켓키워드': str, '11번가키워드': str, '옥션키워드': str, '인터파크키워드': str})
            self.my_category_with_code = self.my_category_with_code[~self.my_category_with_code.index.duplicated(keep='first')]
            self.my_category_with_code = self.my_category_with_code.fillna('')
            self.my_category_with_code.index = self.my_category_with_code.index.map(str)
            # self.my_category_with_code.drop(['Unnamed: 0'], axis = 1, inplace = True)

            try:
                self.display_my_category()
            except:
                pass
        except FileNotFoundError:
            print('not found')
            pass

    def delete_all(self):
        self.category = {}
        self.treeWidget.clear()
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        self.listWidget_4.clear()
        self.listWidget_5.clear()
        self.listWidget_6.clear()
        self.listWidget_7.clear()
        self.listWidget_8.clear()
        self.listWidget_9.clear()

    def open_file(self):
        filedialog = QFileDialog()
        if filedialog.exec():
            filename = filedialog.selectedFiles()[0]
            with open(filename,"rb") as fr:
                self.category = pickle.load(fr)
            self.treeWidget.setColumnCount(2)
            category_maker = list(self.category.keys())[0]
            self.comboBox.setCurrentText(category_maker)
            self.change_category_maker(category_maker)

    def pause_handler(self):
        print('pause_handler')
        self.pause['state'] = True

    def save(self):
        for k1, v1 in self.category.items():
            if k1 == '고객사':
                print('고객사는 저장하지 않습니다')
                continue
            if isinstance(self.category[k1], dict):
                for k2, v2 in self.category[k1].items():
                    k2_filename = re.sub(r'\(.*\)', '', k2) # 괄호안에 긴 숫자가 있는 것을 삭제
                    # with open(f"{self.lineEdit_4.text()}/data - {k1} - {k2_filename.replace('/','／')}.pickle","wb") as fw:
                    with open(f"data - {k1} - {k2_filename.replace('/','／')}.pickle","wb") as fw:
                        category = {}
                        category[k1] = {}
                        category[k1][k2] = self.category[k1][k2]
                        pickle.dump(category, fw)
                        print(f"data - {k1} - {k2_filename.replace('/','／')}.pickle was saved")

    def load_file(self, filename):
        print(f'load_file: {filename}')
        try:
            with open(filename,"rb") as fr:
                category_sub = pickle.load(fr)
                for k1, v1 in category_sub.items():
                    if k1 not in self.category:
                        self.category[k1] = {}
                    for k2, v2 in category_sub[k1].items():
                        if len(list(v2.keys())) > 0:
                            self.category[k1][k2] = v2
                        else:
                            # v2가 key를 가지고 있지 않아도 빈 목록을 만듬
                            self.category[k1][k2] = {}

            self.treeWidget.setColumnCount(2)
            category_maker = list(self.category.keys())[0]
            self.comboBox.setCurrentText(category_maker)
            self.change_category_maker(category_maker)
        except FileNotFoundError:
            self.category = {}

    def load_folder(self, folder):
        try:
            for file in os.listdir(folder):
                if "pickle" in file:
                    self.load_file(folder + '/' + file)
        except FileNotFoundError:
            print('데이터 폴더 설정 안됨. 데이터 로딩 안함.')

    def load(self):
        folder = self.lineEdit_4.text()
        self.load_folder(folder)
        self.load_easywinner_excel()
        self.load_my_category()

    def search_enter(self):
        self.search()

    def search_code(self, code):
        try:
            index = self.comboBox_code.findText(code, Qt.MatchFlag.MatchContains)
            if index != -1:
                self.comboBox_code.setCurrentIndex(index)
            code_int = int(code)
        except:
            pass
    def search_sub(self, dict_val, upper_group_name, search_what, upper_group_name_with_code):
        if isinstance(dict_val, dict):
            for k, v in dict_val.items():
                if isinstance(dict_val[k], dict) and len(dict_val[k]) == 0:
                    # if any([re.search(r'\b'+search_what+r'\b', text) for text in k.split('>')]):
                    # if any([re.search(r'\b'+search_what, text) for text in k.split('>')]):
                    if any([re.search(search_what, text) for text in (upper_group_name_with_code+'>'+k).split('>')]):
                        if upper_group_name.split('>')[0] == '스마트스토어':
                            self.listWidget_11.addItems([upper_group_name+'>'+ re.sub(r'\(\d+\)', '', k)])
                            self.search_result['스마트스토어'].append(upper_group_name_with_code+'>'+k)
                        elif upper_group_name.split('>')[0] == '쿠팡':
                            self.listWidget_12.addItems([upper_group_name+'>'+ re.sub(r'\(\d+\)', '', k)])
                            self.search_result['쿠팡'].append(upper_group_name_with_code+'>'+k)
                        elif upper_group_name.split('>')[0] == '지마켓':
                            self.listWidget_13.addItems([upper_group_name+'>'+ re.sub(r'\(\d+\)', '', k)])
                            self.search_result['지마켓'].append(upper_group_name_with_code+'>'+k)
                        elif upper_group_name.split('>')[0] == '11번가':
                            self.listWidget_10.addItems([upper_group_name+'>'+ re.sub(r'\(\d+\)', '', k)])
                            self.search_result['11번가'].append(upper_group_name_with_code+'>'+k)
                        elif upper_group_name.split('>')[0] == '옥션':
                            self.listWidget_14.addItems([upper_group_name+'>'+ re.sub(r'\(\d+\)', '', k)])
                            self.search_result['옥션'].append(upper_group_name_with_code+'>'+k)
                        elif upper_group_name.split('>')[0] == '카페24':
                            self.listWidget_15.addItems([upper_group_name+'>'+ re.sub(r'\(.*\)', '', k)])
                            self.search_result['카페24'].append(upper_group_name_with_code+'>'+k)
                else:
                    self.search_sub(dict_val[k], upper_group_name+'>'+re.sub(r'\(.*\)', '', k), search_what, upper_group_name_with_code+'>'+k)

    def search_result_selected_string_format(self, str):
        return '>'.join(str.split('>')[-2:])

    def search_result_select_smartstore(self):
        print('search_result_select_smartstore')
        item_text = self.search_result_selected_string_format(self.listWidget_11.selectedItems()[0].text())
        item = QTableWidgetItem(item_text)
        self.tableWidget_2.setItem(0, 2, item)
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_3.setItem(0, 1, QTableWidgetItem(item_text.split('>')[-1]))
        self.tableWidget_3.setItem(0, 0, QTableWidgetItem(self.lineEdit_3.text()))
        self.my_category_selected['스마트스토어'] = self.search_result['스마트스토어'][self.listWidget_11.currentIndex().row()]

    def search_result_select_coupang(self):
        print('search_result_select_coupang')
        item_text = self.search_result_selected_string_format(self.listWidget_12.selectedItems()[0].text())
        item = QTableWidgetItem(item_text)
        self.tableWidget_2.setItem(0, 3, item)
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_3.setItem(0, 2, QTableWidgetItem(item_text.split('>')[-1]))
        self.tableWidget_3.setItem(0, 0, QTableWidgetItem(self.lineEdit_3.text()))
        self.my_category_selected['쿠팡'] = self.search_result['쿠팡'][self.listWidget_12.currentIndex().row()]

    def search_result_select_gmarket(self):
        print('search_result_select_gmarket')
        item_text = self.search_result_selected_string_format(self.listWidget_13.selectedItems()[0].text())
        item = QTableWidgetItem(item_text)
        self.tableWidget_2.setItem(0, 4, item)
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_3.setItem(0, 3, QTableWidgetItem(item_text.split('>')[-1]))
        self.tableWidget_3.setItem(0, 0, QTableWidgetItem(self.lineEdit_3.text()))
        self.my_category_selected['지마켓'] = self.search_result['지마켓'][self.listWidget_13.currentIndex().row()]

    def search_result_select_11st(self):
        print('search_result_select_11st')
        item_text = self.search_result_selected_string_format(self.listWidget_10.selectedItems()[0].text())
        item = QTableWidgetItem(item_text)
        self.tableWidget_2.setItem(0, 5, item)
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_3.setItem(0, 4, QTableWidgetItem(item_text.split('>')[-1]))
        self.tableWidget_3.setItem(0, 0, QTableWidgetItem(self.lineEdit_3.text()))
        self.my_category_selected['11번가'] = self.search_result['11번가'][self.listWidget_10.currentIndex().row()]

    def search_result_select_auction(self):
        print('search_result_select_auction')
        item_text = self.search_result_selected_string_format(self.listWidget_14.selectedItems()[0].text())
        item = QTableWidgetItem(item_text)
        self.tableWidget_2.setItem(0, 6, item)
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_3.setItem(0, 5, QTableWidgetItem(item_text.split('>')[-1]))
        self.tableWidget_3.setItem(0, 0, QTableWidgetItem(self.lineEdit_3.text()))
        self.my_category_selected['옥션'] = self.search_result['옥션'][self.listWidget_14.currentIndex().row()]

    def search_result_select_interpark(self):
        print('search_result_select_interpark')
        item_text = self.search_result_selected_string_format(self.listWidget_15.selectedItems()[0].text())
        item = QTableWidgetItem(item_text)
        self.tableWidget_2.setItem(0, 7, item)
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_3.setItem(0, 6, QTableWidgetItem(item_text.split('>')[-1]))
        self.tableWidget_3.setItem(0, 0, QTableWidgetItem(self.lineEdit_3.text()))
        self.my_category_selected['카페24'] = self.search_result['카페24'][self.listWidget_15.currentIndex().row()]

    def search(self):
        print('검색 시작')
        search_what = self.lineEdit_3.text()
        self.search_result = {}
        self.search_result['스마트스토어'] = []
        self.search_result['쿠팡'] = []
        self.search_result['지마켓'] = []
        self.search_result['11번가'] = []
        self.search_result['옥션'] = []
        self.search_result['카페24'] = []
        self.listWidget_11.clear()
        self.listWidget_12.clear()
        self.listWidget_13.clear()
        self.listWidget_10.clear()
        self.listWidget_14.clear()
        self.listWidget_15.clear()
        for k1, v1 in self.category.items():    # k1 = category maker
            self.search_sub(self.category[k1], k1, search_what, k1)
        self.search_code(search_what)

    def delete_matched_category_one_mall_in_search_tab(self):
        for item in self.tableWidget_3.selectedItems():
            item.setText('')
            self.my_category_selected[self.tableWidget_3.horizontalHeaderItem(item.column()).text()] = ''

    def register_my_category_selected_thread_run(self):
        print('register_my_category_selected_thread_run')
        # Pass the function to execute
        worker = Worker(self.register_my_category_selected, pause=self.pause) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.thread_result)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn_get_category)

        # Execute
        self.threadpool.start(worker)

    def register_my_category_all_thread_run(self):
        print('register_my_category_selected_thread_run')
        # Pass the function to execute
        worker = Worker(self.register_my_category_all, pause=self.pause) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.thread_result)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn_get_category)

        # Execute
        self.threadpool.start(worker)

    def register_thread_run(self):
        print('register_thread_run')
        # Pass the function to execute
        worker = Worker(self.register, pause=self.pause) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.thread_result)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn_get_category)

        # Execute
        self.threadpool.start(worker)

    def change_category_maker(self, category_maker):
        self.treeWidget.clear()
        if category_maker in self.category:
            items = []
            for k1, v1 in self.category[category_maker].items():
                item = QTreeWidgetItem([re.sub(r'\(\d+\)','',k1)])
                if isinstance(self.category[category_maker][k1], dict):
                    for k2, v2 in self.category[category_maker][k1].items():
                        child = QTreeWidgetItem([re.sub(r'\(\d+\)','',k2)])
                        item.addChild(child)
                        if isinstance(self.category[category_maker][k1][k2], dict):
                            for k3, v3 in self.category[category_maker][k1][k2].items():
                                child1 = QTreeWidgetItem([re.sub(r'\(\d+\)','',k3)])
                                child.addChild(child1)
                                if isinstance(self.category[category_maker][k1][k2][k3], dict):
                                    for k4, v4 in self.category[category_maker][k1][k2][k3].items():
                                        child2 = QTreeWidgetItem([re.sub(r'\(\d+\)','',k4)])
                                        child1.addChild(child2)
                items.append(item)
            self.treeWidget.insertTopLevelItems(0, items)
            self.treeWidget.setColumnWidth(0, 400)
            self.treeWidget.setColumnWidth(1, 300)

        # list view
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        self.listWidget_4.clear()
        if category_maker in self.category:
            self.listitem_to_key1 = []
            self.comboBox_2.clear()
            self.comboBox_2.addItem('전체')
            for k1, v1 in self.category[category_maker].items():
                self.listitem_to_key1.append(k1)
                self.listWidget.addItem(re.sub(r'\(.*\)','',k1))
                self.comboBox_2.addItem(re.sub(r'\(.*\)','',k1))
        else:
            self.comboBox_2.clear()

    def category_maker_changed(self):
        print('category_maker_changed')
        category_maker = self.comboBox.currentText()
        self.change_category_maker(category_maker)

    def expand_all(self):
        self.treeWidget.expandAll()
    def collapse_all(self):
        self.treeWidget.collapseAll()

    def list_level1_click(self):
        print('list_level1_click')
        category_maker = self.comboBox.currentText()

        item = self.listWidget.currentIndex().row()
        self.list_k1 = self.listitem_to_key1[item]
        self.listWidget_2.clearSelection()
        self.listWidget_2.clear()
        self.listWidget_3.clearSelection()
        self.listWidget_3.clear()
        self.listWidget_4.clear()
        if category_maker not in self.category:
            return
        self.listitem_to_key2 = []
        for k1, v1 in self.category[category_maker][self.list_k1].items():
            self.listitem_to_key2.append(k1)
            self.listWidget_2.addItem(re.sub(r'\(.*\)','',k1))
        
    def list_level2_click(self):
        print('list_level2_click')
        category_maker = self.comboBox.currentText()
        
        item = self.listWidget_2.selectedItems()
        self.listWidget_3.clearSelection()
        self.listWidget_3.clear()
        self.listWidget_4.clear()
        if len(item) == 0:
            return
        item = self.listWidget_2.currentIndex().row()
        self.list_k2 = self.listitem_to_key2[item]
        self.listitem_to_key3 = []
        for k1, v1 in self.category[category_maker][self.list_k1][self.list_k2].items():
            self.listitem_to_key3.append(k1)
            self.listWidget_3.addItem(re.sub(r'\(.*\)','',k1))

    def list_level3_click(self):
        print('list_level3_click')
        category_maker = self.comboBox.currentText()

        item = self.listWidget_3.selectedItems()
        self.listWidget_4.clear()
        if len(item) == 0:
            return
        item = self.listWidget_3.currentIndex().row()
        self.list_k3 = self.listitem_to_key3[item]
        self.listitem_to_key4 = []
        for k1, v1 in self.category[category_maker][self.list_k1][self.list_k2][self.list_k3].items():
            self.listitem_to_key4.append(k1)
            self.listWidget_4.addItem(re.sub(r'\(.*\)','',k1))

    def list_level4_click(self):
        print('list_level4_click')
        category_maker = self.comboBox.currentText()

        item = self.listWidget_4.selectedItems()
        self.listWidget_5.clear()
        if len(item) == 0:
            return
        item = self.listWidget_4.currentIndex().row()
        self.list_k4 = self.listitem_to_key4[item]
        self.listitem_to_key5 = []
        for k1, v1 in self.category[category_maker][self.list_k1][self.list_k2][self.list_k3][self.list_k4].items():
            self.listitem_to_key5.append(k1)
            self.listWidget_5.addItem(re.sub(r'\(.*\)','',k1))

    def list_level5_click(self):
        print('list_level5_click')
        category_maker = self.comboBox.currentText()

        item = self.listWidget_5.selectedItems()
        self.listWidget_6.clear()
        if len(item) == 0:
            return
        item = self.listWidget_5.currentIndex().row()
        self.list_k5 = self.listitem_to_key5[item]
        self.listitem_to_key6 = []
        for k1, v1 in self.category[category_maker][self.list_k1][self.list_k2][self.list_k3][self.list_k4][self.list_k5].items():
            self.listitem_to_key6.append(k1)
            self.listWidget_6.addItem(re.sub(r'\(\d+\)','',k1))

    def list_level6_click(self):
        print('list_level6_click')
        category_maker = self.comboBox.currentText()

        item = self.listWidget_6.selectedItems()
        self.listWidget_7.clear()
        if len(item) == 0:
            return
        item = self.listWidget_6.currentIndex().row()
        self.list_k6 = self.listitem_to_key6[item]
        self.listitem_to_key7 = []
        for k1, v1 in self.category[category_maker][self.list_k1][self.list_k2][self.list_k3][self.list_k4][self.list_k5][self.list_k6].items():
            self.listitem_to_key7.append(k1)
            self.listWidget_7.addItem(re.sub(r'\(\d+\)','',k1))

    def list_level7_click(self):
        print('list_level7_click')
        category_maker = self.comboBox.currentText()

        item = self.listWidget_7.selectedItems()
        self.listWidget_8.clear()
        if len(item) == 0:
            return
        item = self.listWidget_7.currentIndex().row()
        self.list_k7 = self.listitem_to_key7[item]
        self.listitem_to_key8 = []
        for k1, v1 in self.category[category_maker][self.list_k1][self.list_k2][self.list_k3][self.list_k4][self.list_k5][self.list_k6][self.list_k7].items():
            self.listitem_to_key8.append(k1)
            self.listWidget_8.addItem(re.sub(r'\(\d+\)','',k1))

    def list_level8_click(self):
        print('list_level8_click')
        category_maker = self.comboBox.currentText()

        item = self.listWidget_8.selectedItems()
        self.listWidget_9.clear()
        if len(item) == 0:
            return
        item = self.listWidget_8.currentIndex().row()
        self.list_k8 = self.listitem_to_key8[item]
        for k1, v1 in self.category[category_maker][self.list_k1][self.list_k2][self.list_k3][self.list_k4][self.list_k5][self.list_k6][self.list_k7][self.list_k8].items():
            self.listWidget_9.addItem(re.sub(r'\(\d+\)','',k1))

    def program_exit(self):
        config = configparser.ConfigParser()
        config['DEFAULT']['id'] = self.lineEdit.text()
        config['DEFAULT']['password'] = cryptocode.encrypt(self.lineEdit_2.text(), ENCRYPT_KEY)
        config['DEFAULT']['data_folder'] = self.lineEdit_4.text()
        config['DEFAULT']['easywinner_excel'] = self.lineEdit_5.text()
        config['DEFAULT']['width'] = str(self.width())
        config['DEFAULT']['height'] = str(self.height())
        config['DEFAULT']['loading_wait_time'] = self.lineEdit_7.text()
        if self.checkBox.isChecked():
            config['DEFAULT']['easywinner_code_show_all'] = '1'
        else:
            config['DEFAULT']['easywinner_code_show_all'] = '0'
        with open('config.ini', 'w', encoding='UTF-8') as configfile:
            config.write(configfile)

    def closeEvent(self, event):
        print('closing')
        self.program_exit()

    def thread_result(self, s):
        print('thread_result')

    def thread_result_get_category(self, s):
        for key, value in s.items():
            print(key)
            for key1, value1 in s[key].items():
                print(key1)
                if key not in self.category:
                    self.category[key] = {}
                self.category[key][key1] = value1
        category_maker = self.comboBox.currentText()
        self.change_category_maker(category_maker)
        # self.save()
        # print(self.category)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def thread_complete_get_category(self):
        print("THREAD COMPLETE!")

    def progress_fn_get_category(self, n):
        print("%d%% done" % n)

    def get_first_category_thread_run(self):
        print('get_first_category_thread_run')
        # Pass the function to execute
        worker = Worker(self.get_first_category, pause=self.pause) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.thread_result_get_category)
        worker.signals.finished.connect(self.thread_complete_get_category)
        worker.signals.progress.connect(self.progress_fn_get_category)

        # Execute
        self.threadpool.start(worker)

    def get_category_thread_run(self):
        print('get_category_thread_run')
        # Pass the function to execute
        worker = Worker(self.get_category, pause=self.pause) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.thread_result_get_category)
        worker.signals.finished.connect(self.thread_complete_get_category)
        worker.signals.progress.connect(self.progress_fn_get_category)

        # Execute
        self.threadpool.start(worker)

    def register(self, progress_callback, ret_callback, regMsg_callback, pause=False):
        print('register')
        clearScreen()
        print_logo(PROGRAM_TITLE, VERSION)
        x = 0
        y = 0
        grid_w = 1200
        grid_h = 800
        download_folder = '.'

        w = WEBManipulator([x,y], [grid_w,grid_h], download_folder, int(self.lineEdit_7.text()), headless=False)
        
        login_url = 'https://ad2.shoplinker.co.kr/index.php'
        if w.login_shoplinker(login_url, id=self.lineEdit.text(), password=self.lineEdit_2.text()) == False:
            print('에러')
            return '로그인 에러'

        w.goto_category_mapping()
        
        print(self.tableWidget_2.cellWidget(0, 0).currentText())
        code = self.tableWidget_2.cellWidget(0, 0).currentText()

        if '스마트스토어' in self.my_category_selected:
            smartstore = self.my_category_selected['스마트스토어']
        else:
            smartstore = ""
        if '쿠팡' in self.my_category_selected:
            coupang = self.my_category_selected['쿠팡']
        else:
            coupang = ""
        
        if '지마켓' in self.my_category_selected:
            gmarket = self.my_category_selected['지마켓']
        else:
            gmarket = ""

        if '11번가' in self.my_category_selected:
            m11st = self.my_category_selected['11번가']
        else:
            m11st = ""

        if '옥션' in self.my_category_selected:
            auction = self.my_category_selected['옥션']
        else:
            auction = ""

        if '카페24' in self.my_category_selected:
            interpark = self.my_category_selected['카페24']
        else:
            interpark = ""

        print('code:', code)
        print('smartstore:', smartstore)
        print('coupang:', coupang)
        print('gmarket:', gmarket)
        print('11st:', m11st)
        print('auction:', auction)
        print('interpark:', interpark)

        w.register(code, 
                    smartstore, 
                    coupang, 
                    gmarket,
                    m11st,
                    auction,
                    interpark)
        return {"result":"완료"}

    # 샵링커로 포팅
    def register_my_category_selected(self, progress_callback, ret_callback, regMsg_callback, pause=False):
        print('register_my_category_selected')

        print(self.my_category)
        categories_to_upload = {}
        selected_rows = []
        for item in self.tableWidget.selectedItems():
            if item.row() not in selected_rows:
                selected_rows.append(item.row())

        for row in selected_rows:
            categories_to_upload[self.tableWidget.item(row, 0).text()] = self.my_category_with_code.loc[self.tableWidget.item(row, 0).text()].to_dict()

        clearScreen()
        print_logo(PROGRAM_TITLE, VERSION)
        x = 0
        y = 0
        grid_w = 1200
        grid_h = 800
        download_folder = '.'

        w = WEBManipulator([x,y], [grid_w,grid_h], download_folder, int(self.lineEdit_7.text()), headless=False)
        
        login_url = 'https://ad2.shoplinker.co.kr/index.php'
        if w.login_shoplinker(login_url, id=self.lineEdit.text(), password=self.lineEdit_2.text()) == False:
            print('에러')
            return '로그인 에러'

        w.goto_category_mapping()

        for k, v in categories_to_upload.items():
            # easywinner = self.search_easywinner_category_code(k)
            w.register(k, 
                        v['스마트스토어'], 
                        v['쿠팡'], 
                        v['지마켓'], 
                        v['11번가'], 
                        v['옥션'], 
                        v['카페24'], 
                    )
        return {"result":"완료"}

    def register_my_category_all(self, progress_callback, ret_callback, regMsg_callback, pause=False):
        print('register_my_category_all')

        categories_to_upload = {}
        for row in range(self.tableWidget.rowCount()):
            categories_to_upload[self.tableWidget.item(row, 0).text()] = self.my_category_with_code.loc[self.tableWidget.item(row, 0).text()].to_dict()

        clearScreen()
        print_logo(PROGRAM_TITLE, VERSION)
        x = 0
        y = 0
        grid_w = 1200
        grid_h = 800
        download_folder = '.'

        w = WEBManipulator([x,y], [grid_w,grid_h], download_folder, int(self.lineEdit_7.text()), headless=False)
        
        login_url = 'https://ad2.shoplinker.co.kr/index.php'
        if w.login_shoplinker(login_url, id=self.lineEdit.text(), password=self.lineEdit_2.text()) == False:
            print('에러')
            return '로그인 에러'

        w.goto_category_mapping()

        for k, v in categories_to_upload.items():
            w.register(k, 
                        v['스마트스토어'], 
                        v['쿠팡'], 
                        v['지마켓'], 
                        v['11번가'], 
                        v['옥션'], 
                        v['카페24'], 
                    )
        return {"result":"완료"}

    def get_category(self, progress_callback, ret_callback, regMsg_callback, pause=False):
        print('get_category')
        clearScreen()
        print_logo(PROGRAM_TITLE, VERSION)
        x = 0
        y = 0
        grid_w = 1200
        grid_h = 800
        download_folder = '.'

        w = WEBManipulator([x,y], [grid_w,grid_h], download_folder, int(self.lineEdit_7.text()), headless=False)
        
        login_url = 'https://ad2.shoplinker.co.kr/index.php'
        if w.login_shoplinker(login_url, id=self.lineEdit.text(), password=self.lineEdit_2.text()) == False:
            print('에러')
            return '로그인 에러'

        w.goto_category_mapping()

        if self.comboBox.currentText() == '스마트스토어':
            category = w.get_smartstore_category(self.comboBox_2.currentText(), False, pause)
        elif self.comboBox.currentText() == '쿠팡':
            category = w.get_coupang_category(self.comboBox_2.currentText(), False, pause)
        elif self.comboBox.currentText() == '지마켓':
            category = w.get_gmarket_or_auction_category(self.comboBox.currentText(), self.comboBox_2.currentText(), False, pause)
        elif self.comboBox.currentText() == '11번가':
            category = w.get_11st_category(self.comboBox_2.currentText(), False, pause)
        elif self.comboBox.currentText() == '옥션':
            category = w.get_gmarket_or_auction_category(self.comboBox.currentText(), self.comboBox_2.currentText(), False, pause)
        elif self.comboBox.currentText() == '카페24':
            category = w.get_interpark_category(self.comboBox_2.currentText(), False, pause)

        for i in range(5):
            beepsound()

        return category

    def get_first_category(self, progress_callback, ret_callback, regMsg_callback, pause=False):
        print('get_first_category')
        clearScreen()
        print_logo(PROGRAM_TITLE, VERSION)
        x = 0
        y = 0
        grid_w = 1200
        grid_h = 800
        download_folder = '.'

        w = WEBManipulator([x,y], [grid_w,grid_h], download_folder, int(self.lineEdit_7.text()), headless=False)
        
        login_url = 'https://ad2.shoplinker.co.kr/index.php'
        if w.login_shoplinker(login_url, id=self.lineEdit.text(), password=self.lineEdit_2.text()) == False:
            print('에러')
            return '로그인 에러'

        w.goto_category_mapping()

        w.category = {} # 여기에서 초기화를 한번 하고 아래에서는 중간에 에러가 나면 에러가 난 이후 부터 다시 반복하는 구조로 변경
        if self.comboBox.currentText() == '스마트스토어':
            category = w.get_smartstore_category(self.comboBox_2.currentText(), True, pause)
        elif self.comboBox.currentText() == '쿠팡':
            category = w.get_coupang_category(self.comboBox_2.currentText(), True, pause)
        elif self.comboBox.currentText() == '지마켓':
            category = w.get_gmarket_category(self.comboBox_2.currentText(), True, pause)
        elif self.comboBox.currentText() == '11번가':
            category = w.get_11st_category(self.comboBox_2.currentText(), True, pause)
        elif self.comboBox.currentText() == '옥션':
            category = w.get_auction_category(self.comboBox_2.currentText(), True, pause)
        elif self.comboBox.currentText() == '카페24':
            category = w.get_interpark_category(self.comboBox_2.currentText(), True, pause)

        category_maker = self.comboBox.currentText()
        self.change_category_maker(category_maker)

        return category

    def display_my_category(self):
        print('display_my_category')
        self.tableWidget.clear()
        # clear하면 헤더도 지워지므로 다시 설정
        self.tableWidget.setHorizontalHeaderLabels(table_header)
        self.tableWidget.setRowCount(len(self.my_category))
        self.save_my_category_enabled = False
        # print(self.df_easywinner)
        print(self.my_category)
        for row_num, (index, row) in enumerate(self.my_category.iterrows()):
            item = QTableWidgetItem(str(index))
            self.tableWidget.setItem(row_num, 0, item)
            item = QTableWidgetItem(self.my_category.loc[index]['고객사대분류명'])
            self.tableWidget.setItem(row_num, 1, item)
            item = QTableWidgetItem(row['키워드'])
            self.tableWidget.setItem(row_num, 2, item)
            for idx, store in enumerate(store_list):
                item = QTableWidgetItem(str(row[f'{store}키워드']))
                self.tableWidget.setItem(row_num, idx+3, item)
                item = QTableWidgetItem(row[store])
                self.tableWidget.setItem(row_num, idx+9, item)

        self.tableWidget.resizeColumnsToContents()
        max_width = 150  # Adjust as needed
        for col in range(self.tableWidget.model().columnCount()):
            self.tableWidget.setColumnWidth(col, min(self.tableWidget.columnWidth(col), max_width))        
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.save_my_category_enabled = True

    def adjust_excel_column(self, ws):
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter # Get the column name
            for cell in col:
                try: # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column].width = adjusted_width

    def save_my_category_to_file(self):
        print('save_my_category_to_file')
        filename = self.lineEdit_4.text() + '/my_category.xlsx'
        with pd.ExcelWriter(filename) as writer:
            self.my_category.to_excel(
                writer,
                sheet_name = "Sheet1",
                header = True,
                index = True,
                index_label='고객사대분류코드')
            self.my_category_with_code.to_excel(
                writer,
                sheet_name = "Sheet2",
                header = True,
                index = True,
                index_label='고객사대분류코드')
        wb = openpyxl.open(filename)
        ws = wb['Sheet1']
        self.adjust_excel_column(ws)
        # ws.column_dimensions['A'].width = 20
        ws = wb['Sheet2']
        self.adjust_excel_column(ws)
        # ws.column_dimensions['A'].width = 20
        wb.save(filename)

    def save_category_match(self):
        print('save_category_match')
        category_code = self.tableWidget_2.cellWidget(0, 0).currentText()
        easywinner_all_category = self.tableWidget_2.item(0, 1).text()
        keyword = self.tableWidget_3.item(0, 0).text()
        print(category_code, self.my_category.index)
        if category_code in self.my_category.index:
            store_keyword = []
            store_category = []
            store_category_with_code = []
            for idx, store in enumerate(store_list):
                store_category.append(self.tableWidget_2.item(0, idx+2).text())
                store_keyword.append(self.tableWidget_3.item(0, idx+1).text())
                store_category_with_code.append(self.my_category_selected[store])
            self.my_category.loc[category_code] = [easywinner_all_category, keyword] + store_keyword + store_category
            self.my_category_with_code.loc[category_code] = [easywinner_all_category, keyword] + store_keyword + store_category_with_code
        else:
            store_keyword_dict = {}
            store_category_dict = {}
            store_category_with_code_dict = {}
            for idx, store in enumerate(store_list):
                store_category_dict.update({store:self.tableWidget_2.item(0, idx+2).text()})
                store_keyword_dict.update({f'{store}키워드':self.tableWidget_3.item(0, idx+1).text()})
                store_category_with_code_dict.update({store:self.my_category_selected[store]})
            new_data = {'고객사대분류명': easywinner_all_category, '키워드':keyword}
            new_data.update(store_keyword_dict)
            new_data.update(store_category_dict)
            self.my_category = pd.concat([self.my_category, pd.DataFrame(new_data, index=[category_code])])
            new_data = {'고객사대분류명': easywinner_all_category, '키워드':keyword}
            new_data.update(store_keyword_dict)
            new_data.update(store_category_with_code_dict)
            self.my_category_with_code = pd.concat([self.my_category_with_code, pd.DataFrame(new_data, index=[category_code])])
        self.save_my_category_to_file()
        self.display_my_category()
        self.easywinner_code_show_toggle()

    def test(self):
        print('test')
        # Pass the function to execute
        worker = Worker(self.test_thread) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.test_thread_result)
        worker.signals.finished.connect(self.test_thread_complete)
        worker.signals.progress.connect(self.test_thread_progress)

        # Execute
        self.threadpool.start(worker)

    def test_thread(self, progress_callback, ret_callback, regMsg_callback):
        print('test_thread')
        clearScreen()
        print_logo(PROGRAM_TITLE, VERSION)
        x = 0
        y = 0
        grid_w = 1200
        grid_h = 800
        download_folder = '.'

        w = WEBManipulator([x,y], [grid_w,grid_h], download_folder, int(self.lineEdit_7.text()), headless=False)
        
        login_url = 'https://ad2.shoplinker.co.kr/index.php'
        if w.login_shoplinker(login_url, id=self.lineEdit.text(), password=self.lineEdit_2.text()) == False:
            print('에러')
            return '로그인 에러'

        w.register_shoplinker()
        return {"result":"완료"}
    
    def test_thread_result(self, s):
        print('test_thread_result')
    def test_thread_complete(self):
        print('test_thread_complete')
        print("THREAD COMPLETE!")
    def test_thread_progress(self, n):
        print("%d%% done" % n)


def main():
    app = QApplication()
    w = MainWindow()
    # monitors = QScreen.virtualSiblings(w.screen())
    # print(monitors)
    # monitor = monitors[-1].availableGeometry()
    # # screen = QScreen()
    # # screenGeometry = screen.geometry()
    # height = monitor.height()
    # width = monitor.width()
    # # x=(width - w.width()) / 2.0
    # # y=(height - w.height()) / 2.0
    # x = 100
    # y = 100
    # w.setGeometry(monitor.left() + 100,monitor.top() + 100,w.width(),w.height())
    w.show()
    app.exec()

if __name__ == "__main__":
    main()
