from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from dotenv import load_dotenv
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from facebook_templates import facebook_training
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from facebook_templates import facebook_template

load_dotenv()

class Facebook_Bot():
    def __init__(self) -> None:
        self.template = facebook_template()
        self.embeddings = OpenAIEmbeddings()
        self.set_prompt()
        self.set_example_selector()
        self.llm = ChatOpenAI(temperature=.6, model='gpt-3.5-turbo-16k')
        self.create_chain()

    def set_prompt(self):
        instruction = CommaSeparatedListOutputParser()
        self.prompt = PromptTemplate(
            input_variables=["user_input"],
            template= self.template,
            partial_variables= {"format_instructions": instruction.get_format_instructions()}
        )

    def set_example_selector(self):
        self.example_selector = SemanticSimilarityExampleSelector.from_examples(
            facebook_training(),
            self.embeddings,
            FAISS,
            k=1)

    def get_examples(self, query):
        selected_examples = self.example_selector.select_examples({'question': query})
        self.examples = """"""
        for example in selected_examples:
            for k, v in example.items():
                self.examples += f"""{k}:{v}"""
                self.examples += "\n"
            print(self.examples)

    def create_chain(self):
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, verbose= True)
    
    def run_chain(self, message):
        response = self.chain.predict(user_input= message, few_shot_examples= self.examples)
        return response
    