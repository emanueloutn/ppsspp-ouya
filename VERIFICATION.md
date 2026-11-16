# Verificación de 1.17-ouya.1

- Hardware de prueba: OUYA, Android 4.1.2, Tegra 3 / ARMv7.
- El cierre original mostró ReferenceTable overflow (max=1024), una tabla de arreglos JNI retenidos, y la traza de joystickAxis. La fuente base obtenía dos arreglos sin liberarlos.
- La función corregida se compiló en un arnés independiente y procesó 20.000 llamadas sintéticas sobre Dalvik real. Se validaron datos y rechazo de valores inválidos. NativeAxis se sustituyó en esa prueba por un receptor de prueba; no es una sesión completa de juego.
- Se compiló el núcleo del emulador en Release para ARMv7/API 16, se verificó la firma y se instaló en la OUYA.
- Se comprobó que la biblioteca nativa del APK público es idéntica a la biblioteca corregida probada. Los cambios posteriores al contenedor añaden licencia/créditos y corrigen la clasificación del acceso.
- Se verificó el acceso en MAKE → Software → OUYA17 → LAUNCH, con navegación por teclas del mando y confirmación de que se abrió la actividad de la adaptación. No se usó un inicio directo del componente para esa comprobación.
- GTA: Liberty City Stories USA v1.05 arrancó. El usuario informó de juego ya jugable y audio satisfactorio; 96–102 % de velocidad de emulación y, dependiendo de la escena y salto de cuadros, unos 15–20 FPS en exteriores y hasta 30 en zonas ligeras. No es una comparación controlada ni una mejora garantizada del motor.
- Desactivar el salto de cuadros redujo aproximadamente al 50 % la velocidad en una prueba. Omitir efectos de búfer dejó la pantalla negra y se revirtió. Resolución 2x redujo el rendimiento frente a 1x.

No se garantiza estabilidad absoluta, 30 FPS constantes ni igual comportamiento en otros juegos. La prueba del acceso no implica que todos los mandos o firmwares sean compatibles. Los juegos, partidas y registros completos de la consola no forman parte de esta publicación.
