import math
import time

from random import random


from foe import enemies_dict
from color import Colors
from leg import leg_items
from torso import torso_items
from weapon import weapon_items
from shield import shield_items
from hand import hand_items
from foot import foot_items

all_dicts = [enemies_dict, weapon_items, torso_items, leg_items, hand_items, shield_items, foot_items]


energy: int = 25
level: int = 1
playerHP: int
playerAP: int
playerDP: int
playerDEX: int
playerLUC: int
weaponOnUse = weapon_items.get('000')
torsoOnUse = torso_items.get('000')
gloveOnUse = hand_items.get('000')
legOnUse = leg_items.get('000')
shieldOnUse = shield_items.get('000')
footOnUse = foot_items.get('000')
baseHP: int = 100
baseAP: int = 15
baseDP: int = 15
baseDEX: int = 10
baseLUC: int = 10
piercingRESIS: float = 0
slashingRESIS: float = 0
bludgeoningRESIS: float = 0
fireRESIS: float = 0
iceRESIS: float = 0
thunderRESIS: float = 0
holyRESIS: float = 0
darkRESIS: float = 0
resis_count = {'piercing': 0, 'slashing': 0, 'bludgeoning': 0, 'fire': 0, 'ice': 0, 'thunder': 0, 'holy': 0, 'dark': 0}


playerACC: int = 0
playerEVA: int = 0
SP: int = 0
EXP: int = 0
MONEY: int = 0
criticalChance: float = 0.05
criticalDamage: float = 1.5


def get_entity_by_id(entity_dict, entity_id):
    return entity_dict.get(entity_id)


def get_entity_by_name(entity_dict, name):
    try:
        entity_dict.values()
    except AttributeError:
        return None
    for entity in entity_dict.values():
        if entity.name == name:
            return entity
    return None


def get_dict_by_name(catalog_dicts, name):
    if name == 'none':
        return None
    for dictionary in catalog_dicts:
        for item in dictionary.values():
            if item.name == name:
                return dictionary
    return None


def player_damage_calculator(player_ap, weapon, foe):
    global criticalChance
    ap_bonus_multiplier = 1
    crit_bonus_modifier = 0
    if foe.bonus == 'AP50P':
        ap_bonus_multiplier = 1.5
    elif foe.bonus == 'CRIT30P':
        crit_bonus_modifier = 0.3
    elif foe.bonus == 'ULTIMATE':
        ap_bonus_multiplier = 1.3
        crit_bonus_modifier = 0.2
    foe_dp = foe_dp_calculator(foe)
    player_ap = math.floor((0.85 + 0.3 * random()) * player_ap)
    elemental_factor = 1
    if (not foe.piercing_resistance == 0) and (weapon.element == 'piercing'):
        elemental_factor = 1 - foe.piercing_resistance * weapon.element_percentage
    elif (not foe.slashing_resistance == 0) and (weapon.element == 'slashing'):
        elemental_factor = 1 - foe.slashing_resistance * weapon.element_percentage
    elif (not foe.bludgeoning_resistance == 0) and (weapon.element == 'bludgeoning'):
        elemental_factor = 1 - foe.bludgeoning_resistance * weapon.element_percentage
    elif (not foe.fire_resistance == 0) and (weapon.element == 'fire'):
        elemental_factor = 1 - foe.fire_resistance * weapon.element_percentage
    elif (not foe.ice_resistance == 0) and (weapon.element == 'ice'):
        elemental_factor = 1 - foe.ice_resistance * weapon.element_percentage
    elif (not foe.thunder_resistance == 0) and (weapon.element == 'thunder'):
        elemental_factor = 1 - foe.thunder_resistance * weapon.element_percentage
    elif (not foe.holy_resistance == 0) and (weapon.element == 'holy'):
        elemental_factor = 1 - foe.holy_resistance * weapon.element_percentage
    elif (not foe.dark_resistance == 0) and (weapon.element == 'dark'):
        elemental_factor = 1 - foe.dark_resistance * weapon.element_percentage
    if player_ap <= 0:
        return 0
    if random() < criticalChance + crit_bonus_modifier:
        multiplier = criticalDamage * (player_ap * ap_bonus_multiplier + (0.028 * foe_dp)) / (
                    player_ap * ap_bonus_multiplier + (0.287 * foe_dp))
        is_critical = True
    else:
        multiplier = (player_ap * ap_bonus_multiplier + (0.028 * foe_dp)) / (
                    player_ap * ap_bonus_multiplier + (0.557 * foe_dp))
        is_critical = False
    player_damage = player_ap * multiplier * ap_bonus_multiplier * elemental_factor
    return int(player_damage), bool(is_critical), elemental_factor


