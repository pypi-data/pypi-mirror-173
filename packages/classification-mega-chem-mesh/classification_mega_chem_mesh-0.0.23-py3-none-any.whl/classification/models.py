import json
from enum import Enum
from typing import List


# 基础大类的名称
class Category0(str, Enum):
    Halide = "Halide"
    Amine = "Amine"
    Alcohol = "Alcohol"
    Boronic_Acid = "Boronic Acid"
    Carboxylic_Acid = "Carboxylic Acid"
    Acid_Chloride = "Acid Chloride"
    Sulfonyl_Chloride = "Sulfonyl Chloride"
    Aldehyde = "Aldehyde"
    Ketone = "Ketone"
    Default = "-"
    Error = "Category Error"
    # Alkyne = "Alkyne"
    # Olefin = "Olefin"
    # Epoxides = "Epoxides"
    # Hydrazines = "Hydrazines"
    # Isocyanates = "Isocyanates"
    # Isothiocyanates = "Isothiocyanates"
    # Nitriles = "Nitriles"
    # Ester = "Ester"
    Others = "Others"


# 基础大类含有的官能团，可根据验证结果修改SMARTS
class Category0FunctionalGroup(str, Enum):
    Halide = "[F,Cl,Br,I]"
    Halide_I = "[I]"
    Halide_Br = "[Br]"
    Halide_Cl = "[Cl]"
    Halide_F = "[F]"
    Amine = "[NH2,NH,N,nH]"
    Primary_or_Benzyl_Amine = '[NH2]'
    Secondary_Amine = '[NH]'
    Secondary_Amine_R = '[nH]'
    Tertiary_Amine = '[N]'
    Alcohol = "[OH]"
    Boronic_Acid = "B(O)O"
    Carboxylic_Acid = "C(=O)O"
    Acid_Chloride = "C(=O)Cl"
    Sulfonyl_Chloride = "S(=O)(Cl)=O"
    Aldehyde = "[CH]=O"
    Ketone = "[CX3;$(C([#6])(=[O])[#6])]"
    # Alkyne = "C#C"
    # Olefin = "C=C"
    # Epoxides = "C1CO1"
    # Hydrazines = "NN"
    # Isocyanates = "N=C=O"
    # Isothiocyanates = "N=C=S"
    # Nitriles = "C#N"
    # Ester1 = "COC=O"
    # Ester2 = "CCOC=O"
    # Ester3 = "cOC=O"
    # Ester4 = "cCOC=O"
    # Ester5 = "CcOC=O"
    # Ester6 = "ccOC=O"


# Category4的特定子结构的SMARTS
class Category4Smarts(str, Enum):
    # 5元杂环
    Pyrrole_3H = "N1=CCC=C1"
    Pyrrole_2H = "N1CC=CC=1"
    Pyrrole_2H_Enol = "N1CC=cc=1"
    Pyrazole_3H = "N1=NCC=C1"
    Imidazole_4H = "N1C=NCC=1"
    Triazole_124_3H = "N1=NCN=C1"
    Triazole_123_4H = "N1N=NCC=1"
    Tetrazole_5H = "N1=NN=NC1"

    Furan = "o1cccc1"  # 呋喃
    Oxazole = "o1cncc1"  # 恶唑
    Isoxazole = "o1nccc1"  # 异恶唑
    Oxadiazole_123 = "o1nncc1"
    Oxadiazole_124 = "o1ncnc1"
    Oxatriazole_1235 = "o1nncn1"
    Oxatriazole_1234 = "o1nnnc1"
    Tetranitrogen_monooxide = "o1nnnn1"

    Thiophene = "s1cccc1"  # 噻吩
    Thiazole = "s1cncc1"  # 噻唑
    Isothiazole = "s1nccc1"
    Thiadiazole_123 = "s1nncc1"
    Thiadiazole_124 = "s1ncnc1"
    Thiadiazole_134 = "s1cnnc1"
    Thiatriazole_1235 = "s1nncn1"
    Thiatriazole_1234 = "s1nnnc1"
    Tetranitrogen_monosulfide = "s1nnnn1"

    Pyrrole = "[nH,n]1cccc1"  # 吡咯
    Imidazole_nH = "[nH]1cncc1"  # 13唑 Imidazole  1,3-Diazole
    Imidazole_n = "[n]1cncc1"  # 13唑 Imidazole  1,3-Diazole
    Pyrazole = "[nH,nX3]1nccc1"  # 12唑 Pyrazole  1,2-Diazole
    Triazole_123 = "[nH,n]1nncc1"  # 123三唑
    Triazole_124 = "[nH,n]1ncnc1"  # 124三唑
    Tetrazole_1235 = "[nH,n]1nncn1"
    Tetrazole_1234 = "[nH,n]1nnnc1"
    Pentazole_1H = "[nH,n]1nnnn1"

    # 6元杂环
    Pyridine = "n1ccccc1"  # 吡啶
    Pyridazine = "n1ncccc1"  # 哒嗪
    Pyrimidine = "n1cnccc1"  # 嘧啶
    Pyrazine = "n1ccncc1"  # 吡嗪
    Triazine_123 = "n1nnccc1"
    Triazine_124 = "n1ncncc1"
    Triazine_135 = "n1cncnc1"
    Tetrazine_1234 = "n1nnncc1"
    Tetrazine_1245 = "n1ncnnc1"
    Tetrazine_1235 = "n1cnnnc1"
    Pentazine = "n1nnnnc1"
    Hexazine = "n1nnnnn1"


