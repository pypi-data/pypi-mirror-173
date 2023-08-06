from matplotlib.widgets import Button
from .__dependence__ import *
from rich.markdown import Markdown
from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Container


class AboveFold(Container):
    pass


class Section(Container):
    pass


class SectionTitle(Static):
    pass


class Column(Container):
    pass


class TextContent(Static):
    pass


class Body(Container):
    pass


class Title(Static):
    pass


class QuickAccess(Container):
    pass


class LocationLink(Static):
    def __init__(self, label: str, reveal: str) -> None:
        super().__init__(label)
        self.reveal = reveal

    def on_click(self) -> None:
        self.app.query_one(self.reveal).scroll_visible(top=True)


class Welcome(Container):
    def __init__(self, doc):
        super().__init__()
        self.doc = doc

    def compose(self) -> ComposeResult:
        for item in self.doc:
            yield Static(item)
        yield Button("Start" if user_lang != "zh" else "开始", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.query_one(".config").scroll_visible(speed=50, top=True)


class ConfigForm(Container):
    def __init__(self, questions, path):
        super().__init__()
        self.questions = questions
        self.path = path
        self.widgets = {}
        self.answers = {}

    def compose(self) -> ComposeResult:
        for question in self.questions:
            _question = self.questions[question]
            if _question["type"] == "Doc":
                for item in _question["args"]:
                    yield Static(item)
            else:
                yield Static(question, classes="label")
                widget = requirePackage("textual.widgets", _question["type"], "textual")
                self.widgets[question] = widget(
                    *_question["args"], **_question["kwargs"]
                )
                yield self.widgets[question]
        yield Static()
        yield Button("Save" if user_lang != "zh" else "保存", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # self.app.query_one(".config").scroll_visible(speed=50, top=True)
        self.answers = {i: self.widgets[i].value for i in self.widgets}
        with open(self.path, "w") as f:
            import json

            json.dump(self.answers, f, indent=4, ensure_ascii=False)
        self.app.exit()


class Config(App):
    CSS_PATH = "demo.css"
    BINDINGS = [
        Binding("q", "app.quit", "quit", show=True),
    ]

    def __init__(self, path, *home_page, **kwargs):
        super().__init__()
        self.path = path
        self.doc = home_page
        self.questions = kwargs

    def compose(self) -> ComposeResult:
        yield Container(
            Header(show_clock=True),
            Body(
                QuickAccess(
                    LocationLink("Home" if user_lang != "zh" else "首页", ".welcome"),
                    LocationLink("Config" if user_lang != "zh" else "配置", ".config"),
                ),
                AboveFold(Welcome(self.doc), classes="welcome"),
                Column(
                    Section(
                        SectionTitle("Config" if user_lang != "zh" else "配置"),
                        ConfigForm(self.questions, self.path),
                    ),
                    classes="config",
                ),
            ),
        )
        yield Footer()

    def action_open_link(self, link: str) -> None:
        self.app.bell()
        import webbrowser

        webbrowser.open(link)
