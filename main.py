import math
import re
import time
import os
from random import random
import pickle
from pathlib import Path
from datetime import datetime


from foe import enemies_dict
from color import Colors
from language import Language, pad_chinese_text
from leg import leg_items
from torso import torso_items
from weapon import weapon_items
from shield import shield_items
from hand import hand_items
from foot import foot_items
from accessory import accessory_items

all_dicts = [enemies_dict, weapon_items, torso_items, leg_items, hand_items, shield_items, foot_items, accessory_items]
i18n = Language()


base_energy: int = 0
energy: int = 0
level: int = 0
playerHP: int = 0
playerAP: int = 0
playerDP: int = 0
playerDEX: int = 0
playerLUC: int = 0
weaponOnUse = weapon_items.get('000')
torsoOnUse = torso_items.get('000')
gloveOnUse = hand_items.get('000')
legOnUse = leg_items.get('000')
shieldOnUse = shield_items.get('000')
footOnUse = foot_items.get('000')
acc1OnUse = accessory_items.get('000')
acc2OnUse = accessory_items.get('000')
acc3OnUse = accessory_items.get('000')
acc4OnUse = accessory_items.get('000')
acc5OnUse = accessory_items.get('000')
acc6OnUse = accessory_items.get('000')
slot1 = 0
slot2 = 2000
slot3 = 20000
slot4 = 200000
slot5 = 2000000
slot6 = 20000000

baseHP: int = 0
baseAP: int = 0
baseDP: int = 0
baseDEX: int = 0
baseLUC: int = 0
piercingRESIS: float = 0
slashingRESIS: float = 0
bludgeoningRESIS: float = 0
fireRESIS: float = 0
iceRESIS: float = 0
thunderRESIS: float = 0
holyRESIS: float = 0
darkRESIS: float = 0

SP: int = 0
EXP: int = 0
MONEY: int = 0
criticalChance: float = 0.1
criticalDamage: float = 1.5
bossDefeated = []
bonusEXP = 0


allocation_after_battle = True
autoAllocationStrategy = '0 0 0 0 0'
languages = 'english'


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
    if foe.is_boss:
        print(i18n.t('You encountered') + f' LV{foe.foe_level} {i18n.t(foe.name)}! {Colors.RED}(Boss){Colors.END}')
    else:
        print(i18n.t('You encountered') + f' LV{foe.foe_level} {i18n.t(foe.name)}!')
    hit_rate, eva_rate = evasion_calculator(foe)
    print(i18n.t('Hit Rate:') + f' {round(100 * hit_rate)}% ' + i18n.t('Dodge Rate:') + f' {round(100 * eva_rate)}%')
    if foe.bonus == 'DP100P':
        dp_bonus = 2
    elif foe.bonus == 'ULTIMATE':
        dp_bonus = 1.5
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
    print(i18n.t('Damage Rate:') + f' {damage_rate}% ' + i18n.t('Damage Reduction:') + f' {reduction_rate}%')
    battle_predictor(foe)
    drop_list(foe)
    while True:
        try:
            user_input = input(i18n.t("Choose: ") + "\n" + i18n.t("F:Fight!") + "\n" + i18n.t("R:Retreat!")).strip()
            if user_input == 'r':
                print('________________________________________')
                return 'retreat'
            if user_input == 'f':
                print('________________________________________')
                break
        except ValueError:
            print(i18n.t("Please enter F to fight, or R to retreat!"))
        except KeyboardInterrupt:
            print("\n" + i18n.t("Progress cancelled!"))
        break
    sleep_span: float = 1
    for i in range(10000):
        if random() < hit_rate:
            damage, is_critical, elemental_factor = player_damage_calculator(player_ap, weaponOnUse, foe)
            current_foe_hp -= damage
            if is_critical:
                if elemental_factor == 1:
                    print(i18n.t('You critically hit') + f' {i18n.t(foe.name)} ' + i18n.t('for') + f' {damage}!', end='★')
                elif 0 <= elemental_factor < 1:
                    print(i18n.t('You critically hit') + f' {i18n.t(foe.name)} ' + i18n.t('for') + f' {round(100 * (1 - elemental_factor))}% {Colors.WHITE} ' + i18n.t('attenuated') + f' {Colors.END} {damage}!', end='★')
                elif elemental_factor < 0:
                    print(i18n.t('You critically hit') + f' {i18n.t(foe.name)}, ' + i18n.t('but it') + f' {Colors.RED}' + i18n.t('absorbed') + f'{Colors.END} {-damage}!', end='★')
                elif elemental_factor > 1:
                    print(i18n.t('You') + f' {Colors.GREEN}' + i18n.t('devastatingly') + f'{Colors.END} ' + i18n.t('hit') + f' {i18n.t(foe.name)} ' + i18n.t('for') + f' {damage}!', end='★')
            else:
                if elemental_factor == 1:
                    print(i18n.t('You hit') + f' {i18n.t(foe.name)} ' + i18n.t('for') + f' {damage}!', end=' ')
                elif 0 <= elemental_factor < 1:
                    print(i18n.t('You hit') + f' {i18n.t(foe.name)} ' + i18n.t('for') + f' {round(100 * (1 - elemental_factor))}% {Colors.WHITE} ' + i18n.t('attenuated') + f' {Colors.END} {damage}!', end=' ')
                elif elemental_factor < 0:
                    print(i18n.t('You hit') + f' {i18n.t(foe.name)}, ' + i18n.t('but it') + f' {Colors.RED}' + i18n.t('absorbed') + f'{Colors.END} {-damage}!', end=' ')
                elif elemental_factor > 1:
                    print(i18n.t('You hit') + f' {i18n.t(foe.name)} {Colors.GREEN}' + i18n.t('powerfully') + f' {Colors.END}' + i18n.t('for') + f' {damage}!', end=' ')
            print(f'({current_foe_hp}/{foe_hp})')
        else:
            print(i18n.t('You miss!') + f' ({current_foe_hp}/{foe_hp})')
        if current_foe_hp <= 0:
            print(i18n.t('You have defeated') + f' {i18n.t(foe.name)}!')
            exp = exp_calculator(foe)
            money_calculator(foe)
            print(i18n.t('You gained') + f' {exp} EXP!')
            level_manager(exp)
            return 'win'
        time.sleep(sleep_span)
        if random() >= eva_rate:
            damage, elemental_factor = foe_damage_calculator(foe, player_dp)
            current_player_hp -= damage
            if elemental_factor == 1:
                print(f'{i18n.t(foe.name)} ' + i18n.t('hits you for') + f' {damage}!', end=' ')
            elif 0 <= elemental_factor < 1:
                print(f'{i18n.t(foe.name)} ' + i18n.t('hits you for') + f' {round(100 * (1 - elemental_factor))}% {Colors.BLUE} ' + i18n.t('attenuated') + f' {Colors.END} {damage}!!',
                      end=' ')
            elif elemental_factor < 0:
                print(i18n.t('You') + f' {Colors.GREEN}'+ i18n.t('absorb') + f'{Colors.END} {round(-elemental_factor * 100)}%' + i18n.t('from') + f' {i18n.t(foe.name)}, ' + i18n.t('recovered') + f' {-damage}!!!',
                      end=' ')
            elif elemental_factor > 1:
                print(f'{i18n.t(foe.name)} ' + i18n.t('hits you') + f' {Colors.ORANGE}' + i18n.t('BRUTALLY') + f'{Colors.END} ' + i18n.t('for') + f'{damage}!', end=' ')
            print(f'({current_player_hp} / {player_hp})')
        else:
            print(i18n.t('Nice dodge!') + f' ({current_player_hp}/{player_hp})')
        if current_player_hp <= 0:
            print(i18n.t('You lose...'))
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
    level_exponent = 1.1 + (1 / 35) * math.log10(foe.foe_level)
    foe_ap: int = math.floor((10 + 1.6 * foe.foe_level + foe.foe_level ** level_exponent) * multiplier + foe.foe_ap_modifier)
    return foe_ap


def foe_dp_calculator(foe):
    if foe.is_boss:
        multiplier = 1.2
    else:
        multiplier = 1
    level_exponent = 1.1 + (1 / 35) * math.log10(foe.foe_level)
    foe_dp: int = math.floor((10 + foe.foe_level ** level_exponent) * multiplier + foe.foe_dp_modifier)
    return foe_dp


