import warnings
from rdkit import Chem
from classification.models import Category0FunctionalGroup as C0FG
from classification.models import Category0, Category1, Category2, Category2Aromatic, \
    Category2Aliphatic, Category3, Category4, Category5, CategoryResult, Category4Smarts, Category4FiveMembered, \
    Category4SixMembered, Hydrolysis, Steric_Hindrance
from classification.utils import identify_functional_group as ifg
from classification.utils import functional_group_from_category0 as fgfc0
from classification.utils import convert_category_0, match_alpha_c_ali_aro, is_free_H, is_fused_ring, is_ring_x_atom, \
    alpha_c_index_by_category, count_H, count_ring_atom, locate_alpha_c_index_on_heterocyclic, \
    mapping_from_position_list, is_hydrolysis, neighbor_c_idx_of_alpha_c, is_ring_aromatic, unique_alpha_c_idx_in_ring, \
    is_idx_in_ring_and_aromatic, functional_group_from_category0, count_H_on_alpha_c, alpha_c_bonds_type, \
    is_ring_custom_ar, is_alpha_ring_heterocyclic, is_idx_in_double_ring
from typing import List


# 根据输入的SMILES判断其官能团，可能有一个或多个
def get_category_0(smile: str) -> List[str]:
    category_0_list = []
    # verify Halide
    if ifg(smile, C0FG.Halide.value)[1]:
        category_0_list.append(Category0.Halide.value)
    # verify Amine
    if ifg(smile, C0FG.Amine.value)[1]:
        category_0_list.append(Category0.Amine.value)
    # verify Alcohol
    if ifg(smile, C0FG.Alcohol.value)[1]:
        category_0_list.append(Category0.Alcohol.value)
    # verify Boronic Acid
    if ifg(smile, C0FG.Boronic_Acid.value)[1]:
        category_0_list.append(Category0.Boronic_Acid.value)
    # verify Carboxylic Acid
    if ifg(smile, C0FG.Carboxylic_Acid.value)[1]:
        category_0_list.append(Category0.Carboxylic_Acid.value)
    # verify Acid Chloride
    if ifg(smile, C0FG.Acid_Chloride.value)[1]:
        category_0_list.append(Category0.Acid_Chloride.value)
    # verify Sulfonyl Chloride
    if ifg(smile, C0FG.Sulfonyl_Chloride.value)[1]:
        category_0_list.append(Category0.Sulfonyl_Chloride.value)
    # verify Aldehyde
    if ifg(smile, C0FG.Aldehyde.value)[1]:
        category_0_list.append(Category0.Aldehyde.value)
    # verify Ketone
    if ifg(smile, C0FG.Ketone.value)[1]:
        category_0_list.append(Category0.Ketone.value)
    # # verify Alkyne
    # if ifg(smile, C0FG.Alkyne.value)[1]:
    #     category_0_list.append(Category0.Alkyne.value)
    # # verify Olefin
    # if ifg(smile, C0FG.Olefin.value)[1]:
    #     category_0_list.append(Category0.Olefin.value)
    # # verify Epoxides
    # if ifg(smile, C0FG.Epoxides.value)[1]:
    #     category_0_list.append(Category0.Epoxides.value)
    # # verify Hydrazines
    # if ifg(smile, C0FG.Hydrazines.value)[1]:
    #     category_0_list.append(Category0.Hydrazines.value)
    # # verify Isocyanates
    # if ifg(smile, C0FG.Isocyanates.value)[1]:
    #     category_0_list.append(Category0.Isocyanates.value)
    # # verify Isothiocyanates
    # if ifg(smile, C0FG.Isothiocyanates.value)[1]:
    #     category_0_list.append(Category0.Isothiocyanates.value)
    # # verify Nitriles
    # if ifg(smile, C0FG.Nitriles.value)[1]:
    #     category_0_list.append(Category0.Nitriles.value)
    # # verify Ester
    # if ifg(smile, C0FG.Ester1.value)[1]:
    #     category_0_list.append(Category0.Ester.value)
    # # verify Ester
    # if ifg(smile, C0FG.Ester2.value)[1]:
    #     category_0_list.append(Category0.Ester.value)
    # # verify Ester
    # if ifg(smile, C0FG.Ester3.value)[1]:
    #     category_0_list.append(Category0.Ester.value)
    # # verify Ester
    # if ifg(smile, C0FG.Ester4.value)[1]:
    #     category_0_list.append(Category0.Ester.value)
    # # verify Ester
    # if ifg(smile, C0FG.Ester5.value)[1]:
    #     category_0_list.append(Category0.Ester.value)
    # # verify Ester
    # if ifg(smile, C0FG.Ester6.value)[1]:
    #     category_0_list.append(Category0.Ester.value)

    return category_0_list


