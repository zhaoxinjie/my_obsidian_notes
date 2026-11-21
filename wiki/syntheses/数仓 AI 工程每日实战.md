---
type: synthesis
status: active
created: 2026-10-16
updated: 2026-11-16
tags: [warehouse, practice, agent]
---

# 数仓 AI 工程每日实战

学习路线：确定性脚本与契约 → Skill → 只读 MCP → Agent 工作流 → 测试与评估。
进度：已布置第 01–25 练，尚无完成反馈；不等同于已掌握。

## 第 01 练：检查 Hive 表字段变化

目标：用 Python 3 标准库比较两个表结构 JSON，返回新增、删除、类型变化和检查状态。无需集群和额外依赖。

### 核心概念（2 分钟）

- **输入输出契约**：明确接受怎样的元数据、返回怎样的结果，以及错误如何表达，后续才能可靠接入自动流程。关联 [[wiki/concepts/工具|工具]]。
- **确定性检查与策略分离**：字段差异是事实；哪些差异要阻断是团队规则。本练习约定新增可通过，删除或任何类型变化需要审核，不宣称这是 Hive 的兼容性规则。

职责：今天实现的是脚本；后续 Skill 描述何时、如何使用它，MCP 提供标准工具访问接口，Agent 根据目标和工具结果决定下一步。普通函数调用本身不是 Agent。参见 [[wiki/concepts/MCP|MCP]]、[[wiki/concepts/构建高效智能体|构建高效智能体]]。

### 动手（10 分钟）

1. 将下面代码保存为 `schema_check.py`，先读懂样例中的三处变更。
2. 运行 `python3 schema_check.py`，核对结果与退出码。
3. 将新旧结构改成相同，再运行；随后将新结构改为重复字段，观察错误。

```python
import json
import sys


def parse_schema(text):
    rows = json.loads(text)
    if not isinstance(rows, list):
        raise ValueError("结构必须是字段数组")
    result = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("字段必须是对象")
        name, kind = row.get("name"), row.get("type")
        if not all(isinstance(x, str) and x.strip() for x in (name, kind)):
            raise ValueError("name 和 type 必须是非空字符串")
        name, kind = name.strip().lower(), kind.strip().lower()
        if name in result:
            raise ValueError("重复字段: " + name)
        result[name] = kind
    return result


def check(old_text, new_text):
    try:
        old, new = parse_schema(old_text), parse_schema(new_text)
    except ValueError as exc:
        return {"status": "invalid_input", "error": str(exc)}, 2
    added = sorted(new.keys() - old.keys())
    removed = sorted(old.keys() - new.keys())
    changed = [
        {"name": name, "before": old[name], "after": new[name]}
        for name in sorted(old.keys() & new.keys())
        if old[name] != new[name]
    ]
    review = bool(removed or changed)
    return {
        "status": "needs_review" if review else "pass",
        "added": added, "removed": removed, "type_changed": changed,
    }, 1 if review else 0


if __name__ == "__main__":
    old_text = '''[
      {"name":"id","type":"bigint"},
      {"name":"amount","type":"int"},
      {"name":"legacy","type":"string"}
    ]'''
    new_text = '''[
      {"name":"id","type":"bigint"},
      {"name":"amount","type":"bigint"},
      {"name":"channel","type":"string"}
    ]'''
    report, code = check(old_text, new_text)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(code)
```

运行命令：

```sh
python3 schema_check.py
echo $?
```

预期结果（格式缩写）：

```json
{"status":"needs_review","added":["channel"],"removed":["legacy"],"type_changed":[{"name":"amount","before":"int","after":"bigint"}]}
```

退出码为 `1`，表示需要审核；`0` 表示按本练习策略通过；`2` 表示输入无效。调用者应同时处理状态和退出码。

### 自测（3 分钟）

| 输入变化 | 预期 |
| --- | --- |
| 原始样例 | channel 新增、legacy 删除、amount 类型变化，状态 needs_review，码 1 |
| 新旧结构完全相同 | 三个差异列表均为空，状态 pass，码 0 |
| 只有新增字段 | added 有值，状态 pass，码 0 |
| 新结构为 `[{"name":"id","type":"int"},{"name":"ID","type":"bigint"}]` | invalid_input，提示重复字段，码 2 |
| 新结构为 `{}`、损坏的 JSON 或缺少 type | invalid_input，码 2，不出现未捕获异常 |

独立挑战：增加 `has_changes` 布尔字段，要求“只有新增字段”时为 true，“结构相同”时为 false。不要直接用 status 是否为 pass 推导。

范围：仅比较普通字段名和类型文本，忽略顺序；对大小写与首尾空白做规范化。不解析 DDL、分区、复杂类型语义或字段重命名；类型文本相异一律提交审核。空数组代表无普通字段，当前契约允许。

### 反馈与后续

请回报：实际输出、通过哪些自测、挑战结果以及卡住的位置。之后再决定是练习文件输入与自动测试，还是进入 Skill 封装。

关联：[[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]。本练习由 2026-10-16 本聊天的每日实战请求生成，规则为教学约定；概念基础见 [[wiki/concepts/工具]] 及其来源链接。


## 第 02 练：检查字段说明完整性

日期：2026-10-17。第 01 练尚无完成反馈，本练保持入门难度且可独立运行。
复习入口：回看第 01 练，说明为什么“只有新增字段”时 pass 仍可能有变更。

目标与交付物：用 Python 3 标准库编写 `metadata_check.py`，检查模拟 Hive 表的字段说明，输出可供后续工具消费的结构化问题清单。无需集群或额外依赖。

### 核心概念（2 分钟）

- **输入无效与治理不合格分开**：字段名缺失属于输入契约错误；说明缺失属于治理发现。前者要求修复调用数据，后者要求补齐业务知识。
- **确定性规则与语义判断分开**：脚本可以判断说明是否为空，但不能据此断言说明准确。未来 Agent 可以提出候选说明，需结合业务来源审核。

今天仍是脚本。Skill 可描述检查流程与处理规则；MCP 可提供元数据读取和检查的工具接口；Agent 可根据目标选择工具、补充信息并提出修复建议。脚本调用本身不构成 Agent。关联 [[wiki/concepts/工具]]、[[wiki/concepts/MCP]]。

### 动手（10 分钟）

1. 复制以下完整示例，保存为 `metadata_check.py`（约 4 分钟）。
2. 运行并解释为什么只报告 amount（约 2 分钟）。
3. 补齐 amount 的说明，再制造重复字段，分别观察输出（约 4 分钟）。

输入契约：JSON 对象，包含非空 table 字符串和非空 columns 数组；每个字段有唯一的非空 name。comment 允许缺失或 null（视为缺少说明），存在非 null 值时必须是字符串。忽略其他属性；字段名按去首尾空白、转小写判重。这是教学约定。

```python
import json
import sys


def check(text):
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("输入必须是对象")
        table = data.get("table")
        if not isinstance(table, str) or not table.strip():
            raise ValueError("table 必须是非空字符串")
        columns = data.get("columns")
        if not isinstance(columns, list) or not columns:
            raise ValueError("columns 必须是非空数组")
        seen, issues = set(), []
        for col in columns:
            if not isinstance(col, dict):
                raise ValueError("字段必须是对象")
            name = col.get("name")
            if not isinstance(name, str) or not name.strip():
                raise ValueError("name 必须是非空字符串")
            name = name.strip().lower()
            if name in seen:
                raise ValueError("重复字段: " + name)
            seen.add(name)
            comment = col.get("comment")
            if comment is not None and not isinstance(comment, str):
                raise ValueError("comment 必须是字符串或 null")
            if comment is None or not comment.strip():
                issues.append({"field": name, "rule": "missing_comment"})
        return {
            "status": "needs_review" if issues else "pass",
            "table": table.strip(), "issues": issues,
        }, 1 if issues else 0
    except ValueError as exc:
        return {"status": "invalid_input", "error": str(exc)}, 2


if __name__ == "__main__":
    text = '''{"table":"dwd.orders","columns":[
      {"name":"id","comment":"订单唯一编号"},
      {"name":"amount","comment":"  "}
    ]}'''
    report, code = check(text)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(code)
```

运行：

```sh
python3 metadata_check.py
echo $?
```

预期输出（忽略缩进）：

```json
{"status":"needs_review","table":"dwd.orders","issues":[{"field":"amount","rule":"missing_comment"}]}
```

退出码为 1；说明齐全返回 0；无效输入返回 2。遇到无效字段时返回整个输入无效，不输出可能不完整的治理清单。

### 自测（3 分钟）

每次修改 text 后运行，核对 JSON 和退出码：

| 输入修改 | 预期 |
| --- | --- |
| 原始示例 | 仅 amount 缺少说明；needs_review，1 |
| amount 的 comment 改为“订单金额，单位元” | issues 为空；pass，0 |
| 删除 amount 的 comment 或改为 null | 仍报告 amount；needs_review，1 |
| 增加字段 `{"name":"ID","comment":"重复"}` | invalid_input，2，错误提示重复字段 |
| amount 的 comment 改为数字 123 | invalid_input，2 |
| columns 改为空数组，或输入为损坏 JSON | invalid_input，2；无未捕获异常 |

独立挑战：增加规则 `placeholder_comment`，把去空白、忽略大小写后的 `todo`、`待补充` 也标为问题。要求：空说明仍只报 missing_comment，不能对同一问题重复报告；有效说明仍通过。先自行写出两个预期结果，再修改代码。

限制：只检查说明存在性；不会证明业务含义、金额单位或口径正确，也不读取 Hive Metastore，不修改元数据。

请反馈：通过几项自测、挑战输出和实际用时；若第 01 练仍卡住，直接指出卡住的位置，下一练据此调整。

来源与关联：本练为本聊天每日实战请求的原创教学示例；治理方向参考 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]] 中的元数据要求，工具契约依据 [[wiki/concepts/工具]] 及其来源。没有使用需联网核实的新 API。


## 第 03 练：把检查结果生成治理报告

日期：2026-10-18。第 01–02 练尚无完成反馈；今天可独立完成，不要求先实现上一练。
复习入口：用一句话解释“缺少字段说明”和“comment 类型错误”为什么要分开处理。

目标与交付物：编写 `render_report.py`，把模拟的字段说明检查结果转换成 Markdown 报告。只需 Python 3 标准库，无需集群、模型或额外依赖。

### 核心概念（2 分钟）

- **检查与呈现分离**：检查器负责事实，报告器负责呈现，避免生成文档时重新猜测业务结论。
- **边界契约校验**：输入即使来自另一个工具，也要验证状态与问题列表是否一致。无效输入不应被渲染成“检查通过”。

今天实现确定性报告脚本。Skill 可规定先检查、再生成报告的流程；MCP 可暴露这两项能力；Agent 可选择何时调用、补充信息或请求审核。生成固定模板无需模型推理。关联 [[wiki/concepts/工具]]、[[wiki/concepts/MCP]]。

### 动手（10 分钟）

1. 将以下完整代码保存为 `render_report.py`（4 分钟）。
2. 运行，核对报告；把输入改成无问题版本再运行（3 分钟）。
3. 制造状态矛盾，确认脚本拒绝输出成功报告（3 分钟）。

契约：接受第 02 练正常检查结果的 JSON；status 只能是 pass 或 needs_review，且必须与 issues 是否为空一致；本练只支持 missing_comment。为简化 Markdown 呈现，仅接受英文字母或下划线开头、后接字母数字下划线的字段名，以及以点分隔这类标识符的表名。不覆盖全部 Hive 合法命名。invalid_input 结果应由调用者处理，不能当成正常报告输入。

```python
import json
import re
import sys

IDENT = r"[A-Za-z_][A-Za-z0-9_]*"


def render(text):
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("输入必须是对象")
    table, issues = data.get("table"), data.get("issues")
    if not isinstance(table, str) or not re.fullmatch(IDENT + r"(?:\." + IDENT + r")*", table):
        raise ValueError("table 必须是支持的表标识符")
    if not isinstance(issues, list):
        raise ValueError("issues 必须是数组")
    expected = "needs_review" if issues else "pass"
    if data.get("status") != expected:
        raise ValueError("状态与问题列表不一致或不受支持")
    lines = ["# 字段说明治理报告", "", "表：" + table,
             "检查状态：" + expected, "问题数：" + str(len(issues)), ""]
    for item in issues:
        if not isinstance(item, dict):
            raise ValueError("问题项必须是对象")
        field = item.get("field")
        if not isinstance(field, str) or not re.fullmatch(IDENT, field):
            raise ValueError("field 必须是支持的字段标识符")
        if item.get("rule") != "missing_comment":
            raise ValueError("不支持的规则")
        lines.append("- " + field + "：缺少字段说明；请负责人补充并审核。")
    if not issues:
        lines.append("本次未发现字段说明缺失；不代表业务口径已验证。")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    text = '''{"status":"needs_review","table":"dwd.orders",
      "issues":[{"field":"amount","rule":"missing_comment"}]}'''
    try:
        report = render(text)
    except ValueError as exc:
        print(json.dumps({"status": "invalid_input", "error": str(exc)},
                         ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
    print(report, end="")
```

运行（先直接预览，确认成功后才保存）：

```sh
python3 render_report.py
```

预期输出：

```text
# 字段说明治理报告

表：dwd.orders
检查状态：needs_review
问题数：1

- amount：缺少字段说明；请负责人补充并审核。
```

成功渲染退出码为 0，即使报告包含治理问题；渲染输入无效时退出码为 2，错误 JSON 写到标准错误，不产生报告正文。注意与第 02 练不同：这里退出码表示“报告生成是否成功”，检查状态保留在正文中。

确认成功后，可用 `python3 render_report.py > report.md` 保存到当前练习目录；该命令会覆盖同名文件，首次使用请确保文件名未被其他资料占用。打开生成的 Markdown 查看效果。

### 自测（3 分钟）

| 修改输入 | 预期 |
| --- | --- |
| 原始样例 | 显示 amount 问题，问题数 1；退出码 0 |
| status 改为 pass、issues 改为 [] | 问题数 0，含“本次未发现”限定说明；退出码 0 |
| 仅把 status 改为 pass | 拒绝渲染，状态矛盾；退出码 2 |
| rule 改为 unknown，或 issues 改为对象 | 拒绝渲染；退出码 2 |
| JSON 损坏，或字段名含换行 | 拒绝渲染；退出码 2，无成功报告正文 |

独立挑战：在最后增加“待处理字段：amount”一行，多字段按名称排序；无问题时显示“待处理字段：无”。要求使用已经校验的数据，不凭空生成字段名。先自行写下有两个问题时的预期文本，再改代码。

限制：只呈现输入中的发现，不验证字段业务含义，不补写说明，不读取或修改真实元数据。本练的规则白名单尚未接纳第 02 练可选挑战的 placeholder_comment；如果你已做该挑战，需要显式扩展映射并补测试，不能默默丢弃未知规则。

请回报：自测结果、挑战输出和用时；若前两练未做，可只提交今天的结果。后续根据反馈决定巩固脚本还是进入 Skill 封装。

来源与关联：本聊天的原创练习；契约思想见 [[wiki/concepts/工具]]，治理用途见 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]。未使用外部 API。


## 第 04 练：用字段白名单生成查询草稿

日期：2026-10-19。前三练尚无完成反馈，本练保持入门难度，可独立运行。
复习入口：第 03 练为什么要拒绝“pass 状态却带有问题”的结果？今天同样在工具入口验证契约。

目标与交付物：用 Python 3 标准库编写 `sql_draft.py`，从固定模拟元数据生成指定日期的 Hive/Spark SQL 查询草稿，并编写一个正常用例和一个异常用例。无需额外依赖、集群或付费 API。

### 核心概念（2 分钟）

- **白名单约束**：只允许元数据声明的表和字段，避免把调用者的任意文本直接拼进 SQL。SQL 生成能力越受约束，越容易验证。
- **生成与验证分层**：下面只验证输入契约和生成文本；SQL 是否能在真实环境执行、业务口径是否正确，需要另行验证。固定模板不需要模型推理。

