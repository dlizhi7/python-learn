"""练习：实现一个模型目录（ModelCatalog）。

目标：练习普通类、类属性/实例属性，以及 __len__、__repr__、__iter__、
__contains__、__getitem__ 等特殊方法。

要求：
1. 实现 Model，初始化参数为 name、provider、context_window；repr(model) 应提供清晰的调试信息。
2. 实现 ModelCatalog，并定义类属性 category = "model-catalog"。
3. ModelCatalog 接收 list[Model]；复制传入列表，且模型名称不得重复，重复时抛出 ValueError。
4. 支持 len(catalog)、for model in catalog、"model-name" in catalog；后者按模型名判断。
5. catalog[index] 返回 Model；catalog[start:stop] 返回新的 ModelCatalog。
6. 实现 filter_by_provider(provider)，返回仅包含该供应商模型的新 ModelCatalog。
7. 用 assert 验证长度、包含、索引、切片、筛选、外部列表修改不影响目录，以及重复名称会抛出 ValueError。
"""

from __future__ import annotations

from collections.abc import Iterator

class Model:
    def __init__(self, name: str, provider: str, context_window: int) -> None:
        self._name = name
        self._provider = provider
        self._context_window = context_window

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"name={self._name}, "
            f"provider={self._provider}, "
            f"context_window={self._context_window}"
            f")"
        )

class ModelCatalog:
    category = "model-catalog"

    def __init__(self, models: list[Model]) -> None:
        models_set = set(model._name for model in models)
        if len(models_set) != len(models):
            raise ValueError("模型名称必须唯一。")
        self._models = list(models)

    def __len__(self) -> int:
        return len(self._models)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(size={len(self._models)})"

    def __iter__(self) -> Iterator[Model]:
        return iter(self._models)

    def __contains__(self, name: object) -> bool:
        if not isinstance(name, str):
            return False
        return any(model._name == name for model in self._models)

    def __getitem__(self, position: int | slice) -> Model | ModelCatalog:
        if isinstance(position, int):
            return self._models[position]
        elif isinstance(position, slice):
            return ModelCatalog(self._models[position])
        else:
            raise TypeError("索引必须是整数或切片。")

    def filter_by_provider(self, provider: str) -> ModelCatalog:
        filtered_models = [model for model in self._models if model._provider == provider]
        return ModelCatalog(filtered_models)

def main() -> None:
    models = [
        Model("gpt-5.6-luna", "OpenAI", 4096),
        Model("gpt-5.6-terra", "OpenAI", 8192),
        Model("gpt-5.6-sol", "OpenAI", 16384),
        Model("deepseek-flash", "DeepSeek", 8192)
    ]

    catalog = ModelCatalog(models)

    assert len(catalog) == 4
    assert "gpt-5.6-sol" in catalog
    assert "not-exist" not in catalog
    assert catalog[0]._name == "gpt-5.6-luna"
    assert isinstance(catalog[1:3], ModelCatalog)
    assert len(catalog[1:3]) == 2
    assert len(catalog.filter_by_provider("OpenAI")) == 3

    models.append(Model("gpt-6-astra", "OpenAI", 32768))

    assert len(catalog) == 4

    try:
        ModelCatalog([
            Model("gpt-5.5", "OpenAI", 2048),
            Model("gpt-5.5", "OpenAI", 2048)
        ])
    except ValueError as e:
        print("捕获到 ValueError:", e)
    else:
        raise AssertionError("同名模型应当抛出 ValueError。")

    print(catalog[0])

if __name__ == "__main__":
    main()
