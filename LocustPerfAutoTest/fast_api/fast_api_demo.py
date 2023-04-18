#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @Time : 2022/1/20 14:50
# @Author : hushaozhong
# @File : fast_api_demo.py
# @Software: PyCharm
import base64
import time
import urllib.parse
from typing import Optional
import uuid
from fastapi import FastAPI, Query, Body, Header
import uvicorn

app = FastAPI()


@app.get("/get/test/one/demo_api")
async def read_item(username: Optional[str] = Query(default=...,
                                                    min_length=3,
                                                    max_length=20,
                                                    regex="^ECS.*测试$")
                    ):
    time.sleep(0.3)
    sign = str(base64.b64encode(str(urllib.parse.unquote(username)).encode('utf-8')), 'utf-8')
    resp = {
        "code": 0,
        "msg": "OK",
        "data": {
            "rows": [
                {
                    "supplier": uuid.uuid1()
                },
                {
                    "supplierName": username
                }
            ],
            "rowTotal": 0
        },
        "traceId": sign
    }
    print(resp)
    return resp


@app.post("/post/test/one/demo_api")
async def create_item(sign: Optional[str] = Header(default=...),
                      param: Optional[str] = Header(default=None),
                      username: Optional[dict] = Body(default=...)
                      ):
    time.sleep(0.3)
    data = base64.b64decode(sign).decode('utf-8')
    try:
        resp = {
            "code": 0,
            "msg": "OK",
            "data": {
                "rows": [
                    {
                        "supplierName": data,
                        "UUID": uuid.uuid1()
                    },
                    {
                        "supplierName": "测试接口1"
                    },
                    username
                ],
                "rowTotal": 1
            },
            "traceId": sign
        }
        if data == username.get('username'):
            if param is not None:
                resp.update({"param": param})
                print(resp)
                return resp
            print(resp)
            return resp
        else:
            return {"msg": "接口权限错误！"}
    except Exception as e:
        return {"msg": e}


@app.post("/post/test/two/demo_api")
async def create_item(sign: Optional[str] = Header(default=...),
                      param: Optional[str] = Header(default=None),
                      username: Optional[dict] = Body(default=None)
                      ):
    time.sleep(1)
    data = base64.b64decode(sign).decode('utf-8')
    try:
        resp = {
            "code": 0,
            "msg": "OK",
            "data": {
                "rows": [
                    {
                        "supplierName": data,
                        "UUID": uuid.uuid1()
                    },
                    {
                        "supplierName": "测试接口2"
                    },
                    username
                ],
                "rowTotal": 2
            },
            "traceId": sign
        }
        if data == username.get('username'):
            if param is not None:
                resp.update({"param": param})
                print(resp)
                return resp
            print(resp)
            return resp
        else:
            return {"msg": "接口权限错误！"}
    except Exception as e:
        return {"msg": e}


@app.post("/post/test/three/demo_api")
async def create_item(sign: Optional[str] = Header(default=...),
                      param: Optional[str] = Header(default=None),
                      username: Optional[dict] = Body(default=None)
                      ):
    time.sleep(2)
    data = base64.b64decode(sign).decode('utf-8')
    try:
        resp = {
            "code": 0,
            "msg": "OK",
            "data": {
                "rows": [
                    {
                        "supplierName": data,
                        "UUID": uuid.uuid1()
                    },
                    {
                        "supplierName": "测试接口3"
                    },
                    username
                ],
                "rowTotal": 3
            },
            "traceId": sign
        }
        if data == username.get('username'):
            if param is not None:
                resp.update({"param": param})
                print(resp)
                return resp
            print(resp)
            return resp
        else:
            return {"msg": "接口权限错误！"}
    except Exception as e:
        return {"msg": e}


@app.post("/post/test/four/demo_api")
async def create_item(sign: Optional[str] = Header(default=...),
                      param: Optional[str] = Header(default=None),
                      username: Optional[dict] = Body(default=None)
                      ):
    time.sleep(3)
    data = base64.b64decode(sign).decode('utf-8')
    try:
        resp = {
            "code": 0,
            "msg": "OK",
            "data": {
                "rows": [
                    {
                        "supplierName": data,
                        "UUID": uuid.uuid1()
                    },
                    {
                        "supplierName": "测试接口4"
                    },
                    username
                ],
                "rowTotal": 4
            },
            "traceId": sign
        }
        if data == username.get('username'):
            if param is not None:
                resp.update({"param": param})
                print(resp)
                return resp
            print(resp)
            return resp
        else:
            return {"msg": "接口权限错误！"}
    except Exception as e:
        return {"msg": e}


if __name__ == '__main__':
    uvicorn.run(app='fast_api_demo:app', host='127.0.0.1', port=8888, reload=True, debug=True)
