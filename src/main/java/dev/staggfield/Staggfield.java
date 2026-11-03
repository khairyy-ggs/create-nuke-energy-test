package dev.staggfield;

import com.simibubi.create.foundation.data.CreateRegistrate;
import com.simibubi.create.AllBlocks;
import com.simibubi.create.api.stress.BlockStressValues;
import com.tterrag.registrate.util.entry.BlockEntityEntry;
import dev.staggfield.content.CascadeCentrifugeBlock;
import dev.staggfield.content.CascadeCentrifugeBlockEntity;
import dev.staggfield.content.PileBlock;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour.Properties;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod(Staggfield.ID)
public final class Staggfield {
    public static final String ID = "staggfield";

    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(ID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(ID);
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, ID);
    public static final CreateRegistrate REGISTRATE = CreateRegistrate.create(ID);

    public static final DeferredBlock<PileBlock> GRAPHITE_DRILLED = BLOCKS.register("graphite_drilled",
            () -> new PileBlock(Properties.of().strength(2.0f, 6.0f).sound(SoundType.STONE).requiresCorrectToolForDrops()));
    public static final DeferredBlock<CascadeCentrifugeBlock> CASCADE_CENTRIFUGE = BLOCKS.register("cascade_centrifuge",
            () -> new CascadeCentrifugeBlock(Properties.of().strength(3.5f, 8.0f).sound(SoundType.METAL).noOcclusion()));
    public static final DeferredBlock<Block> MAGNOX_VESSEL = BLOCKS.register("magnox_vessel",
            () -> new Block(Properties.of().strength(5.0f, 12.0f).sound(SoundType.METAL).requiresCorrectToolForDrops().noOcclusion()));
    public static final DeferredBlock<Block> COOLING_TOWER = BLOCKS.register("cooling_tower",
            () -> new Block(Properties.of().strength(4.0f, 10.0f).sound(SoundType.STONE).requiresCorrectToolForDrops().noOcclusion()));
    public static final DeferredBlock<Block> URANINITE_ORE = BLOCKS.register("uraninite_ore",
            () -> new Block(Properties.of().strength(3.0f, 3.0f).sound(SoundType.STONE).requiresCorrectToolForDrops()));
    public static final DeferredBlock<Block> DEEPSLATE_URANINITE_ORE = BLOCKS.register("deepslate_uraninite_ore",
            () -> new Block(Properties.of().strength(4.5f, 3.0f).sound(SoundType.DEEPSLATE).requiresCorrectToolForDrops()));

    public static final DeferredItem<BlockItem> GRAPHITE_DRILLED_ITEM = ITEMS.registerSimpleBlockItem(GRAPHITE_DRILLED);
    public static final DeferredItem<BlockItem> CASCADE_CENTRIFUGE_ITEM = ITEMS.registerSimpleBlockItem(CASCADE_CENTRIFUGE);
    public static final DeferredItem<BlockItem> MAGNOX_VESSEL_ITEM = ITEMS.registerSimpleBlockItem(MAGNOX_VESSEL);
    public static final DeferredItem<BlockItem> COOLING_TOWER_ITEM = ITEMS.registerSimpleBlockItem(COOLING_TOWER);
    public static final DeferredItem<BlockItem> URANINITE_ORE_ITEM = ITEMS.registerSimpleBlockItem(URANINITE_ORE);
    public static final DeferredItem<BlockItem> DEEPSLATE_URANINITE_ORE_ITEM = ITEMS.registerSimpleBlockItem(DEEPSLATE_URANINITE_ORE);

    public static final DeferredItem<Item> URANINITE_CONCENTRATE = item("uraninite_concentrate");
    public static final DeferredItem<Item> WASHED_URANINITE = item("washed_uraninite");
    public static final DeferredItem<Item> CARBON_FINES = item("carbon_fines");
    public static final DeferredItem<Item> FUEL_MIX = item("fuel_mix");
    public static final DeferredItem<Item> FUEL_PELLET = item("fuel_pellet");
    public static final DeferredItem<Item> INCOMPLETE_ROD_SLEEVE = item("incomplete_rod_sleeve");
    public static final DeferredItem<Item> PILE_FUEL_ROD = item("pile_fuel_rod");
    public static final DeferredItem<Item> PILE_SOURCE_ROD = item("pile_source_rod");
    public static final DeferredItem<Item> PILE_ABSORBER_ROD = item("pile_absorber_rod");
    public static final DeferredItem<Item> BORON_POWDER = item("boron_powder");
    public static final DeferredItem<Item> BORON_PELLET = item("boron_pellet");

    public static final BlockEntityEntry<CascadeCentrifugeBlockEntity> CASCADE_CENTRIFUGE_ENTITY =
            REGISTRATE.blockEntity("cascade_centrifuge", CascadeCentrifugeBlockEntity::new)
                    .visual(() -> CascadeCentrifugeVisual::new, false)
                    .validBlocks(CASCADE_CENTRIFUGE)
                    .register();

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> MAIN_TAB = TABS.register("main", () ->
            CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.staggfield"))
                    .icon(() -> new ItemStack(CASCADE_CENTRIFUGE_ITEM.get()))
                    .displayItems((parameters, output) -> {
                        output.accept(GRAPHITE_DRILLED_ITEM.get());
                        output.accept(CASCADE_CENTRIFUGE_ITEM.get());
                        output.accept(MAGNOX_VESSEL_ITEM.get());
                        output.accept(COOLING_TOWER_ITEM.get());
                        output.accept(URANINITE_ORE_ITEM.get());
                        output.accept(DEEPSLATE_URANINITE_ORE_ITEM.get());
                        output.accept(URANINITE_CONCENTRATE.get());
                        output.accept(WASHED_URANINITE.get());
                        output.accept(CARBON_FINES.get());
                        output.accept(FUEL_MIX.get());
                        output.accept(FUEL_PELLET.get());
                        output.accept(PILE_FUEL_ROD.get());
                        output.accept(PILE_SOURCE_ROD.get());
                        output.accept(PILE_ABSORBER_ROD.get());
                        output.accept(BORON_POWDER.get());
                        output.accept(BORON_PELLET.get());
                    })
                    .build());

    private static DeferredItem<Item> item(String id) {
        return ITEMS.registerSimpleItem(id, new Item.Properties());
    }

    public Staggfield(IEventBus modBus) {
        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        TABS.register(modBus);
        REGISTRATE.registerEventListeners(modBus);
        modBus.addListener(Staggfield::commonSetup);
    }

    private static void commonSetup(FMLCommonSetupEvent event) {
        event.enqueueWork(() -> BlockStressValues.IMPACTS.register(CASCADE_CENTRIFUGE.get(),
                () -> BlockStressValues.getImpact(AllBlocks.MECHANICAL_MIXER.get()) + 2.0));
    }
}
