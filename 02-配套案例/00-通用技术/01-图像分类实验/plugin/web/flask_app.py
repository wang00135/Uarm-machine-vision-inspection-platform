import cv2
from flask import Flask, render_template, Response
import logging
from tools.log import log
import numpy as np
from base.components.config import ai_cfg
from tools.config import config
from tools.databus.bus import workFlow
from plugin.web.rest_api.posen_value import fruits_status_bp,setStatus

# logging.getLogger("werkzeug").setLevel(logging.WARNING)
app = Flask(__name__)
app.register_blueprint(fruits_status_bp)

class FlaskTask():
    def __init__(self):
        global app

    def onExit(self):
        pass

    def worker(self, host="127.0.0.1", port=8081, q_flask=None, full_dict=None):
        """
        flask可视化交互界面启动插件
        :param host: 本机的IP地址（同一个局域网均可访问）
        :param port: 端口号（可随意设置）
        :param q_flask: 摄像头图像帧
        :return:
        """
        setStatus(full_dict)

        @app.route('/', methods=['GET', 'POST'])
        def base_layout():
            return render_template('bigdata.html')

        def camera():
            while True:
                if q_flask.empty():
                    continue
                else:
                    img = q_flask.get()
                    if img != False:
                        img = np.array(img).reshape(ai_cfg.CAM_HEIGHT, ai_cfg.CAM_WIDTH, 3)
                ret, buf = cv2.imencode(".jpeg", img)
                yield (
                        b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n\r\n"
                )

        @app.route("/videostreamIpc/", methods=["GET"])
        def videostreamIpc():
            return Response(
                camera(), mimetype="multipart/x-mixed-replace; boundary=frame"
            )

        app.run(host=host, port=port, threaded=True)
        log.info("flask已成功启动！！")

def flaskPluginRegist(host="127.0.0.1", port=8080, q_flask=None, full_dict=None):

    flask_task_plugin = FlaskTask()

    workFlow.registBus(flask_task_plugin.__class__.__name__,
                       flask_task_plugin.worker,
                       (host, port, q_flask, full_dict),
                       flask_task_plugin.onExit)

if __name__ == "__main__":
    flask_task = FlaskTask()
    flask_task.worker()

# 在谷歌浏览器中打开此链接
# p2 = sp.Popen("chromium-browser --kiosk --app='http://127.0.0.1:8080'", shell=True)
