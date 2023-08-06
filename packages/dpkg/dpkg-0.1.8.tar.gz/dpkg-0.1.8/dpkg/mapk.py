import pandas as pd

class MapkScore:
    def get_score(self, apk_list):
        mapk = sum(apk_list)/len(apk_list)
        return mapk

