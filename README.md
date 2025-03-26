# Ontological Document Extraction Using LLM (onto-doc-extract)

## Overview

This project focuses on reading and analyzing PDF documents using a structural scanning approach, ontological reasoning, and LLM-based fact checking. The document is transformed into a graph, where text blocks serve as nodes, and their relationships are defined based on spatial positioning. The extracted information is structured into an RDF graph and validated using a fine-tuned LLM before being presented in XML format. The final application is deployed using FAST-API and Docker on AWS.

## Features

- **Read PDF Document**
- **Document Scanning**:
  - Starts from the top-left (or top-right for RTL documents) corner
  - Uses a predefined bounding box
  - Implements Breadth-First Scanning (BFS) where movement options are one step to the right or down
- **Graph Transformation**:
  - Represents the document as a graph
  - Each text block is a node
  - Nodes have relationships with neighbors:
    - `horizontalRelated` (right)
    - `verticalRelated` (down)
  - Relations follow an RDF-like triple format (Subject-Predicate-Object)
  - Relations are directed but traversable in both directions
- **Ontology and Knowledge Representation**:
  - Constructs an RDF graph of the document (convertible to XML)
  - Defines a domain-specific ontology based on the use case, subset of the general document-extraction ontology, which is gradually expanded and improved.
  - Grounds triples to predefined ontological rules (e.g., `item hasPrice price`)
- **Validation and AI Enhancement**:
  - Uses a fine-tuned LLM for triple validation
  - Utilizes the ontology as a classifier stage for fine-tuning
  - Stores model weights and feeds them back into the model for reinforcement
- **Information Extraction and Representation**:
  - Extracts high-weighted grounded triples as retrieved information
  - Represents extracted information in XML format
- **Deployment**:
  - Uses FAST-API for the application
  - Dockerizes the application
  - Deploys on AWS
