# Perfil probado en OUYA

En PPSSPP / OUYA17, configura estos ajustes. Los nombres pueden variar según el idioma.

| Ajuste | Valor |
|---|---|
| Backend | OpenGL |
| Resolución de renderizado | 1x PSP |
| Filtrado de pantalla | Vecino más cercano |
| Transformación por hardware | Activada |
| Software skinning | Desactivado |
| Salto de cuadros | 1 |
| Salto automático | Activado |
| CPU emulada | Automática / 0 |
| Escalado de texturas | Desactivado / 1x |
| Reemplazo de texturas | Desactivado |
| Posprocesado | Desactivado |
| Omitir efectos de búfer | Desactivado |
| Registros de depuración | Desactivados |
| Contador | FPS y porcentaje de velocidad |

No sobrescribas un ppsspp.ini completo de otra persona: puede contener rutas, datos de red, preferencias o controles distintos. Estos valores no están incrustados como nuevos valores predeterminados en la APK y no garantizan el mismo resultado en todos los juegos.

En la prueba con GTA: Liberty City Stories, desactivar completamente el salto de cuadros redujo la velocidad aproximadamente al 50 %. Omitir efectos de búfer produjo pantalla negra. Se restauraron los ajustes anteriores.
