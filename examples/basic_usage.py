import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyclog import Pyclog, Create_Logger, LogLevel, LogConfig, SimpleFormatter, DetailedFormatter


def Example_Basic_Usage():
    print("=== 基本使用示例 ===")
    
    logger = Create_Logger("logs/basic.log")
    
    logger.Debug("这是一条调试信息")
    logger.Info("这是一条普通信息")
    logger.Warning("这是一条警告信息")
    logger.Error("这是一条错误信息")
    logger.Critical("这是一条严重错误信息")
    
    print("日志已写入 logs/basic.log")


def Example_Custom_Format():
    print("\n=== 自定义格式示例 ===")
    
    custom_format = "[%(asctime)s] | %(levelname)-8s | %(message)s"
    custom_time_format = "%Y-%m-%d %H:%M:%S"
    
    config = LogConfig(
        log_file_path="logs/custom_format.log",
        log_format=custom_format,
        time_format=custom_time_format
    )
    
    formatter = SimpleFormatter()
    formatter.Set_Format(custom_format)
    formatter.Set_Time_Format(custom_time_format)
    
    logger = Pyclog(config, formatter)
    
    logger.Info("使用自定义格式的日志消息")
    logger.Warning("警告: 自定义格式看起来不错!")
    
    print("日志已写入 logs/custom_format.log")


def Example_Detailed_Format():
    print("\n=== 详细格式示例 ===")
    
    config = LogConfig(log_file_path="logs/detailed.log")
    formatter = DetailedFormatter()
    
    logger = Pyclog(config, formatter)
    
    logger.Info("这是一条详细格式的日志")
    logger.Debug("调试信息包含线程ID和时间戳")
    
    print("日志已写入 logs/detailed.log")


def Example_File_Rotation():
    print("\n=== 文件轮转示例 ===")
    
    config = LogConfig(
        log_file_path="logs/rotation.log",
        max_file_size=1024,
        backup_count=3
    )
    
    logger = Pyclog(config)
    
    for i in range(100):
        logger.Info(f"这是第 {i+1} 条日志消息,用于测试文件轮转功能")
    
    print("日志已写入 logs/rotation.log, 文件轮转已触发")


def Example_Date_Rotation():
    print("\n=== 日期轮转示例 ===")
    
    config = LogConfig(
        log_file_path="logs/date_rotation.log",
        enable_date_rotation=True,
        date_format="%Y-%m-%d"
    )
    
    logger = Pyclog(config)
    
    logger.Info("这条日志将根据日期自动轮转")
    logger.Warning("每天会创建一个新的日志文件")
    
    print("日志已写入 logs/date_rotation_YYYY-MM-DD.log")


def Example_Console_Output():
    print("\n=== 控制台输出示例 ===")
    
    logger = Create_Logger("logs/console.log")
    logger.Add_Console_Output()
    
    print("以下消息将同时输出到控制台和文件:")
    logger.Info("这条消息会显示在控制台和日志文件中")
    logger.Warning("警告消息也会显示在两处")
    logger.Error("错误消息同样会显示")
    
    print("日志已写入 logs/console.log")


def Example_Log_Level_Filtering():
    print("\n=== 日志级别过滤示例 ===")
    
    logger = Create_Logger("logs/level_filter.log")
    
    print("设置最低日志级别为 WARNING:")
    logger.Set_Log_Level(LogLevel.WARNING)
    
    logger.Debug("这条调试消息不会显示")
    logger.Info("这条信息消息不会显示")
    logger.Warning("这条警告消息会显示")
    logger.Error("这条错误消息会显示")
    
    print("日志已写入 logs/level_filter.log")


def Example_Extra_Fields():
    print("\n=== 额外字段示例 ===")
    
    logger = Create_Logger("logs/extra_fields.log")
    
    logger.Info("用户登录", user_id=12345, username="test_user", ip="192.168.1.1")
    logger.Error("数据库连接失败", error_code="DB001", retry_count=3)
    logger.Warning("内存使用率高", memory_usage=85.5, threshold=80.0)
    
    print("日志已写入 logs/extra_fields.log")


def Example_Context_Manager():
    print("\n=== 上下文管理器示例 ===")
    
    with Create_Logger("logs/context.log") as logger:
        logger.Info("在上下文管理器中记录日志")
        logger.Warning("退出上下文时会自动关闭日志文件")
    
    print("日志已写入 logs/context.log")


def Example_Multiple_Loggers():
    print("\n=== 多个日志器示例 ===")
    
    app_logger = Create_Logger("logs/app.log")
    db_logger = Create_Logger("logs/database.log")
    api_logger = Create_Logger("logs/api.log")
    
    app_logger.Info("应用程序启动")
    db_logger.Info("数据库连接建立")
    api_logger.Info("API服务启动")
    
    app_logger.Error("应用程序遇到错误")
    db_logger.Warning("数据库查询缓慢")
    api_logger.Info("API请求处理完成")
    
    print("日志已分别写入 logs/app.log, logs/database.log, logs/api.log")


def Example_Thread_Safety():
    print("\n=== 线程安全示例 ===")
    
    import threading
    import time
    
    logger = Create_Logger("logs/thread_safe.log")
    
    def Log_Thread(thread_id: int):
        for i in range(10):
            logger.Info(f"线程 {thread_id} - 消息 {i+1}")
            time.sleep(0.01)
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=Log_Thread, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("日志已写入 logs/thread_safe.log (多线程并发写入)")


def Example_Create_Log_File():
    print("\n=== 创建新日志文件示例 ===")
    
    logger = Create_Logger("logs/main.log")
    
    logger.Info("主日志文件的消息")
    
    logger.Create_Log_File("logs/error.log", max_size=5*1024, backup_count=2)
    logger.Error("这条错误消息会写入 error.log")
    
    logger.Create_Log_File("logs/access.log")
    logger.Info("访问日志消息", endpoint="/api/users", method="GET")
    
    print("日志已分别写入 logs/main.log, logs/error.log, logs/access.log")


if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    
    Example_Basic_Usage()
    Example_Custom_Format()
    Example_Detailed_Format()
    Example_File_Rotation()
    Example_Date_Rotation()
    Example_Console_Output()
    Example_Log_Level_Filtering()
    Example_Extra_Fields()
    Example_Context_Manager()
    Example_Multiple_Loggers()
    Example_Thread_Safety()
    Example_Create_Log_File()
    
    print("\n=== 所有示例运行完成 ===")
    print("请查看 logs/ 目录中的日志文件")