def foe_damage_calculator(foe, player_dp):
    dp_bonus_modifier = 1
    if foe.bonus == 'DP100P':
        dp_bonus_modifier = 2
    elif foe.bonus == 'ULTIMATE':
        dp_bonus_modifier = 1.6
    foe_ap = math.floor((0.85 + 0.3 * random()) * foe_ap_calculator(foe))
    foe_threshold = foe_threshold_calculator(foe.foe_level)
    if (player_dp * dp_bonus_modifier + dp_bonus_modifier * foe.foe_level / 5) <= foe_threshold:
        return foe_ap
    if foe_ap <= 0:
        return 0
    elemental_factor = 1
    if (not piercingRESIS == 0) and (foe.attribute == 'piercing'):
        elemental_factor = 1 - piercingRESIS * foe.attribute_percentage
    elif (not slashingRESIS == 0) and (foe.attribute == 'slashing'):
        elemental_factor = 1 - slashingRESIS * foe.attribute_percentage
    elif (not bludgeoningRESIS == 0) and (foe.attribute == 'bludgeoning'):
        elemental_factor = 1 - bludgeoningRESIS * foe.attribute_percentage
    elif (not fireRESIS == 0) and (foe.attribute == 'fire'):
        elemental_factor = 1 - fireRESIS * foe.attribute_percentage
    elif (not iceRESIS == 0) and (foe.attribute == 'ice'):
        elemental_factor = 1 - iceRESIS * foe.attribute_percentage
    elif (not thunderRESIS == 0) and (foe.attribute == 'thunder'):
        elemental_factor = 1 - thunderRESIS * foe.attribute_percentage
    elif (not holyRESIS == 0) and (foe.attribute == 'holy'):
        elemental_factor = 1 - holyRESIS * foe.attribute_percentage
    elif (not darkRESIS == 0) and (foe.attribute == 'dark'):
        elemental_factor = 1 - darkRESIS * foe.attribute_percentage
    multiplier = (foe_ap + (0.028 * (player_dp * dp_bonus_modifier + dp_bonus_modifier * foe.foe_level / 5))) / (
                foe_ap + (0.557 * (player_dp * dp_bonus_modifier + dp_bonus_modifier * foe.foe_level / 5)))
    foe_damage = foe_ap * multiplier * elemental_factor
    return int(foe_damage), elemental_factor


