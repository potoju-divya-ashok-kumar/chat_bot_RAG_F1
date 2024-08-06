from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ai21.embeddings import AI21Embeddings
from langchain_openai.embeddings import OpenAIEmbeddings

import re


class VectorDB():
    def __init__(self) -> None:
        loader = PyPDFLoader(r'fia_2026_formula_1_technical_regulations_pu_-_issue_1_-_2022-08-16.pdf')
        doc_pages = loader.load_and_split()
        self.doc_pages_new = self.footer_remover(doc_pages)
        

    def footer_remover(self,doc_pages=[]):
        # Removing Footer
        
        doc_pages_new=[]
        for page_no in range(len(doc_pages)):
            page_data = doc_pages[page_no]
            page_text= page_data.page_content
            page_lines_list = page_text.split('\n')
            new_page_lines_list=[]

            for line in page_lines_list:
                footer = re.findall('2026 Formula 1 Power Unit Technical Regulations',line)
                if len(footer)>0:
                    continue
                footer = re.findall('2022 Fédération Internationale de l’Automobile',line)
                if len(footer)>0:
                    line_ind = page_lines_list.index(line)
                    start = line.find('Issue 1')
                    end=start+7
                    new_page_lines_list.append(line[end:].strip())
                    continue
                new_page_lines_list.append(line)
            new_page_lines_list='\n'.join(new_page_lines_list)
            meta_data = page_data.metadata
            doc_pages_new.append(Document(page_content=new_page_lines_list,metadata=meta_data))
        return doc_pages_new
        
    def vector_db_creator(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=50)
        all_splits = text_splitter.split_documents(self.doc_pages_new)
        vector_store = Chroma.from_documents(documents=all_splits,embedding=AI21Embeddings(api_key="Your API KEY"))
        retriever = vector_store.as_retriever(k=2)
        return retriever

if __name__=="__main__":
    obj = VectorDB()
    retriever = obj.vector_db_creator()
    context = retriever.invoke('What are engine oil properties?')
    for x in context:
        print(x.page_content)
        print('-'*80)