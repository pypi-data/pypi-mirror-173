from rdkit import Chem
from rdkit.Chem import rdqueries
from collections.abc import Iterable
from classification.models import Category0, Category5, Category2Aliphatic, Category4Smarts
from classification.models import Category0FunctionalGroup as C0FG


def mol_with_atom_index(mol):
    for atom in mol.GetAtoms():
        atom.SetAtomMapNum(atom.GetIdx())
    return mol


# 类型转换，把输入的category0:string 转换为Category0，以便最后的输出
def convert_category_0(category0: str) -> Category0:
    if category0 == Category0.Halide.value:
        return Category0.Halide
    elif category0 == Category0.Amine.value:
        return Category0.Amine
    elif category0 == Category0.Alcohol.value:
        return Category0.Alcohol
    elif category0 == Category0.Boronic_Acid.value:
        return Category0.Boronic_Acid
    elif category0 == Category0.Carboxylic_Acid.value:
        return Category0.Carboxylic_Acid
    elif category0 == Category0.Acid_Chloride.value:
        return Category0.Acid_Chloride
    elif category0 == Category0.Sulfonyl_Chloride.value:
        return Category0.Sulfonyl_Chloride
    elif category0 == Category0.Aldehyde.value:
        return Category0.Aldehyde
    elif category0 == Category0.Ketone.value:
        return Category0.Ketone
    # elif category0 == Category0.Alkyne.value:
    #     return Category0.Alkyne
    # elif category0 == Category0.Olefin.value:
    #     return Category0.Olefin
    # elif category0 == Category0.Epoxides.value:
    #     return Category0.Epoxides
    # elif category0 == Category0.Hydrazines.value:
    #     return Category0.Hydrazines
    # elif category0 == Category0.Isocyanates.value:
    #     return Category0.Isocyanates
    # elif category0 == Category0.Isothiocyanates.value:
    #     return Category0.Isothiocyanates
    # elif category0 == Category0.Nitriles.value:
    #     return Category0.Nitriles
    # elif category0 == Category0.Ester.value:
    #     return Category0.Ester
    else:
        return Category0.Error


