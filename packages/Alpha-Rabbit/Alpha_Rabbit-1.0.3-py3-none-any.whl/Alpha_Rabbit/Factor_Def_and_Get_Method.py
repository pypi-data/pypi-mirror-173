'''所有因子一律只计算一日数据'''
import pandas as pd
import numpy as np

class Factor_get_method(object):
    def __init__(self) -> None:
        pass

    def get_all_tables(self,con):
        sql = "select name from sqlite_master where type ='table' order by name"
        c = con.cursor()
        result = c.execute(sql)
        factorfilelist = [i[0] for i in result.fetchall()]
        return factorfilelist

    def sql_fetch(self,con,tablename):
        cursorObj = con.cursor()
        cursorObj.execute('PRAGMA table_info("{}")'.format(tablename))
        return cursorObj.fetchall()
    
    def sql_exec(self,sql,sqlcols,conn):
        cur = conn.cursor()
        result = cur.execute(sql)
        result = pd.DataFrame(result,columns = sqlcols).set_index(['date','symbol'])
        return result

    def get_prev_days_factor_by_name(self,factorname:str,date:str,conn):
        sql = "select * from {} where {}.date >= '{}'".format(factorname,factorname,date)
        sqlcols = [txt[1] for txt in self.sql_fetch(conn,factorname)]
        return self.sql_exec(sql,sqlcols,conn)
    
    def get_selected_date_factor_by_name(self,factorname:str,date:str,conn):
        sql = "select * from {} where {}.date = '{}'".format(factorname,factorname,date)
        sqlcols = [txt[1] for txt in self.sql_fetch(conn,factorname)]
        return self.sql_exec(sql,sqlcols,conn)
    
def mmt_intraday_M(tempClose,tempOpen):
    # 1个月日内动量
    mmt_intraday_M = (tempClose/tempOpen - 1).iloc[-22:].cumsum()
    mmt_intraday_M = pd.DataFrame(mmt_intraday_M.iloc[-1:].stack(),columns = ['mmt_intraday_M'])
    return mmt_intraday_M

# 一个月振幅调整动量
def mmt_range_M(tempHigh,tempLow,tempClose):
    High_m = tempHigh.iloc[-22:].max()
    Low_m = tempLow.iloc[-22:].min()
    mmt_range_M = (High_m-Low_m)/tempClose.shift(22)
    mmt_range_M = pd.DataFrame(mmt_range_M.iloc[-1:].stack(),columns = ['mmt_range_M'])
    return mmt_range_M

def mmt_overnight_M(tempOpen,tempClose):
    # 隔夜动量
    mmt_overnight = tempOpen/tempClose.shift(1) - 1
    todaydate = mmt_overnight.index[-1]
    mmt_overnight_M = pd.DataFrame(mmt_overnight.iloc[-20:].sum(),columns = ['mmt_overnight_M'])
    mmt_overnight_M['date'] = todaydate
    mmt_overnight_M = mmt_overnight_M.set_index('date',append=True).swaplevel()
    return mmt_overnight_M

def mmt_route_M(tempClose):
    # 路径调整动量
    mmt_route_M = (tempClose/tempClose.shift(20) - 1)/abs(tempClose/tempClose.shift(1)-1).rolling(20).sum()
    mmt_route_M = pd.DataFrame(mmt_route_M.iloc[-1:].stack(),columns = ['mmt_route_M'])
    return mmt_route_M

def mmt_discrete_M(tempClose):
    # 信息离散度动量
    daily_up = (tempClose/tempClose.shift(1)-1).applymap(lambda x: int(x>0) if not np.isnan(x) else np.nan)
    daily_down = (tempClose/tempClose.shift(1)-1).applymap(lambda x: int(x<0) if not np.isnan(x) else np.nan)
    mmt_discrete_M = daily_up.rolling(20).sum()/20-daily_down.rolling(20).sum()/20
    mmt_discrete_M = pd.DataFrame(mmt_discrete_M.iloc[-1:].stack(),columns = ['mmt_discrete_M'])
    return mmt_discrete_M