def foe_hp_calculator(foe):
    if foe.is_boss:
        multiplier = 1.2
    else:
        multiplier = 1
    level_exponent = 1.3 + (1/35) * math.log10(foe.foe_level)
    foe_hp: int = math.floor((75 + 20 * foe.foe_level + foe.foe_level ** level_exponent) * multiplier + foe.foe_hp_modifier)
    return foe_hp


def foe_threshold_calculator(foe_level):
    foe_threshold: int = math.floor(foe_level / 10) - 100
    return foe_threshold


def evasion_calculator(foe):
    accuracy_evasion_multiplier = 1
    if foe.bonus == 'BLESS100P':
        accuracy_evasion_multiplier = 1.5
    elif foe.bonus == 'ULTIMATE':
        accuracy_evasion_multiplier = 1.2
    foe_level = foe.foe_level
    base_ratio = (playerDEX * accuracy_evasion_multiplier) / (foe_level + 5)
    level_factor = 1.0 + 0.1 * math.log10(max(foe_level, 1))
    adjusted_ratio = base_ratio / level_factor
    if adjusted_ratio <= 0.7:
        if adjusted_ratio >= 0.5:
            hit_rate = 0.95 - (0.95 - 0.86) * ((0.7 - adjusted_ratio) / 0.2)
        else:
            hit_rate = 0.86 - (0.86 - 0.05) * ((0.5 - adjusted_ratio) / 0.5)
            hit_rate = max(0.05, hit_rate)
    elif adjusted_ratio <= 1.0:
        hit_rate = 0.95
    elif adjusted_ratio <= 2.0:
        hit_rate = 0.95 + 0.05 * ((adjusted_ratio - 1.0) / 1.0)
    else:
        hit_rate = 1.0
    hit_rate = max(0.05, min(1.0, hit_rate))
    if adjusted_ratio <= 0.7:
        if adjusted_ratio >= 0.5:
            dodge_rate = 0.14 * ((adjusted_ratio - 0.5) / 0.2)
        else:
            dodge_rate = 0.0
    elif adjusted_ratio <= 1.0:
        dodge_rate = 0.14
    elif adjusted_ratio <= 2.0:
        dodge_rate = 0.14 + 0.26 * ((adjusted_ratio - 1.0) / 1.0)
    elif adjusted_ratio <= 4.0:
        dodge_rate = 0.4 + 0.3 * ((adjusted_ratio - 2.0) / 2.0)
    else:
        dodge_rate = 0.7
    dodge_rate = max(0.0, min(0.7, dodge_rate))
    return round(hit_rate, 4), round(dodge_rate, 4)


def exp_calculator(foe):
    exp_bonus_multiplier = 1
    if foe.bonus == 'EXP100P':
        exp_bonus_multiplier = 2
    if foe.is_boss:
        multiplier = 2
    else:
        multiplier = 1
    exp_gained = math.floor((30 + foe.foe_level * 2 + 1.2 * foe.foe_level ** 2.1) * exp_bonus_multiplier * (1 + bonusEXP / 100))
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
        print(f'LV {level_up} ' + i18n.t('UP') + f' !! LV{level}--->LV{max_level} ({EXP}/{int(10 + max_level ** 1.6)})!!')
        level = max_level
        print(f'{Colors.GREEN}{5 * level_up} ◆{Colors.END} ' + i18n.t('Gained!'))
        SP += 5 * level_up
    level = max_level


def point_allocator(auto, skipped):
    global baseHP, baseAP, baseDP, baseDEX, baseLUC, SP, allocation_after_battle, autoAllocationStrategy
    while True:
        try:
            if auto != '0 0 0 0 0' and skipped:
                user_input = auto
            elif auto == '0 0 0 0 0' and skipped:
                break
            else:
                print(i18n.t('Current:') + f'{Colors.GREEN}{SP} ◆{Colors.END}')
                print("=" * 30)
                print(i18n.t("(1 1 0 0 0,etc): Allocation strategy"))
                if allocation_after_battle:
                    after_battle_sign = "Enabled"
                else:
                    after_battle_sign = "Disabled"
                print(i18n.t("2: Toggle allocation after battle, current:") + f" {i18n.t(after_battle_sign)}")
                print(i18n.t("3: Auto allocation, current:") + f" {autoAllocationStrategy}")
                print(i18n.t("4: RETURN"))
                print("=" * 30)
                user_input = input(i18n.t("Choose: ")).strip()
                if user_input == '2' and allocation_after_battle:
                    allocation_after_battle = False
                    print(i18n.t('Allocation after battle disabled!'))
                    save_manager.save_game()
                    continue
                elif user_input == '2' and not allocation_after_battle:
                    allocation_after_battle = True
                    print(i18n.t('Allocation after battle enabled!'))
                    save_manager.save_game()
                    continue
                elif user_input == '3':
                    while True:
                        try:
                            print("=" * 30)
                            print(i18n.t("(1 1 0 0 0,etc): Auto allocation") + f" ({autoAllocationStrategy})")
                            print(i18n.t("2: Disable auto allocation"))
                            print(i18n.t("3: RETURN"))
                            print("=" * 30)
                            auto_allocation = input(i18n.t("Choose: ")).strip()
                            if auto_allocation == '2':
                                autoAllocationStrategy = '0 0 0 0 0'
                                print(i18n.t("Auto allocation disabled!"))
                            elif auto_allocation == '3':
                                user_input = 'RETURN'
                                break
                            else:
                                numbers2 = list(map(int, auto_allocation.split()))
                                if (len(numbers2) != 5) or any(n < 0 for n in numbers2) or sum(numbers2) == 0:
                                    print(i18n.t("Please enter valid FORMAT") + f"({Colors.RED}2 1 0 0 0 {Colors.END}" + i18n.t("means 66.6% points for HP and 33.3% for AP, etc)!"))
                                    continue
                                autoAllocationStrategy = auto_allocation
                                print(i18n.t("Auto allocation has been set to") + f' {autoAllocationStrategy}')
                            save_manager.save_game()
                            continue
                        except ValueError:
                            print(i18n.t("Please enter valid FORMAT") + f"({Colors.RED}2 1 0 0 0 {Colors.END}" + i18n.t("means 66.6% points for HP and 33.3% for AP, etc)!"))
                            continue
                elif user_input == '4':
                    return
                if SP <= 0:
                    print(i18n.t("No SP available!"))
                    return
                if user_input == 'RETURN':
                    continue
            numbers = list(map(int, user_input.split()))
            if (len(numbers) != 5) or any(n < 0 for n in numbers) or sum(numbers) == 0:
                print(i18n.t("Please enter valid FORMAT") + f"({Colors.RED}2 1 0 0 0 {Colors.END}" + i18n.t("means 66.6% points for HP and 33.3% for AP, etc)!"))
                continue
            total_ratio = sum(numbers)
            allocated = 0
            total_sp = SP
            for i in range(5):
                points_to_assign = math.floor(total_sp * numbers[i] / total_ratio)
                if i == 0:
                    temp_hp = baseHP + 4 * points_to_assign
                    if not baseHP == temp_hp:
                        ole_hp = baseHP
                        baseHP = temp_hp
                        print(f'HP: {ole_hp}({playerHP}) ----> {Colors.BOLD}{baseHP}({stats_calculator()[0]}){Colors.END}')
                if i == 1:
                    temp_ap = baseAP + points_to_assign
                    if not baseAP == temp_ap:
                        ole_ap = baseAP
                        baseAP = temp_ap
                        print(f'AP: {ole_ap}({playerAP}) ----> {Colors.BOLD}{baseAP}({stats_calculator()[1]}){Colors.END}')
                if i == 2:
                    temp_dp = baseDP + points_to_assign
                    if not baseDP == temp_dp:
                        ole_dp = baseDP
                        baseDP = temp_dp
                        print(f'DP: {ole_dp}({playerDP}) ----> {Colors.BOLD}{baseDP}({stats_calculator()[2]}){Colors.END}')
                if i == 3:
                    temp_dex = baseDEX + points_to_assign
                    if not baseDEX == temp_dex:
                        ole_dex = baseDEX
                        baseDEX = temp_dex
                        print(f'DEX: {ole_dex}({playerDEX}) ----> {Colors.BOLD}{baseDEX}({stats_calculator()[3]}){Colors.END}')
                if i == 4:
                    temp_luc = baseLUC + points_to_assign
                    if not baseLUC == temp_luc:
                        ole_luc = baseLUC
                        baseLUC = temp_luc
                        print(f'LUC: {ole_luc}({playerLUC}) ----> {Colors.BOLD}{baseLUC}({stats_calculator()[4]}){Colors.END}')
                allocated += points_to_assign
                SP -= points_to_assign
                if SP <= 0:
                    break
            refresh_player()
            print(i18n.t('Allocation of') + f' {Colors.GREEN}{allocated} ◆ {Colors.END}' + i18n.t('is successful!'))
            save_manager.save_game()
            break
        except ValueError:
            print(i18n.t("Please enter valid FORMAT") + f"({Colors.RED}2 1 0 0 0 {Colors.END}" + i18n.t("means 66.6% points for HP and 33.3% for AP, etc)!"))
            continue
        except KeyboardInterrupt:
            print("\n" + i18n.t("Allocation cancelled!"))
            continue


