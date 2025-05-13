
from pyresparser import ResumeParser
data = ResumeParser("resumes/resume1.docx").get_extracted_data()
print(data)

print(data['skills'])

'''
import docx2txt

temp = docx2txt.process("resumes/resume1.docx")
text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
print(' '.join(text))
'''
