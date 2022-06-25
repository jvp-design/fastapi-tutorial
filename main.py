from datetime import datetime, time, timedelta
from enum import Enum
import time
from typing import Literal, Union
from uuid import UUID

from fastapi import (
    Body,
    Depends,
    FastAPI,
    Query,
    Path,
    Cookie,
    Header,
    status,
    Form,
    File,
    UploadFile,
    HTTPException,
    Request,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse

app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "hello world"}
#
#
# @app.post("/")
# async def post():
#     return {"message": "hello from the post route"}
#
#
# @app.put("/")
# async def put():
#     return {"message": "hello from the put route"}
#
#
# @app.get("/users")
# async def list_users():
#     return {"message": "list users route"}
#
#
# @app.get("/users/me")
# async def get_current_user():
#     return {"Message": "this is the current user"}
#
#
# @app.get("/users/{user_id}")
# async def get_user(user_id: str):
#     return {"user_id": user_id}
#
#
# class FoodEnum(str, Enum):
#     fruits = "fruits"
#     vegetables = "vegetables"
#     dairy = "dairy"
#
#
# @app.get("/foods/{food_name}")
# async def get_food(food_name: FoodEnum):
#     if food_name == FoodEnum.vegetables:
#         return {"food_name": food_name, "message": "you are healthy"}
#
#     if food_name.value == "fruits":
#         return {
#             "food_name": food_name,
#             "message": "you are still healthy, but like sweet things",
#         }
#     return {"food_name": food_name, "message": "i like chocolate milk"}
#
#
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
#
# @app.get("/old_items")
# async def list_old_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]
#
#
# @app.get("/items/{item_id}")
# async def get_item(
#     item_id: str, sample_query_param: str, q: str | None = None, short: bool = False
# ):
#     item = {"item_id": item_id, "sample_query_param": sample_query_param}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {
#                 "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut consectetur."
#             }
#         )
#     return item
#
#
# @app.get("/users/{user_id}/items/{item_id}")
# async def get_user_item(
#     user_id: int, item_id: str, q: str | None = None, short: bool = False
# ):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {
#                 "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut consectetur."
#             }
#         )
#         return item
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#
# @app.post("/items")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict
#
#
# @app.put("/items/{item_id}")
# async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result
#
#
# @app.get("/items")
# async def read_items(
#     q: str
#     | None = Query(
#         None,
#         min_length=3,
#         max_length=10,
#         title="Sample query string",
#         description="This is a sample query string.",
#         alias="item-query",
#     )
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# @app.get("/items_hidden")
# async def hidden_query_route(
#     hidden_query: str | None = Query(None, include_in_schema=False)
# ):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     return {"hidden_query": "Not found"}
#
#
# @app.get("/items_validation/{item_id}")
# async def read_items_validation(
#     *,
#     item_id: int = Path(..., title="The ID of the item to get", gt=10, le=100),
#     q: str = "hello",
#     size: float = Query(..., gt=0, lt=7.75)
# ):
#     results = {"item_id": item_id, "size": size}
#     if q:
#         results.update({"q": q})
#     return results


# Part 7 -> Body - Multiple Parameters
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#
# class User(BaseModel):
#     username: str
#     full_name: str | None = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int = Path(..., title="The ID of the item to get", ge=0, le=150),
#     q: str | None = None,
#     item: Item = Body(..., embed=True),
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     return results

## Part 8 -> Body - Fields
# class Item(BaseModel):
#     name: str
#     description: str | None = Field(
#         None, title="The description of the item", max_length=300
#     )
#     price: float = Field(..., gt=0, description="The price must be greater than zero.")
#     tax: float | None = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(..., embed=True)):
#     results = {"item_id": item_id, "item": item}
#     return results

## Part 9 -> Body - Nested Models
# class Image(BaseModel):
#     url: HttpUrl
#     name: str
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = []
#     image: list[Image] | None = None
#
#
# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     items: list[Item]
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results
#
#
# @app.post("/offers")
# async def create_offer(offer: Offer = Body(..., embed=True)):
#     return offer
#
#
# @app.post("/images/multiple")
# async def create_multiple_images(images: list[Image]):
#     return images
#
#
# @app.post("/blah")
# async def create_some_blahs(blahs: dict[int, float]):
#     return blahs

