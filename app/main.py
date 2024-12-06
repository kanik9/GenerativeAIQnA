import json
import html2text 
from playwright.async_api import async_playwright
from fastapi.responses import JSONResponse
from fastapi import APIRouter, status

from app.models import QnABody
from app.utils import answer_generator

document_qna = APIRouter(
    prefix="/qna",
    tags=["QnA on Context"]
)

async def context_extractor(context: str) -> str:
    content: str = ""
    try:
        if "http" in context or "https" in context:
            async with async_playwright() as playwright_obj:
                browser = await playwright_obj.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(context, wait_until="domcontentloaded")
                await page.wait_for_timeout(5000)
                
                for html_tag in ["nav", "footer", 'iframe', "script", "noscript", "spam", "section", "style", "samp", "progress", "output", "noframes", "meta", "menu", "map"]:
                    await page.evaluate(f"""
                                        const html_tag = document.querySelectorAll('{html_tag}');
                                        html_tag.forEach(tag => tag.remove());
                                    """)
                    
                    html_body = await page.content()
                    
                    # Convert HTML to Markdown
                    markdown_converter = html2text.HTML2Text()
                    markdown_converter.ignore_links = False  # Keep hyperlinks
                    markdown = markdown_converter.handle(html_body)
                    content = markdown
                
                await page.close()      
        else:
            content = context
    except Exception as error:
        raise error
    else:
        return content


@document_qna.post("/context/")
async def qna_on_context(req: QnABody) -> JSONResponse:
    res: dict = {}
    try: 
        user_query: str = req.query
        
        processed_context = await context_extractor(req.context)
        print(processed_context)  
        answer: str = await answer_generator(content=processed_context, query=user_query)
        res = {
        "query": user_query,
        "answer": answer.get("content"),
        "max_token": answer.get('response_metadata').get('token_usage')
    }
    except Exception as error:
        return JSONResponse(
            content=f"{error}",
            status_code= status.HTTP_400_BAD_REQUEST
            )
    else:        
        return JSONResponse(
            content=json.dumps(res),
            status_code=status.HTTP_200_OK
        )