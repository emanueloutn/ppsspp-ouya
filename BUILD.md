# Compilar PPSSPP para OUYA

Base: PPSSPP v1.17, commit 493122a2fcf9ff538e242fe2844f019b53afd483. El ZIP fuente de la release contiene el código correspondiente, dependencias, licencias y cambios fechados. El parche permite revisar las modificaciones. No incluye claves privadas de esta adaptación.

## Herramientas y pasos

Windows x64, Python 3, Git, Android NDK r21e (21.4.7075529), CMake 3.31.6, Android Build Tools 35.0.0 y un JDK. Usa las distribuciones oficiales de esas herramientas.

Extrae el ZIP fuente. Desde la raíz de este repositorio:

```powershell
$env:OUYA_STORE_PASSWORD = 'CLAVE_DE_TU_ALMACEN'
$env:OUYA_KEY_PASSWORD = 'CLAVE_DE_TU_ALIAS'
.\tools\build.ps1 -SourceRoot 'RUTA\ppsspp-source' -NdkRoot 'RUTA\android-ndk-r21e' -CMakeExe 'RUTA\cmake.exe' -BuildTools 'RUTA\build-tools\35.0.0' -Jdk 'RUTA\JDK' -BaseApk 'RUTA\ppsspp-1.17-base.apk' -Keystore 'RUTA\tu-clave.p12' -KeyAlias 'tu-alias'
```

Salidas: build/PPSSPP-OUYA-unsigned.apk y build/PPSSPP-OUYA-signed.apk. Una firma distinta no puede actualizar la APK publicada directamente. No se necesita la clave privada del mantenedor para estudiar, modificar o compilar el programa.

## Método usado

Se recompila la biblioteca nativa para ARMv7/API 16, C++ estático y NEON. Se usa Release, USE_DISCORD=OFF, HEADLESS=OFF y UNITTEST=OFF. Se conservan las clases Java y recursos del contenedor Android 1.17 original de la consola; se modifica manifiesto/etiqueta y se añaden los avisos y la licencia. El empaquetador exige el SHA256 exacto del APK base documentado en BUILD-INFO.json y no debe aplicarse a un APK arbitrario.

El árbol fuente incluye también el proyecto Gradle para recompilar el contenedor completo, con sus dependencias Android; esa ruta no fue la utilizada para generar esta APK. Puedes obtener PPSSPP original en https://www.ppsspp.org/ y su fuente en https://github.com/hrydgard/ppsspp/tree/v1.17. No se incluye el APK base de la consola como descarga adicional.

La fuente se ofrece con las licencias originales. Para limitar el tamaño del archivo se omiten bibliotecas precompiladas de plataformas ajenas al objetivo; se conservan el código y los binarios FFmpeg de Android ARMv7 necesarios para esta compilación. Se excluye la clave debug pública de upstream: genera tu propia clave si usas el proyecto Gradle.

No se promete identidad bit a bit: rutas, compilador, versión generada, fechas ZIP y clave pueden cambiar los bytes. La firma v1 permite instalar en API 16.

## Verificación

Comprueba firma, arquitectura armeabi-v7a, paquete org.ppsspp.ouyapp, etiqueta OUYA17, API mínima 16 y actividad MAIN/LAUNCHER sin categoría OUYA GAME, para MAKE → Software. En el APK deben estar assets/OUYA/LICENSE.TXT, NOTICE.md y CREDITS.md, además de los créditos originales del emulador.

VERIFICATION.md describe las pruebas realizadas y sus límites. Las instrucciones del perfil de rendimiento están en profiles/OUYA.md. Las partidas y juegos se conservan por separado.
