from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton
)

class AuthorDialog(QDialog):
    def __init__(self, language, parent=None):
        super().__init__(parent)

        self.language = language
        self.setWindowTitle(self.get_text("作者的话"))

        layout = QVBoxLayout(self)

        # 作者的话内容
        author_label = QLabel(self.get_text("本软件由 gzh 精心打造。最初，它的诞生源于作者想与一位名叫 wanan 的朋友“友好”互动，为了更方便地“交流”而开发的。"))
        author_label.setWordWrap(True)  # 允许自动换行
        layout.addWidget(author_label)

        # 关闭按钮
        close_button = QPushButton(self.get_text("关闭"))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

    def get_text(self, key):
        translations = {
            "English": {
                "作者的话": "Author's Note",
                "本软件由 gzh 精心打造。最初，它的诞生源于作者想与一位名叫 wanan 的朋友“友好”互动，为了更方便地“交流”而开发的。": "This software was meticulously crafted by gzh. Initially, it was born out of the author's desire to have \"friendly\" interactions with a friend named wanan, and developed to facilitate the \"communication\".",
                "关闭": "Close"
            },
            "简体中文": {
                "作者的话": "作者的话",
                "本软件由 gzh 精心打造。最初，它的诞生源于作者想与一位名叫 wanan 的朋友“友好”互动，为了更方便地“交流”而开发的。": "本软件由 gzh 精心打造。最初，它的诞生源于作者想与一位名叫 wanan 的朋友“友好”互动，为了更方便地“交流”而开发的。",
                "关闭": "关闭"
            },
            "繁體中文": {
                "作者的话": "作者的話",
                "本软件由 gzh 精心打造。最初，它的诞生源于作者想与一位名叫 wanan 的朋友“友好”互动，为了更方便地“交流”而开发的。": "本軟體由 gzh 精心打造。最初，它的誕生源於作者想與一位名叫 wanan 的朋友“友好”互動，為了更方便地“交流”而開發的。",
                "关闭": "關閉"
            },
        }
        return translations.get(self.language, {}).get(key, key)
