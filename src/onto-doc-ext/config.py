from dataclasses import dataclass


@dataclass
class ScaningConfig:
    starting_x: float
    starting_y: float
    box_width: float
    box_height: float
    moving_dis: float
    overlap: float


default_config = ScaningConfig(
    starting_x=0,
    starting_y=0,
    box_width=100,
    box_height=30,
    moving_dis=10,
    overlap=5,
)
