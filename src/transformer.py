from pathlib import Path
from .data_types import GraphNode, BlockNode, BoundingBox, DocGraph, Orientation
import uuid
import pdfplumber
from pdfplumber.page import Page

from collections import deque, defaultdict
from .config import default_config


def read_pdf(pdf_path: Path) -> DocGraph:
    """
    Read pdf and convert it to the graph of connected bbox, with their texts.
    """
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages 
        doc_id = str(pdf_path).split("/")[-1].split(".")[0]
        doc_graph = DocGraph(doc_id, defaultdict(list))
        for index, page in enumerate(pages):
            page_id = str(index)  # Can be revised later
            doc_graph.page_blocks[page_id] = extract_page_graph(page, page_id)
    return doc_graph


def extract_page_graph(page: Page, page_id: str) -> list[GraphNode]:
    """
    Extract graph of each page and return it as the list of GraphNodes.
    """
    root_bbox: BoundingBox = (default_config.starting_x, 
                    default_config.starting_y,
                    default_config.starting_y + default_config.box_width,
                    default_config.starting_y + default_config.box_height)
    root_id = str(uuid.uuid4())
    scanning_q = deque([BlockNode(root_bbox, root_id)])
    nodes: list[GraphNode] = []  
    
    while scanning_q:
        cur_node = scanning_q.pop()
        cur_bbox = cur_node.bbox
        right_border = cur_bbox[2] + default_config.box_width
        bottom_border = cur_bbox[3] + default_config.box_height 
        vicinities = []
        
        right_neighbour = next_node(page.bbox[2], cur_bbox, page, right_border, Orientation.HORIZONTAL)
        if right_neighbour:
            scanning_q.append(right_neighbour)
            vicinities.append(right_neighbour.id)
            
        bottom_neighbour = next_node(page.bbox[3], cur_bbox, page, bottom_border, Orientation.VERTICAL)
        if bottom_neighbour:
            scanning_q.append(bottom_neighbour)
            vicinities.append(bottom_neighbour.id)
        
        nodes.append(GraphNode(cur_bbox, page.within_bbox(cur_bbox).extract_text(), page_id, cur_node.id, vicinities))
    
    return nodes
       
        
def next_node(page_measure: float, bbox: BoundingBox, page: Page, border: float, direction: Orientation) -> BlockNode | None: 
    """
    Find the next node in the page along the spanning direction. 
    """
    while border < page_measure:
        next_bbox: BoundingBox = (bbox[2], bbox[1], border, bbox[3]) if direction ==  Orientation.HORIZONTAL else (bbox[0], bbox[3], bbox[2], border)
        text = page.within_bbox(next_bbox).extract_text()
        
        if text:
            new_id = str(uuid.uuid4())
            return BlockNode(next_bbox, new_id) 

        border = border + default_config.box_width if direction ==  Orientation.HORIZONTAL else border + default_config.box_height
        
    return None
    