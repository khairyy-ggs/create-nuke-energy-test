package dev.staggfield.content;

import com.simibubi.create.content.kinetics.base.KineticBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;

/** The kinetic network owns rotor speed; batch processing is the next machine pass. */
public class CascadeCentrifugeBlockEntity extends KineticBlockEntity {
    public CascadeCentrifugeBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state) {
        super(type, pos, state);
    }
}
