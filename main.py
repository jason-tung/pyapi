from flask import Flask, request
import os
from dotenv import load_dotenv, dotenv_values 
from scipy.stats import binom

load_dotenv() 
PATH = "/" + os.getenv("base")

app = Flask(__name__)

print("started")

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

def extract_reqs():
  l = ["min_damage", "max_damage", "rolls", "chance", "free_rolls"]
  return {
    k : int(request.args.get(k)) if k != "chance" else float(request.args.get(k)) for k in l
  }

@app.route(PATH)
def hello():
  return "hi"

@app.route(f"{PATH}/expected_damage")
def expdmg():
    if request.args.get("key") == os.getenv("key"):
      r = extract_reqs()
      print(r)
      return {"data": expected_damage(r["min_damage"], r["max_damage"], r["rolls"], r["chance"], r["free_rolls"])}
    return {"data": "uh oh"}

@app.route(f"{PATH}/damage_steps")
def dstep():
    if request.args.get("key") == os.getenv("key"):
      r = extract_reqs()
      return {"data": dmg_steps(r["min_damage"], r["max_damage"], r["rolls"], r["chance"], r["free_rolls"])}
    return {"data": "uh oh"}

if __name__ == '__main__': 
  app.run(debug=True, port=5000)