今天是确定性脚本。未来 Skill 可规定何时生成和审核草稿，MCP 可提供元数据读取与生成接口，Agent 可选择工具并根据反馈调整请求；本脚本不执行 SQL，也不构成 Agent。关联 [[wiki/concepts/工具]]、[[wiki/concepts/MCP]]、[[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]。

### 动手（10 分钟）

1. 保存以下完整示例为 `sql_draft.py`（4 分钟）。
2. 运行并核对 SQL；把字段顺序换一下，观察输出（3 分钟）。
3. 添加异常用例：不存在的字段、非法日期（3 分钟）。

教学契约：元数据是代码中可信的固定白名单；dt 是 YYYY-MM-DD 格式的字符串分区，选择字段不为空且不重复，大小写严格匹配。暂不开放用户传入元数据、过滤表达式、排序表达式或 LIMIT。并非通用 SQL 生成器。

```python
from datetime import date
import re

SCHEMA = {"dwd.orders": {"id", "amount", "dt"}}


def build_sql(table, fields, day):
    if not isinstance(table, str) or table not in SCHEMA:
        raise ValueError("表不在白名单")
    if not isinstance(fields, list) or not fields:
        raise ValueError("fields 必须是非空数组")
    if not all(isinstance(f, str) and f in SCHEMA[table] for f in fields):
        raise ValueError("字段不在白名单")
    if len(set(fields)) != len(fields):
        raise ValueError("字段不能重复")
    if not isinstance(day, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", day):
        raise ValueError("日期格式必须是 YYYY-MM-DD")
    date.fromisoformat(day)  # 检查日期真实存在，例如拒绝 2026-02-30
    quoted_table = ".".join("`" + part + "`" for part in table.split("."))
    selected = ", ".join("`" + f + "`" for f in fields)
    return (f"SELECT {selected} FROM {quoted_table} "
            f"WHERE `dt` = '{day}' LIMIT 10;")


if __name__ == "__main__":
    sql = build_sql("dwd.orders", ["id", "amount"], "2026-10-18")
    expected = ("SELECT `id`, `amount` FROM `dwd`.`orders` "
                "WHERE `dt` = '2026-10-18' LIMIT 10;")
    assert sql == expected
    try:
        build_sql("dwd.orders", ["id; DROP TABLE x"], "2026-10-18")
    except ValueError:
        pass
    else:
        raise AssertionError("必须拒绝白名单外的字段")
    print(sql)
    print("2 个基础自测通过")
```

运行（普通模式，不加 -O，以保留 assert）：

```sh
python3 sql_draft.py
```

预期输出：

```text
SELECT `id`, `amount` FROM `dwd`.`orders` WHERE `dt` = '2026-10-18' LIMIT 10;
2 个基础自测通过
```

函数对无效输入抛出 ValueError，交由后续调用层转换为结构化错误；当前示例中的 try/except 演示如何断言异常。没有实现命令行输入解析。

### 自测（3 分钟）

| 调用变化 | 预期 |
| --- | --- |
| 原始调用 | 与 expected 完全一致 |
| fields 改为 ["amount", "id"] | SELECT 顺序跟随输入，不自动排序 |
| fields 改为 []、["id", "id"] 或 ["unknown"] | ValueError，不生成 SQL |
| 表改为 ods.unknown | ValueError |
| 日期改为 2026-02-30 或 2026-1-1 | ValueError |
| 日期中拼入 SQL 文本 | ValueError |

独立挑战：新增 limit 参数，只接受 1–100 的整数并拒绝 bool、浮点数和字符串。先写明 limit=1、limit=101、limit=True 的预期结果，再实现；默认值保持 10。

范围与风险边界：LIMIT 只限制返回行数，不保证扫描量或运行成本；本练不连接集群，也不验证真实分区类型、权限、表存在性或业务口径。不能把白名单检查等同于完整 SQL 校验。

请回报：两个基础自测是否通过、你追加的异常用例、挑战结果及用时。尚未做前三练也可以只交本练，后续按反馈调整节奏。

来源：本聊天原创教学示例，工具契约及数仓元数据依据上方 wiki 关联页；没有使用外部 SDK 或新 API。


## 第 05 练：给 SQL 生成器增加 JSON 调用接口

日期：2026-10-20。前四练尚无完成反馈，今天提供完整独立示例，不要求已保存第 04 练脚本。
复习入口：回看第 04 练，解释白名单检查为什么不能证明 SQL 的业务口径正确。

目标与交付物：保存 `sql_tool.py`，通过标准输入读取一个 JSON 请求，成功返回 SQL，输入错误返回结构化错误。仅需 Python 3 标准库，无集群、额外依赖或 API。

### 核心概念（2 分钟）

- **业务函数与调用适配层分开**：build_sql 负责生成；handle 负责请求契约、错误转换和返回状态；主程序负责输入输出。
- **稳定错误码**：调用者用 error.code 分支处理，用 message 阅读原因，避免靠匹配自由文本作决定。

这是普通命令行 JSON 接口，不是 MCP 服务。Skill 可描述何时调用、如何处理错误；MCP 可在未来提供标准协议接口；Agent 决定调用和后续行动。关联 [[wiki/concepts/工具]]、[[wiki/concepts/MCP]]。

### 动手（10 分钟）

1. 保存下方完整代码为 `sql_tool.py`（4 分钟）；生成函数沿用第 04 练，不用重新设计。
2. 运行正常请求，核对 JSON（3 分钟）。
3. 运行未知字段请求，核对稳定错误码与退出码（3 分钟）。

契约：一个进程处理一个 JSON 对象，读到标准输入结束后返回。顶层键严格为 table、fields、day；其余限制沿用代码内固定白名单与日期校验。标准输出仅一行结果 JSON，成功退出 0，预期输入错误退出 2。只捕获 ValueError，不把意外程序缺陷伪装成输入错误。

```python
import json
import sys
from datetime import date
import re

SCHEMA = {"dwd.orders": {"id", "amount", "dt"}}


def build_sql(table, fields, day):
    if not isinstance(table, str) or table not in SCHEMA:
        raise ValueError("表不在白名单")
    if not isinstance(fields, list) or not fields:
        raise ValueError("fields 必须是非空数组")
    if not all(isinstance(f, str) and f in SCHEMA[table] for f in fields):
        raise ValueError("字段不在白名单")
    if len(set(fields)) != len(fields):
        raise ValueError("字段不能重复")
    if not isinstance(day, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", day):
        raise ValueError("日期格式必须是 YYYY-MM-DD")
    date.fromisoformat(day)  # 检查日期真实存在，例如拒绝 2026-02-30
    quoted_table = ".".join("`" + part + "`" for part in table.split("."))
    selected = ", ".join("`" + f + "`" for f in fields)
    return (f"SELECT {selected} FROM {quoted_table} "
            f"WHERE `dt` = '{day}' LIMIT 10;")


def handle(text):
    try:
        request = json.loads(text)
        if not isinstance(request, dict):
            raise ValueError("请求必须是 JSON 对象")
        if set(request) != {"table", "fields", "day"}:
            raise ValueError("请求必须且只能包含 table、fields、day")
        sql = build_sql(request["table"], request["fields"], request["day"])
        return {"ok": True, "sql": sql}, 0
    except ValueError as exc:
        return {"ok": False, "error": {
            "code": "invalid_input", "message": str(exc)
        }}, 2


if __name__ == "__main__":
    result, exit_code = handle(sys.stdin.read())
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(exit_code)

```

正常请求（命令中的单引号只用于 shell 包住 JSON）：

```sh
printf '%s' '{"table":"dwd.orders","fields":["id"],"day":"2026-10-19"}' | python3 sql_tool.py
echo $?
```

预期结果（忽略 JSON 属性间空格）：

```json
{"ok":true,"sql":"SELECT `id` FROM `dwd`.`orders` WHERE `dt` = '2026-10-19' LIMIT 10;"}
```

退出码 0。此管道中 Python 是最后一个命令，紧接着的 echo 显示其退出码。

异常请求：

```sh
printf '%s' '{"table":"dwd.orders","fields":["unknown"],"day":"2026-10-19"}' | python3 sql_tool.py
echo $?
```

预期结果：

```json
{"ok":false,"error":{"code":"invalid_input","message":"字段不在白名单"}}
```

退出码 2，不包含 sql。不要直接运行脚本后等待交互提示：它会等待完整标准输入，使用上述管道即可。

### 自测（3 分钟）

| 输入 | 预期 |
| --- | --- |
| 正常请求 | ok=true，sql 正确，退出 0 |
| unknown 字段 | ok=false，invalid_input，无 sql，退出 2 |
| 缺少 day 或多传 limit | invalid_input，提示顶层键不符合契约，退出 2 |
| 顶层是 [] 或 null | invalid_input，提示必须为对象，退出 2 |
| 非法日期、损坏 JSON 或空输入 | invalid_input，退出 2 |

独立挑战：给成功与失败结果都添加 `schema_version: 1`。先写下两种预期 JSON，再改代码；验证结果中的 ok、sql、error 和退出码仍符合原约定。思考版本号为什么应在两条路径都存在。

限制：只生成草稿，不执行 SQL；该协议不处理流式请求、网络、MCP 握手或并发。JSON 格式错误的 message 可能随 Python 版本变化，调用方应依赖稳定的 error.code。

请回报：正常/异常请求输出、退出码、挑战结果和实际用时；仍卡在前几练也可以直接指出，不推定已完成。

来源与关联：本聊天原创教学示例，契约设计见 [[wiki/concepts/工具]]；数仓应用背景见 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]。未使用外部 SDK 或新 API。


## 第 06 练：给 SQL 工具加自动回归测试

日期：2026-10-21。前五练仍待完成反馈；本练只练自动验证，暂不增加 Skill/MCP 接口复杂度。
复习入口：第 05 练的错误码为什么比错误提示文本更适合程序判断？

目标与交付物：给现成的 SQL JSON 工具编写三项命令行测试，覆盖正常 SQL、未知字段、损坏 JSON。只需 Python 3 标准库；不需要先完成或复制前五练。

### 核心概念（2 分钟）

- **黑盒契约测试**：像调用者一样启动进程，同时检查输出 JSON、退出码和标准错误。只调用内部函数无法发现命令行封装问题。
- **验证测试有用**：故意让 SQL 的 LIMIT 出错，观察正常用例失败，再恢复；测试全绿之前先证明它能发现目标错误。

今天测试的是确定性脚本。Skill 可规定调用前后的检查流程；MCP 提供标准工具接口；Agent 根据目标和反馈决策。回归测试保护共同的底层工具契约，但不能替代模型行为评估或集群执行验证。参见 [[wiki/concepts/工具]]、[[wiki/concepts/AI评估]]。

### 动手（10 分钟）

完整文件已放在练习目录，无需安装依赖：

- [[system/exercises/06-sql-tool-tests/sql_tool.py|完整 SQL 工具]]：第 05 练代码的练习副本。
- [[system/exercises/06-sql-tool-tests/test_sql_tool.py|完整测试代码]]：见下方，可先阅读，再自行重写一项测试。

```python
import json
from pathlib import Path
import subprocess
import sys
import unittest

TOOL = Path(__file__).with_name("sql_tool.py")


class SqlToolTests(unittest.TestCase):
    def call_tool(self, text):
        proc = subprocess.run(
            [sys.executable, str(TOOL)], input=text,
            capture_output=True, text=True, timeout=3,
        )
        self.assertEqual(proc.stderr, "")
        self.assertEqual(len(proc.stdout.splitlines()), 1)
        return proc.returncode, json.loads(proc.stdout)

    def test_success(self):
        code, result = self.call_tool(json.dumps({
            "table": "dwd.orders", "fields": ["id"], "day": "2026-10-20"
        }))
        self.assertEqual(code, 0)
        self.assertEqual(result, {
            "ok": True,
            "sql": "SELECT `id` FROM `dwd`.`orders` WHERE `dt` = '2026-10-20' LIMIT 10;"
        })

    def test_unknown_field(self):
        code, result = self.call_tool(json.dumps({
            "table": "dwd.orders", "fields": ["unknown"], "day": "2026-10-20"
        }))
        self.assertEqual(code, 2)
        self.assertIs(result["ok"], False)
        self.assertEqual(result["error"]["code"], "invalid_input")
        self.assertNotIn("sql", result)

    def test_malformed_json(self):
        code, result = self.call_tool("{")
        self.assertEqual(code, 2)
        self.assertIs(result["ok"], False)
        self.assertEqual(result["error"]["code"], "invalid_input")
        self.assertNotIn("sql", result)


if __name__ == "__main__":
    unittest.main()

```

1. 阅读三项测试，辨认“输入、执行、断言”（3 分钟）。正常输入是 dwd.orders / id / 2026-10-20；异常输入分别是 unknown 字段和损坏的 JSON `{`。
2. 在任意终端目录执行下面命令（2 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/06-sql-tool-tests/test_sql_tool.py -v
```

预期三个测试均为 ok，末尾为 `Ran 3 tests` 和 `OK`，进程退出码为 0。耗时数字因环境而异。

3. 仅修改练习副本 sql_tool.py 中的 `LIMIT 10;` 为 `LIMIT 11;`，再运行同一命令（3 分钟）。预期 test_success 失败，报告 `FAILED (failures=1)`，测试进程非零退出。
4. 恢复为 LIMIT 10，重新运行，确认全部通过（2 分钟）。不要修改预期结果来迎合错误实现。

### 自测（3 分钟）

- 正常工具：3 项全部通过；正常 SQL 与预期逐字一致。
- unknown 字段：返回 invalid_input 和退出码 2，不能带 sql。
- 损坏 JSON：返回 invalid_input 和退出码 2，不依赖具体解析错误文案。
- 注入 LIMIT 错误：测试确实失败；恢复后通过。

注意：异常用例中的工具退出码 2 是预期结果，因此整个测试套件仍应通过并退出 0；二者不要混淆。

独立挑战：新增 test_invalid_date，用 2026-02-30 调用工具，断言退出码 2、ok=false、error.code=invalid_input 且无 sql。完成后预期为 4 项测试通过。先写断言再运行。

限制：仅验证本地进程契约与固定模板，未验证 SQL 在 Spark/Hive 的真实执行、权限或业务口径。timeout=3 为教学默认值，慢设备可调大，不应因此删掉超时保护。若你做过第 05 练 schema_version 挑战，精确结果断言需要明确升级契约；今天的独立副本尚不含该字段。

请回报：三项测试结果、是否观察到故意错误被抓住、第四项挑战及用时；仍可提交前几练卡点，不把已布置当成已掌握。

来源：本聊天原创教学测试，工具能力边界见 [[wiki/concepts/工具]] 及 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]；无外部 API。


## 第 07 练：为 SQL 工具编写 Skill 工作流程

本练对应 2026-10-24 的触发请求，2026-10-26 完成交付；仅按已交付练习连续编号，不补发空缺日期。第 01–06 练尚无完成反馈，不推定已掌握。
复习入口：第 06 练中，工具退出 2 为什么可以让异常测试通过？若仍不熟悉，今天只做“齐参/缺参”两种场景。

目标与交付物：修改一份 SKILL.md，让智能体知道何时用已有 SQL 工具、缺少信息怎么办、调用失败如何处理。底层脚本保持原样。仅需 Python 3 标准库，无模型 API、集群或额外依赖。

### 核心概念（2 分钟）

- **Skill 是任务指导与资源包**：description 帮助判断适用场景，正文规定操作流程，scripts 保存确定性能力。写了 Markdown 不代表工具逻辑会自动执行。
- **流程也要验收**：除了脚本输出，还要检查缺参不猜测、失败不绕过规则、生成不冒充执行。

职责分工：脚本负责校验并生成 SQL；Skill 指导怎样使用；MCP 提供标准连接协议（今天未实现）；Agent 根据请求与结果做决定（今天用手工场景演练检验流程）。

### 最小完整示例与动手（10 分钟）

文件已准备在 system/exercises/07-sql-skill/warehouse-sql-draft/：SKILL.md 与 scripts/sql_tool.py。它们是教学草案，尚未安装或验证自动发现；今天手动阅读并执行，不依赖 $技能名 的自动调用。

1. 阅读下方完整 SKILL.md，找到适用范围、缺参处理、错误处理三处（3 分钟）。
2. 执行正常请求，核对退出码与 JSON（3 分钟）。
3. 手工按技能流程走一遍缺参及异常场景，在笔记中记录实际决策（4 分钟）。

````markdown
---
name: warehouse-sql-draft
description: 为模拟 dwd.orders 表生成指定日期、指定字段的 Hive/Spark SQL 查询草稿；适用于学习环境中的简单分区取样查询。
---

# 数仓 SQL 草稿

本技能仅覆盖模拟 dwd.orders 表，字段白名单为 id、amount、dt。dt 为 YYYY-MM-DD 字符串分区，固定 LIMIT 10。复杂聚合、JOIN 或实际集群执行超出本练习范围，应说明限制。

## 工作流程

1. 从用户请求中提取 table、fields、day。缺少任一项时，询问缺失项并等待回复；不猜日期，不默认选择全部字段。
2. 参数齐全时，将对象 JSON 编码后交给本技能目录内 scripts/sql_tool.py 的标准输入。不要将用户原话直接拼接为 shell 命令。可用下方 subprocess 示例，按实际技能目录设置脚本路径。
3. 检查进程退出码和结果 JSON：退出 0 且 ok=true 时，展示 sql，并说明“仅完成输入与模板检查，未在集群执行、未验证业务口径”。退出 2 且 error.code=invalid_input 时，报告错误原因并请用户更正对应参数；不绕过白名单，不反复重试相同请求。其他失败应说明工具异常，不编造 SQL。
4. 用户若要求执行 SQL，说明本练习只提供草稿；不声称已经运行。

## 本地调用示例

在技能目录内运行：

```python
import json
from pathlib import Path
import subprocess
import sys

