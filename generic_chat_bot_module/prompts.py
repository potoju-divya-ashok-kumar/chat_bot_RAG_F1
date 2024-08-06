from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

#FIRST CONVERSATION
first_prompt = ChatPromptTemplate.from_messages(
   [
        ("system", "You are a helpful assistant that answers the question when you know the answer, humbly reply that you dont know the answer if you have no information.prefer tables format and explain it in high details.Dont limit the output"),
        ("user","{context_text}"),
        ("human", "What are all the characteristics properties that engine oil must possess ?"),
    ]
)


#SECOND CONVERSATION

second_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that answers the question when you know the answer, humbly reply that you dont know the answer if you have no information.prefer tables format and explain it in high details.Dont limit the output"),
        MessagesPlaceholder(variable_name='history',optional=True),
        MessagesPlaceholder(variable_name='context',optional=True),
        ("human", "{query}"),
    ]
)

#SUMMARY PROMPT
summary_prompt_template = ChatPromptTemplate.from_messages([
    ('system',"Summarise the following text :"),
    MessagesPlaceholder(variable_name='history')
])