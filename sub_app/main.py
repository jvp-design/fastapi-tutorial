from fastapi import Depends, FastAPI

from .dependencies import get_token_header, get_query_token

from .routers import users_router, items_router

app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users_router)  # users router
app.include_router(items_router)  # items router


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
