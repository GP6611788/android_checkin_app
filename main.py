"""
广西水利电力职业技术学院 - 智能查寝签到 Android App
基于KivyMD Material Design
作者：龟龟 (为您服务的AI助手)
"""

import threading
import json
from datetime import datetime
from functools import partial

import requests
from urllib.parse import quote

from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ListProperty, DictProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.selectioncontrol import MDCheckbox

# 导入原始的签到脚本的核心功能
from checkin_core import CheckinBot, aes_encrypt_ecb

# 加载KV文件
Builder.load_string('''
#:import utils kivy.utils

<LoginScreen>:
    name: 'login'
    
    MDFloatLayout:
        canvas.before:
            Color:
                rgba: utils.get_color_from_hex("#1a237e")
            Rectangle:
                pos: self.pos
                size: self.size
        
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            padding: dp(40)
            size_hint: 0.8, 0.8
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            
            MDLabel:
                text: '智能查寝签到'
                font_style: 'H4'
                halign: 'center'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(60)
            
            MDCard:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint: 1, None
                height: dp(320)
                elevation: 8
                radius: [25,]
                
                MDTextField:
                    id: username_field
                    hint_text: '学号/账号'
                    icon_left: 'account'
                    mode: 'rectangle'
                    size_hint_x: 1
                    
                MDTextField:
                    id: password_field
                    hint_text: '密码'
                    icon_left: 'lock'
                    mode: 'rectangle'
                    password: True
                    size_hint_x: 1
                    
                MDRaisedButton:
                    text: '登录'
                    size_hint_x: 1
                    pos_hint: {'center_x': 0.5}
                    on_release: root.login()
                    height: dp(48)
                    
                Widget:
                    size_hint_y: None
                    height: dp(10)
                    
                MDLabel:
                    text: '仅查看模式'
                    theme_text_color: 'Secondary'
                    font_style: 'Body2'
                    size_hint_y: None
                    height: dp(20)
                    
                MDBoxLayout:
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(48)
                    
                    MDCheckbox:
                        id: dry_run_checkbox
                        size_hint: None, None
                        size: dp(40), dp(40)
                        pos_hint: {'center_y': 0.5}
                        
                    MDLabel:
                        text: '仅查看考勤状态，不执行签到'
                        size_hint_y: None
                        height: dp(40)
                        pos_hint: {'center_y': 0.5}
                        theme_text_color: 'Secondary'
                        
                MDLabel:
                    text: '忘记密码请联系学校管理员'
                    theme_text_color: 'Hint'
                    font_style: 'Caption'
                    halign: 'center'
                    size_hint_y: None
                    height: dp(20)

<DashboardScreen>:
    name: 'dashboard'
    
    MDFloatLayout:
        MDBoxLayout:
            orientation: 'vertical'
            spacing: 0
            
            MDTopAppBar:
                title: f"欢迎, {root.username}!"
                right_action_items: [['logout', lambda x: root.logout()]]
                elevation: 4
                md_bg_color: app.theme_cls.primary_color
            
            ScrollView:
                MDList:
                    id: attendance_list
                    padding: dp(10)
                    spacing: dp(10)

<CheckinScreen>:
    name: 'checkin'
    
    MDFloatLayout:
        MDBoxLayout:
            orientation: 'vertical'
            spacing: 0
            
            MDTopAppBar:
                title: '手动签到'
                left_action_items: [['arrow-left', lambda x: root.back_to_dashboard()]]
                elevation: 4
                md_bg_color: app.theme_cls.primary_color
            
            ScrollView:
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(20)
                    padding: dp(20)
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDCard:
                        orientation: 'vertical'
                        padding: dp(15)
                        spacing: dp(10)
                        size_hint: 1, None
                        height: dp(350)
                        
                        MDLabel:
                            text: '选择签到点'
                            font_style: 'H6'
                            size_hint_y: None
                            height: dp(40)
                        
                        MDTextField:
                            id: location_dropdown
                            hint_text: '选择签到点'
                            icon_left: 'map-marker'
                            on_focus: if self.focus: root.open_location_menu()
                            mode: 'rectangle'
                        
                        MDLabel:
                            text: '或手动输入坐标：'
                            font_style: 'Body1'
                            theme_text_color: 'Secondary'
                            size_hint_y: None
                            height: dp(30)
                        
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: dp(10)
                            size_hint_y: None
                            height: dp(60)
                            
                            MDTextField:
                                id: lng_input
                                hint_text: '经度 (如: 103.738)'
                                mode: 'rectangle'
                                input_filter: 'float'
                                
                            MDTextField:
                                id: lat_input
                                hint_text: '纬度 (如: 36.112)'
                                mode: 'rectangle'
                                input_filter: 'float'
                        
                        MDTextField:
                            id: address_input
                            hint_text: '地址描述'
                            icon_left: 'home'
                            mode: 'rectangle'
                        
                        MDRaisedButton:
                            text: '执行签到'
                            size_hint_x: 1
                            pos_hint: {'center_x': 0.5}
                            on_release: root.execute_checkin()
                            height: dp(48)

<HistoryScreen>:
    name: 'history'
    
    MDFloatLayout:
        MDBoxLayout:
            orientation: 'vertical'
            spacing: 0
            
            MDTopAppBar:
                title: '签到历史'
                left_action_items: [['arrow-left', lambda x: app.switch_screen('dashboard')]]
                elevation: 4
                md_bg_color: app.theme_cls.primary_color
            
            ScrollView:
                MDList:
                    id: history_list
                    padding: dp(10)
                    spacing: dp(10)
''')


