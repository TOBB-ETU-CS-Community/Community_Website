import pandas as pd
import translators as ts
import datetime

   #to detect language use 'auto' for from_langCode
def excelTranslator(excel_sheet: str, to_langCode : str, from_langCode : str, export=False, sheetName="Sheet1"): 
    df = pd.read_excel(excel_sheet)
    if(df.empty):
        print("excel file is empty")
        return
    
    for k in range(0,df.columns.size):
        for i in range(0,df.iloc[:,k].size):
            if(not pd.isnull(df.iloc[i,k])):
                word=df.iloc[i,k]

                if(type(word)==type('str')):
                    df.iloc[i,k]=ts.translate_text(query_text=word, to_language=to_langCode)

    column_name=df.columns
      
    for i in range(0,df.iloc[0].size):
        if(type(column_name[i])==str):
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
#print(excelTranslator(excel_sheet="excel sheet.xlsx",to_langCode="tr",from_langCode="auto"))

#translates and exports
#excelTranslator(excel_sheet="excel sheet.xlsx",to_langCode="tr",from_langCode="auto",export=True,sheetName="MySheet")

