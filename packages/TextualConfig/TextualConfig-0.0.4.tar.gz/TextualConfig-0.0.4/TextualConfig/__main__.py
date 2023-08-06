from . import Config
from rich.markdown import Markdown
from rich.table import Table
from rich import box
from rich.text import Text

mark_up = Text.from_markup
command_table = Table(expand=True, row_styles=["none", "dim"], box=box.SIMPLE)

command_table.add_column(mark_up("[bold]命令[/]", justify="center"), no_wrap=True)
command_table.add_column(mark_up("[bold]描述[/]", justify="center"))

command_table.add_row(mark_up("cup-network [bold magenta]login[/]"), "登录")
command_table.add_row(mark_up("cup-network [bold magenta]logout[/]"), "登出")
command_table.add_row(mark_up("cup-network [bold magenta]reset[/]"), "重置密码")
command_table.add_row(
    mark_up("cup-network [bold magenta]config[bold yellow] <key> \[value][/]"),
    "配置",
)
command_table.add_row(mark_up("cup-network [bold magenta]status[/]"), "状态")

res = Config(
    "config.json",
    Markdown(
        """\
# CUP_Network

利用selenium自动登录和登出CUP的校园网

## 安装

```shell
pip3 install cup-network -U
```

## 使用

获取帮助: `cup-network --help`

### 子命令"""
    ),
    command_table,
    username={
        "type": "Input",
        "args": [],
        "kwargs": {
            "placeholder": "Username",
        },
    },
    password={
        "type": "Input",
        "args": [],
        "kwargs": {
            "placeholder": "Password",
            "password": True,
        },
    },
).run()

print(res)
