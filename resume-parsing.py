#!/usr/bin/env python
# coding: utf-8

# In[33]:


import spacy
import pdfminer
import re
import os
import pandas as pd


# In[34]:


import pdf2txt


# In[52]:


# converting pdf to text

def convert_pdf(filename):
    output_filename = os.path.basename(os.path.splitext(filename)[0]) + '.txt'
    output_filepath = os.path.join('output/txt/', output_filename)
    pdf2txt.main(args=[filename, "--outfile", output_filepath])
    print(output_filepath + " saved successfully!!")
    with open(output_filepath, 'r') as f:
        return f.read()
    



# In[53]:


# Load the language model
nlp = spacy.load("en_core_web_sm")


# In[54]:


# placeholders
result_dict = {'name': [], 'phone': [], 'email': [], 'skills': []}
names = []
phones = []
emails = []
skills = []


# In[55]:

# regex: https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script
def parse_content(text):
    skillset = re.compile("python|java|sql|tableau|r")
    phone_num = re.compile('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    doc = nlp(text)
    name = [entity.text for entity in doc.ents if entity.label_ == "PERSON"][0]
    print(name)
    email = [word for word in doc if word.like_email == True][0]
    print(email)
    phone = str(re.findall(phone_num, text.lower()))
    skills_list = re.findall(skillset, text.lower())
    unique_skills_list = str(set(skills_list))
    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print('Extraction completed successfully')


# In[56]:


for file in os.listdir('resumes/'):
    if file.endswith('.pdf'):
        print('Reading...' + file)
        txt = convert_pdf(os.path.join('resumes/', file))
        parse_content(txt)


# In[61]:


result_dict['name'] = names
result_dict['phone'] = phones
result_dict['email'] = emails
result_dict['skills'] = skills


# In[63]:


result_df = pd.DataFrame(result_dict)
result_df


# In[64]:


result_df.to_csv('output/csv/parsed_resumes.csv', index=False)

