[app]
title = Nia IA
package.name = niaia
package.domain = org.wizkhay
source.dir = .
source.include_exts = py,png,json
version = 1.0
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,openssl
presplash.filename = nia.png
icon.filename = nia.png
orientation = portrait

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.private_storage = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
