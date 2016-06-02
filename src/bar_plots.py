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

####################################################################################
# https://github.com/dcchivian/kb_sdk_catalog_metrics/blob/master/src/bar_plots.py #
####################################################################################

from biokbase.catalog.Client import Catalog
catalog = Catalog(url="https://kbase.us/services/catalog")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
#pd.__version__

# requires Admin priveleges
#aggregated_by_app = catalog.get_exec_aggr_stats({})
aggregated_by_user = catalog.get_exec_aggr_table({})

total_runs_by_app = dict()
total_runs_by_module = dict()
total_users_by_app = dict()
total_users_by_module = dict()
total_app_runs_by_user = dict()
total_apps_by_user = dict()
total_modules_by_user = dict()
module_seen_by_user = dict()
user_seen_by_module = dict()

for app_user_stats in aggregated_by_user:
    app    = app_user_stats['func']
    module = app_user_stats['func_mod']
    user   = app_user_stats['user']
    n      = app_user_stats['n']
    
    if filter_internal_users and user in internal_users:
        continue
        
    try:
        total_runs_by_app[app] += n
        total_users_by_app[app] += 1
    except:
        total_runs_by_app[app] = n
        total_users_by_app[app] = 1
        
    try:
        total_runs_by_module[module] += n        
    except:
        total_runs_by_module[module] = n

    try:
        users_seen = user_seen_by_module[module]
        if user not in users_seen:      
            total_users_by_module[module] += 1
            user_seen_by_module[module][user] = True
    except:
        total_users_by_module[module] = 1
        user_seen_by_module[module] = dict()
        user_seen_by_module[module][user] = True

    try:
        total_app_runs_by_user[user] += n
    except:
        total_app_runs_by_user[user] = n
        
    try:
        total_apps_by_user[user] += 1
    except:
        total_apps_by_user[user] = 1
        
    try:
        modules_seen = module_seen_by_user[user]
        if module not in modules_seen:
            total_modules_by_user[user] += 1
            module_seen_by_user[user][module] = True
    except:
        total_modules_by_user[user] = 1
        module_seen_by_user[user] = dict()
        module_seen_by_user[user][module] = True

###############################################################################
# NEW CELL                                                              
###############################################################################

total_users_by_module_df = pd.DataFrame({'total_users_by_module': pd.Series(total_users_by_module.values(),
                                                                            index=total_users_by_module.keys())
                                     })
total_users_by_app_df = pd.DataFrame({'total_users_by_app': pd.Series(total_users_by_app.values(),
                                                                      index=total_users_by_app.keys())
                                     })
total_runs_by_module_df = pd.DataFrame({'total_runs_by_module': pd.Series(total_runs_by_module.values(),
                                                                          index=total_runs_by_module.keys())
                                     })
total_runs_by_app_df = pd.DataFrame({'total_runs_by_app': pd.Series(total_runs_by_app.values(),
                                                                    index=total_runs_by_app.keys())
                                     })
total_modules_by_user_df = pd.DataFrame({'total_modules_by_user': pd.Series(total_modules_by_user.values(),
                                                                            index=total_modules_by_user.keys())
                                     })
total_apps_by_user_df = pd.DataFrame({'total_apps_by_user': pd.Series(total_apps_by_user.values(),
                                                                      index=total_apps_by_user.keys())
                                     })
total_app_runs_by_user_df = pd.DataFrame({'total_app_runs_by_user': pd.Series(total_app_runs_by_user.values(),
                                                                              index=total_app_runs_by_user.keys())
                                     })

###############################################################################
# NEW CELL                                                              
###############################################################################

print (total_users_by_module_df.sort(columns='total_users_by_module', ascending=False))

###############################################################################
# NEW CELL                                                              
###############################################################################

total_users_by_module_plot = total_users_by_module_df \
                                .sort(columns='total_users_by_module', ascending=False) \
                                .head(30) \
                                .plot(kind='bar', figsize=(15,5), fontsize=15)
total_users_by_module_plot.xaxis.grid(False)
total_users_by_module_plot.yaxis.grid(True) 

###############################################################################
# NEW CELL                                                              
###############################################################################

print (total_users_by_app_df.sort(columns='total_users_by_app', ascending=False))

###############################################################################
# NEW CELL                                                              
###############################################################################

total_users_by_app_plot = total_users_by_app_df \
                                .sort(columns='total_users_by_app', ascending=False) \
                                .head(30) \
                                .plot(kind='bar', figsize=(15,5), fontsize=15)
total_users_by_app_plot.xaxis.grid(False)
total_users_by_app_plot.yaxis.grid(True) 

###############################################################################
# NEW CELL                                                              
###############################################################################

print (total_runs_by_module_df.sort(columns='total_runs_by_module', ascending=False))

###############################################################################
# NEW CELL                                                              
###############################################################################

total_runs_by_module_plot = total_runs_by_module_df \
                                .sort(columns='total_runs_by_module', ascending=False) \
                                .head(30) \
                                .plot(kind='bar', figsize=(15,5), fontsize=15)
total_runs_by_module_plot.xaxis.grid(False)
total_runs_by_module_plot.yaxis.grid(True) 

###############################################################################
# NEW CELL                                                              
###############################################################################

print (total_runs_by_app_df.sort(columns='total_runs_by_app', ascending=False))

###############################################################################
# NEW CELL                                                              
###############################################################################

total_runs_by_app_plot = total_runs_by_app_df \
                                .sort(columns='total_runs_by_app', ascending=False) \
                                .head(30) \
                                .plot(kind='bar', figsize=(15,5), fontsize=15)
total_runs_by_app_plot.xaxis.grid(False)
total_runs_by_app_plot.yaxis.grid(True) 

###############################################################################
# NEW CELL                                                              
###############################################################################

print (total_app_runs_by_user_df.sort(columns='total_app_runs_by_user', ascending=False))

###############################################################################
# NEW CELL                                                              
###############################################################################

total_app_runs_by_user_plot = total_app_runs_by_user_df \
                                .sort(columns='total_app_runs_by_user', ascending=False) \
                                .head(30) \
                                .plot(kind='bar', figsize=(15,5), fontsize=15)
total_app_runs_by_user_plot.xaxis.grid(False)
total_app_runs_by_user_plot.yaxis.grid(True) 

###############################################################################
# NEW CELL                                                              
###############################################################################

print (total_modules_by_user_df.sort(columns='total_modules_by_user', ascending=False))

###############################################################################
# NEW CELL                                                              
###############################################################################

total_modules_by_user_plot = total_modules_by_user_df \
                                .sort(columns='total_modules_by_user', ascending=False) \
                                .head(30) \
                                .plot(kind='bar', figsize=(15,5), fontsize=15)
total_modules_by_user_plot.xaxis.grid(False)
total_modules_by_user_plot.yaxis.grid(True) 

###############################################################################
# NEW CELL                                                              
###############################################################################

print (total_apps_by_user_df.sort(columns='total_apps_by_user', ascending=False))

###############################################################################
# NEW CELL                                                              
###############################################################################

total_apps_by_user_plot = total_apps_by_user_df \
                                .sort(columns='total_apps_by_user', ascending=False) \
                                .head(30) \
                                .plot(kind='bar', figsize=(15,5), fontsize=15)
total_apps_by_user_plot.xaxis.grid(False)
total_apps_by_user_plot.yaxis.grid(True) 

###############################################################################
# END
###############################################################################
