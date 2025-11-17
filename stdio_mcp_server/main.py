import asyncio
import logging
from typing import Dict, Any

import httpx
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# 1) Server + Tools
# ---------------------------------------------------------
async def serve():

    mcp = FastMCP(name="Facilities_Analysis_MCP_Server")

    BASE_URL = "http://49.12.77.163:8001"

    # ---------------------------------------------------------
    # POST Tool
    # ---------------------------------------------------------
    @mcp.tool(
        name="analyze_facilities",
        description="""
        POST /api/ai/analysis/facilities
        Analyze banking facilities and return the AI-generated analytical paragraphAnalyze banking facilities and return the AI-generated analytical paragraph.
        """,
    )
    async def analyze_facilities(
        bankName: str,
        ageOfRelationship: float,
        totalUtilization: int,
        language: str = "English",
    ) -> Dict[str, Any]:

        endpoint = "/api/ai/analysis/facilities"

        payload = {
            "bankName": bankName,
            "ageOfRelationship": ageOfRelationship,
            "totalUtilization": totalUtilization,
            "language": language,
        }

        headers = {
            "Content-Type": "application/json",
            "Accept-Language": "en",
            "X-TraceId": "MCP-Request",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BASE_URL}{endpoint}",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()

                return {"success": True, "data": response.json()}

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error: {e}")
            return {
                "success": False,
                "status_code": e.response.status_code,
                "error": e.response.text,
            }

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"success": False, "error": str(e)}

    # ---------------------------------------------------------
    # GET Tool
    # ---------------------------------------------------------
    @mcp.tool(
        name="get_analysis_result",
        description="Retrieve the generated AI facility analysis by analysisId.",
    )
    async def get_analysis_result(analysisId: str) -> Dict[str, Any]:

        endpoint = "/api/ai/get_analysis_result"
        url = f"{BASE_URL}{endpoint}?analysisId={analysisId}"

        headers = {
            "Accept-Language": "en",
            "X-TraceId": "MCP-Request",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return {"success": True, "data": response.json()}

        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "status_code": e.response.status_code,
                "error": e.response.text,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    return mcp


# ---------------------------------------------------------
# 2) main()
# ---------------------------------------------------------
def main():

    async def _run():
        server = await serve()
        logger.info("Starting Facilities Analysis MCP Server...")
        return server

    server = asyncio.run(_run())
    server.run()


# ---------------------------------------------------------
# 3) Runner
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
