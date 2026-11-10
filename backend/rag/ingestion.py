import os
import re
from typing import List, Dict, Any
from pathlib import Path

try:
    from langchain.document_loaders import UnstructuredFileLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGAVAILABLE = True
except ImportError:
    LANGAVAILABLE = False


class DocumentIngestion:
    """Handle document ingestion for the agriculture knowledge base."""
    
    def __init__(self, knowledge_base_path: str = "data/knowledge_base"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def load_text_files(self) -> List[Any]:
        """Load all text documents from the knowledge base directory."""
        documents = []
        
        if not self.knowledge_base_path.exists():
            print(f"Knowledge base directory not found: {self.knowledge_base_path}")
            return documents
        
        for filepath in self.knowledge_base_path.rglob("*"):
            if filepath.is_file():
                try:
                    if filepath.suffix.lower() in [".txt", ".md", ".csv"]:
                        loader = TextLoader(str(filepath), encoding="utf8")
                        docs = loader.load()
                        documents.extend(docs)
                        print(f"Loaded: {filepath.name}")
                    elif filepath.suffix.lower() in [".pdf"]:
                        # PDF loading would require additional dependency
                        print(f"PDF support coming soon: {filepath.name}")
                    else:
                        print(f"Unsupported file type: {filepath.suffix}")
                except Exception as e:
                    print(f"Error loading {filepath.name}: {e}")
        
        return documents
    
    def split_documents(self, documents: List[Any]) -> List[Any]:
        """Split documents into chunks for embedding."""
        if not documents:
            return []
        
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks
    
    def ingest_all(self) -> List[Any]:
        """Full ingestion pipeline: load and split documents."""
        documents = self.load_text_files()
        chunks = self.split_documents(documents)
        return chunks


class KnowledgeBaseManager:
    """Manage the agriculture knowledge base content."""
    
    @staticmethod
    def init_sample_knowledge_base(base_path: str = "data/knowledge_base"):
        """Initialize sample knowledge base documents if they don't exist."""
        kb_dir = Path(base_path)
        kb_dir.mkdir(parents=True, exist_ok=True)
        
        # Sample documents - in production, these would be comprehensive guides
        samples = {
            "crop_guides.txt": """
## Rice Cultivation Guide

**Growth Stages:**
- Germination (0-14 days): Maintain saturated soil conditions
- Vegetative (15-30 days): Ensure adequate nitrogen
- Tillering (31-60 days): Monitor tiller number per hill
- Panicle Initiation (61-90): Critical stage for nutrient uptake
- Flowering (91-120): Ensure water availability
- Grain Filling (121-150): Maintain optimal soil moisture
- Maturity (151+): Harvest when 80% grains are golden yellow

**Nutrient Management:**
- Nitrogen: 120-150 kg/ha (basal + topdress)
- Phosphorus: 40-60 kg/ha at sowing
- Potassium: 40-50 kg/ha at tillering

**Pest Management:**
- Monitor for stem borer, leaf roller, leaf blight
- Use integrated pest management approach
            """,
            "fertilizer_guidelines.txt": """
## Fertilizer Recommendations

**Basal Application (at planting):**
- 50% of total Nitrogen requirement
- 100% of Phosphorus requirement (P2O5)
- 100% of Potassium requirement (K2O)

**Topdressing (split applications):**
- Remaining 50% Nitrogen at tillering stage
- Apply based on soil test results
- Timing: 30-40 days after sowing for rice

**Organic Fertilizers:**
- Compost: 5-10 tons/ha
- Farmyard manure: 10-15 tons/ha
- Apply 2-3 weeks before planting
            """,
            "irrigation_guides.txt": """
## Irrigation Practices

**Rice:**
- Maintain 5-7 cm water depth during tillering to flowering
- Alternate Wetting and Drying (AWD) can save 15-30% water
- Irrigate when field water depth drops to 5 cm
- Avoid water stress during panicle initiation

**Wheat:**
- Irrigation at crown root initiation (30 DAS)
- Critical stage: flowering to grain filling
- Avoid irrigation 2 weeks before harvest
- Apply 5-7 cm irrigation per session

**General Principles:**
- Irrigation scheduling based on soil moisture tension
- Early morning irrigation reduces evaporation losses
- Monitor rainfall and adjust irrigation accordingly
            """,
            "pest_disease_management.txt": """
## Pest and Disease Management

**Common Rice Pests:**
- Stem Borer: Yellowing leaves, dead hearts
- Leaf Roller: Rolled leaves, web formation
- Green Leafhopper: Yellowing, stuntiness

**Common Rice Diseases:**
- Blast: Diamond-shaped lesions on leaves
- Brown Spot: Small brown spots on leaves
- Bacterial Leaf Blight: Yellowing V-shaped lesions

**Integrated Pest Management (IPM):**
1. Regular field monitoring (twice weekly)
2. Use resistant varieties when available
3. Apply pesticides only when economic threshold is exceeded
4. Use biocontrol agents (Trichoderma, Bacillus)
5. Follow pre-harvest interval for chemical pesticides

**General Prevention:**
- Seed treatment with fungicides
- Field sanitation and removal of crop residues
- Crop rotation to break pest cycles
            """,
        }
        
        for filename, content in samples.items():
            file_path = kb_dir / filename
            if not file_path.exists():
                with open(file_path, "w", encoding="utf8") as f:
                    f.write(content.strip())
                print(f"Created sample: {filename}")
        
        return kb_dir