# 根据category0匹配其对应的原子索引和官能团
def functional_group_from_category0(smile, category0):
    if category0 == Category0.Halide.value:
        # 脂肪类优先于芳香类，优先级按照I Br Cl F，脂肪类F不考虑
        if identify_functional_group(smile, 'C[I]')[1]:
            return identify_functional_group(smile, '[I]')[0], C0FG.Halide_I.value
        elif identify_functional_group(smile, 'C[Br]')[1]:
            return identify_functional_group(smile, '[Br]')[0], C0FG.Halide_Br.value
        elif identify_functional_group(smile, 'C[Cl]')[1]:
            return identify_functional_group(smile, '[Cl]')[0], C0FG.Halide_Cl.value
        elif identify_functional_group(smile, 'c[I]')[1]:
            return identify_functional_group(smile, '[I]')[0], C0FG.Halide_I.value
        elif identify_functional_group(smile, 'c[Br]')[1]:
            return identify_functional_group(smile, '[Br]')[0], C0FG.Halide_Br.value
        elif identify_functional_group(smile, 'c[Cl]')[1]:
            return identify_functional_group(smile, '[Cl]')[0], C0FG.Halide_Cl.value
        elif identify_functional_group(smile, 'c[F]')[1]:
            return identify_functional_group(smile, '[F]')[0], C0FG.Halide_F.value
        elif identify_functional_group(smile, 'C(F)')[1]:
            return identify_functional_group(smile, '[F]')[0], C0FG.Halide_F.value
        elif identify_functional_group(smile, '[n+]I')[1]:
            return identify_functional_group(smile, '[I]')[0], C0FG.Halide_I.value
        elif identify_functional_group(smile, '[n+]F')[1]:
            return identify_functional_group(smile, '[F]')[0], C0FG.Halide_F.value
        else:
            raise Exception('Incorrect Halide classification')
    elif category0 == Category0.Amine.value:
        # Amine优先芳香性alpha-c
        if identify_functional_group(smile, '[nH]')[1] and identify_functional_group(smile, 'c[nH]')[1] \
                or identify_functional_group(smile, 'C[nH]')[1]:
            return identify_functional_group(smile, '[nH]')[0], C0FG.Secondary_Amine_R.value
        elif identify_functional_group(smile, '[NH2]')[1] and identify_functional_group(smile, 'c[NH2]')[1] \
                or identify_functional_group(smile, 'C[NH2]')[1]:
            return identify_functional_group(smile, '[NH2]')[0], C0FG.Primary_or_Benzyl_Amine.value
        elif identify_functional_group(smile, '[NH]')[1] and identify_functional_group(smile, 'c[NH]')[1] \
                or identify_functional_group(smile, 'C[NH]')[1]:
            return identify_functional_group(smile, '[NH]')[0], C0FG.Secondary_Amine.value
        elif identify_functional_group(smile, '[N]')[1] and identify_functional_group(smile, 'c[N]')[1] \
                or identify_functional_group(smile, 'C[N]')[1]:
            return identify_functional_group(smile, '[N]')[0], C0FG.Tertiary_Amine.value
        else:
            raise Exception('Incorrect Amine classification')
    elif category0 == Category0.Alcohol.value:
        (matches, flag) = identify_functional_group(smile, C0FG.Alcohol.value)
        return matches, C0FG.Alcohol.value
    elif category0 == Category0.Boronic_Acid.value:
        (matches, flag) = identify_functional_group(smile, C0FG.Boronic_Acid.value)
        return matches, C0FG.Boronic_Acid.value
    elif category0 == Category0.Carboxylic_Acid.value:
        (matches, flag) = identify_functional_group(smile, C0FG.Carboxylic_Acid.value)
        return matches, C0FG.Carboxylic_Acid.value
    elif category0 == Category0.Acid_Chloride.value:
        (matches, flag) = identify_functional_group(smile, C0FG.Acid_Chloride.value)
        return matches, C0FG.Acid_Chloride.value
    elif category0 == Category0.Sulfonyl_Chloride.value:
        (matches, flag) = identify_functional_group(smile, C0FG.Sulfonyl_Chloride.value)
        return matches, C0FG.Sulfonyl_Chloride.value
    elif category0 == Category0.Aldehyde.value:
        (matches, flag) = identify_functional_group(smile, C0FG.Aldehyde.value)
        return matches, C0FG.Aldehyde.value
    elif category0 == Category0.Ketone.value:
        (matches, flag) = identify_functional_group(smile, C0FG.Ketone.value)
        return matches, C0FG.Ketone.value
    # elif category0 == Category0.Alkyne.value:
    #     (matches, flag) = identify_functional_group(smile, C0FG.Alkyne.value)
    #     return matches, C0FG.Alkyne.value
    # elif category0 == Category0.Olefin.value:
    #     (matches, flag) = identify_functional_group(smile, C0FG.Olefin.value)
    #     return matches, C0FG.Olefin.value
    # elif category0 == Category0.Epoxides.value:
    #     (matches, flag) = identify_functional_group(smile, C0FG.Epoxides.value)
    #     return matches, C0FG.Epoxides.value
    # elif category0 == Category0.Hydrazines.value:
    #     (matches, flag) = identify_functional_group(smile, C0FG.Hydrazines.value)
    #     return matches, C0FG.Hydrazines.value
    # elif category0 == Category0.Isocyanates.value:
    #     (matches, flag) = identify_functional_group(smile, C0FG.Isocyanates.value)
    #     return matches, C0FG.Isocyanates.value
    # elif category0 == Category0.Isothiocyanates.value:
    #     (matches, flag) = identify_functional_group(smile, C0FG.Isothiocyanates.value)
    #     return matches, C0FG.Isothiocyanates.value
    # elif category0 == Category0.Nitriles.value:
    #     (matches, flag) = identify_functional_group(smile, C0FG.Nitriles.value)
    #     return matches, C0FG.Nitriles.value
    # elif category0 == Category0.Ester.value:
    #     if identify_functional_group(smile, C0FG.Ester1.value)[1]:
    #         return identify_functional_group(smile, C0FG.Ester1.value)[0], C0FG.Ester1.value
    #     elif identify_functional_group(smile, C0FG.Ester2.value)[1]:
    #         return identify_functional_group(smile, C0FG.Ester2.value)[0], C0FG.Ester2.value
    #     elif identify_functional_group(smile, C0FG.Ester3.value)[1]:
    #         return identify_functional_group(smile, C0FG.Ester3.value)[0], C0FG.Ester3.value
    #     elif identify_functional_group(smile, C0FG.Ester4.value)[1]:
    #         return identify_functional_group(smile, C0FG.Ester4.value)[0], C0FG.Ester4.value
    #     elif identify_functional_group(smile, C0FG.Ester5.value)[1]:
    #         return identify_functional_group(smile, C0FG.Ester5.value)[0], C0FG.Ester5.value
    #     elif identify_functional_group(smile, C0FG.Ester6.value)[1]:
    #         return identify_functional_group(smile, C0FG.Ester6.value)[0], C0FG.Ester6.value
    #     else:
    #         raise Exception('Incorrect Ester classification')
    else:
        raise Exception('Incorrect compound classification')


