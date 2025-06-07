from io import BytesIO
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from persiantools.jdatetime import JalaliDate
import base64, logging
from Eitaa_login import login
import os

# Set up basic logging configuration
logging.basicConfig(level=logging.ERROR,
                    format='%(levelname)s: %(message)s')

logging.basicConfig(level=logging.DEBUG)

def verifyLogin(driver):
    # I made the chat sidebar of the Eitaa WebAPP as my identifier if the user is logged in, your welcome to change it to whatever you want
    try:
        check_sidebar_exist = WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="chatlist-container"]/div[2]/div[1]')
        )
        # driver.find_element(By.XPATH, '//*[@id="chatlist-container"]/div[2]/div[1]')
        print("\n --Logged In-- \n")
    except TimeoutException:
        print("please Log in first........")
        try:
            login(driver)
            # driver.refresh()
            return True
        except Exception as e:
            logging.exception(f"An unexpected error occurred in login(): {e}")
            return False
    except Exception as e:
        logging.exception(f"An unexpected error occurred in verifyLogin(): {e}")
        return False

    return True

def target_user(driver):
    # data-peer-id is a CSS selector that is specific to each user find it using inspect in any browser and replace the number
    unread_message = False
    unread_message_detector = False
    try:
        user_element = WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.CSS_SELECTOR ,'[data-peer-id="1231229"]') # majid data peer id 1231229 , Babak data peer id 19771465
        )   
        try:
            unread_message_detector = user_element.find_element(By.XPATH, "//*[@id='folders-container']/div[1]/div[1]/ul[2]/li[1]/div[2]/p[2]/div[contains(@class, 'unread') and contains(@class, 'is-visible')]")
            user_name = user_element.find_element(By.CLASS_NAME, "peer-title")
            print(f"You have an unread message from : {user_name}")
            unread_message = True
            return unread_message
        except NoSuchElementException:
            print(f"There is no unread messages from : {user_name}")
        finally:
            if unread_message_detector:
                print("You have an unread message")
                unread_message = True
            user_element.click()
            return unread_message
    except TimeoutException as e:
        logging.error(f"Timeout occurred in login(): {e}")
        return 1
    except Exception as e:
        print(e)
        return 1


def message_box_finder(driver):
    message_box = WebDriverWait(driver, 20).until(
        lambda d: d.find_element(By.XPATH, '//*[@id="column-center"]/div/div/div[4]/div/div[1]/div[7]/div[1]/div[1]')
    )
    driver.execute_script("arguments[0].scrollIntoView();", message_box)
    message_box.click()
    sleep(1)

    return message_box

def find_clear_message_box(driver):
    try:
        message_box = WebDriverWait(driver, 20).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="column-center"]/div/div/div[4]/div/div[1]/div[7]/div[1]/div[1]')
        )
        driver.execute_script("arguments[0].scrollIntoView();", message_box)
        message_box.click()
        sleep(1)

        # delete drafted messages
        message_box.send_keys(Keys.CONTROL, 'a')  # Select all text
        message_box.send_keys(Keys.BACKSPACE)  # Delete everything
        print("Message field cleared.")
        sleep(1)

        return message_box
    except TimeoutException as e:
        logging.error(f"Timeout occurred in login(): {e}")
        return 1
    except Exception as e:
        logging.error(f"An unexpected error occurred in find_clear_message_box(): {e}")
        return 1



def send_message_button(driver):
    try:
        send_button = driver.find_element(By.XPATH, '//*[@id="column-center"]/div/div/div[4]/div/div[4]/button/div')
        send_button.click()
        # clicks the send button which send your message
        return 0
    except TimeoutException as e:
        logging.error(f"Timeout occurred in login(): {e}")
        return 1
    except Exception as e:
        logging.exception(f"An unexpected error occurred in send_message_button(): {e}")
        return 1