## Part 10 - Declare Request Example Data
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#     # class Config:
#     #     schema_extra = {
#     #         "example": {
#     #             "name": "Foo",
#     #             "description": "A very nice Item",
#     #             "price": 16.25,
#     #             "tax": 1.67,
#     #         }
#     #     }
#
#
# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Item = Body(
#         ...,
#         examples={
#             "normal": {
#                 "summary": "A normal example",
#                 "description": "A __normal__ item works _correctly_",
#                 "value": {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 16.25,
#                     "tax": 1.67,
#                 },
#             },
#             "converted": {
#                 "summary": "An example with converted data",
#                 "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
#                 "value": {"name": "Bar", "price": "16.25"},
#             },
#             "invalid": {
#                 "summary": "Invalid data is rejected with an error",
#                 "description": "Hello youtubers",
#                 "value": {"name": "Baz", "price": "sixteen point two five"},
#             },
#         },
#     ),
# ):
#     results = {"item_id": item_id, "item": item}
#     return results

## Part 11 - Extra Data Types
# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_date: datetime | None = Body(None),
#     end_date: datetime | None = Body(None),
#     repeat_at: time | None = Body(None),
#     process_after: timedelta | None = Body(None),
# ):
#     start_process = start_date + process_after
#     duration = end_date - start_process
#     return {
#         "item_id": item_id,
#         "start_date": start_date,
#         "end_date": end_date,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "start_process": start_process,
#         "duration": duration,
#     }

## Part 12 - Cookie and Header Parameters
# @app.get("/items")
# async def read_items(
#     cookie_id: str | None = Cookie(None),
#     accept_encoding: str | None = Header(None),
#     sec_ch_ua: str | None = Header(None),
#     user_agent: str | None = Header(None),
#     x_token: list[str] | None = Header(None),
# ):
#     return {
#         "cookie_id": cookie_id,
#         "Accept-Encoding": accept_encoding,
#         "sec-ch-ua": sec_ch_ua,
#         "User-Agent": user_agent,
#         "X-Token values": x_token,
#     }

## Part 13 - Response Model
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5
#     tags: list[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
#
#
# @app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]
#
#
# @app.post("/items/", response_model=Item)
# async def create_item(item: Item):
#     return item
#
#
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None
#
#
# class UserIn(UserBase):
#     password: str
#
#
# class UserOut(UserBase):
#     pass
#
#
# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn):
#     return user
#
#
# @app.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include={"name", "description"},
# )
# async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]
#
#
# @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
# async def read_items_public_data(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]

## Part 14 - Extra Models
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None
#
#
# class UserIn(UserBase):
#     password: str
#
#
# class UserOut(UserBase):
#     pass
#
#
# class UserInDB(UserBase):
#     hashed_password: str
#
#
# def fake_password_hasher(raw_password: str):
#     return f"supersecret{raw_password}"
#
#
# def fake_save_user(user_in: UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
#     print("User 'saved'.")
#     return user_in_db
#
#
# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved
#
#
# class BaseItem(BaseModel):
#     description: str
#     type: str
#
#
# class CarItem(BaseItem):
#     type = "car"
#
#
# class PlaneItem(BaseItem):
#     type = "plane"
#     size: int
#
#
# items = {
#     "item1": {"description": "All my friends drive a low rider", "type": "car"},
#     "item2": {
#         "description": "Music is my aeroplane, it's my aeroplane",
#         "type": "plane",
#         "size": 5,
#     },
# }
#
#
# @app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
# async def read_item(item_id: Literal["item1", "item2"]):
#     return items[item_id]
#
#
# class ListItem(BaseModel):
#     name: str
#     description: str
#
#
# list_items = [
#     {"name": "Foo", "description": "There comes my hero"},
#     {"name": "Red", "description": "It's my aeroplane"},
# ]
#
#
# @app.get("/list_items/", response_model=list[ListItem])
# async def read_items():
#     return items
#
#
# @app.get("/arbitrary", response_model=dict[str, float])
# async def get_arbitrary():
#     return {"foo": 1, "bar": "2"}