def get_category_1(smile: str, category0: str) -> Category1:
    if is_free_H(smile, category0):
        return Category1.Free_Hydrogen
    else:
        if category0 == Category0.Halide.value:
            ali, aro = match_alpha_c_ali_aro(smile, fgfc0(smile, category0)[1])
            # if ifg(smile, 'C(F)')[1]:
            #     if len(aro) > 0:
            #         return Category1.Aromatic
            #     else:
            #         return Category1.Aliphatic
            # else:
            if len(ali) > 0:
                return Category1.Aliphatic
            else:
                return Category1.Aromatic
        elif category0 == Category0.Alcohol.value:
            if alpha_c_bonds_type(smile, category0):
                # 如果是烯醇，再判断一次自定义的芳香性，再给出芳香or烯醇的结论
                if is_ring_custom_ar(smile, category0):
                    return Category1.Aromatic
                else:
                    return Category1.Enol
            else:
                if len(match_alpha_c_ali_aro(smile, fgfc0(smile, category0)[1])[1]):
                    if is_ring_aromatic(smile, category0):
                        return Category1.Aromatic
                    else:
                        return Category1.Aliphatic
                else:
                    return Category1.Aliphatic
        else:
            if len(match_alpha_c_ali_aro(smile, fgfc0(smile, category0)[1])[1]):
                if is_ring_aromatic(smile, category0):
                    return Category1.Aromatic
                else:
                    return Category1.Aliphatic
            else:
                return Category1.Aliphatic


def get_category_exclude_freeH(smile: str, category0: str) -> Category1:
    if category0 == Category0.Halide.value:
        ali, aro = match_alpha_c_ali_aro(smile, fgfc0(smile, category0)[1])
        if len(ali) > 0:
            return Category1.Aliphatic
        else:
            return Category1.Aromatic
    elif category0 == Category0.Alcohol.value:
        if alpha_c_bonds_type(smile, category0):
            # 如果是烯醇，再判断一次自定义的芳香性，再给出芳香or烯醇的结论
            if is_ring_custom_ar(smile, category0):
                return Category1.Aromatic
            else:
                return Category1.Enol
        else:
            if len(match_alpha_c_ali_aro(smile, fgfc0(smile, category0)[1])[1]):
                if is_ring_aromatic(smile, category0):
                    return Category1.Aromatic
                else:
                    return Category1.Aliphatic
            else:
                return Category1.Aliphatic
    else:
        if len(match_alpha_c_ali_aro(smile, fgfc0(smile, category0)[1])[1]):
            if is_ring_aromatic(smile, category0):
                return Category1.Aromatic
            else:
                return Category1.Aliphatic
        else:
            return Category1.Aliphatic