def passing_file_fields(driver):
    try:
        message_title = WebDriverWait(driver, 20).until(
            lambda d: d.find_element(By.XPATH, '/html/body/div[5]/div/div[3]/div[1]')
        )
        message_title.send_keys(f'لیست قیمت {JalaliDate.today()}')
        return 0
    except TimeoutException as e:
        logging.error(f"Timeout occurred in login(): {e}")
        return 1
    except NoSuchElementException as e:
        logging.exception(f"Element not found in passing_file_fields(): {e}")
        return 1
    except Exception as e:
        logging.exception(f"An unexpected error occurred in passing_file_fields(): {e}")
        return 1

# def passing_file(driver, prices_pdf):
    print(f"prices_pdf is of type: {type(prices_pdf)}")
    print(f"prices_pdf value: {prices_pdf}")

    if prices_pdf is None or not os.path.exists(prices_pdf):
        raise ValueError("Error: prices_pdf is None or does not exist!")

    print("Trying to send the file.....")        

    # path for the file you want to send if you have one
    # path_to_file = r'D:\babak\In progress\Babak\DEV\Projects\Web scraping\Eitaa-Web-APP-API\.gitignore' # path for work laptop
    

    if isinstance(prices_pdf, BytesIO):
        file_data = prices_pdf.getvalue()  # Read directly from BytesIO
    elif isinstance(prices_pdf, str):
        with open(prices_pdf, "rb") as file:
            file_data = file.read()
    else:
        raise TypeError("prices_pdf must be a file path (str) or a file-like object (BytesIO)")

    base64_file = base64.b64encode(file_data).decode("utf-8")

    print("running javascript for passing the file....")
    try: 
        js_script = f"""
        async function pasteFile() {{
            // Decode the Base64 file data back into a Blob
            let byteCharacters = atob("{base64_file}");
            let byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {{
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }}
            let byteArray = new Uint8Array(byteNumbers);
            let blob = new Blob([byteArray], {{ type: "application/pdf" }});

            // Create a File object
            let file = new File([blob], "test.txt", {{ type: blob.type }});

            // Use DataTransfer API
            let dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);

            // Dispatch a paste event
            let event = new ClipboardEvent("paste", {{
                bubbles: true, 
                cancelable: true,
                clipboardData: dataTransfer
            }});

            document.dispatchEvent(event);
        }}

        pasteFile();
        """
        print("JavaScript finished....")

        sleep(0.5)

        print("Executing JavaScript....")
        driver.execute_script(js_script)
        print("JavaScript Done!")

        return 0
    except TimeoutException as e:
        logging.error(f"Timeout occurred in login(): {e}")
        return 1
    except Exception as e:
        logging.exception(f"An unexpected error occurred in passing_file(): {e}")
        return 1

def passing_file(driver, prices_pdf):
    print(f"prices_pdf is of type: {type(prices_pdf)}")
    print(f"prices_pdf value: {prices_pdf}")

    if prices_pdf is None or not os.path.exists(prices_pdf):
        raise ValueError("Error: prices_pdf is None or does not exist!")

    print("Trying to send the file.....")        

    if isinstance(prices_pdf, BytesIO):
        file_data = prices_pdf.getvalue()  # Read directly from BytesIO
        file_name = "prices.pdf"
        mime_type = "application/pdf"
    elif isinstance(prices_pdf, str):
        with open(prices_pdf, "rb") as file:
            file_data = file.read()
        file_name = os.path.basename(prices_pdf)
        mime_type = "application/pdf"
    else:
        raise TypeError("prices_pdf must be a file path (str) or a file-like object (BytesIO)")

    base64_file = base64.b64encode(file_data).decode("utf-8")

    print("running javascript for passing the file....")
    try: 
        js_script = f"""
        async function pasteFile() {{
            let byteCharacters = atob("{base64_file}");
            let byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {{
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }}
            let byteArray = new Uint8Array(byteNumbers);
            let blob = new Blob([byteArray], {{ type: "{mime_type}" }});

            let file = new File([blob], "{file_name}", {{ type: blob.type }});

            let dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);

            let event = new ClipboardEvent("paste", {{
                bubbles: true, 
                cancelable: true,
                clipboardData: dataTransfer
            }});

            document.dispatchEvent(event);
        }}

        pasteFile();
        """
        print("JavaScript finished....")

        sleep(0.5)

        print("Executing JavaScript....")
        driver.execute_script(js_script)
        print("JavaScript Done!")

        return 0
    except TimeoutException as e:
        logging.error(f"Timeout occurred in passing_file(): {e}")
        return 1
    except Exception as e:
        logging.exception(f"An unexpected error occurred in passing_file(): {e}")
        return 1


