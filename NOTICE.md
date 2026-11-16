# Aviso de modificación — 15 de noviembre de 2026

OUYA17 / PPSSPP para OUYA es una adaptación comunitaria no oficial de PPSSPP 1.17, creado por Henrik Rydgård y sus colaboradores.

Archivo de código modificado: android/jni/app-android.cpp. La función del mando joystickAxis usa copias de arreglos JNI y validación de entradas para evitar el desbordamiento de referencias retenidas observado en Android 4.1. También se incluye <vector> explícitamente. El parche contiene la modificación y su fecha.

El contenedor Android fue adaptado para instalarse como org.ppsspp.ouyapp, con etiqueta OUYA17 y minSdkVersion 16. Se conservan las clases Java, recursos, assets y créditos originales; se sustituye la biblioteca nativa por la recompilada y se añaden estos avisos y la licencia. Se firma con una clave local de la adaptación, diferente de la del proyecto original.

Esta versión no incorpora una optimización del motor que garantice más FPS. La configuración documentada prioriza velocidad de emulación y audio en OUYA a cambio de resolución y cuadros omitidos.

El código fuente correspondiente y las instrucciones se distribuyen junto con la APK bajo GNU GPL v2 o posterior. Sin garantía conforme a la licencia. Donaciones voluntarias al mantenedor de esta adaptación; no representan pagos ni aportes al equipo original.

Acceso OUYA corregido: se conserva MAIN + LAUNCHER y se elimina la categoría OUYA GAME del filtro principal para su inclusión como app instalada en MAKE → Software. La etiqueta de la consola es OUYA17. Cambio fechado el 15 de noviembre de 2026.