request = {"table": "dwd.orders", "fields": ["id"], "day": "2026-10-23"}
proc = subprocess.run(
    [sys.executable, str(Path("scripts/sql_tool.py").resolve())],
    input=json.dumps(request), capture_output=True, text=True, timeout=3,
)
print(proc.returncode)
print(proc.stdout, end="")
```

````

正常请求运行命令：

```sh
printf '%s' '{"table":"dwd.orders","fields":["id"],"day":"2026-10-23"}' | python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/07-sql-skill/warehouse-sql-draft/scripts/sql_tool.py
echo $?
```

预期结果：

```json
{"ok":true,"sql":"SELECT `id` FROM `dwd`.`orders` WHERE `dt` = '2026-10-23' LIMIT 10;"}
```

退出码 0。按 Skill 交付时还需说明尚未执行和验证业务口径。

异常请求：把 fields 中的 id 改成 unknown，重新执行。预期 ok=false、error.code=invalid_input、message 为“字段不在白名单”、退出码 2；不返回 sql。

### 自测（3 分钟）

| 请求/输入 | 应有决策或输出 |
| --- | --- |
| “为 dwd.orders 查询 2026-10-23 的 id，取 10 行草稿” | 参数齐全，调用工具，交付 SQL 和验证范围 |
| “为 dwd.orders 查 id” | 先问日期；不调用、不猜当天日期 |
| fields 为 unknown | 展示字段错误，请求更正；不改成 id 偷偷重试 |
| “执行生成的 SQL” | 说明练习只产出草稿；不报告执行成功 |

前两项既可手工扮演，也可将实际 SKILL.md 路径与请求交给有本地文件访问能力的助手，显式要求先读文件再操作。手工检查只证明流程能被理解；脚本检查只证明工具行为，二者都不等同于真实智能体行为评估。

独立挑战：增加一条“用户要求全字段时，不擅自展开，先确认具体字段列表”的流程说明，并写一个正例和一个反例作为验收场景。无需改 Python；不要把 SKILL.md 的名称写对当成行为已通过。

请回报：完整请求输出、缺参时准备问的那句话、挑战的两条验收场景及用时。下一练根据反馈决定继续练 Skill 还是开始只读 MCP。

来源与关联：本聊天原创教学草案，结构依据本地 skill-creator/SKILL.md；工具契约见 [[wiki/concepts/工具]]，协议角色见 [[wiki/concepts/MCP]]。今天不依赖任何宿主应用的安装或自动发现行为。


## 第 08 练：将模拟 Hive 表结构暴露为只读 MCP 工具

交付日期：2026-10-28。承接 2026-10-27 未完成的练习；前七练尚无完成反馈。今天只做一个工具，不接真实集群。
复习入口：第 07 练里，Skill 为什么不能替代 Python 工具的字段校验？

目标与交付物：运行 MCP 服务和客户端，完成工具发现，以及已知/未知表的两次调用。文件已放在 system/exercises/08-readonly-mcp/。Python 3.10+；首次下载依赖需要联网。练习采用固定版本 mcp==1.28.0 的 v1 SDK API，不表示它是最新版本，不与 v2 示例混用。

### 核心概念（2 分钟）

- **协议接口与业务函数分离**：catalog.py 负责模拟元数据；server.py 将函数暴露为 MCP 工具；client.py 通过 stdio 通信，进行初始化、工具发现和调用。普通 JSON 脚本不会自动具备这些协议行为。
- **协议成功与业务成功分离**：未知表在本练中返回 ok=false / table_not_found，属于可解析的业务结果，不将它伪装成成功查表。MCP isError 和业务 ok 是两个不同层次。

Skill 指导何时调用，MCP 连接调用双方，Agent 根据目标决定调用与后续行动。今天的客户端按固定步骤调用，没有模型决策，不构成 Agent。关联 [[wiki/concepts/MCP]]、[[wiki/concepts/工具]]。

### 完整最小示例

**catalog.py**

```python
def lookup_schema(table: str) -> dict:
    if table != "dwd.orders":
        return {"ok": False, "error": {"code": "table_not_found"}}
    return {"ok": True, "table": table, "columns": [
        {"name": "id", "type": "bigint"},
        {"name": "amount", "type": "decimal(18,2)"},
        {"name": "dt", "type": "string"}
    ]}
```

**server.py**

```python
import json
from mcp.server.fastmcp import FastMCP
from catalog import lookup_schema

mcp = FastMCP("warehouse-metadata-demo")


@mcp.tool()
def get_table_schema(table: str) -> str:
    """只读查询模拟 Hive 表结构，仅支持 dwd.orders；不执行 SQL。"""
    return json.dumps(lookup_schema(table), ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**client.py**

```python
import asyncio
import json
from pathlib import Path
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("server.py").resolve())],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert [t.name for t in tools.tools] == ["get_table_schema"]
            print("工具发现通过")
            for table in ["dwd.orders", "unknown.table"]:
                result = await session.call_tool(
                    "get_table_schema", arguments={"table": table}
                )
                assert not result.isError
                payload = json.loads(result.content[0].text)
                if table == "dwd.orders":
                    assert payload == {"ok": True, "table": table, "columns": [
                        {"name": "id", "type": "bigint"},
                        {"name": "amount", "type": "decimal(18,2)"},
                        {"name": "dt", "type": "string"}
                    ]}
                else:
                    assert payload == {"ok": False, "error": {
                        "code": "table_not_found"
                    }}
                print(json.dumps(payload, ensure_ascii=False))
            print("2 个 MCP 调用场景通过")


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=15))
```

### 动手（10 分钟）

1. 创建隔离环境并安装固定依赖（约 3 分钟，首次网络下载较慢时另计准备时间）。在终端执行：

```sh
cd /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/08-readonly-mcp
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

2. 阅读装饰器、初始化、list_tools 和 call_tool 四处代码（约 3 分钟）。服务端不要向 stdout 打印调试信息，那里用于 stdio 协议通信；客户端可以正常打印结果。
3. 运行客户端（约 4 分钟），它会自动启动服务进程，不必另开终端：

```sh
.venv/bin/python client.py
```

预期标准输出（JSON 空白可不同；SDK 日志可能出现在标准错误）：

```text
工具发现通过
{"ok": true, "table": "dwd.orders", "columns": [{"name": "id", "type": "bigint"}, {"name": "amount", "type": "decimal(18,2)"}, {"name": "dt", "type": "string"}]}
{"ok": false, "error": {"code": "table_not_found"}}
2 个 MCP 调用场景通过
```

### 自测（3 分钟）

- 工具发现只包含 get_table_schema。
- dwd.orders 返回三个指定字段及类型；未知表返回 table_not_found。
- 所有断言通过，客户端退出 0；超时或断言失败不能算通过。
- 客户端退出后服务随 stdio 上下文关闭；不会查询或修改真实数仓。

独立挑战：在 catalog.py 中增加模拟 dwd.users（id bigint、dt string），保留未知表错误行为；在客户端增加新表调用并断言字段类型。不要增加执行 SQL 的工具。

若依赖安装不通，可先在此练习目录运行下面的无依赖自测，但它只能证明业务函数工作，不能替代 MCP 连通验收：

```sh
python3 -c 'from catalog import lookup_schema; assert lookup_schema("dwd.orders")["ok"] is True; assert lookup_schema("unknown.table")["error"]["code"] == "table_not_found"; print("业务逻辑自测通过，MCP 连通待验证")'
```

验证记录：交付时已做三份 Python 文件语法检查，已验证已知表、未知表以及返回值修改不污染后续查询。此前依赖下载遇到网络限制，扩展权限下载未完成；未在本环境完成 MCP 协议连通测试，不据此宣称已跑通。

请反馈：Python 版本、安装是否成功、客户端输出与挑战结果。若安装卡住，贴出错误末尾即可，后续先处理环境，不加难度。

来源：官方 [v1 SDK 说明](https://py.sdk.modelcontextprotocol.io/v1/)、[服务端文档](https://py.sdk.modelcontextprotocol.io/v1/server/)、[客户端文档](https://py.sdk.modelcontextprotocol.io/v1/client/)，本聊天据其接口编写教学示例。SDK 主版本不同会影响代码用法，因此固定依赖版本。这里只演示本机 stdio，不涉及宿主应用配置或生产权限。


## 第 09 练：为工具返回值设计错误分支

日期：2026-10-29。前八练仍待完成反馈；第 08 练 MCP 连通尚未验证。今天使用模拟返回值，完全独立运行，不安装依赖。
复习入口：第 08 练中，为什么 isError 为假仍可能查不到表？

目标与交付物：编写 route_result.py，根据表结构工具的返回值决定继续、请用户确认表名或停止；不把工具失败误判为可继续。不连接真实数仓。

### 核心概念（2 分钟）

- **分层错误**：工具执行失败、表不存在、返回结构损坏需要不同动作，不能统一无限重试。
- **数据契约与停止条件**：只有结构满足预期，且表名与请求一致，才允许进入后续步骤。continue 只表示收到合格结构，不代表 SQL 或业务口径正确。

输入为本练自己定义的规范化字典：tool_error 是 bool，payload 是已解析的业务 JSON。本练不直接接收 MCP SDK 对象；未来适配器需要检查 MCP isError、解析内容并处理连接异常，不能把本字典冒充完整 MCP 消息。今日没有使用需查证的新 SDK API。

脚本执行规则判断；Skill 描述这些判断何时适用；MCP 负责连接；Agent 才负责根据任务做后续决策。固定规则分支本身不是 Agent。关联 [[wiki/concepts/工具]]、[[wiki/concepts/MCP]]、[[wiki/concepts/harness工程]]。

### 完整最小示例与动手（10 分钟）

文件：[[system/exercises/09-tool-result-routing/route_result.py|route_result.py]]。仅需 Python 3 标准库。

```python
def decide(result, expected_table="dwd.orders"):
    stop = {"action": "stop", "reason": "invalid_result"}
    if not isinstance(result, dict) or type(result.get("tool_error")) is not bool:
        return stop
    if result["tool_error"]:
        return {"action": "stop", "reason": "tool_failure"}
    payload = result.get("payload")
    if not isinstance(payload, dict):
        return stop
    if payload.get("ok") is False:
        error = payload.get("error")
        if isinstance(error, dict) and error.get("code") == "table_not_found":
            return {"action": "ask_user", "reason": "confirm_table"}
        return {"action": "stop", "reason": "unknown_business_error"}
    if payload.get("ok") is not True or payload.get("table") != expected_table:
        return stop
    columns = payload.get("columns")
    if not isinstance(columns, list) or not columns:
        return stop
    names = set()
    for column in columns:
        if not isinstance(column, dict):
            return stop
        name, kind = column.get("name"), column.get("type")
        if not all(isinstance(x, str) and x.strip() for x in (name, kind)):
            return stop
        key = name.strip().lower()
        if key in names:
            return stop
        names.add(key)
    return {"action": "continue", "reason": "schema_received"}


if __name__ == "__main__":
    good = {"tool_error": False, "payload": {
        "ok": True, "table": "dwd.orders",
        "columns": [{"name": "id", "type": "bigint"}]
    }}
    missing = {"tool_error": False, "payload": {
        "ok": False, "error": {"code": "table_not_found"}
    }}
    failed = {"tool_error": True, "payload": None}
    cases = [(good, "continue"), (missing, "ask_user"),
             (failed, "stop"), ({"tool_error": False, "payload": {}}, "stop")]
    for result, expected in cases:
        decision = decide(result)
        assert decision["action"] == expected
        print(decision["action"] + ": " + decision["reason"])
    print("4 个基础场景通过")

```

1. 阅读 good/missing/failed 三份样例，预测输出（3 分钟）。
2. 运行下面命令，核对实际结果（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/09-tool-result-routing/route_result.py
```

预期输出：

```text
continue: schema_received
ask_user: confirm_table
stop: tool_failure
stop: invalid_result
4 个基础场景通过
```

3. 修改样例：返回另一张表、添加大小写重复字段，再分别核对 stop（4 分钟）。恢复原始示例后再次运行。

### 自测（3 分钟）

| 输入 | 预期 |
| --- | --- |
| 合格的 dwd.orders 结构 | continue / schema_received |
| table_not_found | ask_user / confirm_table，不自动改表名 |
| tool_error=true，即使 payload 看似成功 | stop / tool_failure |
| payload 缺少 ok 或返回另一张表 | stop / invalid_result |
| 空字段列表、字段缺类型、字段重复 | stop / invalid_result |

本地策略约定普通字段数组非空；这是教学检查条件，并非声称 Hive 的完整 schema 规范。代码不会处理复杂类型语义。输入类型损坏应返回 stop，不产生未捕获异常。

独立挑战：新增 reason=permission_denied 分支：当业务错误码为 permission_denied 时，返回 stop，不重试。先写预期决策，再增加分支和一个断言；不要把它放在通用未知错误返回之后。

落地问题：如果 action=ask_user，你会向用户问哪一句话？写下问题，并明确收到回复前不会调用后续 SQL 生成器。

验证记录：交付时四个命令行场景通过，另验证五项损坏/错表/重复字段输入会停止。未开展 MCP 连通测试或真实 Agent 决策评估。

请反馈：四个场景输出、你设计的确认问题、挑战断言和实际用时。下一练据此决定继续巩固错误处理还是衔接 MCP 客户端。

来源与关联：本聊天原创练习，承接本页第 08 练的双层状态；工具契约见 [[wiki/concepts/工具]]，数仓场景见 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]。


## 第 10 练：将人工审核结果绑定到 SQL 草稿版本

日期：2026-10-30。前九练仍待用户反馈，MCP 连通也未确认；本练独立运行，Python 3 标准库即可，无需集群或模型 API。
复习入口：第 09 练中为什么工具失败应停止，而不是猜一个结果继续？今天把相同思路用于过期审核。

目标与交付物：编写 review_gate.py，区分待审核、审核匹配、草稿变更和拒绝四种状态。输出只做状态判断，不调用执行器。

### 核心概念（2 分钟）

- **审核绑定具体产物**：审核结果应针对用户实际看过的 SQL；SQL 改变后要重新审核，不能只保留一个 approved=true。
- **版本指纹不是身份认证**：SHA-256 方便判断文本版本是否相同，不能证明是谁审核、是否有权审核。本练 approval 是模拟数据，不能把它当真实授权凭证。

固定规则脚本负责版本核对；Skill 可规定呈现 SQL、收集人工结果、变更后重新审核的流程；MCP 可承载受控工具调用；Agent 在这些边界内选择行动。今天没有模型决策或 MCP 调用，不构成完整 Agent 系统。关联 [[wiki/concepts/工具]]、[[wiki/concepts/harness工程]]。

### 最小完整示例与动手（10 分钟）

文件已备好：[[system/exercises/10-sql-review-gate/review_gate.py|review_gate.py]]。

```python
import hashlib


def fingerprint(sql):
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("SQL 必须是非空字符串")
    return hashlib.sha256(sql.encode("utf-8")).hexdigest()


def review_gate(sql, approval=None):
    try:
        current = fingerprint(sql)
    except ValueError:
        return {"status": "invalid_input", "executed": False}
    if approval is None:
        return {"status": "needs_review", "sql_sha256": current,
                "executed": False}
    if (not isinstance(approval, dict)
            or type(approval.get("approved")) is not bool
            or not isinstance(approval.get("sql_sha256"), str)):
        return {"status": "invalid_approval", "executed": False}
    if approval["approved"] is False:
        return {"status": "rejected", "executed": False}
    if approval["sql_sha256"] != current:
        return {"status": "stale_approval", "executed": False}
    return {"status": "review_matched", "sql_sha256": current,
            "executed": False}


if __name__ == "__main__":
    sql = "SELECT `id` FROM `dwd`.`orders` WHERE `dt` = '2026-10-29' LIMIT 10;"
    card = review_gate(sql)
    # 模拟人工查看 SQL 后留下审核结果；此处不是实际用户授权。
    approval = {"approved": True, "sql_sha256": card["sql_sha256"]}
    cases = [
        (sql, None, "needs_review"),
        (sql, approval, "review_matched"),
        (sql.replace("LIMIT 10", "LIMIT 100"), approval, "stale_approval"),
        (sql, {"approved": False, "sql_sha256": card["sql_sha256"]}, "rejected"),
    ]
    for text, audit, expected in cases:
        result = review_gate(text, audit)
        assert result["status"] == expected
        assert result["executed"] is False
        print(result["status"])
    print("4 个基础场景通过；未执行 SQL")

```

