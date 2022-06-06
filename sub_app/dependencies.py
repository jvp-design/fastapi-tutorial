from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header('fake-super-secret-token')):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header Invalid")


async def get_query_token(token: str = "jessica"):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
