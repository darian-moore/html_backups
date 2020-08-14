import os
import requests
import concurrent.futures
import shutil
import time
from colorama import init, Back, Fore, Style
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
init(convert=True) #problem with colorama not working properly

def main():
    # Starting the timer
    start = time.time()

    cwd = os.getcwd()
    # Setting up drivers for anyone to use
    driver1 = webdriver.Chrome(ChromeDriverManager().install())
    driver2 = webdriver.Chrome(ChromeDriverManager().install())
    driver3 = webdriver.Chrome(ChromeDriverManager().install())
    driver4 = webdriver.Chrome(ChromeDriverManager().install())

    # List of tabs that require buttons to be clicked
    special_tabs = ['aliases', 'import-mappings', 'materials']
    
    # Multi-threading to execute functions all at once
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(save_regular_tabs, driver1, special_tabs, cwd)
        executor.submit(save_special_tabs, driver2, special_tabs, cwd)
        executor.submit(save_filters_tab, driver3, cwd)
        executor.submit(save_project_roles_tab, driver4, cwd)

    # Ending the timer and printing how long the program took
    end = time.time()
    timeTracking(start, end)

def save_regular_tabs(driver1, special_tabs, cwd):
    '''
    Saving HTML for the project roles tab
    Inputs:
    - driver1, webdriver to launch and interact with a webpage (driver object)
    - special_tabs, list of certain tabs that require different steps to collect all data (list)
    - cwd, current working directory (string)
    '''
    # Logging into Stratus
    driver1.get('https://www.gtpstratus.com/companyadmin#tab_aliases')
    driver1.set_window_position(-2000, 0) #move the window off the screen
    login(driver1)
    time.sleep(1)

    driver1.find_element_by_xpath('//a[@href="#aliases"]').click()
    time.sleep(0.25)
    driver1.refresh()
    time.sleep(0.25)

    tabs = driver1.find_elements_by_xpath('//a[@data-toggle="tab"]')

    for tab in tabs:
        tab.click()
        time.sleep(0.5)

        tab_name = (tab.text).lower().replace(' ', '-')

        show_all(driver1, tab_name)

        if tab_name in special_tabs or tab_name == 'project-roles' or tab_name == 'templates' or tab_name == 'filters':
            pass
        elif tab_name == 'naming-and-numbering':
            save(tab_name, driver1, '(naming-conventions)')
            shutil.move((cwd+'\\'+tab_name+'(naming-conventions).html'), ("S:\\Stratus\\Backups\\"+tab_name+"(naming-conventions).html"))
            headers = driver1.find_elements_by_xpath('//button[@class="h3 btn btn-sm btn-primary margin-v-5 col-sm-3"]')
            for header in headers:
                header.click()
                time.sleep(1)
                save(tab_name, driver1, '('+header.text.lower().replace(' ', '-')+')')
                shutil.move((cwd+'\\'+tab_name+'('+header.text.lower().replace(' ', '-')+').html'), ("S:\\Stratus\\Backups\\"+tab_name+'('+header.text.lower().replace(' ', '-')+").html"))
        else:
            save(tab_name, driver1)
            shutil.move((cwd+'\\'+tab_name+'.html'), ("S:\\Stratus\\Backups\\"+tab_name+".html"))

    driver1.quit()

def save_special_tabs(driver2, special_tabs, cwd):
    '''
    Saving HTML for the project roles tab
    Inputs:
    - driver2, webdriver to launch and interact with a webpage (driver object)
    - special_tabs, list of certain tabs that require different steps to collect all data (list)
    - cwd, current working directory (string)
    '''
    start = time.time()

    # Logging into Stratus
    driver2.get('https://www.gtpstratus.com/companyadmin#tab_aliases')
    driver2.set_window_position(-2000, 0) #move the window off the screen
    login(driver2)
    time.sleep(1)

    for name in special_tabs:
        start  = time.time()

        driver2.refresh()
        tab = driver2.find_element_by_xpath('//a[@href="#'+name+'"]')
        tab.click()
        time.sleep(1.5)

        show_all(driver2, name)

        expanding_buttons = driver2.find_elements_by_xpath('//div[@id="'+name+'-table"]//button[@title="Expand"]')

        for button in expanding_buttons:
            if name != 'aliases':
                time.sleep(0.5)

            try:
                button.click()
            except exceptions.ElementClickInterceptedException:
                time.sleep(1)
                button.click()

            if name == 'filters':
                loading = driver2.find_elements_by_xpath('//div[@id="'+name+'-table"]//button[@class="btn btn-dt-expander btn-primary loader"]')
                while len(loading) >= 1:
                    loading = driver2.find_elements_by_xpath('//div[@id="'+name+'-table"]//button[@class="btn btn-dt-expander btn-primary loader"]')

        if name == 'aliases':
            wait(name, ""'//a[@class="btn btn-default buttons-csv buttons-html5"]'"", driver2, expanding_buttons)
        elif name == 'import-mappings':
            wait(name, ""'//td[@colspan="5"]//a[@class="btn btn-default buttons-csv buttons-html5"]'"", driver2, expanding_buttons)
        elif name == 'materials':
            wait(name, ""'//div[@class="col-sm-12"]//button[@class="btn btn-success"]'"", driver2, expanding_buttons)
        else:
            pass

        save(name, driver2)
        shutil.move((cwd+'\\'+name+'.html'), ("S:\\Stratus\\Backups\\"+name+'.html'))

        end = time.time()
        timeTracking(start, end, name+' tab')

    driver2.quit()

    end = time.time()
    timeTracking(start, end, 'save_special_tabs function')

