from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QComboBox,
    QMessageBox,
    QPushButton,
)
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QCloseEvent

class SettingsDialog(QDialog):
    def __init__(self, api_key, api_domain, ai_tone, system_language, ai_model, answer_language, ai_gender, ai_age, auto_copy, parent=None):
        super().__init__(parent)

        self.language_combo = QComboBox()
        self.setWindowTitle(self.get_text("设置"))

        # 布局
        layout = QVBoxLayout(self)

        # 系统语言
        layout.addWidget(QLabel(self.get_text("系统语言")))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "简体中文", "繁體中文"])
        self.language_combo.setCurrentText(system_language)
        layout.addWidget(self.language_combo)

        # 回答语言
        layout.addWidget(QLabel(self.get_text("回答语言")))
        self.answer_language_combo = QComboBox()
        self.answer_language_combo.addItems(["English", "简体中文", "繁體中文"])
        self.answer_language_combo.setCurrentText(answer_language)
        layout.addWidget(self.answer_language_combo)

        # API Key
        api_key_layout = QHBoxLayout()
        self.api_key_label = QLabel(self.get_text("API 密钥:"))
        api_key_layout.addWidget(self.api_key_label)
        self.api_key_input = QLineEdit(api_key)
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_key_layout.addWidget(self.api_key_input)
        self.api_key_hide_button = QPushButton(self.get_text("隐藏"))
        self.api_key_hide_button.setFlat(True)
        self.api_key_hide_button.clicked.connect(self.toggle_api_key_visibility)
        api_key_layout.addWidget(self.api_key_hide_button)
        self.api_key_show_button = QPushButton(self.get_text("显示"))
        self.api_key_show_button.setFlat(True)
        self.api_key_show_button.clicked.connect(self.toggle_api_key_visibility)
        self.api_key_show_button.hide()
        api_key_layout.addWidget(self.api_key_show_button)
        layout.addLayout(api_key_layout)

        # API Domain
        self.api_domain_label = QLabel(self.get_text("API 域名:"))
        layout.addWidget(self.api_domain_label)
        self.api_domain_input = QLineEdit(api_domain)
        layout.addWidget(self.api_domain_input)

         # AI Model
        self.ai_model_label = QLabel(self.get_text("AI 模型:"))
        layout.addWidget(self.ai_model_label)
        self.ai_model_input = QLineEdit(ai_model)
        layout.addWidget(self.ai_model_input)

        # AI Tone
        ai_tone_group = QGroupBox(self.get_text("AI 语气"))
        ai_tone_layout = QHBoxLayout(ai_tone_group)
        self.aggressive_radio = QRadioButton(self.get_text("激进"))
        self.neutral_radio = QRadioButton(self.get_text("中立"))
        self.submissive_radio = QRadioButton(self.get_text("顺从"))
        if ai_tone == "激进":
            self.aggressive_radio.setChecked(True)
        elif ai_tone == "中立":
            self.neutral_radio.setChecked(True)
        else:
            self.submissive_radio.setChecked(True)
        ai_tone_layout.addWidget(self.aggressive_radio)
        ai_tone_layout.addWidget(self.neutral_radio)
        ai_tone_layout.addWidget(self.submissive_radio)
        layout.addWidget(ai_tone_group)

        # AI Gender
        ai_gender_group = QGroupBox(self.get_text("AI 性别"))
        ai_gender_layout = QHBoxLayout(ai_gender_group)
        self.male_radio = QRadioButton(self.get_text("男"))
        self.female_radio = QRadioButton(self.get_text("女"))
        self.martian_radio = QRadioButton(self.get_text("火星人"))
        if ai_gender == "男":
            self.male_radio.setChecked(True)
        elif ai_gender == "女":
            self.female_radio.setChecked(True)
        else:
            self.martian_radio.setChecked(True)
        ai_gender_layout.addWidget(self.male_radio)
        ai_gender_layout.addWidget(self.female_radio)
        ai_gender_layout.addWidget(self.martian_radio)
        layout.addWidget(ai_gender_group)

        # AI Age
        self.ai_age_label = QLabel(self.get_text("AI 年龄:"))
        layout.addWidget(self.ai_age_label)
        self.ai_age_input = QLineEdit(ai_age)
        self.ai_age_input.setPlaceholderText(self.get_text("可选"))
        layout.addWidget(self.ai_age_input)

        # Auto Copy
        auto_copy_group = QGroupBox(self.get_text("自动复制"))
        auto_copy_layout = QHBoxLayout(auto_copy_group)
        self.auto_copy_yes_radio = QRadioButton(self.get_text("是"))
        self.auto_copy_no_radio = QRadioButton(self.get_text("否"))
        if auto_copy == "是":
            self.auto_copy_yes_radio.setChecked(True)
        else:
            self.auto_copy_no_radio.setChecked(True)
        auto_copy_layout.addWidget(self.auto_copy_yes_radio)
        auto_copy_layout.addWidget(self.auto_copy_no_radio)
        layout.addWidget(auto_copy_group)

        # 按钮
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
            | QDialogButtonBox.StandardButton.Ok
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self.apply_settings
        )
        layout.addWidget(self.button_box)

        # 设置初始语言
        self.update_labels(system_language)

        # 添加关闭事件
        self.close_flag = False
        self.rejected.connect(self.on_close)

    def toggle_api_key_visibility(self):
        if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.api_key_hide_button.hide()
            self.api_key_show_button.show()
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.api_key_show_button.hide()
            self.api_key_hide_button.show()

    def on_close(self):
        if not self.close_flag:
            self.show_close_message()

    def closeEvent(self, event: QCloseEvent):
        self.on_close()
        if self.close_flag:
          event.accept()
        else:
          event.ignore()

    def show_close_message(self):
      if not self.aggressive_radio.isChecked() and not self.neutral_radio.isChecked() and not self.submissive_radio.isChecked():
        msg_box = QMessageBox()
        msg_box.setWindowTitle(self.get_text("设置未应用"))
        msg_box.setText(self.get_text("请先选择一个AI语气"))
        msg_box.setIcon(QMessageBox.Icon.Warning)

        confirm_button = QPushButton(self.get_text("确认"))
        msg_box.addButton(confirm_button, QMessageBox.ButtonRole.AcceptRole)

        msg_box.exec()
        if not self.aggressive_radio.isChecked() and not self.neutral_radio.isChecked() and not self.submissive_radio.isChecked():
          self.show_close_message()
      else:
        self.close_flag = True

    def update_labels(self, language):
        if language == "English":
            self.api_key_label.setText("API Key:")
            self.api_domain_label.setText("API Domain:")
            self.ai_model_label.setText("AI Model:")
            self.ai_age_label.setText("AI Age:")
        elif language == "简体中文":
            self.api_key_label.setText("API 密钥:")
            self.api_domain_label.setText("API 域名:")
            self.ai_model_label.setText("AI 模型:")
            self.ai_age_label.setText("AI 年龄:")
        elif language == "繁體中文":
            self.api_key_label.setText("API 密鑰:")
            self.api_domain_label.setText("API 網域:")
            self.ai_model_label.setText("AI 模型:")
            self.ai_age_label.setText("AI 年齡:")

        self.setWindowTitle(self.get_text("设置"))
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText(self.get_text("Cancel"))
        self.button_box.button(QDialogButtonBox.StandardButton.Apply).setText(self.get_text("Apply"))
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText(self.get_text("OK"))

        ai_tone_group = self.findChild(QGroupBox)
        ai_tone_group.setTitle(self.get_text("AI 语气"))

        ai_gender_group = self.findChildren(QGroupBox)[1]
        ai_gender_group.setTitle(self.get_text("AI 性别"))

        auto_copy_group = self.findChildren(QGroupBox)[2]
        auto_copy_group.setTitle(self.get_text("自动复制"))

        self.aggressive_radio.setText(self.get_text("激进"))
        self.neutral_radio.setText(self.get_text("中立"))
        self.submissive_radio.setText(self.get_text("顺从"))

        self.male_radio.setText(self.get_text("男"))
        self.female_radio.setText(self.get_text("女"))
        self.martian_radio.setText(self.get_text("火星人")) # 新增火星人选项

        self.auto_copy_yes_radio.setText(self.get_text("是"))
        self.auto_copy_no_radio.setText(self.get_text("否"))

        self.findChild(QLabel).setText(self.get_text("系统语言"))
        self.findChildren(QLabel)[1].setText(self.get_text("回答语言"))

    def apply_settings(self):
        # 隐藏取消按钮
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).hide()
        print("设置已应用 (但未关闭对话框)")

    def exec(self):
        # 在 exec 前立即显示窗口
        self.show()
        self.update_labels(self.language_combo.currentText())
        return super().exec()

    def get_text(self, key):
      translations = {
            "English": {
                "设置": "Settings",
                "API 密钥": "API Key",
                "API 域名": "API Domain",
                "AI 语气": "AI Tone",
                 "激进": "Aggressive",
                "中立": "Neutral",
                "顺从": "Submissive",
                "语言:": "Language:",
                "设置未应用": "Settings not applied",
                "请先选择一个AI语气": "Please select an AI tone first",
                "确认": "Confirm",
                "Cancel": "Cancel",
                "Apply": "Apply",
                "OK": "OK",
                "AI 模型": "AI Model",
                "系统语言": "System Language",
                "回答语言": "Answer Language",
                 "请使用{language}回答，并且只给出一个结果：":"Please respond in {language} and provide only one result:",
                 "回答中...":"Answering...",
                 "重新回答":"Re-answer",
                "隐藏": "Hide",
                "显示": "Show",
                "男": "Male",
                "女": "Female",
                "火星人": "Martian",
                "AI 性别": "AI Gender",
                "AI 年龄": "AI Age",
                "自动复制": "Auto Copy",
                "是": "Yes",
                "否": "No",
                "可选": "Optional",
                "作者的话": "Author's Note"
            },
            "简体中文": {
                "设置": "设置",
                "API 密钥": "API 密钥",
                "API 域名": "API 域名",
                 "AI 语气": "AI 语气",
                "激进": "激进",
                "中立": "中立",
                "顺从": "顺从",
                 "语言:": "语言:",
                 "设置未应用": "设置未应用",
                "请先选择一个AI语气": "请先选择一个AI语气",
                 "确认": "确认",
                 "Cancel": "取消",
                "Apply": "应用",
                "OK": "确定",
                 "AI 模型": "AI 模型",
                "系统语言": "系统语言",
                "回答语言": "回答语言",
                 "请使用{language}回答，并且只给出一个结果：": "请使用{language}回答，并且只给出一个结果：",
                   "回答中...": "回答中...",
                    "重新回答": "重新回答",
                     "隐藏": "隐藏",
                 "显示": "显示",
                 "男": "男",
                 "女": "女",
                 "火星人": "火星人",
                 "AI 性别": "AI 性别",
                 "AI 年龄": "AI 年龄",
                 "自动复制": "自动复制",
                 "是": "是",
                 "否": "否",
                 "可选": "可选",
                 "作者的话": "作者的话"
            },
            "繁體中文": {
                "设置": "設定",
                "API 密钥": "API 密鑰",
                "API 域名": "API 網域",
                "AI 语气": "AI 語氣",
                "激进": "激進",
                "中立": "中立",
                "顺从": "順從",
                 "语言:": "語言:",
                 "设置未应用": "設定未應用",
                 "请先选择一个AI语气": "請先選擇一個AI語氣",
                 "确认": "確認",
                "Cancel": "取消",
                "Apply": "應用",
                "OK": "確定",
                "AI 模型": "AI 模型",
                "系统语言": "系統語言",
                "回答语言": "回答語言",
                 "请使用{language}回答，并且只给出一个结果：": "請使用{language}回答，並且只給出一個結果：",
                   "回答中...": "回答中...",
                   "重新回答": "重新回答",
                   "隐藏": "隱藏",
                   "显示": "顯示",
                   "男": "男",
                   "女": "女",
                   "火星人": "火星人",
                   "AI 性别": "AI 性別",
                   "AI 年龄": "AI 年齡",
                   "自动复制": "自動複製",
                   "是": "是",
                   "否": "否",
                   "可选": "可選",
                   "作者的话": "作者的話"
            },
        }
      return translations.get(self.language_combo.currentText(), {}).get(key, key)
