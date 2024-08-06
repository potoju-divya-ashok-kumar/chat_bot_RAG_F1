import streamlit as st
from chat_bot_initializer import ChatInitializer

@st.cache_resource
def chatInitiater():
    init_obj=ChatInitializer()
    response_gen_obj = init_obj.initiate()
    return response_gen_obj

response_gen_obj = chatInitiater()


class Rambo():
    
    def chat_bot(self,response_gen_obj):
        self.response_gen_obj = response_gen_obj
        if "messages" not in st.session_state:
            
            st.session_state.messages=[]
            with st.chat_message("Assistant"):
                st.markdown('Hi, Welcome to self service portal !!!')
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        #React to user watch
        if prompt :=st.chat_input("what is up ?"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            st.session_state.messages.append({'role':'user','content':prompt})

            response = self.response_gen_obj.response_generation(query=prompt)

            # Display assistant response in chat message container

            with st.chat_message("Assistant"):
                st.markdown(response)

            st.session_state.messages.append({'role':"Assistant",'content':response})

if __name__=="__main__":
    obj=Rambo()
    obj.chat_bot(response_gen_obj)