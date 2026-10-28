"""Self-contained unit tests for grouping and aggregate calculations."""
import sys
from pathlib import Path
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analyse import prepare, analyse, code_group

class AnalysisTests(unittest.TestCase):
    def test_repayment_codes_not_mislabelled(self):
        self.assertEqual(code_group(-2),'Code -2')
        self.assertEqual(code_group(0),'Code 0')
        self.assertEqual(code_group(2),'2+ months late')

    def fixture(self):
        fields=['LIMIT_BAL','SEX','EDUCATION','MARRIAGE','AGE',
                'PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6',
                *[f'BILL_AMT{i}' for i in range(1,7)],
                *[f'PAY_AMT{i}' for i in range(1,7)]]
        rows=[]
        for i,(limit,code,default) in enumerate([(50000,0,1),(120000,2,1),(200000,-1,0),(30000,-2,0)]):
            row={col:1 for col in fields};row.update({'ID':i+1,'LIMIT_BAL':limit,'AGE':25+i,'PAY_0':code,'default.payment.next.month':default})
            rows.append(row)
        return pd.DataFrame(rows)

    def test_outcomes_and_segments(self):
        result=analyse(prepare(self.fixture()))
        self.assertEqual(result['portfolio']['clients'],4)
        self.assertEqual(result['portfolio']['defaults'],2)
        self.assertAlmostEqual(result['portfolio']['default_rate'],.5)
        self.assertEqual(sum(r['clients'] for r in result['segments']['limit_band']),4)
        self.assertEqual(sum(r['defaults'] for r in result['segments']['repayment_group']),2)

    def test_rejects_duplicate_identifier(self):
        df=self.fixture();df.loc[1,'ID']=1
        with self.assertRaises(ValueError): prepare(df)

    def test_rejects_invalid_target(self):
        df=self.fixture();df.loc[1,'default.payment.next.month']=2
        with self.assertRaises(ValueError): prepare(df)

if __name__=='__main__': unittest.main()
