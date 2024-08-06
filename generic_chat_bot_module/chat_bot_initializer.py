from langchain_ai21 import ChatAI21
from vector_db_creator import VectorDB
from response_generator import ResponseGenerator

class ChatInitializer():
    def initiate(self) -> None:
        # Initialize chat history
        print("Calling Rambo...")
        self.chat_model = ChatAI21(model="j2-ultra",api_key="Your API KEY",temperature=0.2,max_tokens=500)
        print("Yooo Ramboooo is here !!!")
        print("Rambo is going through your docs....")
        vector_db_obj = VectorDB()
        self.retriever = vector_db_obj.vector_db_creator()
        print("Rambo is ready...")
        response_gen_obj = ResponseGenerator(chat_model=self.chat_model,retriever=self.retriever)
        return response_gen_obj