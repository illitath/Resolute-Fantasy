

class Foe:
    def __init__(self, name, foe_id, foe_level, foe_hp_modifier, foe_ap_modifier, foe_dp_modifier, is_boss, bonus, drop1, drop2, drop3, attribute, attribute_percentage, piercing_resistance, slashing_resistance, bludgeoning_resistance, fire_resistance, ice_resistance, thunder_resistance, holy_resistance, dark_resistance):
        self.name = name
        self.foe_id = foe_id
        self.foe_level = foe_level
        self.foe_hp_modifier = foe_hp_modifier
        self.foe_ap_modifier = foe_ap_modifier
        self.foe_dp_modifier = foe_dp_modifier
        self.is_boss = is_boss
        self.bonus = bonus
        self.drop1 = drop1
        self.drop2 = drop2
        self.drop3 = drop3
        self.attribute = attribute
        self.attribute_percentage = attribute_percentage
        self.piercing_resistance = piercing_resistance
        self.slashing_resistance = slashing_resistance
        self.bludgeoning_resistance = bludgeoning_resistance
        self.fire_resistance = fire_resistance
        self.ice_resistance = ice_resistance
        self.thunder_resistance = thunder_resistance
        self.holy_resistance = holy_resistance
        self.dark_resistance = dark_resistance


