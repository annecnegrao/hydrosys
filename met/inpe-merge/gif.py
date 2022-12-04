import datetime as dt
import pandas as pd
import imageio

datai = dt.date(2015,2,1)
dataf = dt.date(2015,3,31)

dias = pd.date_range(datai, dataf)
files = []
for dia in dias:
    strdia = dt.datetime.strftime(dia, '%Y-%m-%d')
    files.append(f'./plots/{strdia}.png')

images = []
strdatai = dt.datetime.strftime(datai, '%Y%m%d')
strdataf = dt.datetime.strftime(dataf, '%Y%m%d')

# for file in files:
#     images.append(imageio.v2.imread(file))
#imageio.mimsave(f'{strdatai}-{strdataf}.gif', images)

with imageio.get_writer(f'{strdatai}-{strdataf}.gif', mode='I', duration=1) as writer:
    for file in files:
        image = imageio.v2.imread(file)
        writer.append_data(image)

print('Fim! =D')