def get_category_2(smile: str, category0: str):
    cate1_str = get_category_1(smile, category0).value
    # 父分类为芳香类
    if cate1_str == Category1.Aromatic.value:
        # 先判断并环
        if is_fused_ring(smile, category0):
            return Category2Aromatic.Fused_Ring
        else:
            # 芳香类问题排查，不能使用键判断，从alpha-c索引入手查是否包含在环索引元组中，然后根据个数判断5元6元，利用子结构判断是否苯环
            ring_len = is_ring_x_atom(smile, category0)
            if len(ring_len):
                if ring_len[0] == 6 and ifg(smile, 'O=C1C=C(O)C(=O)cc1')[1] or ifg(smile, 'O=C1C=CC(=O)C=C1')[1]:
                    return Category2Aromatic.Quinone
                elif ring_len[0] == 6 and not is_alpha_ring_heterocyclic(smile, category0):
                    return Category2Aromatic.Benzene
                elif ring_len[0] == 5 or ring_len[0] == 6 and is_alpha_ring_heterocyclic(smile, category0):
                    return Category2Aromatic.Heterocyclic
                else:
                    return Category2.Error
            else:
                return Category2.Error

    # 父分类为脂肪类
    elif cate1_str == Category1.Aliphatic.value:
        # 如果是胺类，则判断N原子的氢原子数
        if category0 == Category0.Amine.value:
            n_h_num = []
            res = fgfc0(smile, category0)
            for match in res[0]:
                h_num = count_H(smile, match[0])
                n_h_num.append(h_num)
            if 2 in n_h_num:
                if ifg(smile, '[R]C[NH2]')[1]:
                    if is_idx_in_ring_and_aromatic(smile, ifg(smile, '[R]C[NH2]')[0][0][0]):
                        return Category2Aliphatic.Benzyl
                    else:
                        return Category2Aliphatic.Primary
                else:
                    return Category2Aliphatic.Primary
            elif 3 in n_h_num:
                if ifg(smile, '[R]C[NH3+]')[1]:
                    if is_idx_in_ring_and_aromatic(smile, ifg(smile, '[R]C[NH3+]')[0][0][0]):
                        return Category2Aliphatic.Benzyl
                    else:
                        return Category2Aliphatic.Primary
                else:
                    return Category2Aliphatic.Primary
            elif 1 in n_h_num:
                return Category2Aliphatic.Secondary
            elif 0 in n_h_num:
                return Category2Aliphatic.Tertiary
            else:
                return Category2.Error

        # 醇类和醛类先判断beta位连接的是否为芳香环，其次再判断alpha-c上H的个数分
        elif category0 == Category0.Alcohol.value or category0 == Category0.Aldehyde.value:
            fg = functional_group_from_category0(smile, category0)[1]
            if ifg(smile, '[R]C'+fg)[1]:
                if is_idx_in_ring_and_aromatic(smile, ifg(smile, '[R]C'+fg)[0][0][0]):
                    return Category2Aliphatic.Benzyl
                else:
                    return count_H_on_alpha_c(smile, category0)
            else:
                return count_H_on_alpha_c(smile, category0)

        # 其他大类类根据alpha-c上H的个数分
        else:
            return count_H_on_alpha_c(smile, category0)
    # 父分类为活泼氢，不做处理
    else:
        return Category2.Default


# 上一级分类为杂环
def get_category_3(smile: str, category0: str) -> Category3:
    cate2_str = get_category_2(smile, category0).value
    if cate2_str == Category2Aromatic.Heterocyclic.value:
        alpha_c_idx_list = alpha_c_index_by_category(smile, category0)
        u_alpha_c = unique_alpha_c_idx_in_ring(alpha_c_idx_list, smile)
        ring_atom_num = []
        for u in u_alpha_c:
            num = count_ring_atom(smile, u)
            ring_atom_num.append(num)
        # 考虑了官能团连接一个或多个5或6元环，同时连接5且6元环的情况不在该范围中
        if sum(ring_atom_num) == 5 * len(ring_atom_num):
            return Category3.FiveMembered
        elif sum(ring_atom_num) == 6 * len(ring_atom_num):
            return Category3.SixMembered
        # 如果集合[5,6]，又因为杂环大于苯环，有5出现必定是杂环
        elif 5 in ring_atom_num:
            return Category3.FiveMembered
        else:
            return Category3.Error

    # 父分类不是杂环，不做处理
    else:
        return Category3.Default


