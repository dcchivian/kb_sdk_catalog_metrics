###############################################################################
# DEPLOYED AT
#   https://narrative.kbase.us/narrative/ws.15030.obj.1
###############################################################################

###############################################################################
# NEW CELL
###############################################################################

filter_internal_users = True
#filter_internal_users = False
if filter_internal_users:
    internal_users = dict()
    import urllib2
    response = urllib2.urlopen('https://raw.githubusercontent.com/kbase/metrics/master/kbase-staff.lst')
    for user in response.read().split("\n"):
        internal_users[user] = True

###############################################################################
# NEW CELL
###############################################################################

###########################################################################################
# https://github.com/dcchivian/kb_sdk_catalog_metrics/blob/master/src/time_based_plots.py #
###########################################################################################

from biokbase.catalog.Client import Catalog
catalog = Catalog(url="https://kbase.us/services/catalog")
import pandas as pd
import numpy as np
import math as math
import matplotlib.pyplot as plt
%matplotlib inline
#pd.__version__

import datetime, time
secs_per_week = 7*24*60*60 


# Init data containers
#
total_users = []
total_regular_users = []
seen_user = dict()
seen_twice_user = dict()

total_runs_by_app_vector = dict()
total_runs_by_app_final = dict()

total_users_by_app_vector = dict()
total_users_by_app_final = dict()

total_app_runs_by_user_vector = dict()
total_app_runs_by_user_final = dict()

total_app_runs_by_user_and_app_vector = dict()
total_app_runs_by_user_and_app_final = dict()

total_app_runs_by_app_and_user_vector = dict()
total_app_runs_by_app_and_user_final = dict()


# Config
#
dates = [ '2016-01-02',
          '2016-01-09',
          '2016-01-16',
          '2016-01-23',
          '2016-01-30',
          '2016-02-06',
          '2016-02-13',
          '2016-02-20',
          '2016-02-27',
          '2016-03-05',
          '2016-03-12',
          '2016-03-19',
          '2016-03-26',
          '2016-04-02',
          '2016-04-09',
          '2016-04-16',
          '2016-04-23',
          '2016-04-30',
          '2016-04-09',
          '2016-05-07',
          '2016-05-14',
          '2016-05-21',
          '2016-05-28',
          '2016-06-04'
        ]

color_list = ['#FF0000',
              '#FF8000',
              '#FFFF00',
              '#80FF00',
              '#00FF00',
              '#00FF80',
              '#00FFFF',
              '#0080FF',
              '#0000FF',
              '#7F00FF',
              '#FF00FF',
              '#FF007F',
              '#990000',
              '#994C00',
              '#999900',
              '#4C9900',
              '#009900',
              '#00994C',
              '#009999',
              '#004C99',
              '#000099',
              '#4C0099',
              '#990099',
              '#99004C',
              '#FF6666',
              '#FFB266',
              '#FFFF66',
              '#B2FF66',
              '#66FF66',
              '#66FFB2',
              '#66FFB2',
              '#66FFFF',
              '#66B2FF',
              '#6666FF',
              '#B266FF',
              '#FF66FF',
              '#FF66B2'
             ]

