import pandas as pd 

# print('minus one')
gps = pd.read_csv('/var/storage/sandra/mdc_analysis/mdc_data/nokia_data_gps.csv')
# print('zero')
wlan = pd.read_csv('/var/storage/sandra/mdc_analysis/mdc_data/nokia_data_gpswlan.csv')

# print('one')
# print('gps : ', gps.head(n=10), gps.shape, len(set(list(gps['user_id']))))
# print('two')
# print('wlan : ', wlan.head(n=10), wlan.shape)
# print('three')
merged = pd.concat([gps, wlan], axis=0,ignore_index=True)
# print('merged : ', merged.head(n=10), merged.shape, len(set(list(merged['user_id']))))
merged.to_csv('/var/storage/sandra/mdc_analysis/mdc_data/nokia_data_full.csv', index = False)

