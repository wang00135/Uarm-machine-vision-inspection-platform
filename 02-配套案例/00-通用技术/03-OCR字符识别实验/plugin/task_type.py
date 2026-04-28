from enum import Enum

class TaskType(Enum):
    FLASK_TASK = 1
    IMAGE_GET_TASK = 2
    IMAGE_REC_TASK = 3
    EMBD_READ_SEND = 4

if __name__ == '__main__':
    try:
        print(TaskType(1))
    except ValueError:
        print('ValueError: {} is not a valid TaskType'.format(100))