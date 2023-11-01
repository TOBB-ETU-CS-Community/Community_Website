import pandas as pd
import translators as ts
import unittest as test

class testTranslator(test.TestCase):
    def testTranslation_onDates(self):
        df = pd.read_excel("testCase2.xlsx")
        dfTrue=pd.read_excel("testCase2_translated.xlsx")
        
        for i in range(0,df.columns.size):
            for k in range(0,df.iloc[:,i].size):
                word=df.iloc[i,k]
                if(type(word)==type('str')):
                    transWord=ts.translate_text(query_text=word, to_language="en")
                    self.assertEqual(transWord,dfTrue.iloc[i,k])

        column_name=df.columns
        trueColumns=dfTrue.columns
        
        for i in range(0,df.iloc[0].size):
            if(type(column_name[i])==str):
                newName=ts.translate_text(query_text=column_name[i], to_language="en")
                self.assertEqual(newName,trueColumns[i])


def excelTranslator(excel_sheet: str, to_langCode : str, from_langCode : str, export=False, sheetName="Sheet1"): 
    df = pd.read_excel(excel_sheet)
    if(df.empty):
        print("excel file is empty")
        return

    # Change the alignment of the date column to day, month, and year

    #if a column is full of dates then pd reads it as pd object but if it has objects different than date pd reads it as datetime

    for k in range(0,df.columns.size):
        for i in range(0,df.iloc[:,k].size):
            word=df.iloc[i,k]
            if(type(word)==type('str')):
                df.iloc[i,k]=ts.translate_text(query_text=word, to_language=to_langCode)

    column_name=df.columns
      
    for i in range(0,df.iloc[0].size):
        newName=ts.translate_text(query_text=column_name[i], to_language=to_langCode,from_language=from_langCode)
        column_name_map={column_name[i]:newName}
        df.rename(columns=column_name_map,inplace=True)
    
    if(not export):
        return df
    else:
        index=str(excel_sheet).find(".xlsx")
        excelName=excel_sheet[:index]
        df.to_excel(excelName+"_translated.xlsx", sheet_name=sheetName, index=False)


#just translates and returns
#print(excelTranslator(excel_sheet="testCase2.xlsx",to_langCode="en",from_langCode="auto"))

#translates and exports
#excelTranslator(excel_sheet="testCase2.xlsx",to_langCode="en",from_langCode="auto",export=True,sheetName="MySheet")