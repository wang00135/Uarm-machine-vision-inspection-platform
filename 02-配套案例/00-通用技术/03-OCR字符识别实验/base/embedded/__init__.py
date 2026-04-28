from base.embedded.uart_init import UartConfig
from base.embedded.wifi_init import WifiConfig
from tools.config import Config

def clientMode(cline_mode=Config.CLINET_MODE):
    cline = None
    if cline_mode == "uart":
        cline = UartConfig()
    elif cline_mode == "wifi":
        cline = WifiConfig()
    return cline

