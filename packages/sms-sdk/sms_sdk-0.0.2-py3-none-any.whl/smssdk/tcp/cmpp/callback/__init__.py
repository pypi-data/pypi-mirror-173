"""
ISMG响应/ISMG主动事件回调
"""
from smssdk.utils.logger import Logger

logger = Logger('tcp.cmpp.callback.__init__.py')


class BasicCallback:
    def for_connect(self, res: dict):
        """
        连接ISMG回调
        :param res: 响应数据，结构如下：
        {
            'code': 0为成功，1为异常：int
            'message': code相应的说明：string
            'data': 成功时内容为None，异常时该key包含具体原因，内容同CMPP协议规范中返回内容：dict
        }
        """
        logger.info(f'[BasicCallback:for_connect()][CMPP_CONNECT回调]{res}。')

    def for_submit(self, res: dict):
        """
        SP向ISMG发送消息（发短信）回调
        :param res: 响应数据，结构如下：
        {
            'code': 0为成功，1为异常：int
            'message': code相应的说明：string
            'data': {
                'msg_id': 响应msg_id。长短信拆分时，为代表该组拆分短信的响应中的主msg_id：string
                'failed_res': 失败时，提供原始响应数据：list[dict]
            }
        }
        """
        logger.info(f'[BasicCallback:for_submit()][CMPP_SUBMIT回调]{res}。')

    def for_submit_report(self, res: dict):
        """
        收到ISMG发送的状态报告的回调
        :param res: 响应数据，结构如下：
        {
            'code': 0为成功，1为异常：int
            'message': code相应的说明：string
            'data': {
                'msg_id': 报告msg_id。长短信拆分时，为代表该组拆分短信的状态报告中的主msg_id：string
                'all_report': 状态报告原始详细信息。长短信拆分时，包含多条，若失败，失败的状态报告也在其中：list[dict]
            }
        }
        """
        logger.info(f'[BasicCallback:for_submit_report()][CMPP_DELIVER(REPORT)回调]{res}。')
