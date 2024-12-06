from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app import document_qna

app = FastAPI(
    title="SE/ML technical challenge",
    description="Technical Assignment Provided by the Open Inncovation Company",
    version="0.0.1",
    contact={
        "name": "Kanik Vijay",
        "email": "kanikvijay.it20@gmail.com",
        "phone_number": "7611879062"
    },
)

# Handling the CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POSt"],
    allow_headers=["*"],
)


# Testing Route
@app.get(
    "/test",
    tags=["Testing Endpoint"]
)
async def test() -> JSONResponse:
    """
    Normal Testing Function to test that application is running or not
    :return: JSONResponse
    """
    return JSONResponse(
        content="Your Application is running. This is testing Endpoint!",
        status_code= status.HTTP_200_OK
    )


@app.get(
    "/detailedProblem",
    tags=["Testing Endpoint"]
)
async def getProblemStatement() -> JSONResponse:
    return JSONResponse(
        content="""We have a collection of internal documents, and we want to implement a document-based GPT system that can answer
questions based on their content. The primary goal is to enable users to ask questions about these documents and
receive short, precise, and well-sourced answers. Each answer should include a link to the specific part of the document
where the information was found, allowing users to verify the information directly.""",
        status_code=status.HTTP_200_OK
    )


# Including the app routes
app.include_router(document_qna)