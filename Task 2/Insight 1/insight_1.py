#Installations and imports
'''!pip install sec_api
!pip install langchain
!pip install unstructured
!pip install openai
!pip install tiktoken
!pip install plotly
!pip install kaleido
import plotly.graph_objs as go
from sec_api import ExtractorApi
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.chains import LLMChain'''

# extracting 1A section using extractor api
extractorApi = ExtractorApi("api_key")
OPENAI_API_KEY = 'api_key'
url_10k = "https://www.sec.gov/ix?doc=/Archives/edgar/data/0000320193/000032019323000106/aapl-20230930.htm"
item_1A_text = extractorApi.get_section(url_10k, "1A", "text")

 #function to save text file
def save_text(file_path, text):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
        print("Text content saved to", file_path)
    except Exception as e:
        print("An error occurred while saving text content:", e)

    file_path = "summary.txt"
    save_text(file_path,item_1A_text)

llm = OpenAI(openai_api_key=OPENAI_API_KEY) # initializing llm

path1 = '/content/summary.txt'

#function to read text file
def read_file(path):
    try:
        with open(path, 'r') as file:
            # Read text content from the file
            text = file.read()
        return text
    except Exception as e:
        print("An error occurred while reading text content:", e)
        return None
essay= read_file(path1)

#using the map_reduce method to chunk the text and generate summary using langchain's summary chain
llm.get_num_tokens(essay)
text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
docs = text_splitter.create_documents([essay])
num_docs = len(docs)
num_tokens_first_doc = llm.get_num_tokens(docs[0].page_content)
print (f"Now we have {num_docs} documents and the first one has {num_tokens_first_doc} tokens")
summary_chain = load_summarize_chain(llm=llm, chain_type='map_reduce', )
output = summary_chain.run(docs)



#using better prompts and generating summary on all chunks
map_prompt = """
Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:
"""
map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

combine_prompt = """
Write a concise summary of the following text delimited by triple backquotes.
Return your response in bullet points which covers the key points of the text.
```{text}```
BULLET POINT SUMMARY:
"""
combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

summary_chain = load_summarize_chain(llm=llm,
                                     chain_type='map_reduce',
                                     map_prompt=map_prompt_template,
                                     combine_prompt=combine_prompt_template,  )
output = summary_chain.run(docs)
formatted_output = "\n".join(["* " + substr for substr in output.split("\n")])
save_text('summarized_1A',formatted_output)


# Generating one-word for all the one-line explanation of risk factors
final_template = ''' I want you to give me a one word for the one-line explanation of risk factors that I will give
you as input. Each bullet point corresponds to one line explanation of a risk factor. for example: The company also faces challenges with intellectual property protection and has a minority market share in the smartphone, personal computer, and tablet markets." this will correspond to intellectual property risk.one word for each explanation. {risk_factors} is the text that you will need to work on.'''
prompt1=PromptTemplate(
    input_variables=['risk_factors'],
    template=final_template
    )
prompt1.format(risk_factors=formatted_output)
chain1 = LLMChain(llm=llm,prompt=prompt1)
one_word= chain1.run(formatted_output)
formatted_one_word = "\n".join(["* " + substr for substr in one_word.split("\n")])
save_text ('one_word.txt',one_word)


# generating intensity ratings based on the risk factors
number_template= ''' I will give a set of risk factors associated with a company as bullet points. Each bullet point
corresponds to the explanation of a risk factor. Using your knowledge , i want you to rate the risk factor based on its intensity
on a scale of 10, 10 being the most intense risk factor.{risk_factors} is the text. keep the ratings diverse.Give only the ratings  as output.Please judge on various diverse paramters.'''
prompt2=PromptTemplate(
    input_variables=['risk_factors'],
    template=number_template
    )
chain2 = LLMChain(llm=llm,prompt=prompt2)
rating= chain2.run(formatted_output)
formatted_rating= "\n".join(["* " + substr for substr in rating.split("\n")])
save_text('rating.txt',rating)

one_word_risk=read_file('/content/one_word.txt')
one_word_rating=read_file('/content/rating.txt')

ratings = [int(line.split(". ")[1]) for line in one_word_rating.strip().split("\n")]
risk_factors = [line.split("- ")[1].strip() for line in one_word_risk.strip().split("\n")]


#generating visualization using plotly
fig = go.Figure(data=[go.Bar(
    x=risk_factors,
    y=ratings,
    marker_color='skyblue',  # Set color of bars
)])
fig.update_layout(
    title="Intensity Ratings of Risk Factors",
    xaxis_title="Risk Factors",
    yaxis_title="Intensity Rating",
    yaxis=dict(range=[0, 10]),  # Set range of y-axis to 0-10
)
fig.show()
fig.write_image("risk_factors_intensity_ratings.png", engine="kaleido")
