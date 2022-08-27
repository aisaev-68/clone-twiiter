from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates




BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH))

app = FastAPI(
    title="Twitter API",
    description="This is a copy of Twitter API",
    version="1.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Users Routes",
        },
        {
            "name": "Tweets",
            "description": "Tweets Routes",
        }
    ]
)

RECIPES = {
 "id": 1,
 "label": "Chicken Vesuvio",
 "source": "Serious Eats",
 "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
 }

@app.get("/", status_code=200)
def root(request: Request) -> dict:
    """ Root GET """

    return TEMPLATES.TemplateResponse(
        "/templates/index.html",
        {"request": request, "recipes": RECIPES},
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="task5:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )