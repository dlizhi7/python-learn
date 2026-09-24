"""第二个示例：理解实例方法、类方法与静态方法。

运行：
    ./.venv/bin/python examples/01_objects_and_classes/method_binding.py
"""

from __future__ import annotations

from typing import ClassVar


class ModelInfo:
    """用于演示不同种类的方法如何绑定。"""

    created_count: ClassVar[int] = 0

    def __init__(self, name: str, provider: str, context_window: int) -> None:
        self.name = name
        self.provider = provider
        self.context_window = context_window
        type(self).created_count += 1

    def description(self) -> str:
        """实例方法：self 会自动绑定为调用该方法的实例。"""
        return f"{self.provider}/{self.name} ({self.context_window} tokens)"

    @classmethod
    def from_record(cls, record: str) -> ModelInfo:
        """类方法：cls 是调用该方法的类，适合用作替代构造器。"""
        name, provider, context_window = record.split(",")
        return cls(name, provider, int(context_window))

    @classmethod
    def total_created(cls) -> int:
        return cls.created_count

    @staticmethod
    def is_valid_context_window(value: int) -> bool:
        """静态方法：不需要实例状态或类状态的相关辅助逻辑。"""
        return value > 0


def main() -> None:
    primary = ModelInfo("gpt-5.6-sol", "OpenAI", 16_384)
    secondary = ModelInfo.from_record("deepseek-flash,DeepSeek,8192")

    # 实例方法调用等价于从类中取函数后，手动传入实例。
    print(primary.description())
    print(ModelInfo.description(primary))
    print(primary.description.__self__ is primary)

    # 类方法使用 cls 创建对象，因此没有把类名硬编码在方法体中。
    print(secondary.description())
    print(ModelInfo.total_created())

    # 静态方法不会自动接收 self 或 cls。
    print(ModelInfo.is_valid_context_window(8_192))
    print(primary.is_valid_context_window(-1))


if __name__ == "__main__":
    main()
