# functions to perform exploratory data analysis of the daily dataframes per user

def extrema(df):
	return [df.loc[df['lat'].idxmin()][['lat', 'lon']], df.loc[df['lat'].idxmax()][['lat', 'lon']], df.loc[df['lon'].idxmin()][['lat', 'lon']], df.loc[df['lon'].idxmax()][['lat', 'lon']]]
	 

def n_samples(df):
	return df.shape[0]

def sampling_times(df):
	return [x.total_seconds() for x in df['datetime'].diff()[1:]]