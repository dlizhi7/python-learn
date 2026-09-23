from random import choice


class ModelCatalog:
    category = "model-catalog"

    def __init__(self, models: list[str]):
        self._models = list(models)

    def __len__(self) -> int:
        return len(self._models)

    def __getitem__(self, position: int | slice) -> str | list[str]:
        return self._models[position]

    def __repr__(self) -> str:
        return f"{type(self).__name__}(size={len(self._models)})"

def main() -> None:
    catalog = ModelCatalog(
        [
            "gpt-5.6-luna",
            "gpt-5.6-terra",
            "gpt-5.6-sol"
        ]
    )

    print("类属性：", ModelCatalog.category)
    print("对象表示：", catalog)
    print("模型数量：", len(catalog))
    print("第一个模型：", catalog[0])
    print("最后一个模型：", catalog[-1])
    print("切片结果：", catalog[1:])
    print("随机选择：", choice(catalog))
    print("遍历结果：")
    for model in catalog:
        print("-", model)

    catalog.category = "custom-model-catalog"
    print("实例属性：", catalog.__dict__)
    print("类属性：", ModelCatalog.__dict__)
    print("类属性：", ModelCatalog.category)

if __name__ == "__main__":
    main()