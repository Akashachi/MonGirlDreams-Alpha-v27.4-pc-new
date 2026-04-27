# Plucked out of the example, size adjusted. - FCMCL

screen color_picker(BodySetting):
    ## The preview swatch. Needs to be provided the picker variable from above.
    default picker_swatch = DynamicDisplayable(picker_color, picker=BodySetting,
        xsize=69, ysize=69)
    default picker_hex = DynamicDisplayable(picker_hexcode, picker=BodySetting)

    style_prefix 'cpicker'

    hbox:
        vbox:
            add BodySetting
            bar value FieldValue(BodySetting, "hue_rotation", 1.0):
                changed [renpy.hide_screen("ON_AppearanceCreatorShowSample"), renpy.show_screen("ON_AppearanceCreatorShowSample")]
        vbox:
            xsize 200 spacing 10 align (0.0, 0.0)
            add picker_swatch
            ## Note that these do not update in
            ## tandem with the picker, but when the mouse is released. You
            ## will need to use a DynamicDisplayable for real-time updates.
            add picker_hex
            ## These update when the mouse button is released
            ## since they aren't a dynamic displayable
            text "R: [BodySetting.color.rgb[0]:.2f]"
            text "G: [BodySetting.color.rgb[1]:.2f]"
            text "B: [BodySetting.color.rgb[2]:.2f]"

################################################################################
## Styles
style cpicker_vbox:
    align (0.5, 0.5)
    spacing 15
style cpicker_hbox:
    align (0.5, 0.5)
    spacing 15
style cpicker_vbar:
    xysize (50, 340)
    base_bar At(Transform("#000", xysize=(50, 340)), spectrum(horizontal=False))
    thumb Transform("selector_bg", xysize=(50, 20))
    thumb_offset 10
style cpicker_bar:
    xysize (340, 50)
    base_bar At(Transform("#000", xysize=(340, 50)), spectrum())
    thumb Transform("selector_bg", xysize=(20, 50))
    thumb_offset 10
style cpicker_text:
    color "#fff"
style cpicker_button:
    padding (10, 10) insensitive_background "#fff"
style cpicker_button_text:
    color "#aaa"
    hover_color "#fff"
style cpicker_image_button:
    xysize (69, 69)
    padding (10, 10)
    hover_foreground "#fff2"