def save_filters_tab(driver3, cwd):
    '''
    Saving HTML for the filter tab
    Inputs:
    - driver3, webdriver to launch and interact with a webpage (driver object)
    - cwd, current working directory (string)
    '''
    start = time.time()

    # Logging into Stratus
    driver3.get('https://www.gtpstratus.com/companyadmin#tab_aliases')
    driver3.set_window_position(-2000, 0) #move the window off the screen
    login(driver3)
    time.sleep(1)

    driver3.find_element_by_xpath('//a[@href="#filters"]').click()
    time.sleep(0.25)
    driver3.refresh()
    time.sleep(0.25)

    show_all(driver3, 'filters')

    expanding_buttons = driver3.find_elements_by_xpath('//div[@id="filters-table"]//button[@title="Expand"]')

    for button in expanding_buttons:
        time.sleep(0.5)

        try:
            button.click()
        except exceptions.ElementClickInterceptedException:
            time.sleep(1)
            button.click()

        loading = driver3.find_elements_by_xpath('//div[@id="filters-table"]//button[@class="btn btn-dt-expander btn-primary loader"]')
        while len(loading) >= 1:
            loading = driver3.find_elements_by_xpath('//div[@id="filters-table"]//button[@class="btn btn-dt-expander btn-primary loader"]')

    save('filters', driver3)
    shutil.move((cwd+'\\'+'filters.html'), ("S:\\Stratus\\Backups\\"+'filters.html'))

    end = time.time()
    timeTracking(start, end, 'save_filters_tab function')

    driver3.quit()

def save_project_roles_tab(driver4, cwd):
    '''
    Saving HTML for the project roles tab
    Inputs:
    - driver4, webdriver to launch and interact with a webpage (driver object)
    - cwd, current working directory (string)
    '''
    start = time.time()

    # Logging into Stratus
    driver4.get('https://www.gtpstratus.com/companyadmin#tab_aliases')
    driver4.set_window_position(-2000, 0) #move the window off the screen
    login(driver4)
    time.sleep(1)

    driver4.find_element_by_xpath('//a[@href="#project-roles"]').click()
    time.sleep(0.25)
    driver4.refresh()
    time.sleep(1)

    expand_all = driver4.find_element_by_xpath('//*[@id="project-roles"]/div/div[2]/div/div/div[1]/div[1]/button[1]')
    while bool(expand_all) != True:
        expand_all = driver4.find_element_by_xpath('//*[@id="project-roles"]/div/div[2]/div/div/div[1]/div[1]/button[1]')
    expand_all.click()
    
    ready = (bool(driver4.find_element_by_xpath('//span[@class="glyphicon glyphicon-chevron-up"]')))
    while ready != True:
        ready = (bool(driver4.find_element_by_xpath('//span[@class="glyphicon glyphicon-chevron-up"]')))
    save('project-roles', driver4)
    shutil.move((cwd+'\\'+'project-roles.html'), ("S:\\Stratus\\Backups\\"+'project-roles.html'))

    driver4.quit()

    end = time.time()
    timeTracking(start, end, 'save_project_roles_tab function')

def wait_click(driver, sec, element, key, x, value = "", count = 0):
    '''
    Uses try and except to catch any errors when waiting to click elements on the webpage
    Inputs:
    - driver, webdriver to launch and interact with a webpage (driver object)
    - sec, amount of seconds to wait before throwing an error (int)
    - element, the type attribute we are trying to click (attribute)
    - key, the value of an element's attribute like name, class, xpath, etc. (string)
    - x, True or False (boolean)
    - value, string to send to the webpage to be used in a search box for an example (string)
    - count, used for error control (int)
    '''
    try:
        if x:
            WebDriverWait(driver,sec).until(EC.element_to_be_clickable((element, key))).send_keys(value)
        else:
            WebDriverWait(driver,sec).until(EC.element_to_be_clickable((element,key))).click()
    except (exceptions.TimeoutException, exceptions.ElementClickInterceptedException, exceptions.StaleElementReferenceException):
        if count < 3:
            print(Fore.RED+"\nERROR: UNABLE TO CLICK ELEMENT ("+str(count+1)+"/3 ATTEMPTS)"+Style.RESET_ALL)
            wait_click(driver, sec, element, key, x, value, count+1)

