import re

import streamlit as st
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

import pdf_parser as pdp


st.set_page_config(layout="wide", page_title="Reportify")

st.write("## Reportify(Blood Test): Data -> Information")
st.write("### Convert scary pathological reports into friendly, readable visuals!")

uploaded_reports = st.file_uploader("Select PDF Report files from your PC", accept_multiple_files=True)
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

# print(visual_dict)

month_list = []
score_list = []
ab_list = []
pie_value = []

dic = visual_dict


for mon in dic.keys():
    month_list.append(mon)

for value in dic.values():
    score_list.append(value["score"])

st.write("### Comparative Analysis Over Time: Health Score")

if not visual_dict:
    st.write("*Upload reports to generate graph!*")
else:
    st.write(f"#### The most recent Health Score is {visual_dict[list(visual_dict.keys())[-1]]['score']}")

if visual_dict:
    fig = plt.figure(figsize=(7, 7))
    plt.plot(month_list, score_list)
    plt.xlabel('Month')
    plt.ylabel('Score')
    plt.title('Overall Score')
    st.pyplot(fig)

df = pd.DataFrame({'Month':month_list, 'Health Score':score_list})

st.write("### Summary of biggest health indicators: larger share equals higher change.")

option = st.selectbox('Pick a month for a Pie Chart', df)

if not option:
    st.write("*Upload reports to generate pie chart!*")

if option:
    ab_value = []
    for ab in dic[option]["abnormal"]:
        ab_list.append(ab[0])
        ab_value.append(ab[1])
        pie_value.append(ab[2])

    pie_fig = plt.figure(figsize=(7, 7))
    plt.pie(pie_value, labels=ab_list, autopct='%1.1f%%', startangle=90)
    plt.title('Abnormal element distribution')
    st.pyplot(pie_fig)
    st.write("### Always see a doctor for proper advice!")
    i = 0
    while i < 3:
        if ab_value[i] < 0:
            st.write(f"*Your {ab_list[i]} level is "  + str(pie_value[i]) + "% lower than normal value!*")   
        else:
            st.write(f"*Your {ab_list[i]} level is "  + str(pie_value[i]) + "% higher than normal value!*")
        i += 1
    st.write("Higher than normal value means you have too many red blood cells. It can be due to smoking, living at high altitudes, lung problems, or a rare condition called polycythemia vera. Quit smoking, treat lung issues, and stay hydrated.\n")
    st.write("Lower than normal value happens when your blood doesn't have enough hemoglobin. It can make you feel tired and weak. To fix it, eat foods rich in iron (like meat and beans) and vitamins (like B12 and folate). Also, manage any chronic diseases and stop any bleeding.")