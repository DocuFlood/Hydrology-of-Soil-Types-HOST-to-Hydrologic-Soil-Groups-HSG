import os
import pandas as pd


csv_file_path = 'HOST.csv' # Update this to your desired location


data = pd.read_csv(csv_file_path)


host_to_scs = {
    'A': [1, 2, 4, 11, 13],
    'B': [3, 5],
    'C': [6, 9, 10, 14, 16, 17, 18, 24],
    'D': [7, 8, 12, 15, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 98]  
}


host_to_scs_reverse = {}
for group, hosts in host_to_scs.items():
    for host in hosts:
        host_to_scs_reverse[host] = group


def convert_host_to_scs(row):
    scs_groups = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for host, percentage in row.items():
        if host.startswith('HOSTCODE'):
            if percentage > 0:  
                host_class = int(host.replace('HOSTCODE', ''))
                scs_group = host_to_scs_reverse.get(host_class, 'D')  
                scs_groups[scs_group] += percentage
    
    
    sorted_scs = sorted(scs_groups.items(), key=lambda item: item[1], reverse=True)
    primary_class, primary_percentage = sorted_scs[0]
    secondary_class, secondary_percentage = sorted_scs[1]

    if primary_class == 'D' and primary_percentage < 75 and secondary_class in ['A', 'B', 'C']:
        
        weighted_class = f"{secondary_class}D"
    elif primary_class == 'D' and primary_percentage >= 75:
        
        weighted_class = 'D'
    else:
        
        weighted_class = primary_class

    return pd.Series([weighted_class])


first_columns = data.iloc[:, :3]
host_columns = data.filter(regex='^HOSTCODE')
scs_data = host_columns.apply(convert_host_to_scs, axis=1)


result_data = pd.concat([first_columns, scs_data], axis=1)
result_data.columns = ['FID', 'ID', 'IDO', 'Weighted_SCS_Class']


output_file_path = 'SCS_Soil_Groups.csv'   # Update this to your desired location
result_data.to_csv(output_file_path, index=False)
