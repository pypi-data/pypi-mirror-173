<h1 style="text-align: center"> TextualConfig </h1>

A Config Tool with [Textual](https://github.com/Textualize/textual) support.

## Install

```shell
pip3 install TextualConfig
```

## Usage

```python
from TextualConfig import Config

questions = {
    "username": {
        "type": "Input",
        "args": [],
        "kwargs": {
            "placeholder": "Username",
        },
    },
    "password": {
        "type": "Input",
        "args": [],
        "kwargs": {
            "placeholder": "Password",
            "password": True,
        },
    },
    "_doc1": {
        "type": "Doc",
        "args": *Any_Rich_Renderable # 可用rich渲染的对象列表
    },
    "enable": {
        "type": "Checkbox"
    }
}

res = Config("save.path.json", *Any_Rich_Renderable, **questions)
```

## Demo

```sh
python3 -m TextualConfig
```

|                                      Home                                      |                                      Config                                      |
| :----------------------------------------------------------------------------: | :------------------------------------------------------------------------------: |
| ![Home](https://cos.rhythmlian.cn/ImgBed/1ca0a330f881701b27e4c32b6bb8b7cc.png) | ![Config](https://cos.rhythmlian.cn/ImgBed/55df1073d17d7117b5b56b1b005b34c7.png) |