## Part 15 - Response Status Codes
# @app.post("/items/", status_code=status.HTTP_201_CREATED)
# async def create_item(name: str):
#     return {"name": name}
#
#
# @app.delete("/items/{pk}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_item(pk: str):
#     print("pk", pk)
#     return pk
#
#
# @app.get("/items/", status_code=status.HTTP_302_FOUND)
# async def read_items_redirect():
#     return {"hello": "world"}

## Part 16 - Form Fields
# @app.post("/login/")
# async def login(username: str = Form(...), password: str = Body(...)):
#     print("password", password)
#     return {"username": username}
#
#
# @app.post("/login-json/")
# async def login_json(username: str = Body(...), password: str = Body(...)):
#     print("password", password)
#     return {"username": username}

## Part 17 - Request Files
# @app.post("/files/")
# async def create_file(
#     files: list[bytes] = File(..., description="A file read as bytes")
# ):
#     return {"file_sizes": [len(file) for file in files]}
#
#
# @app.post("/uploadfile/")
# async def create_upload_file(
#     files: list[UploadFile] = File(..., description="A file read as UploadFile")
# ):
#     return {"filename": [file.filename for file in files]}
#
#
# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)

## Part 18 - Request Forms and Files
# @app.post("/files/")
# async def create_file(
#     file: bytes = File(...),
#     fileb: UploadFile = File(...),
#     token: str = Form(...),
#     hello: str = Body(...),
# ):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#         "hello": hello,
#     }


