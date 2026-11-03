# HBM Nuclear Tech scan and Stagg Field adaptation

## Scope and source caution

This is a progression and systems scan, not a port. HBM's public wiki describes a very broad industrial/nuclear sandbox (the machine category lists 110 pages across power, heat, multiblocks, petrochemistry, and processing). The main page identifies the mod as Minecraft 1.7.10; several machine and progression pages warn of planned changes, deprecation, or stale details. Treat exact recipes, values, names, and current implementation as edition-specific. Do not copy code, assets, machine names, or recipes.

## Systems mapped from the guide

1. **Preparation and early fuel**: metalworking, drilling, ore treatment, and access to fissile feed. HBM makes early nuclear a long progression branch rather than a single block unlock.
2. **Neutron breeding**: the Chicago Pile turns graphite channels plus source and fuel rods into a spatial flux problem. Rod placement, spacing, heat and depletion matter; breeding creates later feed. The wiki says the pile is optional in one route and planned for redesign, so its exact recipe path is weak evidence, while the mechanic and progression role are strong references.
3. **Isotope enrichment**: uranium feed is chemically converted to uranium hexafluoride, then passed through a cascade of four gas centrifuges. Cascade arrangement and throughput upgrades create a physical automation goal.
4. **First power reactor**: ZIRNOX introduces controlled heat and coolant/steam handling. Its guide highlights mismatched steam grades, blocked output and minimum temperature as concrete operating hazards. It is presented as an introductory bridge rather than the final reactor.
5. **Reactor branches**: PWR emphasizes a modular water loop; RBMK emphasizes channel layout, fuel choices and a dangerous positive-void feedback regime; research and breeding reactors support isotope production. The guide shows these as distinct operating patterns rather than simple tiers of one machine.
6. **Spent fuel and reuse**: depleted fuel has useful isotopes. Hot spent fuel is extracted, cooled in an underwater pool, then separated by PUREX/SILEX-like processing. Waste handling is both a safety step and a progression gate for useful materials.
7. **Late energy and industry**: turbine/steam chains, cooling towers, advanced petrochemistry, materials, fusion and other endgame systems sit beyond fission. The machine catalog is much wider than the nuclear path; adding all branches would make this addon incoherent.
8. **Safety and readability**: radiation protection and material handling are explicit progression systems. HBM's broad machine breadth creates setup complexity; one community report also describes progression instructions as difficult to follow. Treat that report as a prompt for clarity, not representative research.

## What Stagg Field adopts

- Make the first pile build a legible spatial puzzle: graphite channel, source/fuel/absorber rods, neutron escape, heat and decay heat.
- Make later enrichment a Create-driven kinetic cascade whose RPM and stage count matter, with a recipe viewer and Ponder guidance.
- Use a safe introductory gas-cooled vessel with a real heat-transfer loop before designing the more hazardous channel reactor.
- Give spent fuel a cooling/reprocessing loop with useful outputs and clear handling feedback.
- Gate each stage on useful outputs from the previous one and expose prerequisites before failure.

## What stays distinct or deferred

- Stagg Field uses Create rotation and stress as its power interface; it does not reproduce HBM's energy system.
- The pile's flux geometry and shaft-held scram remain Stagg Field's core mechanic.
- Wave 1.3 has a visual kinetic centrifuge, but custom RPM-dependent separation is not implemented yet. Ordinary Create recipes only cover feed preparation.
- The pile rods are currently stored in a blockstate; an assembled lattice simulation, heat loop, and actuator are still roadmap work.
- Radiation, breeder reactor, RBMK-like positive void feedback, fusion, petrochemistry and material trees are later design gates, not current features.

## Staged build order

1. Workshop, uranium feed prep, pile lattice, and fail-safe scram.
2. RPM cascade, gas-cooled vessel, heat rejection, and spent-fuel pool.
3. Two-circuit pressurized-water loop and approachable turbine output.
4. Channel reactor with explicit positive-void behavior and safety gates.
5. Advanced breeding and fusion only after the earlier loops are playable.

## Sources

- [HBM Nuclear Age guide](https://nucleartech.wiki/wiki/Guide%3A_Nuclear_Age)
- [Chicago Pile](https://nucleartech.wiki/wiki/Chicago_Pile)
- [Guide: Pre-Nuclear](https://nucleartech.wiki/wiki/Guide%3A_Pre-Nuclear)
- [ZIRNOX](https://nucleartech.wiki/wiki/ZIRNOX)
- [PWR](https://nucleartech.wiki/wiki/PWR)
- [RBMK](https://nucleartech.wiki/wiki/RBMK)
- [Breeding Reactor](https://nucleartech.wiki/wiki/Breeding_Reactor)
- [Machine category](https://nucleartech.wiki/wiki/Category%3AMachines)
- [Reactor category](https://nucleartech.wiki/wiki/Category%3AReactors)
- [One player progression discussion](https://www.reddit.com/r/HBMNuclearTechMod/comments/1cifeu8)
