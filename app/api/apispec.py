from flasgger import APISpec
from .calls import create_call, get_bill
from .schemas import StartEndCallSchema, BillSchema, BillDetailSchema


spec = APISpec(
    title="Olist Technical Challenge - REST api",
    version='1.0',
    plugins=[
        'apispec.ext.flask',
        'apispec.ext.marshmallow',
    ],
    contact={
        "name": "André Felipe Dias",
        "url": "https://pronus.io",
        "email": "andre.dias@pronus.io",
    },
    route='/v1/spec',
)

definitions = [StartEndCallSchema, BillSchema, BillDetailSchema]
paths = [create_call, get_bill]
