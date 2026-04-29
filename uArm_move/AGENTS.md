# Repository Guidelines

## 项目结构与模块组织

本仓库是 uArm 机械臂视觉分拣程序，入口为 `run.py`，会同时启动机械臂控制、图像识别和 PyQt5 界面。`ai_lib/` 存放视觉识别、检测器和推理组件；`embedded/` 存放机械臂运动控制、逆运动学和嵌入式 uArm 封装；`pyqt_ui/` 存放界面控制代码、Qt Designer 生成文件和图片资源；`tools/` 存放摄像头、配置、日志和标定工具；`resource/` 存放模型、标定参数、字体和 YAML 配置；`uarm/` 是 uArm 通信与 API 封装。新增代码应放在对应职责目录，避免把业务逻辑堆到 `run.py`。

## 构建、测试与本地运行命令

- `python run.py`：启动桌面界面、摄像头识别进程和机械臂控制进程。
- `bash run.sh`：Linux 桌面环境下的启动脚本，默认切换到固定目录并用 `sudo` 运行。
- `python setup.py`：使用 Cython 编译项目内 `.py` 模块到 `build/`，并清理生成的 `.c` 文件。
- `python -m compileall .`：在没有硬件环境时做基础语法检查。

运行前确认 PyQt5、OpenCV、Cython、ONNX/TFLite 推理依赖和 uArm 串口权限已就绪。

## 代码风格与命名约定

代码以 Python 3 为主，保持 4 空格缩进。模块、函数和变量使用 `snake_case`；类名使用 `PascalCase`，例如 `ArmServo`、`BoxDetectRec`。Qt 自动生成文件和资源文件放在 `pyqt_ui/bkrc_ui_lib/`，手写控制逻辑优先放在 `main_ui_ctl.py` 或独立模块。路径常量、识别模式和共享字典键应集中复用 `tools/config.py` 与 `ai_lib/components/config.py`，不要散落魔法字符串。

## 测试指南

当前仓库未包含正式测试目录。提交前至少运行 `python -m compileall .`；涉及视觉算法时，用 `resource/image_test/` 中的样例图做回归检查；涉及摄像头、串口或机械臂动作时，记录硬件型号、端口、标定文件和实际验证步骤。新增测试建议放入 `tests/`，文件命名为 `test_<module>.py`。

## 提交与 Pull Request 规范

现有历史提交较少，消息以简短中文描述为主，例如 `源代码`。后续提交建议使用祈使式短句，说明修改范围：`修复颜色识别阈值保存`、`调整机械臂初始坐标`。PR 需包含变更摘要、验证命令或硬件验证记录；修改 UI 时附截图；修改模型、标定参数或 YAML 时说明来源和兼容影响。

## 代理协作要求

所有对话与文档说明使用中文。执行命令或修改代码前，必须先输出计划，说明将执行的步骤；计划完成并得到确认后再开始操作。不要提交 `__pycache__/`、`build/`、本地 IDE 配置或临时标定输出。
