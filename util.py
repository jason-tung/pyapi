from scipy.stats import binom

def expected_damage(min_damage, max_damage, rolls, chance, free_rolls):
  damage_range = max_damage - min_damage
  adjusted_rolls = rolls - free_rolls
  expected_range = chance * adjusted_rolls
  expected_damage = min_damage + damage_range * expected_range
  return expected_damage

def dmg_steps(min_damage, max_damage, rolls, chance, free_rolls):
  damage_range = max_damage - min_damage
  remain = 1
  results = []
  for k in range(free_rolls, rolls + 1):
    expected_damage = min_damage + damage_range * k/rolls + min_damage
    results.append((expected_damage, remain))
    remain -= binom.pmf(k - free_rolls, rolls - free_rolls, chance)
  return results
  
# print(dmg_steps(4, 20, 3, 0.85, 0))
# print(dmg_steps(4, 20, 3, 0.85, 1))