def mmt_sec_rank_M(tempClose): 
    # 截面rank动量
    mmt_sec_rank_M = (tempClose/tempClose.shift(1)-1).rank(axis = 1).rolling(20).mean()
    mmt_sec_rank_M = pd.DataFrame(mmt_sec_rank_M.iloc[-1:].stack(),columns = ['mmt_sec_rank_M'])
    return mmt_sec_rank_M

def mmt_time_rank_M(anaual_close):
    # 时序rank_score
    # anaual_close = Close.iloc[-272:]
    mmt_time_rank_M = (anaual_close/anaual_close.shift(1)-1).rolling(252).rank().rolling(20).mean()
    mmt_time_rank_M  = pd.DataFrame(mmt_time_rank_M.iloc[-1:].stack(),columns = ['mmt_time_rank_M'])
    return mmt_time_rank_M

def mmt_highest_days_A(anaual_High):
# 最高价距今天数
    todaydate = anaual_High.index[-1]
    mmt_highest_days_A = 252- anaual_High.iloc[-252:].apply(lambda x: x.argmax())
    mmt_highest_days_A = pd.DataFrame(mmt_highest_days_A,columns= ['mmt_highest_days_A'])
    mmt_highest_days_A['date'] = todaydate
    mmt_highest_days_A = mmt_highest_days_A.set_index('date',append=True).swaplevel()
    return mmt_highest_days_A

def volumestable(volume):
    # 成交量稳定度
    vol_m = volume.rolling(20).mean()
    vol_std = volume.rolling(20).std()
    volumestable = (vol_m/vol_std)
    volumestable = pd.DataFrame(volumestable.iloc[-1:].stack(),columns = ['volumestable'])
    return volumestable

def re_con(tempClose):
    # 收益一致性因子
    import numpy as np
    d5_r = tempClose.pct_change(5).iloc[-1:]/5
    d10_r = tempClose.pct_change(10).iloc[-1:]/10/np.sqrt(2)
    d15_r = tempClose.pct_change(15).iloc[-1:]/15/np.sqrt(3)
    con = pd.concat([d5_r.stack(),d10_r.stack(),d15_r.stack()],axis = 1).dropna()
    con = con.mean(axis =1)/con.std(axis = 1)
    con = con.unstack()

    con_output = con.rank(axis = 1) 
    con_output = con_output.apply(lambda x: x-x.mean(),axis = 1).abs()
    _con = pd.DataFrame(con_output.iloc[-1:].stack(),columns = ['_con'])
    return _con

def bofu_money(tempHigh,tempLow,tempOpen,total_turnover):
    # 波幅/成交额
    bofu_money = (tempHigh-tempLow)/tempOpen/total_turnover
    bofu_money = pd.DataFrame(bofu_money.iloc[-1:].stack(),columns = ['bofu_money'])
    return bofu_money

def mts(sta_del_extrm,minbar,todaydate):
    mts = sta_del_extrm[['single_trade_amt']]
    mts['total_turnover'] = minbar['total_turnover']
    mts = mts.groupby(level = 0).corr()[::2]['total_turnover'].droplevel(1)
    mts=  pd.DataFrame(mts)
    mts.columns = ['mts']
    mts['date'] = todaydate
    mts = mts.set_index('date',append=True).swaplevel()
    return mts

def mte(sta_del_extrm,minbar,todaydate):
    mte = sta_del_extrm[['single_trade_amt']]
    mte['close'] = minbar['close']
    mte = mte.groupby(level = 0).corr()[::2]['close'].droplevel(1)
    mte=  pd.DataFrame(mte)
    mte.columns = ['mte']
    mte['date'] = todaydate
    mte = mte.set_index('date',append=True).swaplevel()
    return mte

