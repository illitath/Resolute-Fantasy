class Shield:
    def __init__(self, name, num, gotten, element, element_percentage, base_stats1, base_stats2, base_stats3, base_stats4, base_stats5, multiplier1, multiplier2, multiplier3, multiplier4, multiplier5, attri1, attri2, attri3, attri4, price):
        self.gotten = gotten
        self.name = name
        self.num = num
        self.element = element
        self.element_percentage = element_percentage
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


shield_items = {
    '000': Shield("bare", '000', True, 'none', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '001': Shield("couch-grass lid", '001', False, 'none', 0, 20, 0, 5, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '002': Shield("shattered wooden shield", '002', False, 'piercing', 0.2, 60, 0, 10, 0, 0, 0.05, 0, 0.05, 0, 0, 'none', 'none', 'none', 'none', 300),
    '003': Shield("softwood round shield", '003', False, 'piercing', 0.2, 100, 0, 0, 0, 0, 0.15, 0, 0.1, 0, 0, 'none', 'none', 'none', 'none', 0),
    '004': Shield("copper shield", '004', False, 'fire', -0.4, 180, 0, 50, 0, 0, 0.2, 0, 0.1, 0, 0, 'none', 'none', 'none', 'none', 0),
    '005': Shield("iron shield", '005', False, 'slashing', 0.2, 400, 0, 100, 0, 0, 0.2, 0, 0.3, 0, 0, 'none', 'none', 'none', 'none', 25000),
    '006': Shield("steel shield", '006', False, 'slashing', 0.3, 500, 0, 200, 0, 0, 0.4, 0, 0.1, 0, 0, 'none', 'none', 'none', 'none', 60000),
    '007': Shield("life wood shield", '007', False, 'holy', 0.5, 1200, 0, 150, 0, 0, 0.4, 0, 0.2, 0, 0, 'none', 'none','none', 'none', 0),
}