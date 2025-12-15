# Plan de Implementación - Prueba de Fuego Veo3

- [ ] 1. Configurar estructura de pruebas y dependencias
  - Crear directorio `tests/` con subdirectorios para unit, integration, properties, y e2e
  - Crear archivo `requirements-test.txt` con pytest, hypothesis, pytest-cov, pytest-mock, responses
  - Crear archivo `tests/conftest.py` con fixtures compartidos
  - Crear directorio `tests/fixtures/` para datos de prueba
  - _Requirements: 6.1, 6.2, 6.5_

- [ ] 2. Implementar módulo de configuración de pruebas
  - Crear `tests/test_config.py` con clase TestConfig
  - Implementar método `get_test_api_key()` que retorna API key de prueba
  - Implementar método `get_test_image_path()` que retorna path a imagen de prueba
  - Implementar método `create_test_image()` que genera imágenes temporales en diferentes formatos
  - _Requirements: 1.1, 1.2, 2.1, 2.2_

- [ ] 3. Implementar mocks de la API de Gemini
  - Crear `tests/test_mocks.py` con clase MockGenAIClient
  - Implementar MockOperation que simula operaciones asíncronas
  - Implementar MockResponse con datos de video simulados
  - Agregar soporte para simular diferentes estados (éxito, error, timeout)
  - _Requirements: 6.2_

- [ ] 4. Implementar clases de error personalizadas
  - Crear archivo `veo_errors.py` con jerarquía de excepciones
  - Implementar Veo3Error como clase base
  - Implementar ConfigurationError, APIError, ValidationError
  - Agregar atributos útiles para debugging (status_code, context)
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 5. Refactorizar veo_generator.py para mejor testabilidad
  - Extraer función `load_api_key()` que maneja carga desde env y .env
  - Extraer función `validate_parameters()` que valida parámetros antes de llamar API
  - Agregar manejo de errores con excepciones personalizadas
  - Agregar timeout configurable para polling
  - _Requirements: 1.1, 1.2, 1.3, 4.5_

- [ ] 6. Implementar pruebas unitarias de carga de API key
  - Crear `tests/unit/test_api_key.py`
  - Implementar test para carga desde variable de entorno
  - Implementar test para carga desde archivo .env
  - Implementar test para error cuando falta API key
  - _Requirements: 1.1, 1.2, 1.3_

- [ ]* 6.1 Implementar property test para carga de configuración
  - **Property 1: Configuration loading consistency**
  - **Validates: Requirements 1.1, 1.2**

- [ ]* 6.2 Implementar property test para detección de API keys inválidas
  - **Property 2: Invalid API key detection**
  - **Validates: Requirements 1.5**

- [ ] 7. Implementar pruebas unitarias de carga de imágenes
  - Crear `tests/unit/test_image_loading.py`
  - Implementar test para carga de imagen JPEG
  - Implementar test para carga de imagen PNG
  - Implementar test para FileNotFoundError con archivo inexistente
  - Implementar test para detección de tipo MIME
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ]* 7.1 Implementar property test para carga de imágenes
  - **Property 3: Image format loading consistency**
  - **Validates: Requirements 2.1, 2.2**

- [ ]* 7.2 Implementar property test para detección de MIME type
  - **Property 4: MIME type detection accuracy**
  - **Validates: Requirements 2.4**

- [ ] 8. Implementar pruebas unitarias de validación de parámetros
  - Crear `tests/unit/test_validation.py`
  - Implementar test para validación de parámetros completos
  - Implementar test para rechazo cuando faltan parámetros requeridos
  - Implementar test para validación de aspect ratio
  - Implementar test para validación de duración
  - _Requirements: 4.5_

- [ ]* 8.1 Implementar property test para validación de parámetros
  - **Property 13: Parameter validation before API call**
  - **Validates: Requirements 4.5**

- [ ] 9. Implementar pruebas de integración con API mockeada
  - Crear `tests/integration/test_generation.py`
  - Implementar test de generación exitosa con mock
  - Implementar test de manejo de error de API
  - Implementar test de manejo de respuesta malformada
  - _Requirements: 3.1, 4.2, 4.4_

- [ ]* 9.1 Implementar property test para solicitudes válidas
  - **Property 5: Valid request returns operation**
  - **Validates: Requirements 3.1**

- [ ]* 9.2 Implementar property test para extracción de mensajes de error
  - **Property 11: API error message extraction**
  - **Validates: Requirements 4.2**