class LoginScreen(Screen):
    """登录屏幕"""
    def login(self):
        """处理登录"""
        username = self.ids.username_field.text.strip()
        password = self.ids.password_field.text.strip()
        dry_run = self.ids.dry_run_checkbox.active
        
        if not username or not password:
            Snackbar(text="请输入账号和密码").open()
            return
            
        app = MDApp.get_running_app()
        app.username = username
        app.password = password
        app.dry_run = dry_run
        
        # 显示加载
        self.ids.password_field.text = ''
        self.show_progress("正在登录...")
        
        # 异步登录
        threading.Thread(target=self._login_thread, args=(username, password)).start()
    
    def _login_thread(self, username, password):
        """后台登录线程"""
        try:
            bot = CheckinBot(username, password)
            
            # 在UI线程更新进度
            Clock.schedule_once(lambda dt: self.show_progress("正在初始化应用..."), 0)
            
            if bot.login() and bot.init_app():
                Clock.schedule_once(lambda dt: self._login_success(bot), 0)
            else:
                Clock.schedule_once(lambda dt: self._login_failed("登录失败，请检查账号密码"), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._login_failed(f"登录错误: {str(e)}"), 0)
    
    def _login_success(self, bot):
        """登录成功"""
        app = MDApp.get_running_app()
        app.checkin_bot = bot
        
        # 获取考勤信息
        self.show_progress("获取考勤信息...")
        threading.Thread(target=self._get_attendance_info).start()
    
    def _get_attendance_info(self):
        """获取考勤信息"""
        app = MDApp.get_running_app()
        try:
            info = app.checkin_bot.get_kq_info()
            Clock.schedule_once(lambda dt: self._show_dashboard(info), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._login_failed(f"获取信息失败: {str(e)}"), 0)
    
    def _show_dashboard(self, info):
        """显示主面板"""
        app = MDApp.get_running_app()
        app.attendance_info = info
        app.switch_screen('dashboard')
        
    def _login_failed(self, message):
        """登录失败"""
        self.hide_progress()
        Snackbar(text=message).open()
    
    def show_progress(self, message):
        """显示进度对话框"""
        app = MDApp.get_running_app()
        if not hasattr(app, 'progress_dialog') or not app.progress_dialog:
            app.progress_dialog = MDDialog(
                title="请稍候",
                text=message,
                auto_dismiss=False
            )
        else:
            app.progress_dialog.text = message
        
        app.progress_dialog.open()
    
    def hide_progress(self):
        """隐藏进度对话框"""
        app = MDApp.get_running_app()
        if hasattr(app, 'progress_dialog') and app.progress_dialog:
            app.progress_dialog.dismiss()


