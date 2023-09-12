import streamlit as st
import pandas as pd 
import re


# to extract text from pdf using PyMuPDF
def extract_text_pdf(pdf):
    with fitz.open(pdf) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# removing punctuations and converting to lower case
def punctution_removal_lowercase_conversion(words):
  words_re = []
  words_lower = []
  for i in  range(len(words)):
      words_re.append(re.sub(r"[^a-zA-Z0-9]","",words[i]))
      words_lower.append(words_re[i].lower())
  return words_lower

# removing empty string from words without stopwords
def empty_string_removal(words_sw):
  while '' in words_sw:
    words_sw.remove('')
  return words_sw

# creating a frequency table to identify how many times a word appreared in the whole text
def frequency_table(words_sw):
  freqTable = {}
  for word in words_sw:
      if word in freqTable:
          freqTable[word] += 1
      else:
          freqTable[word] = 1
  return freqTable

# calculating sentence value to priortise which sentences are more important
def sentence_value():
    sentenceValue = {}
    for sentence in sentences:
        sentence_value = 0
        for word in sentence.split():
            if word in freqTable:
                sentence_value += freqTable[word]
        sentenceValue[sentence] = sentence_value
    return sentenceValue

# printing summary
def get_summary(df1, max_words):
    summary = pd.DataFrame(columns=df1.columns)
    total_words = 0
    
    for index, row in df1.iterrows():
        sentence = row['Key']
        words = sentence.split()
        if total_words + len(words) <= max_words:
            summary = summary.append(row)
            total_words += len(words)
        else:
            break
            
    return summary

def segment_sentences(pdf_data2):
  sentences = re.split("[.!?]", pdf_data2)
  return sentences

def tokenize(pdf_data2):
  tokens = re.split("[ .,!?]", pdf_data2)
  return tokens



st.header("Pdf summarizer:")
num_of_words = int(st.text_input("Enter number of maximum words for summary:",value=500))
pdf = st.file_uploader("Upload PDF:")

if pdf is not None:
    text = extract_text_pdf(pdf.name)

extracted_pdf = extract_text_pdf(pdf)
extracted_pdf = re.sub('\n', ' ', extracted_pdf)
sentences = segment_sentences(extracted_pdf)
words = tokenize(extracted_pdf)

stopwords = pd.read_csv('/stopwords.csv')
stopwords = list(stopwords['0'])
words_lower = punctution_removal_lowercase_conversion(words)
words_sw = [w for w in words_lower if w not in stopwords]
words_sw = empty_string_removal(words_sw)

freqTable = frequency_table(words_sw)

sentenceValue = sentence_value()

df = pd.DataFrame(list(sentenceValue.items()), columns=['Key', 'Value'])
df['index'] = df.index
df1 = df.sort_values(by='Value', ascending=False)
df1 = df1.reset_index()

summary = get_summary(df1, num_of_words)
df2 = summary.sort_values(by='index', ascending=True)
joined_text = ' '.join(df2['Key'])
joined_text
