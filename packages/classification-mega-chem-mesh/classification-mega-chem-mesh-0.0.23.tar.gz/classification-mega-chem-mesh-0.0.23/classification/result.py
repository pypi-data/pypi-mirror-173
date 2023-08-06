# -*- coding: utf-8 -*-
# @Time : 2021/11/24 17:15
# @Author : EdwardTsai
# @Email : caiweimin@megarobo.tech
# @File : result.py
# @Project : chem-mesh-notebook
# @Introduction : For PyPI. You can get classification result directly through the method.
from classification.rules import classify


def custom_classification(smiles, category0):
    result = classify(smiles, category0)
    return result.toJson()