- [ ]* 9.3 Implementar property test para manejo de respuestas malformadas
  - **Property 12: Malformed response handling**
  - **Validates: Requirements 4.4**

- [ ] 10. Implementar pruebas de polling
  - Crear `tests/integration/test_polling.py`
  - Implementar test de polling que completa después de N iteraciones
  - Implementar test de timeout cuando polling excede límite
  - Implementar test de obtención de URI después de completar
  - _Requirements: 3.2, 3.3, 4.3_

- [ ]* 10.1 Implementar property test para garantía de completado de polling
  - **Property 6: Polling completion guarantee**
  - **Validates: Requirements 3.2**

- [ ]* 10.2 Implementar property test para obtención de URI
  - **Property 7: Successful operation yields video URI**
  - **Validates: Requirements 3.3**

- [ ] 11. Implementar pruebas de descarga y validación de video
  - Crear `tests/integration/test_video_download.py`
  - Implementar test de descarga de video desde URI mockeada
  - Implementar test de validación de archivo MP4
  - Implementar test de verificación de tamaño de archivo
  - _Requirements: 3.4_

- [ ]* 11.1 Implementar property test para validez de archivos descargados
  - **Property 8: Downloaded video file validity**
  - **Validates: Requirements 3.4**

- [ ]* 11.2 Implementar property test para preservación de parámetros de configuración
  - **Property 9: Configuration parameter preservation**
  - **Validates: Requirements 3.5, 3.6**

- [ ] 12. Implementar pruebas de manejo de errores de red
  - Crear `tests/integration/test_error_handling.py`
  - Implementar test de manejo de timeout de conexión
  - Implementar test de manejo de error DNS
  - Implementar test de manejo de error SSL
  - Verificar que todos los errores muestran mensajes descriptivos
  - _Requirements: 4.1_

- [ ]* 12.1 Implementar property test para manejo de errores de red
  - **Property 10: Network error handling**
  - **Validates: Requirements 4.1**

- [ ] 13. Checkpoint - Asegurar que todas las pruebas pasan
  - Ejecutar `pytest tests/unit tests/integration tests/properties -v`
  - Verificar que no hay fallos
  - Si hay problemas, preguntar al usuario

- [ ]* 14. Implementar prueba end-to-end opcional
  - Crear `tests/e2e/test_full_flow.py`
  - Marcar con `@pytest.mark.slow` y `@pytest.mark.requires_api`
  - Implementar test que ejecuta flujo completo con API real
  - Verificar que genera archivo de video válido
  - Medir y reportar tiempo de ejecución
  - Validar que archivo existe y tiene tamaño > 0
  - Implementar manejo de fallos con reporte de etapa
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 15. Crear script de smoke test runner
  - Crear `smoke_test.py` en la raíz del proyecto
  - Implementar función `run_smoke_tests()` que ejecuta pytest programáticamente
  - Agregar opción `--include-e2e` para incluir prueba end-to-end
  - Implementar clase TestResults para almacenar resultados
  - Generar reporte legible con resumen de éxitos/fallos
  - Calcular y mostrar porcentaje de éxito
  - _Requirements: 6.3, 6.4_

- [ ] 16. Crear fixtures de datos de prueba
  - Generar `tests/fixtures/test_image.jpg` (imagen pequeña 100x100)
  - Generar `tests/fixtures/test_image.png` (imagen pequeña 100x100)
  - Crear `tests/fixtures/test_image_corrupted.jpg` (archivo corrupto para testing)
  - Documentar fixtures en `tests/fixtures/README.md`
  - _Requirements: 2.1, 2.2, 2.5_

- [ ] 17. Configurar pytest y cobertura
  - Crear `pytest.ini` con configuración de markers (slow, requires_api)
  - Crear `.coveragerc` con configuración de cobertura
  - Agregar script en README para ejecutar pruebas
  - Documentar cómo ejecutar diferentes tipos de pruebas
  - _Requirements: 6.1, 6.3_

- [ ]* 18. Crear documentación de pruebas
  - Crear `tests/README.md` explicando estructura de pruebas
  - Documentar cómo ejecutar cada tipo de prueba
  - Documentar cómo agregar nuevas pruebas
  - Incluir ejemplos de property tests y unit tests
  - _Requirements: 6.3, 6.4_

- [ ] 19. Checkpoint final - Ejecutar suite completa
  - Ejecutar `pytest tests/ -v --cov=veo_generator --cov-report=html`
  - Verificar cobertura > 80%
  - Ejecutar smoke_test.py y verificar reporte
  - Si hay problemas, preguntar al usuario
