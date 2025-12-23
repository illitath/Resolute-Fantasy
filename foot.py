class Foot:
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


foot_items = {
    '000': Foot("clog", '000', True, 'piercing', 0.1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '001': Foot("cloth shoes", '001', False, 'bludgeoning', 0.2, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 700),
    '002': Foot("rattan sandal", '002', False, 'none', 0, 0, 0, 10, 0, 0, 0, 0, 0.1, 0, 0, 'none', 'none', 'none', 'none', 0),
    '003': Foot("worn sneaker", '003', False, 'bludgeoning', 0.2, 0, 0, 20, 10, 0, 0, 0, 0.2, 0, 0, 'none', 'none', 'none', 'none', 0),
    '004': Foot("casual shoes", '004', False, 'none', 0, 0, 0, 20, 40, 0, 0, 0, 0.2, 0.1, 0, 'none', 'none', 'none', 'none', 9500),
    '005': Foot("traveller boots", '005', False, 'slashing', 0.2, 50, 0, 60, 50, 0, 0, 0, 0.2, 0, 0, 'none', 'none', 'none', 'none', 13000),
    '006': Foot("plate boots", '006', False, 'slashing', 0.4, 0, 0, 250, 0, 0, 0, 0, 0.25, 0, 0, 'none', 'none', 'none', 'none', 0),
    '007': Foot("royal boots", '007', False, 'piercing', 0.2, 0, 0, 400, 0, 0, 0, 0, 0.3, 0.1, 0, 'none', 'none', 'none','none', 0)
}