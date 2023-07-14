from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from selenium.webdriver.chrome.options import Options
import os
 

# (0: Monday, 1: Tuesday, ..., 6: Sunday)
def get_next_desired_date(desired_date: int):
    current_date = datetime.date.today()
    days_ahead = (desired_date - current_date.weekday()) % 7
    if days_ahead == 0:
        days_ahead += 7
    return current_date + datetime.timedelta(days=days_ahead)

def get_current_day():
    current_date = datetime.date.today()
    return current_date.weekday()

def write_file(filename, data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:          
            f.write('\n' + data)   
    else:
        with open(filename, 'w') as f:                   
            f.write(data)


# (0: Monday, 1: Tuesday, ..., 6: Sunday)

classes = {2: 'bookings-timetable-timetableitem-wod-squad-int-1830', 4: 'bookings-timetable-timetableitem-strongman-0745'}

login_url = "https://gymbox.legendonlineservices.co.uk/enterprise/account/login"


options = Options()
options.add_argument('--headless=new')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

def book():
    try:
        current_day_number = get_current_day()
        desired_date = get_next_desired_date(current_day_number)

        if(not current_day_number in classes):
            write_file('/Users/nelson/projects/gymboxBot/success.txt', "No desired classes today :  " + str(datetime.datetime.now()))
            return

        desired_class = classes[current_day_number]

        classes_url = f"https://gymbox.legendonlineservices.co.uk/enterprise/bookingscentre/membertimetable#Search?LocationIds=1255&ActivityIds=93,95,99,343&SearchDate={desired_date}"

        driver.get(login_url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, "account-login-email")))

        username_input = driver.find_element(By.ID, 'account-login-email')
        password_input = driver.find_element(By.ID, 'account-login-password')

        # add username
        username_input.send_keys('')
        # add password
        password_input.send_keys('')

        password_input.send_keys(Keys.RETURN)

        time.sleep(3)

        driver.get(classes_url)

        desired_class_element = f"[data-test-id='{desired_class}']"

        # print("Desired class element: ", desired_class_element)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, desired_class_element)))
        activity_link = driver.find_element(By.CSS_SELECTOR, desired_class_element)

        activity_link.click()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn-primary")))

        buy_now =  driver.find_element(By.CSS_SELECTOR, "button.btn-primary")

        buy_now.click()

        wait.until(EC.visibility_of_element_located((By.ID, "universal-basket-continue-button")))

        continue_button =  driver.find_element(By.ID, "universal-basket-continue-button")

        continue_button.click()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test-id='shared-checkbox-i-accept-the-terms-&-conditions-input']")))

        t_and_cs =  driver.find_element(By.CSS_SELECTOR, "[data-test-id='shared-checkbox-i-accept-the-terms-&-conditions-input']")

        t_and_cs.click()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test-id='universalbasket-paymentsummary-continueoptions-continue']")))

        confirm_button = t_and_cs =  driver.find_element(By.CSS_SELECTOR, "[data-test-id='universalbasket-paymentsummary-continueoptions-continue']")

        confirm_button.click()

        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-test-id='shared-header']"), "Confirmation"))

        write_file('/Users/nelson/projects/gymboxBot/success.txt', "booked! :  " + str(datetime.datetime.now()))
        driver.quit()
    except:
        write_file('/Users/nelson/projects/gymboxBot/error.txt', "failed to book: " + str(datetime.datetime.now()))
        driver.quit()

if __name__ == "__main__":
    book()