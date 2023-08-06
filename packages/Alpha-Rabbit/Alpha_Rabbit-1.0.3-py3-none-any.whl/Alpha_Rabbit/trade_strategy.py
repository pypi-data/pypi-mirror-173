def TopK_dropout(k,oldpos,newsignal,allsignal):
    oldpos = list(filter(lambda x: x.volume>0,oldpos))
    if len(oldpos)==0:
        return [],newsignal
    symbollist = [p.symbol for p in oldpos]
    inold_notinnew = list(set(symbollist) - set(newsignal['codes'].to_list()))
    if 0<len(inold_notinnew)<=k:
        clean_pos = list(filter(lambda x: x.symbol in inold_notinnew,oldpos))
        buy_item = newsignal.sort_values('weighted_factor_rank').iloc[-len(inold_notinnew):]
        return clean_pos,buy_item
    if len(inold_notinnew)>k:
        clean_stocks = [ c[5:]+'.XSHG' if c[:5]=='SHSE.' else c[5:]+'.XSHE' for c in inold_notinnew] # 非标代码转换
        intersec = list(filter(lambda x: x in allsignal.index,clean_stocks))
        unsec = list(filter(lambda x: x not in allsignal.index,clean_stocks))
        print("异常持仓股票注意：",unsec)
        clean_stocks = allsignal.loc[intersec].sort_values('weighted_factor_rank').iloc[:k] # 寻找最拉的股票
        clean_stocks = ['SHSE.'+c[:6] if c[-4:] == 'XSHG' else 'SZSE.'+c[:6] for c in clean_stocks.index] #找完再变回来
        clean_pos = list(filter(lambda x: x.symbol in clean_stocks,oldpos))
        buy_item = newsignal.sort_values('weighted_factor_rank').iloc[-k:]
        return clean_pos,buy_item
    if len(inold_notinnew)==0:
        return [],None