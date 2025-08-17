from enum import Enum

class ZStyleDataKey(Enum):
    Text = 'Text'
    TextHover = 'TextHover'
    TextPressed = 'TextPressed'

    TextBackSectcted = 'TextBackSectcted'

    TextToggled = 'TextToggled'
    TextToggledHover = 'TextToggledHover'
    TextToggledPressed = 'TextToggledPressed'

    Icon = 'Icon'
    IconHover = 'IconHover'
    IconPressed = 'IconPressed'

    IconToggled = 'IconToggled'
    IconToggledHover = 'IconToggledHover'
    IconToggledPressed = 'IconToggledPressed'

    Body = 'Body'
    BodyHover = 'BodyHover'
    BodyPressed = 'BodyPressed'
    BodySatrt = 'BodyStart'
    BodyEnd = 'BodyEnd'
    BodyFocused = 'BodyFocused'

    BodyToggled = 'BodyToggled'
    BodyToggledHover = 'BodyToggledHover'
    BodyToggledPressed = 'BodyToggledPressed'

    Border = 'Border'
    BorderHover = 'BorderHover'
    BorderPressed = 'BorderPressed'

    BorderToggled = 'BorderToggled'
    BorderToggledHover = 'BorderToggledHover'
    BorderToggledPressed = 'BorderToggledPressed'

    Radius = 'Radius'
    RadiusHover = 'RadiusHover'
    RadiusPressed = 'RadiusPressed'

    Handle = 'Handle'
    HandleHover = 'HandleHover'
    HandlePressed = 'HandlePressed'
    HandleBorder = 'HandleBorder'
    HandleInner = 'HandleInner'
    HandleOuter = 'HandleOuter'

    Track = 'Track'
    TrackBorder = 'TrackBorder'

    FillArea = 'FillArea'
    FillAreaStart = 'FillAreaStart'
    FillAreaEnd = 'FillAreaEnd'
    FillAreaBorder = 'FillAreaBorder'

    Underline = 'Underline'
    UnderlineFocused = 'UnderlineFocused'
    Cursor = 'Cursor'
    Mask = 'Mask'