def login(driver):
    '''
    Logging into website
    Inputs:
    - driver, webdriver to launch and interact with a webpage (driver object)
    '''
    email = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASSWORD')

    wait_click(driver, 10, By.NAME, 'email', True, email)
    wait_click(driver, 10, By.NAME, 'password', True, password)
    wait_click(driver, 10, By.XPATH, '//*[@id="auth0-lock-container-1"]/div/div[2]/form/div/div/button/span', False)
    wait_click(driver, 10, By.XPATH, '//*[@id="company-admin-page"]/div[1]/ul/li[9]/a', False)

def show_all(driver, tab_name):
    '''
    Clicks all buttons on the page that expand down to reveal more content
    Inputs:
    - driver, webdriver to launch and interact with a webpage (driver object)
    - tab_name, the current tab name in the special tabs list (string)
    '''
    if tab_name == 'app-keys':
        tab_name = tab_name.replace('-', '')
        tab_name = 'company-'+tab_name
    
    # Selecting as many items as possible to view on one page
    try:
        driver.find_element_by_xpath('//div[@id="'+tab_name+'"]//option[@value="All"]').click()
    except exceptions.NoSuchElementException:
        try:
            driver.find_element_by_xpath('//div[@id="'+tab_name+'"]//option[@value="-1"]').click()
        except exceptions.NoSuchElementException:
            try:
                driver.find_element_by_xpath('//div[@id="'+tab_name+'"]//option[@value="100"]').click()
            except exceptions.NoSuchElementException:
                pass

def tData(xpath, driver, x):
    '''
    Creates a list of all elements based off of an xpath
    Inputs:
    - xpath, the xpath for a target element(s)
    - driver, webdriver to launch and interact with a webpage (driver object)
    - x, True or False (boolean)
    Returns: list of all elements found in the HTML with the given xpath
    '''
    if x:
        elems = driver.find_elements_by_xpath(xpath)
        elems_list = []
        for elem in elems:
            if elem != '' or elem != ' ':
                elems_list.append(elem.text)
            else:
                elems_list.append('null')
    else:
        elems = driver.find_elements_by_xpath(xpath)
        elems_list = []
        for elem in elems:
            elems_list.append(elem.get_attribute('checked'))
        
    return elems_list

def timeTracking(start, end, phrase = "Program"):
    '''
    Used to see how fast the program is running
    Inputs:
    - start, the program start time (float)
    - end, the program end time (float)
    - phrase, optional param to specify what you are timing (string)
    '''
    run_time = int(end-start)
    if run_time >= 60 and run_time < 3600:
        minute = int(run_time/60)
        sec = int(run_time%60)
        print('\n'+phrase+' finished in '+Fore.GREEN+str(minute)+'m '+Style.RESET_ALL+'and '+Fore.GREEN+str(sec)+'s'+Style.RESET_ALL)
    elif run_time >= 3600:
        hour = int(run_time/3600)
        minute = int((run_time%3600)/60)
        sec = int((run_time%3600)%60)
        print('\n'+phrase+' finished in '+Fore.YELLOW+str(hour)+'hr '+Fore.GREEN+str(minute)+'m '+Style.RESET_ALL+'and '+\
            Fore.GREEN+str(sec)+'s'+Style.RESET_ALL)
    else:
        print('\n'+phrase+' finished in '+Fore.GREEN+str(run_time)+'s'+Style.RESET_ALL)

def wait(name, xpath, driver, expanding_buttons):
    '''
    Wait for the content to load after a dropdown button is clicked
    Inputs:
    - name, the name of the current tab (string)
    - xpath, the xpath for a target element
    - driver, webdriver to launch and interact with a webpage (driver object)
    - expanding_buttons, total number of buttons to click that loads content (int)
    '''
    if name == 'materials':
        loading_buttons = len(driver.find_elements_by_xpath(xpath))
        while loading_buttons != len(expanding_buttons):
            loading_buttons = len(driver.find_elements_by_xpath(xpath))
    else:
        loading_buttons = len(driver.find_elements_by_xpath(xpath))
        while loading_buttons != len(expanding_buttons):
            loading_buttons = len(driver.find_elements_by_xpath(xpath))
    time.sleep(10)

def save(tab_name, driver, header = ''):
    '''
    Saving the HTML of the current web page
    Inputs:
    - tab_name, the current tab name in the special tabs list (string)
    - driver, webdriver to launch and interact with a webpage (driver object)
    - header, optional param to add additional text to the file name (string)
    '''
    try:
        with open(tab_name+header+'.html', 'w') as f:
            f.write(driver.page_source)
    except:
        print(Fore.RED+tab_name+' tab failed to back up'+Style.RESET_ALL)

if __name__ == "__main__":
    main()
