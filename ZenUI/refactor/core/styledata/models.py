from dataclasses import dataclass

@dataclass
class ZFramelessWindowStyleData:
    body: str

@dataclass
class ZTitleBarButtonData:
    icon: str
    iconhover: str
    iconpressed: str
    body: str
    bodyhover: str
    bodypressed: str

@dataclass
class ZButtonStyleData:
    text: str
    icon: str
    body: str
    bodyhover: str
    bodypressed: str
    border: str
    radius: int

@dataclass
class ZTooltipStyleData:
    text: str
    body: str
    border: str
    radius: int
    flash: str

@dataclass
class ZTextBlockStyleData:
    text: str