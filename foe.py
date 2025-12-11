

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
    '002': Foe("dwarf", '002', 5, -1, 0, -1, False, 'no_bonus', "scotland skirt", "couch-grass lid", "none", 'none', 0, 0, 0, 0, 0, 0, 0, 0, 0),
    '003': Foe("dirt doll", '003', 9, -50, 5, 0, False, 'no_bonus', "knife", "rattan sandal", "none", 'none', 0, 0.2, 0.2, -0.4, 0.5, -0.2, 0.5, 0, 0),
    '004': Foe("green bush", '004', 14, 0, 0, -10, False, 'no_bonus', "woolen gloves", "cloth shoes", "woolen shirt", 'slashing', 0.5, 0, 0, 0, -0.5, 0, 0, 0, -0.5),
    '005': Foe("forest sprite", '005', 20, 0, 0, 0, True, 'no_bonus', "oak wand", "worn sneaker", "none", 'holy', 0.2, 0.2, 0.2, 0.2, -0.5, 0, 0, 0, -0.5),
    '006': Foe("cat warrior", '006', 25, 0, 0, 0, False, 'no_bonus', "hand axe", "casual trousers", "shattered wooden shield", 'slashing', 0.5, 0, -0.2, 0, -0.2, -0.2, -0.2, 0, 0),
    '007': Foe("cat mage", '007', 28, 0, 40, 0, False, 'no_bonus', "casual shoes", "leather jacket", "none", 'fire', 0.5, 0, -0.2, 0, -0.2, -0.2, -0.2, 0, 0),
    '008': Foe("cat rogue", '008', 30, 0, 0, 50, False, 'no_bonus', "toothy club", "fabricated mittens", "none", 'piercing', 0.5, 0, -0.2, 0, -0.2, -0.2, -0.2, 0, 0),
    '009': Foe("doppelganger", '009', 35, 0, 0, 0, False, 'no_bonus', "leather pants", "chain armor", "none", 'none', 0, 0, 0, 0, 0, 0, 0, 0, 0),
    '010': Foe("baby shapeshifter", '010', 40, -50, -20, 0, False, 'no_bonus', "light hammer", "none", "none", 'dark', 0.5, 0, 0, 0, 0, 0, 0, -0.5, 0),
    '011': Foe("haunting tree", '011', 48, 0, 0, 0, False, 'no_bonus', "handsaw", "softwood round shield", "none", 'dark', 0.5, 0, -0.4, -0.4, 0, 0, 0, 0, 0.5),
    '012': Foe("deep gnome", '012', 52, -200, 0, 80, False, 'no_bonus', "claw hammer", "plate boots", "none", 'bludgeoning', 0.5, -0.2, -0.2, -0.2, 0.2, 0.2, 0.2, -0.2, 0.2),
    '013': Foe("crow", '013', 60, -200, 50, -50, False, 'no_bonus', "scale armor", "oven gloves", "none", 'piercing', 0.5, -0.4, -0.2, 0, 0, 0, -0.4, -0.2, 0.2),
    '014': Foe("huge green slime", '014', 60, 300, 50, -50, True, 'no_bonus', "soft lapboard", "copper shield", "none", 'bludgeoning', 0.5, 0, 0, -0.4, -0.5, 0, 0, -0, 0),
    '015': Foe("flying eye", '015', 65, 0, 0, 0, False, 'no_bonus', "long spear", "padded gloves", "none", 'none', 0, 0, 0, -0.2, -0.2, -0.2, -0.2, -0.2, 0.2),
    '016': Foe("giant lizard", '016', 75, 200, -20, 100, False, 'no_bonus', "fiber legging", "none", "none", 'slashing', 0.5, 0.2, 0.2, -0.2, 0, 0, 0, 0, 0),
    '017': Foe("black bear", '017', 80, 0, 0, 80, True, 'no_bonus', "rogue dagger", "light plate", "none", 'bludgeoning', 0.5, 0, 0, 0, -0.2, 0.2, 0.2, 0, 0),
    '018': Foe("haunting soul", '018', 90, -400, 50, -100, False, 'no_bonus', "gauntlets", "steel shield", "none", 'bludgeoning', 0.5, 0, -0.2, 0, 0.5, 0.5, 0.5, -0.5, 0.5)
}
