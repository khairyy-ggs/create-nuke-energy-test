"""Generate the first playable fuel-preparation recipes and uraninite deposit data."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "src/main/resources"
ASSETS = RES / "assets/staggfield"
DATA = RES / "data/staggfield"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def item_model(item, texture):
    write_json(ASSETS / f"models/item/{item}.json", {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": f"staggfield:block/{texture}"},
    })


def block_cube(name, texture):
    write_json(ASSETS / f"blockstates/{name}.json", {
        "variants": {"": {"model": f"staggfield:block/{name}"}}
    })
    write_json(ASSETS / f"models/block/{name}.json", {
        "parent": "minecraft:block/cube_all",
        "textures": {"all": f"staggfield:block/{texture}"},
    })
    write_json(ASSETS / f"models/item/{name}.json", {
        "parent": f"staggfield:block/{name}"
    })


def create_processing(recipe_type, ingredients, results, **extra):
    return {"type": f"create:{recipe_type}", "ingredients": ingredients,
            "results": results, **extra}


def shaped(pattern, key, item):
    return {"type": "minecraft:crafting_shaped", "category": "misc",
            "pattern": pattern, "key": key, "result": {"id": f"staggfield:{item}"}}


def main():
    block_cube("uraninite_ore", "uraninite_ore")
    block_cube("deepslate_uraninite_ore", "deepslate_uraninite_ore")

    item_textures = {
        "uraninite_concentrate": "uraninite_concentrate",
        "washed_uraninite": "washed_uraninite",
        "carbon_fines": "carbon_fines",
        "fuel_mix": "fuel_mix",
        "fuel_pellet": "fuel_pellet",
        "incomplete_rod_sleeve": "casing_steel",
        "pile_fuel_rod": "pile_rod_fuel",
        "pile_source_rod": "pile_rod_source",
        "pile_absorber_rod": "pile_rod_absorber",
        "boron_powder": "boron_powder",
        "boron_pellet": "boron_pellet",
    }
    for item, texture in item_textures.items():
        item_model(item, texture)

    # Flywheel partial: an asymmetric three-arm plate and one hazard stripe make rotation visible.
    def rotor_faces(top="#main"):
        return {face: {"texture": top if face == "up" else "#main"}
                for face in ("down", "up", "north", "south", "east", "west")}
    write_json(ASSETS / "models/block/cascade_centrifuge/rotor.json", {
        "textures": {"main": "staggfield:block/casing_steel", "warning": "staggfield:block/rotor_warning",
                      "particle": "#main"},
        "elements": [
            {"from": [8, 16, 7], "to": [15, 17, 9], "faces": rotor_faces("#warning")},
            {"from": [7, 16, 2], "to": [9, 17, 8], "faces": rotor_faces()},
            {"from": [3, 16, 10], "to": [8, 17, 12], "faces": rotor_faces()},
            {"from": [6, 16, 6], "to": [10, 17, 10], "faces": rotor_faces()},
        ],
    })

    recipes = {
        "uraninite_ore_crushing": create_processing("crushing",
            [{"item": "staggfield:uraninite_ore"}],
            [{"id": "staggfield:uraninite_concentrate", "count": 2},
             {"id": "minecraft:gravel", "chance": 0.35}], processing_time=240),
        "deepslate_uraninite_crushing": create_processing("crushing",
            [{"item": "staggfield:deepslate_uraninite_ore"}],
            [{"id": "staggfield:uraninite_concentrate", "count": 3},
             {"id": "minecraft:gravel", "chance": 0.5}], processing_time=300),
        "uraninite_washing": create_processing("splashing",
            [{"item": "staggfield:uraninite_concentrate"}],
            [{"id": "staggfield:washed_uraninite"},
             {"id": "minecraft:flint", "chance": 0.2}]),
        "carbon_fines_milling": create_processing("milling",
            [{"item": "minecraft:coal_block"}],
            [{"id": "staggfield:carbon_fines", "count": 4}], processing_time=160),
        "fuel_mix": create_processing("mixing",
            [{"item": "staggfield:washed_uraninite"},
             {"item": "staggfield:carbon_fines"},
             {"item": "minecraft:clay_ball"}],
            [{"id": "staggfield:fuel_mix", "count": 2}], heat_requirement="heated"),
        "fuel_pellet_pressing": create_processing("pressing",
            [{"item": "staggfield:fuel_mix"}],
            [{"id": "staggfield:fuel_pellet", "count": 2}]),
        "boron_powder_milling": create_processing("milling",
            [{"item": "minecraft:lapis_lazuli"}],
            [{"id": "staggfield:boron_powder"}], processing_time=120),
        "boron_pellet_mixing": create_processing("mixing",
            [{"item": "staggfield:boron_powder"}, {"item": "minecraft:clay_ball"}],
            [{"id": "staggfield:boron_pellet"}], heat_requirement="heated"),
        "graphite_block_pressing": create_processing("compacting",
            [{"item": "minecraft:coal_block"}, {"item": "minecraft:coal_block"}],
            [{"id": "staggfield:graphite_drilled"}]),
    }
    for name, recipe in recipes.items():
        write_json(DATA / f"recipe/{name}.json", recipe)

    write_json(DATA / "recipe/fuel_element_assembly.json", {
        "type": "create:sequenced_assembly",
        "ingredient": {"item": "create:iron_sheet"},
        "loops": 1,
        "results": [
            {"id": "staggfield:pile_fuel_rod"},
            {"id": "create:iron_sheet", "chance": 0.25},
        ],
        "sequence": [
            {"type": "create:deploying", "ingredients": [
                {"item": "create:iron_sheet"},
                {"item": "staggfield:fuel_pellet"}],
             "results": [{"id": "staggfield:incomplete_rod_sleeve"}]},
            {"type": "create:pressing", "ingredients": [
                {"item": "staggfield:incomplete_rod_sleeve"}],
             "results": [{"id": "staggfield:incomplete_rod_sleeve"}]},
        ],
        "transitional_item": {"id": "staggfield:incomplete_rod_sleeve"},
    })
    write_json(DATA / "recipe/absorber_element_assembly.json", {
        "type": "create:sequenced_assembly",
        "ingredient": {"item": "create:copper_sheet"},
        "loops": 1,
        "results": [{"id": "staggfield:pile_absorber_rod"}],
        "sequence": [
            {"type": "create:deploying", "ingredients": [
                {"item": "create:copper_sheet"},
                {"item": "staggfield:boron_pellet"}],
             "results": [{"id": "staggfield:incomplete_rod_sleeve"}]},
            {"type": "create:pressing", "ingredients": [
                {"item": "staggfield:incomplete_rod_sleeve"}],
             "results": [{"id": "staggfield:incomplete_rod_sleeve"}]},
        ],
        "transitional_item": {"id": "staggfield:incomplete_rod_sleeve"},
    })
    write_json(DATA / "recipe/source_element.json", {
        "type": "minecraft:crafting_shaped", "category": "misc",
        "pattern": [" G ", " S ", " C "],
        "key": {"G": {"item": "minecraft:glowstone_dust"},
                "S": {"item": "create:iron_sheet"},
                "C": {"item": "minecraft:copper_ingot"}},
        "result": {"id": "staggfield:pile_source_rod", "count": 1},
    })
    write_json(DATA / "recipe/incomplete_rod_sleeve.json", shaped([" I ", "ISI", " I "], {
        "I": {"item": "create:iron_sheet"}, "S": {"item": "create:shaft"}}, "incomplete_rod_sleeve"))
    block_recipes = {
        "cascade_centrifuge": shaped([" S ", "CPC", " S "], {
            "S": {"item": "create:shaft"}, "C": {"item": "create:andesite_casing"},
            "P": {"item": "create:precision_mechanism"}}, "cascade_centrifuge"),
        "magnox_vessel": shaped(["ICI", "IHI", "ICI"], {
            "I": {"item": "create:iron_sheet"}, "C": {"item": "create:copper_sheet"},
            "H": {"item": "create:fluid_tank"}}, "magnox_vessel"),
        "cooling_tower": shaped(["S S", "SIS", "S S"], {
            "S": {"item": "minecraft:stone_bricks"}, "I": {"item": "create:iron_sheet"}}, "cooling_tower"),
    }
    for name, recipe in block_recipes.items():
        write_json(DATA / f"recipe/{name}_crafting.json", recipe)

    for block in ("graphite_drilled", "cascade_centrifuge", "magnox_vessel", "cooling_tower",
                  "uraninite_ore", "deepslate_uraninite_ore"):
        write_json(DATA / f"loot_table/blocks/{block}.json", {
            "type": "minecraft:block",
            "pools": [{"rolls": 1.0, "entries": [{"type": "minecraft:item", "name": f"staggfield:{block}"}],
                       "conditions": [{"condition": "minecraft:survives_explosion"}]}],
        })
    write_json(RES / "data/minecraft/tags/block/mineable/pickaxe.json", {
        "replace": False,
        "values": [f"staggfield:{block}" for block in
                   ("graphite_drilled", "cascade_centrifuge", "magnox_vessel", "cooling_tower",
                    "uraninite_ore", "deepslate_uraninite_ore")],
    })
    write_json(RES / "data/minecraft/tags/block/needs_iron_tool.json", {
        "replace": False,
        "values": ["staggfield:uraninite_ore", "staggfield:deepslate_uraninite_ore"],
    })

    worldgen = RES / "data/staggfield/worldgen"
    write_json(worldgen / "configured_feature/uraninite_ore.json", {
        "type": "minecraft:ore",
        "config": {
            "size": 6,
            "discard_chance_on_air_exposure": 0.15,
            "targets": [
                {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"},
                 "state": {"Name": "staggfield:uraninite_ore"}},
                {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"},
                 "state": {"Name": "staggfield:deepslate_uraninite_ore"}},
            ],
        },
    })
    write_json(worldgen / "placed_feature/uraninite_ore.json", {
        "feature": "staggfield:uraninite_ore",
        "placement": [
            {"type": "minecraft:count", "count": 5},
            {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range", "height": {
                "type": "minecraft:trapezoid",
                "min_inclusive": {"absolute": -48}, "max_inclusive": {"absolute": 20}}},
            {"type": "minecraft:biome"},
        ],
    })
    write_json(RES / "data/staggfield/neoforge/biome_modifier/add_uraninite_ore.json", {
        "type": "neoforge:add_features",
        "biomes": "#minecraft:is_overworld",
        "features": "staggfield:uraninite_ore",
        "step": "underground_ores",
    })

    lang_path = ASSETS / "lang/en_us.json"
    lang = json.loads(lang_path.read_text(encoding="utf-8"))
    lang.update({
        "itemGroup.staggfield": "Stagg Field",
        "block.staggfield.uraninite_ore": "Uraninite Ore",
        "block.staggfield.deepslate_uraninite_ore": "Deepslate Uraninite Ore",
        "item.staggfield.uraninite_concentrate": "Uraninite Concentrate",
        "item.staggfield.washed_uraninite": "Washed Uraninite",
        "item.staggfield.carbon_fines": "Carbon Fines",
        "item.staggfield.fuel_mix": "Fuel Pellet Mix",
        "item.staggfield.fuel_pellet": "Sintered Fuel Pellet",
        "item.staggfield.incomplete_rod_sleeve": "Incomplete Rod Sleeve",
        "item.staggfield.pile_fuel_rod": "Pile Fuel Rod",
        "item.staggfield.pile_source_rod": "Neutron Source Rod",
        "item.staggfield.pile_absorber_rod": "Boron Absorber Rod",
        "item.staggfield.boron_powder": "Boron Powder",
        "item.staggfield.boron_pellet": "Boron Carbide Pellet",
    })
    write_json(lang_path, lang)


if __name__ == "__main__":
    main()
