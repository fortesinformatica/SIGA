import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

with open('20190410.log', 'r', encoding='utf-8', errors='ignore') as content_file:
    content = content_file.readlines()

aux = []
bytes_vazao = []
vazao = []
time_train = []

for line in content:
    if 'INFO: Trained' in line:
        idx = line.find('Trained') + 8
        end_idx = line.find('bytes') - 1

        size_collection = line[idx: end_idx]
        bytes_vazao.append(int(size_collection))

    if 'transitions:' in line:
        idx = line.find('transitions:') + len('transitions:') + 1

        size_collection = line[idx: -1]
        vazao.append(int(size_collection))

    if 'INFO: Training...' in line:
        aux = []
        date = datetime.strptime(line[0:19], '%Y-%m-%d %H:%M:%S')
        date - timedelta(hours=3)
        aux.append(date)

    if 'INFO: Training Finished' in line:
        date = datetime.strptime(line[0:19], '%Y-%m-%d %H:%M:%S')
        date - timedelta(hours=3)
        aux.append(date)
        if len(aux) == 2:
            time_train.append(aux)


days = [d[0].date() for d in time_train]
timeline = [d[0] for d in time_train]


cost_train = [(date[1] - date[0]).seconds for date in time_train]
print("Média segundos: {:.2f}\nMédia minutos: {:.2f}".format(np.mean(cost_train), np.mean(cost_train)/60))
print("Média quantidade de transições: {:.2f}\nMédia quantidade de bytes: {:.2f}".format(np.mean(vazao),
                                                                                         np.mean(bytes_vazao)))

print("Total quantidade de transições: {:.2f}\nTotal quantidade de Mbytes: {:.2f}".format(np.sum(vazao),
                                                                                          np.sum(bytes_vazao)/1048576))


fig, ax1 = plt.subplots()


color = 'tab:red'
ax1.set_ylabel('Qtd SigaTimeLine', color=color)
ax1.plot(timeline, bytes_vazao, color=color)
ax1.tick_params(axis='y', labelcolor=color, rotation=45)
ax1.tick_params(axis='x', rotation=45, labelsize=8)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('time (s)', color=color)  # we already handled the x-label with ax1
ax2.plot(timeline, cost_train, color=color)
ax2.tick_params(axis='y', labelcolor=color)


fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.title("Tempo treinamento: {}h à {}h".format(timeline[0].strftime("%d/%m/%y %H"),
                                                timeline[-1].strftime("%d/%m/%y %H")))

color = ['#b3e6b3', '#339933']
init = 0
for d in np.unique(days):
    end = days.count(d) + init - 1
    c = d.day % 2
    plt.axvspan(days[init], days[end] + timedelta(days=1), facecolor=color[c], alpha=0.3)
    init = end + 1


days = np.unique(days)
date_list = []
for d in days:
    date_list.append(d)
    date_list.append(datetime.combine(d, datetime.min.time()) + timedelta(hours=12))

# plt.xlim(xmin=date_list[0])
# plt.xlim(xmax=date_list[-1])

if timeline[0].hour >= 12:
    date = timeline[0].date()
    initial_day = datetime.combine(date, datetime.min.time()) + timedelta(hours=12)
else:
    initial_day = timeline[0].date()

plt.xlim(xmin=initial_day)
plt.xlim(xmax=timeline[-1] + timedelta(hours=1))

fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y %Hh'))
plt.show()