def money_calculator(foe):
    global MONEY, playerLUC
    money_bonus_multiplier = 1
    if foe.bonus == 'MONEY100P':
        money_bonus_multiplier = 2
    if foe.is_boss:
        multiplier = 2
    else:
        multiplier = 1
    base_money: int = round(75 + foe.foe_level * 16 + foe.foe_level ** 1.5)
    looted_money: int = math.floor(base_money * money_bonus_multiplier * multiplier * math.log10(playerLUC))
    MONEY += looted_money
    print(i18n.t('Looted') + f' {Colors.YELLOW}{looted_money} G{Colors.END}!' + i18n.t("Current:") + f'{Colors.YELLOW}{MONEY} G{Colors.END}')


def map_bonus_generator(foe):
    bonus_indicator = random()
    if bonus_indicator < 0.02:
        foe.bonus = 'EXP100P'
    elif bonus_indicator < 0.04:
        foe.bonus = 'AP50P'
    elif bonus_indicator < 0.06:
        foe.bonus = 'DP100P'
    elif bonus_indicator < 0.08:
        foe.bonus = 'MONEY100P'
    elif bonus_indicator < 0.1:
        foe.bonus = 'CRIT30P'
    elif bonus_indicator < 0.11:
        foe.bonus = 'ULTIMATE'
    elif bonus_indicator < 0.13:
        foe.bonus = 'BLESS100P'


def get_map_bonus(foe):
    if foe.is_boss:
        boss_sign = '(BOSS)'
    else:
        boss_sign = ''
    if foe.bonus == 'EXP100P':
        print(f'({Colors.CYAN}{foe.foe_id}{Colors.END}) {Colors.BOLD}LV{foe.foe_level}{Colors.END} {i18n.t(foe.name)}{Colors.RED}{boss_sign}{Colors.END} ' + i18n.t('now drops 200% EXP!'))
    elif foe.bonus == 'AP50P':
        print(f'({Colors.CYAN}{foe.foe_id}{Colors.END}) {Colors.BOLD}LV{foe.foe_level}{Colors.END} {i18n.t(foe.name)}{Colors.RED}{boss_sign}{Colors.END} ' + i18n.t('is fragile!'))
    elif foe.bonus == 'DP100P':
        print(f'({Colors.CYAN}{foe.foe_id}{Colors.END}) {Colors.BOLD}LV{foe.foe_level}{Colors.END} {i18n.t(foe.name)}{Colors.RED}{boss_sign}{Colors.END} ' + i18n.t('is exhausted!'))
    elif foe.bonus == 'MONEY100P':
        print(f'({Colors.CYAN}{foe.foe_id}{Colors.END}) {Colors.BOLD}LV{foe.foe_level}{Colors.END} {i18n.t(foe.name)}{Colors.RED}{boss_sign}{Colors.END} ' + i18n.t('now drops 200% MONEY!'))
    elif foe.bonus == 'CRIT30P':
        print(f'({Colors.CYAN}{foe.foe_id}{Colors.END}) {Colors.BOLD}LV{foe.foe_level}{Colors.END} {i18n.t(foe.name)}{Colors.RED}{boss_sign}{Colors.END} ' + i18n.t('is exposing its weakness!'))
    elif foe.bonus == 'ULTIMATE':
        print(f'({Colors.YELLOW}{foe.foe_id}{Colors.END}) {Colors.BOLD}LV{foe.foe_level}{Colors.END} {i18n.t(foe.name)}{Colors.RED}{boss_sign}{Colors.END} ' + i18n.t('is at last gasp!!!'))
    elif foe.bonus == 'BLESS100P':
        print(f'({Colors.CYAN}{foe.foe_id}{Colors.END}) {Colors.BOLD}LV{foe.foe_level}{Colors.END} {i18n.t(foe.name)}{Colors.RED}{boss_sign}{Colors.END} ' + i18n.t('is slow in movement!'))


def reset_bonus(foe):
    foe.bonus = 'no_bonus'
    map_bonus_generator(foe)


def battle_predictor(foe):
    player_ap = playerAP
    player_dp = playerDP
    player_hp = playerHP
    foe_hp = foe_hp_calculator(foe)
    win_count: int = 0
    for simulation_count in range(100):
        simulated_foe_hp = foe_hp
        simulated_player_hp = player_hp
        for i in range(10000):
            acc_rate, eva_rate = evasion_calculator(foe)
            if random() < acc_rate:
                damage, is_critical, elemental = player_damage_calculator(player_ap, weaponOnUse, foe)
                simulated_foe_hp -= damage
            if simulated_foe_hp <= 0:
                win_count += 1
                break
            if random() >= eva_rate:
                damage, elemental = foe_damage_calculator(foe, player_dp)
                simulated_player_hp -= damage
            if simulated_player_hp <= 0:
                break
            if i > 5000:
                print(f"{Colors.PURPLE}" + i18n.t("The battle will take too much time") + f"{Colors.END}")
                return
    if win_count > 95:
        print(f"{Colors.GREEN}" + i18n.t("Victory is assured!") + f"{Colors.END}")
    elif win_count > 75:
        print(f"{Colors.BLUE}" + i18n.t("You are likely to win this") + f"{Colors.END}")
    elif win_count > 55:
        print(f"{Colors.CYAN}" + i18n.t("This seems like a fair fight") + f"{Colors.END}")
    elif win_count > 25:
        print(f"{Colors.YELLOW}" + i18n.t("You face a challenge") + f"{Colors.END}")
    elif win_count > 5:
        print(f"{Colors.ORANGE}" + i18n.t("Your opponent is too powerful") + f"{Colors.END}")
    else:
        print(f"{Colors.RED}" + i18n.t("The battle looks impossible") + f"{Colors.END}")


