#导入数据集

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

full = pd.read_csv(r'E:\PythonPratise\Game\tap_fun_test.csv')
pd.set_option('display.max_columns', 10)  # 方便显示，只显示10列字段。

print('full前五行：', full.head(5))
print(full.info())

# 检查重复值和缺失值
duplicate_row = full.duplicated(subset=['user_id'])  # 筛选出重复的user_id
print('duplicate_row', duplicate_row.describe())
print(full.loc[duplicate_row, :].head(5))  # 筛选出重复的user_id的记录
print('full.isna:', full.isna().head(5))  # 检查空字符串
print('full.isnull:', full.isnull().head(5))  # 检查null

# 构造注册日期字段用于统计分析注册随时间的走势。
full['register_date'] = full['register_time'].astype('datetime64').dt.date
count_date = full.groupby(by='register_date').agg({'user_id': 'count'})  # 按注册日期统计注册人数
count_date = pd.Series(data=count_date['user_id'], index=count_date.index)
print(count_date.head(5))

# 按注册日期统计新增用户数，使用柱状图显示。
fig = plt.figure(figsize=(10, 10))
count_date.plot(kind='bar')
plt.axhline(y=count_date.mean(), label='平均值', color='red', linestyle=':')
plt.annotate(s='平均值', xy=(12,count_date.mean()), xytext=(12,count_date.mean()))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.xlabel('日期',fontsize=14)
plt.ylabel('新注册用户数',fontsize=14)
plt.title('2018年3月7日至22月新注册用户数',fontsize=18)
plt.show()

# 留存用户数
retention_count = (full['avg_online_minutes'] > 0).astype('int').sum()
print('retention_count', retention_count)
retention_user = full.loc[full['avg_online_minutes'] > 0,:]
print('留存用户：',retention_user.head(5))
print('留存用户用户的7天在线时间的总计：', retention_user['avg_online_minutes'].sum())
print('留存用户的7天在线时间的平均值：', retention_user['avg_online_minutes'].mean())

# 留存用户的分钟数组成：饼图
retention_level = pd.cut(x=full['avg_online_minutes'], bins=[-0.01, 0, 1, 5, np.inf])
print(retention_level.value_counts())
retention_level2 = retention_level.value_counts()[0:5]  #使用前5种占比大的结果来画图。
print(retention_level2)
retention_level3= pd.Series([17413,320116,284623,206782],
                            index=['0分钟','0至1分钟','1至5分钟','5分钟以上'])
fig = plt.figure(figsize=(10, 10))
retention_level3.plot(kind='pie',fontsize=14)
plt.ylabel('平均在线时长',fontsize=14)
plt.title('平均在线时长的分布情况',fontsize=18)
plt.show()

# 付费情况
revenue = full.loc[full['pay_price'] > 0, 'pay_price'].sum()
paid_user_count = (full['pay_price'] > 0).astype('int').sum()
pr = paid_user_count / retention_count
arpu = revenue / retention_count
arppu = revenue / paid_user_count
print('付费人数，付费率，arpu，arppu分别是：', paid_user_count, pr, arpu, arppu )

# ARPU消费对比图，使用柱状图
paid_user = pd.Series([19549, 791972], index=['付费用户', '非付费用户'])
fig = plt.figure(figsize=(10, 10))
paid_user.plot(kind='bar',fontsize=14)
plt.title('付费用户和非付费用户数对比',fontsize=18)
plt.xticks(rotation=0)
plt.yticks(ticks=[10000, 100000, 800000, 900000])
plt.ylabel('用户数',fontsize=14)
plt.show()

# PVP和PVE对战次数的对比
print('PVP对战次数的分布：', full['pvp_battle_count'].value_counts().head(5))
print('主动发起PVP对战的次数的分布：', full['pvp_lanch_count'].value_counts().head(5))

print('PVE对战次数的分布：', full['pve_battle_count'].value_counts().head(5))
print('主动发起PVE对战的次数的分布：', full['pve_lanch_count'].value_counts().head(5))

# PVP和PVE的对战次数和发起对战次数的对比
battle = pd.DataFrame(
         data=[full.loc[full['pvp_battle_count']>0, 'pvp_battle_count'].value_counts().head(5),
         full.loc[full['pvp_lanch_count']>0, 'pvp_lanch_count'].value_counts().head(5),
         full.loc[full['pve_battle_count']>0, 'pve_battle_count'].value_counts().head(5),
         full.loc[full['pve_lanch_count']>0, 'pve_lanch_count'].value_counts().head(5)
         ], index=['pvp_battle_count','pvp_lanch_count','pve_battle_count','pve_lanch_count'])

fig = plt.figure(figsize=(10, 10))
battle.plot(kind='barh', fontsize=14)
plt.title('PVP和PVE的对战次数/发起对战次数的对比',fontsize=18)
plt.xlabel('对战用户数', fontsize=14)
plt.legend(['1次','2次','3次','4次','5次'])
plt.show()

