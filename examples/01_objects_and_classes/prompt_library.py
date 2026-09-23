"""第一个示例：让自定义对象支持 Python 的内置语法。

运行：
    python examples/01_objects_and_classes/prompt_library.py

本示例借鉴《流畅的 Python》第 2 版开篇的思路：
不继承 list，也能让自定义对象支持 len()、索引、切片、随机选择和遍历。
"""

from random import choice


class PromptLibrary:
    """保存提示词的轻量集合。"""

    category = "prompt-library"  # 类属性：所有实例共享

    def __init__(self, prompts: list[str]) -> None:
        # 复制传入的列表，避免外部后续修改 prompts 影响当前对象。
        self._prompts = list(prompts)

    def __len__(self) -> int:
        """支持 len(library)。"""
        return len(self._prompts)

    def __getitem__(self, position: int | slice) -> str | list[str]:
        """支持 library[index] 和 library[start:stop]。"""
        return self._prompts[position]

    def __repr__(self) -> str:
        """提供适合调试的对象表示。"""
        return f"{type(self).__name__}(size={len(self)})"


def main() -> None:
    library = PromptLibrary(
        [
            "总结下面的文本：{text}",
            "从文本中提取实体：{text}",
            "将文本翻译为中文：{text}",
        ]
    )

    print("对象表示：", library)
    print("提示词数量：", len(library))
    print("第一个提示词：", library[0])
    print("最后一个提示词：", library[-1])
    print("切片结果：", library[1:])
    print("随机选择：", choice(library))

    print("遍历结果：")
    for prompt in library:
        print("-", prompt)

    print("实例属性：", library.__dict__)
    print("类属性：", PromptLibrary.category)


if __name__ == "__main__":
    main()