def switch_to_gear(equipment, item_type):
    global weaponOnUse, torsoOnUse, legOnUse, gloveOnUse, footOnUse, shieldOnUse, acc1OnUse, acc2OnUse, acc3OnUse, acc4OnUse, acc5OnUse, acc6OnUse
    if item_type == '1':
        temp_element = equipment.element
        if not temp_element == weaponOnUse.element:
            print(i18n.t('weapon element:') + f' {i18n.t(weaponOnUse.element)}({format(weaponOnUse.element_percentage, ".0%")}%) ----> {i18n.t(equipment.element)}({format(equipment.element_percentage, ".0%")}%)')
        weaponOnUse = equipment
    elif item_type == '2':
        torsoOnUse = equipment
    elif item_type == '3':
        legOnUse = equipment
    elif item_type == '4':
        gloveOnUse = equipment
    elif item_type == '5':
        shieldOnUse = equipment
    elif item_type == '6':
        footOnUse = equipment
    elif item_type == 'a1':
        acc1OnUse = equipment
    elif item_type == 'a2':
        acc2OnUse = equipment
    elif item_type == 'a3':
        acc3OnUse = equipment
    elif item_type == 'a4':
        acc4OnUse = equipment
    elif item_type == 'a5':
        acc5OnUse = equipment
    elif item_type == 'a6':
        acc6OnUse = equipment
    temp_hp, temp_ap, temp_dp, temp_dex, temp_luc = stats_calculator()
    if not playerHP == temp_hp:
        print(f'HP: {playerHP} ----> {Colors.BOLD}{temp_hp}{Colors.END}')
    if not playerAP == temp_ap:
        print(f'AP: {playerAP} ----> {Colors.BOLD}{temp_ap}{Colors.END}')
    if not playerDP == temp_dp:
        print(f'DP: {playerDP} ----> {Colors.BOLD}{temp_dp}{Colors.END}')
    if not playerDEX == temp_dex:
        print(f'DEX: {playerDEX} ----> {Colors.BOLD}{temp_dex}{Colors.END}')
    if not playerLUC == temp_luc:
        print(f'LUC: {playerLUC} ----> {Colors.BOLD}{temp_luc}{Colors.END}')
    resistance_count = {'piercing': 0, 'slashing': 0, 'bludgeoning': 0, 'fire': 0, 'ice': 0, 'thunder': 0, 'holy': 0, 'dark': 0}
    for item_info in [gloveOnUse, shieldOnUse, legOnUse, torsoOnUse, footOnUse]:
        resistance = item_info.element
        percentage = item_info.element_percentage
        if resistance != 'none':
            resistance_count[resistance] += percentage
    if not resistance_count['piercing'] == piercingRESIS:
        print(i18n.t('piercingRESIS:') + f' {100 * piercingRESIS}% ----> {100 * resistance_count['piercing']}%')
    if not resistance_count['slashing'] == slashingRESIS:
        print(i18n.t('slashingRESIS:') + f' {100 * slashingRESIS}% ----> {100 * resistance_count['slashing']}%')
    if not resistance_count['bludgeoning'] == bludgeoningRESIS:
        print(i18n.t('bludgeoningRESIS:') + f' {100 * bludgeoningRESIS}% ----> {100 * resistance_count['bludgeoning']}%')
    if not resistance_count['fire'] == fireRESIS:
        print(i18n.t('fireRESIS:') + f' {100 * fireRESIS}% ----> {100 * resistance_count['fire']}%')
    if not resistance_count['ice'] == iceRESIS:
        print(i18n.t('iceRESIS:') + f' {100 * iceRESIS}% ----> {100 * resistance_count['ice']}%')
    if not resistance_count['thunder'] == thunderRESIS:
        print(i18n.t('thunderRESIS:') + f' {100 * thunderRESIS}% ----> {100 * resistance_count['thunder']}%')
    if not resistance_count['holy'] == holyRESIS:
        print(i18n.t('holyRESIS:') + f' {100 * holyRESIS}% ----> {100 * resistance_count['holy']}%')
    if not resistance_count['dark'] == darkRESIS:
        print(i18n.t('darkRESIS:') + f' {100 * darkRESIS}% ----> {100 * resistance_count['dark']}%')
    exp_bonus = 0
    temp_energy = base_energy
    for i in [weaponOnUse, shieldOnUse, gloveOnUse, torsoOnUse, footOnUse, legOnUse, acc1OnUse, acc2OnUse, acc3OnUse,acc4OnUse, acc5OnUse, acc6OnUse]:
        for j in range(1, 5):
            attr_name = f'attri{j}'
            special_items = getattr(i, attr_name)
            if special_items.startswith("EXP"):
                match = re.search(r'\d+\.?\d*', special_items)
                exp_bonus += round(100 * float(match.group()))
            elif special_items.startswith("ENERGY"):
                match = re.search(r'\d+\.?\d*', special_items)
                temp_energy += int(match.group())
    if not exp_bonus == bonusEXP:
        print(i18n.t('EXP + ') + f' {bonusEXP}% ----> {exp_bonus}%')
    if not temp_energy == energy:
        print(f'{Colors.YELLOW}{energy} ⚡{Colors.END} ----> {Colors.YELLOW}{temp_energy} ⚡{Colors.END}')
    refresh_player()


def stats_calculator():
    temp_hp = 0
    temp_hp_multiplier = 1
    temp_ap = 0
    temp_ap_multiplier = 1
    temp_dp = 0
    temp_dp_multiplier = 1
    temp_dex = 0
    temp_dex_multiplier = 1
    temp_luc = 0
    temp_luc_multiplier = 1
    for i in [weaponOnUse, shieldOnUse, gloveOnUse, torsoOnUse, footOnUse, legOnUse, acc1OnUse, acc2OnUse, acc3OnUse, acc4OnUse, acc5OnUse, acc6OnUse]:
        temp_hp += i.base_stats1
        temp_hp_multiplier += i.multiplier1
        temp_ap += i.base_stats2
        temp_ap_multiplier += i.multiplier2
        temp_dp += i.base_stats3
        temp_dp_multiplier += i.multiplier3
        temp_dex += i.base_stats4
        temp_dex_multiplier += i.multiplier4
        temp_luc += i.base_stats5
        temp_luc_multiplier += i.multiplier5
    temp_hp = round((temp_hp + baseHP) * temp_hp_multiplier)
    temp_ap = round((temp_ap + baseAP) * temp_ap_multiplier)
    temp_dp = round((temp_dp + baseDP) * temp_dp_multiplier)
    temp_dex = round((temp_dex + baseDEX) * temp_dex_multiplier)
    temp_luc = round((temp_luc + baseLUC) * temp_luc_multiplier)
    return temp_hp, temp_ap, temp_dp, temp_dex, temp_luc


def refresh_player():
    global playerHP, playerAP, playerDP, playerDEX, playerLUC, piercingRESIS, slashingRESIS, bludgeoningRESIS, fireRESIS, iceRESIS, thunderRESIS, holyRESIS, darkRESIS, bonusEXP, energy
    playerHP, playerAP, playerDP, playerDEX, playerLUC = stats_calculator()
    resistance_count = {'piercing': 0, 'slashing': 0, 'bludgeoning': 0, 'fire': 0, 'ice': 0, 'thunder': 0, 'holy': 0, 'dark': 0}
    for item_info in [gloveOnUse, shieldOnUse, legOnUse, torsoOnUse, footOnUse]:
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
    bonusEXP = 0
    energy = base_energy
    for i in [weaponOnUse, shieldOnUse, gloveOnUse, torsoOnUse, footOnUse, legOnUse, acc1OnUse, acc2OnUse, acc3OnUse,acc4OnUse, acc5OnUse, acc6OnUse]:
        for j in range(1, 5):
            attr_name = f'attri{j}'
            special_items = getattr(i, attr_name)
            if special_items.startswith("EXP"):
                match = re.search(r'\d+\.?\d*', special_items)
                bonusEXP += round(100 * float(match.group()))
            elif special_items.startswith("ENERGY"):
                match = re.search(r'\d+\.?\d*', special_items)
                energy += int(match.group())