# 上一分类为5元或6元杂环
def get_category_4(smile: str, category0: str):
    cate3_str = get_category_3(smile, category0).value
    if cate3_str == Category3.FiveMembered.value:
        if ifg(smile, Category4Smarts.Pyrrole_3H.value)[1]:
            return Category4FiveMembered.Pyrrole_3H
        elif ifg(smile, Category4Smarts.Pyrrole_2H.value)[1]:
            return Category4FiveMembered.Pyrrole_2H
        elif ifg(smile, Category4Smarts.Pyrrole_2H_Enol.value)[1]:
            return Category4FiveMembered.Pyrrole_2H
        elif ifg(smile, Category4Smarts.Pyrazole_3H.value)[1]:
            return Category4FiveMembered.Pyrazole_3H
        elif ifg(smile, Category4Smarts.Imidazole_4H.value)[1]:
            return Category4FiveMembered.Imidazole_4H
        elif ifg(smile, Category4Smarts.Triazole_124_3H.value)[1]:
            return Category4FiveMembered.Triazole_124_3H
        elif ifg(smile, Category4Smarts.Triazole_123_4H.value)[1]:
            return Category4FiveMembered.Triazole_123_4H
        elif ifg(smile, Category4Smarts.Tetrazole_5H.value)[1]:
            return Category4FiveMembered.Tetrazole_5H
        elif ifg(smile, Category4Smarts.Furan.value)[1]:
            return Category4FiveMembered.Furan
        elif ifg(smile, Category4Smarts.Oxazole.value)[1]:
            return Category4FiveMembered.Oxazole
        elif ifg(smile, Category4Smarts.Isoxazole.value)[1]:
            return Category4FiveMembered.Isoxazole
        elif ifg(smile, Category4Smarts.Oxadiazole_123.value)[1]:
            return Category4FiveMembered.Oxadiazole_123
        elif ifg(smile, Category4Smarts.Oxadiazole_124.value)[1]:
            return Category4FiveMembered.Oxadiazole_124
        elif ifg(smile, Category4Smarts.Oxatriazole_1235.value)[1]:
            return Category4FiveMembered.Oxatriazole_1235
        elif ifg(smile, Category4Smarts.Oxatriazole_1234.value)[1]:
            return Category4FiveMembered.Oxatriazole_1234
        elif ifg(smile, Category4Smarts.Tetranitrogen_monooxide.value)[1]:
            return Category4FiveMembered.Tetranitrogen_monooxide
        elif ifg(smile, Category4Smarts.Thiophene.value)[1]:
            return Category4FiveMembered.Thiophene
        elif ifg(smile, Category4Smarts.Thiazole.value)[1]:
            return Category4FiveMembered.Thiazole
        elif ifg(smile, Category4Smarts.Isothiazole.value)[1]:
            return Category4FiveMembered.Isothiazole
        elif ifg(smile, Category4Smarts.Thiadiazole_123.value)[1]:
            return Category4FiveMembered.Thiadiazole_123
        elif ifg(smile, Category4Smarts.Thiadiazole_124.value)[1]:
            return Category4FiveMembered.Thiadiazole_124
        elif ifg(smile, Category4Smarts.Thiadiazole_134.value)[1]:
            return Category4FiveMembered.Thiadiazole_134
        elif ifg(smile, Category4Smarts.Thiatriazole_1235.value)[1]:
            return Category4FiveMembered.Thiatriazole_1235
        elif ifg(smile, Category4Smarts.Thiatriazole_1234.value)[1]:
            return Category4FiveMembered.Thiatriazole_1234
        elif ifg(smile, Category4Smarts.Tetranitrogen_monosulfide.value)[1]:
            return Category4FiveMembered.Tetranitrogen_monosulfide
        elif ifg(smile, Category4Smarts.Pyrrole.value)[1]:
            return Category4FiveMembered.Pyrrole
        elif ifg(smile, Category4Smarts.Imidazole_nH.value)[1]:
            return Category4FiveMembered.Imidazole
        elif ifg(smile, Category4Smarts.Imidazole_n.value)[1]:
            return Category4FiveMembered.Imidazole
        elif ifg(smile, Category4Smarts.Pyrazole.value)[1]:
            return Category4FiveMembered.Pyrazole
        elif ifg(smile, Category4Smarts.Triazole_123.value)[1]:
            return Category4FiveMembered.Triazole_123
        elif ifg(smile, Category4Smarts.Triazole_124.value)[1]:
            return Category4FiveMembered.Triazole_124
        elif ifg(smile, Category4Smarts.Tetrazole_1235.value)[1]:
            return Category4FiveMembered.Tetrazole
        elif ifg(smile, Category4Smarts.Tetrazole_1234.value)[1]:
            return Category4FiveMembered.Tetrazole
        elif ifg(smile, Category4Smarts.Pentazole_1H.value)[1]:
            return Category4FiveMembered.Pentazole_1H
        else:
            return Category4.Error
    elif cate3_str == Category3.SixMembered.value:
        if ifg(smile, Category4Smarts.Pyridine.value)[1]:
            return Category4SixMembered.Pyridine
        elif ifg(smile, Category4Smarts.Pyridazine.value)[1]:
            return Category4SixMembered.Pyridazine
        elif ifg(smile, Category4Smarts.Pyrimidine.value)[1]:
            return Category4SixMembered.Pyrimidine
        elif ifg(smile, Category4Smarts.Pyrazine.value)[1]:
            return Category4SixMembered.Pyrazine
        elif ifg(smile, Category4Smarts.Triazine_123.value)[1]:
            return Category4SixMembered.Triazine_123
        elif ifg(smile, Category4Smarts.Triazine_124.value)[1]:
            return Category4SixMembered.Triazine_124
        elif ifg(smile, Category4Smarts.Triazine_135.value)[1]:
            return Category4SixMembered.Triazine_135
        elif ifg(smile, Category4Smarts.Tetrazine_1234.value)[1]:
            return Category4SixMembered.Tetrazine_1234
        elif ifg(smile, Category4Smarts.Tetrazine_1245.value)[1]:
            return Category4SixMembered.Tetrazine_1245
        elif ifg(smile, Category4Smarts.Tetrazine_1235.value)[1]:
            return Category4SixMembered.Tetrazine_1235
        elif ifg(smile, Category4Smarts.Pentazine.value)[1]:
            return Category4SixMembered.Pentazine
        elif ifg(smile, Category4Smarts.Hexazine.value)[1]:
            return Category4SixMembered.Hexazine
        else:
            return Category4.Error
    else:
        return Category4.Error


