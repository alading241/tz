import time
from app.uTask import taskList
import celery


# 启动celery
# celery -A app.uTask.taskList worker -l info -P eventlet

# 启动celery后台管理工具 flower 命令
# celery flower --address=0.0.0.0 --port=555 --broker=redis://127.0.0.1:6379/1

# TODO 初始化更新沪深股票
def stock_base_task():
    """沪深股市-初始化股票信息"""
    tasks_id = taskList.stock_base_stock_update.delay()
    return tasks_id

# TODO 更新各股每日指标 每日更新
def stock_daily_data_task():
    """各股每日指标"""
    t_result = taskList.stock_base_stock_daily_data.delay()
    return t_result

# TODO 更新各股财务数据 每日更新
def stock_fi_data_task():
    """各股基本财务数据"""
    tasks_id = taskList.stock_base_stock_fi_data.delay()
    return tasks_id

def stock_init_group():
    c_result = celery.chain(taskList.stock_base_stock_update.s(), taskList.stock_base_stock_daily_data.s(),
                            taskList.stock_base_stock_fi_data.s()).apply_async(priority=0)
    return c_result

# TODO  整理用户使用股票数据格式 每日更新
def stock_user_data_task():
    """用户使用股票数据"""
    ts_result = taskList.stock_base_stock_user_data.apply_async(priority=3)
    return ts_result

if __name__ == '__main__':
    # result = stock_init_group()
    # result = stock_user_data_task()
    result = taskList.init_base_stock_data
    print(result)

