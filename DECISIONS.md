- Name: Create: Stagg Field. Plain and tied to the first pile under a stadium stand, no "Advanced/Quantum".
- Sim first in pure Java: provable without Create, reusable for every tier.
- Flux peak at 2 cells (HBM peaks at 1.5): own constants, own rule.
- Doppler 0.5 after a scan: 0.25 melted cooled cores, higher pins temperature; recorded in gotchas.
- Rods are a blockstate on the graphite block, not block entities: cheap, no renderer.
- Output is rotation via Create boiler heat, never FE.
- Rejected: weapons, new ore filler, tier-numbered names (Mk2), fusion in half one.

## Wave 1.3 decisions

- Pin the implementation to Create 6.0.10-280 and matching Ponder/Flywheel/Registrate coordinates from the official NeoForge dependency guide.
- Keep the first uranium resource modest: one ore plus a deepslate variant feeding Create processing, not a family of filler ores.
- Use Create's kinetic entity and Flywheel rotating partial for the visible centrifuge. Add a custom RPM-aware recipe type in a later pass, after compile and client API validation.
- Keep pile rods in the existing blockstate model. Put insert/remove behavior on the block until connected-lattice simulation is ready.
- Use HBM's progression dependencies as research, while keeping Stagg Field names, recipes, assets and core mechanics original.
