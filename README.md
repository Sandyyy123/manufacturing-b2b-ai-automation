# Manufacturing B2B AI Automation

AI-powered tools for B2B manufacturing workflows: quotation automation, pricing intelligence, and repeat-order pipelines.

## Architecture

```
manufacturing-b2b-ai-automation/
├── main.py                    # FastAPI entry point
├── quotation_engine.py        # LLM-powered quote generation
├── pricing_intelligence.py    # ML pricing model + margin optimization
├── repeat_order_workflow.py   # Repeat-order detection and automation
├── erp_connector.py           # ERP/CRM integration abstraction
├── rag_catalog.py             # RAG over product catalog / specs
└── requirements.txt
```

## Features

- **Quotation Automation** - parse RFQ PDFs, extract requirements, generate structured quotes via LLM
- **Pricing Intelligence** - historical order analysis, competitor benchmarking, margin scoring
- **Repeat-Order Workflows** - detect repeat patterns, auto-generate PO drafts for approval
- **RAG over Product Catalog** - semantic search over composite specs, certifications, datasheets
- **ERP/CRM Integration** - SAP / HubSpot / Salesforce connectors via unified abstraction layer

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in OPENAI_API_KEY and DB_URL
python main.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /quote/generate | Generate quote from RFQ input |
| POST | /pricing/score | Score a price for margin + competitiveness |
| GET  | /orders/repeat-candidates | List orders likely to recur |
| POST | /catalog/search | Semantic search over product catalog |

## Stack

Python 3.11 - FastAPI - LangChain - OpenAI GPT-4 - PostgreSQL - ChromaDB - Docker
