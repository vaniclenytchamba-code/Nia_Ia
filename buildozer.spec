[app]

# (str) Title of your application
title = Nia IA

# (str) Package name
package.name = niaia

# (str) Package domain (needed for android packaging)
package.domain = org.wizkhay

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,json

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,openssl

# (str) Presplash of the application
presplash.filename = nia.png

# (str) Icon of the application
icon.filename = nia.png

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# ==============================================================================
# CONFIGURAÇÕES ESPECÍFICAS DO ANDROID (PERMISSÕES E INTERNET)
# ==============================================================================

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use (Atualizado para evitar o erro 404)
android.ndk = 26b

# (bool) Use --private data directory for storage (true or false)
android.private_storage = True

# (list) The Android architectures for which to build the APK
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup
android.allow_backup = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