def battle_simulator(player_ap, player_dp, player_hp, foe):
    current_player_hp = player_hp
    foe_hp = foe_hp_calculator(foe)
    foe_ap = foe_ap_calculator(foe)
    foe_dp = foe_dp_calculator(foe)
    current_foe_hp = foe_hp
    player_acc = playerACC
    player_eva = playerEVA
    print(f'You encountered {foe.name}!')
    if foe.bonus == 'BLESS100P':
        acc_eva_multiplier = 2
    elif foe.bonus == 'ULTIMATE':
        acc_eva_multiplier = 1.5
    else:
        acc_eva_multiplier = 1
    hit_rate = 100 - round((foe.foe_level / 2) * 100 / ((player_acc ** 0.9) * acc_eva_multiplier))
    eva_rate = 100 - round((20 + foe.foe_level) * 100 / ((player_eva ** 0.9) * acc_eva_multiplier))
    if hit_rate < 3:
        hit_rate = 2
    else:
        hit_rate = round(0.98 * hit_rate + 2)
    if eva_rate < 0:
        eva_rate = 0
    elif eva_rate > 60:
        eva_rate = 60
    print(f'Hit Rate: {hit_rate}% Dodge Rate: {eva_rate}%')
    if foe.bonus == 'DP100P':
        dp_bonus = 2
    elif foe.bonus == 'ULTIMATE':
        dp_bonus = 1.6
    else:
        dp_bonus = 1
    if foe.bonus == 'AP50P':
        ap_bonus = 1.5
    elif foe.bonus == 'ULTIMATE':
        ap_bonus = 1.3
    else:
        ap_bonus = 1
    if (player_dp * dp_bonus + dp_bonus * foe.foe_level / 5) <= foe_threshold_calculator(foe.foe_level):
        reduction_rate = 0
    else:
        reduction_rate = round(100 - ((foe_ap + (0.028 * (player_dp * dp_bonus + dp_bonus * foe.foe_level / 5))) * 100 / (foe_ap + (0.557 * (player_dp * dp_bonus + dp_bonus * foe.foe_level / 5)))))
    damage_rate = round((player_ap * ap_bonus + (0.028 * foe_dp)) * 100 / (player_ap * ap_bonus + (0.557 * foe_dp)))
    print(f'Damage Rate: {damage_rate}% Damage Reduction: {reduction_rate}%')
    battle_predictor(foe)
    drop_list(foe)
    while True:
        try:
            user_input = input("Choose:\nF:Fight!\nR:Retreat!").strip()
            if user_input == 'r':
                print('________________________________________')
                return 'retreat'
            if user_input == 'f':
                print('________________________________________')
                break
        except ValueError:
            print("Please enter R to retreat!")
        except KeyboardInterrupt:
            print("\nProgress cancelled!")
        break
    sleep_span: float = 1
    for i in range(10000):
        is_hit, is_evaded = evasion_calculator(player_acc, player_eva, foe)
        if is_hit:
            damage, is_critical, elemental_factor = player_damage_calculator(player_ap, weaponOnUse, foe)
            current_foe_hp -= damage
            if is_critical:
                if elemental_factor == 1:
                    print(f'You critically hit {foe.name} for {damage}!', end='★')
                elif 0 <= elemental_factor < 1:
                    print(f'You critically hit {foe.name} for {round(100 * (1 - elemental_factor))}% {Colors.WHITE}attenuated{Colors.END} {damage}!', end='★')
                elif elemental_factor < 0:
                    print(f'You critically hit {foe.name}, but it {Colors.RED}absorbed{Colors.END} {-damage}!', end='★')
                elif elemental_factor > 1:
                    print(f'You {Colors.GREEN}devastatingly{Colors.END} hit {foe.name} for {damage}!', end='★')
            else:
                if elemental_factor == 1:
                    print(f'You hit {foe.name} for {damage}!', end=' ')
                elif 0 <= elemental_factor < 1:
                    print(f'You hit {foe.name} for {round(100 * (1 - elemental_factor))}% {Colors.WHITE}attenuated{Colors.END} {damage}!', end=' ')
                elif elemental_factor < 0:
                    print(f'You hit {foe.name}, but it {Colors.RED}absorbed{Colors.END} {-damage}!', end=' ')
                elif elemental_factor > 1:
                    print(f'You hit {foe.name} {Colors.GREEN}powerfully{Colors.END} for {damage}!', end=' ')
            print(f'({current_foe_hp}/{foe_hp})')
        else:
            print(f'You miss! ({current_foe_hp}/{foe_hp})')
        if current_foe_hp <= 0:
            print(f'You have defeated {foe.name}!')
            exp = exp_calculator(foe)
            money_calculator(foe)
            print(f'You gained {exp} exp!')
            level_manager(exp)
            return 'win'
        time.sleep(sleep_span)
        if not is_evaded:
            damage, elemental_factor = foe_damage_calculator(foe, player_dp)
            current_player_hp -= damage
            if elemental_factor == 1:
                print(f'{foe.name} hits you for {damage}!', end=' ')
            elif 0 <= elemental_factor < 1:
                print(f'{foe.name} hits you for {round(100 * (1 - elemental_factor))}% {Colors.BLUE}attenuated{Colors.END} {damage}!!',
                      end=' ')
            elif elemental_factor < 0:
                print(f'You {Colors.GREEN}absorb{Colors.END} {round(-elemental_factor * 100)}% from {foe.name}, recovered {-damage}!!!',
                      end=' ')
            elif elemental_factor > 1:
                print(f'{foe.name} hits you {Colors.ORANGE}BRUTALLY{Colors.END} for {damage}!', end=' ')
            print(f'({current_player_hp} / {player_hp})')
        else:
            print(f'Nice dodge! ({current_player_hp}/{player_hp})')
        if current_player_hp <= 0:
            print(f'You lose...')
            return 'lose'
        time.sleep(sleep_span)
        if i < 11:
            pass
        elif i < 31:
            sleep_span = 0.5
        elif i < 61:
            sleep_span = 0.25
        elif i < 101:
            sleep_span = 0.125
        elif i < 161:
            sleep_span = 0.06
    return 'lose'


def foe_ap_calculator(foe):
    if foe.is_boss:
        multiplier = 1.2
    else:
        multiplier = 1
    foe_ap: int = math.floor((10 + 2 * foe.foe_level + math.floor(foe.foe_level ** 1.1)) * multiplier) + foe.foe_ap_modifier
    return foe_ap


def foe_dp_calculator(foe):
    if foe.is_boss:
        multiplier = 1.2
    else:
        multiplier = 1
    foe_dp: int = math.floor((10 + math.floor(foe.foe_level ** 1.1)) * multiplier) + foe.foe_dp_modifier
    return foe_dp


def foe_hp_calculator(foe):
    if foe.is_boss:
        multiplier = 1.2
    else:
        multiplier = 1
    foe_hp: int = math.floor((75 + 25 * foe.foe_level + foe.foe_level ** 1.3) * multiplier + foe.foe_hp_modifier)
    return foe_hp


def foe_threshold_calculator(foe_level):
    foe_threshold: int = math.floor(foe_level / 10) - 100
    return foe_threshold


def dexterity_calculator(player_dex):
    player_acc: int = 10 + player_dex * 4
    player_eva: int = 10 + player_dex * 2
    return player_acc, player_eva


