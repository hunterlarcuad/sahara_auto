import os # noqa
import sys # noqa
import argparse
import random
import time
import copy
import pdb # noqa
import shutil
import math
import re
from datetime import datetime

from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from DrissionPage._elements.none_element import NoneElement
# from DrissionPage.common import Keys
# from DrissionPage import Chromium
# from DrissionPage.common import Actions
# from DrissionPage.common import Settings

from fun_utils import ding_msg
from fun_utils import get_date
from fun_utils import load_file
from fun_utils import save2file
from fun_utils import format_ts
# from fun_utils import time_difference
from fun_utils import extract_numbers

from conf import DEF_LOCAL_PORT
from conf import DEF_INCOGNITO
from conf import DEF_USE_HEADLESS
from conf import DEF_DEBUG
from conf import DEF_PATH_USER_DATA
from conf import DEF_NUM_TRY
from conf import DEF_DING_TOKEN
from conf import DEF_PATH_BROWSER
from conf import DEF_PATH_DATA_STATUS
from conf import DEF_HEADER_STATUS
from conf import DEF_OKX_EXTENSION_PATH
from conf import EXTENSION_ID_OKX
from conf import DEF_PWD

from conf import DEF_PATH_DATA_PURSE
from conf import DEF_HEADER_PURSE

from conf import TZ_OFFSET
from conf import DEL_PROFILE_DIR

from conf import logger

"""
2025.02.08
https://legends.saharalabs.ai
"""

# Wallet balance
DEF_INSUFFICIENT = -1
DEF_SUCCESS = 0
DEF_FAIL = 1


