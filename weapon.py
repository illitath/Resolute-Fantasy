class Weapon:
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


weapon_items = {
    '000': Weapon("fist", '000', True, 'bludgeoning', 0.5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '001': Weapon("dagger", '001', False, 'piercing', 0.5, 0, 5, 0, 2, 0, 0, 0.1, 0, 0, 0, 'none', 'none', 'none', 'none', 300),
    '002': Weapon("knife", '002', False, 'slashing', 0.3, 0, 10, 0, 0, 0, 0, 0.15, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '003': Weapon("oak wand", '003', False, 'bludgeoning', 0.5, 0, 10, 0, 0, 0, 0, 0.3, 0, 0, 0, 'none', 'none', 'none', 'none', 1600),
    '004': Weapon("copper gladius", '004', False, 'slashing', 0.5, 0, 50, 0, 0, 0, 0, 0.2, 0, 0, 0, 'none', 'none', 'none', 'none', 3500),
    '005': Weapon("hand axe", '005', False, 'slashing', 0.5, 0, 80, 0, 0, 0, 0, -0.1, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '006': Weapon("toothy club", '006', False, 'piercing', 0.3, 100, 50, 0, 0, 0, 0, 0.25, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '007': Weapon("rusty crowbar", '007', False, 'bludgeoning', 0.5, 0, 100, 20, 20, 0, 0, 0.3, 0, 0, 0, 'none', 'none', 'none', 'none', 10500),
    '008': Weapon("light hammer", '008', False, 'bludgeoning', 0.5, 0, 150, 0, 0, 0, 0, 0.25, 0, 0, 0, 'none', 'none', 'none', 'none', 15000),
    '009': Weapon("handsaw", '009', False, 'slashing', 0.2, 0, 150, 0, 0, 0, 0, 0.3, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '010': Weapon("claw hammer", '010', False, 'piercing', 0.3, 0, 200, 0, 0, 0, 0, 0.5, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '011': Weapon("iron sword", '011', False, 'slashing', 0.5, 0, 250, 0, 0, 0, 0, 0.4, 0, 0, 0, 'none', 'none', 'none', 'none', 42000),
    '012': Weapon("long spear", '012', False, 'piercing', 0.5, 0, 400, 0, 0, 0, 0, 0.1, 0, 0, 0, 'none', 'none', 'none', 'none', 62000),
    '013': Weapon("rogue dagger", '013', False, 'piercing', 0.5, 0, 250, 0, 50, 0, 0, 0.6, 0, 0, 0, 'none', 'none', 'none', 'none', 0),
    '014': Weapon("glaive", '014', False, 'slashing', 0.5, 0, 600, 0, 0, 0, 0, 0.15, 0, 0, 0, 'none', 'none', 'none','none', 62000),
    '015': Weapon("oak staff", '015', False, 'bludgeoning', 0.5, 500, 500, 0, 0, 0, 0, 0.5, 0, 0, 0, 'none', 'none','none', 'none', 0),

}