def evasion_calculator(player_acc, player_eva, foe):
    accuracy_evasion_multiplier = 1
    if foe.bonus == 'BLESS100P':
        accuracy_evasion_multiplier = 2
    elif foe.bonus == 'ULTIMATE':
        accuracy_evasion_multiplier = 1.5
    foe_level = foe.foe_level
    is_evaded = False
    if (player_acc ** 0.9) * accuracy_evasion_multiplier * random() >= (foe_level / 2):
        is_hit = True
    else:
        if random() < 0.02:
            is_hit = True
        else:
            is_hit = False
    if (100 - round((25 + foe_level) * 100 / ((player_eva ** 0.9) * accuracy_evasion_multiplier))) > 60:
        if random() > 0.4:
            is_evaded = True
            return is_hit, is_evaded
        return is_hit, is_evaded
    if (player_eva ** 0.9) * accuracy_evasion_multiplier * random() >= 20 + foe_level:
        is_evaded = True
    return is_hit, is_evaded


def exp_calculator(foe):
    exp_bonus_multiplier = 1
    if foe.bonus == 'EXP100P':
        exp_bonus_multiplier = 2
    if foe.is_boss:
        multiplier = 2
    else:
        multiplier = 1
    exp_gained = math.floor(30 + foe.foe_level * 2 + 1.2 * foe.foe_level ** 2.1) * exp_bonus_multiplier
    return multiplier * exp_gained


