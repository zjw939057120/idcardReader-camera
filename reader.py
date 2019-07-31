from websocket_server import WebsocketServer
import sdk
import json


# 处理客户端消息
def handle_message(message):
    if message == '--OpenReader':
        # 打开设备
        ret = sdk.API().init_comm()
        if ret == 1:
            sdk.Init.Initialization['comm'] = True
    elif message == '--ReadCard':
        # 读取身份证信息
        if not sdk.Init.Initialization['comm']:
            ret = sdk.API().init_comm()
            if ret['ret'] == 1:
                sdk.Init.Initialization['comm'] = True
            else:
                return ret
        # 卡认证
        sdk.API().authenticate()
        # 判断卡
        ret = sdk.API().card_on()
        if ret['ret'] != 1:
            return ret
        # 读取卡
        ret = sdk.API().read_base_infos()
        if ret['ret'] != 1:
            return ret
    elif message == '--CloseReader':
        # 关闭设备
        ret = sdk.API().close_comm()
        if ret == 1:
            sdk.Init.Initialization['comm'] = False
    else:
        ret = {'ret': 0, 'msg': '未知指令', 'data': ''}
    return ret



# 客户端上线
def new_client(client, server):
    pass
    ret = sdk.API().init_comm()
    if ret['ret'] == 1:
        sdk.Init.Initialization['comm'] = True
    print(ret)
    server.send_message(client, json.dumps(ret))



# 客户端离线
def client_left(client, server):
    pass
    ret = sdk.API().close_comm()
    if ret['ret'] == 1:
        sdk.Init.Initialization['comm'] = False
    print(ret)


# 接收客户端消息
def message_received(client, server, message):
    pass
    if len(message) > 200:
        message = message[:200] + '..'
    received = handle_message(message)
    server.send_message(client, json.dumps(received))


PORT = 9000
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
