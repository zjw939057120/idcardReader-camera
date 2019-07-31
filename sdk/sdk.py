# -*- coding: UTF-8 -*-
import ctypes
import base64
import os
import cv2


class Init:
    # 初始化状态
    Initialization = {
        'comm': False,
    }


class API:
    try:
        dll = ctypes.windll.LoadLibrary("bin/Sdtapi.dll")
    except Exception as e:
        ctypes.windll.user32.MessageBoxA(0, str(e).encode('gbk'), '提示'.encode('gbk'), 0)
        os._exit(0)

    # 4.1.1.端口初始化函数
    def init_comm(self):
        # 根据实际情况选择USB口和串口循环次数
        # USB型iDR, 1001 - 1016
        for i in range(1001, 1006):
            ret = self.dll.InitComm(i)
            if ret == 1:
                break
        # 串口型iDR,1--16
        if ret != 1:
            for i in range(1, 16):
                ret = self.dll.InitComm(i)
                if ret == 1:
                    break
        if ret == 1:
            return {'ret': 1, 'msg': '端口初始化成功', 'data': ''}
        else:
            return {'ret': 0, 'msg': '端口初始化失败', 'data': ''}

    # 4.1.2.端口关闭接口
    def close_comm(self):
        ret = self.dll.CloseComm()
        if ret == 1:
            return {'ret': 1, 'msg': '端口关闭成功', 'data': ''}
        elif ret == -1:
            return {'ret': 0, 'msg': '端口未打开', 'data': ''}
        else:
            return {'ret': 0, 'msg': '端口关闭失败', 'data': ''}

    # 4.2.1.卡认证接口
    def authenticate(self):
        ret = self.dll.Authenticate()
        if ret == 1:
            return {'ret': 1, 'msg': '卡认证成功', 'data': ''}
        else:
            return {'ret': 0, 'msg': '卡认证失败', 'data': ''}

    # 4.2.6.判断身份证是否在设备上
    def card_on(self):
        ret = self.dll.CardOn()
        if ret == 1:
            return {'ret': 1, 'msg': '有身份证', 'data': ''}
        else:
            return {'ret': 0, 'msg': '无身份证', 'data': ''}

    # 4.2.2.读卡信息接口
    # 原型4
    def read_base_infos(self):
        name, gender, folk, birthDay, code, address, agency, expireStart, expireEnd = bytes(192), bytes(192), bytes(
            192), bytes(
            192), bytes(192), bytes(192), bytes(192), bytes(192), bytes(192),
        ret = self.dll.ReadBaseInfos(name, gender, folk, birthDay, code, address, agency, expireStart, expireEnd)
        if ret == 1:
            info = {}
            info['name'] = name.decode('gbk').strip('\x00')
            info['gender'] = gender.decode('gbk').strip('\x00')
            info['folk'] = folk.decode('gbk').strip('\x00')
            info['birthDay'] = birthDay.decode('gbk').strip('\x00')
            info['code'] = code.decode('gbk').strip('\x00')
            info['address'] = address.decode('gbk').strip('\x00')
            info['agency'] = agency.decode('gbk').strip('\x00')
            info['expireStart'] = expireStart.decode('gbk').strip('\x00')
            info['expireEnd'] = expireEnd.decode('gbk').strip('\x00')

            try:
                with open("bin/photo.bmp", 'rb') as f:
                    base64_data = base64.b64encode(f.read())
                    s = base64_data.decode()
            except Exception as e:
                s = ''
            info['photo'] = "data:image/bmp;base64," + s
            return {'ret': 1, 'msg': '读卡成功', 'data': info}
        elif ret == 0:
            return {'ret': 0, 'msg': '读卡失败', 'data': ''}
        elif ret == -4:
            return {'ret': 0, 'msg': '缺少文件', 'data': ''}
        else:
            return {'ret': 0, 'msg': '未知错误', 'data': ''}

class OpenCV:
    cap = cv2.VideoCapture(0)
    # 从摄像头中取得视频
    def video_capture(self):
        if self.cap.isOpened():
            # 读取帧摄像头
            ret, frame = self.cap.read()
            img_str = cv2.imencode('.jpg', frame)[1].tostring()  # 将图片编码成流数据，放到内存缓存中，然后转化成string格式
            b64_code = base64.b64encode(img_str)  # 编码成base64
            return {'ret': 1, 'msg': '视频捕获成功', 'data': 'data:image/jpg;base64,' + b64_code.decode()}
        else:
            return {'ret': 0, 'msg': '未发现摄像头', 'data': ''}

    # 回收资源
    def destroy(self):
        self.cap.release()