# 根据category0反推alpha c index
def alpha_c_index_by_category(smile, category0):
    # Halide大类先脂肪后芳香
    if category0 == Category0.Halide.value:
        is_al, match_al = is_aliphatic_carbon(smile, category0)
        if is_al:
            return match_al
        else:
            is_ar, match_ar = is_aromatic_carbon(smile, category0)
            return match_ar
    # 醇类要去掉羧基的干扰
    elif category0 == Category0.Alcohol.value:
        if identify_functional_group(smile, 'C(=O)O')[1]:
            # 羧基中的C索引
            ex_c_idx = identify_functional_group(smile, 'C(=O)O')[0][0][0]
            is_ar, match_ar = is_aromatic_carbon(smile, category0)
            if is_ar:
                return delete_all_x_idx(match_ar, ex_c_idx)
            else:
                is_al, match_al = is_aliphatic_carbon(smile, category0)
                return delete_all_x_idx(match_al, ex_c_idx)
        else:
            is_ar, match_ar = is_aromatic_carbon(smile, category0)
            if is_ar:
                return match_ar
            else:
                is_al, match_al = is_aliphatic_carbon(smile, category0)
                return match_al
    # 其余大类先芳香后脂肪
    else:
        is_ar, match_ar = is_aromatic_carbon(smile, category0)
        if is_ar:
            return match_ar
        else:
            is_al, match_al = is_aliphatic_carbon(smile, category0)
            return match_al


# 判断与芳香碳的匹配
def is_aromatic_carbon(smile, category0):
    res = functional_group_from_category0(smile, category0)
    matches_ar = identify_functional_group(smile, 'c' + res[1])
    if not matches_ar[1]:
        matches_ar = identify_functional_group(smile, 'n' + res[1])
    return matches_ar[1], list(set([i[0] for i in matches_ar[0]]))


# 判断与脂肪C的匹配
def is_aliphatic_carbon(smile, category0):
    res = functional_group_from_category0(smile, category0)
    matches_al = identify_functional_group(smile, 'C' + res[1])
    return matches_al[1], list(set([i[0] for i in matches_al[0]]))


# 验证化合物是否含有官能团
def identify_functional_group(smile, smart):
    mol = Chem.MolFromSmiles(smile)
    functional_group = Chem.MolFromSmarts(smart)
    matches = mol.GetSubstructMatches(functional_group)
    return matches, len(matches) > 0