# Calculate
#
for i,date_str in enumerate(dates):

    # year, month, day, something, something
    year,month,day = date_str.split('-')
    date = datetime.datetime(int(year),int(month),int(day),0,0)
    date_in_secs = (date - datetime.datetime(1970,1,1)).total_seconds()
    date_week_ago_secs = date_in_secs - secs_per_week
    
    # init this dates user tally
    if i == 0:
        total_users.append(0)
        total_regular_users.append(0)
    else:
        total_users.append(total_users[i-1])
        total_regular_users.append(total_regular_users[i-1])

    # Get user exec stats
    #   requires Admin priveleges
    #
    time_slice = { 'begin': int(date_week_ago_secs)+1,
                   'end': int(date_in_secs)
                 }
    #aggregated_by_app = catalog.get_exec_aggr_stats({})
    aggregated_by_user = catalog.get_exec_aggr_table(time_slice)

    total_runs_by_app = dict()
    total_users_by_app = dict()
    total_app_runs_by_user = dict()
    total_app_runs_by_user_and_app = dict()
    total_app_runs_by_app_and_user = dict()

    for app_user_stats in aggregated_by_user:
        app    = app_user_stats['func']
        user   = app_user_stats['user']
        n      = app_user_stats['n']

        if filter_internal_users and user in internal_users:
            continue
        
        # user tally
        if user in seen_user:
            if seen_user[user] == i:
                pass
            else:
                if user not in seen_twice_user:
                    seen_twice_user[user] = True
                    total_regular_users[i] += 1
        else:
            seen_user[user] = i  # keep track of when first seen
            total_users[i] += 1

        # runs by app and by user
        try:
            total_runs_by_app[app] += n
            total_users_by_app[app] += 1
        except:
            total_runs_by_app[app] = n
            total_users_by_app[app] = 1

        try:
            total_app_runs_by_user[user] += n
        except:
            total_app_runs_by_user[user] = n
        
        # 2D USER and APP
        try:
            user_defined = total_app_runs_by_user_and_app[user]
            try:
                app_defined = total_app_runs_by_user_and_app[user][app]
                total_app_runs_by_user_and_app[user][app] += n
            except:
                total_app_runs_by_user_and_app[user][app] = n
        except:
            total_app_runs_by_user_and_app[user] = dict()
            total_app_runs_by_user_and_app[user][app] = n

        # 2D APP and USER
        try:
            app_defined = total_app_runs_by_app_and_user[app]
            try:
                user_defined = total_app_runs_by_app_and_user[app][user]
                total_app_runs_by_app_and_user[app][user] += n
            except:
                total_app_runs_by_app_and_user[app][user] = n
        except:
            total_app_runs_by_app_and_user[app] = dict()
            total_app_runs_by_app_and_user[app][user] = n
                
    # Add to vectors
    #
    for app in total_runs_by_app.keys():
        try:
            vector = total_runs_by_app_vector[app]
            total_runs_by_app_vector[app][i] = total_runs_by_app[app]
        except:
            total_runs_by_app_vector[app] = []
            for j in range(0,len(dates)):
                total_runs_by_app_vector[app].append(0)
            total_runs_by_app_vector[app][i] = total_runs_by_app[app]

    for app in total_users_by_app.keys():
        try:
            vector = total_users_by_app_vector[app]
            total_users_by_app_vector[app][i] = total_users_by_app[app]
        except:
            total_users_by_app_vector[app] = []
            for j in range(0,len(dates)):
                total_users_by_app_vector[app].append(0)
            total_users_by_app_vector[app][i] = total_users_by_app[app]
                
    for user in total_app_runs_by_user.keys():
        try:
            vector = total_app_runs_by_user_vector[user]
            total_app_runs_by_user_vector[user][i] = total_app_runs_by_user[user]
        except:
            total_app_runs_by_user_vector[user] = []
            for j in range(0,len(dates)):
                total_app_runs_by_user_vector[user].append(0)
            total_app_runs_by_user_vector[user][i] = total_app_runs_by_user[user]

    for user in total_app_runs_by_user_and_app.keys():
        try:
            user_dict = total_app_runs_by_user_and_app_vector[user]
            for app in total_app_runs_by_user_and_app[user].keys():
                try:
                    app_vector = total_app_runs_by_user_and_app_vector[user][app]
                    total_app_runs_by_user_and_app_vector[user][app][i] = total_app_runs_by_user_and_app[user][app]
                except:
                    total_app_runs_by_user_and_app_vector[user][app] = []
                    for j in range(0,len(dates)):
                        total_app_runs_by_user_and_app_vector[user][app].append(0)
                    total_app_runs_by_user_and_app_vector[user][app][i] = total_app_runs_by_user_and_app[user][app]
        except:
            total_app_runs_by_user_and_app_vector[user] = dict()

    for app in total_app_runs_by_app_and_user.keys():
        try:
            app_dict = total_app_runs_by_app_and_user_vector[app]
            for user in total_app_runs_by_app_and_user[app].keys():
                try:
                    user_vector = total_app_runs_by_app_and_user_vector[app][user]
                    total_app_runs_by_app_and_user_vector[app][user][i] = total_app_runs_by_app_and_user[app][user]
                except:
                    total_app_runs_by_app_and_user_vector[app][user] = []
                    for j in range(0,len(dates)):
                        total_app_runs_by_app_and_user_vector[app][user].append(0)
                    total_app_runs_by_app_and_user_vector[app][user][i] = total_app_runs_by_app_and_user[app][user]
        except:
            total_app_runs_by_app_and_user_vector[app] = dict()            
            
            
