import asyncio
import base64

import aio_pika
import gino
from gino.ext.sanic import Gino
from sanic import Sanic, response
from sanic.response import json
from sanic_openapi import swagger_blueprint

db = Gino()


def code_base64():
    jpgtxt = base64.encodebytes(open("py.jpeg","rb").read())
    f = open("jpg1_b64.txt", "wb")
    f.write(jpgtxt)
    f.close()
    return str(jpgtxt)[:-3].replace("'","").replace("b","",1).replace(" ","")


""" Работа с бд """
class User(db.Model):
    __tablename__ = 'img'
    id = db.Column(db.Integer(), primary_key=True)
    picture = db.Column(db.Bytea())


async def main():
    await db.set_bind('postgresql://localhost/gino')
    await db.gino.create_all()
    img_code = code_base64()
    user = await User.create(picture = img_code)


asyncio.get_event_loop().run_until_complete(main())