1. 阅读 sql、card、approval 三个变量，指出审批针对哪份文本（3 分钟）。
2. 执行下面命令并核对四个分支（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/10-sql-review-gate/review_gate.py
```

预期输出：

```text
needs_review
review_matched
stale_approval
rejected
4 个基础场景通过；未执行 SQL
```

3. 把查询日期从 2026-10-29 改为其他日期，沿用旧 approval 调用 review_gate，验证 stale_approval（4 分钟）。应先用旧 SQL 生成 card，再修改 SQL，避免重新算出新审核指纹后误以为旧审核仍有效。

### 自测（3 分钟）

| 场景 | 预期 |
| --- | --- |
| SQL 合法且无审核结果 | needs_review |
| approved=true 且指纹匹配 | review_matched；executed=false |
| 修改 LIMIT 或日期，沿用旧结果 | stale_approval |
| approved=false | rejected |
| 空 SQL、非字符串 SQL | invalid_input |
| approved 为字符串或缺少指纹 | invalid_approval |

所有状态都必须 executed=false。这里“SQL 合法”仅指非空字符串，不是 SQL 语法、权限、业务或成本校验；即使 SELECT 1 也可被计算指纹。逐字节比较 UTF-8 文本指纹，所以只改空白也需重新审核，这是本练有意采用的简单策略。

独立挑战：增加 reviewer 非空字符串字段检查，缺失或空白时返回 invalid_approval。先写一个缺失与一个正常 reviewer 的预期结果，再实现；同时更新模拟 approval，否则原有基础示例会按新契约失败。思考：字符串名字为什么仍不能证明真实审核者身份？

落地范围：真实人工批准必须由可信的用户交互和受控存储记录；不能让模型自行生成 approval 后宣称得到人类批准。本练只演示版本检查，不设计认证系统或接入生产执行权限。

验证记录：四个命令行场景及七项非法输入/审核对象检查通过。没有执行 SQL，也没有验证真实用户身份或数据库行为。

请反馈：四项输出、修改日期后的结果、reviewer 挑战及用时。若前几练卡住，可只指出卡点，后续不自动提高难度。

来源与关联：本聊天原创教学示例；行动契约与停止边界见 [[wiki/concepts/工具]] 和 [[wiki/concepts/harness工程]]，数仓上下文见 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]。未使用外部 SDK 或变化中的 API。


## 第 11 练：为表结构查询生成可追踪记录

日期：2026-10-31。前十练尚无完成反馈；本练可独立完成。复习入口：第 09 练的“停止”结果若没有记录原因，日后排查会缺少什么信息？

目标与交付物：用 trace_lookup.py 为模拟元数据查询输出 JSON Lines（一行一个 JSON 事件），能区分一次运行中的事件顺序及失败原因。Python 3 标准库即可，无集群、模型 API 或依赖安装。

### 核心概念（2 分钟）

- **关联标识与顺序号**：run_id 将同次运行串联，seq 标记该运行内事件顺序；不能仅依赖一堆无法关联的打印文字。
- **事件摘要与事实边界**：记录实际发生的步骤、状态和必要摘要；未执行 SQL 就不记执行成功。日志辅助排查，不自动证明业务结果正确。

脚本负责事件记录；Skill 可规定需记录哪些关键边界；MCP 连接工具与调用者；Agent 使用工具反馈做决策。今天是固定的模拟查询流程，不是完整 Agent，也不是 MCP 客户端。关联 [[wiki/concepts/harness工程]]、[[wiki/concepts/工具]]、[[wiki/concepts/AI评估]]。

### 最小完整示例与动手（10 分钟）

文件：[[system/exercises/11-workflow-trace/trace_lookup.py|trace_lookup.py]]。

```python
import json
from uuid import uuid4


def trace_lookup(table):
    run_id = uuid4().hex
    events = []

    def emit(step, status, detail):
        events.append({"run_id": run_id, "seq": len(events) + 1,
                       "step": step, "status": status, "detail": detail})

    if not isinstance(table, str) or not table.strip():
        emit("workflow", "stopped", {"reason": "invalid_table"})
        return events
    emit("schema_lookup", "started", {"table": table})
    if table != "dwd.orders":
        emit("schema_lookup", "failed", {"code": "table_not_found"})
        emit("workflow", "stopped", {"reason": "confirm_table"})
        return events
    # 模拟只读工具调用成功；摘要不代表真实集群查询结果。
    emit("schema_lookup", "succeeded", {"column_count": 3})
    emit("workflow", "paused", {"reason": "awaiting_next_step"})
    return events


if __name__ == "__main__":
    for table in ["dwd.orders", "unknown.table"]:
        events = trace_lookup(table)
        for event in events:
            print(json.dumps(event, ensure_ascii=False))

```

1. 阅读 emit，解释 run_id 在哪生成、seq 为何从 1 开始（3 分钟）。
2. 执行命令，找到成功路径和失败路径各三条事件（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/11-workflow-trace/trace_lookup.py
```

预期共 6 行 JSON。首组三行状态依次 started、succeeded、paused；第二组三行依次 started、failed、stopped。实际 run_id 每次不同；下面用 RUN_A/RUN_B 代示，非固定输出：

```json
{"run_id":"RUN_A","seq":1,"step":"schema_lookup","status":"started","detail":{"table":"dwd.orders"}}
{"run_id":"RUN_A","seq":2,"step":"schema_lookup","status":"succeeded","detail":{"column_count":3}}
{"run_id":"RUN_A","seq":3,"step":"workflow","status":"paused","detail":{"reason":"awaiting_next_step"}}
{"run_id":"RUN_B","seq":1,"step":"schema_lookup","status":"started","detail":{"table":"unknown.table"}}
{"run_id":"RUN_B","seq":2,"step":"schema_lookup","status":"failed","detail":{"code":"table_not_found"}}
{"run_id":"RUN_B","seq":3,"step":"workflow","status":"stopped","detail":{"reason":"confirm_table"}}
```

3. 将主程序中的一项输入改为 None，确认只有一条 invalid_table 停止事件；恢复后重复运行，确认 run_id 改变（4 分钟）。

### 自测（3 分钟）

- 同次运行所有事件 run_id 一致，两次运行 run_id 不同。
- 每次运行 seq 均从 1 连续递增。
- dwd.orders 的最后状态为 paused，不是“SQL 已执行”。
- unknown.table 先记录 table_not_found，再停止，不产生成功事件。
- None、数字和空字符串仅产生一条 invalid_table 事件，不出现未捕获异常。

独立挑战：新增 summarize(events) 函数，返回 run_id、event_count、final_status、reason；以最后一条事件决定最终状态和原因。先为成功路径、未知表路径写预期字典并断言；额外约定空事件列表应抛出 ValueError。不要因为出现 started 就判断运行成功。

范围：当前事件先保存在内存，再由独立脚本输出；进程崩溃时未必能保留历史，不是持久化审计系统。没有记录完整 SQL、凭证或数据行。未来在 stdio MCP 服务中使用时，应将诊断日志写到标准错误或专用日志接口，不能占用协议标准输出；本练是独立程序，输出本身就是交付物。

验证记录：实际运行得到 6 行合法 JSON，核对了两条路径、运行标识、序号及三类非法输入。没有验证真实 MCP 通信、崩溃恢复或 Agent 行为。

请反馈：六行输出能否分组、非法输入结果、汇总挑战及用时。若仍卡在 MCP 安装，可只提交本练，不要求先补齐前十练。

来源与关联：本聊天原创练习，长时流程交接与反馈原则见 [[wiki/concepts/harness工程]]，评估用途见 [[wiki/concepts/AI评估]]；未使用外部 SDK 或变化中的 API。


## 第 12 练：评测工具结果决策，抓住危险误放行

日期：2026-11-01。前十一练尚无完成反馈；MCP 连通也未确认。本练独立运行，Python 3 标准库即可。
复习入口：第 09 练规定哪些情况下必须停止？第 11 练记录了事件，这次再给决策结果加可判定的评测。

目标与交付物：编写 evaluate.py，用带预期动作的案例评测决策函数，报告通过数、失败详情和误继续次数。重点是学会设计评测，不把“能跑”当成可靠。

### 核心概念（2 分钟）

- **案例与判分器分离**：每条案例包含输入、预期动作和稳定 id；evaluate 负责比较，policy 负责被测决策。预期答案由人依据需求确定，不从被测输出倒推。
- **单列高风险错误**：unsafe_continue 统计“应该询问或停止却继续”的次数。总通过率可能掩盖这种错误；该指标依赖人工标签，并不是生产安全证明。

今天评测的是第 09 练的确定性规则副本，不是模型 Agent 的行为。Skill 可规定使用哪组验收案例，MCP 可连接真实工具，Agent 可作为未来被测对象；更换为模型后还需验证重复运行、任务结果和真实工具轨迹。参见 [[wiki/concepts/AI评估]]、[[wiki/concepts/工具]]。

### 完整最小示例与动手（10 分钟）

完整文件位于 system/exercises/12-routing-eval/：

- [[system/exercises/12-routing-eval/policy.py|policy.py]]：第 09 练 decide 的独立副本，可直接阅读，无需之前做过该练。
- [[system/exercises/12-routing-eval/evaluate.py|evaluate.py]]：完整案例与判分代码如下。

```python
import json
from policy import decide

CASES = [
    {"id": "valid_schema", "expected": "continue", "input": {
        "tool_error": False, "payload": {"ok": True, "table": "dwd.orders",
        "columns": [{"name": "id", "type": "bigint"}]}}},
    {"id": "missing_table", "expected": "ask_user", "input": {
        "tool_error": False, "payload": {"ok": False,
        "error": {"code": "table_not_found"}}}},
    {"id": "tool_failure", "expected": "stop", "input": {
        "tool_error": True, "payload": None}},
    {"id": "broken_payload", "expected": "stop", "input": {
        "tool_error": False, "payload": {}}},
]


def evaluate(cases, policy):
    if not cases:
        raise ValueError("评测集不能为空")
    passed, unsafe_continue, failures = 0, 0, []
    for case in cases:
        actual = policy(case["input"])["action"]
        if actual == case["expected"]:
            passed += 1
        else:
            failures.append({"id": case["id"], "expected": case["expected"],
                             "actual": actual})
        if actual == "continue" and case["expected"] != "continue":
            unsafe_continue += 1
    return {"total": len(cases), "passed": passed,
            "unsafe_continue": unsafe_continue, "failures": failures}


if __name__ == "__main__":
    report = evaluate(CASES, decide)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["passed"] == report["total"] else 1)

```

1. 先看四项案例，不运行代码，写下应该继续/询问/停止的理由（3 分钟）。
2. 运行评测（2 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/12-routing-eval/evaluate.py
```

预期输出（格式缩写）：

```json
{"total":4,"passed":4,"unsafe_continue":0,"failures":[]}
```

退出码 0。

3. 只在今天的 policy.py 练习副本中，把 decide 临时改为总返回 `{"action":"continue"}`，运行同一命令（3 分钟）。预期 total=4、passed=1、unsafe_continue=3；failures 列出 missing_table、tool_failure、broken_payload，退出码 1。不要修改 expected 来让错误策略通过。
4. 恢复 policy.py，再运行确认四项通过（2 分钟）。修改前可先复制内容到临时笔记，方便恢复；不要改动第 09 练原文件。

### 自测（3 分钟）

- 原规则：4/4，通过数正确，误继续为 0，退出 0。
- 总是继续：1/4，误继续为 3，失败详情能定位案例，退出 1。
- 恢复规则后结果恢复；本练没有调用 SQL 执行器或真实 MCP。

独立挑战：新增 wrong_table 案例：ok=true，但返回的表为 dwd.other（同时有非空合法 columns），预期 stop。先独立写完整输入；原规则应变成 5/5，总是继续应为 1/5、误继续为 4。注意：案例只改表名，避免用空 columns 提前触发另一条拒绝规则。

范围：这是最小教学集，不是具有统计代表性的 benchmark；空案例集抛 ValueError，若 policy 自身抛异常则评测进程失败，不将其假装为有效动作。本练只判 action，不证明 reason、业务答案或真实系统行为正确。

验证记录：已实际运行原规则得 4/4；在临时副本注入“总是继续”得 1/4、误继续 3 次且退出 1。交付的 policy.py 保持原规则。

请反馈：原规则报告、错误策略报告、第五项挑战结果和用时。后续根据实际卡点决定是否连接 MCP，不默认已经完成前十一练。

来源与关联：本聊天原创教学示例；评测设计见 [[wiki/concepts/AI评估]]，数仓背景见 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]。未使用新 SDK 或外部 API。


## 第 13 练：串联查结构、字段校验与 SQL 草稿生成

日期：2026-11-02。前十二练尚无完成反馈；MCP 连通尚待确认。本练不增加新依赖，可独立运行。
复习入口：第 12 练中为什么“应该停止却继续”要单独统计？今天检查错误能否真正阻止后续工具调用。

目标与交付物：实现 workflow.py，输入 table/fields/day，依次查模拟结构、校验字段、生成草稿，最后停在 needs_review。缺少参数或表不存在时询问；字段错误时停止。

### 核心概念（2 分钟）

- **工作流的阶段依赖**：后一步只在前一步满足条件时运行。返回一个 stopped 字符串还不够，必须确认后续函数确实没有执行。
- **工具与编排分离**：catalog.py 查询结构，sql_generator.py 生成 SQL，workflow.py 负责顺序、分支与停止。方便未来替换工具接入方式，而不混写一大段提示词。

今天是确定性 workflow，不是自主 Agent。Skill 可指导何时发起流程、如何向人呈现结果；MCP 可替换本地查询调用；Agent 可在受控边界内选择工具和处理反馈。没有模型决策也不宣称实现了 Agent。关联 [[wiki/concepts/构建高效智能体]]、[[wiki/concepts/工具]]、[[wiki/concepts/harness工程]]。

### 完整最小示例与动手（10 分钟）

准备好的独立目录 system/exercises/13-sql-workflow/ 包含：

- [[system/exercises/13-sql-workflow/catalog.py|catalog.py]]：第 08 练无依赖模拟元数据副本。
- [[system/exercises/13-sql-workflow/sql_generator.py|sql_generator.py]]：已有 SQL 生成函数副本。
- [[system/exercises/13-sql-workflow/workflow.py|workflow.py]]：完整编排代码如下。三个文件同目录，仅需 Python 3 标准库。

```python
import json
from catalog import lookup_schema
from sql_generator import build_sql


def run(request):
    steps = []

    def finish(status, **detail):
        return {"status": status, "steps": steps.copy(),
                "executed": False, **detail}

    steps.append("validate_request")
    if not isinstance(request, dict):
        return finish("stopped", reason="invalid_request")
    required = {"table", "fields", "day"}
    missing = sorted(required - request.keys())
    if missing:
        return finish("ask_user", missing=missing)
    if set(request) != required:
        return finish("stopped", reason="unexpected_keys")
    table, fields, day = request["table"], request["fields"], request["day"]
    if not isinstance(table, str) or not table.strip():
        return finish("stopped", reason="invalid_table")
    steps.append("lookup_schema")
    schema = lookup_schema(table)
    if schema["ok"] is not True:
        return finish("ask_user", reason=schema["error"]["code"])
    steps.append("validate_fields")
    allowed = {column["name"] for column in schema["columns"]}
    if (not isinstance(fields, list) or not fields
            or not all(isinstance(f, str) and f in allowed for f in fields)
            or len(set(fields)) != len(fields)):
        return finish("stopped", reason="invalid_fields")
    steps.append("build_sql")
    try:
        sql = build_sql(table, fields, day)
    except ValueError as exc:
        return finish("stopped", reason="invalid_sql_request", message=str(exc))
    return finish("needs_review", sql=sql)


if __name__ == "__main__":
    requests = [
        {"table": "dwd.orders", "fields": ["id"], "day": "2026-11-01"},
        {"table": "unknown.table", "fields": ["id"], "day": "2026-11-01"},
        {"table": "dwd.orders", "fields": ["unknown"], "day": "2026-11-01"},
    ]
    for request in requests:
        print(json.dumps(run(request), ensure_ascii=False))

```

1. 阅读三个阶段和提前 return 的位置，预测三份请求的结果（3 分钟）。
2. 运行下面命令，核对三行 JSON（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/13-sql-workflow/workflow.py
```

预期第一行：

```json
{"status":"needs_review","steps":["validate_request","lookup_schema","validate_fields","build_sql"],"executed":false,"sql":"SELECT `id` FROM `dwd`.`orders` WHERE `dt` = '2026-11-01' LIMIT 10;"}
```

