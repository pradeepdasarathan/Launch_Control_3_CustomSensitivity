# Launch Control 3 encoder sensitivity patch

This repository contains a replacement `elements.py` for the Novation Launch Control 3 Ableton Live remote script. It adapts the sensitivity fix to the LC3 encoder matrix and keeps the configured multiplier when Live's device mapping supplies parameter-specific sensitivities. The public repository contains only this patch and these instructions; it does not redistribute Ableton's factory script files.

## Install

1. Close Ableton Live.
2. Copy Live's factory `Launch_Control_3` remote-script folder into `~/Music/Ableton/User Library/Remote Scripts/` and rename the copy to `Launch_Control_3_CustomSensitivity`.
3. Replace the copy's `elements.py` with this repository's `elements.py`. Keep the other files from the factory folder.
4. If the custom copy contains `elements.pyc` or an `__pycache__` directory, remove them so Live loads the replacement source.
5. Start Live and select `Launch_Control_3_CustomSensitivity` as the Control Surface. Use the Launch Control 3 DAW input and output ports.

Set `ENCODER_MAPPING_SENSITIVITY` near the top of `elements.py`. It is `2.0` by default, scaling Live's parameter-specific standard and fine sensitivities by 2 while preserving their relative differences. Restart Live after changing it.

This patch expects Ableton Live 12 or later and the factory Launch Control 3 script files supplied with Live. It has been confirmed working on the user's controller and setup.
