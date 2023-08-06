import pandas as pd

class MapkScore:
    def get_score(self, *args):
        mapk = sum(args)/len(args)
        return mapk

