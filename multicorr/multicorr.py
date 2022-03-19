# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:22:35 2022

@author: sarathbabu.karunanit
"""

import pandas as pd
class multi_corr:
    def __init__(self,df,threshold=0.5):
        if len(df)>0:
            self.df=df
        self.threshold=threshold
    def __corr_stack(self):
        self.__df_corr=self.df.corr()
        self.__df_corr=self.__df_corr.stack().reset_index()
        self.__df_corr.columns=['x','y','corr']
        self.__df_corr['abs_corr']=abs(self.__df_corr['corr'])
        self.__df_corr=self.__df_corr.loc[(self.__df_corr['abs_corr']>=self.threshold)&(self.__df_corr['x']!=self.__df_corr['y'])]
        self.__df_corr=self.__df_corr.sort_values(by=['abs_corr'],ascending=False)
        
    def calc(self):
        self.__corr_stack()
        cols=sorted(self.df.columns.values)

        self.__final=pd.DataFrame()
        for i in range(len(cols)):
            corr_cols=[]
            corr_cols.append(cols[i])

            j=self.__df_corr.loc[self.__df_corr.x==cols[i]].y.values
            if len(j)>0:
                j=sorted(j)[0]
                corr_cols.append(j)

            rem_cols=sorted(list(set(cols)-set(corr_cols)))

            for j in rem_cols:
                counts=0
                for k in corr_cols:
                    counts=counts+(self.__df_corr.loc[(self.__df_corr.x==k)&(self.__df_corr.y==j)].shape[0])
                if counts==len(corr_cols):
                    corr_cols.append(j)
            self.__final=pd.concat([self.__final,pd.DataFrame(corr_cols)],axis=1)
            self.__final.columns=self.__final.iloc[0].values
            
        del self.__df_corr['abs_corr']
        self.__df_corr=self.__df_corr.sort_values(by=['x'])
        self.__df_corr=self.__df_corr.reset_index(drop=True)
        
        self.__final=self.__final.iloc[1:]
        
        
        return self.__df_corr,self.__final
    