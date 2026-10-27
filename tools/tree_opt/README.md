# tree_opt — talent re-plans with a prism (written 2026-10-27 for the Lich -> Warlock / Phantasmagoria plan)
- `scen.py`: panel cells (kind m/M/L, gates, left-pairing), validity (24-pt cores, gates, pairing, prism slot), prism area + compensation
  (3.5% per micro/medium rank, legendaries count), scenario build (Warlock, Frozen Lotus, Pedigree core, Lone Walker's, freed aura slot).
- `opt.py`: greedy + swap local search with defence locks. `opt2.py`: fills the prism area, forces 2 legendaries (CC), single + double swaps.
- `decomp.py`: step-by-step gain breakdown. Plans live in ss14/thea/plan_trees_*.json (validate with tools/tree.py).
