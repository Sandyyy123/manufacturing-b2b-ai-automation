import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Manufacturing B2B AI Automation",
    description="Quotation automation, pricing intelligence, and repeat-order workflows",
    version="1.0.0"
)

from quotation_engine import QuotationEngine
from pricing_intelligence import PricingIntelligence
from repeat_order_workflow import RepeatOrderWorkflow
from rag_catalog import CatalogRAG

quotation_engine = QuotationEngine()
pricing_intel = PricingIntelligence()
repeat_orders = RepeatOrderWorkflow()
catalog_rag = CatalogRAG()


class RFQInput(BaseModel):
    customer_id: str
    rfq_text: str
    product_category: Optional[str] = None
    required_volume: Optional[int] = None
    deadline: Optional[str] = None


class PriceScoreInput(BaseModel):
    product_id: str
    proposed_price: float
    volume: int
    customer_tier: str = "standard"


class CatalogQuery(BaseModel):
    query: str
    top_k: int = 5


@app.post("/quote/generate")
async def generate_quote(rfq: RFQInput):
    result = await quotation_engine.generate(rfq.dict())
    if not result:
        raise HTTPException(status_code=422, detail="Could not parse RFQ")
    return result


@app.post("/pricing/score")
async def score_price(data: PriceScoreInput):
    score = pricing_intel.score(data.dict())
    return score


@app.get("/orders/repeat-candidates")
async def get_repeat_candidates(customer_id: Optional[str] = None, min_confidence: float = 0.7):
    candidates = repeat_orders.get_candidates(customer_id=customer_id, min_confidence=min_confidence)
    return {"candidates": candidates, "count": len(candidates)}


@app.post("/catalog/search")
async def search_catalog(query: CatalogQuery):
    results = catalog_rag.search(query.query, top_k=query.top_k)
    return {"results": results, "query": query.query}


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
