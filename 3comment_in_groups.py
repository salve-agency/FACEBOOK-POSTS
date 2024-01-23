from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from dotenv import load_dotenv
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from facebook_templates import facebook_comments_template, facebook_selector_template
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class online():
    def __init__(self) -> None:
        client = MongoClient("mongodb+srv://bulkmemorytest:22485@cluster0.0irwfrm.mongodb.net/")
        db = client['facebook_data']
        self.mongo_comments = db["comments"]


class Facebook_Selector:
    def __init__(self) -> None:
        self.template = facebook_selector_template()
        self.set_prompt()
        self.llm = ChatOpenAI(temperature=.6, model='gpt-3.5-turbo')
        self.craete_chain()
        
    def set_prompt(self):
        self.prompt = PromptTemplate(
            input_variables=["post"],
            template= self.template
        )
    
    def craete_chain(self):
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, verbose= True)
    
    def run_chain(self, post):
        response = self.chain.predict(post= post)
        return response


class Facebook_Comments_Bot:
    
    def __init__(self):
        self.template = facebook_comments_template()
        self.set_prompt()
        self.llm = ChatOpenAI(temperature=.6, model='gpt-3.5-turbo-16k')
        self.create_chain()
        
        
    def set_prompt(self):
        self.prompt = PromptTemplate(
            input_variables=["post"],
            template= self.template
        )
    
    def create_chain(self):
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, verbose= True)

    def run_chain(self, post):
        response = self.chain.predict(post= post)
        return response
    
    
def comment_in_posts(urls, email, password):
    
    posts_list = []
    translations_list = []
    comments_list = []
    
    db = online()
    fb = Facebook_Comments_Bot()
    selector = Facebook_Selector()
    
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
    
    for group in urls:
        sleep(5)
        driver.get(group)
        # Espera a que la página se cargue completamente (ajusta el tiempo de espera según sea necesario)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'xi81zsa')]")))
        ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
        sleep(5)
        
        sort_by = driver.find_elements(By.XPATH, '//div[contains(@class, "x1i10hfl")]')
        for sort in sort_by:
            print(sort.text)
            if "most relevant" in sort.text.lower():
                while True:
                    try:
                        print("found")
                        sort.click()
                        break
                    except Exception:
                        ActionChains(driver).key_down(Keys.PAGE_UP).perform()
                print("paso el error")
                        
                sleep(2)
                ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()
                sleep(2)
                ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()
                sleep(2)
                ActionChains(driver).key_down(Keys.ENTER).perform()
                sleep(2)
                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                sleep(2)
                
                break
        sleep(5)
        print("paso el for de sort")
        posts_elem = driver.find_elements(By.XPATH, '//div[contains(@class, "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkb")]')
        comments_elem = driver.find_elements(By.XPATH, '//div[contains(@style, "text-align")]')
        translations = driver.find_elements(By.XPATH, '//div[contains(@class, "x126k92a")]')

        # for translation in translations:
        #     translations_list.append(translation.text)
        # for comment in comments_elem:
        #     if comment.text not in translations_list:
        #         comments_list.append(comment.text)
        # for postel in posts_elem:
        #     if postel.text not in comments_list:
        #         browser = db.mongo_comments.find_one({"post": postel.text})
        #         if not browser:
        #             selector_response = selector.run_chain(post= postel.text)
        #             print("SELECTOR RESPONSE: ",selector_response)
        #             if selector_response == "True":                       
        #                 posts_list.append(postel.text)
        #                 print("COMENTARIO AÑADIDO: ",postel.text)
        #             else:
        #                 print(f"This comment {postel.text} is not worth commenting")
        #                 posts_list.append("commented")
        #         else:
        #             print(f"This comment {postel.text} is already in the database")
        #             posts_list.append("commented")


        print("POSTS LIST: ",posts_list)
        posts = driver.find_elements(By.XPATH, '//div[contains(@class, "x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")]')
        # Locate the element again before interacting with it
        sleep(5)
        print("hola")
        counter = 0
        for element in posts:
            post_text = element.text
            print(post_text)
            sleep(5)
            if "Comment" in post_text or "Comentar" in post_text:
            # if "Write a" in post_text or "Escribe un" in post_text:
                sleep(5)
                print("found")
                ActionChains(driver).move_to_element(element).click().perform()
                sleep(3)
                ActionChains(driver).move_to_element(element).send_keys("Hola chavalin como te encuentras").perform()
                ActionChains(driver).move_to_element(element).send_keys(Keys.ENTER).perform()
                ActionChains(driver).move_to_element(element).send_keys(Keys.ESCAPE).perform()
                # element2 = element.find_elements(By.XPATH, '//div[contains(@class, "x78zum5")]')
                # for post in element2:
                #     print(post.text)
                #     if "Comment" in post.text or "Comentar" in post.text:
                #         element3 = post.find_elements(By.XPATH, './/div[contains(@class, "notranslate") and (@contenteditable="true")]')
                #         for el2 in element3:
                #             print("Entre")
                #             if counter < len(posts_list):
                #                 if not posts_list[counter] == "commented":
                #                     comment = fb.run_chain(posts_list[counter])
                #                     ActionChains(driver).move_to_element(el2).click().perform()
                #                     ActionChains(driver).move_to_element(el2).send_keys(comment).perform()
                #                     ActionChains(driver).move_to_element(el2).send_keys(Keys.ENTER).perform()
                #                     db.mongo_comments.insert_one({"post": posts_list[counter], "comment": comment })
                #                 else:
                #                     print(f"Comment {counter} is already in the database")
                #                 counter += 1
                #             else:
                #                 break
                #         break
                    
def get_comments(urls, email, password, db: online):
    posts_list = []
    translations_list = []
    comments_list = []
    
    fb = Facebook_Comments_Bot()
    
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options= chrome_options)

    driver.get('https://www.facebook.com/')
    wait = WebDriverWait(driver, 10)
    driver.find_element(by= By.XPATH, value= '//*[@id="email"]').send_keys(email)
    driver.find_element(by= By.XPATH, value= '//*[@id="pass"]').send_keys(password)
    login = driver.find_element(by= By.XPATH, value= '/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button')
    login.click()

    
    for group in urls:
        sleep(5)
        driver.get(group)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'xi81zsa')]")))
        ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
        sleep(5)
        posts_elem = driver.find_elements(By.XPATH, '//div[contains(@class, "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkb")]')
        comments_elem = driver.find_elements(By.XPATH, '//div[contains(@style, "text-align")]')
        translations = driver.find_elements(By.XPATH, '//div[contains(@class, "x126k92a")]')
        structure_element = driver.find_elements(By.XPATH, '//div[contains(@class, "j83agx80 cbu4d94t ew0dbk1b irj2b8pg")]')
        
        for element in posts_elem:
            print("Elemento: ",element.text)
        for translation in translations:
            translations_list.append(translation.text)
        for comment in comments_elem:
            if comment.text not in translations_list:
                comments_list.append(comment.text)
        for postel in posts_elem:
            if postel.text not in comments_list:
                browser = db.mongo_comments.find_one({"post": postel.text})
                if not browser:
                    posts_list.append(postel.text)
                    print("COMENTARIO AÑADIDO: ",postel.text)

                else:
                    print(f"This comment {postel.text} is already in the database")



