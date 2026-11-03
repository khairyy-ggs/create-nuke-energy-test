package dev.staggfield.content;

import com.simibubi.create.content.kinetics.base.KineticBlock;
import com.simibubi.create.foundation.block.IBE;
import dev.staggfield.Staggfield;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.Direction.Axis;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;

public class CascadeCentrifugeBlock extends KineticBlock implements IBE<CascadeCentrifugeBlockEntity> {
    public CascadeCentrifugeBlock(Properties properties) {
        super(properties);
    }

    @Override
    public Axis getRotationAxis(BlockState state) {
        return Axis.Y;
    }

    @Override
    public boolean hasShaftTowards(LevelReader world, BlockPos pos, BlockState state, Direction face) {
        return face.getAxis() == Axis.Y;
    }

    @Override
    public Class<CascadeCentrifugeBlockEntity> getBlockEntityClass() {
        return CascadeCentrifugeBlockEntity.class;
    }

    @Override
    public BlockEntityType<? extends CascadeCentrifugeBlockEntity> getBlockEntityType() {
        return Staggfield.CASCADE_CENTRIFUGE_ENTITY.get();
    }
}