class DashboardScreen(Screen):
    """主面板屏幕"""
    username = StringProperty('')
    
    def on_pre_enter(self, *args):
        """进入屏幕前加载数据"""
        if hasattr(self, '_data_loaded') and self._data_loaded:
            return
            
        app = MDApp.get_running_app()
        self.username = app.username
        
        if hasattr(app, 'attendance_info'):
            self.display_attendance_info(app.attendance_info)
            self._data_loaded = True
    
    def display_attendance_info(self, info):
        """显示考勤信息"""
        self.ids.attendance_list.clear_widgets()
        
        if not info:
            self.ids.attendance_list.add_widget(
                MDLabel(text="无考勤信息", halign='center')
            )
            return
        
        # 添加考勤状态卡片
        card = MDCard(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(250)
        )
        
        config = info.get('CONFIG_INFO', {})
        qd_info = info.get('QD_INFO', {})
        
        # 考勤日期
        date_label = MDLabel(
            text=f"考勤日期: {config.get('KQRQ', '未知')}",
            font_style='H6',
            size_hint_y=None,
            height=dp(30)
        )
        card.add_widget(date_label)
        
        # 考勤状态
        status_text = "✅ 需要签到" if config.get('IN_DATE') else "❌ 非考勤日"
        status_color = (0, 0.7, 0, 1) if config.get('IN_DATE') else (0.8, 0, 0, 1)
        
        status_label = MDLabel(
            text=status_text,
            theme_text_color='Custom',
            text_color=status_color,
            size_hint_y=None,
            height=dp(25)
        )
        card.add_widget(status_label)
        
        # 是否在时间段内
        time_status = "✅ 在签到时间段内" if config.get('IN_TIME') else "⚠️ 不在签到时间段内"
        time_label = MDLabel(
            text=time_status,
            size_hint_y=None,
            height=dp(25)
        )
        card.add_widget(time_label)
        
        # 是否已签到
        signed_status = "✅ 已签到" if qd_info.get('hasQd') else "❌ 未签到"
        signed_label = MDLabel(
            text=signed_status,
            size_hint_y=None,
            height=dp(25)
        )
        card.add_widget(signed_label)
        
        # 签到地点数量
        dd_list = info.get('DD_LIST', [])
        locations_label = MDLabel(
            text=f"可用签到点: {len(dd_list)}个",
            size_hint_y=None,
            height=dp(25)
        )
        card.add_widget(locations_label)
        
        self.ids.attendance_list.add_widget(card)
        
        # 添加操作按钮
        action_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(200)
        )
        
        # 刷新按钮
        refresh_btn = MDRaisedButton(
            text="刷新考勤信息",
            size_hint_x=1,
            on_release=self.refresh_info
        )
        action_layout.add_widget(refresh_btn)
        
        # 手动签到按钮
        manual_btn = MDRaisedButton(
            text="手动签到",
            size_hint_x=1,
            on_release=self.manual_checkin
        )
        action_layout.add_widget(manual_btn)
        
        # 查看历史按钮
        history_btn = MDFlatButton(
            text="查看签到历史",
            size_hint_x=1,
            on_release=self.show_history
        )
        action_layout.add_widget(history_btn)
        
        # 自动签到按钮（仅非dry_run模式）
        app = MDApp.get_running_app()
        if not app.dry_run:
            auto_btn = MDRaisedButton(
                text="自动签到",
                size_hint_x=1,
                md_bg_color=(0.2, 0.6, 0.9, 1),
                on_release=self.auto_checkin
            )
            action_layout.add_widget(auto_btn)
        
        self.ids.attendance_list.add_widget(action_layout)
    
    def refresh_info(self, *args):
        """刷新考勤信息"""
        app = MDApp.get_running_app()
        threading.Thread(target=self._refresh_thread).start()
    
    def _refresh_thread(self):
        """后台刷新线程"""
        app = MDApp.get_running_app()
        try:
            info = app.checkin_bot.get_kq_info()
            Clock.schedule_once(lambda dt: self.display_attendance_info(info), 0)
            Snackbar(text="信息已刷新").open()
        except Exception as e:
            Snackbar(text=f"刷新失败: {str(e)}").open()
    
    def manual_checkin(self, *args):
        """跳转到手动签到屏幕"""
        app = MDApp.get_running_app()
        app.switch_screen('checkin')
    
    def show_history(self, *args):
        """查看签到历史"""
        app = MDApp.get_running_app()
        app.switch_screen('history')
    
    def auto_checkin(self, *args):
        """自动签到（使用默认签到点）"""
        app = MDApp.get_running_app()
        
        if app.dry_run:
            Snackbar(text="仅查看模式，无法签到").open()
            return
        
        # 执行自动签到线程
        threading.Thread(target=self._auto_checkin_thread).start()
    
    def _auto_checkin_thread(self):
        """后台自动签到线程"""
        app = MDApp.get_running_app()
        try:
            result = app.checkin_bot.do_checkin()
            if result.get('success'):
                Snackbar(text="自动签到成功").open()
                # 刷新信息
                Clock.schedule_once(lambda dt: self.refresh_info(), 1)
            else:
                Snackbar(text=f"自动签到失败: {result.get('msg')}").open()
        except Exception as e:
            Snackbar(text=f"自动签到错误: {str(e)}").open()
    
    def logout(self, *args):
        """退出登录"""
        app = MDApp.get_running_app()
        app.reset_app()
        app.switch_screen('login')