第二行 status=ask_user、reason=table_not_found，steps 到 lookup_schema 为止；第三行 status=stopped、reason=invalid_fields，steps 到 validate_fields 为止。两行均没有 sql，且 executed=false。

3. 删除第一份请求的 day，观察 ask_user 和 missing=["day"]，此时 steps 仅有 validate_request；再把 day 改成 2026-02-30，观察 invalid_sql_request（4 分钟）。

### 自测（3 分钟）

- 正常请求最终 needs_review，而非已执行。
- 缺参时不查结构，查不到表时不生成 SQL，未知字段时不生成 SQL。
- 非法日期停止，返回中不含 sql；进入 build_sql 步骤不等于生成成功。
- 所有输出 executed=false；演示程序正常打印业务错误时进程仍可退出 0，不能用进程退出 0 推断每份请求成功。

独立挑战：增加字段数量上限 2，超过时返回 stopped/reason=too_many_fields，且不调用生成器。先写一份包含 id、amount、dt 的请求及预期 steps，再实现。用临时替换生成函数为“被调用就抛错”的方式，验证它没有被调用；完成后恢复。

范围：元数据来自可信固定函数，尚未加入第 09 练针对外部损坏结果的完整校验。生成函数仍保留 dwd.orders 静态白名单，支持新表需同步更新元数据与生成契约，本练不做泛化。needs_review 只是等待审核状态，不包含真实人工审批；第 10 练可在后续衔接，今天不要求一起实现。没有执行 SQL 或 MCP 通信。

验证记录：实际核对三条主路径及五项异常输入；用会抛错的生成函数验证缺参、未知表、未知字段三条路径确实未调用生成器。

请反馈：三条输出、缺参后的 steps、挑战结果与用时。仍卡在前练可直接说明，不默认已掌握十二练。

来源：本聊天原创教学编排，复用前练经验证的本地工具；分阶段流程依据 [[wiki/concepts/构建高效智能体]]，工程边界见 [[wiki/concepts/harness工程]]。未涉及变化中的 SDK/API。


## 第 14 练：把元数据查询换成可注入接口

日期：2026-11-03。前十三练尚无完成反馈；本练不要求 MCP 连通，Python 3 标准库即可。
复习入口：第 13 练为什么要证明“生成函数没被调用”，而不只检查最后状态是 stopped？

目标与交付物：将查询和生成函数作为参数传给工作流，用正常、超时、损坏结果三种场景证明查询接口可替换，失败后不会生成 SQL。

### 核心概念（2 分钟）

- **依赖注入**：通过 run(request, lookup=..., generate=...) 传入工具能力，编排流程不必绑定一种接入方式。未来可用适配器连接 MCP，但适配器仍需负责通信与解析。
- **故障注入**：用小函数稳定地产生 TimeoutError 或损坏结果，测试错误路径，无需让真实服务出故障。

Skill 规定使用流程，MCP 连接实际工具，Agent 决定使用哪些能力；今天仍是固定工作流和模拟工具，不将函数替换本身称作 Agent。

### 完整最小示例与动手（10 分钟）

独立目录 system/exercises/14-replaceable-lookup/ 已包含全部代码，无需复制前练或安装依赖：

- [[system/exercises/14-replaceable-lookup/workflow.py|完整工作流]]：下面的核心代码。
- [[system/exercises/14-replaceable-lookup/catalog.py|模拟元数据]]、[[system/exercises/14-replaceable-lookup/sql_generator.py|SQL 生成器]]、[[system/exercises/14-replaceable-lookup/result_policy.py|结果契约检查]]：前练函数的独立副本。
- [[system/exercises/14-replaceable-lookup/demo.py|完整运行与断言示例]]：正常输入与两类异常输入。

```python
import json
from catalog import lookup_schema
from sql_generator import build_sql
from result_policy import decide


def run(request, lookup=lookup_schema, generate=build_sql):
    steps = []

    def finish(status, **detail):
        return {"status": status, "steps": steps.copy(),
                "executed": False, **detail}

    steps.append("validate_request")
    if not isinstance(request, dict):
        return finish("stopped", reason="invalid_request")
    required = {"table", "fields", "day"}
    missing = sorted(required - request.keys())
    if missing:
        return finish("ask_user", missing=missing)
    if set(request) != required:
        return finish("stopped", reason="unexpected_keys")
    table, fields, day = request["table"], request["fields"], request["day"]
    if not isinstance(table, str) or not table.strip():
        return finish("stopped", reason="invalid_table")
    steps.append("lookup_schema")
    try:
        schema = lookup(table)
    except TimeoutError:
        return finish("stopped", reason="lookup_timeout")
    decision = decide({"tool_error": False, "payload": schema}, table)
    if decision["action"] == "ask_user":
        return finish("ask_user", reason="table_not_found")
    if decision["action"] != "continue":
        return finish("stopped", reason=decision["reason"])
    steps.append("validate_fields")
    allowed = {column["name"] for column in schema["columns"]}
    if (not isinstance(fields, list) or not fields
            or not all(isinstance(f, str) and f in allowed for f in fields)
            or len(set(fields)) != len(fields)):
        return finish("stopped", reason="invalid_fields")
    steps.append("build_sql")
    try:
        sql = generate(table, fields, day)
    except ValueError as exc:
        return finish("stopped", reason="invalid_sql_request", message=str(exc))
    return finish("needs_review", sql=sql)



```

1. 阅读 run 的两个默认函数参数，找到 lookup 与 generate 的调用位置（3 分钟）。
2. 阅读并运行下面的完整 demo（3 分钟）：

```python
from workflow import run

REQUEST = {"table": "dwd.orders", "fields": ["id"], "day": "2026-11-02"}


def timeout_lookup(table):
    raise TimeoutError("模拟查询超时")


def broken_lookup(table):
    return {"ok": True}  # 缺少表名和字段


if __name__ == "__main__":
    normal = run(REQUEST)
    assert normal["status"] == "needs_review" and "sql" in normal
    print("normal: " + normal["status"])
    for lookup, expected in [(timeout_lookup, "lookup_timeout"),
                             (broken_lookup, "invalid_result")]:
        calls = []

        def forbidden_generate(*args):
            calls.append(args)
            raise AssertionError("失败后不得调用生成器")

        result = run(REQUEST, lookup=lookup, generate=forbidden_generate)
        assert result["status"] == "stopped"
        assert result["reason"] == expected
        assert "build_sql" not in result["steps"]
        assert "sql" not in result and not calls
        assert result["executed"] is False
        print("failure: " + result["reason"] + "; generate_calls=0")
    print("3 个场景通过")

```

命令：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/14-replaceable-lookup/demo.py
```

预期输出：

```text
normal: needs_review
failure: lookup_timeout; generate_calls=0
failure: invalid_result; generate_calls=0
3 个场景通过
```

3. 将 broken_lookup 的返回值改成另一张表的完整结构，仍应被拒绝；再暂时删掉 workflow 中的结果检查，观察 demo 能否发现问题，最后恢复（4 分钟）。删掉检查后可能抛出异常或误入后续步骤，均应使测试失败，不能把这种失败改判为通过。

### 自测（3 分钟）

- 默认工具生成草稿，停在 needs_review。
- 模拟 TimeoutError 返回 lookup_timeout，不调用生成器。
- 损坏或错表结果返回 invalid_result，不调用生成器。
- 失败结果无 sql、executed=false，步骤列表没有 build_sql。

独立挑战：新增 denied_lookup，返回 {"ok": false, "error": {"code": "permission_denied"}}。为它添加断言：stopped、reason=unknown_business_error、生成器调用 0 次。然后考虑是否要给权限错误单独命名；若修改策略，需同步修改预期契约，不要只改测试让其通过。

限制：捕获 TimeoutError 不会自动给函数设置超时，也不能中断永久阻塞；今天只验证适配器主动报告超时后的处理。真实 MCP 适配器还需明确超时、取消、协议错误和结果解析。未捕获的意外异常会让进程失败，本练不把一切异常包装成“查询超时”。固定生成器仍只支持原来的 dwd.orders，未做通用数仓工具。

验证记录：实际运行正常、超时和损坏结果三项场景，后两项通过计数与禁止调用的函数核对生成器调用为 0。没有进行真实 MCP 通信或模型决策评测。

请反馈：三项输出、错表测试结果、权限错误挑战及用时；卡在前练也可直接说明，不自动提高难度。

来源与关联：本聊天原创教学示例，复用第 09、13 练本地函数；行动契约见 [[wiki/concepts/工具]]，编排边界见 [[wiki/concepts/harness工程]]，未来适配目标见 [[wiki/concepts/MCP]]。未使用外部 SDK 或变化中的 API。


## 第 15 练：给工具调用提议加白名单与预算

日期：2026-11-04。前十四练仍待反馈；本练可独立完成，Python 3 标准库即可，无模型 API、集群或依赖安装。
复习入口：第 14 练中，工具可替换之后，为什么仍不能允许调用方任意挑一个函数执行？

目标与交付物：实现 dispatch.py，只允许 get_table_schema，限制每次最多两次查询，拒绝未知工具和错误参数。用实际调用计数验证被拒绝的调用没有执行。

### 核心概念（2 分钟）

- **提议不等于执行权**：模型或上游程序可提出工具调用，执行层仍要验证名称、参数与可用预算，不能使用 eval 或根据工具名任意加载函数。
- **预算是执行前的条件**：第三次提议应在查询前拒绝；执行后才发现超限，已经无法避免那次成本。

下面 proposals 是人工构造的模拟模型输出，不是模型实际推理结果。脚本实现执行关卡；Skill 可指导何时查询和停止；MCP 负责工具通信；Agent 才根据反馈决定下一步。固定提议回放不构成完整 Agent。

### 完整最小示例与动手（10 分钟）

文件：[[system/exercises/15-tool-call-budget/dispatch.py|dispatch.py]]。模拟表只有 id 一个字段，专用于验证调用关卡，不表示真实 dwd.orders 的结构或覆盖此前示例元数据。

```python
import json


def lookup_schema(table):
    if table != "dwd.orders":
        return {"ok": False, "error": {"code": "table_not_found"}}
    return {"ok": True, "table": table,
            "columns": [{"name": "id", "type": "bigint"}]}


def dispatch(proposals, max_calls=2, lookup=lookup_schema):
    if (not isinstance(proposals, list) or type(max_calls) is not int
            or not 1 <= max_calls <= 10):
        raise ValueError("调用提议必须是数组，预算必须是 1–10 的整数")
    results = []

    def finish(status, reason):
        return {"status": status, "reason": reason,
                "calls": len(results), "results": results.copy()}

    for proposal in proposals:
        if len(results) >= max_calls:
            return finish("stopped", "call_budget_exceeded")
        if (not isinstance(proposal, dict)
                or set(proposal) != {"tool", "arguments"}):
            return finish("stopped", "invalid_proposal")
        if proposal["tool"] != "get_table_schema":
            return finish("stopped", "unknown_tool")
        args = proposal["arguments"]
        if (not isinstance(args, dict) or set(args) != {"table"}
                or not isinstance(args["table"], str) or not args["table"].strip()):
            return finish("stopped", "invalid_arguments")
        result = lookup(args["table"])
        results.append(result)
        if result.get("ok") is not True:
            return finish("stopped", "lookup_failed")
    return finish("completed", "proposals_consumed")


if __name__ == "__main__":
    call = {"tool": "get_table_schema", "arguments": {"table": "dwd.orders"}}
    cases = [
        ([call], "completed", "proposals_consumed", 1),
        ([call, call, call], "stopped", "call_budget_exceeded", 2),
        ([{"tool": "execute_sql", "arguments": {}}], "stopped", "unknown_tool", 0),
        ([{"tool": "get_table_schema", "arguments": {}}], "stopped", "invalid_arguments", 0),
    ]
    for proposals, status, reason, expected_calls in cases:
        seen = []

        def counted_lookup(table):
            seen.append(table)
            return lookup_schema(table)

        report = dispatch(proposals, lookup=counted_lookup)
        assert (report["status"], report["reason"]) == (status, reason)
        assert report["calls"] == len(seen) == expected_calls
        print(json.dumps({key: report[key] for key in ["status", "reason", "calls"]}))
    print("4 个调用关卡场景通过")

```

1. 阅读 call 与四组提议，先写下预期调用次数（3 分钟）。
2. 执行命令，核对报告与真实计数断言（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/15-tool-call-budget/dispatch.py
```

预期输出（JSON 空白可不同）：

```text
{"status": "completed", "reason": "proposals_consumed", "calls": 1}
{"status": "stopped", "reason": "call_budget_exceeded", "calls": 2}
{"status": "stopped", "reason": "unknown_tool", "calls": 0}
{"status": "stopped", "reason": "invalid_arguments", "calls": 0}
4 个调用关卡场景通过
```

3. 将预算改为 1：三次查询提议应在一次执行后停止；同步调整该场景的预期调用数。再将 table 改为 unknown，观察一次查询后 lookup_failed 停止（4 分钟）。

### 自测（3 分钟）

- 正常提议查询一次；completed 只表示这批提议已处理，不是 SQL 已执行或任务业务目标已完成。
- 三次合法提议、预算 2：实际查询恰好两次，第三次未执行。
- execute_sql 不在白名单：查询计数为 0。
- 缺少 table：查询计数为 0。
- 预算为 True、字符串、0 或超过 10 时抛 ValueError，不接受 bool 充当整数。

独立挑战：增加“同一表本次最多查询一次”的规则。两次相同表提议时，第二次查询前返回 stopped/duplicate_lookup，实际查询数为 1。先写预期，再实现；不要只修改最终报告的 calls 数字，要用 seen 验证真实调用数。

范围：每次 dispatch 独立计数，反复调用函数会重置预算；这不是跨轮 Agent 的全局预算，也不是超时或金额限制。当前使用可信的模拟查询返回值，意外异常会使程序失败；未来接入 MCP 需同时衔接第 09/14 练的结果校验和异常处理。未知工具检查与预算同时不满足时，本实现先报告预算耗尽。没有查询真实数仓或执行 SQL。

验证记录：四项运行场景通过，实际调用计数与报告一致；另验证四项非法预算、空提议、未知表业务失败。

请反馈：四项输出、预算改为 1 后的实际调用次数、去重挑战及用时。前练未做也可先交本练，后续不默认提升难度。

来源与关联：本聊天原创教学示例，工具能力边界见 [[wiki/concepts/工具]]，停止条件见 [[wiki/concepts/harness工程]]，协议角色见 [[wiki/concepts/MCP]]。未使用变化中的外部 SDK/API。


## 第 16 练：只对查询超时做有限重试

日期：2026-11-05。前十五练尚无完成反馈，MCP 连通未确认。本练独立运行，Python 3 标准库即可。
复习入口：第 15 练预算是先检查还是先调用？若一次查询内部重试两次，工具总预算应如何记账？

目标与交付物：retry_lookup.py，为只读模拟元数据查询提供最多两次尝试（含首次），只捕获 TimeoutError；表不存在、损坏结果不自动重试。

### 核心概念（2 分钟）

- **可重试错误需要明确分类**：本练约定只有适配器报告的 TimeoutError 可重试，表不存在不是临时网络故障，原参数重复调用通常不能修复它。
- **尝试次数含首次调用**：max_attempts=2 表示首次加一次重试；每次尝试都产生实际调用，不能只给成功请求计数。

这是工具适配层策略：Skill 可规定失败后如何呈现或询问；MCP 负责通信但不替你决定业务重试；Agent 的决策仍应受执行层预算约束。固定模拟序列不是 Agent 推理。

### 完整最小示例与动手（10 分钟）

文件：[[system/exercises/16-bounded-retry/retry_lookup.py|retry_lookup.py]]。

```python
def query_with_retry(query, max_attempts=2):
    if type(max_attempts) is not int or not 1 <= max_attempts <= 3:
        raise ValueError("max_attempts 必须是 1–3 的整数，含首次调用")
    for attempt in range(1, max_attempts + 1):
        try:
            result = query()
        except TimeoutError:
            if attempt == max_attempts:
                return {"status": "stopped", "reason": "timeout_exhausted",
                        "attempts": attempt}
            continue
        if not isinstance(result, dict) or type(result.get("ok")) is not bool:
            return {"status": "stopped", "reason": "invalid_result",
                    "attempts": attempt}
        if result["ok"] is False:
            return {"status": "stopped", "reason": "business_error",
                    "attempts": attempt, "result": result}
        return {"status": "received", "attempts": attempt, "result": result}


def scripted_query(outcomes):
    sequence = iter(outcomes)
    calls = []

    def query():
        calls.append("lookup")
        outcome = next(sequence)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    return query, calls


if __name__ == "__main__":
    success = {"ok": True, "table": "dwd.orders",
               "columns": [{"name": "id", "type": "bigint"}]}
    missing = {"ok": False, "error": {"code": "table_not_found"}}
    cases = [
        ("recover", [TimeoutError(), success], "received", 2),
        ("exhaust", [TimeoutError(), TimeoutError()], "stopped", 2),
        ("missing", [missing, success], "stopped", 1),
    ]
    for name, outcomes, status, attempts in cases:
        query, calls = scripted_query(outcomes)
        report = query_with_retry(query)
        assert report["status"] == status
        assert report["attempts"] == len(calls) == attempts
        if name == "exhaust":
            assert report["reason"] == "timeout_exhausted"
        if name == "missing":
            assert report["reason"] == "business_error"
        print(f"{name}: {status}; calls={len(calls)}")
    print("3 个有限重试场景通过")

```