def level_manager(exp):
    global level, EXP, SP
    EXP += exp

    def estimate_max_level():
        current_exp = EXP
        current_level = level
        step = max(1, current_level // 1000)
        while True:
            exp_for_step = 0
            for i in range(step):
                exp_for_step += int(10 + (current_level + i) ** 1.6)
            if current_exp >= exp_for_step:
                current_level += step
                current_exp -= exp_for_step
                step = min(step * 2, 1000000)
            else:
                if step == 1:
                    break
                step = max(1, step // 10)
        return current_level

    max_level = estimate_max_level()
    if max_level > level:
        total_exp_used = 0
        for lvl in range(level, max_level):
            exp_needed = int(10 + lvl ** 1.6)
            total_exp_used += exp_needed
        EXP -= total_exp_used
        level_up = max_level - level
        print(f'LV {level_up} UP !! LV{level}--->LV{max_level} ({EXP}/{int(10 + max_level ** 1.6)})!!')
        level = max_level
        print(f'{5 * level_up} SP Gained!')
        SP += 5 * level_up
    level = max_level


def point_allocator():
    global baseHP, baseAP, baseDP, baseDEX, baseLUC, SP
    if SP <= 0:
        print("No SP available!")
        return
    while True:
        try:
            user_input = input("Please enter your allocation strategy(1 1 0 0 0,etc):").strip()
            if not user_input:
                continue
            numbers = list(map(int, user_input.split()))
            if (len(numbers) != 5) or any(n < 0 for n in numbers) or sum(numbers) == 0:
                print("Invalid number!")
                continue
            total_ratio = sum(numbers)
            allocated = 0
            total_sp = SP
            for i in range(5):
                points_to_assign = math.floor(total_sp * numbers[i] / total_ratio)
                if i == 0:
                    baseHP += 4 * points_to_assign
                if i == 1:
                    baseAP += points_to_assign
                if i == 2:
                    baseDP += points_to_assign
                if i == 3:
                    baseDEX += points_to_assign
                if i == 4:
                    baseLUC += points_to_assign
                allocated += points_to_assign
                SP -= points_to_assign
                if SP <= 0:
                    break
            print(f'Allocation of {allocated} SP is successful!')
            break
        except ValueError:
            print("Please enter valid integer!")
        except KeyboardInterrupt:
            print("\nAllocation cancelled!")
        break


def money_calculator(foe):
    global MONEY, playerLUC
    money_bonus_multiplier = 1
    if foe.bonus == 'MONEY100P':
        money_bonus_multiplier = 2
    if foe.is_boss:
        multiplier = 2
    else:
        multiplier = 1
    base_money: int = round(75 + foe.foe_level * 5 + foe.foe_level ** 1.25)
    looted_money: int = math.floor(base_money * money_bonus_multiplier * multiplier * math.log10(playerLUC))
    MONEY += looted_money
    print(f'Looted {looted_money} money! current money: {MONEY}')


def map_bonus_generator(foe):
    bonus_indicator = random()
    if bonus_indicator < 0.035:
        foe.bonus = 'EXP100P'
    elif bonus_indicator < 0.07:
        foe.bonus = 'AP50P'
    elif bonus_indicator < 0.105:
        foe.bonus = 'DP100P'
    elif bonus_indicator < 0.14:
        foe.bonus = 'MONEY100P'
    elif bonus_indicator < 0.175:
        foe.bonus = 'CRIT30P'
    elif bonus_indicator < 0.2:
        foe.bonus = 'ULTIMATE'
    elif bonus_indicator < 0.235:
        foe.bonus = 'BLESS100P'


def get_map_bonus(foe):
    if foe.bonus == 'EXP100P':
        print(f'({foe.foe_id}){foe.name} now drops 200% EXP!')
    elif foe.bonus == 'AP50P':
        print(f'({foe.foe_id}){foe.name} is fragile!')
    elif foe.bonus == 'DP100P':
        print(f'({foe.foe_id}){foe.name} is exhausted!!')
    elif foe.bonus == 'MONEY100P':
        print(f'({foe.foe_id}){foe.name} now drops 200% MONEY!')
    elif foe.bonus == 'CRIT30P':
        print(f'({foe.foe_id}){foe.name} is exposing its weakness!')
    elif foe.bonus == 'ULTIMATE':
        print(f'({foe.foe_id}){foe.name} is at last gasp!!!')
    elif foe.bonus == 'BLESS100P':
        print(f'({foe.foe_id}){foe.name} is slow in movement!')


def reset_bonus(foe):
    foe.bonus = 'no_bonus'
    map_bonus_generator(foe)


def battle_predictor(foe):
    player_acc = playerACC
    player_eva = playerEVA
    player_ap = playerAP
    player_dp = playerDP
    player_hp = playerHP
    foe_hp = foe_hp_calculator(foe)
    win_count: int = 0
    for simulation_count in range(100):
        simulated_foe_hp = foe_hp
        simulated_player_hp = player_hp
        for i in range(10000):
            is_hit, is_evaded = evasion_calculator(player_acc, player_eva, foe)
            if is_hit:
                damage, is_critical, elemental = player_damage_calculator(player_ap, weaponOnUse, foe)
                simulated_foe_hp -= damage
            if simulated_foe_hp <= 0:
                win_count += 1
                break
            if not is_evaded:
                damage, elemental = foe_damage_calculator(foe, player_dp)
                simulated_player_hp -= damage
            if simulated_player_hp <= 0:
                break
            if i > 5000:
                print(f"{Colors.PURPLE}The battle will take too much time{Colors.END}")
                return
    if win_count > 95:
        print(f"{Colors.GREEN}Victory is assured!{Colors.END}")
    elif win_count > 75:
        print(f"{Colors.BLUE}You are likely to win this{Colors.END}")
    elif win_count > 55:
        print(f"{Colors.CYAN}This seems like a fair fight{Colors.END}")
    elif win_count > 25:
        print(f"{Colors.YELLOW}You face a challenge{Colors.END}")
    elif win_count > 5:
        print(f"{Colors.ORANGE}Your opponent is too powerful{Colors.END}")
    else:
        print(f"{Colors.RED}The battle looks impossible{Colors.END}")


def switch_to_gear(equipment, item_type):
    global weaponOnUse, torsoOnUse, legOnUse, gloveOnUse, footOnUse, shieldOnUse
    if item_type == 'w':
        temp_element = equipment.element
        if not temp_element == weaponOnUse.element:
            print(f'weapon element: {weaponOnUse.element}({100 * weaponOnUse.element_percentage}%) ----> {equipment.element}({100 * equipment.element_percentage}%)')
        weaponOnUse = equipment
    elif item_type == 't':
        torsoOnUse = equipment
    elif item_type == 'l':
        legOnUse = equipment
    elif item_type == 'h':
        gloveOnUse = equipment
    elif item_type == 'f':
        footOnUse = equipment
    elif item_type == 's':
        shieldOnUse = equipment
    temp_hp, temp_ap, temp_dp, temp_dex, temp_luc = stats_calculator()
    if not playerHP == temp_hp:
        print(f'HP: {playerHP} ----> {temp_hp}')
    if not playerAP == temp_ap:
        print(f'AP: {playerAP} ----> {temp_ap}')
    if not playerDP == temp_dp:
        print(f'DP: {playerDP} ----> {temp_dp}')
    if not playerDEX == temp_dex:
        print(f'DEX: {playerDEX} ----> {temp_dex}')
    if not playerLUC == temp_luc:
        print(f'LUC: {playerLUC} ----> {temp_luc}')
    resistance_count = resis_count
    for item_info in [gloveOnUse, shieldOnUse, legOnUse, torsoOnUse, shieldOnUse, footOnUse]:
        resistance = item_info.element
        percentage = item_info.element_percentage
        if resistance != 'none':
            resistance_count[resistance] += percentage
    if not resistance_count['piercing'] == piercingRESIS:
        print(f'piercingRESIS: {100 * piercingRESIS}% ----> {100 * resistance_count['piercing']}%')
    if not resistance_count['slashing'] == slashingRESIS:
        print(f'slashingRESIS: {100 * slashingRESIS}% ----> {100 * resistance_count['slashing']}%')
    if not resistance_count['bludgeoning'] == bludgeoningRESIS:
        print(f'bludgeoningRESIS: {100 * bludgeoningRESIS}% ----> {100 * resistance_count['bludgeoning']}%')
    if not resistance_count['fire'] == fireRESIS:
        print(f'fireRESIS: {100 * fireRESIS}% ----> {100 * resistance_count['fire']}%')
    if not resistance_count['ice'] == iceRESIS:
        print(f'iceRESIS: {100 * iceRESIS}% ----> {100 * resistance_count['ice']}%')
    if not resistance_count['thunder'] == thunderRESIS:
        print(f'thunderRESIS: {100 * thunderRESIS}% ----> {100 * resistance_count['thunder']}%')
    if not resistance_count['holy'] == holyRESIS:
        print(f'holyRESIS: {100 * holyRESIS}% ----> {100 * resistance_count['holy']}%')
    if not resistance_count['dark'] == darkRESIS:
        print(f'darkRESIS: {100 * darkRESIS}% ----> {100 * resistance_count['dark']}%')


def stats_calculator():
    temp_hp = round(sum([baseHP, weaponOnUse.base_stats1, torsoOnUse.base_stats1, legOnUse.base_stats1, gloveOnUse.base_stats1, shieldOnUse.base_stats1, footOnUse.base_stats1]) * sum([weaponOnUse.multiplier1, torsoOnUse.multiplier1, legOnUse.multiplier1, gloveOnUse.multiplier1, shieldOnUse.multiplier1, footOnUse.multiplier1], 1))
    temp_ap = round(sum([baseAP, weaponOnUse.base_stats2, torsoOnUse.base_stats2, legOnUse.base_stats2, gloveOnUse.base_stats2, shieldOnUse.base_stats2, footOnUse.base_stats2]) * sum([weaponOnUse.multiplier2, torsoOnUse.multiplier2, legOnUse.multiplier2, gloveOnUse.multiplier2, shieldOnUse.multiplier2, footOnUse.multiplier2], 1))
    temp_dp = round(sum([baseDP, weaponOnUse.base_stats3, torsoOnUse.base_stats3, legOnUse.base_stats3, gloveOnUse.base_stats3, shieldOnUse.base_stats3, footOnUse.base_stats3]) * sum([weaponOnUse.multiplier3, torsoOnUse.multiplier3, legOnUse.multiplier3, gloveOnUse.multiplier3, shieldOnUse.multiplier3, footOnUse.multiplier3], 1))
    temp_dex = round(sum([baseDEX, weaponOnUse.base_stats4, torsoOnUse.base_stats4, legOnUse.base_stats4, gloveOnUse.base_stats4, shieldOnUse.base_stats4, footOnUse.base_stats4]) * sum([weaponOnUse.multiplier4, torsoOnUse.multiplier4, legOnUse.multiplier4, gloveOnUse.multiplier4, shieldOnUse.multiplier4, footOnUse.multiplier4], 1))
    temp_luc = round(sum([baseLUC, weaponOnUse.base_stats5, torsoOnUse.base_stats5, legOnUse.base_stats5, gloveOnUse.base_stats5, shieldOnUse.base_stats5, footOnUse.base_stats5]) * sum([weaponOnUse.multiplier5, torsoOnUse.multiplier5, legOnUse.multiplier5, gloveOnUse.multiplier5, shieldOnUse.multiplier5, footOnUse.multiplier5], 1))
    return temp_hp, temp_ap, temp_dp, temp_dex, temp_luc


def refresh_player():
    global playerHP, playerAP, playerDP, playerDEX, playerLUC, piercingRESIS, slashingRESIS, bludgeoningRESIS, fireRESIS, iceRESIS, thunderRESIS, holyRESIS, darkRESIS
    playerHP, playerAP, playerDP, playerDEX, playerLUC = stats_calculator()
    resistance_count = resis_count
    for item_info in [gloveOnUse, shieldOnUse, legOnUse, torsoOnUse, shieldOnUse, footOnUse]:
        resistance = item_info.element
        percentage = item_info.element_percentage
        if resistance != 'none':
            resistance_count[resistance] += percentage
    piercingRESIS = resistance_count['piercing']
    slashingRESIS = resistance_count['slashing']
    bludgeoningRESIS = resistance_count['bludgeoning']
    fireRESIS = resistance_count['fire']
    iceRESIS = resistance_count['ice']
    thunderRESIS = resistance_count['thunder']
    holyRESIS = resistance_count['holy']
    darkRESIS = resistance_count['dark']


def drop_manager(foe):
    drop_chance = 0.12 * (foe.foe_level ** -0.1) * math.log(80 * playerLUC, 800)
    if foe.is_boss:
        drop_chance *= 6
    if drop_chance > 1:
        drop_chance = 1
    elif drop_chance < 0:
        drop_chance = 0
    if random() < drop_chance:
        count = 0
        while True:
            r = math.ceil(3 * random())
            try:
                if r == 1 and not get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).gotten:
                    get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).gotten = True
                    print(f'You got {Colors.UNDERLINE}{foe.drop1}{Colors.END} from {foe.name}!!!')
                    return
                r = 2
                if r == 2 and not get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).gotten:
                    get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).gotten = True
                    print(f'You got {Colors.UNDERLINE}{foe.drop2}{Colors.END} from {foe.name}!!!')
                    return
                r = 3
                if r == 3 and not get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten:
                    get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten = True
                    print(f'You got {Colors.UNDERLINE}{foe.drop3}{Colors.END} from {foe.name}!!!')
                    return
                elif r == 3 and get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten:
                    continue
                return
            except AttributeError:
                if r == 1:
                    return
                count += 1
                if count > 50:
                    return
                continue