# turn vector into accumulation
#
for i in range(1,len(dates)):
    for app in total_runs_by_app_vector.keys():
        total_runs_by_app_vector[app][i] += total_runs_by_app_vector[app][i-1]
    for app in total_users_by_app_vector.keys():
        total_users_by_app_vector[app][i] += total_users_by_app_vector[app][i-1]
    for user in total_app_runs_by_user_vector.keys():
        total_app_runs_by_user_vector[user][i] += total_app_runs_by_user_vector[user][i-1]
        
    for user in total_app_runs_by_user_and_app_vector.keys():
        for app in total_app_runs_by_user_and_app_vector[user].keys():
            total_app_runs_by_user_and_app_vector[user][app][i] += total_app_runs_by_user_and_app_vector[user][app][i-1]

    for app in total_app_runs_by_app_and_user_vector.keys():
        for user in total_app_runs_by_app_and_user_vector[app].keys():
            total_app_runs_by_app_and_user_vector[app][user][i] += total_app_runs_by_app_and_user_vector[app][user][i-1]
            
            
# final totals
#
for app in total_runs_by_app_vector:
    total_runs_by_app_final[app] = total_runs_by_app_vector[app][-1]
for app in total_users_by_app_vector:
    total_users_by_app_final[app] = total_users_by_app_vector[app][-1]
for user in total_app_runs_by_user_vector:
    total_app_runs_by_user_final[user] = total_app_runs_by_user_vector[user][-1]
    
for user in total_app_runs_by_user_and_app_vector.keys():
    total_app_runs_by_user_and_app_final[user] = dict()
    for app in total_app_runs_by_user_and_app_vector[user].keys():
        total_app_runs_by_user_and_app_final[user][app] = total_app_runs_by_user_and_app_vector[user][app][-1]

for app in total_app_runs_by_app_and_user_vector.keys():
    total_app_runs_by_app_and_user_final[app] = dict()
    for user in total_app_runs_by_app_and_user_vector[app].keys():
        total_app_runs_by_app_and_user_final[app][user] = total_app_runs_by_app_and_user_vector[app][user][-1]

###############################################################################
# NEW CELL
###############################################################################

total_users_df = pd.DataFrame({'total_users': pd.Series(total_users,
                                                        index=dates),
                               'total_regular_users': pd.Series(total_regular_users,
                                                               index=dates)
                              })

###############################################################################
# NEW CELL
###############################################################################

total_users_plot = total_users_df \
                                .plot(kind="line", figsize=(15,5), ylim=(0,total_users[-1]+int(math.floor(total_users[-1]/10))), fontsize=15, lw=5)
total_users_plot.xaxis.grid(True)
total_users_plot.yaxis.grid(True) 

###############################################################################
# NEW CELL
###############################################################################

