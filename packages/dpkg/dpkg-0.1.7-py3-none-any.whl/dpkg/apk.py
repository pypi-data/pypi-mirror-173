# -*- coding: utf-8 -*-
import pandas as pd

"""
    Computes the average precision at k.
    This function computes the average prescision at k between two lists of
    items.
    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The average precision at k over the input lists
"""

class ApkScore:
    def __init__(self, actual, predicted, k=None):
        self.actual = actual
        self.predicted = predicted
        if k is None:
            self.k = 5
        else:
            self.k = k

    def get_apk_score(self):

        if len(self.predicted)>self.k:
            self.predicted = self.predicted[:self.k]

        score = 0.0
        num_hits = 0.0

        for i,p in enumerate(self.predicted):
            if p in self.actual and p not in self.predicted[:i]:
                num_hits += 1.0
                score += num_hits / (i+1.0)

        if not self.actual:
            return 0.0

        return score / min(len(self.actual), self.k)

if __name__ == "__main__":
    actual = ['a', 'b', 'c']
    predicted = ['a', 'b', 'd']
    k = 5
    score = ApkScore(actual, predicted, k).get_apk_score()
    print(score)

# class Mapk:
#     def __init__(self, file_name, target_obj, output, k=5):
#         super().__init__()
#         self.file_name = file_name
#         self.dataset = pd.read_excel(self.file_name, sheet_name='metabolite')
#         self.bodyfat_items = ['가르시니아캄보지아추출물', '공액리놀레산', '녹차추출물', '콜레우스포스콜리 추출물', '키토산/키토올리고당']
#         self.bloodsugar_items = ['바나바잎추출물', '귀리식이섬유', '난소화성말토덱스트린', '이눌린/치커리추출물']
#         self.bloodpressure_items = ['코엔자임Q10']
#         self.cholesterol_items = ['홍국', '감마리놀렌산 함유 유지', '귀리식이섬유', '녹차추출물', '레시틴', '마늘', '스피루리나', '이눌린/치커리추출물', '차전차피식이섬유', '클로렐라', '키토산/키토올리고당']
#         self.triglyceride_items = ['EPA 및 DHA 함유유지', '난소화성말토덱스트린']
#         self.target_obj = target_obj
#         self.output_file = output
#         self.k = k

#     def get_mapk_score(self):
#         rc_dict = self.dataset.groupby('userID')['name'].apply(list).to_dict()

#         apk_list = []
#         apk_rts = []

#         for k, v in rc_dict.items():
#             if self.target_obj == 'bf':
#                 apk_value = Apk(self.bodyfat_items, v, k=self.k).get_apk_score()
#                 apk_list.append(apk_value)
#                 apk_rts.append({'userID':k, 'apk':apk_value})
#             elif self.target_obj == 'bs':
#                 apk_value = Apk(self.bloodsugar_items, v, k=self.k).get_apk_score()
#                 apk_list.append(apk_value)
#                 apk_rts.append({'userID':k, 'apk':apk_value})
#             elif self.target_obj == 'bp':
#                 apk_value = Apk(self.bloodpressure_items, v, k=self.k).get_apk_score()
#                 apk_list.append(apk_value)
#                 apk_rts.append({'userID':k, 'apk':apk_value})
#             elif self.target_obj == 'chl':
#                 apk_value = Apk(self.cholesterol_items, v, k=self.k).get_apk_score()
#                 apk_list.append(apk_value)
#                 apk_rts.append({'userID':k, 'apk':apk_value})
#             elif self.target_obj == 'trig':
#                 apk_value = Apk(self.triglyceride_items, v, k=self.k).get_apk_score()
#                 apk_list.append(apk_value)
#                 apk_rts.append({'userID':k, 'apk':apk_value})
#             else:
#                 raise Exception('target object type error')
        
#         apk_result = pd.DataFrame.from_dict(apk_rts)
#         mapk = sum(apk_list)/len(apk_list)
#         mapk_value = [{'target': self.target_obj, 'mapk': mapk}]
#         mapk_result = pd.DataFrame.from_dict(mapk_value)

#         writer = pd.ExcelWriter(f'output/mapk/{self.output_file}', engine='xlsxwriter')
#         apk_result.to_excel(writer, sheet_name='apk')
#         mapk_result.to_excel(writer, sheet_name='mapk')
#         writer.save()


#         print(f'mapk : {mapk}')
#         print('apk result:\n', apk_result)

# def main(file_name, target_obj, output, k):
#     Mapk(file_name, target_obj, output, k).get_mapk_score()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='measurement of mapk', epilog='written by smlee')
#     parser.add_argument('--input', '-i', required=True, help='xlsx format, file sheetname : metabolite')
#     parser.add_argument('--type', '-t', required=True, help='''
#                                             target object
#                                              * bf: bodyFat
#                                              * bs: bloodSugar
#                                              * bp: bloodPressure
#                                              * chl: cholesterol
#                                              * trig: triglyceride
#                                              '''
#                                              )
#     parser.add_argument('--kvalue', '-k', required=True, help='mapk k value, default k = 5')
#     parser.add_argument('--output', '-o', required=True, help='output file name')

#     args = parser.parse_args()

#     input_file = args.input
#     target_obj = args.type
#     k_value = args.kvalue
#     output_file = args.output

#     main(input_file, target_obj, output_file, int(k_value))