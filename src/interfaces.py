from dataclasses import dataclass


@dataclass
class IdentityDataPointInterface:
    name: str  # Name to be used internally
    pretty_name: str  # Name to be displayed as label to user.
    type: str  # Enum: text, date, email


@dataclass
class Alert:
    message: str # The message to be displayed
