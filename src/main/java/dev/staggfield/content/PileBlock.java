package dev.staggfield.content;

import java.util.Locale;
import dev.staggfield.Staggfield;
import net.minecraft.core.BlockPos;
import net.minecraft.util.StringRepresentable;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.phys.BlockHitResult;

/** Drilled graphite block. The rod in its channel is a blockstate, so no renderer is needed. */
public class PileBlock extends Block {
    public enum Rod implements StringRepresentable {
        EMPTY, FUEL, SOURCE, ABSORBER;
        @Override public String getSerializedName() { return name().toLowerCase(Locale.ROOT); }
    }
    public static final EnumProperty<Rod> ROD = EnumProperty.create("rod", Rod.class);

    public PileBlock(Properties props) {
        super(props);
        registerDefaultState(stateDefinition.any().setValue(ROD, Rod.EMPTY));
    }

    @Override
    public InteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player,
                                       InteractionHand hand, BlockHitResult hit) {
        Rod rod = rodFor(stack);
        if (rod == Rod.EMPTY || state.getValue(ROD) != Rod.EMPTY)
            return super.useItemOn(stack, state, level, pos, player, hand, hit);
        if (!level.isClientSide) {
            level.setBlock(pos, state.setValue(ROD, rod), Block.UPDATE_ALL);
            if (!player.isCreative())
                stack.shrink(1);
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player) {
        Rod rod = state.getValue(ROD);
        if (!player.isCrouching() || rod == Rod.EMPTY)
            return super.useWithoutItem(state, level, pos, player);
        if (!level.isClientSide) {
            level.setBlock(pos, state.setValue(ROD, Rod.EMPTY), Block.UPDATE_ALL);
            ItemStack removed = itemFor(rod);
            if (!player.addItem(removed))
                Block.popResource(level, pos, removed);
        }
        return InteractionResult.SUCCESS;
    }

    private static Rod rodFor(ItemStack stack) {
        if (stack.is(Staggfield.PILE_FUEL_ROD.get())) return Rod.FUEL;
        if (stack.is(Staggfield.PILE_SOURCE_ROD.get())) return Rod.SOURCE;
        if (stack.is(Staggfield.PILE_ABSORBER_ROD.get())) return Rod.ABSORBER;
        return Rod.EMPTY;
    }

    private static ItemStack itemFor(Rod rod) {
        return switch (rod) {
            case FUEL -> new ItemStack(Staggfield.PILE_FUEL_ROD.get());
            case SOURCE -> new ItemStack(Staggfield.PILE_SOURCE_ROD.get());
            case ABSORBER -> new ItemStack(Staggfield.PILE_ABSORBER_ROD.get());
            case EMPTY -> ItemStack.EMPTY;
        };
    }

    @Override
    public void playerDestroy(Level level, Player player, BlockPos pos, BlockState state, BlockEntity blockEntity,
                              ItemStack tool) {
        super.playerDestroy(level, player, pos, state, blockEntity, tool);
        if (!level.isClientSide) {
            ItemStack rod = itemFor(state.getValue(ROD));
            if (!rod.isEmpty())
                Block.popResource(level, pos, rod);
        }
    }

    @Override protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> b) { b.add(ROD); }
}
