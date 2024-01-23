from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



def post_to_facebook(email, password, facebook_groups):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options= chrome_options)

    driver.get('https://www.facebook.com/')
    wait = WebDriverWait(driver, 10)
    driver.find_element(by= By.XPATH, value= '//*[@id="email"]').send_keys(email)
    driver.find_element(by= By.XPATH, value= '//*[@id="pass"]').send_keys(password)
    login = driver.find_element(by= By.XPATH, value= '/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button')
    login.click()

    # Espera a que la página se cargue completamente (ajusta el tiempo de espera según sea necesario)
    
    for group in facebook_groups:
        sleep(5)
        driver.get(group)

        # Espera a que la página se cargue completamente (ajusta el tiempo de espera según sea necesario)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'xi81zsa')]")))
        ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
        sleep(2)
        posts_elem = driver.find_elements(By.XPATH, '//div[contains(@class, "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkb")]')
        for postel in posts_elem:
            print(postel.text)
    

            
            
        posts = driver.find_elements(By.XPATH, '//div[contains(@class, "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")]')
        # Locate the element again before interacting with it
        sleep(2)
        print("hola")
        for element in posts:
            post_text = element.text
            print(post_text)
            sleep(2)
            if "Write a comment" in post_text:
                sleep(2)
                print("found")
                sleep(2)
                element2 = element.find_elements(By.XPATH, '//div[contains(@class, "x78zum5")]')
                for post in element2:
                    # print(post.text)
                    if "Comment" in post.text:
                        element3 = post.find_elements(By.XPATH, './/div[contains(@class, "notranslate") and (@contenteditable="true")]')
                        for el2 in element3:
                            print("Entre")
                            ActionChains(driver).move_to_element(el2).click().perform()
                            ActionChains(driver).move_to_element(el2).send_keys("hola?").perform()
                        break

                # driver.implicitly_wait(4)

                # element2.click()
                # sleep(2)
                # WebDriverWait(driver, 10).until(EC.visibility_of(element2))
                # ActionChains(driver).move_to_element(element2).send_keys("hola").perform()
                    
                
                
        sleep(6)

        #     print("elemento exterior", element.text)
        #     if element.text == "Crear publicación" or element.text == "Escribe algo..." or element.text == "Write something...":
        #         element.click()
        #         sleep(2)
        #         write_post = element.find_elements(By.XPATH, '//div[contains(@class, "x1ed109x")]')
        #         for element2 in write_post:
        #             print(element2.text)
        #             if "Crea una publicación pública" in element2.text or "Create a public post" in element2.text:
        #                 print("encontré el elemento create a public post")
        #                 sleep(2)
        #                 # Hacer clic en el element2o usando JavaScript
        #                 # element2.execute_script("arguments[0].scrollIntoView();", element2)
        #                 # driver.execute_script("arguments[0].click();", element2)
        #                 driver.implicitly_wait(4)
                        
        #                 ActionChains(driver).move_to_element(element2).send_keys(post).perform()

        #                 find_bttn = element.find_elements(By.XPATH, '//div[contains(@class, "x1n2onr6")]')
        #                 for bttn in find_bttn:
        #                     if bttn.text == "Publicar" or bttn.text == "Post":
        #                         bttn.click()
        #                         break
                        
        #                 sleep(4)
        #                 break
        #         break
        # print("elemento clickeado")
        # sleep(5)

    driver.quit()

