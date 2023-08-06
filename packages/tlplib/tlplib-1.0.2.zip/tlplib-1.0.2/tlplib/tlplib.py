import pandas as pd


def convertPercent(val):
	return str(val)


def run(path_picked, path_full, path_out):
	"""
	:param path_picked: 已挑券单路径
	:param path_full: 原始券单路径
	:param path_out: 输出券单路径
	:return: none
	"""
	df = pd.read_excel(path_picked, converters={'code': convertPercent})
	df1 = pd.read_excel(path_full, converters={'证券代码': convertPercent})

	df_list = df['code'].tolist()
	df2 = df1.drop(df1[df1['证券代码'].isin(df_list)].index, axis=0)

	df2['证券代码'] = df2['证券代码'].apply(lambda x: x + '.SH' if x > '599999' else x + '.SZ')
	df2.drop(['证券名称'], axis=1, inplace=True)

	df2.to_csv(path_out, index=False, header=False)