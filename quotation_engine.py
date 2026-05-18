import os
from typing import Optional
from pydantic import BaseModel

QUOTE_PROMPT_TEMPLATE = (
    "You are a B2B quotation specialist for an industrial composite manufacturing company. "
    "Extract: product_type, quantity, specifications list, delivery_deadline, "
    "special_requirements, recommended_lead_time (working days), quote_notes. "
    "Return structured JSON.\n\nRFQ: {rfq_text}\nCategory: {product_category}\nVolume: {volume}"
)


class QuotationEngine:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.available = bool(api_key)
        if self.available:
            try:
                from langchain_openai import ChatOpenAI
                from langchain.prompts import ChatPromptTemplate
                self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key=api_key)
            except Exception:
                self.available = False

    async def generate(self, rfq_data: dict) -> dict:
        if not self.available:
            return self._demo_response(rfq_data)
        try:
            from langchain.prompts import ChatPromptTemplate
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a B2B quotation specialist for industrial composite manufacturing."),
                ("human", QUOTE_PROMPT_TEMPLATE)
            ])
            chain = prompt | self.llm
            result = await chain.ainvoke({
                "rfq_text": rfq_data.get("rfq_text", ""),
                "product_category": rfq_data.get("product_category", "composite"),
                "volume": rfq_data.get("required_volume", "not specified")
            })
            return {"customer_id": rfq_data["customer_id"], "status": "generated",
                    "quote_draft": result.content, "confidence": 0.87}
        except Exception as e:
            return self._demo_response(rfq_data)

    def _demo_response(self, rfq_data: dict) -> dict:
        return {
            "customer_id": rfq_data["customer_id"],
            "status": "demo_mode",
            "quote_draft": {
                "product_type": "carbon_fiber_composite",
                "quantity": rfq_data.get("required_volume", 100),
                "specifications": ["ISO 14125 compliant", "Fire retardant class B1"],
                "recommended_lead_time": 15,
                "quote_notes": ["Custom mold tooling required for <500 units"]
            },
            "confidence": 0.91
        }
