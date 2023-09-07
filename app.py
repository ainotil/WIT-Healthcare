import re
import streamlit as st
from PyPDF2 import PdfReader

import pdf_parser as pdp


st.set_page_config(layout="wide", page_title="Un-Report")

st.write("## Un-Report: Data -> Information")
st.write("Convert scary pathological reports into friendly, readable visuals!")

uploaded_reports = st.file_uploader("Select PDF files from your PC", accept_multiple_files=True)
for uploaded_file in uploaded_reports:
    st.write("File:", uploaded_file.name)

# print('reports:', uploaded_reports)

month_dct = {}
for uploaded_file in uploaded_reports:
    month_dct[pdp.get_month(uploaded_file)] = uploaded_file
month_dct = dict(sorted(month_dct.items(), key = lambda x: x[0]))

visual_dict = {}
for mnth, fl in month_dct.items():
    pdp.update_dictionary(visual_dict, mnth, fl)

print(visual_dict)

# for uploaded_file in uploaded_reports:
#     pdf_reader = PdfReader(uploaded_file)
#     dates = ""
#     for page in pdf_reader.pages:
#         dates += page.extract_text()
#     # print('extracted dates value', dates)
#     match = re.search('\nDate.*\n', dates)
#     date_value = match.group(0)
#     dates = date_value.split('-')[1]
#     # print(dates)

