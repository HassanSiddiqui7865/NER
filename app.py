from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import spacy
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global model variable
nlp = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load the model
    global nlp
    try:
        logger.info("Loading MED7 model...")
        nlp = spacy.load("en_core_med7_lg")
        logger.info("MED7 model loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load MED7 model: {e}")
        raise
    yield
    # Shutdown: Cleanup if needed
    nlp = None

app = FastAPI(
    title="MED7 NER API",
    description="Medical Named Entity Recognition API using MED7 model",
    version="1.0.0",
    lifespan=lifespan
)

# Request/Response models
class TextInput(BaseModel):
    text: str

class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int

class NERResponse(BaseModel):
    text: str
    entities: List[Entity]
    entity_count: int

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "MED7 NER API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": nlp is not None
    }

@app.post("/extract", response_model=NERResponse, tags=["NER"])
async def extract_entities(input_data: TextInput):
    """
    Extract medical entities from text.
    
    MED7 entity types:
    - DOSAGE: Medication dosage information
    - DRUG: Medication names
    - DURATION: Duration of medication
    - FORM: Medication form (tablet, capsule, etc.)
    - FREQUENCY: Frequency of administration
    - ROUTE: Route of administration
    - STRENGTH: Medication strength
    """
    if nlp is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Process the text
        doc = nlp(input_data.text)
        
        # Extract entities
        entities = [
            Entity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char
            )
            for ent in doc.ents
        ]
        
        return NERResponse(
            text=input_data.text,
            entities=entities,
            entity_count=len(entities)
        )
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.post("/extract/batch", tags=["NER"])
async def extract_entities_batch(texts: List[str]):
    """
    Extract medical entities from multiple texts in batch.
    """
    if nlp is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not texts:
        raise HTTPException(status_code=400, detail="Texts list cannot be empty")
    
    results = []
    for text in texts:
        try:
            doc = nlp(text)
            entities = [
                {
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                }
                for ent in doc.ents
            ]
            results.append({
                "text": text,
                "entities": entities,
                "entity_count": len(entities)
            })
        except Exception as e:
            logger.error(f"Error processing text in batch: {e}")
            results.append({
                "text": text,
                "error": str(e),
                "entities": [],
                "entity_count": 0
            })
    
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