# 验证化合物是否为活泼氢
def is_free_H(smile, category0):
    # 不含活泼氢官能团（OH COOH NH2 NH）的大类，直接匹配活泼氢官能团子结构
    if category0 == Category0.Halide.value or category0 == Category0.Acid_Chloride.value or \
            category0 == Category0.Sulfonyl_Chloride.value or category0 == Category0.Aldehyde.value or \
            category0 == Category0.Ketone.value:  # or category0 == Category0.Alkyne.value or category0 == Category0.Olefin.value or category0 == Category0.Epoxides.value or category0 == Category0.Isocyanates.value or category0 == Category0.Isothiocyanates.value or category0 == Category0.Nitriles.value or category0 == Category0.Ester.value:
        matches_h = identify_functional_group(smile, '[OH,NH2,NH,nH]')
        matches_cooh = identify_functional_group(smile, 'C(=O)[OH1]')
        return len(matches_h[0]) > 0 or len(matches_cooh[0]) > 0
    # 胺类直接匹配OH COOH
    elif category0 == Category0.Amine.value:  # or category0 == Category0.Hydrazines.value:
        # 优先匹配[NH2]
        matches_nh2 = identify_functional_group(smile, C0FG.Primary_or_Benzyl_Amine.value)
        # 含有1个[NH2]以上则为活泼氢
        if len(matches_nh2[0]) > 1:
            return True
        # 恰有1个[NH2], 再看是否含有[NH]或[nH]或[OH,COOH]
        elif len(matches_nh2[0]) == 1:
            matches_nh = identify_functional_group(smile, C0FG.Secondary_Amine.value)
            matches_nhr = identify_functional_group(smile, C0FG.Secondary_Amine_R.value)
            matches_h = identify_functional_group(smile, '[OH]')
            matches_cooh = identify_functional_group(smile, 'C(=O)[OH1]')
            return len(matches_nh[0]) > 0 or len(matches_nhr[0]) > 0 or len(matches_h[0]) > 0 or len(
                matches_cooh[0]) > 0
        # 不含[NH2]
        else:
            # 看[NH]或[nH]的个数
            matches_nh = identify_functional_group(smile, C0FG.Secondary_Amine.value)
            matches_nhr = identify_functional_group(smile, C0FG.Secondary_Amine_R.value)
            if len(matches_nh[0]) > 1 or len(matches_nhr[0]) > 1 or (len(matches_nh[0]) + len(matches_nhr[0])) > 1:
                return True
            # elif len(matches_nh[0]) == 1 or len(matches_nhr[0]) == 1:
            #     matches_h = identify_functional_group(smile, '[OH,COOH]')
            #     return len(matches_h[0]) > 0
            else:
                matches_h = identify_functional_group(smile, '[OH]')
                matches_cooh = identify_functional_group(smile, 'C(=O)[OH1]')
                return len(matches_h[0]) > 0 or len(matches_cooh[0]) > 0

    # 醇类多元醇或含有活泼氢官能团
    elif category0 == Category0.Alcohol.value:
        # matches_al = identify_functional_group(smile, C0FG.Alcohol.value)
        matches_h = identify_functional_group(smile, '[NH2,NH,nH]')
        matches_cooh = identify_functional_group(smile, 'C(=O)[OH1]')
        return len(matches_h[0]) > 0 or len(matches_cooh[0]) > 0
    # 羧酸多元羧酸或含有活泼氢官能团
    elif category0 == Category0.Carboxylic_Acid.value:
        flag = False
        matches_ca = identify_functional_group(smile, C0FG.Carboxylic_Acid.value)
        if len(matches_ca[0]) > 1:
            flag = True
        else:
            matches_h = identify_functional_group(smile, '[OH,NH2,NH,nH]')
            for h in matches_h[0]:
                for ca in matches_ca[0]:
                    if h[0] not in ca:
                        flag = True
        return flag
    # 硼酸本身含有2个OH
    elif category0 == Category0.Boronic_Acid.value:
        flag = False
        matches_ba = identify_functional_group(smile, C0FG.Boronic_Acid.value)
        matches_h = identify_functional_group(smile, '[OH,NH2,NH,nH]')
        for h in matches_h[0]:
            for ba in matches_ba[0]:
                if h[0] not in ba:
                    flag = True
                    return flag
        matches_cooh = identify_functional_group(smile, 'C(=O)[OH1]')
        for cooh in matches_cooh[0]:
            for ba in matches_ba[0]:
                if cooh[0] not in ba:
                    flag = True
                    return flag
        return flag
    else:
        raise Exception('Incorrect compound classification')


