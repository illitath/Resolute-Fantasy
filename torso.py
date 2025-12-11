class Torso:
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


torso_items = {
    '000': Torso("bare", '000', True, 'none', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '001': Torso("worn vest", '001', False, 'none', 0, 0, 0, 5, 0, 0, 0, 0, 0.1, 0, 0, 'none', 'none', 'none', 'none', 400),
    '002': Torso("woolen shirt", '002', False, 'none', 0, 0, 0, 30, 0, 0, 0, 0, 0.15, 0, 0, 'none', 'none', 'none', 'none', 1200),
    '003': Torso("leather jacket", '003', False, 'bludgeoning', 0.2, 0, 0, 30, 0, 0, 0, 0, 0.25, 0, 0, 'none', 'none', 'none', 'none', 0),
    '004': Torso("chain armor", '004', False, 'slashing', 0.6, 0, 0, 50, 0, 0, 0, 0, 0.3, 0, 0, 'none', 'none', 'none', 'none', 0),
    '005': Torso("scale armor", '005', False, 'slashing', 0.4, 0, 0, 100, 0, 0, 0, 0, 0.4, 0, 0, 'none', 'none', 'none', 'none', 0),
    '006': Torso("light plate", '006', False, 'piercing', 0.4, 0, 0, 400, 0, 0, 0, 0, 0.1, 0, 0, 'none', 'none', 'none', 'none', 20000),
}