1. 看三条 outcomes，先预测 calls 数量；尤其注意 missing 后虽准备了 success，也不该继续调用（3 分钟）。
2. 执行命令并核对输出（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/16-bounded-retry/retry_lookup.py
```

预期输出：

```text
recover: received; calls=2
exhaust: stopped; calls=2
missing: stopped; calls=1
3 个有限重试场景通过
```

3. 在 recover 场景把预算改为 1，观察一次超时就停止；同步调整预期，不应读取后面的 success。再传入损坏结果 {}，验证只调用一次（4 分钟）。

### 自测（3 分钟）

- 第一次超时、第二次成功：received，attempts=2，实际调用 2。
- 连续两次超时：timeout_exhausted，实际调用 2，无第三次。
- table_not_found：business_error，实际调用 1。
- 损坏结果：invalid_result，实际调用 1。
- PermissionError 等非 TimeoutError 异常不重试，由上层处理；本练不将其误报为超时。
- 预算 True、0、4、字符串均拒绝。

独立挑战：增加一个 delay(attempt) 可注入回调，仅在“还可重试的超时”之后调用。测试时传入记录列表的假回调，不实际等待；恢复场景应记录 [1]，连续超时耗尽也只记录 [1]，业务错误应记录 []。暂不做指数退避或随机抖动。

边界：本练没有实现超时计时或中断阻塞调用，也没有实际等待；TimeoutError 是模拟工具主动抛出的信号。只做了最低限度的 ok 字段校验，received 不代表完整 schema 合格，更不代表 SQL 已验证；后续仍应接第 09 练的结构检查。脚本未实现跨调用全局预算，接第 15 练时必须让每次重试占用共享预算，避免嵌套重试放大调用量。模拟序列用尽会报错，这是测试数据不足，不应包装成业务成功。

验证记录：三项主场景实际调用计数通过；另外核对四种非法预算、损坏结果不重试、PermissionError 传播且只调用一次。

请反馈：三行调用次数、预算 1 的结果、延迟回调挑战和用时。前练未做可只交本练，后续按卡点调整。

来源与关联：本聊天原创教学示例，契约和错误处理见 [[wiki/concepts/工具]]，调用控制见 [[wiki/concepts/harness工程]]，协议位置见 [[wiki/concepts/MCP]]。未调用外部 API 或真实服务。


## 第 17 练：让重试与多次查询共用调用预算

日期：2026-11-06。前十六练尚无完成反馈；本练独立运行，仅需 Python 3 标准库。
复习入口：第 16 练指出每次调用都重新创建重试次数，可能绕过第 15 练总预算。若两次查询各自重试两次，实际会调用几次？

目标与交付物：shared_budget.py，在一次模拟工作流开始时只创建一份 Budget；所有查询及其重试在调用前扣减它，用实际调用记录证明总次数不超过 3。

### 核心概念（2 分钟）

- **预算所有权**：总预算属于一次工作流，不能在每次查询或每轮模型决策中重新初始化。
- **预算耗尽与重试耗尽分开**：budget_exhausted 表示共享额度不够；timeout_exhausted 表示本次查询的尝试上限用完。两种停止原因帮助后续诊断和策略调整。

脚本强制执行预算；Skill 指导何时查询与如何呈现停止原因；MCP 提供连接；Agent 的下一步选择不能绕过预算。今天固定调用三个查询，不构成自主 Agent，也未接入 MCP。

### 完整最小示例与动手（10 分钟）

文件：[[system/exercises/17-shared-retry-budget/shared_budget.py|shared_budget.py]]。

```python
class Budget:
    def __init__(self, total):
        if type(total) is not int or not 0 <= total <= 10:
            raise ValueError("总预算必须是 0–10 的整数")
        self.remaining = total

    def take(self):
        if self.remaining == 0:
            return False
        self.remaining -= 1
        return True


def query_with_retry(query, budget, max_attempts=2):
    if type(max_attempts) is not int or not 1 <= max_attempts <= 3:
        raise ValueError("尝试上限必须是 1–3 的整数")
    attempts = 0
    while attempts < max_attempts:
        if not budget.take():
            return {"status": "budget_exhausted", "attempts": attempts}
        attempts += 1  # 首次、重试、超时都计入实际调用预算
        try:
            result = query()
        except TimeoutError:
            continue
        if not isinstance(result, dict) or type(result.get("ok")) is not bool:
            return {"status": "invalid_result", "attempts": attempts}
        if result["ok"] is False:
            return {"status": "business_error", "attempts": attempts}
        return {"status": "received", "attempts": attempts}
    return {"status": "timeout_exhausted", "attempts": attempts}