# 验证化合物对脂肪类和环类的匹配度，即alpha-c所在的环是否为环状结构
def match_alpha_c_ali_aro(smile, func_group):
    smart_ali = 'C' + func_group
    smart_aro = '[R]' + func_group
    m = Chem.MolFromSmiles(smile)
    substructure_ali = Chem.MolFromSmarts(smart_ali)
    substructure_aro = Chem.MolFromSmarts(smart_aro)
    matches_ali = m.GetSubstructMatches(substructure_ali)
    matches_aro = m.GetSubstructMatches(substructure_aro)
    return matches_ali, matches_aro


# 验证alpha-c所在的环是否为芳香环
def is_ring_aromatic(smile, category0):
    m = Chem.MolFromSmiles(smile)
    # alpha-c原子索引列表
    ac = alpha_c_index_by_category(smile, category0)
    ac_ring = []
    for ri in m.GetRingInfo().AtomRings():
        for c_idx in ac:
            if c_idx in ri:
                ac_ring.append(ri)
    # 查询分子中所有芳香性原子的索引，结果为set集合
    q = rdqueries.IsAromaticQueryAtom()
    ar_atom = {x.GetIdx() for x in m.GetAtomsMatchingQuery(q)}
    # alpha-c所在环的碳原子索引集合 vs 分子中芳香性原子索引集合
    if set(get_item(ac_ring)) != set():
        for ac_r in ac_ring:
            if set(get_item(ac_r)).issubset(ar_atom):
                return True
        return False
    else:
        return False


# 验证某个index是否在环上以及环是否为芳香环
def is_idx_in_ring_and_aromatic(smile, index):
    m = Chem.MolFromSmiles(smile)
    # 得到环信息，并循环
    for ri in m.GetRingInfo().AtomRings():
        if index in ri:
            # index在环上，进一步判断环的芳香性
            q = rdqueries.IsAromaticQueryAtom()
            ar_atom = {x.GetIdx() for x in m.GetAtomsMatchingQuery(q)}
            # index所在环的碳原子索引集合 vs 分子中芳香性原子索引集合
            if set(get_item(ri)).issubset(ar_atom):
                return True
            else:
                return False
        else:
            return False


# 判断idx是否是两个环的并点
def is_idx_in_double_ring(smile, idx):
    m = Chem.MolFromSmiles(smile)
    ct = 0
    for ri in m.GetRingInfo().AtomRings():
        if idx in ri:
            ct += 1
    return ct


# 根据alpha-c上的H区分脂肪类
def count_H_on_alpha_c(smile, category0):
    idx_list = alpha_c_index_by_category(smile, category0)
    alpha_c_h_num = []
    for idx in idx_list:
        h_num = count_H(smile, idx)
        alpha_c_h_num.append(h_num)
    if sum(alpha_c_h_num) == 2 * len(alpha_c_h_num) or max(alpha_c_h_num) >= 2:
        return Category2Aliphatic.Primary
    elif sum(alpha_c_h_num) == len(alpha_c_h_num) or max(alpha_c_h_num) == 1:
        return Category2Aliphatic.Secondary
    elif sum(alpha_c_h_num) == 0:
        return Category2Aliphatic.Tertiary
    else:
        return Category2Aliphatic.Error


# 验证是否为并环
def is_fused_ring(smile, category0):
    flag = False
    # 先拿到alpha-c列表
    alpha_c_idx_list = alpha_c_index_by_category(smile, category0)
    # 再拿到环列表
    mol = Chem.MolFromSmiles(smile)
    ring_atom_idx_list = mol.GetRingInfo().AtomRings()
    # 定义含有alpha-c的环
    alpha_c_rings = []
    for alpha_c_idx in alpha_c_idx_list:
        for ring_atom_idx in ring_atom_idx_list:
            if alpha_c_idx in ring_atom_idx:
                alpha_c_rings.append(ring_atom_idx)
    # alpha-c环与环列表匹配，各自都必须是芳香环且交集个数等于2则是并环
    for alpha_c_ring in alpha_c_rings:
        for ring_atom_idx in ring_atom_idx_list:
            acr_is_ar = is_tuple_aromatic(smile, alpha_c_ring)
            rai_is_ar = is_tuple_aromatic(smile, ring_atom_idx)
            if alpha_c_ring != ring_atom_idx and acr_is_ar and rai_is_ar \
                    and len(set(alpha_c_ring).intersection(ring_atom_idx)) == 2:
                flag = True
    return flag


