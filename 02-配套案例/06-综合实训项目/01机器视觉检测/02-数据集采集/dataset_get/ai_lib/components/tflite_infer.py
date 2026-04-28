import os
import tflite_runtime.interpreter as tflite

POSENET_MODEL = '../../resource/model_zoo/fruits_veges_model.tflite'

# 加载tflite模型 ，model_name: 模型名称，model_path: 模型路径
class TfliteRun:
    def __init__(self, model_name="fruit_detection", model_path=POSENET_MODEL):
        self.interpreter = tflite.Interpreter(model_path=model_path)   # 读取模型
        self.interpreter.allocate_tensors()                            # 分配张量
        self.model_name = model_name

        # 获取输入层和输出层维度
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        print(self.model_name + "_input_details", self.input_details)
        print(self.model_name + "_output_datalis", self.output_details)

        # 获取输入数据的形状
        print(self.model_name + "_input_shape", self.input_details[0]['shape'])

    def inference(self, img):
        input_data = img
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()     # 模型推理
        output_data1 = self.interpreter.get_tensor(self.output_details[0]['index'])    # 获取输出层数据
        return output_data1

if __name__ == "__main__":
    tflite_run = TfliteRun()
