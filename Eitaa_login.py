from selenium import webdriver # type: ignore
import pickle
from time import time, sleep
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import NoSuchElementException, TimeoutException # type: ignore


def login(driver):
    # options = webdriver.ChromeOptions()
    # options.add_argument(r"user-data-dir=C:\Selenium")
    # options.add_argument("profile-directory=Default")

    # driver = webdriver.Chrome(options=options)

    # driver.get('https://web.eitaa.com')
    holder = False

    try:
        number_field = WebDriverWait(driver, 20).until(lambda d: d.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[1]/div/div[3]/div[2]/div[1]'))
        user_number = input("Enter your phone number : (No +98 no 0 ,e.g. : 9114445555) :\n")
        while len(user_number) != 10 or not user_number.isdigit():
            print("Invalid number. Please enter the number correctly this time.")
            user_number = input("Enter your phone number : (No +98 no 0 ,e.g. : 9114445555) :\n")

        number_field.send_keys(user_number)
        driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[1]/div/div[3]/button/div').click()
    except TimeoutException:
        verification_code = input("The code has already been sent\nEnter the 5-digit verification code sent to your phone: ")

        while len(verification_code) != 5 or not verification_code.isdigit():
            print("Invalid code. Please enter a 5-digit number.")
            verification_code = input("Enter the 5-digit verification code sent to your phone: ")


        WebDriverWait(driver, 10).until(driver.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[3]/div/input').send_keys(verification_code))
        holder = True
    except Exception as e:
        print(e)
        print('\n---------------------------------------------\n')
        return False

    if holder:
        pass
    else:
        verification_code = input("Enter the 5-digit verification code sent to your phone: ")
        while len(verification_code) != 5 or not verification_code.isdigit():
            print("Invalid code. Please enter a 5-digit number.")
            verification_code = input("Enter the 5-digit verification code sent to your phone: ")


        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[3]/div/input').send_keys(verification_code))

    sleep(10)
    return True

if __name__ == "__main__":
    login()