def qua(sta_del_extrm,todaydate):
    qua = sta_del_extrm.groupby(level = 0).\
        apply(lambda x: (x['single_trade_amt'].quantile(0.1)-\
            x['single_trade_amt'].min())/(x['single_trade_amt'].max()-x['single_trade_amt'].min()))
    qua = pd.DataFrame(qua,columns = ['qua'])
    qua['date'] = todaydate
    qua = qua.set_index('date',append=True).swaplevel()
    qua.index.name = ('date','symbol')
    return qua

def skew(sta_50pct,todaydate):# 偏度因子skew
    skew = sta_50pct.groupby(level = 0).\
        apply(lambda x: (((x['single_trade_amt']-x['single_trade_amt'].mean())/x['single_trade_amt'].std())**3).mean())
    skew = pd.DataFrame(skew,columns = ['skew'])
    skew['date'] = todaydate
    skew = skew.set_index('date',append=True).swaplevel()
    skew.index.name = ('date','symbol')
    return skew

def s_reverse(sing_trade_amt,minbar,todaydate):# 强反转因子
    minute_r = sing_trade_amt.copy()
    minute_r['minute_r'] = minbar['close']/minbar['open'] - 1
    minute_r = minute_r.set_index('trading_date',append = True)
    s_reverse = minute_r.groupby(level = 0).\
        apply(lambda x: x[x.single_trade_amt > x.single_trade_amt.quantile(0.8)].minute_r.sum())
    s_reverse = pd.DataFrame(s_reverse,columns = ['s_reverse'])
    s_reverse['date'] = todaydate
    s_reverse = s_reverse.set_index('date',append=True).swaplevel()
    s_reverse.index.name = ('date','symbol')
    return s_reverse

def daily_sta_90pct(sta_del_extrm):# 日单笔成交额90分位值
    daily_sta = sta_del_extrm.set_index('trading_date',append = True)
    daily_sta_90pct = daily_sta.droplevel(1).groupby(level = 0).apply(lambda x: x.groupby(level = 1).quantile(0.9)).swaplevel()
    daily_sta_90pct.columns = ['daily_sta_90pct']
    return daily_sta_90pct

# def ideal_reverse(daily_sta_cal,Close):
#     daily_sta_cal['day_return'] = Close.pct_change().stack()
#     by_stock = list(daily_sta_cal.groupby(level = 1))
#     def apply_rolling_cal(rollingdata):
#         def iv(x):
#             temp = x.sort_values('daily_sta_90pct')
#             return temp.iloc[:10].day_return.sum() - temp.iloc[10:].day_return.sum()
#         templist = []
#         if len(rollingdata.index)<20:
#             return
#         for i in range(19,len(rollingdata.index)):
#             append_x = rollingdata.iloc[i-19:i+1].copy()
#             append_x['ideal_reverse'] = iv(append_x)
#             templist.append(append_x['ideal_reverse'].iloc[-1:])
#         return pd.concat(templist)
#     ideal_reverse = list(map(lambda x:apply_rolling_cal(x[1]),by_stock))
#     ideal_reverse = pd.concat(ideal_reverse)
#     ideal_reverse = pd.DataFrame(ideal_reverse)
#     ideal_reverse.columns = ['ideal_reverse']
#     return ideal_reverse
def ideal_reverse(daily_sta_cal,Close):
    daily_sta_cal['day_return'] = Close.pct_change().stack()
    by_stock = list(daily_sta_cal.groupby(level = 1))
    def apply_rolling_cal(rollingdata):
        if len(rollingdata.index)<20:
            return
        else:
            temp = rollingdata.sort_values('daily_sta_90pct')
            returndf = rollingdata.iloc[-1:].copy()
            returndf['ideal_reverse'] = temp.iloc[:10].day_return.sum() - temp.iloc[10:].day_return.sum()
        return returndf['ideal_reverse']
    ideal_reverse = list(map(lambda x:apply_rolling_cal(x[1]),by_stock))
    ideal_reverse = pd.concat(ideal_reverse)
    ideal_reverse = pd.DataFrame(ideal_reverse)
    ideal_reverse.columns = ['ideal_reverse']
    return ideal_reverse