# 验证某tuple是否为芳香性环
def is_tuple_aromatic(smile, t):
    m = Chem.MolFromSmiles(smile)
    q = rdqueries.IsAromaticQueryAtom()
    ar_atom = {x.GetIdx() for x in m.GetAtomsMatchingQuery(q)}
    if len(t):
        return set(get_item(t)).issubset(ar_atom)
    else:
        return False


# 验证某tuple是否为自定义芳香性环
def is_tuple_custom_aromatic(smile, t):
    m = Chem.MolFromSmiles(smile)
    sp2_flag = 1
    for idx in t:
        if str(m.GetAtomWithIdx(idx).GetHybridization()) != 'SP2':
            sp2_flag = 0
    return sp2_flag


# 验证苯环还是杂环，前提是上一级分类为芳香环，且非并环
# 从alpha-c索引入手查是否包含在环索引元组中，然后根据个数判断5元6元
def is_ring_x_atom(smile, category0):
    alpha_c_idx_list = alpha_c_index_by_category(smile, category0)
    ring_len = []
    for alpha_c_idx in alpha_c_idx_list:
        num = count_ring_atom(smile, alpha_c_idx)
        if num:
            ring_len.append(num)

    return ring_len


# 判断alpha-c所在的环是不是杂环，前提是该化合物已经被分为芳香类
def is_alpha_ring_heterocyclic(smile, category0):
    # alpha-c列表
    alpha_c_idx_list = alpha_c_index_by_category(smile, category0)
    # 环tuple列表
    mol = Chem.MolFromSmiles(smile)
    ring_list = mol.GetRingInfo().AtomRings()
    ar_ring_list = []
    for t in ring_list:
        if is_tuple_custom_aromatic(smile, t):
            ar_ring_list.append(t)
    is_hete = 0
    for idx in alpha_c_idx_list:
        for ring in ar_ring_list:
            if idx in ring:
                for ri in ring:
                    if mol.GetAtomWithIdx(ri).GetAtomicNum() != 6:
                        is_hete = 1
    return is_hete


# 某个原子上H的个数
def count_H(smile, c_index):
    m = Chem.MolFromSmiles(smile)
    num = m.GetAtomWithIdx(c_index).GetTotalNumHs()
    return num


def is_aromatic(smile, c_index):
    m = Chem.MolFromSmiles(smile)
    return m.GetAtomWithIdx(c_index).GetIsAromatic()


# 判断某索引所在环的原子个数
def count_ring_atom(smile, alpha_c_idx):
    m = Chem.MolFromSmiles(smile)
    ri = m.GetRingInfo()
    num = 0
    for r in ri.AtomRings():
        if is_tuple_aromatic(smile, r):
            if alpha_c_idx in r:
                num = len(r)
    if num:
        return num
    else:
        for r in ri.AtomRings():
            if is_tuple_custom_aromatic(smile, r):
                if alpha_c_idx in r:
                    num = len(r)
        return num


# 判断alpha-c在环上的位置，前提是上一级为5、6元杂环
def locate_alpha_c_index_on_heterocyclic(smile, category0, heterocyclic):
    # 得到alpha-c index
    alpha_c_idx = alpha_c_index_by_category(smile, category0)
    # 匹配对应的杂环
    (matches, flag) = identify_functional_group(smile, heterocyclic)
    position_list = []
    for alpha_c in alpha_c_idx:
        for match in matches:
            if alpha_c in match:
                position = match.index(alpha_c) + 1
                # 对于对称结构做互补替换
                # 五元杂环对称结构5->2, 4->3
                if heterocyclic in [Category4Smarts.Furan.value, Category4Smarts.Tetranitrogen_monooxide.value,
                                    Category4Smarts.Thiophene.value, Category4Smarts.Thiadiazole_134.value,
                                    Category4Smarts.Tetranitrogen_monosulfide.value, Category4Smarts.Pyrrole.value,
                                    Category4Smarts.Pentazole_1H.value]:
                    if position == 5:
                        position = 2
                    elif position == 4:
                        position = 3
                # 六元杂环对称结构6->2, 5->3
                elif heterocyclic in [Category4Smarts.Pyridine.value, Category4Smarts.Hexazine.value]:
                    if position == 6:
                        position = 2
                    elif position == 5:
                        position = 3
                # 六元杂环中心对称结构
                elif heterocyclic in [Category4Smarts.Pyrazine.value]:
                    if position in [3, 5, 6]:
                        position = 2
                # 六元杂环中心对称结构
                elif heterocyclic in [Category4Smarts.Triazine_135.value]:
                    if position in [2, 4, 6]:
                        position = 2
                # 六元杂环中心对称结构
                elif heterocyclic in [Category4Smarts.Tetrazine_1235.value]:
                    if position in [2, 6]:
                        position = 2
                position_list.append(position)

    return position_list