def drop_list(foe):
    try:
        if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).gotten:
            print(f'-----------------------\n{foe.drop1} {Colors.GREEN}√{Colors.END}', end=' ')
        else:
            print(f'-----------------------\n ???', end='   ')
    except AttributeError:
        print(f'-----------------------\n       None       \n-----------------------')
        return
    try:
        if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).gotten:
            print(f'{foe.drop2} {Colors.GREEN}√{Colors.END}', end=' ')
        else:
            print(f' ???', end='   ')
    except AttributeError:
        print(f'\n-----------------------')
        return
    try:
        if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten:
            print(f'{foe.drop3} {Colors.GREEN}√{Colors.END}\n-----------------------')
        else:
            print(f' ???\n-----------------------')
    except AttributeError:
        print(f'\n-----------------------')


def show_gear_info(equipment, item_type):
    print('________________________________________')
    if item_type == 'w':
        print(f'current: {equipment.name}\nelement: {equipment.element}({100 * equipment.element_percentage}%)')
    else:
        print(f'current: {equipment.name}\nresistance: {equipment.element}({100 * equipment.element_percentage}%)')
    gear_info(equipment)


def gear_info(equipment):
    for i in range(1, 6):
        attr_name = f'base_stats{i}'
        attr_name2 = f'multiplier{i}'
        value = getattr(equipment, attr_name)
        value2 = getattr(equipment, attr_name2)
        if value != 0:
            if i == 1:
                print(f"HP+{value} ", end='  ')
            elif i == 2:
                print(f"AP+{value} ", end='  ')
            elif i == 3:
                print(f"DP+{value} ", end='  ')
            elif i == 4:
                print(f"DEX+{value} ", end='  ')
            elif i == 5:
                print(f"LUC+{value} ", end='  ')
        if value2 != 0:
            if i == 1:
                print(f"HP×{round(100 * (1 + value2))}%")
            elif i == 2:
                print(f"AP×{round(100 * (1 + value2))}%")
            elif i == 3:
                print(f"DP×{round(100 * (1 + value2))}%")
            elif i == 4:
                print(f"DEX×{round(100 * (1 + value2))}%")
            elif i == 5:
                print(f"LUC×{round(100 * (1 + value2))}%")
        elif value != 0 and value2 == 0:
            print('')
    print('________________________________________')


