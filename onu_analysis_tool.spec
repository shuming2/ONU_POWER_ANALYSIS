# -*- mode: python -*-
# -*- coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['G:\\PyCharmProjects\\端口分析\\venv', 'G:\\PyCharmProjects\\端口分析', 'G:\\PyCharmProjects\\端口分析\\venv\\Lib\\site-packages'],
             binaries=[],
             datas=[('pic\\panda.ico', 'pic'), ('config.py', '\\')],
             hiddenimports=['pymysql', 'clipboard', 'matplotlib', 'requests'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='onu_analysis_tool',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False, icon='pic/panda.ico' )
