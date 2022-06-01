"""
下载接口
"""

import json
import time
import random
from math import floor
from turtle import down
from django.http import JsonResponse, FileResponse
from core.api.status_code import HttpStatusCode, RetStatusCode, RetMessage


def decide_tile_layer(x, y):
    over = False
    left_x = x - 640
    if left_x < 0:
        left_x = left_x + 3840
        over = True
    right_x = x + 640
    if right_x > 3840:
        right_x = right_x - 3840
        over = True
    up_y = y - 360
    down_y = y + 360
    if up_y < 0:
        down_y = 720
        up_y = 0
    if down_y > 1920:
        up_y = 1200
        down_y = 1920
    # print(str(left_x) + ' ' + str(right_x) + ' ' + str(up_y) + ' ' + str(down_y))
    res = []
    begin_tile_x = floor(left_x / 320) - 1
    for i in range(12):
        tile_x = (i + begin_tile_x) % 12
        for tile_y in range(8):
            if tile_y * 240 >= down_y or tile_y * 240 + 240 <= up_y:
                continue
            if not over:
                if tile_x * 320 > right_x or tile_x * 320 + 320 < left_x:
                    continue
            else:
                if tile_x * 320 > right_x and tile_x * 320 + 320 < left_x:
                    continue
            res.append([tile_x, tile_y])
    # print(res)
    return res


def tile_list(request):
    if request.method == 'POST':
        request_json = json.loads(request.body.decode(encoding="utf-8"))
        try:
            seg = int(request_json['seg'])
            viewpoint_x = int(request_json['viewpoint_x'])
            viewpoint_y = int(request_json['viewpoint_y'])
        except Exception:
            ret = {
                'status_code': RetStatusCode.STAT_DATA_INVALID,
                'detail': RetMessage.MSG_DATA_INVALID
            }
            return JsonResponse(ret, status=HttpStatusCode.RET_GENERAL_ERROR)

        res = decide_tile_layer(viewpoint_x, viewpoint_y)

        data = {
            'status_code': RetStatusCode.STAT_SUCCESS,
            'res': res
        }
        return JsonResponse(data, status=HttpStatusCode.RET_SUCCESS)
    return JsonResponse({"status_code": RetStatusCode.STAT_GENERAL_OTHER_ERR,
                         "detail": RetMessage.MSG_UNKNOWN_ERROR}, status=HttpStatusCode.RET_OTHER_ERROR)


def download(request):
    if request.method == 'POST':
        request_json = json.loads(request.body.decode(encoding="utf-8"))
        try:
            seg = int(request_json['seg'])
            tile_x = int(request_json['x'])
            tile_y = int(request_json['y'])
            layer = int(request_json['layer'])
        except Exception:
            response = {
                'status_code': RetStatusCode.STAT_DATA_INVALID,
                'detail': RetMessage.MSG_DATA_INVALID
            }
            return JsonResponse(response, status=HttpStatusCode.RET_GENERAL_ERROR)

        # TODO: change to linux
        time.sleep(random.choice([0.01, 0.02, 0.03, 0.04]))
        file_name = '..\\..\\static_svc\\seg' + str(seg) + '_tile' + str(tile_x) + '_' + str(tile_y) + '_L' + str(layer) + '.svc'
        file = open(file_name,'rb')
        try:
            response =FileResponse(file)  
            response['Content-Type']='application/octet-stream'  
            response['Content-Disposition']='attachment;filename="' + file_name + '"'  
            return response 
        except Exception:
            return JsonResponse({"status_code": RetStatusCode.STAT_GENERAL_OTHER_ERR,
                         "detail": RetMessage.MSG_DATA_INVALID}, status=HttpStatusCode.RET_OTHER_ERROR)

    return JsonResponse({"status_code": RetStatusCode.STAT_GENERAL_OTHER_ERR,
                         "detail": RetMessage.MSG_UNKNOWN_ERROR}, status=HttpStatusCode.RET_OTHER_ERROR)