def get_category_5(smile: str, category0: str) -> List:
    cate4_str = get_category_4(smile, category0).value
    if cate4_str == Category4FiveMembered.Pyrrole_3H.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyrrole_3H.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Pyrrole_2H.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyrrole_2H.value)
        if len(pos):
            return mapping_from_position_list(pos)
        else:
            pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyrrole_2H_Enol.value)
            return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Pyrazole_3H.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyrazole_3H.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Imidazole_4H.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Imidazole_4H.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Triazole_124_3H.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Triazole_124_3H.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Triazole_123_4H.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Triazole_123_4H.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Tetrazole_5H.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Tetrazole_5H.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Furan.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Furan.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Oxazole.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Oxazole.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Isoxazole.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Isoxazole.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Oxadiazole_123.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Oxadiazole_123.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Oxadiazole_124.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Oxadiazole_124.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Oxatriazole_1235.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Oxatriazole_1235.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Oxatriazole_1234.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Oxatriazole_1234.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Tetranitrogen_monooxide.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Tetranitrogen_monooxide.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Thiophene.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Thiophene.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Thiazole.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Thiazole.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Isothiazole.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Isothiazole.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Thiadiazole_123.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Thiadiazole_123.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Thiadiazole_124.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Thiadiazole_124.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Thiadiazole_134.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Thiadiazole_134.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Thiatriazole_1235.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Thiatriazole_1235.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Thiatriazole_1234.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Thiatriazole_1234.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Tetranitrogen_monosulfide.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Tetranitrogen_monosulfide.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Pyrrole.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyrrole.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Imidazole.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Imidazole_nH.value)
        if len(pos):
            return mapping_from_position_list(pos)
        else:
            pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Imidazole_n.value)
            return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Pyrazole.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyrazole.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Triazole_123.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Triazole_123.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Triazole_124.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Triazole_124.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Tetrazole.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Tetrazole_1235.value)
        if len(pos):
            return mapping_from_position_list(pos)
        else:
            pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Tetrazole_1234.value)
            return mapping_from_position_list(pos)

    elif cate4_str == Category4FiveMembered.Pentazole_1H.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pentazole_1H.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Pyridine.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyridine.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Pyridazine.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyridazine.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Pyrimidine.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyrimidine.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Pyrazine.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pyrazine.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Triazine_123.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Triazine_123.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Triazine_124.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Triazine_124.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Triazine_135.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Triazine_135.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Tetrazine_1234.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Tetrazine_1234.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Tetrazine_1245.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Tetrazine_1245.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Tetrazine_1235.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Tetrazine_1235.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Pentazine.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Pentazine.value)
        return mapping_from_position_list(pos)

    elif cate4_str == Category4SixMembered.Hexazine.value:
        pos = locate_alpha_c_index_on_heterocyclic(smile, category0, Category4Smarts.Hexazine.value)
        return mapping_from_position_list(pos)

    else:
        return ["Category5 Error"]


