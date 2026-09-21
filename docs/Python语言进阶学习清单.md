# Python 语言进阶学习清单

适用对象：有一年左右后端开发经验、使用 FastAPI 和 AI Agent 相关技术，希望补齐 Python 语言本身的原理与实践能力。

这不是按周安排的计划。按下列顺序学习即可：状态好时深入阅读源码和完成练习；忙碌或状态一般时，只看概念、运行示例或复盘笔记也可以。每一项至少达到：**能解释、能手写小例子、能说出在 FastAPI 或 Agent 开发中的用法**。

## 1. 对象与类基础

- 实例属性和类属性，以及二者的查找顺序
- 实例方法、类方法、静态方法；理解“绑定方法”
- 继承、方法覆盖、多重继承、MRO 与 `super()`
- `__dict__`、`vars()`、`dir()` 的用途
- `__slots__` 的作用、限制和适用场景
- `dataclass`：默认值、`default_factory`、冻结对象、比较行为

实践：实现一个 Agent 工具的配置类，比较普通类与 `@dataclass` 的可读性、校验与调试体验。

## 2. Python 数据模型与特殊方法

不要把特殊方法当成需要死记的名单。重点是理解：Python 的语法和内置函数会通过一组协议调用对象的特殊方法。

### 2.1 对象展示

- `__repr__`：面向开发者、可调试的表示
- `__str__`：面向用户的文本表示
- `__format__`：支持 `format()` 与 f-string 的格式化

### 2.2 比较与哈希

- `__eq__`、`__lt__` 等富比较方法
- `__hash__` 与字典键、集合元素的关系
- 可变对象作为字典键的风险
- `NotImplemented` 的含义

### 2.3 容器与序列协议

- `__len__`、`__bool__`
- `__getitem__`、切片对象 `slice`
- `__contains__`
- `__iter__`、`__next__`

### 2.4 行为协议

- `__call__`：让实例像函数一样调用
- `__enter__`、`__exit__`：上下文管理器
- `__new__`、`__init__`：创建与初始化的边界
- `__getattr__`、`__getattribute__`、`__setattr__`：属性访问控制；注意无限递归风险

关键细节：`len(obj)`、`obj[index]` 这类隐式特殊方法调用通常从**类**上查找，不要依赖为单个实例临时赋值 `obj.__len__`。

实践：实现 `ToolRegistry`：支持 `@registry.register(name="search")` 注册函数、`registry["search"]` 取工具、`len(registry)` 取数量、`for tool in registry` 按顺序遍历，并实现清晰的 `repr(registry)`。

## 3. 函数、作用域与闭包

- 函数是一等对象：赋值、传参、返回、存入容器
- LEGB 名称查找规则：Local、Enclosing、Global、Built-in
- 自由变量与闭包
- `nonlocal` 和 `global` 的区别
- 循环变量的延迟绑定陷阱
- 默认参数在定义时求值，以及可变默认参数陷阱

实践：写一个 `make_rate_limiter(limit)` 闭包；再故意写出循环闭包 bug，并解释和修正它。

## 4. 装饰器

- 装饰器本质：接收可调用对象并返回可调用对象
- 无参数装饰器和带参数装饰器
- 装饰器的叠加顺序
- `functools.wraps`：保留被装饰函数的名称、文档、签名等元信息
- 类装饰器与函数装饰器的取舍
- 同步函数和异步函数装饰器的不同写法

实践：依次实现并测试：日志装饰器、耗时统计装饰器、`@retry(times=3)`、异步函数的重试与超时装饰器。特别注意：不能把同步包装器错误地用于异步函数。

## 5. 迭代器与生成器

- 可迭代对象（iterable）与迭代器（iterator）的区别
- `iter()`、`next()`、`StopIteration`；`for` 循环的底层过程
- 实现类迭代器：`__iter__` 与 `__next__`
- 生成器函数、生成器表达式、`yield`
- 惰性求值、状态保留、一次性消费
- `yield from`
- `send()`、`throw()`、`close()`：理解即可，优先掌握现代 `async`/`await`
- `itertools`：`chain`、`islice`、`groupby`、`batched` 等常用工具