# 根据position_list返回官能团位置信息list
def mapping_from_position_list(pos):
    pos_info = []
    for p in pos:
        if p == Category5.Pos_1.value:
            pos_info.append("1")
        elif p == Category5.Pos_2.value:
            pos_info.append("2")
        elif p == Category5.Pos_3.value:
            pos_info.append("3")
        elif p == Category5.Pos_4.value:
            pos_info.append("4")
        elif p == Category5.Pos_5.value:
            pos_info.append("5")
        elif p == Category5.Pos_6.value:
            pos_info.append("6")
        else:
            pos_info.append("-")

    return pos_info


# 判断是否易水解
def is_hydrolysis(smile, category0):
    if identify_functional_group(smile, 'C#N')[1]:  # 氰基CN
        return True
    elif identify_functional_group(smile, 'C(=O)O[CH3]')[1]:  # 甲酯COOCH3
        return True
    elif identify_functional_group(smile, 'C(=O)O[CH2][CH3]')[1]:  # 乙酯COOCH2CH3
        return True
    else:
        return False


# 查找alpha-c上邻位c的idx
def neighbor_c_idx_of_alpha_c(smile, category0):
    mol = Chem.MolFromSmiles(smile)
    ring = mol.GetRingInfo().AtomRings()
    neighbor = []
    neighbor_c = []
    alpha_c_idx = alpha_c_index_by_category(smile, category0)[0]
    # 邻位必须在环上
    for nei in mol.GetAtomWithIdx(alpha_c_idx).GetNeighbors():
        for ri in ring:
            if nei.GetIdx() in ri:
                neighbor.append(nei.GetIdx())
    # 邻位必须为c
    for n in neighbor:
        if mol.GetAtomWithIdx(n).GetAtomicNum() == 6 or mol.GetAtomWithIdx(n).GetAtomicNum() == 7 \
                or mol.GetAtomWithIdx(n).GetAtomicNum() == 8 or mol.GetAtomWithIdx(n).GetAtomicNum() == 16:
            neighbor_c.append(n)

    return neighbor, neighbor_c


# alpha-c的化学键类型，是否含有DOUBLE，TRIPLE
def alpha_c_bonds_type(smile, category0):
    flag = False
    mol = Chem.MolFromSmiles(smile)
    # alpha-c列表
    alpha_c_idx_list = alpha_c_index_by_category(smile, category0)
    for alpha_c_idx in alpha_c_idx_list:
        # 获取alpha-c周围的原子
        neighbors = mol.GetAtomWithIdx(alpha_c_idx).GetNeighbors()
        for neighbor in neighbors:
            # 获取相邻两原子的化学键类型
            bond_type = mol.GetBondBetweenAtoms(alpha_c_idx, neighbor.GetIdx()).GetBondType()
            # alpha-c含有双键或三键，符合烯类
            if str(bond_type) in ['DOUBLE', 'TRIPLE']:
                flag = True
                return flag
    return flag