def get_hydrolysis(smile, category0):
    if is_hydrolysis(smile, category0):
        return Hydrolysis.Yes
    else:
        return Hydrolysis.No


def get_steric_hindrance(smile, cate1, category0):
    mol = Chem.MolFromSmiles(smile)
    # 脂肪类，任意alpha-c上H个数小于2
    if cate1 == Category1.Aliphatic.value:
        alpha_c_idx = alpha_c_index_by_category(smile, category0)
        for ac in alpha_c_idx:
            if count_H(smile, ac) < 2:
                return Steric_Hindrance.Yes
        return Steric_Hindrance.No
    # 芳香类，苯环，仲胺也算有位阻
    # elif cate1 == Category1.Aromatic.value and cate2 == Category2Aromatic.Benzene.value and \
    #         ifg(smile, '[NH]c1ccccc1')[1]:
    #     return Steric_Hindrance.Yes
    # 芳香类，alpha-c邻位的c上H的个数为0
    elif cate1 == Category1.Aromatic.value:
        neighbor = neighbor_c_idx_of_alpha_c(smile, category0)[1]
        for n in neighbor:
            if not count_H(smile, n) and mol.GetAtomWithIdx(n).GetAtomicNum() == 6 \
                    and is_idx_in_double_ring(smile, n) != 2:
                return Steric_Hindrance.Yes
        return Steric_Hindrance.No
    # 活泼氢类，还要重新计算cate1，再按照脂肪和芳香计算
    elif cate1 == Category1.Free_Hydrogen.value:
        cate1_exh = get_category_exclude_freeH(smile, category0)
        if cate1_exh == Category1.Aliphatic.value:
            alpha_c_idx = alpha_c_index_by_category(smile, category0)
            for ac in alpha_c_idx:
                if count_H(smile, ac) < 2:
                    return Steric_Hindrance.Yes
            return Steric_Hindrance.No
        elif cate1_exh == Category1.Aromatic.value:
            neighbor = neighbor_c_idx_of_alpha_c(smile, category0)[1]
            for n in neighbor:
                if not count_H(smile, n) and mol.GetAtomWithIdx(n).GetAtomicNum() == 6 \
                        and is_idx_in_double_ring(smile, n) != 2:
                    return Steric_Hindrance.Yes
            return Steric_Hindrance.No
    else:
        return Steric_Hindrance.No


def classify(smile: str, category0: str) -> CategoryResult:
    category_0_list = get_category_0(smile)
    # 判断根据smile划分的大类是否与输入一致
    if category0 in category_0_list:
        # 包含关系，warning提示
        if len(category_0_list) > 1:
            warnings.warn('Compound belongs to multiple category_0!')
        # 无论包含还是等于，都进行下一步分类
        # 先判断是否易水解，与分类无关
        hydroly = get_hydrolysis(smile, category0)
        cate0 = convert_category_0(category0)
        cate1 = get_category_1(smile, category0)
        # cate1为芳香类
        if cate1.value == Category1.Aromatic.value:
            cate2 = get_category_2(smile, category0)
            sh = get_steric_hindrance(smile, cate1.value, category0)
            # cate2 为杂环
            if cate2.value == Category2Aromatic.Heterocyclic.value:
                cate3 = get_category_3(smile, category0)
                cate4 = get_category_4(smile, category0)
                cate5 = " ".join(get_category_5(smile, category0))
                return CategoryResult(cate0, cate1, cate2, cate3, cate4, cate5, hydroly, sh)
            else:
                return CategoryResult(cate0, cate1, cate2, Category3.Default, Category4.Default, "-", hydroly, sh)
        # cate1为脂肪类
        elif cate1.value == Category1.Aliphatic.value:
            cate2 = get_category_2(smile, category0)
            sh = get_steric_hindrance(smile, cate1.value, category0)
            return CategoryResult(cate0, cate1, cate2, Category3.Default, Category4.Default, "-", hydroly, sh)
        # cate1为活泼氢
        else:
            sh = get_steric_hindrance(smile, cate1.value, category0)
            return CategoryResult(cate0, cate1, Category2.Default, Category3.Default, Category4.Default, "-", hydroly,
                                  sh)
    elif category0 == 'Others':
        return CategoryResult(Category0.Others, Category1.Default, Category2.Default, Category3.Default,
                              Category4.Default, "-", Hydrolysis.Default, Steric_Hindrance.Default)

    # 判断有误，直接报错
    else:
        # return CategoryResult(Category0.Error, Category1.Default, Category2.Default, Category3.Default,
        #                       Category4.Default, "-", Hydrolysis.Default, Steric_Hindrance.Default)
        raise Exception('Illegal Category!')


