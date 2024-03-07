from fastapi import APIRouter, HTTPException, Depends, Header, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, AuthEvent
from app.helpers.database import get_db
from app.routers.admin.schema import GetHousesSchema, GetHouseInfoSchema
from app.routers.houses.crud import HousesCRUD
from fastapi.encoders import jsonable_encoder
from app.helpers.utils import is_signed_middleware
from app.settings import OWNER_PASSWORD

app = FastAPI()

router = APIRouter()


@router.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def sign_in():
    return [
        c.Page(
            components=[
                c.Form(
                    submit_url="/sign_in",
                    method="GOTO",
                    form_fields=[c.FormFieldInput(name="password", title="Please enter your password", required=True)],

                )
            ]
        )
    ]


@router.get("/api/sign_in", response_model=FastUI, response_model_exclude_none=True)
async def auth(password: str):
    token = f"Token {password}"
    headers = {"Authorization": token}

    if token == OWNER_PASSWORD:
        return c.FireEvent(event=AuthEvent(token=password, url="/houses"))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/api/houses", response_model=FastUI, response_model_exclude_none=True)
@is_signed_middleware
async def houses_table(authorization: str = Header(...), db: AsyncSession = Depends(get_db)) -> list[AnyComponent]:
    token = authorization.split(" ")[1]

    obj_type = "house"

    house_data = await HousesCRUD.read_houses(db)

    houses = GetHousesSchema(data=jsonable_encoder(house_data)).data

    return [
        c.Page(
            components=[
                c.Navbar(title="Houses",
                         start_links=[c.Link(components=[c.Text(text='Rent Houses')], on_click=GoToEvent(url='')),
                                      c.Link(components=[c.Text(text='Apartments')], on_click=GoToEvent(url='')),
                                      c.Link(components=[c.Text(text='Rent Apartments')]),
                                      ]),
                c.Table(
                    data=houses,
                    data_model=GetHousesSchema,
                    no_data_message="No houses found",
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url=f'/{{id}}/{token}/{obj_type}')),
                        DisplayLookup(field='address'),
                        DisplayLookup(field='price'),
                        DisplayLookup(field='created_statement'),
                        DisplayLookup(field='updated_statement'),
                    ],
                ),
            ]
        ),
    ]


@router.get("/api/{house_id}/{token}/{obj_type}", response_model=FastUI, response_model_exclude_none=True)
async def tokenized(house_id: int, token: str, obj_type: str):
    return c.FireEvent(event=AuthEvent(token=token, url=f"/{obj_type}/{house_id}/"))


@router.get("/api/house/{house_id}/", response_model=FastUI, response_model_exclude_none=True)
@is_signed_middleware
async def user_profile(house_id: int, db: AsyncSession = Depends(get_db), authorization: str = Header(...)) -> list[AnyComponent]:

    house_data = await HousesCRUD.read_houses(db)

    houses = GetHouseInfoSchema(data=jsonable_encoder(house_data)).data

    try:
        house = next(house for house in houses if house.id == house_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="House not found")
    return [
        c.Page(
            components=[
                c.Heading(text='House', level=2),
                c.Heading(text=("Id: " + str(house.id)), level=3),
                c.Details(data=house, fields=[
                    DisplayLookup(field='url'),
                    DisplayLookup(field='address'),
                    DisplayLookup(field='price'),
                    DisplayLookup(field='land_info'),
                    DisplayLookup(field='short_info', mode=DisplayMode.json),
                    DisplayLookup(field='created_statement'),
                    DisplayLookup(field='updated_statement'),
                ]),
                c.Navbar(start_links=[
                    c.Link(components=[c.Text(text='Houses')], on_click=GoToEvent(url='/houses')),
                    c.Link(components=[c.Text(text='Rent Houses')], on_click=GoToEvent(url='')),
                    c.Link(components=[c.Text(text='Apartments')], on_click=GoToEvent(url='')),
                    c.Link(components=[c.Text(text='Rent Apartments')]),
                ]),
            ]
        ),
    ]


@router.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='Houses Data'))