class SaharaTask():
    def __init__(self) -> None:
        self.args = None
        self.page = None
        self.s_today = get_date(is_utc=True)
        self.file_proxy = None

        self.n_points_spin = -1
        self.n_points = -1
        self.n_referrals = -1
        self.n_completed = -1

        # 是否有更新
        self.is_update = False

        # 账号执行情况
        self.dic_status = {}

        self.dic_purse = {}

        self.purse_load()

    def set_args(self, args):
        self.args = args
        self.is_update = False

        self.n_points_spin = -1
        self.n_points = -1
        self.n_referrals = -1
        self.n_completed = -1

    def __del__(self):
        self.status_save()

    def purse_load(self):
        self.file_purse = f'{DEF_PATH_DATA_PURSE}/purse.csv'
        self.dic_purse = load_file(
            file_in=self.file_purse,
            idx_key=0,
            header=DEF_HEADER_PURSE
        )

    def status_load(self):
        self.file_status = f'{DEF_PATH_DATA_STATUS}/status.csv'
        self.dic_status = load_file(
            file_in=self.file_status,
            idx_key=0,
            header=DEF_HEADER_STATUS
        )

    def status_save(self):
        self.file_status = f'{DEF_PATH_DATA_STATUS}/status.csv'
        save2file(
            file_ot=self.file_status,
            dic_status=self.dic_status,
            idx_key=0,
            header=DEF_HEADER_STATUS
        )

    def close(self):
        # 在有头浏览器模式 Debug 时，不退出浏览器，用于调试
        if DEF_USE_HEADLESS is False and DEF_DEBUG:
            pass
        else:
            if self.page:
                try:
                    self.page.quit()
                except Exception as e:
                    logger.info(f'[Close] Error: {e}')

    def initChrome(self, s_profile):
        """
        s_profile: 浏览器数据用户目录名称
        """
        # Settings.singleton_tab_obj = True

        profile_path = s_profile

        # 是否设置无痕模式
        if DEF_INCOGNITO:
            co = ChromiumOptions().incognito(True)
        else:
            co = ChromiumOptions()

        # 设置本地启动端口
        co.set_local_port(port=DEF_LOCAL_PORT)
        if len(DEF_PATH_BROWSER) > 0:
            co.set_paths(browser_path=DEF_PATH_BROWSER)

        co.set_argument('--accept-lang', 'en-US')  # 设置语言为英语（美国）
        co.set_argument('--lang', 'en-US')

        # 阻止“自动保存密码”的提示气泡
        co.set_pref('credentials_enable_service', False)

        # 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
        co.set_argument('--hide-crash-restore-bubble')

        # 关闭沙盒模式
        # co.set_argument('--no-sandbox')

        # popups支持的取值
        # 0：允许所有弹窗
        # 1：只允许由用户操作触发的弹窗
        # 2：禁止所有弹窗
        # co.set_pref(arg='profile.default_content_settings.popups', value='0')

        co.set_user_data_path(path=DEF_PATH_USER_DATA)
        co.set_user(user=profile_path)

        # 获取当前工作目录
        current_directory = os.getcwd()

        # 检查目录是否存在
        if os.path.exists(os.path.join(current_directory, DEF_OKX_EXTENSION_PATH)): # noqa
            logger.info(f'okx plugin path: {DEF_OKX_EXTENSION_PATH}')
            co.add_extension(DEF_OKX_EXTENSION_PATH)
        else:
            print("okx plugin directory is not exist. Exit!")
            sys.exit(1)

        # https://drissionpage.cn/ChromiumPage/browser_opt
        co.headless(DEF_USE_HEADLESS)
        co.set_user_agent(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36') # noqa

        try:
            self.page = ChromiumPage(co)
        except Exception as e:
            logger.info(f'Error: {e}')
        finally:
            pass

        self.page.wait.load_start()
        # self.page.wait(2)

        # tab_new = self.page.new_tab()
        # self.page.close_tabs(tab_new, others=True)

        # 浏览器启动时有 okx 弹窗，关掉
        # self.check_start_tabs()

    def logit(self, func_name=None, s_info=None):
        s_text = f'{self.args.s_profile}'
        if func_name:
            s_text += f' [{func_name}]'
        if s_info:
            s_text += f' {s_info}'
        logger.info(s_text)

    def close_popup_tabs(self, s_keep='OKX Web3'):
        # 关闭 OKX 弹窗
        if len(self.page.tab_ids) > 1:
            self.logit('close_popup_tabs', None)
            n_width_max = -1
            for tab_id in self.page.tab_ids:
                n_width_tab = self.page.get_tab(tab_id).rect.size[0]
                if n_width_max < n_width_tab:
                    n_width_max = n_width_tab

            tab_ids = self.page.tab_ids
            n_tabs = len(tab_ids)
            for i in range(n_tabs-1, -1, -1):
                tab_id = tab_ids[i]
                n_width_tab = self.page.get_tab(tab_id).rect.size[0]
                if n_width_tab < n_width_max:
                    s_title = self.page.get_tab(tab_id).title
                    self.logit(None, f'Close tab:{s_title} width={n_width_tab} < {n_width_max}') # noqa
                    self.page.get_tab(tab_id).close()
                    return True
        return False

    def is_exist(self, s_title, s_find, match_type):
        b_ret = False
        if match_type == 'fuzzy':
            if s_title.find(s_find) >= 0:
                b_ret = True
        else:
            if s_title == s_find:
                b_ret = True

        return b_ret

    def check_start_tabs(self, s_keep='新标签页', match_type='fuzzy'):
        """
        关闭多余的标签页
        match_type
            precise 精确匹配
            fuzzy 模糊匹配
        """
        if self.page.tabs_count > 1:
            self.logit('check_start_tabs', None)
            tab_ids = self.page.tab_ids
            n_tabs = len(tab_ids)
            for i in range(n_tabs-1, -1, -1):
                tab_id = tab_ids[i]
                s_title = self.page.get_tab(tab_id).title
                # print(f's_title={s_title}')
                if self.is_exist(s_title, s_keep, match_type):
                    continue
                if len(self.page.tab_ids) == 1:
                    break
                self.logit(None, f'Close tab:{s_title}')
                self.page.get_tab(tab_id).close()
            self.logit(None, f'Keeped tab: {self.page.title}')
            return True
        return False

    def okx_secure_wallet(self):
        # Secure your wallet
        ele_info = self.page.ele('Secure your wallet')
        if not isinstance(ele_info, NoneElement):
            self.logit('okx_secure_wallet', 'Secure your wallet')
            ele_btn = self.page.ele('Password', timeout=2)
            if not isinstance(ele_btn, NoneElement):
                ele_btn.click(by_js=True)
                self.page.wait(1)
                self.logit('okx_secure_wallet', 'Select Password')

                # Next
                ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    ele_btn.click(by_js=True)
                    self.page.wait(1)
                    self.logit('okx_secure_wallet', 'Click Next')
                    return True
        return False

    def okx_set_pwd(self):
        # Set password
        ele_info = self.page.ele('Set password', timeout=2)
        if not isinstance(ele_info, NoneElement):
            self.logit('okx_set_pwd', 'Set Password')
            ele_input = self.page.ele('@@tag()=input@@data-testid=okd-input@@placeholder:Enter', timeout=2) # noqa
            if not isinstance(ele_input, NoneElement):
                self.logit('okx_set_pwd', 'Input Password')
                self.page.actions.move_to(ele_input).click().type(DEF_PWD)
            self.page.wait(1)
            ele_input = self.page.ele('@@tag()=input@@data-testid=okd-input@@placeholder:Re-enter', timeout=2) # noqa
            if not isinstance(ele_input, NoneElement):
                self.page.actions.move_to(ele_input).click().type(DEF_PWD)
                self.logit('okx_set_pwd', 'Re-enter Password')
            self.page.wait(1)
            ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button@@text():Confirm', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                ele_btn.click(by_js=True)
                self.logit('okx_set_pwd', 'Password Confirmed [OK]')
                return True
        return False

    def okx_bulk_import_private_key(self, s_key):
        ele_btn = self.page.ele('@@tag()=div@@class:_typography@@text():Bulk import private key', timeout=2) # noqa
        if not isinstance(ele_btn, NoneElement):
            ele_btn.click(by_js=True)
            self.logit('okx_bulk_import_private_key', 'Click ...')

            self.page = self.page.get_tab(self.page.latest_tab.tab_id)

            ele_btn = self.page.ele('@@tag()=i@@id=okdDialogCloseBtn', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                self.logit(None, 'Close pwd input box ...')
                ele_btn.click(by_js=True)

            ele_btn = self.page.ele('@@tag()=div@@data-testid=okd-select-reference-value-box', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                self.logit(None, 'Select network ...')
                ele_btn.click(by_js=True)

            ele_btn = self.page.ele('@@tag()=div@@class:_typography@@text()=EVM networks', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                self.logit(None, 'Click EVM networks ...')
                ele_btn.click(by_js=True)

            ele_input = self.page.ele('@@tag()=textarea@@id:pk-input@@placeholder:private', timeout=2) # noqa
            if not isinstance(ele_input, NoneElement):
                self.logit(None, 'Click EVM networks ...')
                self.page.actions.move_to(ele_input).click().type(s_key) # noqa
                self.page.wait(5)

    def init_okx(self, is_bulk=False):
        """
        chrome-extension://jiofmdifioeejeilfkpegipdjiopiekl/popup/index.html
        """
        # self.check_start_tabs()
        s_url = f'chrome-extension://{EXTENSION_ID_OKX}/home.html'
        self.page.get(s_url)
        # self.page.wait.load_start()
        self.page.wait(3)
        self.close_popup_tabs()
        self.check_start_tabs('OKX Wallet', 'precise')

        self.logit('init_okx', f'tabs_count={self.page.tabs_count}')

        self.save_screenshot(name='okx_1.jpg')

        ele_info = self.page.ele('@@tag()=div@@class:balance', timeout=2) # noqa
        if not isinstance(ele_info, NoneElement):
            s_info = ele_info.text
            self.logit('init_okx', f'Account balance: {s_info}') # noqa
            return True

        ele_btn = self.page.ele('Import wallet', timeout=2)
        if not isinstance(ele_btn, NoneElement):
            # Import wallet
            self.logit('init_okx', 'Import wallet ...')
            ele_btn.click(by_js=True)

            self.page.wait(1)
            ele_btn = self.page.ele('Seed phrase or private key', timeout=2)
            if not isinstance(ele_btn, NoneElement):
                # Import wallet
                self.logit('init_okx', 'Select Seed phrase or private key ...') # noqa
                ele_btn.click(by_js=True)
                self.page.wait(1)

                s_key = self.dic_purse[self.args.s_profile][1]
                if len(s_key.split()) == 1:
                    # Private key
                    self.logit('init_okx', 'Import By Private key')
                    ele_btn = self.page.ele('Private key', timeout=2)
                    if not isinstance(ele_btn, NoneElement):
                        # 点击 Private key Button
                        self.logit('init_okx', 'Select Private key')
                        ele_btn.click(by_js=True)
                        self.page.wait(1)
                        ele_input = self.page.ele('@class:okui-input-input input-textarea ta', timeout=2) # noqa
                        if not isinstance(ele_input, NoneElement):
                            # 使用动作，输入完 Confirm 按钮才会变成可点击状态
                            self.page.actions.move_to(ele_input).click().type(s_key) # noqa
                            self.page.wait(5)
                            self.logit('init_okx', 'Input Private key')
                    is_bulk = True
                    if is_bulk:
                        self.okx_bulk_import_private_key(s_key)
                else:
                    # Seed phrase
                    self.logit('init_okx', 'Import By Seed phrase')
                    words = s_key.split()

                    # 输入助记词需要最大化窗口，否则最后几个单词可能无法输入
                    self.page.set.window.max()

                    ele_inputs = self.page.eles('.mnemonic-words-inputs__container__input', timeout=2) # noqa
                    if not isinstance(ele_inputs, NoneElement):
                        self.logit('init_okx', 'Input Seed phrase')
                        for i in range(len(ele_inputs)):
                            ele_input = ele_inputs[i]
                            self.page.actions.move_to(ele_input).click().type(words[i]) # noqa
                            self.logit(None, f'Input word [{i+1}/{len(words)}]') # noqa
                            self.page.wait(1)

                # Confirm
                max_wait_sec = 10
                i = 1
                while i < max_wait_sec:
                    ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button@@text():Confirm', timeout=2) # noqa
                    self.logit('init_okx', f'To Confirm ... {i}/{max_wait_sec}') # noqa
                    if not isinstance(ele_btn, NoneElement):
                        if ele_btn.states.is_enabled is False:
                            self.logit(None, 'Confirm Button is_enabled=False')
                        else:
                            if ele_btn.states.is_clickable:
                                ele_btn.click(by_js=True)
                                self.logit('init_okx', 'Confirm Button is clicked') # noqa
                                self.page.wait(1)
                                break
                            else:
                                self.logit(None, 'Confirm Button is_clickable=False') # noqa

                    i += 1
                    self.page.wait(1)
                # 未点击 Confirm
                if i >= max_wait_sec:
                    self.logit('init_okx', 'Confirm Button is not found [ERROR]') # noqa

                # 导入私钥有此选择页面，导入助记词则没有此选择过程
                # Select network and Confirm
                ele_info = self.page.ele('Select network', timeout=2)
                if not isinstance(ele_info, NoneElement):
                    self.logit('init_okx', 'Select network ...')
                    ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button', timeout=2) # noqa
                    if not isinstance(ele_btn, NoneElement):
                        ele_btn.click(by_js=True)
                        self.page.wait(1)
                        self.logit('init_okx', 'Select network finish')

                self.okx_secure_wallet()

                # Set password
                is_success = self.okx_set_pwd()

                # Start your Web3 journey
                self.page.wait(1)
                self.save_screenshot(name='okx_2.jpg')
                ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button@@text():Start', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    ele_btn.click(by_js=True)
                    self.logit('init_okx', 'import wallet success')
                    self.save_screenshot(name='okx_3.jpg')
                    self.page.wait(2)

                if is_success:
                    return True
        else:
            ele_info = self.page.ele('Your portal to Web3', timeout=2)
            if not isinstance(ele_info, NoneElement):
                self.logit('init_okx', 'Input password to unlock ...')
                s_path = '@@tag()=input@@data-testid=okd-input@@placeholder:Enter'
                ele_input = self.page.ele(s_path, timeout=2) # noqa
                if not isinstance(ele_input, NoneElement):
                    self.page.actions.move_to(ele_input).click().type(DEF_PWD)
                    if ele_input.value != DEF_PWD:
                        self.logit('init_okx', '[ERROR] Fail to input passwrod !')
                        self.page.set.window.max()
                        return False

                    self.page.wait(1)
                    ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button@@text():Unlock', timeout=2) # noqa
                    if not isinstance(ele_btn, NoneElement):
                        ele_btn.click(by_js=True)
                        self.page.wait(1)

                        self.logit('init_okx', 'login success')
                        self.save_screenshot(name='okx_2.jpg')

                        return True
            else:
                ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button@@text()=Approve', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    ele_btn.click(by_js=True)
                    self.page.wait(1)
                else:
                    ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button@@text()=Connect', timeout=2) # noqa
                    if not isinstance(ele_btn, NoneElement):
                        ele_btn.click(by_js=True)
                        self.page.wait(1)
                    else:
                        self.logit('init_okx', '[ERROR] What is this ... [quit]')
                        self.page.quit()

        self.logit('init_okx', 'login failed [ERROR]')
        return False

    def save_screenshot(self, name):
        # 对整页截图并保存
        # self.page.set.window.max()
        s_name = f'{self.args.s_profile}_{name}'
        self.page.get_screenshot(path='tmp_img', name=s_name, full_page=True)

    def is_task_complete(self, idx_status, s_profile=None):
        if s_profile is None:
            s_profile = self.args.s_profile

        if s_profile not in self.dic_status:
            return False

        claimed_date = self.dic_status[s_profile][idx_status]
        date_now = format_ts(time.time(), style=1, tz_offset=TZ_OFFSET) # noqa
        if date_now != claimed_date:
            return False
        else:
            return True

    def update_status(self, idx_status, update_ts=None):
        if not update_ts:
            update_ts = time.time()
        update_time = format_ts(update_ts, 2, TZ_OFFSET)

        claim_date = update_time[:10]

        if self.args.s_profile not in self.dic_status:
            self.dic_status[self.args.s_profile] = [
                self.args.s_profile,
                '',
                '',
                '',
                '',
            ]
        if self.dic_status[self.args.s_profile][idx_status] == claim_date:
            return

        self.dic_status[self.args.s_profile][idx_status] = claim_date
        self.dic_status[self.args.s_profile][4] = update_time

        self.status_save()
        self.is_update = True

    def sahara_login(self):
        """
        """
        for i in range(1, DEF_NUM_TRY+1):
            self.logit('sahara_login', f'try_i={i}/{DEF_NUM_TRY}')

            if i >= DEF_NUM_TRY/2:
                is_bulk = True
            else:
                is_bulk = False
            if self.init_okx(is_bulk) is False:
                continue

            self.page.get('https://legends.saharalabs.ai')
            # self.page.wait.load_start()
            self.page.wait(3)

            self.logit('sahara_login', f'tabs_count={self.page.tabs_count}')

            # 钱包未连接
            ele_btn = self.page.ele('@@tag()=span@@text()= Sign In ', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                self.logit('sahara_login', 'Need to Connect Wallet ...') # noqa
                ele_btn.click(by_js=True)
                self.page.wait(1)
                ele_btn = self.page.ele('@@tag()=div@@class=wallet@@text()=OKX Wallet', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    ele_btn.click(by_js=True)
                    self.page.wait(2)

            # OKX Wallet Connect
            self.save_screenshot(name='page_wallet_connect.jpg')
            if len(self.page.tab_ids) == 2:
                tab_id = self.page.latest_tab
                tab_new = self.page.get_tab(tab_id)
                ele_btn = tab_new.ele('@@tag()=button@@data-testid=okd-button@@text()=Connect', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    ele_btn.click(by_js=True)
                    self.page.wait(2)

            # OKX Wallet Signature request
            self.save_screenshot(name='page_wallet_signature.jpg')
            if len(self.page.tab_ids) == 2:
                tab_id = self.page.latest_tab
                tab_new = self.page.get_tab(tab_id)
                ele_btn = tab_new.ele('@@tag()=button@@data-testid=okd-button@@text():Confirm', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    ele_btn.click(by_js=True)
                    self.logit(None, 'OKX Wallet Signature request Confirmed [OK]')
                    self.page.wait(2)
                    break

            # OKX Wallet Add network
            if len(self.page.tab_ids) == 2:
                tab_id = self.page.latest_tab
                tab_new = self.page.get_tab(tab_id)
                ele_btn = tab_new.ele('@@tag()=button@@data-testid=okd-button@@text()=Approve', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    ele_btn.click(by_js=True)
                    self.page.wait(1)
                    continue

            # 钱包已连接
            ele_btn = self.page.ele('@@tag()=div@@class:address@@text():...', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                self.logit('sahara_login', 'Wallet is connected')
                return True
            else:
                self.logit('sahara_login', 'Wallet is failed to connected [ERROR]') # noqa
                continue

        return False

    def galxe_login(self):
        """
        """
        for i in range(1, DEF_NUM_TRY+1):
            self.logit('galxe_login', f'try_i={i}/{DEF_NUM_TRY}')

            # 钱包未连接
            ele_btn = self.page.ele('@@tag()=button@@text()=Log in', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                self.logit('sahara_login', 'Need to Connect Wallet ...') # noqa
                ele_btn.click(by_js=True)
                self.page.wait(1)
                ele_btn = self.page.ele('@@tag()=div@@class=ml-3@@text()=OKX', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    ele_btn.click(by_js=True)
                    self.page.wait(1)

                    # OKX Wallet Connect
                    self.save_screenshot(name='page_wallet_connect.jpg')
                    if len(self.page.tab_ids) == 2:
                        tab_id = self.page.latest_tab
                        tab_new = self.page.get_tab(tab_id)
                        ele_btn = tab_new.ele('@@tag()=button@@data-testid=okd-button@@text()=Connect', timeout=2) # noqa
                        if not isinstance(ele_btn, NoneElement):
                            ele_btn.click(by_js=True)
                            self.page.wait(3)
                    else:
                        continue

                    # OKX Wallet Signature request
                    self.save_screenshot(name='page_wallet_signature.jpg')
                    if len(self.page.tab_ids) == 2:
                        tab_id = self.page.latest_tab
                        tab_new = self.page.get_tab(tab_id)
                        ele_btn = tab_new.ele('@@tag()=button@@data-testid=okd-button@@text():Confirm', timeout=2) # noqa
                        if not isinstance(ele_btn, NoneElement):
                            ele_btn.click(by_js=True)
                            self.logit(None, 'OKX Wallet Signature request Confirmed [OK]')
                            self.page.wait(3)
                    else:
                        continue

                    # 弹窗
                    ele_btn = self.page.ele('@@tag()=span@@class=sr-only@@text()=Close', timeout=2) # noqa
                    if not isinstance(ele_btn, NoneElement):
                        self.logit(None, 'Close pop window ...') # noqa
                        ele_btn.click(by_js=True)
                        self.page.wait(1)

                    return True
            else:
                self.logit('galxe_login', 'Wallet is connected')
                return True

        return False

    def galxe_visit(self, s_task):
        """
        s_task
            Daily Visit the Sahara AI Blog
            Daily Visit the Sahara AI Twitter
        """
        ele_blk = self.page.ele(f'@@tag()=div@@class:w-full@@text()={s_task}', timeout=2) # noqa
        if not isinstance(ele_blk, NoneElement):
            ele_btn = ele_blk.ele(f'@@tag()=p@@text()={s_task}', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                self.logit('galxe_visit', f'Click {s_task}') # noqa
                ele_btn.click(by_js=True)
                self.page.wait(1)
                ele_btn = self.page.ele('@@tag()=div@@text()=Continue to Access', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    ele_btn.click(by_js=True)
                    self.page.wait(2)

        if len(self.page.tab_ids) == 2:
            tab_id = self.page.latest_tab
            s_title = self.page.get_tab(tab_id).title
            self.logit(None, f'Close tab:{s_title}') # noqa
            self.page.get_tab(tab_id).close()

            self.page.wait(3)
            ele_btn = ele_blk.eles('@@tag()=svg', timeout=2)
            if len(ele_btn) > 1:
                ele_refresh = ele_btn[-1]
                self.logit('galxe_visit', f'Update status {s_task}') # noqa
                ele_refresh.click()
                self.page.wait(3)


        # Check Status
        n_wait_sec = 5
        j = 0
        while j < n_wait_sec:
            j += 1

            ele_blk = self.page.ele(f'@@tag()=div@@class:w-full@@text()={s_task}', timeout=2) # noqa
            if not isinstance(ele_blk, NoneElement):
                ele_btn = ele_blk.ele('@@tag()=div@@class:text-success', timeout=2) # noqa
                if not isinstance(ele_btn, NoneElement):
                    self.logit(None, f'Check status, success, took {j} seconds.') # noqa
                    return True

            self.page.wait(1)
            self.logit(None, f'Wait {j}/{n_wait_sec}')

        if j >= n_wait_sec:
            self.logit(None, f'Check status failed, took {j} seconds.') # noqa
            return False

        return False

    def tips_click(self):
        ele_btn = self.page.ele('Next（1/2）', timeout=2)
        if not isinstance(ele_btn, NoneElement):
            ele_btn.click(by_js=True)
            self.page.wait(2)

        ele_btn = self.page.ele('Done（2/2）', timeout=2)
        if not isinstance(ele_btn, NoneElement):
            ele_btn.click(by_js=True)

    def galxe_task(self):
        """
        """
        for i in range(1, DEF_NUM_TRY+1):
            self.logit('galxe_task', f'try_i={i}/{DEF_NUM_TRY}')

            self.page.get('https://app.galxe.com/quest/SaharaAI/GCNLYtpFM5')
            # self.page.wait.load_start()
            self.page.wait(3)

            self.galxe_login()
            self.tips_click()

            b_ret = self.galxe_visit('Daily Visit the Sahara AI Blog')
            b_ret = b_ret and self.galxe_visit('Daily Visit the Sahara AI Twitter') # noqa

            # self.page.back(1)
            self.page.get('https://legends.saharalabs.ai')

            return b_ret


    def gobibear_claim(self, s_task, idx_status):
        """
        s_task
            Visit the Sahara AI blog
            Visit @SaharaLabsAI on X
        """
        ele_blk = self.page.ele(f'@@tag()=div@@class=task-item@@text():{s_task}', timeout=2) # noqa
        if not isinstance(ele_blk, NoneElement):
            ele_btn = ele_blk.ele('@@tag()=div@@class=task-buttons', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                s_info = ele_btn.text
                self.logit('gobibear_claim', f'Status: {s_info} [{s_task}]') # noqa

                if 'claim' == s_info:
                    ele_btn.click()
                    self.page.wait(3)
                    self.update_status(idx_status)
                    self.logit(None, f'Claim success [{s_task}]') # noqa
                    return True
                elif 'claimed' == s_info:
                    self.logit(None, f'Already claimed before [{s_task}]') # noqa
                    self.update_status(idx_status)
                    return True
                else:
                    if self.galxe_task():
                        self.click_gobibear()

        return False

    def get_utc_date(self, s_text):
        # 提取日期和时间部分
        date_time_str = s_text.split('\n')[1].strip()
        # 定义日期时间格式
        date_time_format = "%m/%d/%Y, %H:%M:%S"
        # 将字符串转换为datetime对象
        date_time_obj = datetime.strptime(date_time_str, date_time_format)
        # 将datetime对象转换为时间戳
        ts_tx = int(time.mktime(date_time_obj.timetuple()))

        if int(time.time()) - ts_tx > 3600 * 4:
            ts_tx = ts_tx - 86400

        date_tx = format_ts(ts_tx, style=1, tz_offset=TZ_OFFSET)
        date_tx = date_tx[:10]

        return date_tx

    def is_tx_exist(self):
        s_url = f'chrome-extension://{EXTENSION_ID_OKX}/home.html'
        self.page.get(s_url)
        # self.page.wait.load_start()
        self.page.wait(3)

        ele_btn = self.page.ele('@@tag()=div@@class=_container_1eikt_1', timeout=2) # noqa
        if not isinstance(ele_btn, NoneElement):
            ele_btn.click(by_js=True)
            self.page.wait(1)

        # Search network name
        ele_input = self.page.ele('@@tag()=input@@data-testid=okd-input', timeout=2) # noqa
        if not isinstance(ele_input, NoneElement):
            self.logit('is_tx_exist', 'Change network to SaharaAI Testnet ...') # noqa
            self.page.actions.move_to(ele_input).click().type('sahara')
            self.page.wait(3)
            ele_btn = self.page.ele('@@tag()=div@@class:_title@@text()=SaharaAI Testnet', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                ele_btn.click(by_js=True)
                self.page.wait(3)

                # History
                ele_blk = self.page.ele(f'@@tag()=div@@class:_iconWrapper_@@text()=History', timeout=2) # noqa
                if not isinstance(ele_blk, NoneElement):
                    self.logit(None, 'Click History ...') # noqa
                    ele_btn = ele_blk.ele('@@tag()=div@@class:_wallet', timeout=2) # noqa
                    if not isinstance(ele_btn, NoneElement):
                        ele_btn.click(by_js=True)
                        self.page.wait(2)

                        # Completed
                        ele_btns = self.page.eles('.tx-history-list-row', timeout=2) # noqa
                        self.logit(None, f'Completed tx: {len(ele_btns)}') # noqa
                        if len(ele_btns) > 0:
                            ele_btn = ele_btns[0]
                            ele_btn.click(by_js=True)
                            self.page.wait(2)

                            ele_info = self.page.ele('@@tag()=div@@class:tx-detail-info__one@@text():Time', timeout=2) # noqa
                            if not isinstance(ele_info, NoneElement):
                                s_info = ele_info.text
                                date_tx = self.get_utc_date(s_info)
                                date_now = format_ts(time.time(), style=1, tz_offset=TZ_OFFSET)

                                self.logit(None, f'latest tx: {s_info.replace('\n', ' ')}') # noqa
                                if date_tx == date_now:
                                    self.logit(None, 'Today\'s tx is exist, return True') # noqa
                                    return True
                                else:
                                    self.logit(None, f'tx is outdated, return False') # noqa
                                #     # 可能是 Pending 状态
                                #     return False

                        # Pending 如果不是0，需要等待
                        ele_info = self.page.ele('@@tag()=div@@class:tx-history__tabs-option@@text():Pending', timeout=2) # noqa
                        if not isinstance(ele_info, NoneElement):
                            s_info = ele_info.text
                            if s_info.find('(0)') >= 0:
                                self.logit(None, 'No pending tx') # noqa
                                return False
                            else:
                                n_sleep = 10
                                self.logit(None, f'[WARNING] tx is Pending: {s_info} Sleep {n_sleep} seconds') # noqa
                                self.page.wait(n_sleep)
                                return True
        else:
            # Cancel Uncomplete request
            ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button@@text():Cancel', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                ele_btn.click(by_js=True)
                self.page.wait(1)
                self.logit(None, 'Uncomplete request. Cancel')

        return True


    def gene_tx(self):
        s_url = f'chrome-extension://{EXTENSION_ID_OKX}/home.html'
        self.page.get(s_url)
        # self.page.wait.load_start()
        self.page.wait(3)

        self.logit('gene_tx', 'Generate a new transaction')

        ele_btn = self.page.ele('@@tag()=div@@class=_container_1eikt_1', timeout=2) # noqa
        if not isinstance(ele_btn, NoneElement):
            ele_btn.click(by_js=True)
            self.page.wait(1)

        # Search network name
        ele_input = self.page.ele('@@tag()=input@@data-testid=okd-input', timeout=2) # noqa
        if not isinstance(ele_input, NoneElement):
            self.page.actions.move_to(ele_input).click().type('sahara')
            self.page.wait(3)
            ele_btn = self.page.ele('@@tag()=div@@class:_title@@text()=SaharaAI Testnet', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                ele_btn.click(by_js=True)
                self.page.wait(3)

                # Send
                ele_blk = self.page.ele(f'@@tag()=div@@class:_iconWrapper_@@text()=Send', timeout=2) # noqa
                if not isinstance(ele_blk, NoneElement):
                    ele_btn = ele_blk.ele('@@tag()=div@@class:_wallet', timeout=2) # noqa
                    if not isinstance(ele_btn, NoneElement):
                        ele_btn.click(by_js=True)
                        self.page.wait(2)

                        # Enter wallet address or domain name
                        ele_input = self.page.ele('@@tag()=textarea@@data-testid=okd-input@@placeholder:Enter', timeout=2) # noqa
                        if not isinstance(ele_input, NoneElement):
                            lst_addr = []
                            # 据说是官方领水地址
                            # lst_addr.append('0x126c08a58cC12494Eb4508c73C703162722256b1')
                            evm_addr = self.dic_purse[self.args.s_profile]
                            if len(evm_addr) >= 3:
                                lst_addr.append(evm_addr[2])
                            to_addr = random.choice(lst_addr)
                            self.page.actions.move_to(ele_input).click().type(to_addr)
                            self.page.wait(2)

                        # Amount
                        ele_input = self.page.ele('@@tag()=input@@data-testid=okd-input@@placeholder=0.000000', timeout=2) # noqa
                        if not isinstance(ele_input, NoneElement):
                            flt_amount = random.uniform(0.0000001, 0.0000009)
                            str_amount = "{:.7f}".format(flt_amount)
                            self.page.actions.move_to(ele_input).click().type(str_amount)
                            self.page.wait(2)

                        # Next
                        ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button', timeout=2) # noqa
                        if not isinstance(ele_btn, NoneElement):
                            ele_btn.click(by_js=True)
                            self.page.wait(2)
                            self.logit(None, '[transaction] Click Next')

                        # Confirm
                        ele_btn = self.page.ele('@@tag()=button@@data-testid=okd-button@@text():Confirm', timeout=2) # noqa
                        if not isinstance(ele_btn, NoneElement):
                            ele_btn.click(by_js=True)
                            self.page.wait(6)
                            self.logit(None, 'Confirm transaction')
                            return True
        return False

    def click_gobibear(self):
        self.page.get('https://legends.saharalabs.ai')
        ele_blocks = self.page.eles(f'@@tag()=div@@class=map-point map-animal', timeout=2) # noqa

        if len(ele_blocks) > 0:
            ele_btn = ele_blocks[0]
            ele_btn.click(by_js=True)
            self.page.wait(1)
            return True
        else:
            return False

    def gobi_bear(self):
        """
        """
        b_ret_tx = False
        b_tx_exist = False

        for i in range(1, DEF_NUM_TRY+1):
            self.logit('gobi_bear', f'try_i={i}/{DEF_NUM_TRY}')

            idx_status = 3
            if self.is_task_complete(idx_status):
                b_ret_tx = True
            else:
                if not b_tx_exist:
                    b_tx_exist = self.is_tx_exist()
                self.logit('gobi_bear', f'b_tx_exist={b_tx_exist}')

                self.click_gobibear()

                s_task = 'Generate at least one transaction on Sahara Testnet'
                s_xpath = f'@@tag()=div@@class=task-item@@text():{s_task}'
                ele_blk = self.page.ele(s_xpath, timeout=2)
                if not isinstance(ele_blk, NoneElement):
                    ele_btn = ele_blk.ele('@@tag()=div@@class=task-buttons', timeout=2) # noqa
                    if not isinstance(ele_btn, NoneElement):
                        s_info = ele_btn.text
                        self.logit('gobibear_claim', f'Status: {s_info} [{s_task}]') # noqa
                        if 'claim' == s_info:
                            ele_btn.click()
                            self.page.wait(3)
                            self.update_status(3)
                            self.logit(None, f'Claim success ✅ [{s_task}]') # noqa
                            b_ret_tx = True
                        elif 'claimed' == s_info:
                            self.logit(None, f'Already claimed before [{s_task}]') # noqa
                            self.update_status(3)
                            b_ret_tx = True
                        elif b_tx_exist:
                            self.logit(None, f'Refresh ⭕️ [{s_task}]') # noqa
                            ele_btn.click()
                            self.page.wait(10)
                        else:
                            self.gene_tx()
                            self.page.wait(10)

            b_ret_visit = True
            ele_btn = self.page.ele('@@tag()=div@@class=task-group-tab active@@text()=Daily Check-in', timeout=2) # noqa
            if not isinstance(ele_btn, NoneElement):
                idx_status = 1
                if not self.is_task_complete(idx_status):
                    s_task = 'Visit the Sahara AI blog'
                    b_visit1 = self.gobibear_claim(s_task, idx_status)
                else:
                    b_visit1 = True

                idx_status = 2
                if not self.is_task_complete(idx_status):
                    s_task = 'Visit @SaharaLabsAI on X'
                    b_visit2 = self.gobibear_claim(s_task, idx_status)
                else:
                    b_visit2 = True

                b_ret_visit = b_visit1 and b_visit2


            if b_ret_tx and b_ret_visit:
                break

        b_ret = b_ret_tx and b_ret_visit

        return b_ret

    def sahara_run(self):
        if not self.sahara_login():
            return False

        self.gobi_bear()

        self.logit('sahara_run', 'Finished!')
        self.close()

        return True


def send_msg(instSaharaTask, lst_success):
    if len(DEF_DING_TOKEN) > 0 and len(lst_success) > 0:
        s_info = ''
        for s_profile in lst_success:
            if s_profile in instSaharaTask.dic_status:
                lst_status = instSaharaTask.dic_status[s_profile]
            else:
                lst_status = [s_profile, -1]

            s_info += '- {} {}\n'.format(
                s_profile,
                lst_status[1],
            )
        d_cont = {
            'title': 'Daily Active Finished! [sahara]',
            'text': (
                'Daily Active [sahara]\n'
                '- {}\n'
                '{}\n'
                .format(DEF_HEADER_STATUS, s_info)
            )
        }
        ding_msg(d_cont, DEF_DING_TOKEN, msgtype="markdown")


def main(args):
    if args.sleep_sec_at_start > 0:
        logger.info(f'Sleep {args.sleep_sec_at_start} seconds at start !!!') # noqa
        time.sleep(args.sleep_sec_at_start)

    if DEL_PROFILE_DIR and os.path.exists(DEF_PATH_USER_DATA):
        logger.info(f'Delete {DEF_PATH_USER_DATA} ...')
        shutil.rmtree(DEF_PATH_USER_DATA)
        logger.info(f'Directory {DEF_PATH_USER_DATA} is deleted') # noqa

    instSaharaTask = SaharaTask()

    if len(args.profile) > 0:
        items = args.profile.split(',')
    else:
        # 从配置文件里获取钱包名称列表
        items = list(instSaharaTask.dic_purse.keys())

    profiles = copy.deepcopy(items)

    # 每次随机取一个出来，并从原列表中删除，直到原列表为空
    total = len(profiles)
    n = 0

    lst_success = []

    def is_complete(lst_status):
        b_ret = True
        if lst_status:
            for idx_status in [1, 2, 3]:
                claimed_date = lst_status[idx_status]
                date_now = format_ts(time.time(), style=1, tz_offset=TZ_OFFSET) # noqa
                if date_now != claimed_date:
                    b_ret = b_ret and False
        else:
            b_ret = False
        return b_ret

    # 将已完成的剔除掉
    instSaharaTask.status_load()
    # 从后向前遍历列表的索引
    for i in range(len(profiles) - 1, -1, -1):
        s_profile = profiles[i]
        if s_profile in instSaharaTask.dic_status:
            lst_status = instSaharaTask.dic_status[s_profile]
            if is_complete(lst_status):
                n += 1
                profiles.pop(i)
        else:
            continue
    logger.info('#'*40)
    percent = math.floor((n / total) * 100)
    logger.info(f'Progress: {percent}% [{n}/{total}]') # noqa

    while profiles:
        n += 1
        logger.info('#'*40)
        s_profile = random.choice(profiles)
        percent = math.floor((n / total) * 100)
        logger.info(f'Progress: {percent}% [{n}/{total}] [{s_profile}]') # noqa
        profiles.remove(s_profile)

        args.s_profile = s_profile

        if s_profile not in instSaharaTask.dic_purse:
            logger.info(f'{s_profile} is not in purse conf [ERROR]')
            sys.exit(0)

        def _run():
            s_directory = f'{DEF_PATH_USER_DATA}/{args.s_profile}'
            if os.path.exists(s_directory) and os.path.isdir(s_directory):
                pass
            else:
                # Create new profile
                instSaharaTask.initChrome(args.s_profile)
                instSaharaTask.init_okx()
                instSaharaTask.close()

            instSaharaTask.initChrome(args.s_profile)
            is_claim = instSaharaTask.sahara_run()
            return is_claim

        # 如果出现异常(与页面的连接已断开)，增加重试
        max_try_except = 3
        for j in range(1, max_try_except+1):
            try:
                is_claim = False
                if j > 1:
                    logger.info(f'异常重试，当前是第{j}次执行，最多尝试{max_try_except}次 [{s_profile}]') # noqa

                instSaharaTask.set_args(args)
                instSaharaTask.status_load()

                if s_profile in instSaharaTask.dic_status:
                    lst_status = instSaharaTask.dic_status[s_profile]
                else:
                    lst_status = None

                is_claim = False
                is_ready_claim = True
                if is_complete(lst_status):
                    logger.info(f'[{s_profile}] Last update at {avail_time}') # noqa
                    is_ready_claim = False
                    break
                if is_ready_claim:
                    is_claim = _run()

                if is_claim:
                    lst_success.append(s_profile)
                    instSaharaTask.close()
                    break

            except Exception as e:
                logger.info(f'[{s_profile}] An error occurred: {str(e)}')
                instSaharaTask.close()
                if j < max_try_except:
                    time.sleep(5)

        if instSaharaTask.is_update is False:
            continue

        logger.info(f'Progress: {percent}% [{n}/{total}] [{s_profile} Finish]')

        if len(items) > 0:
            sleep_time = random.randint(args.sleep_sec_min, args.sleep_sec_max)
            if sleep_time > 60:
                logger.info('sleep {} minutes ...'.format(int(sleep_time/60)))
            else:
                logger.info('sleep {} seconds ...'.format(int(sleep_time)))
            time.sleep(sleep_time)

    send_msg(instSaharaTask, lst_success)


if __name__ == '__main__':
    """
    每次随机取一个出来，并从原列表中删除，直到原列表为空
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--loop_interval', required=False, default=60, type=int,
        help='[默认为 60] 执行完一轮 sleep 的时长(单位是秒)，如果是0，则不循环，只执行一次'
    )
    parser.add_argument(
        '--sleep_sec_min', required=False, default=3, type=int,
        help='[默认为 3] 每个账号执行完 sleep 的最小时长(单位是秒)'
    )
    parser.add_argument(
        '--sleep_sec_max', required=False, default=10, type=int,
        help='[默认为 10] 每个账号执行完 sleep 的最大时长(单位是秒)'
    )
    parser.add_argument(
        '--sleep_sec_at_start', required=False, default=0, type=int,
        help='[默认为 0] 在启动后先 sleep 的时长(单位是秒)'
    )
    parser.add_argument(
        '--profile', required=False, default='',
        help='按指定的 profile 执行，多个用英文逗号分隔'
    )
    args = parser.parse_args()
    if args.loop_interval <= 0:
        main(args)
    else:
        while True:
            main(args)
            logger.info('#####***** Loop sleep {} seconds ...'.format(args.loop_interval)) # noqa
            time.sleep(args.loop_interval)

"""
python3 sahara.py --sleep_sec_min=30 --sleep_sec_max=60 --loop_interval=60
python3 sahara.py --sleep_sec_min=600 --sleep_sec_max=1800 --loop_interval=60
python3 sahara.py --sleep_sec_min=60 --sleep_sec_max=180
"""
