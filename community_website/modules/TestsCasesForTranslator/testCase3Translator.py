import pandas as pd
import translators as ts
import unittest as test

class nullController(test.TestCase):
    def testTranslation_onDates(self):
        df = pd.read_excel("testCase3.xlsx")
        dfTrue=pd.read_excel("testCase3_translated.xlsx")
        
        for i in range(0,df.columns.size):
            for k in range(0,df.iloc[:,i].size):
                if(not pd.isnull(df.iloc[i,k])):
                    word=df.iloc[i,k]
                    if(type(word)==type('str')):
                        transWord=ts.translate_text(query_text=word, to_language="tr")
                        self.assertEqual(transWord,dfTrue.iloc[i,k])

        column_name=df.columns
        trueColumns=dfTrue.columns
        
        for i in range(0,df.iloc[0].size):
            if(type(column_name[i])==str):
                newName=ts.translate_text(query_text=column_name[i], to_language="tr")
                self.assertEqual(newName,trueColumns[i])