实践：用生成器实现数据库/接口分页的惰性拉取，以及 LLM token 流的逐段处理；观察它们不会一次性把全部结果加载进内存。

## 6. 并发前置概念

先不写复杂代码，先建立正确分类能力：

- 并发（concurrency）与并行（parallelism）
- 阻塞与非阻塞
- CPU 密集型与 I/O 密集型任务
- 进程、线程、协程各自的资源模型
- 竞态条件、原子性、锁、队列、背压
- 超时、取消、异常传播和资源清理

判断口诀：大量等待网络、数据库、文件或模型接口时，优先考虑异步 I/O 或线程；纯 Python 的大量计算要考虑多进程。

## 7. 多线程与多进程

### 多线程

- GIL 的实际影响与边界
- `threading.Thread`、`Lock`、`RLock`、`Event`、`Queue`
- `concurrent.futures.ThreadPoolExecutor`
- `Future`、结果获取、异常处理、超时
- 线程池死锁和共享可变状态问题

### 多进程

- `multiprocessing` 和 `ProcessPoolExecutor`
- 进程隔离、序列化（pickle）和数据传输成本
- 子进程入口与 `if __name__ == "__main__"`
- 进程池适合的 CPU 密集任务

实践：分别用线程池和进程池执行 I/O 模拟任务与 CPU 模拟任务，测量耗时并解释差异。

## 8. asyncio 与协程

这是 FastAPI 和 Agent 编排最需要深入的一部分。

- 协程函数、协程对象、事件循环
- `await` 到底在等待什么
- `asyncio.create_task()`、Task、`asyncio.gather()`
- `asyncio.TaskGroup`：结构化并发
- `asyncio.wait_for()`、`asyncio.timeout()`：超时
- 取消：`CancelledError`、取消传播、清理资源
- `asyncio.Semaphore`：并发限流
- `asyncio.Queue`：生产者—消费者与背压
- 异步 HTTP/数据库客户端的正确使用
- 同步阻塞函数为什么会卡住事件循环
- `asyncio.to_thread()` 处理 I/O 型同步调用；CPU 密集任务使用进程池或外部任务系统

实践：实现一个并发调用多个 LLM/工具的编排器，要求具备并发上限、单任务超时、失败隔离、取消清理和结果汇总。

## 9. 综合项目：Agent 工具调用编排器

把前面的知识整合为一个可测试的小项目：

- `ToolRegistry` 使用对象协议和装饰器注册工具
- 同时支持同步和异步工具
- 统一工具调用结果和异常
- 并发执行多个异步工具，限制并发数
- 每个工具支持超时、重试和结构化日志
- 用生成器或异步生成器提供流式事件输出
- 为成功、失败、超时、取消和重试写测试

完成后，你不仅能应对语言机制相关面试题，还能将代码直接迁移到 FastAPI 或 AI Agent 的实际项目中。

## 学习方式建议

1. 先自己预测代码的输出和执行顺序，再运行验证。
2. 每个主题建立一个最小可运行示例，不只阅读。
3. 为每个示例写 2～3 个 `pytest` 测试，尤其测试边界和异常。
4. 记录“我原先以为会怎样，实际上为什么不是这样”。这类笔记最适合面试复习。
5. 不必一次学完；保持顺序即可。遇到真实项目问题时，跳到对应主题学习是完全合理的。

## 推荐资料

- 《流畅的 Python（第 2 版）》：围绕本清单阅读对象模型、函数、迭代器、协程与并发相关章节。
- [Python 官方数据模型文档](https://docs.python.org/3/reference/datamodel.html)
- [Python 官方 asyncio 文档](https://docs.python.org/3/library/asyncio.html)
- [Python 官方 concurrent.futures 文档](https://docs.python.org/3/library/concurrent.futures.html)