total_runs_by_app_pandas_struct = dict()
limit = 20
line_index = []
colors = []
max_val = 0
sorted_total_runs_by_app = sorted(total_runs_by_app_final, key=total_runs_by_app_final.get, reverse=True)
for i,app in enumerate(sorted_total_runs_by_app):
    if total_runs_by_app_final[app] > max_val:
        max_val = total_runs_by_app_final[app]
    line_index.append(app)
    colors.append(color_list[i%len(color_list)])
    total_runs_by_app_pandas_struct[app] = pd.Series(total_runs_by_app_vector[app], index=dates)
    if i >= limit:
        break
total_runs_by_app_df = pd.DataFrame(total_runs_by_app_pandas_struct)
color_series = pd.Series(colors, index=line_index)

###############################################################################
# NEW CELL
###############################################################################

total_runs_by_app_plot = total_runs_by_app_df \
                                .plot(kind="line", figsize=(15,10), color=color_series, ylim=(0,max_val+int(math.floor(max_val/10))), fontsize=15, lw=5)
total_runs_by_app_plot.xaxis.grid(True)
total_runs_by_app_plot.yaxis.grid(True)
for app in sorted_total_runs_by_app:
    if total_runs_by_app_final[app] >= 0.1*max_val:
        total_runs_by_app_plot.text(len(dates)-0.5, total_runs_by_app_final[app], app, fontsize=20)

###############################################################################
# NEW CELL
###############################################################################

total_users_by_app_pandas_struct = dict()
limit = 20
line_index = []
colors = []
max_val = 0
sorted_total_users_by_app = sorted(total_users_by_app_final, key=total_users_by_app_final.get, reverse=True)
for i,app in enumerate(sorted_total_users_by_app):
    if total_users_by_app_final[app] > max_val:
        max_val = total_users_by_app_final[app]
    line_index.append(app)
    colors.append(color_list[i%len(color_list)])
    total_users_by_app_pandas_struct[app] = pd.Series(total_users_by_app_vector[app], index=dates)
    if i >= limit:
        break
total_users_by_app_df = pd.DataFrame(total_users_by_app_pandas_struct)
color_series = pd.Series(colors, index=line_index)

###############################################################################
# NEW CELL
###############################################################################

total_users_by_app_plot = total_users_by_app_df \
                                .plot(kind="line", figsize=(15,10), color=color_series, ylim=(0,max_val+int(math.floor(max_val/10))), fontsize=15, lw=5)
total_users_by_app_plot.xaxis.grid(True)
total_users_by_app_plot.yaxis.grid(True)
for app in sorted_total_users_by_app:
    if total_users_by_app_final[app] >= 0.1*max_val:
        total_users_by_app_plot.text(len(dates)-0.5, total_users_by_app_final[app], app, fontsize=20)

###############################################################################
# NEW CELL
###############################################################################

total_app_runs_by_user_pandas_struct = dict()
limit = 20
line_index = []
colors = []
max_val = 0
sorted_total_app_runs_by_user = sorted(total_app_runs_by_user_final, key=total_app_runs_by_user_final.get, reverse=True)
for i,user in enumerate(sorted_total_app_runs_by_user):
    if total_app_runs_by_user_final[user] > max_val:
        max_val = total_app_runs_by_user_final[user]
    line_index.append(user)
    colors.append(color_list[i%len(color_list)])
    total_app_runs_by_user_pandas_struct[user] = pd.Series(total_app_runs_by_user_vector[user], index=dates)
    if i >= limit:
        break
total_app_runs_by_user_df = pd.DataFrame(total_app_runs_by_user_pandas_struct)
color_series = pd.Series(colors, index=line_index)

###############################################################################
# NEW CELL
###############################################################################

total_app_runs_by_user_plot = total_app_runs_by_user_df \
                                .plot(kind="line", figsize=(15,10), color=color_series, ylim=(0,max_val+int(math.floor(max_val/10))), fontsize=15, lw=5)
total_app_runs_by_user_plot.xaxis.grid(True)
total_app_runs_by_user_plot.yaxis.grid(True)
for user in sorted_total_app_runs_by_user:
    if total_app_runs_by_user_final[user] >= 0.1*max_val:
        total_app_runs_by_user_plot.text(len(dates)-0.5, total_app_runs_by_user_final[user], user, fontsize=20)

