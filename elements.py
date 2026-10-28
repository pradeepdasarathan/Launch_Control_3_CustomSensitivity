from ableton.v3.base import nop
from ableton.v3.control_surface import ElementsBase, MapMode

from Launch_Control_XL_3.colored_encoder import ColoredEncoderElement
from Launchkey_MK4.display_target import DisplayTargetElement

from . import midi


ENCODER_MAPPING_SENSITIVITY = 2.0


class SensitivityColoredEncoderElement(ColoredEncoderElement):
    """Keep the configured scale when Live supplies per-parameter defaults."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        set_sensitivities = self.set_sensitivities

        def set_scaled_sensitivities(standard, fine_grain):
            set_sensitivities(
                standard * ENCODER_MAPPING_SENSITIVITY,
                fine_grain * ENCODER_MAPPING_SENSITIVITY,
            )

        self.set_sensitivities = set_scaled_sensitivities


class Elements(ElementsBase):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

        self.add_modifier_button(63, 'Shift_Button', channel=6)
        self.add_button(30, 'Encoder_Mode_Element', channel=6)
        self.add_button(31, 'Encoder_User_Mode_Element', channel=6)
        self.add_button(66, 'Daw_Function_Button')
        self.add_button(102, 'Track_Right_Button')
        self.add_button(103, 'Track_Left_Button')
        self.add_button(104, 'Novation_Button')
        self.add_button(106, 'Page_Up_Button')
        self.add_button(107, 'Page_Down_Button')

        self.add_modified_control(
            control=self.track_right_button, modifier=self.shift_button
        )
        self.add_modified_control(
            control=self.track_left_button, modifier=self.shift_button
        )
        self.add_modified_control(
            control=self.page_up_button, modifier=self.shift_button
        )
        self.add_modified_control(
            control=self.page_down_button, modifier=self.shift_button
        )

        self.add_button_matrix([range(37, 45)], 'Daw_Buttons')

        # Apply sensitivity once to the parent matrix. Upper_Encoders and
        # Lower_Encoders are submatrices of this matrix.
        self.add_matrix(
            [range(77, 85), range(85, 93)],
            'Encoders',
            map_mode=MapMode.LinearBinaryOffset,
            channels=15,
            element_factory=SensitivityColoredEncoderElement,
            mapping_sensitivity=ENCODER_MAPPING_SENSITIVITY,
        )
        self.add_submatrix(self.encoders, 'Upper_Encoders', rows=(0, 1))
        self.add_submatrix(self.encoders, 'Lower_Encoders', rows=(1, 2))

        self.encoder_mode_element.send_value = nop

        self.add_sysex_element(midi.make_connection_message()[:-2], 'Connection_Element')
        self.add_display_command_for_target('Static', 53, 9)
        self.add_display_command_for_target('Temp', 54, 3, disable_caching=True)

        for i in range(16):
            self.add_display_command_for_target('Encoder_{}'.format(i), 13 + i, 3)

    def add_display_command_for_target(
        self, name, target, num_fields, disable_caching=False
    ):
        self.add_element(
            '{}_Display_Command'.format(name),
            DisplayTargetElement,
            midi.SYSEX_HEADER,
            target,
            num_fields,
            disable_caching=disable_caching,
        )
