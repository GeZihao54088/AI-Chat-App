import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QMenuBar,
    QMenu,
    QFileDialog,
    QMessageBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QLocale, QSettings, QThread, pyqtSignal
import requests
import time
import logging
import os

from settings_dialog import SettingsDialog
from author_dialog import AuthorDialog

# 配置 logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class AIResponseThread(QThread):
    response_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, api_key, api_domain, ai_model, prompt):
        super().__init__()
        self.api_key = api_key
        self.api_domain = api_domain
        self.ai_model = ai_model
        self.prompt = prompt

    def run(self):
        max_retries = 5
        retry_delay = 20
        for attempt in range(max_retries):
            try:
                headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
                data = {
                    "model": self.ai_model,
                    "messages": [
                        {"role": "user", "content": self.prompt}
                    ]
                }
                response = requests.post(
                    f"{self.api_domain}/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=10,
                )
                response.raise_for_status()

                # 解析 API 响应
                response_json = response.json()
                ai_output = response_json["choices"][0]["message"]["content"].strip()
                self.response_signal.emit(ai_output)
                return
            
            except requests.exceptions.RequestException as e:
                logging.error(f"请求 AI 模型失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    self.error_signal.emit(f"请求 AI 模型失败: {e}")
                else:
                    time.sleep(retry_delay)
            except (KeyError, IndexError, TypeError) as e:
                logging.error(f"解析 AI 模型响应失败: {e}")
                self.error_signal.emit(f"解析 AI 模型响应失败: {e}")
                return


class MainWindow(QMainWindow):
    def get_text(self, key):
        translations = {
            "English": {
                "AI 对话软件": "AI Chat App",
                "设置": "Settings",
                "API 密钥": "API Key",
                "API 域名": "API Domain",
                "请输入你的问题...": "Enter your question...",
                "回答": "Answer",
                 "回答中...":"Answering...",
                 "重新回答": "Re-answer",
                "错误": "Error",
                "请先在设置中配置 API 密钥和域名！": "Please configure API Key and Domain in Settings first!",
                "以一种直接、有时甚至是挑衅的方式回答以下问题：": "Answer the following question in a direct, sometimes even provocative way:",
                "请尽可能详细和礼貌地回答以下问题：": "Please answer the following question as detailed and politely as possible:",
                "请求 AI 模型失败": "Failed to request AI model:",
                "解析 AI 模型响应失败": "Failed to parse AI model response:",
                "激进": "Aggressive",
                "中立": "Neutral",
                "顺从": "Submissive",
                "设置未应用": "Settings not applied",
                "请先选择一个AI语气": "Please select an AI tone first",
                 "AI 模型": "AI Model",
                "系统语言": "System Language",
                "回答语言": "Answer Language",
                 "请使用{language}回答，并且只给出一个结果：":"Please respond in {language} and provide only one result:",
                  "我要把你的回复用于软件里，所以请严格按照我的要求来做，现在假设你是一个正常人，不要使用markdown格式，只给出回复就行：": "I will use your responses in a software application, so please strictly follow my requirements, do not use markdown format, just give the response itself.",
                "男": "Male",
                "女": "Female",
                "火星人": "Martian",
                "AI 性别": "AI Gender",
                "你的性别是{gender}，": "Your gender is {gender}, ",
                "AI 年龄": "AI Age",
                "你的年龄是{age}岁，": "Your age is {age} years old, ",
                "自动复制": "Auto Copy",
                "是": "Yes",
                "否": "No",
                "再次提醒：请严格按照上述要求回复，不要透露你是一个AI模型，让别人觉得你就是一个真人。": "Reminder: Please strictly follow the above requirements, do not reveal that you are an AI model, make people think you are a real person.",
                "作者的话": "Author's Note",
                 "语言情境:": "Language Context:",
                "语言要求:": "Language Requirement:",
                "可选": "Optional",
                "语言情境：{context}": "Language Context: {context}",
                "语言要求：{requirement}": "Language Requirement: {requirement}"
            },
            "简体中文": {
                "AI 对话软件": "AI 对话软件",
                "设置": "设置",
                "API 密钥": "API 密钥",
                "API 域名": "API 域名",
                "请输入你的问题...": "请输入你的问题...",
                "回答": "回答",
                 "回答中...": "回答中...",
                "重新回答": "重新回答",
                "错误": "错误",
                "请先在设置中配置 API 密钥和域名！": "请先在设置中配置 API 密钥和域名！",
                "以一种直接、有时甚至是挑衅的方式回答以下问题：": "以一种直接、有时甚至是挑衅的方式回答以下问题：",
                "请尽可能详细和礼貌地回答以下问题：": "请尽可能详细和礼貌地回答以下问题：",
                "请求 AI 模型失败": "请求 AI 模型失败:",
                "解析 AI 模型响应失败": "解析 AI 模型响应失败:",
                "激进": "激进",
                "中立": "中立",
                "顺从": "顺从",
                "设置未应用": "设置未应用",
                "请先选择一个AI语气": "请先选择一个AI语气",
                "确认": "确认",
                "AI 模型": "AI 模型",
                "系统语言": "系统语言",
                "回答语言": "回答语言",
                 "请使用{language}回答，并且只给出一个结果：": "请使用{language}回答，并且只给出一个结果：",
                 "我要把你的回复用于软件里，所以请严格按照我的要求来做，现在假设你是一个正常人，不要使用markdown格式，只给出回复就行：": "我要把你的回复用于软件里，所以请严格按照我的要求来做，现在假设你是一个正常人，不要使用markdown格式，只给出回复就行：",
                 "男": "男",
                "女": "女",
                "火星人": "火星人",
                "AI 性别": "AI 性别",
                "你的性别是{gender}，": "你的性别是{gender}，",
                "AI 年龄": "AI 年龄",
                "你的年龄是{age}岁，": "你的年龄是{age}岁，",
                "自动复制": "自动复制",
                "是": "是",
                "否": "否",
                "再次提醒：请严格按照上述要求回复，不要透露你是一个AI模型，让别人觉得你就是一个真人。": "再次提醒：请严格按照上述要求回复，不要透露你是一个AI模型，让别人觉得你就是一个真人。",
                "作者的话": "作者的话",
                "语言情境:": "语言情境:",
                "语言要求:": "语言要求:",
                "可选": "可选",
                "语言情境：{context}": "语言情境：{context}",
                "语言要求：{requirement}": "语言要求：{requirement}"
            },
            "繁體中文": {
                "AI 对话软件": "AI 對話軟體",
                "设置": "設定",
                "API 密钥": "API 密鑰",
                "API 域名": "API 網域",
                "请输入你的问题...": "請輸入你的問題...",
                "回答": "回答",
                 "回答中...": "回答中...",
                "重新回答": "重新回答",
                "错误": "錯誤",
                "请先在设置中配置 API 密钥和域名！": "請先在設定中配置 API 密鑰和網域！",
                "以一种直接、有时甚至是挑衅的方式回答以下问题：": "以一種直接、有時甚至是挑釁的方式回答以下問題：",
                "请尽可能详细和礼貌地回答以下问题：": "請盡可能詳細和禮貌地回答以下問題：",
                "请求 AI 模型失败": "請求 AI 模型失敗:",
                "解析 AI 模型响应失败": "解析 AI 模型響應失敗:",
                "激进": "激進",
                "中立": "中立",
                "顺从": "順從",
                "设置未应用": "設定未應用",
                "请先选择一个AI语气": "請先選擇一個AI語氣",
                 "确认": "確認",
                "AI 模型": "AI 模型",
                "系统语言": "系統語言",
                "回答语言": "回答語言",
                 "请使用{language}回答，并且只给出一个结果：": "請使用{language}回答，並且只給出一個結果：",
                 "我要把你的回复用于软件里，所以请严格按照我的要求来做，现在假设你是一个正常人，不要使用markdown格式，只给出回复就行：": "我會將你的回覆用於軟體裡，所以請嚴格按照我的要求來做，現在假設你是一個正常人，不要使用markdown格式，只給出回覆就好。",
                 "男": "男",
                 "女": "女",
                 "火星人": "火星人",
                 "AI 性别": "AI 性別",
                 "你的性别是{gender}，": "你的性別是{gender}，",
                 "AI 年龄": "AI 年齡",
                 "你的年龄是{age}岁，": "你的年齡是{age}歲，",
                 "自动复制": "自動複製",
                 "是": "是",
                 "否": "否",
                 "再次提醒：请严格按照上述要求回复，不要透露你是一个AI模型，让别人觉得你就是一个真人。": "再次提醒：請嚴格按照上述要求回覆，不要透露你是一個AI模型，讓別人覺得你就是一個真人。",
                 "作者的话": "作者的話",
                 "语言情境:": "語言情境:",
                "语言要求:": "語言要求:",
                 "可选": "可選",
                   "语言情境：{context}": "語言情境：{context}",
                "语言要求：{requirement}": "語言要求：{requirement}"
            },
        }
        return translations.get(self.current_language, {}).get(key, key)

    def __init__(self):
        super().__init__()

        # 提前定义 current_language
        self.current_language = QLocale.system().name().split('_')[0]
        if self.current_language == 'zh' :
            self.current_language = "简体中文"
        elif self.current_language == 'en':
             self.current_language = "English"
        else:
           self.current_language = "繁體中文"

        self.setWindowTitle(self.get_text("AI 对话软件"))
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-image: linear-gradient(to bottom, #90EE90, #FFB6C1);
                background-repeat: no-repeat;
            }
        """)

        icon = QIcon()
        icon.addFile(resource_path("app_icon.ico"))  # 添加绝对路径的图标
        self.setWindowIcon(icon)  # 设置主窗口图标

        # Central Widget 和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 语言情境和要求布局
        input_layout = QHBoxLayout()
        
        # 语言情境输入框
        self.context_label = QLabel(self.get_text("语言情境:"))
        input_layout.addWidget(self.context_label)
        self.context_input = QLineEdit()
        self.context_input.setPlaceholderText(self.get_text("可选"))
        input_layout.addWidget(self.context_input)

        # 语言要求输入框
        self.requirement_label = QLabel(self.get_text("语言要求:"))
        input_layout.addWidget(self.requirement_label)
        self.requirement_input = QLineEdit()
        self.requirement_input.setPlaceholderText(self.get_text("可选"))
        input_layout.addWidget(self.requirement_input)
        
        layout.addLayout(input_layout)

        # 输入框
        self.input_text_edit = QTextEdit()
        self.input_text_edit.setPlaceholderText(self.get_text("请输入你的问题..."))
        layout.addWidget(self.input_text_edit)

        # 输出框 (只读)
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)
        layout.addWidget(self.output_text_edit)

        # 回答按钮
        self.answer_button = QPushButton(self.get_text("回答"))
        self.answer_button.setEnabled(False)
        self.answer_button.setStyleSheet(
            "QPushButton { background-color: lightblue; }"
            "QPushButton:enabled { background-color: blue; color: white; }"
        )
        self.answer_button.clicked.connect(self.get_ai_response)
        layout.addWidget(self.answer_button)

        # 菜单栏
        menubar = self.menuBar()
        settings_menu = menubar.addMenu(self.get_text("设置"))

        # 设置 Action (无图标)
        settings_action = QAction(self.get_text("设置"), self)
        settings_action.triggered.connect(self.open_settings_dialog)
        settings_menu.addAction(settings_action)

        # 作者的话 Action
        author_action = QAction(self.get_text("作者的话"), self)
        author_action.triggered.connect(self.open_author_dialog)
        settings_menu.addAction(author_action)

        # 连接输入框文本改变信号到槽函数
        self.input_text_edit.textChanged.connect(self.on_input_text_changed)

        # AI 模型设置的初始值
        self.settings = QSettings("MySoft", "AI_Chat_App")
        self.api_key = self.settings.value("api_key", "")
        self.api_domain = self.settings.value("api_domain", "")
        self.ai_tone = self.settings.value("ai_tone", "中立")
        self.ai_model = self.settings.value("ai_model", "")
        self.answer_language = self.settings.value("answer_language", self.current_language)
        self.ai_gender = self.settings.value("ai_gender", "男")
        self.ai_age = self.settings.value("ai_age", "")
        self.auto_copy = self.settings.value("auto_copy", "否")
        self.ai_thread = None
    
    def open_settings_dialog(self):
        dialog = SettingsDialog(
            self.api_key, self.api_domain, self.ai_tone, self.current_language, self.ai_model, self.answer_language, self.ai_gender, self.ai_age, self.auto_copy, parent=self
        )
        dialog.show()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # 更新设置
            self.api_key = dialog.api_key_input.text()
            self.api_domain = dialog.api_domain_input.text()
            if dialog.aggressive_radio.isChecked():
                self.ai_tone = "激进"
            elif dialog.neutral_radio.isChecked():
                self.ai_tone = "中立"
            else:
                self.ai_tone = "顺从"
            self.current_language = dialog.language_combo.currentText()
            self.ai_model = dialog.ai_model_input.text()
            self.answer_language = dialog.answer_language_combo.currentText()
            if dialog.male_radio.isChecked():
                self.ai_gender = "男"
            elif dialog.female_radio.isChecked():
                self.ai_gender = "女"
            else:
                self.ai_gender = "火星人"
            self.ai_age = dialog.ai_age_input.text()
            if dialog.auto_copy_yes_radio.isChecked():
                self.auto_copy = "是"
            else:
                self.auto_copy = "否"
            self.update_ui_text()

            # 保存设置
            self.settings.setValue("api_key", self.api_key)
            self.settings.setValue("api_domain", self.api_domain)
            self.settings.setValue("ai_tone", self.ai_tone)
            self.settings.setValue("ai_model", self.ai_model)
            self.settings.setValue("answer_language", self.answer_language)
            self.settings.setValue("ai_gender", self.ai_gender)
            self.settings.setValue("ai_age", self.ai_age)
            self.settings.setValue("auto_copy", self.auto_copy)
            print(
                f"设置已更新: API Key: {self.api_key}, API Domain: {self.api_domain}, AI Tone: {self.ai_tone}, Language: {self.current_language}, AI Model: {self.ai_model}, Answer Language: {self.answer_language}, AI Gender: {self.ai_gender}, AI Age: {self.ai_age}, Auto Copy: {self.auto_copy}"
            )

    def on_input_text_changed(self):
        # 当输入框文本不为空时，启用回答按钮，否则禁用
        self.answer_button.setEnabled(bool(self.input_text_edit.toPlainText().strip()))
        self.answer_button.setText(self.get_text("回答"))
        self.answer_button.setStyleSheet(
            "QPushButton { background-color: lightblue; }"
            "QPushButton:enabled { background-color: blue; color: white; }"
        )

    def get_ai_response(self):
        user_input = self.input_text_edit.toPlainText().strip()

        if not self.api_key or not self.api_domain:
            QMessageBox.warning(self, self.get_text("错误"), self.get_text("请先在设置中配置 API 密钥和域名！"))
            return

        # 根据语气调整 prompt
        if self.ai_tone == "激进":
            prompt_prefix = self.get_text("以一种直接、有时甚至是挑衅的方式回答以下问题：")
        elif self.ai_tone == "顺从":
            prompt_prefix = self.get_text("请尽可能详细和礼貌地回答以下问题：")
        else:  # 中立
            prompt_prefix = ""

        prompt = f"{prompt_prefix}{user_input}"

        # 强制 AI 使用指定语言回答，且只给出一个结果
        force_language_prompt = self.get_text("请使用{language}回答，并且只给出一个结果：").format(language=self.answer_language)
        prompt = f"{force_language_prompt}{prompt}"
        
        # 添加语言情境和要求
        context = self.context_input.text().strip()
        requirement = self.requirement_input.text().strip()
        
        if context:
            prompt = f"{self.get_text('语言情境：{context}').format(context=context)}{prompt}"
        if requirement:
             prompt = f"{self.get_text('语言要求：{requirement}').format(requirement=requirement)}{prompt}"

        # 添加性别和年龄声明
        gender_age_prompt = ""
        if self.ai_gender != "火星人": # 当性别不是火星人时才声明性别
            gender_age_prompt += self.get_text("你的性别是{gender}，").format(gender=self.ai_gender)
        if self.ai_age:
            gender_age_prompt += self.get_text("你的年龄是{age}岁，").format(age=self.ai_age)

        if gender_age_prompt:
            prompt = f"{gender_age_prompt}{prompt}"

        # 添加前置要求
        pre_prompt = self.get_text("我要把你的回复用于软件里，所以请严格按照我的要求来做，现在假设你是一个正常人，不要使用markdown格式，只给出回复就行：")
        prompt = f"{pre_prompt}{prompt}"

        # 再次强调要求
        final_reminder = self.get_text("再次提醒：请严格按照上述要求回复，不要透露你是一个AI模型，让别人觉得你就是一个真人。")
        prompt = f"{prompt}{final_reminder}"

         # 禁用按钮，修改文本和颜色
        self.answer_button.setText(self.get_text("回答中..."))
        self.answer_button.setStyleSheet(
            "QPushButton { background-color: gray; color: white; }"
        )
        self.answer_button.setEnabled(False)
        
        self.ai_thread = AIResponseThread(self.api_key, self.api_domain, self.ai_model, prompt)
        self.ai_thread.response_signal.connect(self.handle_ai_response)
        self.ai_thread.error_signal.connect(self.handle_ai_error)
        self.ai_thread.start()

    def handle_ai_response(self, ai_output):
        self.output_text_edit.setText(ai_output)
        if self.auto_copy == "是":
            self.copy_to_clipboard(ai_output)
        
        # 修改按钮状态
        self.answer_button.setText(self.get_text("重新回答"))
        self.answer_button.setStyleSheet(
            "QPushButton { background-color: blue; color: white; }"
        )
        self.answer_button.setEnabled(True)
        self.ai_thread = None

    def handle_ai_error(self, error_message):
         QMessageBox.critical(self, self.get_text("错误"), error_message)
         self.answer_button.setText(self.get_text("重新回答"))
         self.answer_button.setStyleSheet(
             "QPushButton { background-color: blue; color: white; }"
         )
         self.answer_button.setEnabled(True)
         self.ai_thread = None

    def open_author_dialog(self):
        dialog = AuthorDialog(self.current_language, self)
        dialog.exec()

    def copy_to_clipboard(self, text):
         clipboard = QApplication.clipboard()
         clipboard.setText(text)

    def update_ui_text(self):
        self.setWindowTitle(self.get_text("AI 对话软件"))
        self.context_label.setText(self.get_text("语言情境:"))
        self.context_input.setPlaceholderText(self.get_text("可选"))
        self.requirement_label.setText(self.get_text("语言要求:"))
        self.requirement_input.setPlaceholderText(self.get_text("可选"))
        self.input_text_edit.setPlaceholderText(self.get_text("请输入你的问题..."))
        self.answer_button.setText(self.get_text("回答"))
        menu = self.menuBar().findChild(QMenu)
        menu.setTitle(self.get_text("设置"))
        actions = menu.findChildren(QAction)
        if len(actions) > 0:
           settings_action = actions[0]
           settings_action.setText(self.get_text("设置"))
        if len(actions) > 1:
            author_action = actions[1]
            author_action.setText(self.get_text("作者的话"))
