class Hand:
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


hand_items = {
    '000': Hand("bare", '000', True, 'none', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '001': Hand("woolen gloves", '001', False, 'none', 0, 0, 0, 0, 0, 0, 0, 0.1, 0, 0, 0, 'none', 'none', 'none', 'none', 800),
    '002': Hand("fabricated mittens", '002', False, 'none', 0, 0, 0, 0, 10, 0, 0, 0.15, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '003': Hand("leather gloves", '003', False, 'slashing', 0.1, 0, 20, 30, 0, 0, 0, 0.25, 0, 0, 0, 'none', 'none', 'none', 'none', 5000),
    '004': Hand("oven gloves", '004', False, 'Fire', 0.4, 20, 50, 0, 0, 0, 0, 0.3, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '005': Hand("padded gloves", '005', False, 'bludgeoning', 0.3, 0, 50, 100, 0, 0, 0, 0.3, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '006': Hand("gauntlets", '006', False, 'piercing', 0.4, 200, 0, 200, 0, 0, 0, 0.4, 0, 0, 0, 'none', 'none', 'none', 'none', 42000),
    '007': Hand("royal gloves", '007', False, 'none', 0, 400, 0, 250, 0, 0, 0, 0.45, 0, 0, 0, 'none', 'none', 'none','none', 0),
}