class CheckinScreen(Screen):
    """手动签到屏幕"""
    def on_pre_enter(self, *args):
        """进入屏幕前加载签到点"""
        app = MDApp.get_running_app()
        if hasattr(app, 'attendance_info'):
            dd_list = app.attendance_info.get('DD_LIST', [])
            self.locations = dd_list
    
    def open_location_menu(self):
        """打开签到点选择菜单"""
        if not hasattr(self, 'locations') or not self.locations:
            return
        
        menu_items = []
        for i, location in enumerate(self.locations):
            text = f"{i+1}. {location.get('QDDD', f'签到点{i+1}')}"
            menu_items.append({
                "text": text,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.select_location(x)
            })
        
        self.location_menu = MDDropdownMenu(
            caller=self.ids.location_dropdown,
            items=menu_items,
            width_mult=4
        )
        self.location_menu.open()
    
    def select_location(self, index):
        """选择签到点"""
        location = self.locations[index]
        self.ids.location_dropdown.text = location.get('QDDD', f'签到点{index+1}')
        self.ids.lng_input.text = str(location.get('JDZB', 0))
        self.ids.lat_input.text = str(location.get('WDZB', 0))
        self.location_menu.dismiss()
    
    def execute_checkin(self):
        """执行手动签到"""
        # 获取坐标
        lng_text = self.ids.lng_input.text.strip()
        lat_text = self.ids.lat_input.text.strip()
        address = self.ids.address_input.text.strip()
        
        # 验证输入
        if not lng_text or not lat_text:
            Snackbar(text="请输入坐标").open()
            return
        
        try:
            lng = float(lng_text)
            lat = float(lat_text)
        except ValueError:
            Snackbar(text="坐标格式错误").open()
            return
        
        if not address:
            address = f"手动坐标({lng},{lat})"
        
        app = MDApp.get_running_app()
        
        if app.dry_run:
            Snackbar(text="仅查看模式，无法签到").open()
            return
        
        # 显示加载
        self.show_progress("正在签到...")
        
        # 后台执行签到
        threading.Thread(
            target=self._checkin_thread,
            args=(lng, lat, address)
        ).start()
    
    def _checkin_thread(self, lng, lat, address):
        """后台签到线程"""
        app = MDApp.get_running_app()
        try:
            result = app.checkin_bot.do_checkin(
                longitude=lng,
                latitude=lat,
                address=address
            )
            
            if result.get('success'):
                Clock.schedule_once(lambda dt: self._checkin_success(), 0)
            else:
                Clock.schedule_once(lambda dt: self._checkin_failed(result.get('msg')), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._checkin_failed(str(e)), 0)
    
    def _checkin_success(self):
        """签到成功"""
        self.hide_progress()
        Snackbar(text="签到成功！").open()
        # 返回主面板
        Clock.schedule_once(lambda dt: self.back_to_dashboard(), 2)
    
    def _checkin_failed(self, message):
        """签到失败"""
        self.hide_progress()
        Snackbar(text=f"签到失败: {message}").open()
    
    def back_to_dashboard(self):
        """返回主面板"""
        app = MDApp.get_running_app()
        app.switch_screen('dashboard')
    
    def show_progress(self, message):
        """显示进度对话框"""
        app = MDApp.get_running_app()
        app.progress_dialog = MDDialog(
            title="请稍候",
            text=message,
            auto_dismiss=False
        )
        app.progress_dialog.open()
    
    def hide_progress(self):
        """隐藏进度对话框"""
        app = MDApp.get_running_app()
        if hasattr(app, 'progress_dialog') and app.progress_dialog:
            app.progress_dialog.dismiss()


