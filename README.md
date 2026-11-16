# PPSSPP para OUYA — adaptación comunitaria no oficial

Versión basada en **PPSSPP 1.17**, creada por **Henrik Rydgård y los colaboradores de PPSSPP**. Esta adaptación incorpora una corrección del mando para Android 4.1 y una configuración de rendimiento probada en una OUYA real.

**PPSSPP original:** https://www.ppsspp.org/ · **Código original:** https://github.com/hrydgard/ppsspp

No es una versión oficial ni está respaldada por el equipo de PPSSPP, Sony, NVIDIA u OUYA. Los créditos originales se conservan. El desarrollo del emulador corresponde al proyecto PPSSPP; el mantenimiento de esta adaptación se realiza en este repositorio.

## Descargar e instalar

Descarga `PPSSPP-OUYA-1.17-ouya.1.apk` en **Releases**, junto con `SHA256SUMS` y el archivo de código fuente correspondiente. En la consola aparece como **OUYA17** y se instala junto a PPSSPP original, con el identificador `org.ppsspp.ouyapp`.

Requiere OUYA con Android 4.1 / API 16 y ARMv7. No necesita una computadora encendida para jugar. No incluye juegos, archivos ISO/CSO ni partidas.

La APK conserva los valores predeterminados de PPSSPP. El ajuste de rendimiento usado en las pruebas se documenta en `profiles/OUYA.md`: no se importa automáticamente ninguna configuración personal. Ambas instalaciones pueden utilizar `/sdcard/PSP`; cierra una antes de abrir la otra porque pueden compartir controles, ajustes y partidas.

## Cambios de esta adaptación

- Corrección de `NativeApp.joystickAxis`: se sustituyen los arreglos JNI retenidos y nunca liberados por copias con `GetIntArrayRegion` / `GetFloatArrayRegion`, con validación de límites y excepciones.
- Compilación nativa ARMv7, API 16, NEON y bibliotecas C++ estáticas.
- Instalación separada y etiqueta OUYA17; Android mínimo ajustado a API 16.
- Licencia y avisos de esta adaptación incluidos también en `assets/OUYA/` dentro del APK. La pantalla de créditos original de PPSSPP permanece intacta.

## Pruebas y límites

El código corregido del mando procesó **20.000 eventos sintéticos en una OUYA real** sin el desbordamiento de referencias JNI observado en la versión anterior. También se comprobaron valores y entradas inválidas. Es una prueba aislada de la función, no una sesión prolongada con un mando físico.

Se verificaron firma, instalación, carga de la biblioteca y arranque de **GTA: Liberty City Stories USA v1.05**. El usuario informó que la versión era jugable, con audio satisfactorio y velocidades de emulación generalmente entre 96 y 102 %, dependiendo de la escena. Con salto automático de cuadros se observaron aproximadamente 15–20 FPS en exteriores y hasta 30 en escenas ligeras. No es una comparación controlada ni una garantía de rendimiento.

No se garantiza que elimine todos los cierres ni que alcance 30 FPS constantes. La resolución 1x se ve pixelada en pantallas grandes; 2x redujo el rendimiento en las pruebas. Omitir efectos de búfer produjo pantalla negra y se descartó. Otros juegos o firmwares pueden comportarse de otra manera.

## Créditos y licencia

Henrik Rydgård creó PPSSPP. Sus numerosos colaboradores y los autores de las dependencias conservan sus créditos y derechos. Consulta `CREDITS.md`, `LICENSE.TXT` y las licencias incluidas en el código fuente.

PPSSPP y esta adaptación se distribuyen bajo **GNU GPL versión 2 o posterior**. Dar crédito por sí solo no sustituye las obligaciones de licencia: el código fuente correspondiente, el parche y las instrucciones de compilación se publican con la APK. Se conservan los avisos de terceros. Se distribuye sin garantía, conforme a la licencia.

## Donaciones voluntarias

Si esta adaptación para OUYA te resulta útil, puedes apoyar voluntariamente su mantenimiento y las pruebas en hardware real:

- [Apoyar en Ko-fi](https://ko-fi.com/enmanuelyepez)
- [Apoyar en PayPal](https://paypal.me/EnmanuelFYepez)

Estos enlaces corresponden al mantenedor de esta adaptación, **emanueloutn**; no representan donaciones al equipo original de PPSSPP. La descarga es gratuita, donar no desbloquea funciones ni compra soporte o mejoras garantizadas. También puedes apoyar al proyecto original mediante los canales oficiales de https://www.ppsspp.org/.

## Código y contribuciones

Consulta `BUILD.md` y `controller-fix.patch`. El código fuente correspondiente se adjunta a cada release. No se publican claves privadas de firma, datos personales, configuraciones de la consola ni registros completos del dispositivo.

Para informar de un fallo, indica consola/firmware, juego y región, configuración, FPS, velocidad de emulación y pasos para reproducirlo. No incluyas contraseñas, cookies ni archivos de juegos.

English: unofficial OUYA-focused PPSSPP 1.17 community adaptation. Preserves upstream credits, fixes a JNI joystick array-reference leak affecting Dalvik, and documents tested settings. Optional donations support this fork's maintainer. No guaranteed FPS increase or universal compatibility.

Acceso OUYA corregido: se conserva MAIN + LAUNCHER y se elimina la categoría OUYA GAME del filtro principal para su inclusión como app instalada en MAKE → Software. La etiqueta de la consola es OUYA17. Cambio fechado el 15 de noviembre de 2026.
