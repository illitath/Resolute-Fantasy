class Leg:
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


leg_items = {
    '000': Leg("pants", '000', True, 'none', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '001': Leg("scotland skirt", '001', False, 'none', 0, 0, 0, 2, 5, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '002': Leg("casual trousers", '002', False, 'bludgeoning', 0.2, 20, 0, 10, 5, 0, 0, 0, 0.1, 0, 0, 'none', 'none', 'none', 'none', 1800),
    '003': Leg("leather pants", '003', False, 'bludgeoning', 0.2, 0, 0, 40, 5, 0, 0, 0, 0.2, 0, 0, 'none', 'none', 'none', 'none', 4000),
    '004': Leg("shin guard", '004', False, 'piercing', 0.2, 0, 0, 20, 50, 0, 0, 0.1, 0.2, 0.1, 0, 'none', 'none', 'none', 'none', 6000),
    '005': Leg("soft lapboard", '005', False, 'bludgeoning', 0.2, 80, 0, 100, 0, 0, 0, 0, 0.2, 0, 0, 'none', 'none', 'none', 'none', 0),
    '006': Leg("fiber legging", '006', False, 'none', 0, 0, 0, 250, 40, 0, 0, 0, 0.4, 0, 0, 'none', 'none', 'none', 'none', 0),
    '007': Leg("legplate", '007', False, 'slashing', 0.5, 0, 0, 600, 0, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
}