# if __name__ == '__main__':
    # a = classify('CC(C)(C)OC(=O)N1CCN(S(=O)(=O)CCN)CC1', 'Amine')
    # a = classify('CC(C)(C)OC(=O)N1CCN(S(=O)(=O)CCN)CC1', 'Amine')  # BOC验证
    # a = classify('COC(=O)c1ccc(Cl)c(N)c1', 'Amine')  # 甲酯
    # a = classify('CCOC(=O)CC(C)(C)N', 'Amine')  # 乙酯
    # a = classify('COC(=O)CCCCCCN.Cl', 'Amine')  # 甲酯
    # a = classify('O=C(O)C1CCC1', 'Carboxylic Acid')
    # a = classify('OB(O)c1cn[nH]c1', 'Boronic Acid')  # 验证活泼氢
    # a = classify('CC1(C)OB(OC1(C)C)c1ccc(nc1)c1ccccc1', 'Boronic Acid')  # 验证吡啶变苯环
    # a = classify('Cn1cc(B2OC(C)(C)C(C)(C)O2)cn1', 'Boronic Acid')  # 验证吡啶变苯环(回归测试)
    # a = classify('CC1(C)OB(c2ccc(N3CCCCC3)nc2)OC1(C)C', 'Boronic Acid')  # 验证硼酸酯位阻
    # a = classify('O=C(O)c1ncon1', 'Carboxylic Acid')  # 验证羧酸位阻
    # a = classify('Cc1nn2c(O)nncc2c1Br', 'Halide')  # 验证卤代物位阻，有位阻
    # a = classify('c12c(cccc1c(c[nH]2)Br)N', 'Halide')  # 验证卤代物位阻，无位阻
    # a = classify('N#CCO', 'Alcohol')  # 验证位阻规则，alpha位小于2H
    # a = classify('CCC(C)=O', 'Ketone')  # 验证Ketone
    # a = classify('N#Cc1sc(Cl)nc1-c1ccc(Cl)cc1', 'Halide')  # 验证Halide
    # a = classify('[Cl-].[NH3+]C1CCCCC1(F)F', 'Amine')
    # a = classify('CC(=O)[O-]', 'Carboxylic Acid')
    # a = classify('O=C(O)CO', 'Alcohol')
    # a = classify('O=C1CCc2ccccc2CC1', 'Ketone')
    # a = classify('O=C(c1ccccc1)c2ccccn2', 'Ketone')
    # a = classify('O=C1COCc2ccccc12', 'Ketone')
    # a = classify('N#Cc1sc(Cl)nc1-c1ccc(Cl)cc1', 'Halide')
    # a = classify('O=C([O-])c1cccnc1.[Na+]', 'Carboxylic Acid')
    # a = classify('Cc1nnc(C(=O)[O-])s1.[Li+]', 'Carboxylic Acid')
    # print(a.category0)
    # print(a.category1)
    # print(a.category2)
    # print(a.category3)
    # print(a.category4)
    # print(a.category5)
    # print(a.hydrolysis)
    # print(a.steric_hindrance)
    # print(ifg('O=C1COCc2ccccc12', 'c1ccccc1'))
    # print(get_category_2('C#CCC(CC#CC)(C(=O)OC)C(=O)OC', 'Alkyne'))
    # print(get_category_2('CC1(C)OB(OC1(C)C)c1ccc(nc1)c1ccccc1', 'Boronic Acid'))
