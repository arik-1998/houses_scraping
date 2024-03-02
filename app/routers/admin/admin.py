from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, AuthEvent
from app.helpers.database import get_db
from app.routers.admin.schema import GetHousesSchema, GetHouseInfoSchema
from app.routers.houses.crud import HousesCRUD
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def sign_in():
    return [
        c.Page(
            components=[
                c.Button(text="Sign in imitation", on_click=GoToEvent(url="/houses"))
                # c.Form(
                #     submit_url="/api/houses",
                #     form_fields=[c.FormFieldInput(name="sign_in", title="Please enter your password", required=True)],
                # )
            ]
        )
    ]


@router.get("/api/houses", response_model=FastUI, response_model_exclude_none=True)
async def users_table(db: AsyncSession = Depends(get_db)) -> list[AnyComponent]:

    house_data = await HousesCRUD.read_houses(db)
    
    houses = GetHousesSchema(data = jsonable_encoder(house_data)).data


    return [
        c.Page(  
            components=[
                c.Navbar(title="Houses",start_links=[c.Link(components=[c.Text(text='Rent Houses')], on_click=GoToEvent(url='')),
                                                    c.Link(components=[c.Text(text='Appartaments')], on_click=GoToEvent(url='')),
                                                    c.Link(components=[c.Text(text='Rent Appartamnets')]),
                                                        ]),
                c.Table(
                    data=houses,
                    
                    columns=[
                        DisplayLookup(field='id',on_click=GoToEvent(url='/house/{id}/')),
                        DisplayLookup(field='adress'),
                        DisplayLookup(field='price'),
                        DisplayLookup(field='created_statement'),
                        DisplayLookup(field='updated_statement'),
                    ],
                ),
            ]
        ),
    ]


@router.get("/api/house/{house_id}/", response_model=FastUI, response_model_exclude_none=True)
async def user_profile(house_id: int, db: AsyncSession = Depends(get_db)) -> list[AnyComponent]:

    house_data = await HousesCRUD.read_houses(db)

    houses = GetHouseInfoSchema(data = jsonable_encoder(house_data)).data

    try:
        house = next(house for house in houses if house.id == house_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="House not found")
    return [
        c.Page(
            components=[
                c.Heading(text='House', level=2),
                c.Heading(text=("Id: " + str(house.id)), level=3),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=house, fields=[
                                              DisplayLookup(field='url'),
                                              DisplayLookup(field='adress'),
                                              DisplayLookup(field='price'),
                                              DisplayLookup(field='land_info'),
                                              DisplayLookup(field='short_info', mode=DisplayMode.json),
                                              DisplayLookup(field='created_statement'),
                                              DisplayLookup(field='updated_statement'),               
                                              ]),
                c.Navbar(start_links=[
                                        c.Link(components=[c.Text(text='Houses')], on_click=GoToEvent(url='/houses')),
                                        c.Link(components=[c.Text(text='Rent Houses')], on_click=GoToEvent(url='')),
                                        c.Link(components=[c.Text(text='Appartaments')], on_click=GoToEvent(url='')),
                                        c.Link(components=[c.Text(text='Rent Appartamnets')]),
                                        ]),
            ]
        ),
    ]


@router.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='Houses Data'))
