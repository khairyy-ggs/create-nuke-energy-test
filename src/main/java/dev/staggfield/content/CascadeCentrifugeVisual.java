package dev.staggfield.content;

import com.simibubi.create.content.kinetics.base.SingleAxisRotatingVisual;
import dev.engine_room.flywheel.api.visualization.VisualizationContext;
import dev.engine_room.flywheel.lib.model.Models;
import dev.staggfield.StaggfieldPartials;

public class CascadeCentrifugeVisual extends SingleAxisRotatingVisual<CascadeCentrifugeBlockEntity> {
    public CascadeCentrifugeVisual(VisualizationContext context, CascadeCentrifugeBlockEntity blockEntity,
                                   float partialTick) {
        super(context, blockEntity, partialTick, Models.partial(StaggfieldPartials.CENTRIFUGE_ROTOR));
    }
}