###############################################################################
# NEW CELL
###############################################################################

# config for single user
user = 'mikaelacashman'

# make pandas dataframe
total_app_runs_by_user_and_app_pandas_struct = dict()  # just going to use app as key since user is collapsed
limit = 20
line_index = []
colors = []
max_val = 0
sorted_total_app_runs_by_user_and_app = sorted(total_app_runs_by_user_and_app_final[user], key=total_app_runs_by_user_and_app_final[user].get, reverse=True)
for i,app in enumerate(sorted_total_app_runs_by_user_and_app):
    if total_app_runs_by_user_and_app_final[user][app] > max_val:
        max_val = total_app_runs_by_user_and_app_final[user][app]
    line_index.append(app)
    colors.append(color_list[i%len(color_list)])
    total_app_runs_by_user_and_app_pandas_struct[app] = pd.Series(total_app_runs_by_user_and_app_vector[user][app], index=dates)
    if i >= limit:
        break
total_app_runs_by_user_and_app_df = pd.DataFrame(total_app_runs_by_user_and_app_pandas_struct)
color_series = pd.Series(colors, index=line_index)

# plot
total_app_runs_by_user_and_app_plot = total_app_runs_by_user_and_app_df \
                                .plot(kind="line", figsize=(15,10), color=color_series, ylim=(0,max_val+int(math.floor(max_val/10))), fontsize=15, lw=5)
total_app_runs_by_user_and_app_plot.xaxis.grid(True)
total_app_runs_by_user_and_app_plot.yaxis.grid(True)
for app in sorted_total_app_runs_by_user_and_app:
    if total_app_runs_by_user_and_app_final[user][app] >= 0.1*max_val:
        total_app_runs_by_user_and_app_plot.text(len(dates)-0.5, total_app_runs_by_user_and_app_final[user][app], app, fontsize=20)

###############################################################################
# NEW CELL
###############################################################################

# config for single app
app = 'gapfill_metabolic_model'

# make pandas dataframe
total_app_runs_by_app_and_user_pandas_struct = dict()  # just going to use user as key since app is collapsed
limit = 20
line_index = []
colors = []
max_val = 0
sorted_total_app_runs_by_app_and_user = sorted(total_app_runs_by_app_and_user_final[app], key=total_app_runs_by_app_and_user_final[app].get, reverse=True)
for i,user in enumerate(sorted_total_app_runs_by_app_and_user):
    if total_app_runs_by_app_and_user_final[app][user] > max_val:
        max_val = total_app_runs_by_app_and_user_final[app][user]
    line_index.append(user)
    colors.append(color_list[i%len(color_list)])
    total_app_runs_by_app_and_user_pandas_struct[user] = pd.Series(total_app_runs_by_app_and_user_vector[app][user], index=dates)
    if i >= limit:
        break
total_app_runs_by_app_and_user_df = pd.DataFrame(total_app_runs_by_app_and_user_pandas_struct)
color_series = pd.Series(colors, index=line_index)

# plot
total_app_runs_by_app_and_user_plot = total_app_runs_by_app_and_user_df \
                                .plot(kind="line", figsize=(15,10), color=color_series, ylim=(0,max_val+int(math.floor(max_val/10))), fontsize=15, lw=5)
total_app_runs_by_user_and_app_plot.xaxis.grid(True)
total_app_runs_by_user_and_app_plot.yaxis.grid(True)
for user in sorted_total_app_runs_by_app_and_user:
    if total_app_runs_by_app_and_user_final[app][user] >= 0.1*max_val:
        total_app_runs_by_app_and_user_plot.text(len(dates)-0.5, total_app_runs_by_app_and_user_final[app][user], user, fontsize=20)

###############################################################################
# END
###############################################################################
