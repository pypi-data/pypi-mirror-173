
import sys

from pyadlml.dataset.stats.activities import activities_count

sys.path.append("../")
from pyadlml.dataset import *

set_data_home('/tmp/pyadlml')
#data = fetch_kasteren_2010(house='C', cache=True)
data = fetch_casas_aruba(cache=True)
#data = fetch_aras(cache=True)

df_acts = data.df_activities
df_devs = data.df_devices

from pyadlml.dataset.util import get_sorted_index, infer_dtypes

df = activities_count(df_acts.copy())
acts = df_acts[ACTIVITY].unique()

from pyadlml.plot import contingency_states
from pyadlml.dataset.stats.acts_and_devs import contingency_table_states, contingency_table_states_old
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)
from time import time

print(len(df_devs))
dtypes = infer_dtypes(df_devs)
df_devs = df_devs[df_devs[DEVICE].isin(dtypes[BOOL])]
df_devs = df_devs.iloc[:100000, :]

parallel = True

if parallel:
    from pandarallel import pandarallel
    pandarallel.initialize()

start = time()
df_con = contingency_table_states_old(df_devs.copy(), df_acts.copy(), distributed=parallel)
contingency_states(df_con_tab=df_con, file_path='tmp_con_old.png')
end = time()
print('second func: ', end - start)
#                       kasteren    amsterdam   aras    casas
# normal        20000 -> 431.80     9.676       55.6
# normal        30000 -> 21.11                  56.5
# normal        50000 ->                        58.4    66.33
# normal        80000 ->                        60.4
# normal       100000 ->                        60.7
# pandarallel   20000 -> 63.0
# pandarallel   30000 -> 63.4
# pandarallel   50000 -> 3.6                    11.2
# pandarallel  100000 ->                        11.8    69.45


start = time()
df_con = contingency_table_states(df_devs.copy(), df_acts.copy(), distributed=parallel)
contingency_states(df_con_tab=df_con, file_path='tmp_con_new.png')
end = time()
print('first func: ', end - start)
#                       kasteren    amsterdam   aras    casas
# normal        20000 -> 41.42s     5.74        36.03
# normal        30000 -> 51.72                  53.67
# normal        50000 -> 233.64 ~4min           87.98
# normal        80000 ->                        139.9
# normal       100000 ->                        174.6   29.5
# pandarallel   20000 -> 7.35s
# pandarallel   30000 -> 9.94s
# pandarallel   50000 -> 3.17                   14.8
# pandarallel  100000 ->                        29.8    15.6