if __name__ == "__main__":
    budget = Budget(3)  # 本次工作流只创建一次，由所有查询共享
    outcomes = iter([TimeoutError(), {"ok": True}, TimeoutError(), {"ok": True}])
    calls = []

    def lookup():
        calls.append("lookup")
        outcome = next(outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    first = query_with_retry(lookup, budget)
    assert first == {"status": "received", "attempts": 2}
    print(f"first: {first['status']}; attempts={first['attempts']}; remaining={budget.remaining}")
    second = query_with_retry(lookup, budget)
    assert second == {"status": "budget_exhausted", "attempts": 1}
    print(f"second: {second['status']}; attempts={second['attempts']}; remaining={budget.remaining}")
    third = query_with_retry(lookup, budget)
    assert third == {"status": "budget_exhausted", "attempts": 0}
    assert len(calls) == 3 and budget.remaining == 0
    print(f"third: {third['status']}; attempts={third['attempts']}; actual_calls={len(calls)}")
    print("共享预算场景通过；第 4 个模拟结果未被读取")

```

1. 预测四个模拟结果中哪些会被读取；找到唯一创建 Budget(3) 的地方（3 分钟）。
2. 运行下面命令核对输出（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/17-shared-retry-budget/shared_budget.py
```

预期输出：

```text
first: received; attempts=2; remaining=1
second: budget_exhausted; attempts=1; remaining=0
third: budget_exhausted; attempts=0; actual_calls=3
共享预算场景通过；第 4 个模拟结果未被读取
```

3. 将总预算改成 0，先写下预期：三个查询都 budget_exhausted、attempts=0、实际调用总数 0。同步调整断言和输出描述后运行，再恢复原示例（4 分钟）。

### 自测（3 分钟）

- 首次查询超时后成功，消耗 2 次预算；第二次查询只剩 1 次机会。
- 总额度为 0 后第三次查询不再触发实际工具调用。
- 总预算 2、单次查询连续超时两次：timeout_exhausted，不应误标成 budget_exhausted（这次循环先达到查询上限）。
- 业务错误只调用一次，也消耗一次总预算。
- Budget(True)、负数、超过 10 或字符串应拒绝。

独立挑战：给 Budget 增加只读 used 属性，返回初始额度减剩余额度，并在每次查询后断言 used 等于 len(calls)。不要用独立的、可能与 remaining 不一致的可写计数器。

限制：这是同步、单进程、可信代码内的教学对象，不具备线程安全、持久化或跨进程预算能力，也不防止调用方恶意修改属性。take 必须位于调用前；扣减后即使超时或失败也不退还。本练只校验返回的 ok，received 不代表完整元数据或业务正确。没有实现真实超时计时、等待、模型 token 预算或金额预算。

验证记录：实际运行共享预算三条路径，并核对四种非法预算、零预算无调用、业务错误消耗额度、连续超时达到查询上限。

请反馈：三条输出、总预算为 0 的结果、used 挑战和用时。尚未完成前练可直接说明卡点，后续不默认提高难度。

来源与关联：本聊天原创教学示例，承接第 15–16 练；能力边界见 [[wiki/concepts/工具]]，流程控制见 [[wiki/concepts/harness工程]]，通信位置见 [[wiki/concepts/MCP]]。未使用外部 SDK/API。


## 第 18 练：为 SQL 助手生成带来源的字段上下文包

日期：2026-11-07。前十七练尚无完成反馈；本练可独立运行，仅需 Python 3 标准库，无模型 API 或集群。
复习入口：第 04 练为什么需要字段白名单？今天把字段的类型、说明与来源一起交给后续 SQL 助手，而不只给字段名。

目标与交付物：schema_context.py，接受表名及字段列表，只输出相关字段的元数据与快照来源；找不到字段时明确报错，不猜业务别名。

### 核心概念（2 分钟）

- **最小相关上下文**：只提供本任务所需字段，可减少无关 schema 干扰；减少字段数不等同于精确控制模型 token 数。
- **来源与快照**：保留来源和日期，帮助日后核对“当时依据哪份元数据”。来源标识不保证信息真实、完整或最新，仍需实际维护。

脚本组装上下文；Skill 可规定先读取元数据再生成草稿；MCP 可提供真实元数据接口；Agent 根据任务选择需要的字段并处理缺失信息。今天没有调用模型或 MCP，不宣称已减少真实模型的幻觉率。关联 [[wiki/concepts/上下文工程]]、[[wiki/concepts/工具]]、[[wiki/concepts/MCP]]。

### 完整最小示例与动手（10 分钟）

文件：[[system/exercises/18-schema-context/schema_context.py|schema_context.py]]。

```python
import json

# 教学快照，金额单位与日期口径仅对本例有效。
CATALOG = {
    "table": "dwd.orders",
    "source": "mock://catalog/orders/v1",
    "snapshot_date": "2026-11-07",
    "columns": {
        "id": {"type": "bigint", "comment": "订单唯一编号"},
        "amount": {"type": "decimal(18,2)", "comment": "订单金额，单位元"},
        "dt": {"type": "string", "comment": "分区日期，格式 YYYY-MM-DD"},
    },
}


def build_context(table, fields):
    if not isinstance(table, str) or table != CATALOG["table"]:
        raise ValueError("unknown_table")
    if (not isinstance(fields, list) or not fields
            or not all(isinstance(f, str) for f in fields)):
        raise ValueError("invalid_fields")
    if len(set(fields)) != len(fields):
        raise ValueError("duplicate_fields")
    missing = sorted(set(fields) - CATALOG["columns"].keys())
    if missing:
        raise ValueError("unknown_fields: " + ", ".join(missing))
    return {
        "table": table,
        "source": CATALOG["source"],
        "snapshot_date": CATALOG["snapshot_date"],
        "columns": [{"name": field, **CATALOG["columns"][field]}
                    for field in fields],
    }


if __name__ == "__main__":
    context = build_context("dwd.orders", ["amount", "dt"])
    assert [c["name"] for c in context["columns"]] == ["amount", "dt"]
    assert context["source"] == "mock://catalog/orders/v1"
    print(json.dumps(context, ensure_ascii=False, indent=2))
    try:
        build_context("dwd.orders", ["gmv"])
    except ValueError as exc:
        assert str(exc) == "unknown_fields: gmv"
        print("未知字段自测通过；未猜测 gmv 与 amount 的映射")
    else:
        raise AssertionError("未知字段必须失败")

```

1. 阅读 CATALOG，把“元数据事实”与后续“生成指令”分开理解；不要将快照注释当作通用业务口径（3 分钟）。
2. 运行并查看 JSON（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/18-schema-context/schema_context.py
```

预期 JSON（格式缩写）：

```json
{"table":"dwd.orders","source":"mock://catalog/orders/v1","snapshot_date":"2026-11-07","columns":[{"name":"amount","type":"decimal(18,2)","comment":"订单金额，单位元"},{"name":"dt","type":"string","comment":"分区日期，格式 YYYY-MM-DD"}]}
```

随后输出“未知字段自测通过；未猜测 gmv 与 amount 的映射”。mock:// 是模拟来源标识，不是可访问的真实目录服务。

3. 把请求改为 ["id"]，确认上下文不包含 amount/dt；请求 ["gmv"] 时拒绝，不将它自动翻译成金额（4 分钟）。

### 自测（3 分钟）

- amount、dt 请求只返回这两个字段，顺序与请求一致。
- 输出包含 source 与 snapshot_date；无未知字段补写。
- 空列表、重复字段、非字符串字段、未知表或未知字段均抛 ValueError。
- 修改返回的字段说明，不改变 CATALOG 中的原始快照。

独立挑战：为列明确定义 business_aliases，仅允许人工确认的“订单金额”→amount，默认不收录 gmv。先写“已确认别名可解析”及“未知别名必须报错”两条用例，再实现解析；输出保留用户原词和最终字段名，方便追溯。不要依赖字符串相似度自动确认口径。

范围：固定快照与输入字段精确匹配，大小写不自动归一化；不验证快照时效，不读取真实表，不解析 SQL。外部表说明可能包含不可信文字，将它们放进 JSON 不会自动消除提示注入风险，后续流程应把说明当数据而非操作指令。今天只处理可信的模拟说明。

验证记录：正常和未知字段脚本场景通过，另核对五项异常输入以及返回值修改不污染快照。尚未做真实模型效果评测或 MCP 连通验证。

请反馈：单字段上下文、未知字段错误、别名挑战和用时。若前练仍卡住，可只交本练或直接说明卡点，不默认已完成前十七练。

来源与关联：本聊天原创教学示例；上下文组织依据 [[wiki/concepts/上下文工程]]，数仓元数据与别名建设见 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]。未涉及外部 SDK 或变化中的 API。


## 第 19 练：校验 SQL 助手的结构化回答契约

日期：2026-11-08。前十八练仍待完成反馈；本练独立运行，Python 3 标准库即可，无模型 API、集群或额外依赖。
复习入口：第 18 练遇到 gmv 时为什么不直接猜成 amount？今天让助手输出明确的“待补信息”状态，而非把不确定性混在 SQL 草稿里。

目标与交付物：validate_reply.py，校验模拟模型输出的 JSON。只允许 ready 或 needs_info 两种状态，拒绝状态、请求参数与问题列表相互矛盾。

### 核心概念（2 分钟）

- **结构化回答是调用边界**：自然语言模型输出进入工作流之前，先解析和校验契约；一段看起来像 JSON 的文本不等于合法输入。
- **状态相关约束**：needs_info 必须提出问题且不提供可执行请求；ready 必须有完整参数且没有未解决问题。格式合法也不代表模型忠实理解用户需求。

脚本校验输出；Skill 可规定缺参先询问、参数齐全再给候选请求；MCP 提供工具连接；Agent 使用反馈选择下一步。今天只模拟模型回答，没有模型推理或工具执行，不构成真实 Agent。

### 完整最小示例与动手（10 分钟）

文件：[[system/exercises/19-model-output-contract/validate_reply.py|validate_reply.py]]。

```python
import json
from datetime import date
import re


def validate_reply(text):
    data = json.loads(text)
    if not isinstance(data, dict) or set(data) != {"status", "request", "questions"}:
        raise ValueError("回答必须且只能包含 status、request、questions")
    questions = data["questions"]
    if (not isinstance(questions, list)
            or not all(isinstance(q, str) and q.strip() for q in questions)):
        raise ValueError("questions 必须是非空白问题组成的数组")
    if data["status"] == "needs_info":
        if data["request"] is not None or not questions:
            raise ValueError("待补充信息时 request 必须为 null，且至少有一个问题")
        return data
    if data["status"] != "ready" or questions:
        raise ValueError("ready 不得带问题，且不支持其他状态")
    request = data["request"]
    if not isinstance(request, dict) or set(request) != {"table", "fields", "day"}:
        raise ValueError("ready 必须提供 table、fields、day")
    if request["table"] != "dwd.orders":
        raise ValueError("表不在教学白名单")
    fields = request["fields"]
    if (not isinstance(fields, list) or not fields
            or not all(isinstance(f, str) and f in {"id", "amount", "dt"} for f in fields)
            or len(set(fields)) != len(fields)):
        raise ValueError("字段列表无效")
    day = request["day"]
    if not isinstance(day, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", day):
        raise ValueError("日期必须为 YYYY-MM-DD")
    date.fromisoformat(day)
    return data


if __name__ == "__main__":
    ready = {"status": "ready", "request": {
        "table": "dwd.orders", "fields": ["id"], "day": "2026-11-07"
    }, "questions": []}
    missing = {"status": "needs_info", "request": None,
               "questions": ["请提供要查询的分区日期。"]}
    for item in [ready, missing]:
        result = validate_reply(json.dumps(item, ensure_ascii=False))
        print("accepted: " + result["status"])
    contradictory = {**ready, "questions": ["请确认日期。"]}
    try:
        validate_reply(json.dumps(contradictory, ensure_ascii=False))
    except ValueError:
        print("rejected: ready_with_questions")
    else:
        raise AssertionError("矛盾回答必须被拒绝")
    print("3 个回答契约场景通过")

```

1. 阅读 ready 与 missing 两份完整样例，解释 request=null 的作用（3 分钟）。
2. 运行下面命令（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/19-model-output-contract/validate_reply.py
```

预期输出：

```text
accepted: ready
accepted: needs_info
rejected: ready_with_questions
3 个回答契约场景通过
```

3. 构造 needs_info 却没有问题的回答，再构造字段为 unknown 的 ready，分别确认 ValueError；不要把错误回答静默改写成 ready（4 分钟）。

### 自测（3 分钟）

- 合格 ready：保留完整请求，返回原对象，不生成或执行 SQL。
- 合格 needs_info：request=null，问题至少一条；调用者应等待用户回答。
- ready 同时提出问题、needs_info 缺少问题、未知状态都拒绝。
- 额外顶层键、损坏 JSON、未知字段、非法日期均拒绝。

独立挑战：增加顶层 schema_version，要求值严格为整数 1（拒绝 True）。先写旧输出缺版本、新输出版本 1、版本 True 三条用例，再修改契约和两个正常样例；不要只放宽顶层键而遗漏值检查。

使用建议：若给本地助手做手工实验，可要求“缺少信息时输出 needs_info/request=null/questions，齐全时输出 ready/request/questions=[]；只输出 JSON”。但此提示只是实验入口，不保证模型遵守，也不保证用户没给日期时模型不编造。日期来源、用户意图一致性和人工审核仍需独立验证。

范围：只验证教学表与字段白名单、日历日期、状态一致性；不验证数据是否存在、业务口径或参数是否由用户提供。needs_info 中的问题可能无关或误导，仍需行为评测。成功解析绝不直接授权执行 SQL。本练未调用模型，也未使用具体厂商结构化输出 API。

验证记录：三个脚本场景通过，另有六项损坏 JSON、缺失/额外字段、状态矛盾、未知字段及非法日期检查通过。

请反馈：三行输出、你构造的反例、版本挑战和用时。前练仍卡住也可只说明卡点，不默认提高难度。

来源与关联：本聊天原创教学示例，工具契约见 [[wiki/concepts/工具]]，元数据上下文见 [[wiki/concepts/上下文工程]]，行为评测见 [[wiki/concepts/AI评估]]。未涉及变化中的外部 SDK/API。


## 第 20 练：把模型回答交给 SQL 草稿工作流

日期：2026-11-09。前十九练仍待反馈；本练自带全部本地依赖，Python 3 标准库即可。无模型 API、集群或 MCP 安装要求。
复习入口：第 19 练中，一份格式合法的 ready 是否可能包含用户没给过的日期？校验 JSON 形状之后还缺哪项核对？

目标与交付物：handoff.py，连接“回答契约校验→已确认参数核对→草稿工作流”。信息缺失、回答损坏或参数被替换时，不调用工作流。

### 核心概念（2 分钟）

- **格式与意图一致性分开**：日期格式合法，不等于它是用户要求的日期；需要与可信输入另行核对。
- **模型与执行层之间的交接关卡**：模型给出候选请求，程序验证后才调用工具流程。阻断不是仅返回错误文案，还要证明下游未调用。

脚本实现校验与交接，Skill 可规定询问与确认流程，MCP 可连接真实元数据，Agent 可使用这些能力根据反馈决策。今天用人工构造的回答，不是真实模型决策或完整 Agent。

### 完整最小示例与动手（10 分钟）

目录 system/exercises/20-model-to-workflow/ 已包含：

- [[system/exercises/20-model-to-workflow/handoff.py|handoff.py]]：下方完整交接代码与四份样例。
- [[system/exercises/20-model-to-workflow/validate_reply.py|validate_reply.py]]：第 19 练校验函数副本。
- [[system/exercises/20-model-to-workflow/workflow.py|workflow.py]]、[[system/exercises/20-model-to-workflow/catalog.py|catalog.py]]、[[system/exercises/20-model-to-workflow/sql_generator.py|sql_generator.py]]：第 13 练草稿工作流及工具副本。

```python
import json
from validate_reply import validate_reply
from workflow import run


def handoff(reply_text, confirmed_request, workflow=run):
    try:
        reply = validate_reply(reply_text)
    except ValueError:
        return {"status": "stopped", "reason": "invalid_model_reply", "executed": False}
    if reply["status"] == "needs_info":
        return {"status": "ask_user", "questions": reply["questions"], "executed": False}
    if not isinstance(confirmed_request, dict) or reply["request"] != confirmed_request:
        return {"status": "stopped", "reason": "request_mismatch", "executed": False}
    return workflow(reply["request"])


if __name__ == "__main__":
    # 模拟从用户确认界面取得的参数；不能从同一份模型回答生成。
    confirmed = {"table": "dwd.orders", "fields": ["id"], "day": "2026-11-08"}
    ready = {"status": "ready", "request": confirmed.copy(), "questions": []}
    missing = {"status": "needs_info", "request": None,
               "questions": ["请确认查询日期。"]}
    changed = {"status": "ready", "request": {**confirmed, "day": "2026-11-07"},
               "questions": []}
    cases = [
        ("matched", json.dumps(ready), "needs_review", 1),
        ("missing", json.dumps(missing), "ask_user", 0),
        ("changed", json.dumps(changed), "stopped", 0),
        ("broken", "{", "stopped", 0),
    ]
    for name, text, expected, expected_calls in cases:
        calls = []

        def counted_workflow(request):
            calls.append(request)
            return run(request)

        result = handoff(text, confirmed, workflow=counted_workflow)
        assert result["status"] == expected
        assert result["executed"] is False
        assert len(calls) == expected_calls
        if name == "matched":
            assert "2026-11-08" in result["sql"]
        else:
            assert "sql" not in result
        print(f"{name}: {result['status']}; workflow_calls={len(calls)}")
    print("4 个回答交接场景通过；未执行 SQL")

```

1. 阅读 confirmed、ready、changed，指出为什么 changed 虽可通过日期格式校验仍须拒绝（3 分钟）。
2. 运行下面命令核对四条路径（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/20-model-to-workflow/handoff.py
```

预期输出：

```text
matched: needs_review; workflow_calls=1
missing: ask_user; workflow_calls=0
changed: stopped; workflow_calls=0
broken: stopped; workflow_calls=0
4 个回答交接场景通过；未执行 SQL
```

3. 再将 changed 的 fields 改成 ["amount"]，同时保持原日期，验证合法字段的无授权替换仍不调用工作流；不是只防未知字段（4 分钟）。

### 自测（3 分钟）

- 请求与已确认参数完全一致，才进入工作流并产出待审核草稿。
- needs_info 只返回问题，workflow_calls=0。
- 合法但不同的日期或字段：stopped/request_mismatch，workflow_calls=0，无 sql。
- 损坏 JSON：stopped/invalid_model_reply，workflow_calls=0，无 sql。
- 所有结果 executed=false；needs_review 不意味着人工已批准。

独立挑战：新增 missing_confirmation 场景，将 confirmed_request 传为 None；预期 request_mismatch 且工作流调用 0 次。先写断言，再考虑是否把停止原因细分为 confirmation_required；如改契约，需同时更新测试。

范围：confirmed_request 是教学中模拟的可信确认信息，不验证真实身份或 UI 事件；必须来自用户输入/确认渠道，不能直接复制模型候选作为“确认”。本练采用字典精确相等比较，字段顺序改变也会被拒绝，不尝试推断语义等价。真实系统还需记录确认来源与版本；同意查询参数也不等于授权执行 SQL。尚未测试真实模型、MCP 或数据库。

验证记录：四条实际进程场景通过；用工作流计数器确认三类被阻断输入确实没有进入工作流，正常路径生成正确日期的 SQL 草稿。

请反馈：四条输出、合法字段被替换时的结果、缺确认挑战与用时。前练仍卡住可只说明卡点，不默认前十九练已完成。

来源与关联：本聊天原创教学交接，复用第 13、19 练；契约见 [[wiki/concepts/工具]]，阶段边界见 [[wiki/concepts/harness工程]]，行为验证见 [[wiki/concepts/AI评估]]。未使用变化中的 SDK/API。


## 第 21 练：保存并回放模型回答的回归案例

日期：2026-11-10。前二十练尚无完成反馈；本练提供完整本地文件，Python 3 标准库即可。
复习入口：第 19 练拒绝 ready 同时带问题的回答，如何让这个要求在后续修改后仍持续被检查？

目标与交付物：cases.jsonl 保存已知回答和人工预期标签，replay.py 每次修改后回放，按稳定案例 id 输出失败明细。不同于第 12 练内置案例，这次把案例变成独立文件，重点练习新增回归数据与严格读取。

### 核心概念（2 分钟）

- **回归案例是可维护资产**：发现问题后，把最小复现输入、稳定 id 和预期结果保存下来；不要只在聊天里记一句“修好了”。
- **案例损坏不等于回答应拒绝**：外层 JSONL 文件坏了要停止评测；内层 reply 是模型原文，损坏 JSON 可以是合法的“应拒绝”测试输入。

脚本回放案例；Skill 可规定修改后运行哪些案例；MCP 连接实际工具；Agent 或其输出校验层可成为被测对象。今天只测试确定性回答校验器，不重新调用模型，也不证明真实模型会正确回答。

### 完整最小示例与动手（10 分钟）

独立目录 system/exercises/21-regression-fixtures/ 包含：

- [[system/exercises/21-regression-fixtures/cases.jsonl|cases.jsonl]]：以下完整样例，每行一个案例；reply 是 JSON 字符串中的模型原文。
- [[system/exercises/21-regression-fixtures/validate_reply.py|validate_reply.py]]：第 19 练回答校验器的完整副本。
- [[system/exercises/21-regression-fixtures/replay.py|replay.py]]：下方读取及回放程序。

```jsonl
{"id": "ready_valid", "expected": "accept", "reply": "{\"status\": \"ready\", \"request\": {\"table\": \"dwd.orders\", \"fields\": [\"id\"], \"day\": \"2026-11-09\"}, \"questions\": []}"}
{"id": "missing_valid", "expected": "accept", "reply": "{\"status\": \"needs_info\", \"request\": null, \"questions\": [\"请提供日期。\"]}"}
{"id": "ready_with_question", "expected": "reject", "reply": "{\"status\": \"ready\", \"request\": {\"table\": \"dwd.orders\", \"fields\": [\"id\"], \"day\": \"2026-11-09\"}, \"questions\": [\"日期是哪天？\"]}"}
{"id": "broken_json", "expected": "reject", "reply": "{"}
```

```python
import json
from pathlib import Path
from validate_reply import validate_reply


def load_cases(path):
    cases, seen = [], set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except ValueError as exc:
            raise ValueError(f"案例文件第 {line_number} 行不是合法 JSON") from exc
        if not isinstance(case, dict) or set(case) != {"id", "expected", "reply"}:
            raise ValueError(f"第 {line_number} 行案例字段错误")
        key = case["id"]
        if not isinstance(key, str) or not key.strip() or key in seen:
            raise ValueError(f"第 {line_number} 行案例 id 无效或重复")
        if case["expected"] not in ("accept", "reject") or not isinstance(case["reply"], str):
            raise ValueError(f"第 {line_number} 行标签或 reply 类型错误")
        seen.add(key)
        cases.append(case)
    if not cases:
        raise ValueError("案例文件为空")
    return cases


def replay(cases):
    failures = []
    for case in cases:
        try:
            validate_reply(case["reply"])
            actual = "accept"
        except ValueError:
            actual = "reject"
        if actual != case["expected"]:
            failures.append({"id": case["id"], "expected": case["expected"], "actual": actual})
    return {"total": len(cases), "passed": len(cases) - len(failures), "failures": failures}


if __name__ == "__main__":
    cases = load_cases(Path(__file__).with_name("cases.jsonl"))
    report = replay(cases)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if report["failures"] else 0)

```

1. 读案例文件，区分外层案例 JSON 与内层 reply 字符串；解释 broken_json 为什么不是案例文件损坏（3 分钟）。
2. 运行下面命令（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/21-regression-fixtures/replay.py
```

预期输出（格式缩写）：

```json
{"total":4,"passed":4,"failures":[]}
```

退出码 0。文件路径相对脚本解析，不依赖终端当前目录。

3. 将今天练习目录内的校验函数临时改成“任何输入都返回 {}”，运行回放，应只通过 2/4，ready_with_question 和 broken_json 失败，退出 1；最后恢复原函数再确认 4/4（4 分钟）。请先保存副本便于恢复，不修改第 19 练原文件，也不改 expected 来迎合错误实现。

### 自测（3 分钟）

- 正常案例文件与原校验器：4/4，退出 0。
- 校验器不再拒绝错误回答：2/4，失败报告能定位两个稳定 id，退出 1。
- 重复 id、空案例集或外层 JSON 损坏：评测程序失败，不输出“全部通过”。
- 内层 reply 为损坏 JSON 且 expected=reject：该项应通过，不中断其他案例。

独立挑战：添加 invalid_calendar_day 案例，ready 中日期为 2026-02-30、questions=[]，预期 reject。原校验器应 5/5；总是接受的错误校验器应 2/5。建议用 Python json.dumps 构造 reply 字符串，减少手工转义错误。

范围：这是一组教学回归案例，不是有统计代表性的模型能力评测。修改 prompt 但不重新采集模型回答时，本程序只能验证保存的旧回答是否被校验器正确接受/拒绝；要评估新提示词效果，需另外调用模型并核对新结果，不能声称本回放已测到。没有读取或保存真实业务数据。

验证记录：原校验器实际回放 4/4；临时错误校验器 2/4 并退出 1；重复 id 文件被拒绝。交付文件保持原校验器与四项案例。

请反馈：原始报告、错误校验器报告、新案例结果和用时。前练仍卡住也可只说明卡点，不默认已完成二十练。

来源与关联：本聊天原创教学示例，行为回归概念见 [[wiki/concepts/AI评估]]，可复现执行与交接见 [[wiki/concepts/harness工程]]。未使用外部 SDK/API。


## 第 22 练：将字段变更映射到下游任务复核清单

日期：2026-11-11。前二十一练尚无完成反馈；本练可独立完成，Python 3 标准库即可。
复习入口：第 01 练能列出字段删除和类型变化，但还不能回答“哪些下游任务需要看一眼”。今天补上最小字段依赖映射。

目标与交付物：impact.py，对比单张模拟表的新旧结构，根据手工声明的任务字段依赖输出复核清单，不解析 SQL，不操作 DataLeap 或真实 Hive 表。

### 核心概念（2 分钟）

- **变更事实与影响判断分开**：结构差异是一层；下游是否引用这些字段是另一层。类型变化一律标为需复核，不直接判为不兼容或必然失败。
- **依赖清单必须可用**：依赖字段不在旧结构时应拒绝分析，不能悄悄输出“无影响”。结果的完整性取决于依赖清单本身是否完整。

脚本计算差异和关联；Skill 可规定变更前生成影响清单；MCP 可未来连接元数据和血缘接口；Agent 可汇总复核事项并寻求决策。今天是确定性分析，不做自主修改或发布。

### 完整最小示例与动手（10 分钟）

文件：[[system/exercises/22-schema-change-impact/impact.py|impact.py]]。

```python
import json


def impact(old, new, jobs):
    for schema in (old, new):
        if not isinstance(schema, dict) or not all(
            isinstance(k, str) and k.strip() and isinstance(v, str) and v.strip()
            for k, v in schema.items()
        ):
            raise ValueError("表结构必须是字段名到非空类型字符串的字典")
    if not isinstance(jobs, list):
        raise ValueError("任务依赖必须是数组")
    changes = {name: "removed" for name in old.keys() - new.keys()}
    changes.update({name: "type_changed" for name in old.keys() & new.keys()
                    if old[name] != new[name]})
    seen, affected = set(), []
    for job in jobs:
        if not isinstance(job, dict) or set(job) != {"name", "fields"}:
            raise ValueError("任务必须包含且仅包含 name、fields")
        name, fields = job["name"], job["fields"]
        if not isinstance(name, str) or not name.strip() or name in seen:
            raise ValueError("任务名称无效或重复")
        seen.add(name)
        if (not isinstance(fields, list) or not fields
                or not all(isinstance(f, str) and f in old for f in fields)
                or len(set(fields)) != len(fields)):
            raise ValueError("依赖字段必须唯一、非空且存在于旧结构")
        hits = [{"field": field, "reason": changes[field]}
                for field in sorted(fields) if field in changes]
        if hits:
            affected.append({"job": name, "review": hits})
    return {"affected": sorted(affected, key=lambda item: item["job"]),
            "unaffected_by_declared_fields": len(jobs) - len(affected)}


if __name__ == "__main__":
    old = {"id": "bigint", "amount": "int", "legacy": "string"}
    new = {"id": "bigint", "amount": "bigint", "channel": "string"}
    jobs = [
        {"name": "daily_amount", "fields": ["id", "amount"]},
        {"name": "old_export", "fields": ["legacy"]},
        {"name": "id_only", "fields": ["id"]},
    ]
    report = impact(old, new, jobs)
    assert [item["job"] for item in report["affected"]] == ["daily_amount", "old_export"]
    assert report["unaffected_by_declared_fields"] == 1
    print(json.dumps(report, ensure_ascii=False, indent=2))

```

1. 看 old/new/jobs，预测 amount 类型变化和 legacy 删除各影响哪个任务（3 分钟）。
2. 运行命令核对报告（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/22-schema-change-impact/impact.py
```

预期输出（格式缩写）：

```json
{"affected":[{"job":"daily_amount","review":[{"field":"amount","reason":"type_changed"}]},{"job":"old_export","review":[{"field":"legacy","reason":"removed"}]}],"unaffected_by_declared_fields":1}
```

3. 在 id_only 中增加 amount 依赖，应变成三个任务需复核；再将依赖改为不存在的 gmv，应抛 ValueError。按新输入调整示例断言后运行，最后恢复（4 分钟）。

### 自测（3 分钟）

- 原样例仅 daily_amount、old_export 需复核，原因可对应到字段。
- 结构完全相同或只有新增字段：已声明普通字段引用没有命中，不报删除/类型变化。
- 未知依赖字段、重复任务名、重复字段和空依赖列表均拒绝。
- id_only 的“未命中”仅表示已声明字段不涉及变更，不等于真实任务一定无影响。

独立挑战：给受影响任务增加 priority：引用被删除字段为 high，仅有类型变化为 review。一个任务同时命中删除和类型变化时优先 high；先写两类和混合场景的预期，再实现。

范围：仅单表、显式字段依赖，精确比较类型字符串；不覆盖 SELECT *、位置相关 INSERT、分区布局、隐式类型转换、业务口径、多跳血缘或动态 SQL。仅新增字段也可能影响 SELECT * 或位置写入，不能据此断言新增一律兼容。依赖清单为可信手工模拟，不自动发现或修复任务。本练不连接真实平台，不需要任务权限。

验证记录：原样例复核项与原因通过；相同结构、仅新增字段未命中检查通过，四项非法依赖清单被拒绝。

请反馈：原始报告、第三个任务新增依赖后的结果、优先级挑战和用时。前练仍卡住可直接说明，不默认已完成二十一练。

来源与关联：本聊天原创教学示例；工具契约见 [[wiki/concepts/工具]]，数仓元数据要求见 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]，工程阶段边界见 [[wiki/concepts/harness工程]]。未使用变化中的外部 SDK/API。


## 第 23 练：检查指定日期分区是否就绪

日期：2026-11-12。前二十二练尚无完成反馈；本练独立运行，仅需 Python 3 标准库。
复习入口：第 13 练生成了带 dt 条件的 SQL，为什么参数合法仍不能证明目标分区有数据？

目标与交付物：partition_check.py，读取模拟单表分区清单，对指定日期输出状态和下一步；只在目标分区 ready 时建议继续。

### 核心概念（2 分钟）

- **检查具体依赖，不看最大日期猜测**：11 月 10 日已就绪，不代表 11 月 9 日没有缺口；必须按请求的目标分区精确匹配。
- **存在与就绪分开**：存在但运行中或失败的分区不应继续；清单本身损坏也不能伪装成“分区缺失”。

脚本实现检查规则；Skill 可规定提交查询前核对分区；MCP 可连接只读分区元数据服务；Agent 可根据结果说明等待或请求复核。今天只输出建议，不自动调度、重跑或执行查询。

### 完整最小示例与动手（10 分钟）

文件：[[system/exercises/23-partition-readiness/partition_check.py|partition_check.py]]。

```python
import json
import re
from datetime import date


def validate_day(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise ValueError("分区日期必须为 YYYY-MM-DD")
    date.fromisoformat(value)


def check_partition(target_day, partitions):
    validate_day(target_day)
    if not isinstance(partitions, list):
        raise ValueError("分区清单必须是数组")
    states = {}
    for row in partitions:
        if not isinstance(row, dict) or set(row) != {"dt", "state"}:
            raise ValueError("每项必须包含且仅包含 dt、state")
        dt, state = row["dt"], row["state"]
        validate_day(dt)
        if dt in states:
            raise ValueError("重复分区: " + dt)
        if state not in ("ready", "running", "failed"):
            raise ValueError("未知分区状态")
        states[dt] = state
    state = states.get(target_day, "missing")
    action = {"ready": "continue", "missing": "wait",
              "running": "wait", "failed": "review"}[state]
    return {"target_day": target_day, "state": state, "action": action}


if __name__ == "__main__":
    partitions = [
        {"dt": "2026-11-08", "state": "failed"},
        {"dt": "2026-11-10", "state": "ready"},
        {"dt": "2026-11-11", "state": "running"},
    ]
    cases = [("2026-11-10", "ready", "continue"), ("2026-11-09", "missing", "wait"),
             ("2026-11-11", "running", "wait"), ("2026-11-08", "failed", "review")]
    for day, state, action in cases:
        result = check_partition(day, partitions)
        assert result == {"target_day": day, "state": state, "action": action}
        print(json.dumps(result, ensure_ascii=False))
    print("4 个分区就绪场景通过")

```

1. 阅读清单，先预测 2026-11-09 的结果，解释为什么 11-10 已就绪无关（3 分钟）。
2. 执行命令（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/23-partition-readiness/partition_check.py
```

预期输出（JSON 空白可不同）：

```text
{"target_day":"2026-11-10","state":"ready","action":"continue"}
{"target_day":"2026-11-09","state":"missing","action":"wait"}
{"target_day":"2026-11-11","state":"running","action":"wait"}
{"target_day":"2026-11-08","state":"failed","action":"review"}
4 个分区就绪场景通过
```

3. 在清单增加 11-09 的 ready 记录，调整该场景预期，应从 wait 变为 continue；再添加同一日期的第二条记录，预期 ValueError。最后恢复原示例（4 分钟）。

### 自测（3 分钟）

- 目标 ready 才返回 continue；更新分区 ready 不影响更早缺失分区的结果。
- running → wait，failed → review，空清单 → missing/wait。
- 重复日期、非法日历日期、未知状态、缺失字段、非数组清单应抛 ValueError。
- 清单是完整且成功读取的快照才可将空列表解释为缺失；工具错误或快照不完整应在外层另行处理。

独立挑战：新增 check_required_days(days, partitions)，输入两个依赖日期并返回所有未就绪项；只有两项均 ready 时才允许继续。先写“两天均就绪”“一天缺失”两条断言，再实现；定义空依赖列表如何处理。无需引入等待循环。

范围：只做单表日分区，ready 是模拟上游状态，不是 Hive/Spark 自动提供的完整性证明，也不保证数据质量。真实使用前需明确业务时区、元数据快照来源及就绪信号（例如任务提交成功或业务校验）。没有查询真实平台、调度任务或验证数据库行为。

验证记录：四条正常/异常状态路径通过，另核对五类非法清单和空清单。

请反馈：原始四行结果、补齐 11-09 后的状态、重复分区异常和挑战用时。前练未完成可独立提交本练。

来源与关联：本聊天原创模拟示例，工具契约见 [[wiki/concepts/工具]]，流程控制见 [[wiki/concepts/harness工程]]，数仓元数据背景见 [[wiki/syntheses/企业数仓 Text-to-SQL Agent 落地清单]]。未使用变化中的外部 SDK/API。


## 第 24 练：为已就绪分区增加行数波动检查

日期：2026-11-13。前二十三练尚无完成反馈；本练独立运行，仅需 Python 3 标准库。
复习入口：第 23 练的 ready 只说明上游报告已就绪，为什么还不能证明分区数据量合理？

目标与交付物：volume_check.py，比较同口径的模拟当前行数和参考行数，输出 pass、review 或 insufficient_data；支持可配置的整数百分比阈值。

### 核心概念（2 分钟）

- **就绪与质量分开**：分区可读不代表数量合理；行数波动只提供复核信号，不证明数据正确。
- **缺数据与零值分开**：None 表示缺少统计，0 是实际测得零行；参考行数为零时，相对变化不可计算，不能自动判通过。

脚本判断阈值；Skill 可规定先核对就绪再比行数；MCP 可只读获取统计；Agent 可解释波动并请人复核。本练不自动扫描、修改或重跑真实数仓任务。

### 完整最小示例与动手（10 分钟）

文件：[[system/exercises/24-partition-volume/volume_check.py|volume_check.py]]。

```python
import json


def check_volume(current_rows, baseline_rows, threshold_pct=20):
    if type(threshold_pct) is not int or not 0 <= threshold_pct <= 100:
        raise ValueError("阈值必须是 0–100 的整数百分数")
    for count in (current_rows, baseline_rows):
        if count is not None and (type(count) is not int or count < 0):
            raise ValueError("行数必须是非负整数或 None")
    if current_rows is None or baseline_rows is None:
        return {"status": "insufficient_data", "reason": "missing_count"}
    if baseline_rows == 0:
        return {"status": "insufficient_data", "reason": "zero_baseline"}
    delta = current_rows - baseline_rows
    # abs(delta) / baseline_rows > threshold_pct / 100 的整数比较。
    exceeded = abs(delta) * 100 > baseline_rows * threshold_pct
    return {"status": "review" if exceeded else "pass",
            "delta_rows": delta, "baseline_rows": baseline_rows,
            "threshold_pct": threshold_pct}


if __name__ == "__main__":
    cases = [(1100, 1000, "pass"), (700, 1000, "review"),
             (1200, 1000, "pass"), (None, 1000, "insufficient_data"),
             (100, 0, "insufficient_data")]
    for current, baseline, expected in cases:
        result = check_volume(current, baseline)
        assert result["status"] == expected
        print(json.dumps({"current_rows": current, **result}, ensure_ascii=False))
    print("5 个行数检查场景通过")

```

1. 先预测 1100、700、1200 相对参考 1000 的判断。默认“超过 20%”才复核，恰好 20% 通过（3 分钟）。
2. 运行命令核对报告（3 分钟）：

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/24-partition-volume/volume_check.py
```

预期逐行结果（格式缩写）：

```text
{"current_rows":1100,"status":"pass","delta_rows":100,"baseline_rows":1000,"threshold_pct":20}
{"current_rows":700,"status":"review","delta_rows":-300,"baseline_rows":1000,"threshold_pct":20}
{"current_rows":1200,"status":"pass","delta_rows":200,"baseline_rows":1000,"threshold_pct":20}
{"current_rows":null,"status":"insufficient_data","reason":"missing_count"}
{"current_rows":100,"status":"insufficient_data","reason":"zero_baseline"}
5 个行数检查场景通过
```

3. 将 1200 改为 1201，预期改为 review；将当前行数改为 0，应 review 而非 missing_count；再传 True，应 ValueError。最后恢复示例（4 分钟）。

### 自测（3 分钟）

- 正常波动和阈值边界通过，越界增减均复核。
- None 与实际零行不混淆；参考行数为 0 时输出 zero_baseline。
- 布尔值、字符串、负行数或非法阈值应报错。
- 报告保留基线、实际差值和阈值，便于人工说明原因。

独立挑战：增加两个方向的阈值，上涨最多 30%、下降最多 10%。先写同样变化量的两条用例：1150/1000 通过，850/1000 复核，再实现。保留缺统计和零基线处理。

范围：固定教学规则，不是异常检测模型；真实参考值必须同口径、同分区粒度，节假日/补数等应另行考虑。高于或低于阈值不等于业务错误；pass 只表示行数在本阈值内。没有运行 SELECT COUNT(*) 或访问真实集群，也不把缺失统计当作零。

验证记录：五条脚本场景、零行和越界检查、五类非法输入通过。

请反馈：五行输出、1201 与零行的结果、方向阈值挑战和用时。前练仍卡住可直接说明，不推定已掌握。

来源与关联：本聊天原创教学示例；工程契约见 [[wiki/concepts/工具]]，阶段校验见 [[wiki/concepts/harness工程]]。未使用外部 SDK/API。


## 第 25 练：先核对行数统计口径，再做比较

日期：2026-11-16。前二十四练仍待反馈。本练可独立完成，仅用 Python 3 标准库。复习：第 24 练中 700 对 1000 超过阈值；如果 700 只统计已支付订单，还能据此判断波动吗？

交付物：`check_comparable` 核对模拟 Hive 分区统计的表名、时间粒度、统计范围和指标版本，并返回不匹配项。结果为 `comparable` 时，才交给第 24 练的行数检查器验证行数和阈值。

### 理解（2 分钟）

- **口径与取值分开**：不同日期是比较的目的；不同统计范围或指标版本才会破坏可比性。
- **缺信息与已知不一致分开**：缺字段要补资料；口径不一致要换基线。口径标签一致仍不证明统计可信、行数有效或日期合理。

脚本强制核对，Skill 规定检查顺序，MCP 可读取统计元数据，Agent 可解释差异并请求合理基线。本练没有调用真实工具、模型或集群。关联 [[wiki/concepts/工具]]、[[wiki/concepts/MCP]]。

### 动手（10 分钟）

示例文件：[[system/exercises/25-comparable-metrics/compare_scope.py|compare_scope.py]]。

```python
import json

KEYS = ("table", "grain", "scope", "metric_version")


def check_comparable(current, baseline):
    for label, stats in (("current", current), ("baseline", baseline)):
        if not isinstance(stats, dict):
            return {"status": "invalid_metadata", "side": label}
        missing = [key for key in KEYS
                   if not isinstance(stats.get(key), str) or not stats[key].strip()]
        if missing:
            return {"status": "invalid_metadata", "side": label, "fields": missing}
    differences = [key for key in KEYS if current[key] != baseline[key]]
    if differences:
        return {"status": "incomparable", "fields": differences}
    return {"status": "comparable"}


if __name__ == "__main__":
    baseline = {"table": "dwd.orders", "grain": "daily",
                "scope": "all_orders", "metric_version": "v1",
                "dt": "2026-11-14", "rows": 1000}
    current = {**baseline, "dt": "2026-11-15", "rows": 700}
    cases = [
        (current, {"status": "comparable"}),
        ({**current, "scope": "paid_only"},
         {"status": "incomparable", "fields": ["scope"]}),
        ({**current, "metric_version": None},
         {"status": "invalid_metadata", "side": "current",
          "fields": ["metric_version"]}),
    ]
    for sample, expected in cases:
        result = check_comparable(sample, baseline)
        assert result == expected, result
        print(json.dumps(result))
```

1. 读样例，预测三项状态（3 分钟）。
2. 运行脚本，核对差异字段（3 分钟）。
3. 试将当前粒度改为 weekly、范围改为 paid_only，把预期差异改为 grain 和 scope；再将基线版本设为空白，确认报告指出 baseline（4 分钟）。

```sh
python3 /Users/bytedance/Workspace/Gits/my_obsidian_notes/system/exercises/25-comparable-metrics/compare_scope.py
```

预期：

```text
{"status": "comparable"}
{"status": "incomparable", "fields": ["scope"]}
{"status": "invalid_metadata", "side": "current", "fields": ["metric_version"]}
```

### 自测（3 分钟）

- 只改日期和行数，仍通过口径检查。
- 改统计范围或版本，报告相应字段；同时改两项，报告两项。
- 元数据缺失、为 null 或空白时返回 `invalid_metadata`，不运行行数比较；若两侧都无效，先报当前侧。

独立挑战：给四项都相同的统计加入 `timezone` 必填项。先写三条预期：同为 Asia/Shanghai 则可比较；UTC 与 Asia/Shanghai 不可比较；缺时区则无效。使用明确标签，不自动推断两个时区标签是否等价。

请回报运行结果、两项差异输出、挑战结果和用时。来源：本聊天原创示例，承接本页第 24 练；不涉及变化中的 SDK/API。
