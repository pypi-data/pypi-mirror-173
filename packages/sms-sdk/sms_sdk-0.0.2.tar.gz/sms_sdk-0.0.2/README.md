# 智慧短信Python SDK说明文档

## 1 用途

通过SDK提供的函数可直接发起对智慧短信业务的调用，大幅减少为调用能力需提供的代码量。支持HTTP和TCP协议两种方式。

## 2 如何使用

    pip install sms-sdk

### 2.1 HTTP

    from smssdk.https import HttpTool
    
    # 创建http工具类实例。serverName是服务端域名，protocol是http协议（http/https）
    http_tool = HttpTool('your account', 'your password', 'serverName', 'protocol')

    # 姿势1：向一批号码发送内容相同的短信。accessNumber（虚拟接入码）选填
    http_tool._http_batch_sms(
        ['number1', 'numbern'], 
        'content',
        'accessNumber'
    )
    
    # 姿势2：点对点批量发送短信。bizId（业务侧id）和accessNumber（虚拟接入码）选填
    http_tool._http_p2p_sms(
        [
            {'phoneNumber': 'number1', 'messageContent': 'content1'},
            {'phoneNumber': 'number2', 'messageContent': 'content2', 'bizId': 'bizId2', 'accessNumber': 'accessNumber2'}
        ]
    )

### 2.2 TCP

#### 2.2.1 CMPP

    1.初始化SDK
    # 引入CmppTool
    from smssdk.tcp.cmpp import CmppTool
    # 初始化CmppTool
    tool = CmppTool(
        version=2,                          // CMPP协议版本，2或3，现仅支持2。必填。
        host={hostAddress},                 // 服务地址。必填。
        port={port},                        // 服务端口。必填。
        sp_id={spId},                       // 您的spId。必填。
        sp_secret={spSecret},               // 您的spSecret。必填。
        access_number={accessNumber},       // 您的虚拟接入码。必填。
        callback_imp={BasicCallbackImpl}    // 您的回调实现。非必填，若您需要接收事件回调，通过该参数实现，具体回调实现参考下方教程。
    )


    2.自定义回调实现（选做）
    # 引入回调基类
    from smssdk.tcp.cmpp import BasicCallback
    # 继承基类，重写函数。各函数入参res的数据结构和含义可见BasicCallback中的函数注释
    class SelfCallback(BasicCallback):
        # 连接回调
        def for_connect(self, res):
            pass
        # 发送短信结果回调
        def for_submit(self, res):
            pass
        # 发送短信状态报告回调
        def for_submit_report(self, res):
            pass
    # 创建实现的回调类的实例ins，并将其作为初始化SDK时的参数callback_imp的值
    ins = SelfCallback()


    3.TCP（socket）事件
    # 须知：一般来说，如下事件的使用顺序为：3.1 -> 3.2 -> 3.3   

    3.1连接TCP服务端并登录sms服务
    try:
        tool.connect_ismg()
    except Exception as e:
        # 自行处理
        pass
    
    3.2发送短信
    try:
        # 支持长短信发送，将自动拆分
        tool.submit_msg(message, phone_numbers)
    except Exception as e:
        # 自行处理
        pass

    3.3从sms服务注销
    try:
        tool.terminate_ismg()
    except Exception as e:
        # 自行处理
        pass

#### 2.2.2 SMGP

    待补充

#### 2.2.3 SGIP

    待补充

## 3 目录结构说明

├── smssdk &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// sdk实际代码</br>
│ ├── https &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// http方式相关代码<br>
│ ├── ├── auth                    </br>
│ └── └── └── auth.py &emsp;&emsp;&emsp;&emsp;&emsp;// http接口鉴权封装</br>
│ ├── ├── requests                </br>
│ ├── ├── ├── abstract_func.py &emsp;// http请求抽象封装</br>
│ └── └── └── api_request.py &emsp;&emsp;// 后台http接口请求封装</br>
│ └── └── init.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 包文件，定义了sdk(http)工具</br>
│ ├── tcp &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// tcp方式相关代码<br>
│ ├── ├── cmpp                    </br>
│ ├── ├── ├── callback            </br>
│ └── └── └── └── init.py &emsp;&emsp;&emsp;&emsp;// 包文件，定义了TCP-CMPP基础回调类</br>
│ ├── ├── ├── reqdata             </br>
│ ├── ├── ├── ├── init.py &emsp;&emsp;&emsp;&emsp;// 包文件，定义了CMPP事件基础参数封装</br>
│ ├── ├── ├── ├── connect_req.py &emsp;// CMPP_CONNECT事件参数封装</br>
│ ├── ├── ├── ├── submit_req.py &emsp;&emsp;// CMPP_SUBMIT事件参数封装</br>
│ └── └── └── └── terminate_req.py &emsp;// CMPP_TERMINATE事件参数封装</br>
│ ├── ├── ├── resdata             </br>
│ ├── ├── ├── ├── router          </br>
│ └── └── └── └── └── init.py &emsp;&emsp;// 包文件，定义了CMPP事件响应解析函数路由</br>
│ ├── ├── ├── ├── init.py &emsp;&emsp;&emsp;&emsp;// 包文件，定义TCP-CPMM事件响应基础参数解析</br>
│ ├── ├── ├── ├── active_req.py &emsp;// CMPP_ACTIVE_TEST事件参数解析</br>
│ ├── ├── ├── ├── connect_res.py &emsp;// CMPP_CONNECT_RESP事件参数解析</br>
│ ├── ├── ├── ├── deliver_req.py &emsp;// CMPP_DELIVER事件参数解析</br>
│ ├── ├── ├── ├── submit_res.py &emsp;// CMPP_SUBMIT_RESP事件参数解析</br>
│ └── └── └── └── terminate_res.py &emsp;// CMPP_TERMINATE_RESP事件参数解析</br>
│ ├── ├── ├── sockettool          </br>
│ └── └── └── └── init.py &emsp;&emsp;&emsp;&emsp;&emsp;// 包文件，定义了socket封装</br>
│ └── └── └── init.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 包文件，定义了TCP-CMPP-SDK工具CmppTool</br>
│ └── └── init.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 包文件，定义了TCP统一回调结构</br>
│ ├── utils                       </br>
│ ├── ├── exceptions.py &emsp;&emsp;&emsp;&emsp;// 自定义异常</br>
│ ├── ├── logger.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 日志类封装</br>
│ └── └── values.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 常量数据</br>
│ └── └── mythread.py &emsp;&emsp;&emsp;&emsp;&emsp;// 线程类</br>
│ └── └── init.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 包文件</br>
│ └── init.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 包文件</br>
├── .gitignore &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// git忽略文件</br>
├── LICENSE.txt &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 许可证</br>
├── main.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 程序入口</br>
├── README.md &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 工程说明</br>
├── requirements.txt &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 依赖列表</br>
├── setup.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// 打包信息和配置</br>
└── web_listen.py &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;// web应用配置，用于测试TCP业务</br>

## 4 版本记录

- v0.0.1

> HTTP SDK

- v0.0.2

> TCP-CMPP SDK