from scipy.stats import binom

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def approx(a,b,error=0.00000001):
  assert abs(a - b) < error

def expect_rolls(chance, rolls):
  lottery = binom(p=chance,n=rolls)
  return lottery.expect() 

assert(expect_rolls(.55, 3) == 1.65)

def calc_damage(min_damage=0, max_damage=0, rolls=0, chance=0, multiplier=0, free_rolls=0):
  damage_range = max_damage - min_damage
  expected_multiplier = (free_rolls + expect_rolls(chance*multiplier, rolls - free_rolls))/rolls
  expected_damage = min_damage + damage_range * expected_multiplier
  return expected_damage

def dmg_steps(min_damage, max_damage, rolls, chance, multiplier, free_rolls):
  damage_range = max_damage - min_damage
  adj_chance = chance * multiplier
  remain = 1
  for k in range(free_rolls, rolls + 1):
    expected_damage = damage_range * k/rolls + min_damage
    color = bcolors.OKGREEN if remain >= 0.5 else bcolors.FAIL
    print(f'[{free_rolls} Focus]\t{color}{remain:.3f}{bcolors.ENDC} chance to roll {k} and deal {round(expected_damage, 4)}+ damage')
    remain -= binom.pmf(k - free_rolls, rolls - free_rolls, adj_chance)

approx(calc_damage(min_damage=0, max_damage=27, rolls=4, chance=0.55, multiplier=1, free_rolls=0), 14.85)
approx(calc_damage(min_damage=0, max_damage=27, rolls=4, chance=0.55, multiplier=1, free_rolls=1), 17.8875)
approx(calc_damage(min_damage=4, max_damage=22, rolls=6, chance=0.55, multiplier=1, free_rolls=0), 13.9)
approx(calc_damage(min_damage=4, max_damage=22, rolls=6, chance=0.8, multiplier=.9, free_rolls=0), 16.96)

def report_stats(attack_name, min_damage, max_damage, rolls, chance, multiplier):
  dmg = calc_damage(min_damage=min_damage, max_damage=max_damage, rolls=rolls, chance=chance, multiplier=multiplier, free_rolls=0)
  bonus_dmg = calc_damage(min_damage=min_damage, max_damage=max_damage, rolls=rolls, chance=chance, multiplier=multiplier, free_rolls=1)
  odds_of_perfect = binom.pmf(rolls, rolls, chance*multiplier)
  bonus_odds_of_perfect = binom.pmf(rolls - 1, rolls - 1, chance*multiplier)
  print(f'\n{attack_name} deals {bcolors.OKGREEN}{round(dmg, 4)}{bcolors.ENDC}/{bcolors.WARNING}{round(bonus_dmg, 4)}{bcolors.ENDC} damage with {round(odds_of_perfect,4)}/{round(bonus_odds_of_perfect,4)} chance of perfect')
  dmg_steps(min_damage, max_damage, rolls, chance, multiplier, 0)
  print()
  dmg_steps(min_damage, max_damage, rolls, chance, multiplier, 1)

report_stats("light_swing", 4, 20, 3, 0.85, 1)
report_stats("heavy_swing", 0, 27, 3, 0.85, 0.8)