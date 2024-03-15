def fix_weightdelts(patient,pchange):
    
    pchange = pchange
    pchange["Start Date"] = pd.to_datetime(pchange["Start Date"])
    pchange=pchange[['Patient', 'Subject Disposition','Interval Value','Start Date', 'ScreeningWgt',
           'VisitWgt', 'PercentChange', 'DoseAdjusted']]
    pchange = pchange.sort_values(by=["Patient", "Start Date"], ascending = [True,True])
    
    pchange = pchange[pchange["Patient"]==patient].reset_index(drop=True)
    mask = abs((pchange['VisitWgt'] - pchange['ScreeningWgt']) / pchange['ScreeningWgt']) * 100 >= 5
    indexlst = np.where(mask,pchange.index,np.nan)
    points = pd.Series(indexlst).dropna().reset_index(drop=True)
    i = 0
    while i < len(points) and len(points)!= 0:

        point = points[i]
        pchange.loc[point+1:,"ScreeningWgt"] = pchange.loc[point,"VisitWgt"]
        mask = abs((pchange['VisitWgt'] - pchange['ScreeningWgt']) / pchange['ScreeningWgt']) * 100 >= 5
        indexlst = np.where(mask,pchange.index,np.nan)
        points = pd.Series(indexlst).dropna().reset_index(drop=True)
        i+=1

    
    return pchange