def purchase(equipment, item_type):
    global MONEY
    print('________________________________________')
    print(f'{equipment.name}: {equipment.element}({100 * equipment.element_percentage}%)')
    gear_info(equipment)
    target = input(f"Do you want to buy {equipment.name} and equip it immediately? Cost:{equipment.price} Gold:{MONEY}\n[Y/N]")
    if target == 'y' and equipment.price <= MONEY:
        equipment.gotten = True
        MONEY -= equipment.price
        switch_to_gear(equipment, item_type)
        print(f'Switched to {equipment.name} successfully!')
    elif target == 'y' and equipment.price > MONEY:
        print("You don't have enough GOLD!")
    elif target == 'n':
        pass
    print('________________________________________')
    return


def list_gear(item_dict):
    for key in sorted(item_dict.keys()):
        data = item_dict[key]
        if (not data.gotten) and data.price == 0:
            blank = ''
            print(f'({data.num}) ???{blank:15}×| ???')
            continue
        elif (not data.gotten) and data.price != 0:
            print(f'({data.num}){data.name:19}×|', end='')
        elif data in [weaponOnUse, legOnUse, torsoOnUse, footOnUse, shieldOnUse, gloveOnUse]:
            print(f'({data.num}){data.name:19}{Colors.BOLD}E{Colors.END}|', end='')
        else:
            print(f'({data.num}){data.name:19}√|', end='')
        for i in range(1, 6):
            attr_name = f'base_stats{i}'
            attr_name2 = f'multiplier{i}'
            value = getattr(data, attr_name)
            value2 = getattr(data, attr_name2)
            if value != 0:
                if i == 1:
                    print(f"HP+{value} ", end=' ')
                elif i == 2:
                    print(f"AP+{value} ", end=' ')
                elif i == 3:
                    print(f"DP+{value} ", end=' ')
                elif i == 4:
                    print(f"DEX+{value} ", end=' ')
                elif i == 5:
                    print(f"LUC+{value} ", end=' ')
            if value2 != 0:
                if i == 1:
                    print(f"HP×{round(100 * (1 + value2))}%", end='  ')
                elif i == 2:
                    print(f"AP×{round(100 * (1 + value2))}%", end='  ')
                elif i == 3:
                    print(f"DP×{round(100 * (1 + value2))}%", end='  ')
                elif i == 4:
                    print(f"DEX×{round(100 * (1 + value2))}%", end='  ')
                elif i == 5:
                    print(f"LUC×{round(100 * (1 + value2))}%", end='  ')
        if (not data.gotten) and data.price != 0:
            if data.price > MONEY:
                print(f'{Colors.RED}€:{data.price} Gold{Colors.END}')
            else:
                print(f'{Colors.GREEN}€:{data.price} Gold{Colors.END}')
        else:
            print('')
    print('________________________________________')


