package dev.staggfield;

import dev.engine_room.flywheel.lib.model.baked.PartialModel;
import net.minecraft.resources.ResourceLocation;

public final class StaggfieldPartials {
    public static final PartialModel CENTRIFUGE_ROTOR = PartialModel.of(
            ResourceLocation.fromNamespaceAndPath(Staggfield.ID, "block/cascade_centrifuge/rotor"));

    private StaggfieldPartials() {}
}
