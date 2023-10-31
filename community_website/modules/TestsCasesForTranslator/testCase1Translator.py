import pandas as pd
import translators as ts
import unittest as test

class testTranslator(test.TestCase):
    def testTranslation_toTurkish(self):
        df = pd.read_excel("testCase1.xlsx")
        dfTrue=pd.read_excel("testCase1_translated.xlsx")
        
        for i in range(0,df.columns.size):
            for k in range(0,df.iloc[:,i].size):
                word=df.iloc[i,k]
                transWord=ts.translate_text(query_text=word, to_language="en")
                self.assertEqual(transWord,dfTrue.iloc[i,k])

        column_name=df.columns
        trueColumns=dfTrue.columns
        
        for i in range(0,df.iloc[0].size):
            if(type(column_name[i])==str):
                newName=ts.translate_text(query_text=column_name[i], to_language="en")
                self.assertEqual(newName,trueColumns[i])