def drop_manager(foe):
    drop_chance = 0.15 * (foe.foe_level ** -0.1) * math.log(80 * playerLUC, 800)
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
                if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1) in accessory_items.values():
                    if r == 1 and not get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).gotten:
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).gotten = True
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).item_count += 1
                        print(i18n.t('You got') + f' {Colors.UNDERLINE}{i18n.t(foe.drop1)}{Colors.END} ' + i18n.t('from') + f'{i18n.t(foe.name)}!!!')
                        return
                    elif r == 1 and get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).item_count < get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).limit:
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).item_count += 1
                        print(i18n.t('You got') + f' {Colors.UNDERLINE}{i18n.t(foe.drop1)}{Colors.END} ' + i18n.t('from') + f'{i18n.t(foe.name)}!!!')
                        return
                else:
                    if r == 1 and not get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).gotten:
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).gotten = True
                        print(i18n.t('You got') + f' {Colors.UNDERLINE}{i18n.t(foe.drop1)}{Colors.END} ' + i18n.t('from') + f'{i18n.t(foe.name)}!!!')
                        return
                r = 2
                if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2) in accessory_items.values():
                    if r == 2 and not get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).gotten:
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).gotten = True
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).item_count += 1
                        print(i18n.t('You got') + f' {Colors.UNDERLINE}{i18n.t(foe.drop2)}{Colors.END} ' + i18n.t('from') + f'{i18n.t(foe.name)}!!!')
                        return
                    elif r == 2 and get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2),foe.drop2).item_count < get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).limit:
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).item_count += 1
                        print(i18n.t('You got') + f' {Colors.UNDERLINE}{i18n.t(foe.drop2)}{Colors.END} ' + i18n.t('from') + f'{i18n.t(foe.name)}!!!')
                        return
                else:
                    if r == 2 and not get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).gotten:
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).gotten = True
                        print(i18n.t('You got') + f' {Colors.UNDERLINE}{i18n.t(foe.drop2)}{Colors.END} ' + i18n.t('from') + f'{i18n.t(foe.name)}!!!')
                        return
                r = 3
                if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3) in accessory_items.values():
                    if r == 3 and not get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten:
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten = True
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).item_count += 1
                        print(i18n.t('You got') + f' {Colors.UNDERLINE}{i18n.t(foe.drop3)}{Colors.END} ' + i18n.t('from') + f'{i18n.t(foe.name)}!!!')
                        return
                    elif r == 3 and get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3),foe.drop3).item_count < get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).limit:
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).item_count += 1
                        print(i18n.t('You got') + f' {Colors.UNDERLINE}{i18n.t(foe.drop3)}{Colors.END} ' + i18n.t('from') + f'{i18n.t(foe.name)}!!!')
                        return
                else:
                    if r == 3 and not get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten:
                        get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten = True
                        print(i18n.t('You got') + f' {Colors.UNDERLINE}{i18n.t(foe.drop3)}{Colors.END} ' + i18n.t('from') + f'{i18n.t(foe.name)}!!!')
                        return
                if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3) in accessory_items.values():
                    if r == 3 and get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten:
                        if r == 3 and get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3),foe.drop3).item_count == get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).limit:
                            continue
                else:
                    if r == 3 and get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten:
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
            if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1) in accessory_items.values():
                print(f'-----------------------\n{i18n.t(foe.drop1)} ({get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).item_count}/{get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).limit}) {Colors.GREEN}√{Colors.END}', end=' ')
            else:
                print(f'-----------------------\n{i18n.t(foe.drop1)} {Colors.GREEN}√{Colors.END}', end=' ')
        else:
            print(f'-----------------------\n ???', end='   ')
    except AttributeError:
        print(f'-----------------------\n       None       \n-----------------------')
        return
    try:
        if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).gotten:
            if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2) in accessory_items.values():
                print(f'{i18n.t(foe.drop2)} ({get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).item_count}/{get_entity_by_name(get_dict_by_name(all_dicts, foe.drop2), foe.drop2).limit}) {Colors.GREEN}√{Colors.END}', end=' ')
            else:
                print(f'{i18n.t(foe.drop2)} {Colors.GREEN}√{Colors.END}', end=' ')
        else:
            print(f' ???', end='   ')
    except AttributeError:
        print(f'\n-----------------------')
        return
    try:
        if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop3), foe.drop3).gotten:
            if get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1) in accessory_items.values():
                print(f'{i18n.t(foe.drop1)} ({get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).item_count}/{get_entity_by_name(get_dict_by_name(all_dicts, foe.drop1), foe.drop1).limit}) {Colors.GREEN}√{Colors.END}', end=' ')
            else:
                print(f'{i18n.t(foe.drop3)} {Colors.GREEN}√{Colors.END}\n-----------------------')
        else:
            print(f' ???\n-----------------------')
    except AttributeError:
        print(f'\n-----------------------')


def show_gear_info(equipment, item_type):
    print('________________________________________')
    if item_type == '1':
        print(i18n.t('Current:') + f' {i18n.t(equipment.name)}\n' + i18n.t("Element:") + f' {i18n.t(equipment.element)}({format(equipment.element_percentage, ".0%")})')
    elif item_type in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']:
        if equipment.name == "empty":
            print(i18n.t('Current:') + f' {i18n.t(equipment.name)}\n')
        else:
            print(i18n.t('Current:') + f' {i18n.t(equipment.name)} ({equipment.item_count}/{equipment.limit})\n')
    else:
        print(i18n.t('Current:') + f' {i18n.t(equipment.name)}\n' + i18n.t("Resistance:") + f' {i18n.t(equipment.element)}({format(equipment.element_percentage, ".0%")})')
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
                print(f"HP×{format(1 + value2, ".0%")}")
            elif i == 2:
                print(f"AP×{format(1 + value2, ".0%")}")
            elif i == 3:
                print(f"DP×{format(1 + value2, ".0%")}")
            elif i == 4:
                print(f"DEX×{format(1 + value2, ".0%")}")
            elif i == 5:
                print(f"LUC×{format(1 + value2, ".0%")}")
        elif value != 0 and value2 == 0:
            print('')
    for i in range(1, 5):
        attr_name = f'attri{i}'
        special_items = getattr(equipment, attr_name)
        if special_items.startswith("EXP"):
            match = re.search(r'\d+\.?\d*', special_items)
            print(f'EXP + {round(100 * float(match.group()))}%')
        elif special_items.startswith("ENERGY"):
            match = re.search(r'\d+\.?\d*', special_items)
            print(f'ENERGY + {int(match.group())}')
    print('________________________________________')


def purchase(equipment, item_type):
    global MONEY
    print('________________________________________')
    if not item_type in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']:
        print(f'{i18n.t(equipment.name)}: {equipment.element}({format(equipment.element_percentage, ".0%")})')
    gear_info(equipment)
    if equipment.price > MONEY:
        target = input(i18n.t("Do you want to buy") + f' {i18n.t(equipment.name)} ' + i18n.t("and equip it immediately? Cost:") + f"{Colors.RED}{equipment.price} G{Colors.END} " + i18n.t("Gold:") + f"{Colors.YELLOW}{MONEY} G{Colors.END}\n[Y/N]")
    else:
        target = input(i18n.t("Do you want to buy") + f' {i18n.t(equipment.name)} ' + i18n.t("and equip it immediately? Cost:") + f"{Colors.GREEN}{equipment.price} G{Colors.END} " + i18n.t("Gold:") + f"{Colors.YELLOW}{MONEY} G{Colors.END}\n[Y/N]")
    print("=" * 30)
    if target == 'y' and equipment.price <= MONEY:
        equipment.gotten = True
        MONEY -= equipment.price
        switch_to_gear(equipment, item_type)
        print(i18n.t('Switched to ') + f'{i18n.t(equipment.name)}' + i18n.t(' successfully!'))
    elif target == 'y' and equipment.price > MONEY:
        print(i18n.t("You don't have enough GOLD!"))
    elif target == 'n':
        pass
    return


def list_gear(item_dict):
    print(i18n.t('Your GOLD:') + f'{Colors.YELLOW}{MONEY} G{Colors.END}')
    for key in sorted(item_dict.keys()):
        data = item_dict[key]
        if (not data.gotten) and data.price == 0:
            blank = ''
            print(f'({data.num}) ???{blank:15}×| ???')
            continue
        elif (not data.gotten) and data.price != 0:
            print(f'({data.num}) {pad_chinese_text(i18n.t(data.name), 19)}×|', end='')
        elif data in [weaponOnUse, legOnUse, torsoOnUse, footOnUse, shieldOnUse, gloveOnUse]:
            print(f'({data.num}) {pad_chinese_text(i18n.t(data.name), 19)}E|', end='')
        else:
            print(f'({data.num}) {pad_chinese_text(i18n.t(data.name), 19)}√|', end='')
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
                    print(f"HP×{format(1 + value2, ".0%")}", end='  ')
                elif i == 2:
                    print(f"AP×{format(1 + value2, ".0%")}", end='  ')
                elif i == 3:
                    print(f"DP×{format(1 + value2, ".0%")}", end='  ')
                elif i == 4:
                    print(f"DEX×{format(1 + value2, ".0%")}", end='  ')
                elif i == 5:
                    print(f"LUC×{format(1 + value2, ".0%")}", end='  ')
        for i in range(1, 5):
            attr_name = f'attri{i}'
            special_items = getattr(data, attr_name)
            if special_items.startswith("EXP"):
                match = re.search(r'\d+\.?\d*', special_items)
                print(f'EXP + {round(100 * float(match.group()))}%', end='  ')
            elif special_items.startswith("ENERGY"):
                match = re.search(r'\d+\.?\d*', special_items)
                print(f'ENERGY + {int(match.group())}', end='  ')
        if (not data.gotten) and data.price != 0:
            if data.price > MONEY:
                print(f'{Colors.RED}€:{data.price} G{Colors.END}')
            else:
                print(f'{Colors.GREEN}€:{data.price} G{Colors.END}')
        else:
            print('')
    print('________________________________________')