# 自定义芳香性环的判断
def is_ring_custom_ar(smile, category0):
    # 如果满足rdkit定义的芳香性，则为芳香
    if is_ring_aromatic(smile, category0):
        return 1
    # 未满足rdkit定义的，则用原子连接的化学键个数判断
    else:
        # alpha-c列表
        alpha_c_idx_list = alpha_c_index_by_category(smile, category0)
        # 环列表
        mol = Chem.MolFromSmiles(smile)
        ring_atom_idx_list = mol.GetRingInfo().AtomRings()
        # 找出含有alpha-c的环
        alpha_c_rings = []
        for alpha_c_idx in alpha_c_idx_list:
            for ring_atom_idx in ring_atom_idx_list:
                if alpha_c_idx in ring_atom_idx:
                    alpha_c_rings.append(ring_atom_idx)
        sp2_flag = 1
        if len(alpha_c_rings):
            for alpha_c_ring in alpha_c_rings:
                for idx in alpha_c_ring:
                    if str(mol.GetAtomWithIdx(idx).GetHybridization()) != 'SP2':
                        sp2_flag = 0
        else:
            sp2_flag = 0
        return sp2_flag


# 解决任意层次的嵌套元素提取
def get_item(total: Iterable) -> list:
    # 创建用于计算的闭包
    def calculate(lst: Iterable):  # 传入一个可迭代对象
        for item in lst:
            # 如果其中元素不可迭代，说明到达嵌套列表底层。将这个元素加到储存最终结果的result列表中，用return结束此次递归
            if not isinstance(item, Iterable):  # 这里判断元素是否可以迭代
                result.append(item)
            # 如果元素依旧可以迭代，调用递归对这个元素进行计算
            else:
                calculate(item)

    result = []  # 创建储存结果的列表
    calculate(total)  # 调用闭包计算
    return result  # 返回最终结果


# 判断alpha-c list与成环原子索引的关系，优先考虑了环上的alpha-c
def unique_alpha_c_idx_in_ring(alpha_c_list, smile):
    m = Chem.MolFromSmiles(smile)
    # 环原子索引
    ring = m.GetRingInfo().AtomRings()
    deduplicated = []
    # 1个alpha-c list与不同环做交集
    for ri in ring:
        i = set(alpha_c_list).intersection(set(ri))
        # 如果有交集，只取一个
        if len(i):
            deduplicated.append(list(i)[0])
    # 一直无交集，则保持原样
    if not len(deduplicated):
        deduplicated = alpha_c_list

    return deduplicated


# 删除某列表中的所有特定元素
def delete_all_x_idx(li, x):
    while True:
        if x in li:
            li.remove(x)
            continue
        else:
            break
    return li


# if __name__ == '__main__':
#     print(is_ring_custom_ar('O=C1COCc2ccccc12', 'Ketone'))
# print(identify_functional_group('C(=O)(CO)O', 'C(=O)O')[0][0][0])
# print(alpha_c_index_by_category('C(=O)(CO)O', 'Alcohol'))
# print(count_H_on_alpha_c('C#CCC(CC#CC)(C(=O)OC)C(=O)OC', 'Alkyne'))
# print(alpha_c_index_by_category('CCC(C)=O', 'Ketone'))
# print(alpha_c_index_by_category('C#CCC(CC#CC)(C(=O)OC)C(=O)OC', 'Alkyne'))
# print(identify_functional_group('O=C(O)C1CCC1', C0FG.Carboxylic_Acid.value))
# print(is_free_H('OB(O)c1cn[nH]c1', 'Boronic Acid'))
# print(is_free_H('O=C(O)C1CCO1', "Carboxylic Acid"))
# print(is_free_H('OB(O)c1cc(F)ccc1C(F)(F)F', "Boronic Acid"))
# print(is_alpha_ring_heterocyclic('CC1(C)OB(OC1(C)C)c1ccc(nc1)c1ccccc1', "Boronic Acid"))
# print(count_H('C1=CNCC1', 3))
# print(neighbor_c_idx_of_alpha_c('CN1CCN(c2ccc(B3OC(C)(C)C(C)(C)O3)cc2)CC1', 'Boronic Acid'))
# print(neighbor_c_idx_of_alpha_c('O=C(O)c1ccno1', 'Carboxylic Acid'))
# print(is_idx_in_double_ring('Oc1nccc2c(Br)[nH]nc12', 9))
