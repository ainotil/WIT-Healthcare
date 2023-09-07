import matplotlib.pyplot as plt

# dic = {"April":{"score":90, "abnormal":[["whit blood cell", 35], ["red blood cell", 35], ["x",30]]},
# "May":{"score":95, "abnormal":[["whit blood cell", 25], ["red blood cell", 35], ["x",40]]},
# "June":{"score":85, "abnormal":[["whit blood cell", 35], ["red blood cell", 25], ["x",40]]},
# "July":{"score":80, "abnormal":[["whit blood cell", 15], ["red blood cell", 45], ["x",40]]},
# "August":{"score":70, "abnormal":[["whit blood cell", 45], ["red blood cell", 35], ["x",20]]}
# }

month_list = []
score_list = []
ab_list = []
pie_value = []


for mon in dic.keys():
    month_list.append(mon)

for value in dic.values():
    score_list.append(value["score"])

plt.plot(month_list, score_list)

plt.xlabel('Month')
plt.ylabel('Score')
plt.title('Overal Score')
plt.show()

if mon_flag == 4:
    for ab in dic["April"]["abnormal"]:
        ab_list.append(ab[0])
        pie_value.append(ab[1])

    plt.pie(pie_value, labels=ab_list, autopct='%1.1f%%', startangle=90)
    plt.title('Abnormal element distribution')
    plt.show()