def enter_shop(listed, item, target):
    if get_entity_by_id(listed, item).gotten:
        if target in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']:
            acc_count = 0
            for i in [acc1OnUse, acc2OnUse, acc3OnUse, acc4OnUse, acc5OnUse, acc6OnUse]:
                if i == get_entity_by_id(listed, item):
                    acc_count += 1
                if (acc_count >= get_entity_by_id(listed, item).limit) or (acc_count >= get_entity_by_id(listed, item).item_count):
                    print(i18n.t("You can't equip this more than" + f"{get_entity_by_id(listed, item).item_count}" + "!"))
                    return
        switch_to_gear(get_entity_by_id(listed, item), target)
        print("=" * 30)
        print(i18n.t('Switched to ') + f'{i18n.t(get_entity_by_id(listed, item).name)}' + i18n.t(' successfully!'))
        save_manager.save_game()
    elif get_entity_by_id(listed, item).price != 0:
        purchase(get_entity_by_id(listed, item), target)
        save_manager.save_game()
    else:
        print("=" * 30)
        print(i18n.t("You don't have that unknown equipment!"))


def bonus_initialization():
    foe_sorted_keys = sorted(enemies_dict.keys())
    print('☆' * 30)
    for index, key in enumerate(foe_sorted_keys):
        map_bonus_generator(enemies_dict[key])
        get_map_bonus(enemies_dict[key])
    print('☆' * 30)
    return foe_sorted_keys


def bonus_delete():
    foe_sorted_keys = sorted(enemies_dict.keys())
    for index, key in enumerate(foe_sorted_keys):
        enemies_dict[key].bonus = 'no_bonus'


def in_game_menu():
    while True:
        print("\n" + "=" * 30)
        print(i18n.t("1: STATS"))
        print(i18n.t("2: EQUIPMENT"))
        print(i18n.t("3: RETURN"))
        print(i18n.t("4: MENU"))
        print("=" * 30)
        choice = input(i18n.t("Choose: "))
        if choice == "1":
            allocation_menu()
            continue
        elif choice == "2":
            equipment_menu()
            continue
        elif choice == "3":
            break
        elif choice == "4":
            return choice
        else:
            print(i18n.t("Invalid Choice!"))
        continue


def allocation_menu():
    print("\n" + "=" * 30)
    print(f'HP: {baseHP}({playerHP})')
    print(f'AP: {baseAP}({playerAP})')
    print(f'DP: {baseDP}({playerDP})')
    print(f'DEX:{baseDEX}({playerDEX})')
    print(f'LUC:{baseLUC}({playerLUC})')
    point_allocator(autoAllocationStrategy, False)


