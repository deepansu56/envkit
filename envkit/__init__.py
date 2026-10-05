"""envkit —— 一个用于演示 Fissue 的小型配置/缓存/校验工具库。

已发布的稳定功能：
    Registry          按需构建的组件注册表
    TTLCache          带过期时间的缓存
    load_settings     按「环境变量 > 默认值」装载配置
    get_bool          从环境变量读布尔
    parse_offset      解析时区偏移（分钟）
    split_iso         拆解 ISO-8601 时间戳
    parse_size        解析容量字符串
    format_size       容量格式化
    sanitize_filename 清洗文件名
    parse_email       解析并校验邮箱
    parse_port        解析并校验端口号
    aggregate         按类别聚合事件
"""

from .cache import TTLCache
from .config import get_bool, load_settings
from .registry import Registry
from .report import aggregate
from .timeutil import parse_offset, split_iso
from .units import format_size, parse_size
from .validate import parse_email, parse_port, sanitize_filename

__version__ = "0.6.0"

__all__ = [
    "Registry",
    "TTLCache",
    "load_settings",
    "get_bool",
    "parse_offset",
    "split_iso",
    "parse_size",
    "format_size",
    "sanitize_filename",
    "parse_email",
    "parse_port",
    "aggregate",
    "__version__",
]
