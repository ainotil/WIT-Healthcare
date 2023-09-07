import camelot
import PyPDF2
from PyPDF2 import PdfReader
import re

month_mapping = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

def get_month(pdf):
    pdf_reader = PdfReader(pdf)
    date = ""
    for page in pdf_reader.pages:
        date += page.extract_text()
    match = re.search('\nDate.*\n', date)
    date_value = match.group(0)
    return int(date_value.split('-')[1])


def write_pdf(pdf_object):
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_reader=PyPDF2.PdfFileReader(pdf_object)

    for pagenum in range(pdf_reader.numPages):
        obj=pdf_reader.getPage(pagenum)
        pdf_writer.addPage(obj)

    output_file=open("output.pdf",'wb')
    pdf_writer.write(output_file)


def update_dictionary(dic, month, pdf):
    month = month_mapping[month]
    dic[month] = {"score": 0, "abnormal": []}
    write_pdf(pdf)
    tables = camelot.read_pdf('output.pdf', flavor='stream')
    
    score = 0
    for index, row in tables[0].df[3:-1].iterrows():
        rows = str(row).split('\n')[:3]
        i = 0
        while i < 3:
            rows[i] = rows[i][1:].strip()
            i += 1
        rows[2] = rows[2].split('-')
        if len(rows[2]) == 2:
            if float(rows[1]) < float(rows[2][0]):
                sd = round((float(rows[2][0]) - float(rows[1])) / (float(rows[2][1])-float(rows[2][0])) * 100)
                dic[month]["abnormal"].append([rows[0], float(rows[1]), sd])
                score += sd
            elif float(rows[1]) > float(rows[2][1]):
                sd = round((float(rows[1]) - float(rows[2][1])) / (float(rows[2][1])-float(rows[2][0])) * 100)
                dic[month]["abnormal"].append([rows[0], float(rows[1]), sd])
                score += sd
        elif float(rows[1]) != float(rows[2][0]):
            sd = round(abs(float(rows[1]) - float(rows[2][0])) / float(rows[2][0]) * 100)
            dic[month]["abnormal"].append([rows[0], float(rows[1]), sd])
            score += sd
    for i in range(len(dic[month]["abnormal"])):
        dic[month]["abnormal"][i][2] = round(dic[month]["abnormal"][i][2]/score*100)
    dic[month]["score"]  = round(score/16)
    # return dic


if __name__ == "__main__":
    dict = {}
    month = get_month("Complete_Blood_Count_1.pdf")
    dict = update_dictionary(dict, month, "Complete_Blood_Count_1.pdf")
    print(dict)
