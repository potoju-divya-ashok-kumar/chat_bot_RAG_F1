from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from prompts import *



class ResponseGenerator():
    def __init__(self,chat_model,retriever) -> None:
        self.chat_model = chat_model
        self.retriever = retriever
        self.chat_history = ChatMessageHistory()

    

    def add_to_history(self,type='',message=''):
        if type=='user':
            self.chat_history.add_user_message(message=message)
        elif type=='ai':
            self.chat_history.add_ai_message(message=message)
        return self.chat_history

    def format_prompt(self,prompt_template,history=[''],context=[''],query=['']):
        if history==['']:
            prompt = prompt_template.invoke({
                'context':context,
                'query':query
            })
        else:
            prompt = prompt_template.invoke({
                    'history':history,
                    'context':context,
                    'query':query
                })
        return prompt

    def doc_retriver(self,query=''):
        docs=self.retriever.invoke(query)
        context = docs
        docs=[]
        for doc in context:
            docs.append(doc.page_content)
        return docs

    def chat_summariser(self,chat_history):
        memory = ConversationSummaryMemory.from_messages(
        llm=self.chat_model,
        chat_memory=chat_history,
        return_messages=True
        )
        summary = [memory.buffer]
        return summary

    def chat_model_response(self,prompt):
        return self.chat_model(prompt.messages)
    
    def response_generation(self,query=''):
        print("Generating Response....")
        self.chat_history = self.add_to_history(type='user',message=query)
        context = self.doc_retriver(query=query)
        print(len(context))
        for i in context:
            print(i)
            print("*"*100)
        if len(self.chat_history.messages)>1:

            if len(self.chat_history.messages)>5:
                summary = self.chat_summariser(chat_history=self.chat_history)
                prompt = self.format_prompt(prompt_template=second_prompt,history=summary,context=context,query=query)
            else:
                prompt = self.format_prompt(prompt_template=second_prompt,history=self.chat_history.messages,context=context,query=query)
        else:
            prompt = self.format_prompt(prompt_template=second_prompt,context=context,query=query)

        response = self.chat_model(prompt.messages)
        self.chat_history = self.add_to_history(type='ai',message=response)
        return response.content
        