def enter_shop(listed, item, target):
    if get_entity_by_id(listed, item).gotten:
        switch_to_gear(get_entity_by_id(listed, item), target)
        print(f'Switched to {get_entity_by_id(listed, item).name} successfully!')
    elif get_entity_by_id(listed, item).price != 0:
        purchase(get_entity_by_id(listed, item), target)
    else:
        print("You don't have that unknown equipment!")


def main_program():
    global energy, playerACC, playerEVA
    foe_sorted_keys = sorted(enemies_dict.keys())
    print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')
    for index, key in enumerate(foe_sorted_keys):
        map_bonus_generator(enemies_dict[key])
        get_map_bonus(enemies_dict[key])
    print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')
    while True:
        refresh_player()
        target = input("Fight: foe ID(001/002...):\nGear: W/T/L/H/F...\n").strip()
        if target == 'w':
            show_gear_info(weaponOnUse, target)
            list_gear(weapon_items)
            targeted_weapon = input("Input weapon ID you gonna swap, or purchase(001/002...):").strip()
            enter_shop(weapon_items, targeted_weapon, target)
            continue
        elif target == 't':
            show_gear_info(torsoOnUse, target)
            list_gear(torso_items)
            targeted_torso = input("Input torso equipment ID you gonna swap, or purchase(001/002...):").strip()
            enter_shop(torso_items, targeted_torso, target)
            continue
        elif target == 'l':
            show_gear_info(legOnUse, target)
            list_gear(leg_items)
            targeted_leg = input("Input leg guard ID you gonna swap, or purchase(001/002...):").strip()
            enter_shop(leg_items, targeted_leg, target)
            continue
        elif target == 'h':
            show_gear_info(gloveOnUse, target)
            list_gear(hand_items)
            targeted_hand = input("Input hand proof ID you gonna swap, or purchase(001/002...):").strip()
            enter_shop(hand_items, targeted_hand, target)
            continue
        elif target == 's':
            show_gear_info(shieldOnUse, target)
            list_gear(shield_items)
            targeted_shield = input("Input shield ID you gonna swap, or purchase(001/002...):").strip()
            enter_shop(shield_items, targeted_shield, target)
            continue
        elif target == 'f':
            show_gear_info(footOnUse, target)
            list_gear(foot_items)
            targeted_boots = input("Input foot equipment ID you gonna swap, or purchase(001/002...):").strip()
            enter_shop(foot_items, targeted_boots, target)
            continue
        playerACC, playerEVA = dexterity_calculator(playerDEX)
        temp_level = level
        battle_result = battle_simulator(playerAP, playerDP, playerHP, get_entity_by_id(enemies_dict, target))
        if battle_result == 'win':
            if get_entity_by_id(enemies_dict, target).is_boss:
                energy += 2
                print(f'Gain 2 energy! current energy: {energy}')
            else:
                energy -= 1
                print(f'Consume 1 energy,current energy: {energy}')
            drop_manager(get_entity_by_id(enemies_dict, target))
            print('________________________________________')
            if temp_level == level:
                pass
            else:
                point_allocator()
                refresh_player()
                print(f'HP:{playerHP}\nAP:{playerAP}\nDP:{playerDP}\nDEX:{playerDEX}\nLUC:{playerLUC}')
                reset_bonus(get_entity_by_id(enemies_dict, target))
        elif battle_result == 'lose':
            energy -= 3
            print(f'Lose 3 energy...current energy: {energy}')
        else:
            continue
        if energy <= 0:
            print("You run out of energy!")
            print(f'Score: Highest LEVEL: {level} !\n')
            break
        print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')
        for index, key in enumerate(foe_sorted_keys):
            get_map_bonus(enemies_dict[key])
        print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')


if __name__ == '__main__':
    main_program()
