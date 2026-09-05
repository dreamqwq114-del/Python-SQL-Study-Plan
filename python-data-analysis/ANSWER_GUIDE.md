# 参考答案使用说明

重构后，每一章的教材、示例、练习、答案和测试都放在同一个章节目录中：

```text
course/<主题>/<章节>/
├── lesson.md      # 教材
├── example.py     # 课堂示例
├── practice.py    # 练习题（需要你完成 TODO）
├── answer.py      # 参考答案
└── test.py        # 本章契约测试
```

`answer.py` 与 `practice.py` 的函数接口一一对应，目前包含：

- Python：9 章、36 道答案
- Pandas：14 章、42 道答案
- Matplotlib：6 章、18 道答案
- scikit-learn：15 章、45 道答案
- 综合客户项目（`projects/combined_customer_project/`）：6 道答案

推荐顺序：

1. 阅读本章 `lesson.md` 并亲自运行短代码。
2. 从项目根目录运行 `example.py`（`python -m course.<主题>.<章节>.example`），确认完整流程能工作。
3. 只编辑同目录 `practice.py` 中的 TODO。
4. 运行 `pytest course/<主题>/<章节>/test.py`，根据失败信息修改。
5. 尝试过多种方法仍卡住时，再查看同目录 `answer.py`。
6. 理解差异后关闭答案，在 `practice.py` 中从头独立写一遍。

答案不是需要背诵的唯一写法。只要你的实现满足题目明确规定的输入、返回值、特殊情况和不修改输入等要求，并通过测试，就可以采用不同的清晰写法。

不要修改答案或测试来让失败消失。答案测试的作用是证明题目、参考实现和测试契约互相一致；练习测试才反映你的完成进度。
