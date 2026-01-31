# pyclog-helper

pyclog 的第三方辅助工具库,提供增强的日志记录能力和便捷的辅助功能。

## 关于 pyclog-helper

pyclog-helper 是 pyclog 日志库的第三方辅助工具包,提供了丰富的日志管理功能,包括文件轮转、自定义格式化、线程安全等特性。

## 特性

- 简单易用的日志文件创建方法
- 支持自定义命名约定
- 自动创建不存在的目录
- 基于大小和日期的日志文件轮转
- 五个日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
- 自定义日志格式(时间戳、日志级别、模块名等)
- 线程安全的并发日志写入
- 完善的错误处理
- 完整的类型提示
- 兼容 Python 3.6+
- 仅使用 Python 标准库,无外部依赖

## 安装

### 源代码安装

```bash
git clone https://github.com/heibaiya-dev/pyclog-helper.git
cd pyclog-helper
pip install -e .
```

### 从 GitHub 直接安装

```bash
pip install git+https://github.com/heibaiya-dev/pyclog-helper.git
```

## 快速开始

### 基本使用

```python
from pyclog import Create_Logger

logger = Create_Logger("app.log")

logger.Debug("这是一条调试信息")
logger.Info("这是一条普通信息")
logger.Warning("这是一条警告信息")
logger.Error("这是一条错误信息")
logger.Critical("这是一条严重错误信息")
```

### 自定义配置

```python
from pyclog import Pyclog, LogConfig, SimpleFormatter

config = LogConfig(
    log_file_path="logs/app.log",
    max_file_size=10 * 1024 * 1024,  # 10MB
    backup_count=5,
    enable_date_rotation=True
)

formatter = SimpleFormatter()
formatter.Set_Format("[%(asctime)s] %(levelname)s: %(message)s")

logger = Pyclog(config, formatter)
logger.Info("使用自定义配置的日志消息")
```

### 文件轮转

```python
from pyclog import Create_Logger

# 基于大小的轮转
logger = Create_Logger(
    "logs/rotation.log",
    max_file_size=5 * 1024 * 1024,  # 5MB
    backup_count=3
)

# 基于日期的轮转
logger = Create_Logger(
    "logs/date_rotation.log",
    enable_date_rotation=True
)
```

### 控制台输出

```python
from pyclog import Create_Logger

logger = Create_Logger("app.log")
logger.Add_Console_Output()

logger.Info("这条消息会同时输出到控制台和文件")
```

### 日志级别过滤

```python
from pyclog import Create_Logger, LogLevel

logger = Create_Logger("app.log")
logger.Set_Log_Level(LogLevel.WARNING)

logger.Debug("这条消息不会显示")
logger.Info("这条消息不会显示")
logger.Warning("这条消息会显示")
logger.Error("这条消息会显示")
```

### 额外字段

```python
from pyclog import Create_Logger

logger = Create_Logger("app.log")

logger.Info("用户登录", user_id=12345, username="test_user")
logger.Error("数据库连接失败", error_code="DB001", retry_count=3)
```

### 上下文管理器

```python
from pyclog import Create_Logger

with Create_Logger("app.log") as logger:
    logger.Info("在上下文管理器中记录日志")
    # 退出时会自动关闭日志文件
```

## API 文档

### Pyclog 类

主要的日志记录类。

#### 方法

- `Debug(message: str, **kwargs) -> bool` - 记录调试级别日志
- `Info(message: str, **kwargs) -> bool` - 记录信息级别日志
- `Warning(message: str, **kwargs) -> bool` - 记录警告级别日志
- `Error(message: str, **kwargs) -> bool` - 记录错误级别日志
- `Critical(message: str, **kwargs) -> bool` - 记录严重错误级别日志
- `Create_Log_File(file_path: str, max_size: int = None, backup_count: int = None) -> bool` - 创建新的日志文件
- `Add_Handler(handler) -> None` - 添加日志处理器
- `Remove_Handler(handler) -> bool` - 移除日志处理器
- `Add_Console_Output() -> None` - 添加控制台输出
- `Set_Formatter(formatter: LogFormatter) -> None` - 设置日志格式化器
- `Set_Log_Level(level: LogLevel) -> None` - 设置最低日志级别
- `Flush() -> None` - 刷新所有处理器
- `Close() -> None` - 关闭所有处理器

### LogConfig 类

日志配置类。

#### 参数

- `log_file_path: str` - 日志文件路径
- `max_file_size: int = 10 * 1024 * 1024` - 最大文件大小(字节)
- `backup_count: int = 5` - 备份文件数量
- `enable_date_rotation: bool = False` - 是否启用日期轮转
- `date_format: str = "%Y-%m-%d"` - 日期格式
- `time_format: str = "%Y-%m-%d %H:%M:%S"` - 时间格式
- `log_format: str = "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s"` - 日志格式
- `auto_create_directory: bool = True` - 是否自动创建目录
- `encoding: str = "utf-8"` - 文件编码
- `min_log_level: LogLevel = LogLevel.DEBUG` - 最低日志级别

### LogFormatter 类

日志格式化器类。

#### 方法

- `Format_Message(message: LogMessage) -> str` - 格式化日志消息
- `Format_Timestamp(timestamp: datetime = None) -> str` - 格式化时间戳
- `Set_Format(format_string: str) -> None` - 设置格式字符串
- `Set_Time_Format(time_format: str) -> None` - 设置时间格式

### 预定义格式化器

- `SimpleFormatter` - 简单格式化器
- `DetailedFormatter` - 详细格式化器(包含线程ID)
- `JSONFormatter` - JSON格式化器

### LogLevel 枚举

日志级别枚举。

- `LogLevel.DEBUG = 10`
- `LogLevel.INFO = 20`
- `LogLevel.WARNING = 30`
- `LogLevel.ERROR = 40`
- `LogLevel.CRITICAL = 50`

### 便捷函数

- `Create_Logger(log_file_path: str = "app.log", **kwargs) -> Pyclog` - 创建日志器
- `Get_Logger(name: str = "default") -> Pyclog` - 获取命名日志器

## 示例

更多示例请参见 [examples/basic_usage.py](examples/basic_usage.py)

## 许可证

MIT License

## 贡献

欢迎提交问题和拉取请求!

## TIPS
所有东西都是由GLM 4.7完成的,不保证稳定性,以上的readme也是ai写的,在我自己接手这个库前，最好不要把它用在正式的项目上(真的会有人用吗awa)
如果不会用可以发邮件给我:bilibilisome@outlook.com