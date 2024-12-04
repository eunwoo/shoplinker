from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.edge.service import Service
# from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException
from bs4 import BeautifulSoup as bs
import urllib.request
import re
import os
import sys
from datetime import date, datetime
import time
import openpyxl
from inspect import currentframe, getframeinfo
from shutil import copyfile
from PySide6.QtCore import QFileSystemWatcher, QObject
from pathlib import Path
import readchar
import subprocess
# selenium 4
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import copy

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

class WEBManipulator(QObject):
    def __init__(self, position, size, download_folder, loading_wait_time, headless=False):

        self.position = position
        self.size = size
        self.download_folder = download_folder
        self.headless = headless
        self.driver = None

        self.open_browser(self.position, self.size, self.download_folder, self.headless)

        self.wait_time = 10

        self.category = {}

        self.loading_wait_time = loading_wait_time

    # destructor
    def __del__(self):
        print('WEBManipulator.__del__')
        if self.driver:
            self.driver.quit()
            self.driver = None
        # subprocess.call("TASKKILL /f  /IM  CHROME.EXE")

    def get_log_filename(self, out_path):
        # 날짜_Log_일련번호.txt
        from datetime import datetime
        files = os.listdir(out_path)
        file_str = datetime.today().strftime('%Y%m%d')+"_Log_"
        p = re.compile(file_str+r"(\d*).log")
        # print(file_str)
        no = 1
        for file in files:
            print(file)
            if p.match(file):
                cur_no = int(os.path.splitext(file)[0].replace(file_str, ''))
                if cur_no >= no:
                    no = cur_no + 1
        print(file_str+str(no))
        return file_str+str(no)
    
    def open_browser(self, position, size, download_folder, headless=False):
        print('WEBManipulator.open_browser')
        # s = Service("chromedriver.exe")   # Chrome
        # s = Service("msedgedriver.exe") # Edge
        
        # s = Service("geckodriver.exe")    # Firefox 사용시 필요없음
        # options = webdriver.ChromeOptions()
        # options = webdriver.FirefoxOptions()
        options = Options()
        if headless == True:
            options.add_argument('headless')
        # options.add_argument('--window-size=1000,800')
        # options.add_argument('--start-maximized')
        # options.add_argument("--mute-audio")    
        # options.add_argument('disable-gpu') # Firefox 사용시 사용불가

        options = Options()
        # options.binary_location = "C:\\\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # default 경로가 아닌 경우 필요
        # options.add_argument('--headless')
        options.add_argument('--incognito') # 시크릿모드
        # optional
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        # optional
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("download.default_directory=D:/Users/jieun/work/soomgo/029. easywinner/download")    # download folder setting option #1 not work
        options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Firefox 사용시 사용불가

        # https://stackoverflow.com/questions/35331854/downloading-a-file-at-a-specified-location-through-python-and-selenium-using-chr
        download_folder = download_folder.replace('/', '\\')
        prefs = {'download.default_directory' : download_folder}    # download folder setting option #2
        options.add_experimental_option('prefs', prefs)

        if self.driver:
            self.driver.quit()
            self.driver = None

        # self.driver = webdriver.Chrome(options=options, service=s)
        # self.driver = webdriver.Edge(options=options, service=s)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        # self.driver = webdriver.Chrome(".\\chromedriver.exe")
        driver_path = ChromeDriverManager().install()
        print(driver_path)
        correct_driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")
        self.driver = webdriver.Chrome(options=options, service=ChromeService(correct_driver_path))

        self.driver.implicitly_wait(1)

        self.driver.set_window_position(position[0], position[1], windowHandle = 'current')
        self.driver.set_window_size(size[0], size[1])

    def quit(self):
        print('WEBManipulator.quit')
        self.driver.quit()

    def input(self, xpath, value):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        inp = self.driver.find_element(by=By.XPATH, value=xpath)
        inp.send_keys(value)
    
    def clear(self, xpath):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        inp = self.driver.find_element(by=By.XPATH, value=xpath)
        inp.clear()

    def check_checkbox(self, xpath):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        inp = self.driver.find_element(by=By.XPATH, value=xpath)
        inp.click()

    def click(self, xpath):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        inp = self.driver.find_element(by=By.XPATH, value=xpath)
        inp.send_keys(Keys.ENTER)

    def click_element(self, element):
        element.send_keys(Keys.ENTER)

    def select_by_visible_text(self, xpath, value):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        select = Select(self.driver.find_element(by=By.XPATH, value=xpath))
        select.select_by_visible_text(value)

    def select_by_value(self, xpath, value):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        select = Select(self.driver.find_element(by=By.XPATH, value=xpath))
        select.select_by_value(value)

    def select_by_index(self, xpath, value):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        select = Select(self.driver.find_element(by=By.XPATH, value=xpath))
        select.select_by_index(value)

    def get_select_current_option(self, xpath):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        select = Select(self.driver.find_element(by=By.XPATH, value=xpath))
        return select.first_selected_option.text

    def get_select_all_options(self, xpath):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        select = Select(self.driver.find_element(by=By.XPATH, value=xpath))
        return select.options

    def get_text(self, xpath):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        inp = self.driver.find_element(by=By.XPATH, value=xpath)
        return inp.text

    def login(self, url, id, password):
        self.id = id
        self.password = password
        try:
            self.set_url(url)
            time.sleep(5)
            self.input('//*[@id="user_id"]', id)
            self.input('//*[@id="passwords"]', password)
            self.click('//*[@id="login_form"]/div[1]/div[2]/button')

            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')

                alert = self.driver.switch_to.alert
                alert.accept()
                print("alert accepted")
                return False
            except TimeoutException:
                print("no alert")

        except UnexpectedAlertPresentException as e:
            print('로그인 정보가 잘못되었습니다')

        self.main_page = self.driver.current_window_handle
        return True

    def login_shoplinker(self, url, id, password):
        self.id = id
        self.password = password
        try:
            self.set_url(url)
            self.input('/html/body/form/div[1]/div[1]/div[1]/div[1]/input[1]', id)
            self.input('/html/body/form/div[1]/div[1]/div[1]/div[2]/input[1]', password)
            self.click('/html/body/form/div[1]/div[1]/div[1]/a')

            try:
                WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')

                alert = self.driver.switch_to.alert
                alert.accept()
                print("alert accepted")
                return False
            except TimeoutException:
                print("no alert")

        except UnexpectedAlertPresentException as e:
            print('로그인 정보가 잘못되었습니다')

        self.main_page = self.driver.current_window_handle
        time.sleep(10)
        return True

    def set_url(self, url):
        print('set_url', url)
        self.driver.get(url)

    def print_msg(self, msg):
        current_time = time.time()
        time_elapsed = current_time - self.start_time
        hours, rem = divmod(time_elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        formatted_msg = f"\n[경과시간 {int(hours):0>2}:{int(minutes):0>2}:{float(seconds):02.0f}] {msg}"
        print(formatted_msg)

    def save_as_excel(self, mall_str, page, download_folder):
        if not os.path.exists(download_folder):
            createFolder(download_folder)
        chrome_download_folder = Path(download_folder).parent.parent.absolute()
        done = False
        while not done:
            for x in os.listdir(chrome_download_folder):
                if x.split('.')[-1] == 'xls':
                    chrome_download_file = str(chrome_download_folder).replace('\\','/') + '/' + x
                    if os.path.isfile(chrome_download_file):
                        os.rename(chrome_download_file, download_folder + '/' + str(page) + '.xls')
                        done = True
                        break
            time.sleep(1)

    def download_mall(self, mall_str, download_folder):

        self.print_msg(f'{mall_str} 시작')

        xpath_mall = '//*[@id="mall_id"]'   # 쇼팡몰 선택
        self.select_by_visible_text(xpath_mall, mall_str)
        current_page = 1
        self.print_msg(f'{current_page} 페이지')
        # 검색 버튼을 클릭하지 않고 페이지 당 표시 개수를 변경해도 검색 결과가 업데이트된다.
        xpath_items_per_page = '//*[@id="search_form"]/div/div[3]/div[1]/select'
        if self.get_select_current_option(xpath_items_per_page) != '500 개씩':
            self.select_by_visible_text(xpath_items_per_page, '500 개씩')
        else:
            self.click('//*[@id="submit_btn"]') # 검색 버튼 클릭. 1페이지 보기

        # 총 아이템 수 읽어오기
        total_items_str = self.get_text('//*[@id="total_cnt"]')
        total_items = int(total_items_str.replace(',',''))
        print(f"총 아이템 {total_items}")
        if total_items == 0:
            return

        while True:
            # 엑셀작업클릭
            self.click('//*[@id="search_form"]/div/div[3]/div[1]/a[4]') # 
            print('Step 1')
            # 선택클릭
            self.click('//*[@id="fake_chk"]')
            print('Step 2')
            # 엑셀다운 클릭
            self.click('//*[@id="search_form"]/div/div[3]/div[4]/p/input')
            print('Step 3')
            # 다운로드 상자 표시 확인
            selector = 'body > div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable.ui-resizable'
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            inp = self.driver.find_element(by=By.CSS_SELECTOR, value=selector)
            # print(inp.get_attribute('style'))
            style = inp.get_attribute('style')
            p = re.compile('display: (.+?);')
            print('Step 4')
            # wait for display block
            while True:
                style = inp.get_attribute('style')
                m = p.search(style)
                if m:
                    if m.group(1) == 'block':
                        print('엑셀 다운로드 시작', end='')
                        sys.stdout.flush()
                        break
                time.sleep(1)
                print('Step 5')
            # wait for display none
            while True:
                style = inp.get_attribute('style')
                m = p.search(style)
                if m:
                    if m.group(1) == 'none':
                        print('완료')
                        sys.stdout.flush()
                        self.save_as_excel(mall_str, current_page, download_folder + '/' + mall_str)
                        break
                print('.',end='')
                sys.stdout.flush()
                time.sleep(1)

            xpath = '//*[@id="pagination_div"]'
            WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            inp = self.driver.find_element(by=By.XPATH, value=xpath)
            children = inp.find_elements(by=By.CSS_SELECTOR, value='a')
            # print('search next page', children)
            # print("아무키나 누르면 계속 진행")
            # k = readchar.readchar()            
            need_continue = False
            for child in children:
                # print(child.text)
                if self.isint(child.text) and int(child.text) > current_page:
                    # print(child.text)
                    current_page = int(child.text)
                    next_page = child
                    self.click_element(next_page)
                    self.print_msg(f'{current_page} 페이지')
                    need_continue = True
                    break
            if need_continue:
                continue
            else:
                break   # escape while loop

    def download(self, download_folder):

        self.start_time = time.time()
        self.files_chrome_download = [x for x in os.listdir(download_folder) if x.split('.')[-1] == "xls"]

        self.click('//*[@id="gnb"]/li[1]/a')    # 상품관리 탭 클릭
        self.click('//*[@id="search_form"]/div/div[1]/ul[1]/li[3]/a')   # 쇼핑몰 등록상품 탭 클릭
        self.clear('//*[@id="st_date"]')        # 날짜 삭제
        self.input('//*[@id="st_date"]', '2005-01-01')  # 날짜 입력
        # print("아무키나 누르면 계속 진행")
        # k = readchar.readchar()

        today = date.today()
        now = datetime.now()
        date_folder = f'{today.year}{today.month:02d}{today.day:02d}{now.strftime("%H%M%S")}'
        if not os.path.exists(download_folder + '/' + date_folder):
            createFolder(download_folder + '/' + date_folder)

        # 개별 스토어 작업 시작
        xpath_mall = '//*[@id="mall_id"]'
        all_stores = self.get_select_all_options(xpath_mall)
        store_list = []
        for i, store in enumerate(all_stores):
            if i != 0: # '전체 쇼핑몰 보기' 스킵
                store_list.append(store.text)
        print(store_list)
        for store in store_list:
            self.download_mall(store, download_folder + '/' + date_folder)

    def get_not_prepared_num(self, upload_files):
        cnt = 0
        for upload_file in upload_files:
            if upload_file['state'] != 'prepared':
                cnt += 1
        return cnt
    
    def get_progress(self, upload_files):
        total = len(upload_files)
        done_cnt = self.get_not_prepared_num(upload_files)
        return int(done_cnt / total * 100)

    def is_upload_done(self, upload_files):
        for upload_file in upload_files:
            if upload_file['state'] == 'prepared':
                return False
        return True

    def isint(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def query(self, str):
        print('검색어:', str)
        time.sleep(3)
        while True:
            try:
                value='//*[@id="explore"]/div/form/div/input'
                # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, value)))

                # my_element_id = 'something123'
                # ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,)
                ignored_exceptions=()
                your_element = WebDriverWait(self.driver, 10, ignored_exceptions=ignored_exceptions)\
                                        .until(EC.presence_of_element_located((By.XPATH, value)))

                inp = self.driver.find_element(by=By.XPATH, value=value)
                inp.send_keys(str)
                btn = self.driver.find_element(by=By.XPATH, value='//*[@id="explore"]/div/form/div/button')
                self.driver.execute_script("arguments[0].click();", btn)
                break
            except:
                time.sleep(1)
                pass

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def toFloat(self, str):
        if self.isfloat(str.replace(',','')):
            return float(str.replace(',',''))
        else:
            return str
        

    def num_with_unit(self, num, unit):
        if unit == "억원":
            return int(num.replace(',',''))*100000000
        elif unit == "만원":
            return int(num.replace(',',''))*10000
        else:
            return int(num.replace(',',''))

    def wait_loading(self, xpath, wait_time = 8):
        wait_time = self.loading_wait_time
        ret_msg = 'ok'
        print(f'wait_loading: {wait_time} sec')
        p = re.compile('display: (.+?);')
        inp = self.driver.find_element(by=By.XPATH, value=xpath)

        # wait for display block
        # time_start = time.time()
        # while True:
        #     style = inp.get_attribute('style')
        #     m = p.search(style)
        #     if m:
        #         if m.group(1) == 'block':
        #             break
        #     time.sleep(0.01)
        #     if time.time() - time_start > 5:
        #         print('5 sec timeout')
        #         break
        #     print('.',end='')
        #     sys.stdout.flush()
        time.sleep(wait_time)
        # wait for display none
        time_start = time.time()
        while True:
            try:
                style = inp.get_attribute('style')
                m = p.search(style)
                if m:
                    if m.group(1) == 'none':
                        break
                time.sleep(0.04)
                if time.time() - time_start > 5:
                    print('5 sec timeout')
                    ret_msg = 'timeout'
                    break
                print('-',end='')
                sys.stdout.flush()
            except UnexpectedAlertPresentException as e:
                print('UnexpectedAlertPresentException')
                print(e)
                # print("아무키나 누르시면 닫힙니다.")
                # k = readchar.readchar()
                continue
        return ret_msg

    def cleanup(self, category):
        # "pass"와 "timeout"을 삭제
        print('cleanup')
        new_category = copy.deepcopy(category)
        for k1, v1 in category.items():
            if type(category[k1]) == dict:
                for k2, v2 in category[k1].items():
                    if type(category[k1][k2]) == dict:
                        for k3, v3 in category[k1][k2].items():
                            print(v3)
                    else:
                        print(f'{k1}{k2} is not dict and gets removed')
                        del new_category[k1][k2]
            else: # must be "pass" or "timeout"
                print(f'{k1} is not dict and gets removed')
                del new_category[k1]
        del category
        return new_category

    def get_gmarket_or_auction_category(self, maker, category_to_get, first_only=False, pause=False):
        self.success = False
        self.category[maker] = {}
        self.start_time = time.time()

        while self.success == False:
            self.get_gmarket_or_auction_category_retry(maker, category_to_get, first_only, pause)
        self.category[maker] = self.cleanup(self.category[maker])
        return self.category

    def get_gmarket_or_auction_category_retry(self, maker, category_to_get, first_only=False, pause=False):
        self.print_msg(f'{maker} 카테고리 가져오기 시작')
        if maker == '지마켓':
            xpath = '//*[@id="mall0010_3_V1"]'
        else:
            xpath = '//*[@id="mall0003_0_V1"]'
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        e1 = self.driver.find_element(by=By.XPATH, value=xpath)
        e1.send_keys(Keys.ENTER)
        
        time.sleep(3)
        e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory1"]') # 대분류
        d1 = Select(e1)
        for opt1 in d1.options:
            if opt1.text in ["대분류선택", '도서', '음반/DVD', '여행/티켓/e쿠폰', '생활서비스', '렌탈']:
                continue
            if category_to_get != '전체' and category_to_get != '' and category_to_get != opt1.text:
                continue
            self.print_msg(f' > {opt1.text}({opt1.get_attribute("value")})')
            key1 = opt1.text+'('+opt1.get_attribute('value')+')'
            # 이미 key가 있는 경우, timeout에 의해서 실패했으면 키 삭제
            if key1 in self.category[maker]:
                if "timeout" in self.category[maker][key1]:
                    print(f'{key1}에서 timeout 에러 발생하여 삭제처리함')
                    del self.category[maker][key1]
                    continue
                elif "pass" in self.category[maker][key1]:
                    continue
            else:
                self.category[maker][key1] = {}
            if first_only: # 대분류만 가져오기
                continue
            self.select_by_visible_text('//*[@id="goodsCategory1"]', opt1.text)
            while True:
                try:
                    self.wait_loading('//*[@id="page_progress"]')
                    break
                except:
                    self.select_by_visible_text('//*[@id="goodsCategory1"]', "대분류선택")
                    self.select_by_visible_text('//*[@id="goodsCategory1"]', opt1.text)

            self.select_by_visible_text('//*[@id="goodsCategory2"]', "중분류선택")
            e2 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory2"]') # 중분류
            d2 = Select(e2)
            for idx2, opt2 in enumerate(d2.options):
                # -------------------- start of test -------------------
                # if opt2.text in ['신생아/영유아완구','공간놀이완구', '승용완구', '인형', '작동완구', 'RC완구', '스포츠완구', '물놀이완구', '블록/레고', '유아동퍼즐']:
                #     continue
                # -------------------- end of test -------------------
                if opt2.text == "중분류선택":
                    continue
                self.print_msg(f' > > {opt2.text}({opt2.get_attribute("value")})')
                key2 = opt2.text+'('+opt2.get_attribute('value')+')'
                # 이미 key가 있는 경우, timeout에 의해서 실패했으면 키 삭제, 아니면 다음 카테고리 처리
                if key2 in self.category[maker][key1]:
                    if "timeout" in self.category[maker][key1][key2]:
                        print(f'{key2}에서 timeout 에러 발생하여 삭제처리함')
                        del self.category[maker][key1][key2]
                        continue
                    elif "pass" in self.category[maker][key1][key2]:
                        continue
                else:
                    self.category[maker][key1][key2] = {}
                self.select_by_index('//*[@id="goodsCategory2"]', idx2)
                while True:
                    try:
                        progress_ret = self.wait_loading('//*[@id="page_progress"]')
                        print('progress_ret:', progress_ret)
                        if progress_ret == "timeout":
                            print('closing browser due to timeout')
                            return
                        break
                    except:
                        self.select_by_visible_text('//*[@id="goodsCategory2"]', "중분류선택")
                        self.select_by_index('//*[@id="goodsCategory2"]', idx2)

                # self.select_by_visible_text('//*[@id="Esm_goodsCategory3"]', "소분류선택")
                WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="goodsCategory3"]')))
                e3 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory3"]') # 세분류
                if e3.text == "최종분류입니다":
                    print('최종분류입니다')
                    self.category[maker][key1][key2]['최종분류'] = {}
                    self.category[maker][key1][key2]['최종분류']['없음'] = {}
                    self.category[maker][key1][key2]['최종분류']['없음']['없음'] = {}
                    self.wait_loading('//*[@id="text_info2"]')
                    self.get_category_common(self.category[maker][key1][key2]['최종분류']['없음']['없음'], pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')
                    continue
                d3 = Select(e3)
                for idx3, opt3 in enumerate(d3.options):
                    if opt3.text in ["소분류선택"]:
                        continue
                    # -------------------- start of test -------------------
                    # if opt3.text in ['감각발달완구','언어/학습완구', '역할놀이완구', '미술/공작놀이', '음악/악기놀이']:
                    #     continue
                    # -------------------- end of test -------------------
                    if 'test' in opt3.text: # test로 시작하는 카테고리는 선택하지 않음
                        print('skipping test 카테고리')
                        continue
                    self.print_msg(f' > > > {opt3.text}({opt3.get_attribute("value")})')
                    key3 = opt3.text+'('+opt3.get_attribute('value')+')'
                    print(f'key3: {key3}')
                    # 이미 key가 있는 경우, timeout에 의해서 실패했으면 키 삭제, 아니면 다음 카테고리 처리
                    if key3 in self.category[maker][key1][key2]:
                        if "timeout" in self.category[maker][key1][key2][key3]:
                            print(f'{key3}에서 timeout 에러 발생하여 삭제처리함')
                            del self.category[maker][key1][key2][key3]
                            continue
                        elif "pass" in self.category[maker][key1][key2][key3]:
                            continue
                    else:
                        self.category[maker][key1][key2][key3] = {}
                    self.select_by_index('//*[@id="goodsCategory3"]', idx3)
                    while True:
                        try:
                            progress_ret = self.wait_loading('//*[@id="page_progress"]')
                            print('progress_ret:', progress_ret)
                            if progress_ret == "timeout":
                                print('closing browser due to timeout')
                                self.category[maker][key1][key2][key3]["timeout"] = True
                                return self.category
                            break
                        except:
                            self.select_by_visible_text('//*[@id="goodsCategory3"]', "소분류선택")
                            self.select_by_index('//*[@id="goodsCategory3"]', idx3)

                    # self.select_by_visible_text('//*[@id="Esm_goodsCategory4"]', "세분류선택") # 최종분류입니다 가 나오는 경우가 있으므로 삭제
                    WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="goodsCategory4"]')))
                    e4 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory4"]') # 세분류
                    if e4.text == "최종분류입니다":
                        print('최종분류입니다')
                        self.category[maker][key1][key2][key3]['최종분류'] = {}
                        self.category[maker][key1][key2][key3]['최종분류']['없음'] = {}
                        self.wait_loading('//*[@id="text_info2"]')
                        self.get_category_common(self.category[maker][key1][key2][key3]['최종분류']['없음'], pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')
                        continue
                    d4 = Select(e4)
                    for idx4, opt4 in enumerate(d4.options):
                        if opt4.text == "세분류선택":
                            continue
                        self.print_msg(f' > > > > {opt4.text}({opt4.get_attribute("value")})')
                        key4 = opt4.text+'('+opt4.get_attribute('value')+')'
                        self.category[maker][key1][key2][key3][key4] = {}

                        self.select_by_index('//*[@id="goodsCategory4"]', idx4)
                        self.wait_loading('//*[@id="page_progress"]')
                        time.sleep(0.2)
                        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="goodsCategory5"]')))
                        e5 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory5"]') # 상세분류
                        if e5.text == "최종분류입니다":
                            print('최종분류입니다')
                            self.category[maker][key1][key2][key3][key4]['최종분류'] = {}
                            if self.wait_loading('//*[@id="text_info2"]') == 'timeout':
                                print(f'{maker}>{key1}>{key2}>{key3}>{key4} 조회실패(timeout)')
                                continue
                            self.get_category_common(self.category[maker][key1][key2][key3][key4]['최종분류'], pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')
                            continue
                        d5 = Select(e5)
                        for idx5, opt5 in enumerate(d5.options):
                            if opt5.text == "상세분류선택":
                                continue
                            self.print_msg(f' > > > > > {opt5.text}({opt5.get_attribute("value")})')
                            key5 = opt5.text+'('+opt5.get_attribute('value')+')'
                            self.category[maker][key1][key2][key3][key4][key5] = {}
                            self.select_by_index('//*[@id="goodsCategory5"]', idx5)
                            self.wait_loading('//*[@id="text_info2"]')
                            self.get_category_common(self.category[maker][key1][key2][key3][key4][key5], pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')

                    self.category[maker][key1][key2][key3]["pass"] = True
                self.category[maker][key1][key2]["pass"] = True
            self.category[maker][key1]["pass"] = True

        self.print_msg(f'{maker} 카테고리 가져오기 완료')
        self.success = True
        return self.category

    def get_gmarket_category(self, category_to_get, first_only=False, pause=False):
        self.success = False
        maker = '지마켓'
        self.category[maker] = {}
        self.start_time = time.time()

        while self.success == False:
            self.get_gmarket_category_retry(category_to_get, first_only, pause)
        return self.category

    def get_gmarket_category_retry(self, category_to_get, first_only=False, pause=False):
        maker = '지마켓'

        self.print_msg(f'{maker} 카테고리 가져오기 시작')
        # self.category = {}
        e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="mall0010_3_V1"]') # 지마켓
        e1.send_keys(Keys.ENTER)
        
        time.sleep(3)
        # self.category[maker] = {}
        e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory1"]') # 대분류
        d1 = Select(e1)
        for opt1 in d1.options:
            if opt1.text in ["대분류선택", '도서', '음반/DVD', '여행/티켓/e쿠폰', '생활서비스', '렌탈']:
                continue
            if category_to_get != '전체' and category_to_get != '' and category_to_get != opt1.text:
                continue
            self.print_msg(f' > {opt1.text}({opt1.get_attribute("value")})')
            key1 = opt1.text+'('+opt1.get_attribute('value')+')'
            # 이미 key가 있는 경우, timeout에 의해서 실패했으면 키 삭제
            if key1 in self.category[maker]:
                if "timeout" in self.category[maker][key1]:
                    print(f'{key1}에서 timeout 에러 발생하여 삭제처리함')
                    del self.category[maker][key1]
                    continue
                elif "pass" in self.category[maker][key1]:
                    continue
            else:
                self.category[maker][key1] = {}
            if first_only: # 대분류만 가져오기
                continue
            self.select_by_visible_text('//*[@id="goodsCategory1"]', opt1.text)
            while True:
                try:
                    self.wait_loading('//*[@id="page_progress"]')
                    break
                except:
                    self.select_by_visible_text('//*[@id="goodsCategory1"]', "대분류선택")
                    self.select_by_visible_text('//*[@id="goodsCategory1"]', opt1.text)

            self.select_by_visible_text('//*[@id="goodsCategory2"]', "중분류선택")
            e2 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory2"]') # 중분류
            d2 = Select(e2)
            for idx2, opt2 in enumerate(d2.options):
                # -------------------- start of test -------------------
                # if opt2.text in ['신생아/영유아완구','공간놀이완구', '승용완구', '인형', '작동완구', 'RC완구', '스포츠완구', '물놀이완구', '블록/레고', '유아동퍼즐']:
                #     continue
                # -------------------- end of test -------------------
                if opt2.text == "중분류선택":
                    continue
                self.print_msg(f' > > {opt2.text}({opt2.get_attribute("value")})')
                key2 = opt2.text+'('+opt2.get_attribute('value')+')'
                # 이미 key가 있는 경우, timeout에 의해서 실패했으면 키 삭제, 아니면 다음 카테고리 처리
                if key2 in self.category[maker][key1]:
                    if "timeout" in self.category[maker][key1][key2]:
                        print(f'{key2}에서 timeout 에러 발생하여 삭제처리함')
                        del self.category[maker][key1][key2]
                        continue
                    elif "pass" in self.category[maker][key1][key2]:
                        continue
                else:
                    self.category[maker][key1][key2] = {}
                self.select_by_index('//*[@id="goodsCategory2"]', idx2)
                while True:
                    try:
                        progress_ret = self.wait_loading('//*[@id="page_progress"]')
                        print('progress_ret:', progress_ret)
                        if progress_ret == "timeout":
                            print('closing browser due to timeout')
                            return
                        break
                    except:
                        self.select_by_visible_text('//*[@id="goodsCategory2"]', "중분류선택")
                        self.select_by_index('//*[@id="goodsCategory2"]', idx2)

                # self.select_by_visible_text('//*[@id="Esm_goodsCategory3"]', "소분류선택")
                WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="goodsCategory3"]')))
                e3 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory3"]') # 세분류
                if e3.text == "최종분류입니다":
                    print('최종분류입니다')
                    self.category[maker][key1][key2]['최종분류'] = {}
                    self.category[maker][key1][key2]['최종분류']['없음'] = {}
                    self.category[maker][key1][key2]['최종분류']['없음']['없음'] = {}
                    self.wait_loading('//*[@id="text_info2"]')
                    self.get_category_common(self.category[maker][key1][key2]['최종분류']['없음']['없음'], pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')
                    continue
                d3 = Select(e3)
                for idx3, opt3 in enumerate(d3.options):
                    if opt3.text in ["소분류선택"]:
                        continue
                    # -------------------- start of test -------------------
                    # if opt3.text in ['감각발달완구','언어/학습완구', '역할놀이완구', '미술/공작놀이', '음악/악기놀이']:
                    #     continue
                    # -------------------- end of test -------------------
                    if 'test' in opt3.text: # test로 시작하는 카테고리는 선택하지 않음
                        print('skipping test 카테고리')
                        continue
                    self.print_msg(f' > > > {opt3.text}({opt3.get_attribute("value")})')
                    key3 = opt3.text+'('+opt3.get_attribute('value')+')'
                    print(f'key3: {key3}')
                    # 이미 key가 있는 경우, timeout에 의해서 실패했으면 키 삭제, 아니면 다음 카테고리 처리
                    if key3 in self.category[maker][key1][key2]:
                        if "timeout" in self.category[maker][key1][key2][key3]:
                            print(f'{key3}에서 timeout 에러 발생하여 삭제처리함')
                            del self.category[maker][key1][key2][key3]
                            continue
                        elif "pass" in self.category[maker][key1][key2][key3]:
                            continue
                    else:
                        self.category[maker][key1][key2][key3] = {}
                    self.select_by_index('//*[@id="goodsCategory3"]', idx3)
                    while True:
                        try:
                            progress_ret = self.wait_loading('//*[@id="page_progress"]')
                            print('progress_ret:', progress_ret)
                            if progress_ret == "timeout":
                                print('closing browser due to timeout')
                                self.category[maker][key1][key2][key3]["timeout"] = True
                                return self.category
                            break
                        except:
                            self.select_by_visible_text('//*[@id="goodsCategory3"]', "소분류선택")
                            self.select_by_index('//*[@id="goodsCategory3"]', idx3)

                    # self.select_by_visible_text('//*[@id="Esm_goodsCategory4"]', "세분류선택") # 최종분류입니다 가 나오는 경우가 있으므로 삭제
                    WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="goodsCategory4"]')))
                    e4 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory4"]') # 세분류
                    if e4.text == "최종분류입니다":
                        print('최종분류입니다')
                        self.category[maker][key1][key2][key3]['최종분류'] = {}
                        self.category[maker][key1][key2][key3]['최종분류']['없음'] = {}
                        self.wait_loading('//*[@id="text_info2"]')
                        self.get_category_common(self.category[maker][key1][key2][key3]['최종분류']['없음'], pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')
                        continue
                    d4 = Select(e4)
                    for idx4, opt4 in enumerate(d4.options):
                        if opt4.text == "세분류선택":
                            continue
                        self.print_msg(f' > > > > {opt4.text}({opt4.get_attribute("value")})')
                        key4 = opt4.text+'('+opt4.get_attribute('value')+')'
                        self.category[maker][key1][key2][key3][key4] = {}

                        self.select_by_index('//*[@id="goodsCategory4"]', idx4)
                        self.wait_loading('//*[@id="page_progress"]')
                        time.sleep(0.2)
                        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="goodsCategory5"]')))
                        e5 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory5"]') # 상세분류
                        if e5.text == "최종분류입니다":
                            print('최종분류입니다')
                            self.category[maker][key1][key2][key3][key4]['최종분류'] = {}
                            if self.wait_loading('//*[@id="text_info2"]') == 'timeout':
                                print(f'{maker}>{key1}>{key2}>{key3}>{key4} 조회실패(timeout)')
                                continue
                            self.get_category_common(self.category[maker][key1][key2][key3][key4]['최종분류'], pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')
                            continue
                        d5 = Select(e5)
                        for idx5, opt5 in enumerate(d5.options):
                            if opt5.text == "상세분류선택":
                                continue
                            self.print_msg(f' > > > > > {opt5.text}({opt5.get_attribute("value")})')
                            key5 = opt5.text+'('+opt5.get_attribute('value')+')'
                            self.category[maker][key1][key2][key3][key4][key5] = {}
                            self.select_by_index('//*[@id="goodsCategory5"]', idx5)
                            self.wait_loading('//*[@id="text_info2"]')
                            self.get_category_common(self.category[maker][key1][key2][key3][key4][key5], pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')

                    self.category[maker][key1][key2][key3]["pass"] = True
                self.category[maker][key1][key2]["pass"] = True
            self.category[maker][key1]["pass"] = True

        self.print_msg(f'{maker} 카테고리 가져오기 완료')
        self.success = True
        return self.category

    def get_auction_category_sub(self, category_to_get, category_parent, first_only=False, pause=False, level=1):
        print(f'get_auction_category_sub (level={level})')
        print('category_to_get', category_to_get)
        self.select_by_index('//*[@id="goodsCategory{0}"]'.format(level), 0)

        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="goodsCategory{0}"]'.format(level))))
        e3 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory{0}"]'.format(level))
        print(f'e3.text: {e3.text}, level: {level}')
        if e3.text == "최종분류입니다":
            print('최종분류입니다')
            while level <= 5:
                if level == 3:
                    category_parent['최종분류'] == {}
                    category_parent = category_parent['최종분류']
                else:
                    category_parent['없음'] = {}
                    category_parent = category_parent['없음']
                level += 1
            self.wait_loading('//*[@id="text_info2"]')  # 옥션 카테고리를 조회중입니다. 문구 사라질 때까지 대기
            self.get_category_common(category_parent, pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')
            print('return 1')
            return

        e2 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory{0}"]'.format(level))
        d2 = Select(e2)
        for idx2, opt2 in enumerate(d2.options):
            if idx2 == 0:
                continue
            if category_to_get != '' and category_to_get != opt2.text:
                continue
            if level==2 and opt2.text == '자동차':
                print('자동차 skip')
                continue

            self.print_msg(' > '*level + f'{opt2.text}({opt2.get_attribute("value")})')
            key2 = opt2.text+'('+opt2.get_attribute('value')+')'
            category_parent[key2] = {}
            self.select_by_index('//*[@id="goodsCategory{0}"]'.format(level), idx2)
            while True:
                try:
                    self.wait_loading('//*[@id="page_progress"]')
                    break
                except:
                    # 0번 인덱스를 선택한 후 다시 선택
                    self.select_by_index('//*[@id="goodsCategory{0}"]'.format(level), 0)
                    self.select_by_index('//*[@id="goodsCategory{0}"]'.format(level), idx2)
            if '>' in category_to_get:
                next_category_to_get = '>'.join(category_to_get.split('>')[1:])
            else:
                next_category_to_get = ''
            if level == 5:
                self.get_category_common(category_parent[key2], pause, categories_xpath='//*[@id="disp_goodsCategory{0}"]')
            else:
                self.get_auction_category_sub(next_category_to_get, category_parent[key2], False, False, level + 1)

    def get_auction_category(self, category_to_get, first_only=False, pause=False, level=1):
        self.start_time = time.time()
        maker = '옥션'
        self.print_msg(f'{maker} 카테고리 가져오기 시작')
        self.category = {}
        e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="mall0003_0_V1"]') # 옥션
        e1.send_keys(Keys.ENTER)
        
        time.sleep(3)
        self.category[maker] = {}
        e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="goodsCategory{0}"]'.format(level)) # 대분류
        d1 = Select(e1)
        for idx1, opt1 in enumerate(d1.options):
            if opt1.text in ["대분류선택", '도서', '음반/DVD', '여행/티켓/e쿠폰', '생활서비스', '렌탈']:
                continue
            # 지정된 카테고리만 가져오기
            if category_to_get != '전체' and category_to_get != '' and category_to_get != opt1.text:
                continue
            self.print_msg(' > '*level+f'{opt1.text}({opt1.get_attribute("value")})')
            key1 = opt1.text+'('+opt1.get_attribute('value')+')'
            self.category[maker][key1] = {}
            if first_only: # 대분류만 가져오기
                continue
            self.select_by_visible_text('//*[@id="goodsCategory{0}"]'.format(level), opt1.text)
            while True:
                try:
                    self.wait_loading('//*[@id="page_progress"]')
                    break
                except:
                    self.select_by_index('//*[@id="goodsCategory{0}"]'.format(level), 0)
                    self.select_by_index('//*[@id="goodsCategory{0}"]'.format(level), idx1)

            next_category_to_get = ''
            # next_category_to_get = '카익스테리어용품' # 테스트용 코드
            self.get_auction_category_sub(next_category_to_get, self.category[maker][key1], False, False, level + 1)
   
        self.print_msg(f'{maker} 카테고리 가져오기 완료')
        return self.category

    def get_category_common(self, category, pause=False, categories_xpath='//*[@id="goodsCategory{0}"]', level=1, category_to_get='', first_only=False, max_level=6):
        print(f'get_category_common, level={level}')
        while True:
            e1 = self.driver.find_element(by=By.XPATH, value=categories_xpath.format(level))
            time.sleep(1)
            d1 = Select(e1)
            if len(d1.options) > 1:
                print('len(d1.options) > 1')
                for idx1, opt1 in enumerate(d1.options):
                    print(opt1.text)
                break
            print('.', end='')
            sys.stdout.flush()
            time.sleep(1)
        if category_to_get != '':
            next_category_to_get = '>'.join(category_to_get.split('>')[1:])
        else:
            next_category_to_get = ''
        print('next_category_to_get', next_category_to_get)
        current_category_to_get = category_to_get.split('>')[0]
        print('current_category_to_get', current_category_to_get)
        for idx1, opt1 in enumerate(d1.options):
            if idx1 == 0:
                print('get_category_common 1')
                continue
            if level == 1 and opt1.text in ["대분류선택", '도서', '음반/DVD', '여행/티켓/e쿠폰', '생활서비스', '렌탈']:
                continue
            if category_to_get != '':
                if opt1.text != current_category_to_get:
                    continue
            print('100')
            self.print_msg(' > '*level+f'{opt1.text}({opt1.get_attribute("value")})')
            print('101')
            key1 = opt1.text+'('+opt1.get_attribute('value')+')'
            print(f'key1: {key1}')
            category[key1] = {}
            if first_only == True:
                continue
            if level == 6:  # 쿠팡은 최대 6단계까지 있음
                continue
            if level == max_level:
                continue
            self.select_by_index(categories_xpath.format(level), idx1)
            print("waiting page loading...")
            time.sleep(2)
            self.wait_loading('//*[@id="page_progress"]')
            print(categories_xpath.format(level+1))
            try:
                e2 = self.driver.find_element(by=By.XPATH, value=categories_xpath.format(level+1)) # 다음 하위 분류
            except NoSuchElementException as e:
                print('더이상 하위 분류가 없습니다')
                print(e)
                continue
            style = e2.get_attribute('style')
            print('style', style)
            p = re.compile('display: (.+?);')
            m = p.search(style)
            if m:
                if 'block' in m.group(1): # block or inline-block
                    e2 = self.driver.find_element(by=By.XPATH, value=categories_xpath.format(level+1))
                    time.sleep(1)
                    d2 = Select(e2)
                    print('len options 2', len(d2.options))
                    if len(d2.options) > 1:
                        self.get_category_common(category[key1], False, categories_xpath, level+1, next_category_to_get, first_only, max_level)
                    else:
                        print('get_category_common continue 2')
                        continue
                else:
                    print('get_category_common continue 1')
                    continue
            else:
                e2 = self.driver.find_element(by=By.XPATH, value=categories_xpath.format(level+1))
                try:
                    d2 = Select(e2)
                except UnexpectedAlertPresentException as e:
                    print('이상한 분류:', e2.text)
                    alert = self.driver.switch_to.alert
                    alert.accept()
                    self.driver.switch_to.default_content
                    print(e)
                    continue
                print('len options 3: ', len(d2.options))
                if len(d2.options) > 1:
                    self.get_category_common(category[key1], False, categories_xpath, level+1, next_category_to_get, first_only, max_level)
                else:
                    print('get_category_common continue 3')
                    continue


    def set_easy_winner_category_arbitrary(self):
        self.set_url('https://mgr.easywinner.co.kr/admin/basic/category')   # 카테고리 지정 페이지
        e = self.driver.find_element(by=By.XPATH, value='//*[@id="category_l"]')    # 대분류
        es = e.find_elements(by=By.TAG_NAME, value='li')
        found_leaf = False
        for e in es:
            # print(e.text)
            e.click()
            e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="category_m"]')    # 중분류
            es1 = e1.find_elements(by=By.TAG_NAME, value='li')
            for e1 in es1:
                # print('------', e1.text)
                e1.click()
                if 'sub_non' in e1.get_attribute('class'):
                    found_leaf = True
                    break
                e2 = self.driver.find_element(by=By.XPATH, value='//*[@id="category_s"]')    # 소분류
                es2 = e2.find_elements(by=By.TAG_NAME, value='li')
                for e2 in es2:
                    # print('------------', e2.text)
                    e2.click()
                    if 'sub_non' in e2.get_attribute('class'):
                        found_leaf = True
                        break
                    found_leaf = True
                if found_leaf:
                    break
            if found_leaf:
                break

    def get_coupang_category(self, level1_category, first_only, pause):
        self.start_time = time.time()
        maker = '쿠팡'
        self.print_msg(f'{maker} 카테고리 가져오기 시작')
        self.category = {}

        e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="mall0184_5_V1"]') # 쿠팡
        e1.send_keys(Keys.ENTER)
        time.sleep(3)
        self.category[maker] = {}
        if level1_category == '전체':
            category_to_get = ''
        else:
            category_to_get = f"{level1_category}"
            # category_to_get = f"{level1_category}>계절환경가전>가습기/에어워셔/공기청정기>가습기"
        self.get_category_common(self.category[maker], False, '//*[@id="goodsCategory{0}"]', 1, category_to_get, first_only)

        self.print_msg(f'{maker} 카테고리 가져오기 완료')
        return self.category

    def get_smartstore_category(self, level1_category, first_only, pause):
        self.start_time = time.time()
        maker = '스마트스토어'
        self.print_msg(f'{maker} 카테고리 가져오기 시작')
        self.category = {}

        e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="mall0148_2_V1"]') # 스마트스토어
        e1.send_keys(Keys.ENTER)
        time.sleep(3)
        self.category[maker] = {}
        if level1_category == '전체':
            category_to_get = ''
        else:
            category_to_get = f"{level1_category}"        
        self.get_category_common(self.category[maker], False, '//*[@id="goodsCategory{0}"]', 1, category_to_get, first_only, 4)
        self.print_msg(f'{maker} 카테고리 가져오기 완료')
        return self.category

    def get_interpark_category(self, level1_category, first_only, pause):
        self.start_time = time.time()
        maker = '카페24'
        self.print_msg(f'{maker} 카테고리 가져오기 시작')
        self.category = {}

        e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="mall0284_4_V1"]') # 카페24
        e1.send_keys(Keys.ENTER)
        time.sleep(3)
        self.category[maker] = {}
        if level1_category == '전체':
            category_to_get = ''
        else:
            category_to_get = f"{level1_category}"
        self.get_category_common(self.category[maker], False, '//*[@id="goodsCategory{0}"]', 1, category_to_get, first_only, 4)
        self.print_msg(f'{maker} 카테고리 가져오기 완료')
        return self.category

    def get_11st_category(self, level1_category, first_only, pause):
        self.start_time = time.time()
        maker = '11번가'
        self.print_msg(f'{maker} 카테고리 가져오기 시작')
        self.category = {}

        e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="mall0025_1_V1"]') # 11번가
        e1.send_keys(Keys.ENTER)
        time.sleep(3)
        self.category[maker] = {}
        if level1_category == '전체':
            category_to_get = ''
        else:
            category_to_get = f"{level1_category}"
        self.get_category_common(self.category[maker], False, '//*[@id="goodsCategory{0}"]', 2, category_to_get, first_only, 5)
        self.print_msg(f'{maker} 카테고리 가져오기 완료')
        return self.category

    def get_category(self):
        self.start_time = time.time()
        self.print_msg('카테고리 가져오기 시작')
        self.category = {}
        self.set_url('https://mgr.easywinner.co.kr/admin/basic/category')   # 카테고리 지정 페이지
        e = self.driver.find_element(by=By.XPATH, value='//*[@id="category_l"]')    # 대분류
        es = e.find_elements(by=By.TAG_NAME, value='li')
        self.category['이지위너'] = {}
        for e in es:
            # print(e.text)
            self.category['이지위너'][e.text] = {}
            e.click()
            e1 = self.driver.find_element(by=By.XPATH, value='//*[@id="category_m"]')    # 중분류
            es1 = e1.find_elements(by=By.TAG_NAME, value='li')
            for e1 in es1:
                # print('------', e1.text)
                self.category['이지위너'][e.text][e1.text] = {}
                if 'sub_non' in e1.get_attribute('class'):
                    continue
                e1.click()
                e2 = self.driver.find_element(by=By.XPATH, value='//*[@id="category_s"]')    # 소분류
                es2 = e2.find_elements(by=By.TAG_NAME, value='li')
                for e2 in es2:
                    # print('------------', e2.text)
                    self.category['이지위너'][e.text][e1.text][e2.text] = {}
                    if 'sub_non' in e2.get_attribute('class'):
                        continue
                    e2.click()
                    e3 = self.driver.find_element(by=By.XPATH, value='//*[@id="category_d"]')    # 상세분류
                    es3 = e3.find_elements(by=By.TAG_NAME, value='li')
                    for e3 in es3:
                        # print('------------------', e3.text)
                        self.category['이지위너'][e.text][e1.text][e2.text][e3.text] = {}

        # print(self.category)
        self.print_msg('카테고리 가져오기 완료')
        return self.category

    def click_easywinner_category(self, xpath, category_name):
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        e = self.driver.find_element(by=By.XPATH, value=xpath)    # 대분류
        es = e.find_elements(by=By.TAG_NAME, value='li')
        for e in es:
            if e.text == category_name:
                # e.click()   # 이걸로 해야 함
                # e.send_keys(Keys.ENTER) # 에러 발생함
                self.driver.execute_script("arguments[0].click();", e)
                break

    def select_store(self, store_name, tag='V1', wait_time=5):
        print(f'select_store: wait_time={wait_time} sec')
        if store_name == '스마트스토어':
            xpath = f'//*[@id="mall0148_2_{tag}"]'
        elif store_name == '쿠팡':
            xpath = f'//*[@id="mall0184_5_{tag}"]'
        elif store_name == '지마켓':
            xpath = f'//*[@id="mall0010_3_{tag}"]'
        elif store_name == '11번가':
            xpath = f'//*[@id="mall0025_1_{tag}"]'
        elif store_name == '옥션':
            xpath = f'//*[@id="mall0003_0_{tag}"]'
        elif store_name == '카페24':
            xpath = f'//*[@id="mall0284_4_{tag}"]'

        e1 = self.driver.find_element(by=By.XPATH, value=xpath)
        e1.send_keys(Keys.ENTER)
        time.sleep(wait_time)

    def select_store_category(self, xpath, category_name):
        print('select_store_category')
        print(category_name)
        p = re.compile('\((.*)\)')
        m = p.search(category_name)
        print(m.group(1))
        self.select_by_value(xpath, m.group(1))
        self.wait_loading('//*[@id="page_progress"]', 2)

    def delete_category(self, mall='스마트스토어', tag = 'V1'):
        if mall == '스마트스토어':
            xpath = '//*[@id="mall0148"]/input[3]'
        elif mall == '쿠팡':
            xpath = f'//*[@id="mall0184_5_{tag}"]'
        elif mall == '지마켓':
            xpath = '//*[@id="mall0271"]/input[3]'
        elif mall == '11번가':
            xpath = '//*[@id="mall0025"]/input[3]'
        elif mall == '옥션':
            xpath = '//*[@id="mall0270"]/input[3]'
        elif mall == '카페24':
            xpath = '//*[@id="mall0284"]/input[3]'
        else:
            return

        # main_page = self.driver.current_window_handle

        e1 = self.driver.find_element(by=By.XPATH, value=xpath)
        e1.send_keys(Keys.ENTER)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')

            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert accepted")
            return False
        except TimeoutException:
            print("no alert")
        
        self.driver.switch_to.default_content
                        
    def complete_selection_v2(self):
        print('complete_selection_v2')

        time.sleep(self.loading_wait_time)
        # 신상품 영역 체크
        xpath = '//*[@id="new"]'
        e1 = self.driver.find_element(by=By.XPATH, value=xpath)
        e1.click()
        # self.click(xpath)
        time.sleep(self.loading_wait_time)

        # 추천상품 영역 체크
        xpath = '//*[@id="recommend"]'
        e1 = self.driver.find_element(by=By.XPATH, value=xpath)
        e1.click()
        # self.click(xpath)
        time.sleep(self.loading_wait_time)

        # 추가버튼 클릭
        xpath = '//*[@id="ctry_sel"]/input[2]'
        e1 = self.driver.find_element(by=By.XPATH, value=xpath)
        e1.click()

        # 확정 버튼 클릭
        xpath = '//*[@id="btn_mall_category_selection"]'
        e1 = self.driver.find_element(by=By.XPATH, value=xpath)
        e1.click()
        # self.click(xpath)
        time.sleep(self.loading_wait_time)

        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')

            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert accepted")
            return False
        except TimeoutException:
            print("no alert")

    def complete_selection(self):
        xpath = '//*[@id="btn_mall_category_selection"]'
        e1 = self.driver.find_element(by=By.XPATH, value=xpath)
        e1.click()        

        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')

            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert accepted")
            return False
        except TimeoutException:
            print("no alert")

    def register(self, tag, smartstore, coupang, gmarket, m11st, auction, cafe24):
        self.start_time = time.time()
        self.print_msg('카테고리 등록 시작')

        smartstore_category_xpath = '//*[@id="goodsCategory{0}"]'
        smartstore_category = smartstore.split('>')[1:]

        coupang_category_xpath = smartstore_category_xpath
        coupang_category = coupang.split('>')[1:]
        coupang_category = [x.replace(")", "|)") for x in coupang_category] # 이상하게 숫자뒤에 '|'가 붙어 있음

        gmarket_esm_category_xpath = '//*[@id="goodsCategory{0}"]'  # level 1~5
        gmarket_category_xpath = '//*[@id="disp_goodsCategory{0}"]' # level 6~9
        gmarket_category = gmarket.split('>')[1:]

        m11st_category_xpath = smartstore_category_xpath
        m11st_category = m11st.split('>')[1:]

        auction_esm_category_xpath = gmarket_esm_category_xpath
        auction_category_xpath = gmarket_category_xpath
        auction_category = auction.split('>')[1:]

        cafe24_category_xpath = smartstore_category_xpath
        cafe24_category = cafe24.split('>')[1:]

        if coupang != "":
            self.select_store('쿠팡', tag)
            time.sleep(4) # 이거 기다리는 시간 꼭 필요함. 첫번째 아이템을 너무 빨리 선택하면 두번째 아이템이 갱신되지 않음.
            for level, value in enumerate(coupang_category):
                self.select_store_category(coupang_category_xpath.format(level+1), coupang_category[level])
            self.complete_selection()

        if smartstore != "":
            self.select_store('스마트스토어', tag)
            time.sleep(4) # 이거 기다리는 시간 꼭 필요함. 첫번째 아이템을 너무 빨리 선택하면 두번째 아이템이 갱신되지 않음.
            for level, value in enumerate(smartstore_category):
                self.select_store_category(smartstore_category_xpath.format(level+1), smartstore_category[level])
            self.complete_selection()

        if gmarket != "":
            self.select_store('지마켓', tag)
            time.sleep(4) # 이거 기다리는 시간 꼭 필요함. 첫번째 아이템을 너무 빨리 선택하면 두번째 아이템이 갱신되지 않음.
            for level, value in enumerate(gmarket_category):
                if level < 5:
                    if gmarket_category[level] in ["최종분류", "없음"]:
                        continue
                    self.select_store_category(gmarket_esm_category_xpath.format(level+1), gmarket_category[level])
                else:
                    self.select_store_category(gmarket_category_xpath.format(level-4), gmarket_category[level])
            self.complete_selection()

        if m11st != "":
            self.select_store('11번가', tag)
            time.sleep(4) # 이거 기다리는 시간 꼭 필요함. 첫번째 아이템을 너무 빨리 선택하면 두번째 아이템이 갱신되지 않음.
            for level, value in enumerate(m11st_category):
                self.select_store_category(m11st_category_xpath.format(level+2), m11st_category[level])
            self.complete_selection()

        if auction != "":
            self.select_store('옥션', tag)
            time.sleep(4) # 이거 기다리는 시간 꼭 필요함. 첫번째 아이템을 너무 빨리 선택하면 두번째 아이템이 갱신되지 않음.
            for level, value in enumerate(auction_category):
                if level < 5:
                    if auction_category[level] in ["최종분류", "없음"]:
                        continue
                    self.select_store_category(auction_esm_category_xpath.format(level+1), auction_category[level])
                else:
                    self.select_store_category(auction_category_xpath.format(level-4), auction_category[level])
            self.complete_selection()

        if cafe24 != "":
            self.select_store('카페24', tag)
            time.sleep(4) # 이거 기다리는 시간 꼭 필요함. 첫번째 아이템을 너무 빨리 선택하면 두번째 아이템이 갱신되지 않음.
            for level, value in enumerate(cafe24_category):
                self.select_store_category(cafe24_category_xpath.format(level+1), cafe24_category[level])
            self.complete_selection_v2()

        # time.sleep(5)
        # self.driver.refresh()

        self.print_msg('카테고리 등록 완료')
        return {'test':'success'}


    def register_shoplinker(self):
        print('register_shoplinker')
        self.goto_category_mapping()

        # 카테고리 매칭 창에서 작업 시작
        xpath_auction = '//*[@id="mall0003_0_V2"]'

        # 스마트 스토어
        xpath_smartstore = '//*[@id="mall0148_2_V2"]'
        self.click(xpath_smartstore)
        smartstore = '스마트스토어>식품(50000006)>음료(50000148)>청량/탄산음료(50001079)>콜라(50002254)'
        smartstore_category_xpath = '//*[@id="goodsCategory{0}"]'
        smartstore_category = smartstore.split('>')[1:]
        time.sleep(4) # 이거 기다리는 시간 꼭 필요함. 첫번째 아이템을 너무 빨리 선택하면 두번째 아이템이 갱신되지 않음.
        if smartstore != "":
            for level, value in enumerate(smartstore_category):
                self.select_store_category(smartstore_category_xpath.format(level+1), smartstore_category[level])
            self.complete_selection_shoplinker()
        else:   # 삭제
            self.delete_category('스마트스토어')

    def goto_category_mapping(self):
        print('goto_category_mapping')
        # self.click('//*[@id="topnav"]/li[2]/a')

        # Find all frames on the page
        frames = self.driver.find_elements(By.TAG_NAME, "frame")  # Use 'frame' for <frame> tags
        print(f"Total frames found: {len(frames)}")

        # Iterate through frames and print their attributes
        for index, frame in enumerate(frames):
            frame_id = frame.get_attribute("id")
            frame_name = frame.get_attribute("name")
            frame_src = frame.get_attribute("src")
            print(f"Frame {index}: ID={frame_id}, Name={frame_name}, Src={frame_src}")

        # switch to main frame. https://ad2.shoplinker.co.kr/admin/main
        self.driver.switch_to.frame(2)  # Switch to the 3rd frame (index starts at 0)

        try:
            xpath_popup = '//*[@id="evt1129"]/div[2]/label/input'
            self.check_checkbox(xpath_popup)
        except Exception:
            pass

        xpath = '/html/body/div[2]/ul/li[2]/a'
        xpath1 = '/html/body/div[2]/ul/li[2]/div/div/ul/li[5]/a'
        # print(self.driver.page_source)
        element_to_hover_over = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))  # Replace with your locator
        )        
        # element_to_hover_over = self.driver.find_element(by=By.XPATH, value=xpath)
        element_to_hover_over1 = self.driver.find_element(by=By.XPATH, value=xpath1)

        hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
        hover.perform()

        # time.sleep(2)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath1))
        )
        hover.move_to_element(element_to_hover_over1)
        hover.perform()
        time.sleep(2)
        self.click(xpath1)

        # time.sleep(5)

        # 카테고리 매치하기 버튼 클릭
        xpath2 = '//*[@id="search_form"]/table/tbody/tr[3]/td/a'
        self.click(xpath2)
        # time.sleep(5)

        # Wait for the new window to open
        self.driver.implicitly_wait(5)  # Optional: Add an explicit wait for better control

        # Get all window handles
        window_handles = self.driver.window_handles

        # Switch to the newly opened window (usually the last in the list)
        self.driver.switch_to.window(window_handles[-1])

        # Perform actions in the popup window
        print(self.driver.title)  # Example: Print the title of the popup window

        # 카테고리 매칭 내용이 많으면 대기시간이 오래 걸림. page_progress 가 없어질 때까지 대기
        self.wait_loading('//*[@id="page_progress"]', 2)