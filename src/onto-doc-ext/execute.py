from pathlib import Path
from .data_types import GraphNode, BlockNode, BoundingBox, DocGraph
import uuid
import pdfplumber

from collections import deque, defaultdict
from .config import default_config


def read_pdf(pdf_path: Path) -> DocGraph:
    """
    
    """
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages 
        doc_id = str(pdf_path).split("/")[-1].split(".")[0]
        doc_graph = DocGraph(doc_id, defaultdict(list))
        for index, page in enumerate(pages):
            page_id = str(index)  # Can be revised later
            page_width = page.bbox[2]
            page_height = page.bbox[3]
            root_bbox: BoundingBox = (default_config.starting_x, 
                         default_config.starting_y,
                         default_config.starting_y + default_config.box_width,
                         default_config.starting_y + default_config.box_height)
            root_id = str(uuid.uuid4())
            root_text = page.within_bbox(root_bbox).extract_text()  # Extract text within the bounding box
            scanning_q = deque([BlockNode(root_bbox, root_text, page_id, root_id)])
            vicinities: dict[BoundingBox, list[str]] = defaultdict(list)
            observed_areas: list[BoundingBox] = []
            covered_areas: list[GraphNode] = []
            
            while scanning_q:
                cur_node = scanning_q.pop()
                cur_bbox = cur_node.bbox
                
                if cur_bbox[2] + default_config.box_width < page_width:
                    right_bbox: BoundingBox = (cur_bbox[2], cur_bbox[1], cur_bbox[2] + default_config.box_width, cur_bbox[3])
                    if right_bbox not in observed_areas:
                        right_id = str(uuid.uuid4())
                        right_text = page.within_bbox(right_bbox).extract_text()
                        scanning_q.append(BlockNode(right_bbox, right_text, page_id, right_id))  # move to right
                        vicinities[cur_bbox].append(right_id)
                if cur_bbox[3] + default_config.box_height < page_height:
                    down_bbox: BoundingBox = (cur_bbox[0], cur_bbox[3], cur_bbox[2], cur_bbox[3] + default_config.box_height)
                    if down_bbox not in observed_areas:
                        down_id = str(uuid.uuid4())
                        down_text = page.within_bbox(down_bbox).extract_text()
                        scanning_q.append(BlockNode(down_bbox, down_text, page_id, down_id))  # move down
                        vicinities[cur_bbox].append(down_id)
                
                observed_areas.append(cur_bbox)
                covered_areas.append(GraphNode(cur_bbox, cur_node.text, page_id, cur_node.id, vicinities[cur_bbox]))
            
            doc_graph.page_blocks[page_id] = covered_areas       
        
    
    return doc_graph