def check_sending_status(driver):
    # Define a maximum timeout (e.g., 30 minutes)
    timeout = 5 * 60  # 30 minutes in seconds
    interval = 10  # 5 minutes in seconds
    elapsed_time = 0  # Keep track of the elapsed time

    while elapsed_time < timeout:
        bubbles_date_groups = driver.find_elements(By.CLASS_NAME, "bubbles-date-group")
        if bubbles_date_groups:
            last_group = bubbles_date_groups[-1]  # Get the last group

            # Find the last message div within the last group
            messages_in_last_group = last_group.find_elements(By.XPATH, "./div")
            if messages_in_last_group:
                last_message = messages_in_last_group[-1]  # Get the last message
                if elapsed_time == 0:
                    sleep(5) # wait for 5 seconds for the first time that file is being sent 
                # Check the status of the last message
                if "is-sending" in last_message.get_attribute("class"):
                    print("The file is still sending...")
                    sleep(interval)  # Wait for {interval} seconds
                    elapsed_time += interval
                elif "is-sent" in last_message.get_attribute("class"):
                    print("Sending the file is Done;)")
                    return 0
                else:
                    print("The status of the last message is unknown.")
                    return 1
            else:
                print("No messages found in the last group.")
                return 1
        else:
            print("No bubbles-date-group elements found.")
            return 1


    if elapsed_time >= timeout:
        print("Timeout reached. The file may still be sending.")
        return 1


def send_file(driver, prices_pdf):
    try:
        passing_file(driver, prices_pdf) # Finds your file and passes it Eitaa for you to send the file, change the path to your file

        # if you want to send file with no title , just comment the line blew
        passing_file_fields(driver) # writes your title that you want to send the file with

        # clicks the send button
        try:
            send_file_btn = WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.CSS_SELECTOR, 'body > div.popup.popup-send-photo.popup-new-media.active > div > div.popup-header > button')
            )
            ActionChains(driver).move_to_element(send_file_btn).click().perform()
            check_sending_status(driver)
        except TimeoutException as e:
            logging.error(f"Timeout occurred in send_file(): {e}")
            return 1
        except Exception as e:
            logging.exception(f"An unexpected error occurred in clicking the send file button: {e}")
            return 1
    except TimeoutException as e:
        logging.error(f"Timeout occurred in send_file(): {e}")
        return
    except Exception as e:
        logging.exception(f"An unexpected error occurred in send_file(): {e}")
        return 1


def send_to_Eitaa(prices_pdf):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Selenium")
        options.add_argument("profile-directory=Default")
        options.add_argument("--start-maximized")


        driver = webdriver.Chrome(options=options)
        driver.get("https://web.eitaa.com")


        if verifyLogin(driver):

            unread_message = target_user(driver)

            find_clear_message_box(driver)

            send_file(driver, prices_pdf)
        else:
            return 1
    except Exception as e:
        logging.exception(f"An unexpected error occurred in main(): {e}")
    finally:
        if unread_message:
            print("\nYou have a new message.")
            input("press any key to Exit the program and close the browser...")
        else:
            driver.quit()

if __name__ == "__main__":
    send_to_Eitaa()