class HistoryScreen(Screen):
    """历史记录屏幕"""
    def on_pre_enter(self, *args):
        """进入屏幕前加载历史记录"""
        threading.Thread(target=self._load_history).start()
    
    def _load_history(self):
        """后台加载历史记录"""
        app = MDApp.get_running_app()
        try:
            history = app.checkin_bot.get_history(limit=10)
            Clock.schedule_once(lambda dt: self._display_history(history), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: Snackbar(text=f"加载历史失败: {str(e)}").open(), 0)
    
    def _display_history(self, history):
        """显示历史记录"""
        self.ids.history_list.clear_widgets()
        
        if not history:
            self.ids.history_list.add_widget(
                MDLabel(text="暂无签到记录", halign='center')
            )
            return
        
        for i, record in enumerate(history):
            if isinstance(record, dict):
                date = record.get('KQRQ', record.get('CZSJ', '未知时间'))
                status = record.get('CQZT', record.get('KQWZXX', '未知状态'))
                
                item = TwoLineListItem(
                    text=f"记录 {i+1}",
                    secondary_text=f"{date} - {status}"
                )
                self.ids.history_list.add_widget(item)


class CheckinApp(MDApp):
    """主应用程序"""
    
    def build(self):
        """构建应用"""
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"
        
        # 初始化属性
        self.username = ''
        self.password = ''
        self.dry_run = True
        self.checkin_bot = None
        self.attendance_info = None
        
        # 创建屏幕管理器
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        self.sm.add_widget(CheckinScreen(name='checkin'))
        self.sm.add_widget(HistoryScreen(name='history'))
        
        return self.sm
    
    def switch_screen(self, screen_name):
        """切换屏幕"""
        self.sm.current = screen_name
    
    def reset_app(self):
        """重置应用状态"""
        self.username = ''
        self.password = ''
        self.dry_run = True
        self.checkin_bot = None
        self.attendance_info = None
        
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.dismiss()
            self.progress_dialog = None


if __name__ == '__main__':
    CheckinApp().run()