enemies_dict = {
    '001': Foe("green slime", '001', 1, 0, 0, 0, False, 'no_bonus', "dagger", "worn vest", "none", 'bludgeoning', 0.5, 0, 0, -0.4, -0.5, 0, 0, 0, 0),
    '002': Foe("dwarf", '002', 5, -10, 0, -5, False, 'no_bonus', "scotland skirt", "couch-grass lid", "none", 'none', 0, 0, 0, 0, 0, 0, 0, 0, 0),
    '003': Foe("dirt doll", '003', 9, -50, 5, 0, False, 'no_bonus', "knife", "rattan sandal", "none", 'none', 0, 0.2, 0.2, -0.4, 0.5, -0.2, 0.5, 0, 0),
    '004': Foe("green bush", '004', 14, 0, 0, -10, False, 'no_bonus', "woolen gloves", "cloth shoes", "none", 'slashing', 0.5, 0, 0, 0, -0.5, 0, 0, 0, -0.5),
    '005': Foe("forest sprite", '005', 20, 0, 0, 0, True, 'no_bonus', "oak wand", "worn sneaker", "none", 'holy', 0.2, 0.2, 0.2, 0.2, -0.5, 0, 0, 0, -0.5),
    '006': Foe("cat warrior", '006', 25, 0, 0, 0, False, 'no_bonus', "hand axe", "casual trousers", "shattered wooden shield", 'slashing', 0.5, 0, -0.2, 0, -0.2, -0.2, -0.2, 0, 0),
    '007': Foe("cat mage", '007', 28, 0, 40, 0, False, 'no_bonus', "casual shoes", "woolen shirt", "none", 'fire', 0.5, 0, -0.2, 0, -0.2, -0.2, -0.2, 0, 0),
    '008': Foe("cat rogue", '008', 30, 0, 0, 50, False, 'no_bonus', "toothy club", "fabricated mittens", "none", 'piercing', 0.5, 0, -0.2, 0, -0.2, -0.2, -0.2, 0, 0),
    '009': Foe("doppelganger", '009', 35, 0, 0, 0, False, 'no_bonus', "leather pants", "leather jacket", "none", 'none', 0, 0, 0, 0, 0, 0, 0, 0, 0),
    '010': Foe("baby shapeshifter", '010', 40, -50, -20, 0, False, 'no_bonus', "light hammer", "aether powder", "none", 'dark', 0.5, 0, 0, 0, 0, 0, 0, -0.5, 0),
    '011': Foe("haunting tree", '011', 48, 0, 0, 0, False, 'no_bonus', "handsaw", "softwood round shield", "none", 'dark', 0.5, 0, -0.4, -0.4, 0, 0, 0, 0, 0.5),
    '012': Foe("deep gnome", '012', 52, -200, 0, 80, False, 'no_bonus', "claw hammer", "plate boots", "none", 'bludgeoning', 0.5, -0.2, -0.2, -0.2, 0.2, 0.2, 0.2, -0.2, 0.2),
    '013': Foe("crow", '013', 60, -200, 50, -50, False, 'no_bonus', "chain armor", "oven gloves", "none", 'piercing', 0.5, -0.4, -0.2, 0, 0, 0, -0.4, -0.2, 0.2),
    '014': Foe("huge green slime", '014', 60, 300, 50, -50, True, 'no_bonus', "soft lapboard", "copper shield", "none", 'bludgeoning', 0.5, 0, 0, -0.4, -0.5, 0, 0, -0, 0),
    '015': Foe("flying eye", '015', 65, 0, 0, 0, False, 'no_bonus', "long spear", "padded gloves", "none", 'none', 0, 0, 0, -0.2, -0.2, -0.2, -0.2, -0.2, 0.2),
    '016': Foe("giant lizard", '016', 75, 200, -20, 100, False, 'no_bonus', "fiber legging", "none", "none", 'slashing', 0.5, 0.2, 0.2, -0.2, 0, 0, 0, 0, 0),
    '017': Foe("black bear", '017', 80, 0, 0, 80, True, 'no_bonus', "rogue dagger", "scale armor", "none", 'bludgeoning', 0.5, 0, 0, 0, -0.2, 0.2, 0.2, 0, 0),
    '018': Foe("haunting soul", '018', 90, -400, 50, -100, False, 'no_bonus', "gauntlets", "steel shield", "none", 'bludgeoning', 0.5, 0, -0.2, 0, 0.5, 0.5, 0.5, -0.5, 0.5),
    '019': Foe("leopard", '019', 100, -400, 80, -100, False, 'no_bonus', "none", "none", "none", 'slashing', 0.5, 0, 0, 0, 0, 0, 0, 0, 0),
    '020': Foe("goblin scout", '020', 110, 0, 0, 0, False, 'no_bonus', "HP gem +3", "none", "none", 'none', 0, 0, 0, 0, 0, 0, 0, 0, 0),
    '021': Foe("ape", '021', 120, 400, 0, -100, False, 'no_bonus', "none", "DP gem +3", "none", 'bludgeoning', 0.5, 0, 0, -0.4, -0.4, 0, 0, 0, 0),
    '022': Foe("forest tortoise", '022', 130, 800, -50, 200, False, 'no_bonus', "aether shards", "none", "none", 'piercing', 0.5, 0.5, 0.3, -0.4, -0.5, 0.2, 0.5, 0, 0),
    '023': Foe("preying boa", '023', 145, -600, 100, 0, False, 'no_bonus', "light plate", "DEX gem +3", "none", 'none', 0, 0, -0.5, 0, 0, 0, 0, 0, 0),
    '024': Foe("bandit", '024', 160, 0, 0, 0, True, 'no_bonus', "EXP gem +2", "none", "none", 'slashing', 0.5, 0, 0, 0, 0, 0, 0, 0, 0),
    '025': Foe("hunter", '025', 175, 0, 100, -200, False, 'no_bonus', "LUC gem +3", "none", "none", 'piercing', 0.8, 0, 0, 0, 0, 0, 0, 0, 0),
    '026': Foe("fiery butcher", '026', 190, 1200, 0, -300, False, 'no_bonus', "none", "none", "none", 'slashing', 0.6, -0.5, 0, -0.2, 0, 0, 0, 0, 0),
    '027': Foe("oak golem", '027', 210, 1400, -300, 500, False, 'no_bonus', "none", "none", "none", 'bludgeoning', 0.5, 0, -0.5, 0.4, -0.8, 0, 0.2, 0, 0),
    '028': Foe("ancient totem", '028', 220, -200, 0, 100, True, 'no_bonus', "none", "none", "none", 'holy', 1, 0.5, 0.5, -0.8, 0.5, 0.5, 0.5, 0.8, -0.5),
    '029': Foe("forest defender", '029', 240, 1000, -300, 200, False, 'no_bonus', "none", "none", "none", 'bludgeoning', 0.6, 0, 0, -0.4, -0.4, 0.5, 0, 0, 0),
    '030': Foe("illusion of life", '030', 260, 2000, 0, 0, True, 'no_bonus', "none", "none", "none", 'piercing', 0.8, 0, 0, 0, -0.5, 0, 0, -0.5, -0.5),




    #'300': Foe("void eye", '300', 10000000, 0, 0, 0, False, 'no_bonus', "none", "none", "none",'bludgeoning', 0.5, 0, -0.2, 0, 0.5, 0.5, 0.5, -0.5, 0.5)
}
