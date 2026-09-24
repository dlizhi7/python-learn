"""练习：实现模型服务端点（ModelEndpoint）。

目标：练习实例方法、类方法、静态方法，以及类属性与实例属性的边界。

要求：
1. 实现 ModelEndpoint，初始化参数为 provider、name、host、port。
2. 定义类属性：
    - default_timeout = 30
    - created_count = 0
3. 每次成功创建实例时，created_count 加一。
4. 实现实例方法 url()，返回 "https://{host}:{port}/v1/models/{name}"。
5. 实现实例方法 request_summary()，返回包含 provider、name、url 和 timeout 的可读文本；timeout 使用实例属性（若存在），否则使用类属性 default_timeout。
6. 实现类方法 from_connection_string(cls, value)，解析 "provider|name|host|port" 并创建对象。
    - 格式错误时抛出 ValueError。
    - 必须使用 cls(...) 创建对象，不能把类名硬编码在方法体中。
7. 实现类方法 total_created(cls)，返回 cls.created_count。
8. 实现静态方法 is_valid_port(value)，仅在 value 是 int 且范围为 1 到 65535 时返回 True。
9. 初始化时必须使用 is_valid_port 验证 port；无效时抛出 ValueError。

在 main() 中至少用 assert 验证：
- 直接创建对象后，url() 的结果正确。
- from_connection_string 创建的对象字段正确。
- 创建两个合法对象后，ModelEndpoint.total_created() == 2。
- endpoint.timeout = 5 后，request_summary() 使用 5；未设置 timeout 的对象使用 30。
- 不合法端口、格式错误的连接字符串都会抛出 ValueError。

补充思考：静态方法 is_valid_port 为什么不需要 self 或 cls？
"""

from __future__ import annotations

from typing import ClassVar


# 在此处完成你的实现。
class ModelEndpoint:
    default_timeout: ClassVar[int] = 30
    created_count: ClassVar[int] = 0

    def __init__(self, provider: str, name: str, host: str, port: str) -> None:
        self.provider = provider
        self.name = name
        self.host = host
        self.port = port
        if not self.is_valid_port(int(port)):
            raise ValueError("端口无效")
        type(self).created_count += 1

    def url(self) -> str:
        return f"https://{self.host}:{self.port}/v1/models/{self.name}"

    def request_summary(self) -> str:
        return (
            f"provider: {self.provider}, "
            f"name: {self.name}, "
            f"url: {self.url()}, "
            f"timeout: {self.timeout if hasattr(self, 'timeout') else type(self).default_timeout}"
        )

    @classmethod
    def from_connection_string(cls, value: str) -> ModelEndpoint:
        parts = value.split("|")
        if len(parts) != 4:
            raise ValueError("格式错误，应为: provider|name|host|port")
        provider, name, host, port = parts
        return cls(provider, name, host, port)

    @classmethod
    def total_created(cls) -> int:
        return cls.created_count

    @staticmethod
    def is_valid_port(value: int) -> bool:
        return isinstance(value, int) and 1 <= value and value <= 65535

def main() -> None:
    endpoint = ModelEndpoint("DeepSeek", "deepseek-flash", "api.deepseek.com", "8080")
    assert endpoint.url() == "https://api.deepseek.com:8080/v1/models/deepseek-flash"
    endpoint2 = ModelEndpoint.from_connection_string("OpenAI|gpt-5.6-terra|api.openai.com|443")
    assert endpoint2.provider == "OpenAI"
    assert endpoint2.name == "gpt-5.6-terra"
    assert endpoint2.host == "api.openai.com"
    assert endpoint2.port == "443"
    assert ModelEndpoint.total_created() == 2
    endpoint.timeout = 5
    assert endpoint.request_summary() == (
        "provider: DeepSeek, "
        "name: deepseek-flash, "
        "url: https://api.deepseek.com:8080/v1/models/deepseek-flash, "
        "timeout: 5"
    )
    assert endpoint2.request_summary() == (
        "provider: OpenAI, "
        "name: gpt-5.6-terra, "
        "url: https://api.openai.com:443/v1/models/gpt-5.6-terra, "
        "timeout: 30"
    )
    try:
        ModelEndpoint("Invalid", "invalid-model", "localhost", "70000000")
    except ValueError:
        print("捕获到 ValueError: 端口无效")
