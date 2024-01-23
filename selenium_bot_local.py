from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import streamlit as st
from selenium.webdriver.common.keys import Keys

def post_to_facebook(post, email, password, facebook_groups):

    # chrome_options = uc.ChromeOptions()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # driver = webdriver.Remote()
    driver = uc.Chrome(headless= True, no_sandbox= True, options= chrome_options)

    driver.get('https://www.facebook.com/')
    WebDriverWait(driver, 10)

    driver.execute_script('console.log("entre al log en streamlit")')
    driver.find_element(by= By.XPATH, value= '//*[@id="email"]').send_keys(password)
    sleep(4)
    ActionChains(driver).key_down(Keys.TAB).perform()
    sleep(4)
    ActionChains(driver).send_keys(email).perform()    
    sleep(4)
    ActionChains(driver).key_down(Keys.ENTER).perform()
    sleep(4)
    


    # login = driver.find_element(by= By.XPATH, value= '/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button')
    # st.write(login.text)
    # st.write(password)

    # login.click()
    sleep(6)
    # Espera a que la página se cargue completamente (ajusta el tiempo de espera según sea necesario)
    html = driver.page_source
    st.text_area(html)
    sleep(4)
    driver.quit()
    return html 
    for group in facebook_groups:
        st.write("Entre a grupo")
        sleep(5)
        driver.get(group)
        st.write("Entre al link")

        # Espera a que la página se cargue completamente (ajusta el tiempo de espera según sea necesario)
        #CAN'T USE IN DEPLOY # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'xi81zsa')]")))
        sleep(10)
        element_to_click = driver.find_elements(By.XPATH, '//div[contains(@class, "xi81zsa")]')
        st.write("Cantidad de elementos en element_to_click:", len(element_to_click))

        for element in element_to_click:
            st.write(element.text)
        
        for element in element_to_click:
            st.write(element.text)
            print("elemento exterior", element.text)
            if "Crear publicación" in element.text or "Escribe" in element.text or "Write something" in element.text:
                element.click()
                st.write("Entre en publicacion")
                sleep(2)
                write_post = element.find_elements(By.XPATH, '//div[contains(@class, "x1ed109x")]')
                for element2 in write_post:
                    print(element2.text)
                    if "Crea una publicación pública" in element2.text or "Create a public post" in element2.text:
                        print("encontré el elemento create a public post")
                        sleep(2)
                        # Hacer clic en el element2o usando JavaScript
                        # element2.execute_script("arguments[0].scrollIntoView();", element2)
                        # driver.execute_script("arguments[0].click();", element2)
                        driver.implicitly_wait(4)
                        
                        ActionChains(driver).move_to_element(element2).send_keys(post).perform()
                        print("escribi el post", post)
                        find_bttn = element.find_elements(By.XPATH, '//div[contains(@class, "x1n2onr6")]')
                        for bttn in find_bttn:
                            if bttn.text == "Publicar" or bttn.text == "Post":
                                st.write("Encontre el boton de publicar")
                                bttn.click()
                                st.write("POSTED TO FACEBOOK GROUP: ", group)
                                break
                        
                        sleep(4)
                        break
                break
        print("elemento clickeado")
        sleep(5)

    driver.quit()
    return html