def accessory_menu():
    global MONEY, slot1, slot2, slot3, slot4, slot5, slot6
    while True:
        print("=" * 30)
        count = 0
        for i, current in zip([slot1, slot2, slot3, slot4, slot5, slot6], [acc1OnUse, acc2OnUse, acc3OnUse, acc4OnUse, acc5OnUse, acc6OnUse]):
            count += 1
            if i == 0:
                print(str(count) + ': ' + i18n.t("SLOT") + ' ' + str(count) + ' ' + f" {i18n.t(current.name)}")
            else:
                if MONEY > i:
                    print(str(count) + ': ' + i18n.t("SLOT") + ' ' + str(count) + ' ' + f" {Colors.GREEN}€:{i} G{Colors.END}")
                else:
                    print(str(count) + ': ' + i18n.t("SLOT") + ' ' + str(count) + ' ' + f" {Colors.RED}€:{i} G{Colors.END}")
        print(i18n.t("7: RETURN"))
        print("=" * 30)
        target = input(i18n.t("Choose: ")).strip()
        if target == '1':
            target = 'a1'
            show_gear_info(acc1OnUse, target)
            list_gear(accessory_items)
            targeted_acc = input(i18n.t("Input accessory ID you gonna swap, or purchase(001/002...):")).strip()
            enter_shop(accessory_items, targeted_acc, target)
            continue
        elif target == '2':
            if slot2 == 0:
                target = 'a2'
                show_gear_info(acc2OnUse, target)
                list_gear(accessory_items)
                targeted_acc = input(i18n.t("Input accessory ID you gonna swap, or purchase(001/002...):")).strip()
                enter_shop(accessory_items, targeted_acc, target)
            else:
                if MONEY >= slot2:
                    print(i18n.t("Do you want to unlock SLOT") + ' 2 ?' + f" {Colors.GREEN}€:{slot2} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                else:
                    print(i18n.t("Do you want to unlock SLOT") + ' 2 ?' + f" {Colors.RED}€:{slot2} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                choose = input("[Y/N]").strip()
                if choose == 'y':
                    if MONEY > slot2:
                        MONEY -= slot2
                        slot2 = 0
                        save_manager.save_game()
                        print(i18n.t("SLOT 2 is unlocked!"))
                    else:
                        print(i18n.t("Short of GOLD!"))
            continue
        elif target == '3':
            if slot3 == 0:
                target = 'a3'
                show_gear_info(acc3OnUse, target)
                list_gear(accessory_items)
                targeted_acc = input(i18n.t("Input accessory ID you gonna swap, or purchase(001/002...):")).strip()
                enter_shop(accessory_items, targeted_acc, target)
            else:
                if MONEY >= slot3:
                    print(i18n.t("Do you want to unlock SLOT") + ' 3 ?' + f" {Colors.GREEN}€:{slot3} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                else:
                    print(i18n.t("Do you want to unlock SLOT") + ' 3 ?' + f" {Colors.RED}€:{slot3} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                choose = input("[Y/N]").strip()
                if choose == 'y':
                    if MONEY > slot3:
                        MONEY -= slot3
                        slot3 = 0
                        save_manager.save_game()
                        print(i18n.t("SLOT 3 is unlocked!"))
                    else:
                        print(i18n.t("Short of GOLD!"))
            continue
        elif target == '4':
            if slot4 == 0:
                target = 'a4'
                show_gear_info(acc4OnUse, target)
                list_gear(accessory_items)
                targeted_acc = input(i18n.t("Input accessory ID you gonna swap, or purchase(001/002...):")).strip()
                enter_shop(accessory_items, targeted_acc, target)
            else:
                if MONEY >= slot4:
                    print(i18n.t("Do you want to unlock SLOT") + ' 4 ?' + f" {Colors.GREEN}€:{slot4} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                else:
                    print(i18n.t("Do you want to unlock SLOT") + ' 4 ?' + f" {Colors.RED}€:{slot4} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                choose = input("[Y/N]").strip()
                if choose == 'y':
                    if MONEY > slot4:
                        MONEY -= slot4
                        slot4 = 0
                        save_manager.save_game()
                        print(i18n.t("SLOT 4 is unlocked!"))
                    else:
                        print(i18n.t("Short of GOLD!"))
            continue
        elif target == '5':
            if slot5 == 0:
                target = 'a5'
                show_gear_info(acc5OnUse, target)
                list_gear(accessory_items)
                targeted_acc = input(i18n.t("Input accessory ID you gonna swap, or purchase(001/002...):")).strip()
                enter_shop(accessory_items, targeted_acc, target)
            else:
                if MONEY >= slot5:
                    print(i18n.t("Do you want to unlock SLOT") + ' 5 ?' + f" {Colors.GREEN}€:{slot5} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                else:
                    print(i18n.t("Do you want to unlock SLOT") + ' 5 ?' + f" {Colors.RED}€:{slot5} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                choose = input("[Y/N]").strip()
                if choose == 'y':
                    if MONEY > slot5:
                        MONEY -= slot5
                        slot5 = 0
                        save_manager.save_game()
                        print(i18n.t("SLOT 5 is unlocked!"))
                    else:
                        print(i18n.t("Short of GOLD!"))
            continue
        elif target == '6':
            if slot6 == 0:
                target = 'a6'
                show_gear_info(acc6OnUse, target)
                list_gear(accessory_items)
                targeted_acc = input(i18n.t("Input accessory ID you gonna swap, or purchase(001/002...):")).strip()
                enter_shop(accessory_items, targeted_acc, target)
            else:
                if MONEY >= slot6:
                    print(i18n.t("Do you want to unlock SLOT") + ' 6 ?' + f" {Colors.GREEN}€:{slot6} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                else:
                    print(i18n.t("Do you want to unlock SLOT") + ' 6 ?' + f" {Colors.RED}€:{slot6} G{Colors.END} " + i18n.t("Current:") + f' {Colors.YELLOW}{MONEY} G{Colors.END}')
                choose = input("[Y/N]").strip()
                if choose == 'y':
                    if MONEY > slot6:
                        MONEY -= slot6
                        slot6 = 0
                        save_manager.save_game()
                        print(i18n.t("SLOT 6 is unlocked!"))
                    else:
                        print(i18n.t("Short of GOLD!"))
            continue
        elif target == '7':
            break
        else:
            print(i18n.t("Invalid Choice!"))
            continue


def equipment_menu():
    while True:
        print("=" * 30)
        print(i18n.t("1: WEAPON") + " " + f"{i18n.t(weaponOnUse.name)}")
        print(i18n.t("2: TORSO") + "  " + f"{i18n.t(torsoOnUse.name)}")
        print(i18n.t("3: LEG") + "    " + f"{i18n.t(legOnUse.name)}")
        print(i18n.t("4: HAND") + "   " + f"{i18n.t(gloveOnUse.name)}")
        print(i18n.t("5: SHIELD") + " " + f"{i18n.t(shieldOnUse.name)}")
        print(i18n.t("6: FOOT") + "   " + f"{i18n.t(footOnUse.name)}")
        print(i18n.t("7: ACCESSORY"))
        print(i18n.t("8: RETURN"))
        print("=" * 30)
        target = input(i18n.t("Choose: ")).strip()
        if target == '1':
            show_gear_info(weaponOnUse, target)
            list_gear(weapon_items)
            targeted_weapon = input(i18n.t("Input weapon ID you gonna swap, or purchase(001/002...):")).strip()
            enter_shop(weapon_items, targeted_weapon, target)
            continue
        elif target == '2':
            show_gear_info(torsoOnUse, target)
            list_gear(torso_items)
            targeted_torso = input(i18n.t("Input torso equipment ID you gonna swap, or purchase(001/002...):")).strip()
            enter_shop(torso_items, targeted_torso, target)
            continue
        elif target == '3':
            show_gear_info(legOnUse, target)
            list_gear(leg_items)
            targeted_leg = input(i18n.t("Input leg guard ID you gonna swap, or purchase(001/002...):")).strip()
            enter_shop(leg_items, targeted_leg, target)
            continue
        elif target == '4':
            show_gear_info(gloveOnUse, target)
            list_gear(hand_items)
            targeted_hand = input(i18n.t("Input hand proof ID you gonna swap, or purchase(001/002...):")).strip()
            enter_shop(hand_items, targeted_hand, target)
            continue
        elif target == '5':
            show_gear_info(shieldOnUse, target)
            list_gear(shield_items)
            targeted_shield = input(i18n.t("Input shield ID you gonna swap, or purchase(001/002...):")).strip()
            enter_shop(shield_items, targeted_shield, target)
            continue
        elif target == '6':
            show_gear_info(footOnUse, target)
            list_gear(foot_items)
            targeted_boots = input(i18n.t("Input foot equipment ID you gonna swap, or purchase(001/002...):")).strip()
            enter_shop(foot_items, targeted_boots, target)
            continue
        elif target == '7':
            accessory_menu()
            continue
        elif target == '8':
            break
        else:
            print(i18n.t("Invalid Choice!"))
            continue


def game_over():
    while True:
        print("\n" + "=" * 30)
        print(i18n.t("1: NEW RUN"))
        print(i18n.t("2: EQUIPMENT"))
        print(i18n.t("3: MENU"))
        print("=" * 30)
        choice = input(i18n.t("Choose: "))
        if choice == "1":
            revive()
            save_manager.save_game()
            main_program()
        elif choice == "2":
            equipment_menu()
            if energy > 0:
                return choice
        elif choice == "3":
            return choice
        else:
            print(i18n.t("Invalid Choice!"))
        continue


def player_action():
    global base_energy, bossDefeated
    print("")
    bonus_delete()
    foe_sorted_keys = bonus_initialization()
    while True:
        refresh_player()
        if energy <= 0:
            print(i18n.t("You run out of" + f'{Colors.YELLOW} ⚡{Colors.END}' + "!"))
            if game_over() == '3':
                save_manager.save_game()
                break
        print(i18n.t('Your energy: ') + f'{Colors.YELLOW}{energy} ⚡{Colors.END}  ' + i18n.t('Your Level: ') + f'{Colors.BOLD}LV{level}{Colors.END}')
        print("=" * 30)
        print(i18n.t("FOE ID(001/002): FIGHT") + '\n' + i18n.t("2: OPTION"))
        print("=" * 30)
        target = input(i18n.t("Choose: ")).strip()
        try:
            if target == '2':
                choose = in_game_menu()
                if choose == "4":
                    save_manager.save_game()
                    break
                continue
            temp_level = level
            if get_entity_by_id(enemies_dict, target).foe_id in bossDefeated:
                print(i18n.t('Boss can only be defeated once in each round of the game!'))
                continue
            battle_result = battle_simulator(playerAP, playerDP, playerHP, get_entity_by_id(enemies_dict, target))
            if battle_result == 'win':
                if get_entity_by_id(enemies_dict, target).is_boss:
                    base_energy += 2
                    bossDefeated.append(get_entity_by_id(enemies_dict, target).foe_id)
                    refresh_player()
                    print(i18n.t('Gain') + f' 2{Colors.YELLOW} ⚡{Colors.END}! ' + i18n.t('Current:') + f'{energy}{Colors.YELLOW} ⚡{Colors.END}')
                else:
                    base_energy -= 1
                    refresh_player()
                    print(i18n.t('Consume') + f' 1{Colors.YELLOW} ⚡{Colors.END}! ' + i18n.t('Current:') + f'{energy}{Colors.YELLOW} ⚡{Colors.END}')
                drop_manager(get_entity_by_id(enemies_dict, target))
                print('________________________________________')
                save_manager.save_game()
                if temp_level == level:
                    pass
                else:
                    if autoAllocationStrategy != '0 0 0 0 0':
                        point_allocator(autoAllocationStrategy, True)
                    elif allocation_after_battle:
                        point_allocator('0 0 0 0 0', False)
                if get_entity_by_id(enemies_dict, target).foe_id in bossDefeated:
                    get_entity_by_id(enemies_dict, target).foe_bonus = 'no_bonus'
                else:
                    reset_bonus(get_entity_by_id(enemies_dict, target))
                save_manager.save_game()
            elif battle_result == 'lose':
                base_energy -= 3
                refresh_player()
                print(i18n.t('Lose') + f' 3{Colors.YELLOW} ⚡{Colors.END}! ' + i18n.t('Current:') + f'{energy}{Colors.YELLOW} ⚡{Colors.END}')
                save_manager.save_game()
            else:
                save_manager.save_game()
                continue
            refresh_player()
            if energy <= 0:
                print(i18n.t("You run out of energy!"))
                print(i18n.t('Score: Highest LEVEL: ') + f'{Colors.CYAN}{level}{Colors.END} !')
                save_manager.save_game()
                if game_over() == '3':
                    save_manager.save_game()
                    break
            print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')
            for index, key in enumerate(foe_sorted_keys):
                get_map_bonus(enemies_dict[key])
            print('☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆')
        except AttributeError:
            print(i18n.t('Please enter ID to fight') + f'({Colors.RED}001{Colors.END}' + i18n.t('for the first enemy)'))
            continue


def revive():
    global level, baseHP, baseAP, baseDP, baseDEX, baseLUC, SP, MONEY, base_energy, EXP, bossDefeated
    level = 1
    baseHP = 100
    baseAP, baseDP = 15, 15
    baseDEX, baseLUC = 5, 5
    SP, MONEY, EXP = 0, 0, 0
    base_energy = 25
    bossDefeated = []


def main_program():
    player_action()


def show_menu():
    file_path = os.path.join("saves", "save.dat")
    if os.path.isfile(file_path):
        print("\n" + "=" * 30)
        print(i18n.t("1: CONTINUE"))
        print(i18n.t("2: NEW RUN"))
        print(i18n.t("3: SETTINGS"))
        print(i18n.t("4: EXIT"))
        print("=" * 30)
        return True
    else:
        print("\n" + "=" * 30)
        print(i18n.t("1: NEW SAVE"))
        print("2: ---")
        print(i18n.t("3: SETTINGS"))
        print(i18n.t("4: EXIT"))
        print("=" * 30)
        return False


def settings():
    while True:
        global languages
        print("\n" + "=" * 30)
        print(i18n.t("1: SWITCH LANGUAGES TO 简体中文"))
        print(i18n.t("2: DELETE SAVE ☠"))
        print(i18n.t("3: RETURN"))
        print("=" * 30)
        choice = input(i18n.t("Choose: "))
        if choice == "1" and languages == 'english':
            languages = '简体中文'
            i18n.set_lang(languages)
            print("切换至简体中文！")
        elif choice == "1" and languages == '简体中文':
            languages = 'english'
            i18n.set_lang(languages)
            print("Switch to English!")
        elif choice == "2":
            confirm = input(i18n.t("Do you want to continue ☠? (y/n): "))
            if confirm == 'y':
                save_manager.delete_save()
                break
            elif confirm == 'n':
                continue
            else:
                print(i18n.t("Invalid Choice!"))
        elif choice == "3":
            break
        else:
            print(i18n.t("Invalid Choice!"))
        if level != 0:
            save_manager.save_game()


def run():
    quick_load()
    i18n.set_lang(languages)
    while True:
        if show_menu():
            choice = input(i18n.t("Choose: "))
            if choice == "1":
                main_program()
            elif choice == "2":
                revive()
                main_program()
            elif choice == "3":
                settings()
            elif choice == "4":
                break
            else:
                print(i18n.t("Invalid Choice!"))
        else:
            choice = input(i18n.t("Choose: "))
            if choice == "1":
                revive()
                save_manager.save_game()
                main_program()
            elif choice == "2":
                pass
            elif choice == "3":
                settings()
            elif choice == "4":
                break
            else:
                print(i18n.t("Invalid Choice!"))


class GameSaveManager:
    def __init__(self, save_dir="saves"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)

    @staticmethod
    def get_game_state():
        main_vars = {
            'level': level,
            'baseHP': baseHP,
            'baseAP': baseAP,
            'baseDP': baseDP,
            'baseDEX': baseDEX,
            'baseLUC': baseLUC,
            'SP': SP,
            'MONEY': MONEY,
            'base_energy': base_energy,
            'EXP': EXP,
            'allocation_after_battle': allocation_after_battle,
            'weaponOnUse' : weaponOnUse,
            'torsoOnUse' : torsoOnUse,
            'legOnUse' : legOnUse,
            'gloveOnUse' : gloveOnUse,
            'shieldOnUse' : shieldOnUse,
            'footOnUse' : footOnUse,
            'acc1OnUse' : acc1OnUse,
            'acc2OnUse' : acc2OnUse,
            'acc3OnUse' : acc3OnUse,
            'acc4OnUse' : acc4OnUse,
            'acc5OnUse' : acc5OnUse,
            'acc6OnUse' : acc6OnUse,
            'slot1': slot1,
            'slot2': slot2,
            'slot3': slot3,
            'slot4': slot4,
            'slot5': slot5,
            'slot6': slot6,
            'languages' : languages,
            'bossDefeated' : bossDefeated,
            'autoAllocationStrategy': autoAllocationStrategy
        }

        accessory_data = accessory_items.copy()
        weapon_data = weapon_items.copy()
        torso_data = torso_items.copy()
        leg_data = leg_items.copy()
        shield_data = shield_items.copy()
        hand_data = hand_items.copy()
        foot_data = foot_items.copy()
        enemy_data = enemies_dict.copy()

        save_data = {
            'main_data': main_vars,
            'accessory_data': accessory_data,
            'weapon_data': weapon_data,
            'torso_data': torso_data,
            'leg_data': leg_data,
            'shield_data': shield_data,
            'hand_data': hand_data,
            'foot_data': foot_data,
            'enemy_data': enemy_data,
            'save_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'version': '1.1'
        }
        return save_data

    def save_game(self):
        save_data = self.get_game_state()
        save_file = self.save_dir / f"save.dat"
        backup_file = self.save_dir / f"save.bak"

        if save_file.exists():
            if backup_file.exists():
                backup_file.unlink()
            save_file.rename(backup_file)

        try:
            with open(save_file, 'wb') as f:
                pickle.dump(save_data, f)
            return True
        except Exception as e:
            print(i18n.t("Fail to save:") + f'{e}')
            if backup_file.exists():
                backup_file.rename(save_file)
            return False

    def load_game(self):
        save_file = self.save_dir / "save.dat"
        if not save_file.exists():
            return None

        try:
            with open(save_file, 'rb') as f:
                save_data = pickle.load(f)

            if 'main_data' not in save_data:
                print(i18n.t("Saved file is broken!"))
                return None

            return save_data
        except (pickle.UnpicklingError, EOFError, KeyError) as e:
            print(i18n.t("File to load:") + f'{e}')
            return None
        except Exception as e:
            print(i18n.t("Unknown error:") + f'{e}')
            return None

    @staticmethod
    def apply_save_data(save_data):
        global level, baseHP, baseAP, baseDP, baseDEX, baseLUC, SP, EXP, MONEY, base_energy, allocation_after_battle, weaponOnUse,torsoOnUse, gloveOnUse, shieldOnUse, footOnUse, legOnUse, languages, bossDefeated, autoAllocationStrategy
        global acc1OnUse, acc2OnUse, acc3OnUse, acc4OnUse, acc5OnUse, acc6OnUse, slot1, slot2, slot3, slot4, slot5, slot6
        if not save_data:
            return False

        try:
            main_data = save_data['main_data']
            level = main_data['level']
            baseHP = main_data['baseHP']
            baseAP = main_data['baseAP']
            baseDP = main_data['baseDP']
            baseDEX = main_data['baseDEX']
            baseLUC = main_data['baseLUC']
            SP = main_data['SP']
            EXP = main_data['EXP']
            MONEY = main_data['MONEY']
            base_energy = main_data['base_energy']
            allocation_after_battle = main_data['allocation_after_battle']
            languages = main_data['languages']
            weaponOnUse = main_data['weaponOnUse']
            torsoOnUse = main_data['torsoOnUse']
            gloveOnUse = main_data['gloveOnUse']
            legOnUse = main_data['legOnUse']
            shieldOnUse = main_data['shieldOnUse']
            footOnUse = main_data['footOnUse']
            acc1OnUse = main_data['acc1OnUse']
            acc2OnUse = main_data['acc2OnUse']
            acc3OnUse = main_data['acc3OnUse']
            acc4OnUse = main_data['acc4OnUse']
            acc5OnUse = main_data['acc5OnUse']
            acc6OnUse = main_data['acc6OnUse']
            slot1 = main_data['slot1']
            slot2 = main_data['slot2']
            slot3 = main_data['slot3']
            slot4 = main_data['slot4']
            slot5 = main_data['slot5']
            slot6 = main_data['slot6']
            bossDefeated = main_data['bossDefeated']
            autoAllocationStrategy = main_data['autoAllocationStrategy']


            accessory_items.clear()
            accessory_items.update(save_data['accessory_data'])
            weapon_items.clear()
            weapon_items.update(save_data['weapon_data'])
            torso_items.clear()
            torso_items.update(save_data['torso_data'])
            leg_items.clear()
            leg_items.update(save_data['leg_data'])
            shield_items.clear()
            shield_items.update(save_data['shield_data'])
            hand_items.clear()
            hand_items.update(save_data['hand_data'])
            foot_items.clear()
            foot_items.update(save_data['foot_data'])
            enemies_dict.clear()
            enemies_dict.update(save_data['enemy_data'])

            return True
        except Exception as e:
            print(i18n.t("Fail to apply data:") + f'{e}')
            return False


    def delete_save(self):
        save_file = self.save_dir / "save.dat"
        backup_file = self.save_dir / "save.bak"
        if save_file.exists():
            save_file.unlink()
        if backup_file.exists():
            backup_file.unlink()
        print(i18n.t("Save file deleted"))


save_manager = GameSaveManager()


def quick_load():
    save_data = save_manager.load_game()
    if save_data:
        return save_manager.apply_save_data(save_data)
    return False


if __name__ == "__main__":
    run()