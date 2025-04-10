from dataclasses import dataclass
from fitz import Document

from typing import Tuple

from enum import Enum
from dataclasses import dataclass

class Orientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

BoundingBox = Tuple[float, float, float, float]

@dataclass
class BlockNode:
    bbox: BoundingBox
    id: str
    

@dataclass
class GraphNode:
    bbox: BoundingBox
    text: str
    page_id: str
    node_id: str
    vicinities: list[str]

    
@dataclass
class Doc: 
    page_id: str
    left_x: float
    right_x: float
    bottom_y: float
    top_y: float
    doc: Document
    id: str


@dataclass
class DocGraph:
    doc_id: str
    page_blocks: dict[str, list[GraphNode]]  # page_id to its blocks