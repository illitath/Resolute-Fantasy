class Accessory:
    def __init__(self, name, num, gotten, base_stats1, base_stats2, base_stats3, base_stats4, base_stats5, multiplier1, multiplier2, multiplier3, multiplier4, multiplier5, attri1, attri2, attri3, attri4, price, item_count, limit):
        self.gotten = gotten
        self.name = name
        self.num = num
        self.base_stats1 = base_stats1
        self.base_stats2 = base_stats2
        self.base_stats3 = base_stats3
        self.base_stats4 = base_stats4
        self.base_stats5 = base_stats5
        self.multiplier1 = multiplier1
        self.multiplier2 = multiplier2
        self.multiplier3 = multiplier3
        self.multiplier4 = multiplier4
        self.multiplier5 = multiplier5
        self.attri1 = attri1
        self.attri2 = attri2
        self.attri3 = attri3
        self.attri4 = attri4
        self.price = price
        self.item_count = item_count
        self.limit = limit


accessory_items = {
    '000': Accessory("empty", '000', True, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0, 6, 6),

    '001': Accessory("HP gem +1", '001', False, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 500, 0, 3),
    '002': Accessory("HP gem +2", '002', False, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 8000, 0, 3),
    '003': Accessory("HP gem +3", '003', False, 800, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 40000, 0, 3),
    '004': Accessory("HP gem +4", '004', False, 2000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 120000, 0, 3),
    '005': Accessory("HP gem +5", '005', False, 6000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 450000, 0, 3),
    '006': Accessory("HP gem +6", '006', False, 24000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0, 0, 3),

    '007': Accessory("AP gem +1", '007', False, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 500, 0, 3),
    '008': Accessory("AP gem +2", '008', False, 0, 50, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 8000, 0, 3),
    '009': Accessory("AP gem +3", '009', False, 0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 40000, 0, 3),
    '010': Accessory("AP gem +4", '010', False, 0, 500, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 120000, 0, 3),
    '011': Accessory("AP gem +5", '011', False, 0, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 450000, 0, 3),
    '012': Accessory("AP gem +6", '012', False, 0, 6000, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0, 0, 3),

    '013': Accessory("DP gem +1", '013', False, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 500, 0, 3),
    '014': Accessory("DP gem +2", '014', False, 0, 0, 50, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 8000, 0, 3),
    '015': Accessory("DP gem +3", '015', False, 0, 0, 200, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 40000, 0, 3),
    '016': Accessory("DP gem +4", '016', False, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 120000, 0, 3),
    '017': Accessory("DP gem +5", '017', False, 0, 0, 1500, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none',450000, 0, 3),
    '018': Accessory("DP gem +6", '018', False, 0, 0, 6000, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none',0, 0, 3),

    '019': Accessory("DEX gem +1", '019', False, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 500, 0, 3),
    '020': Accessory("DEX gem +2", '020', False, 0, 0, 0, 50, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 8000, 0, 3),
    '021': Accessory("DEX gem +3", '021', False, 0, 0, 0, 200, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 40000, 0, 3),
    '022': Accessory("DEX gem +4", '022', False, 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 120000, 0, 3),
    '023': Accessory("DEX gem +5", '023', False, 0, 0, 0, 1500, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none',450000, 0, 3),
    '024': Accessory("DEX gem +6", '024', False, 0, 0, 0, 6000, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none',0, 0, 3),

    '025': Accessory("LUC gem +1", '025', False, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 500, 0, 3),
    '026': Accessory("LUC gem +2", '026', False, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 8000, 0, 3),
    '027': Accessory("LUC gem +3", '027', False, 0, 0, 0, 0, 200, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 40000, 0, 3),
    '028': Accessory("LUC gem +4", '028', False, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 120000, 0, 3),
    '029': Accessory("LUC gem +5", '029', False, 0, 0, 0, 0, 1500, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none',450000, 0, 3),
    '030': Accessory("LUC gem +6", '030', False, 0, 0, 0, 0, 6000, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none',0, 0, 3),

    '031': Accessory("EXP gem +1", '031', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'EXP0.1', 'none', 'none', 'none', 2000, 0, 3),
    '032': Accessory("EXP gem +2", '032', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'EXP0.2', 'none', 'none', 'none', 25000, 0, 3),
    '033': Accessory("EXP gem +3", '033', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'EXP0.3', 'none', 'none', 'none', 100000, 0, 3),
    '034': Accessory("EXP gem +4", '034', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'EXP0.5', 'none', 'none', 'none', 550000, 0, 3),
    '035': Accessory("EXP gem +5", '035', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'EXP0.7', 'none', 'none', 'none',0, 0, 3),
    '036': Accessory("EXP gem +6", '036', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'EXP1', 'none', 'none', 'none',0, 0, 3),

    '037': Accessory("aether powder", '037', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ENERGY1', 'none', 'none', 'none', 0, 0, 3),
    '038': Accessory("aether shards", '038', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ENERGY2', 'none', 'none', 'none', 0, 0, 3),
    '039': Accessory("aether gem", '039', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ENERGY3', 'none', 'none', 'none',0, 0, 3),
    '040': Accessory("aether crystal", '040', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ENERGY4', 'none', 'none', 'none',0, 0, 3),
    '041': Accessory("aether essence", '041', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ENERGY5', 'none', 'none', 'none', 0, 0, 3),
    '042': Accessory("aether core", '042', False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ENERGY6', 'none', 'none', 'none', 0, 0, 3),
}