class Category1(str, Enum):
    Aromatic = "Aromatic"
    Aliphatic = "Aliphatic"
    Free_Hydrogen = "Free Hydrogen"
    Enol = "Enol"  # 烯醇
    Default = "-"
    Error = "Category1 Error"


class Category2(str, Enum):
    Default = "-"
    Error = "Category2 Error"


class Category2Aromatic(str, Enum):
    Benzene = "Benzene"
    Heterocyclic = "Heterocyclic"
    Fused_Ring = "Fused Ring"
    Quinone = "Quinone"
    Default = "-"
    Error = "Category2 Error"


class Category2Aliphatic(str, Enum):
    Primary = "Primary"
    Secondary = "Secondary"
    Tertiary = "Tertiary"
    Benzyl = "Benzyl"
    Default = "-"
    Error = "Category2 Error"


class Category3(str, Enum):
    FiveMembered = "Five Membered"
    SixMembered = "Six Membered"
    Default = "-"
    Error = "Category3 Error"


class Category4(str, Enum):
    Default = "-"
    Error = "Category4 Error"


class Category4FiveMembered(str, Enum):
    # 5元杂环 # 30
    Pyrrole_3H = "3H-Pyrrole"
    Pyrrole_2H = "2H-Pyrrole"
    Pyrazole_3H = "3H-Pyrazole"
    Imidazole_4H = "4H-Imidazole"
    Triazole_124_3H = "3H-1,2,4-Triazole"
    Triazole_123_4H = "4H-1,2,3-Triazole"
    Tetrazole_5H = "5H-Tetrazole"

    Furan = "Furan"  # 呋喃
    Oxazole = "Oxazole"  # 恶唑
    Isoxazole = "Isoxazole"  # 异恶唑
    Oxadiazole_123 = "1,2,3-Oxadiazole"
    Oxadiazole_124 = "1,2,4-Oxadiazole"
    Oxatriazole_1235 = "1,2,3,5-Oxatriazole"
    Oxatriazole_1234 = "1,2,3,4-Oxatriazole"
    Tetranitrogen_monooxide = "Tetranitrogen(III) monooxide"

    Thiophene = "Thiophene"  # 噻吩
    Thiazole = "Thiazole"  # 噻唑
    Isothiazole = "Isothiazole"
    Thiadiazole_123 = "1,2,3-Thiadiazole"
    Thiadiazole_124 = "1,2,4-Thiadiazole"
    Thiadiazole_134 = "1,3,4-Thiadiazole"
    Thiatriazole_1235 = "1,2,3,5-Thiatriazole"
    Thiatriazole_1234 = "1,2,3,4-Thiatriazole"
    Tetranitrogen_monosulfide = "Tetranitrogen(III) monosulfide"

    Pyrrole = "Pyrrole"  # 吡咯
    Imidazole = "Imidazole"  # 13唑 Imidazole  1,3-Diazole
    Pyrazole = "Pyrazole"  # 12唑 Pyrazole  1,2-Diazole
    Triazole_123 = "1,2,3-Triazole"  # 123三唑
    Triazole_124 = "1,2,4-Triazole"  # 124三唑
    Tetrazole = "Tetrazole"
    Pentazole_1H = "1H-Pentazole"
    Default = "-"


class Category4SixMembered(str, Enum):
    # 6元杂环 # 12
    Pyridine = "Pyridine"  # 吡啶
    Pyridazine = "Pyridazine"  # 哒嗪
    Pyrimidine = "Pyrimidine"  # 嘧啶
    Pyrazine = "Pyrazine"  # 吡嗪
    Triazine_123 = "1,2,3-Triazine"
    Triazine_124 = "1,2,4-Triazine"
    Triazine_135 = "1,3,5-Triazine"
    Tetrazine_1234 = "1,2,3,4-Tetrazine"
    Tetrazine_1245 = "1,2,4,5-Tetrazine"
    Tetrazine_1235 = "1,2,3,5-Tetrazine"
    Pentazine = "Pentazine"
    Hexazine = "Hexazine"


class Category5(int, Enum):
    Pos_1 = 1
    Pos_2 = 2
    Pos_3 = 3
    Pos_4 = 4
    Pos_5 = 5
    Pos_6 = 6


class Hydrolysis(str, Enum):
    Yes = "Y"
    No = "N"
    Default = "-"


class Steric_Hindrance(str, Enum):
    Yes = "Y"
    No = "N"
    Default = "-"


class CategoryResult:
    def __init__(self, category0: Category0, category1: Category1,
                 category2: Category2, category3: Category3,
                 category4: Category4, category5: str,
                 hydrolysis: Hydrolysis, steric_hindrance: Steric_Hindrance):
        self.category0 = category0
        self.category1 = category1
        self.category2 = category2
        self.category3 = category3
        self.category4 = category4
        self.category5 = category5
        self.hydrolysis = hydrolysis
        self.steric_hindrance = steric_hindrance

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
