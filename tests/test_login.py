import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "http://127.0.0.1:5000"


# Setup Chrome
def setup_driver():

    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver


# Helper Function
def register_user(driver, username, password):

    unique_username = username + str(random.randint(1000, 9999))

    driver.get(f"{BASE_URL}/register")

    driver.find_element(By.ID, "username").send_keys(unique_username)
    driver.find_element(By.ID, "password").send_keys(password)

    driver.find_element(By.ID, "register-btn").click()

    time.sleep(1)

    return unique_username


# Helper Function
def login_user(driver, username, password):

    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)

    driver.find_element(By.ID, "login-btn").click()

    time.sleep(1)


# TEST 1
def test_register_user():

    driver = setup_driver()

    register_user(driver, "user1", "123")

    assert "Login" in driver.page_source

    driver.quit()


# TEST 2
def test_login_valid():

    driver = setup_driver()

    username = register_user(driver, "user2", "123")

    login_user(driver, username, "123")

    assert "Dashboard" in driver.page_source

    driver.quit()


# TEST 3
def test_login_invalid():

    driver = setup_driver()

    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "username").send_keys("wrong")
    driver.find_element(By.ID, "password").send_keys("wrong")

    driver.find_element(By.ID, "login-btn").click()

    time.sleep(1)

    assert "Dashboard" not in driver.page_source

    driver.quit()


# TEST 4
def test_logout():

    driver = setup_driver()

    username = register_user(driver, "user3", "123")

    login_user(driver, username, "123")

    driver.get(f"{BASE_URL}/logout")

    time.sleep(1)

    assert "Login" in driver.page_source

    driver.quit()


# TEST 5
def test_dashboard_access_without_login():

    driver = setup_driver()

    driver.get(f"{BASE_URL}/dashboard")

    time.sleep(1)

    assert "Login" in driver.page_source

    driver.quit()


# TEST 6 - Fixed
def test_add_task():
    driver = setup_driver()
    try:
        username = register_user(driver, "user4", "123")
        login_user(driver, username, "123")

        driver.find_element(By.ID, "title").send_keys("Task One")   # ← Fixed
        driver.find_element(By.ID, "add-task-btn").click()

        time.sleep(1.5)
        assert "Task One" in driver.page_source
    finally:
        driver.quit()


# TEST 7 - Fixed
def test_add_multiple_tasks():
    driver = setup_driver()
    try:
        username = register_user(driver, "user5", "123")
        login_user(driver, username, "123")

        tasks = ["Task A", "Task B", "Task C"]
        for task in tasks:
            driver.find_element(By.ID, "title").clear()      # ← Fixed
            driver.find_element(By.ID, "title").send_keys(task)
            driver.find_element(By.ID, "add-task-btn").click()
            time.sleep(1.2)

        assert "Task C" in driver.page_source
    finally:
        driver.quit()


# TEST 8 - Most Robust Version
def test_delete_task():
    driver = setup_driver()
    try:
        username = register_user(driver, "user6", "123")
        login_user(driver, username, "123")

        task_name = "Delete Me"

        # Add task
        driver.find_element(By.ID, "title").send_keys(task_name)
        driver.find_element(By.ID, "add-task-btn").click()
        time.sleep(2)

        # More reliable delete button selector
        delete_btn = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-danger")
        delete_btn.click()

        # Handle alert
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        driver.switch_to.alert.accept()

        time.sleep(3)
        driver.refresh()        # Force reload task list
        time.sleep(2)

        final_source = driver.page_source
        if task_name in final_source:
            print("❌ Still seeing task. Here's proof:")
            print(final_source[final_source.find(task_name)-150:final_source.find(task_name)+400])
            assert False, "Task was not deleted"
        else:
            print("✅ test_delete_task PASSED")
            
    finally:
        driver.quit()

# TEST 9
def test_login_page_loads():

    driver = setup_driver()

    driver.get(f"{BASE_URL}/login")

    assert "Login" in driver.page_source

    driver.quit()


# TEST 10
def test_register_page_loads():

    driver = setup_driver()

    driver.get(f"{BASE_URL}/register")

    assert "Register" in driver.page_source

    driver.quit()


# TEST 11
def test_home_redirect():

    driver = setup_driver()

    driver.get(BASE_URL)

    time.sleep(1)

    assert "Login" in driver.page_source

    driver.quit()


# TEST 12
def test_session_persistence():

    driver = setup_driver()

    username = register_user(driver, "user7", "123")

    login_user(driver, username, "123")

    driver.refresh()

    time.sleep(1)

    assert "Dashboard" in driver.page_source

    driver.quit()


# TEST 13
def test_empty_login_fields():

    driver = setup_driver()

    driver.get(f"{BASE_URL}/login")

    driver.find_element(By.ID, "login-btn").click()

    time.sleep(1)

    assert "Dashboard" not in driver.page_source

    driver.quit()


# TEST 14
def test_empty_task_submission():

    driver = setup_driver()

    username = register_user(driver, "user8", "123")

    login_user(driver, username, "123")

    driver.find_element(By.ID, "add-task-btn").click()

    time.sleep(1)

    assert "Dashboard" in driver.page_source

    driver.quit()


# TEST 15
def test_logout_redirect():

    driver = setup_driver()

    username = register_user(driver, "user9", "123")

    login_user(driver, username, "123")

    driver.get(f"{BASE_URL}/logout")

    time.sleep(1)

    driver.get(f"{BASE_URL}/dashboard")

    time.sleep(1)

    assert "Login" in driver.page_source

    driver.quit()