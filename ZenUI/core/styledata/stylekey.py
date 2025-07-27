from enum import Enum
class StyleKey(Enum):
    Text = 'Text'
    TextHover = 'TextHover'
    TextPressed = 'TextPressed'

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