[app]
title = Nia IA
package.name = niaia
package.domain = org.wizkhay
source.dir = .
source.include_exts = py,png,json
version = 1.0

# Mantém a versão estável com suporte de rede
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,charset-normalizer,idna,chardet,openssl

presplash.filename = nia.png
icon.filename = nia.png
orientation = portrait

# Trava as ferramentas do Android nas versões compatíveis e testadas
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET
android.private_storage = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 1
