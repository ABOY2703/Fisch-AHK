# Required: pip install pyautogui keyboard pillow requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import configparser
import os
import threading
import pyautogui
import keyboard
from PIL import ImageGrab
import requests

SETTINGS_FILE = 'Settings.ini'

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Fisch Macro - Python Version')
        self.geometry('800x550')
        self.configure(bg='#FFFFFF')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.general_frame = ttk.Frame(self.notebook)
        self.shake_frame = ttk.Frame(self.notebook)
        self.minigame_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.general_frame, text='General Settings')
        self.notebook.add(self.shake_frame, text='Shake Settings')
        self.notebook.add(self.minigame_frame, text='Minigame Settings')

        self.create_general_settings(self.general_frame)
        self.create_shake_settings(self.shake_frame)
        self.create_minigame_settings(self.minigame_frame)
        self.load_settings()

    def create_general_settings(self, frame):
        # Variables
        self.var_AutoLowerGraphics = tk.BooleanVar()
        self.var_AutoZoomInCamera = tk.BooleanVar()
        self.var_AutoEnableCameraMode = tk.BooleanVar()
        self.var_AutoLookDownCamera = tk.BooleanVar()
        self.var_AutoBlurCamera = tk.BooleanVar()
        self.var_RestartDelay = tk.StringVar()
        self.var_HoldRodCastDuration = tk.StringVar()
        self.var_WaitForBobberDelay = tk.StringVar()
        self.var_BaitDelay = tk.StringVar()
        self.var_WebhookURL = tk.StringVar()
        self.var_HookInterval = tk.StringVar()
        self.var_LoadSettingsFileName = tk.StringVar(value='settings')

        row = 0
        ttk.Label(frame, text='Auto Lower Graphics:').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Checkbutton(frame, variable=self.var_AutoLowerGraphics).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Auto Zoom In:').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Checkbutton(frame, variable=self.var_AutoZoomInCamera).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Auto Enable Camera Mode:').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Checkbutton(frame, variable=self.var_AutoEnableCameraMode).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Auto Look Down:').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Checkbutton(frame, variable=self.var_AutoLookDownCamera).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Auto Blur:').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Checkbutton(frame, variable=self.var_AutoBlurCamera).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Restart Delay (ms):').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Entry(frame, textvariable=self.var_RestartDelay).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Hold Rod Cast Duration (ms):').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Entry(frame, textvariable=self.var_HoldRodCastDuration).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Wait for Bobber to Land (ms):').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Entry(frame, textvariable=self.var_WaitForBobberDelay).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Bait Delay (ms):').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Entry(frame, textvariable=self.var_BaitDelay).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Webhook URL:').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Entry(frame, textvariable=self.var_WebhookURL, width=30).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Hook Interval (catches):').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Entry(frame, textvariable=self.var_HookInterval).grid(row=row, column=1, sticky='w')
        row += 1
        ttk.Label(frame, text='Config file name (no .ini needed):').grid(row=row, column=0, sticky='w', padx=30, pady=5)
        ttk.Entry(frame, textvariable=self.var_LoadSettingsFileName, width=15).grid(row=row, column=1, sticky='w')
        row += 1
        # Save/Load Buttons
        ttk.Button(frame, text='Save Settings', command=self.save_settings).grid(row=row, column=0, pady=20)
        ttk.Button(frame, text='Load Settings', command=self.load_settings).grid(row=row, column=1, pady=20)
        ttk.Button(frame, text='Exit', command=self.exit_app).grid(row=row, column=2, pady=20)
        ttk.Button(frame, text='Start Macro', command=self.start_macro).grid(row=row, column=3, pady=20)

    def save_settings(self):
        config = configparser.ConfigParser()
        config['General'] = {
            'AutoLowerGraphics': str(self.var_AutoLowerGraphics.get()),
            'AutoZoomInCamera': str(self.var_AutoZoomInCamera.get()),
            'AutoEnableCameraMode': str(self.var_AutoEnableCameraMode.get()),
            'AutoLookDownCamera': str(self.var_AutoLookDownCamera.get()),
            'AutoBlurCamera': str(self.var_AutoBlurCamera.get()),
            'RestartDelay': self.var_RestartDelay.get(),
            'HoldRodCastDuration': self.var_HoldRodCastDuration.get(),
            'WaitForBobberDelay': self.var_WaitForBobberDelay.get(),
            'BaitDelay': self.var_BaitDelay.get(),
            'WebhookURL': self.var_WebhookURL.get(),
            'HookInterval': self.var_HookInterval.get(),
        }
        config['Shake'] = {
            'NavigationKey': self.var_NavigationKey.get(),
            'ShakeMode': self.var_ShakeMode.get(),
            'ClickShakeFailsafe': self.var_ClickShakeFailsafe.get(),
            'ClickShakeColorTolerance': self.var_ClickShakeColorTolerance.get(),
            'ClickScanDelay': self.var_ClickScanDelay.get(),
            'RepeatBypassCounter': self.var_RepeatBypassCounter.get(),
            'NavigationShakeFailsafe': self.var_NavigationShakeFailsafe.get(),
            'NavigationSpamDelay': self.var_NavigationSpamDelay.get(),
        }
        config['Minigame'] = {
            'ManualBarSize': self.var_ManualBarSize.get(),
            'BarCalculationFailsafe': self.var_BarCalculationFailsafe.get(),
            'BarSizeCalculationColorTolerance': self.var_BarSizeCalculationColorTolerance.get(),
            'FishBarColorTolerance': self.var_FishBarColorTolerance.get(),
            'WhiteBarColorTolerance': self.var_WhiteBarColorTolerance.get(),
            'ArrowColorTolerance': self.var_ArrowColorTolerance.get(),
            'StabilizerLoop': self.var_StabilizerLoop.get(),
            'SideBarRatio': self.var_SideBarRatio.get(),
            'SideBarWaitMultiplier': self.var_SideBarWaitMultiplier.get(),
            'StableRightMultiplier': self.var_StableRightMultiplier.get(),
            'StableRightDivision': self.var_StableRightDivision.get(),
            'StableLeftMultiplier': self.var_StableLeftMultiplier.get(),
            'StableLeftDivision': self.var_StableLeftDivision.get(),
            'UnstableRightMultiplier': self.var_UnstableRightMultiplier.get(),
            'UnstableRightDivision': self.var_UnstableRightDivision.get(),
            'UnstableLeftMultiplier': self.var_UnstableLeftMultiplier.get(),
            'UnstableLeftDivision': self.var_UnstableLeftDivision.get(),
            'RightAnkleBreakMultiplier': self.var_RightAnkleBreakMultiplier.get(),
            'LeftAnkleBreakMultiplier': self.var_LeftAnkleBreakMultiplier.get(),
        }
        filename = self.var_LoadSettingsFileName.get().strip() or 'settings'
        with open(f'{filename}.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        messagebox.showinfo('Settings', f'Settings saved as {filename}.ini!')

    def load_settings(self):
        config = configparser.ConfigParser()
        filename = self.var_LoadSettingsFileName.get().strip() or 'settings'
        ini_file = f'{filename}.ini'
        if not os.path.exists(ini_file):
            return
        try:
            config.read(ini_file, encoding='utf-8')
            general = config['General'] if 'General' in config else {}
            shake = config['Shake'] if 'Shake' in config else {}
            minigame = config['Minigame'] if 'Minigame' in config else {}
        except Exception as e:
            try:
                os.remove(ini_file)
            except Exception:
                pass
            messagebox.showwarning('Settings', f'Settings file was corrupt or in the wrong format and will be reset. ({e})')
            self.save_settings()
            config.read(ini_file, encoding='utf-8')
            # Try to load again (now guaranteed to be valid)
            config.read(SETTINGS_FILE, encoding='utf-8')
            general = config['General'] if 'General' in config else {}
        self.var_AutoLowerGraphics.set(general.get('AutoLowerGraphics', 'False') == 'True')
        self.var_AutoZoomInCamera.set(general.get('AutoZoomInCamera', 'False') == 'True')
        self.var_AutoEnableCameraMode.set(general.get('AutoEnableCameraMode', 'False') == 'True')
        self.var_AutoLookDownCamera.set(general.get('AutoLookDownCamera', 'False') == 'True')
        self.var_AutoBlurCamera.set(general.get('AutoBlurCamera', 'False') == 'True')
        self.var_RestartDelay.set(general.get('RestartDelay', '1000'))
        self.var_HoldRodCastDuration.set(general.get('HoldRodCastDuration', '600'))
        self.var_WaitForBobberDelay.set(general.get('WaitForBobberDelay', '1000'))
        self.var_BaitDelay.set(general.get('BaitDelay', '600'))
        self.var_WebhookURL.set(general.get('WebhookURL', ''))
        self.var_HookInterval.set(general.get('HookInterval', '3'))
        messagebox.showinfo('Settings', 'Settings loaded!')

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