## Part 19 - Handling Errors
# items = {"foo": "The Foo Wrestlers"}
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(
#             status_code=404,
#             detail="Item not found",
#             headers={"X-Error": "There goes my error"},
#         )
#     return {"item": items[item_id]}
#
#
# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name
#
#
# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
#     )
#
#
# @app.get("/unicorns/{name}")
# async def read_unicorns(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}
#
#
# # @app.exception_handler(RequestValidationError)
# # async def validation_exception_handler(request, exc):
# #     return PlainTextResponse(str(exc), status_code=400)
# #
# #
# # @app.exception_handler(StarletteHTTPException)
# # async def http_exception_handler(request, exc):
# #     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
# #
# #
# # @app.get("/validation_items/{item_id}")
# # async def read_validation_items(item_id: int):
# #     if item_id == 3:
# #         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
# #     return {"item_id": item_id}
#
#
# # @app.exception_handler(RequestValidationError)
# # async def validation_exception_handler(request: Request, exc: RequestValidationError):
# #     return JSONResponse(
# #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
# #         content=jsonable_encoder({"detail": exc.errors(), "blahblah": exc.body}),
# #     )
# #
# #
# # class Item(BaseModel):
# #     title: str
# #     size: int
# #
# #
# # @app.post("/items/")
# # async def create_item(item: Item):
# #     return item
#
#
# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f"OMG! An HTTP error!: {repr(exc)}")
#     return await http_exception_handler(request, exc)
#
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     print(f"OMG! The client sent invalid data!: {exc}")
#     return await request_validation_exception_handler(request, exc)
#
#
# @app.get("/blah_items/{item_id}")
# async def read_items(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}

## Part 20 - Path Operation Configuration
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#
#
# class Tags(Enum):
#     items = "items"
#     users = "users"
#
#
# @app.post(
#     "/items/",
#     response_model=Item,
#     status_code=status.HTTP_201_CREATED,
#     tags=[Tags.items],
#     summary="Create an Item-type item",
#     # description="Create an item with all the information: "
#     # "name; description; price; tax; and a set of "
#     # "unique tags",
#     response_description="The created item",
# )
# async def create_item(item: Item):
#     """
#     Create an item with all the information:
#
#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item
#
#
# @app.get("/items/", tags=[Tags.items])
# async def read_items():
#     return [{"name": "Foo", "price": 42}]
#
#
# @app.get("/users/", tags=[Tags.users])
# async def read_users():
#     return [{"username": "PhoebeBuffay"}]
#
#
# @app.get("/elements/", tags=[Tags.items], deprecated=True)
# async def read_elements():
#     return [{"item_id": "Foo"}]

## Part 21a - JSON Compatible Encoder
# class Item(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     price: float | None = None
#     tax: float = 10.5
#     tags: list[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {
#         "name": "Bar",
#         "description": "The bartenders",
#         "price": 62,
#         "tax": 20.2,
#     },
#     "baz": {
#         "name": "Baz",
#         "description": None,
#         "price": 50.2,
#         "tax": 10.5,
#         "tags": [],
#     },
# }
#
#
# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items.get(item_id)
#
#
# @app.put("/items/{item_id}", response_model=Item)
# def update_item(item_id: str, item: Item):
#     update_item_encoded = jsonable_encoder(item)
#     items[item_id] = update_item_encoded
#     return update_item_encoded
#
#
# @app.patch("/items/{item_id}", response_model=Item)
# def patch_item(item_id: str, item: Item):
#     stored_item_data = items.get(item_id)
#     if stored_item_data is not None:
#         stored_item_model = Item(**stored_item_data)
#     else:
#         stored_item_model = Item()
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     return updated_item

## Part 22 - Dependencies Intro
# async def hello():
#     return "world"
#
#
# async def common_parameters(
#     q: str | None = None, skip: int = 0, limit: int = 100, blah: str = Depends(hello)
# ):
#     return {"q": q, "skip": skip, "limit": limit, "hello": blah}
#
#
# @app.get("/items/")
# async def read_items(commons: dict = Depends(common_parameters)):
#     return commons
#
#
# @app.get("/users/")
# async def read_users(commons: dict = Depends(common_parameters)):
#     return commons

## Part 23 - Classes as Dependencies
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
#
# class CommonQueryParams:
#     def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
#         self.q = q
#         self.skip = skip
#         self.limit = limit
#
#
# @app.get("/items/{item_id}")
# async def read_items(commons: CommonQueryParams = Depends()):
#     response = {}
#     if commons.q:
#         response.update({"q": commons.q})
#     items = fake_items_db[commons.skip : commons.skip + commons.limit]
#     response.update({"items": items})
#     return response

## Part 24 - Sub-Dependencies
# def query_extractor(q: str | None = None):
#     return q
#
#
# def query_or_body_extractor(
#     q: str = Depends(query_extractor), last_query: str | None = Body(None)
# ):
#     if q:
#         return q
#     return last_query
#
#
# @app.post("/item")
# async def try_query(query_or_body: str = Depends(query_or_body_extractor)):
#     return {"q_or_body": query_or_body}

## Part 25 - Dependencies in path operation decorators
# async def verify_token(x_token: str = Header(...)):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")
#
#
# async def verify_key(x_key: str = Header(...)):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key
#
#
# # app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
#
#
# @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
# async def read_items():
#     return [{"item": "Foo"}, {"item": "Bar"}]
#
#
# @app.get("/users/", dependencies=[Depends(verify_token), Depends(verify_key)])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]

## Part 26 - Security, First Steps
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# fake_users_db = {
#     "johndoe": dict(
#         username="johndoe",
#         full_name="John Doe",
#         email="johndoe@example.com",
#         hashed_password="fakehashedsecret",
#         disabled=False,
#     ),
#     "alice": dict(
#         username="alice",
#         full_name="Alice Wonderson",
#         email="alice@example.com",
#         hashed_password="fakehashedsecret2",
#         disabled=True,
#     ),
# }
#
#
# def fake_hash_password(password: str):
#     return f"fakehashed{password}"
#
#
# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def fake_decode_token(token):
#     return get_user(fake_users_db, token)
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}
#
#
# @app.get("/users/me")
# async def get_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
#
# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

## Part 27 - Security, OAuth2 Bearer and JWT
# SECRET_KEY = "thequickbrownfoxjumpedoverthelazydog"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$tJD64mRe0bd/UNdAANZtvuOnWDKScbVtXA9lB6X7arZxJQbAyMbd2",
#         "disabled": False,
#     }
# }
#
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# class TokenData(BaseModel):
#     username: str | None = None
#
#
# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not User:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive User")
#     return current_user
#
#
# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @app.get("/users/me", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
#
# @app.get("/users/me/items")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]

## Part 28 - Middleware and CORS
# class MyMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         start_time = time.time()
#         response = await call_next(request)
#         process_time = time.time() - start_time
#         response.headers["X-Process-Time"] = str(process_time)
#         return response
#
#
# origins = ["http://localhost:8000", "http://localhost:3000"]
# app.add_middleware(MyMiddleware)
# app.add_middleware(CORSMiddleware, allow_origins=origins)
#
# @app.get("/blah")
# async def blah():
#     return {"hello": "world"}
