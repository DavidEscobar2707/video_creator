# Documento de Diseño - Prueba de Fuego Veo3

## Overview

Este diseño describe una suite de pruebas de fuego para el generador de videos Veo3. La suite incluye pruebas unitarias para componentes individuales, pruebas de integración con mocks de la API, y una prueba end-to-end opcional que valida el flujo completo con la API real. El diseño prioriza velocidad de ejecución, claridad en los reportes, y facilidad de mantenimiento.

## Architecture

La arquitectura de pruebas sigue un patrón de tres capas:

```
┌─────────────────────────────────────┐
│   Test Runner (pytest)              │
│   - Descubrimiento automático       │
│   - Reportes y fixtures             │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│   Test Suites                       │
│   - Unit Tests (rápidos)            │
│   - Integration Tests (con mocks)   │
│   - E2E Tests (opcionales)          │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│   Sistema Bajo Prueba               │
│   - veo_generator.py                │
│   - Configuración de API            │
│   - Utilidades de carga             │
└─────────────────────────────────────┘
```

### Principios de Diseño

1. **Aislamiento**: Las pruebas unitarias no deben depender de la API real
2. **Velocidad**: Las pruebas rápidas se ejecutan primero
3. **Claridad**: Cada prueba tiene un propósito único y claro
4. **Reproducibilidad**: Las pruebas producen resultados consistentes
5. **Feedback útil**: Los fallos proporcionan información accionable

## Components and Interfaces

### 1. Test Configuration Module (`test_config.py`)

Maneja la configuración compartida entre todas las pruebas.

```python
class TestConfig:
    """Configuración centralizada para las pruebas"""
    
    @staticmethod
    def get_test_api_key() -> str:
        """Obtiene API key para pruebas"""
        
    @staticmethod
    def get_test_image_path() -> str:
        """Retorna path a imagen de prueba"""
        
    @staticmethod
    def create_test_image(format: str = "jpeg") -> str:
        """Crea una imagen de prueba temporal"""
```

### 2. API Mock Module (`test_mocks.py`)

Proporciona mocks de la API de Gemini para pruebas de integración.

```python
class MockGenAIClient:
    """Mock del cliente de Gemini API"""
    
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail
        
    def models.generate_videos(self, **kwargs) -> MockOperation:
        """Simula generación de video"""
        
class MockOperation:
    """Mock de operación asíncrona"""
    
    def __init__(self, done: bool = False):
        self.done = done
        self.response = MockResponse()
```

### 3. Unit Test Suite (`test_unit.py`)

Pruebas unitarias para funciones individuales.

```python
class TestAPIKeyLoading:
    """Pruebas de carga de API key"""
    
    def test_load_from_env(self):
        """Valida carga desde variable de entorno"""
        
    def test_load_from_dotenv(self):
        """Valida carga desde archivo .env"""
        
    def test_missing_api_key(self):
        """Valida error cuando falta API key"""

class TestImageLoading:
    """Pruebas de carga de imágenes"""
    
    def test_load_jpeg(self):
        """Valida carga de imagen JPEG"""
        
    def test_load_png(self):
        """Valida carga de imagen PNG"""
        
    def test_file_not_found(self):
        """Valida error con archivo inexistente"""
        
    def test_mime_type_detection(self):
        """Valida detección correcta de tipo MIME"""
```

### 4. Integration Test Suite (`test_integration.py`)

Pruebas de integración usando mocks de la API.

```python
class TestVideoGeneration:
    """Pruebas de generación con API mockeada"""
    
    def test_successful_generation(self):
        """Valida flujo exitoso de generación"""
        
    def test_polling_mechanism(self):
        """Valida que el polling funciona correctamente"""
        
    def test_video_download(self):
        """Valida descarga del video generado"""
```

### 5. End-to-End Test Suite (`test_e2e.py`)

Prueba completa con la API real (opcional, marcada con pytest.mark.slow).

```python
@pytest.mark.slow
@pytest.mark.requires_api
class TestEndToEnd:
    """Prueba completa del flujo"""
    
    def test_full_video_generation(self):
        """Ejecuta generación completa de video"""
```

### 6. Smoke Test Runner (`smoke_test.py`)

Script principal que ejecuta las pruebas de fuego.

```python
def run_smoke_tests(include_e2e: bool = False) -> TestResults:
    """
    Ejecuta suite de pruebas de fuego
    
    Args:
        include_e2e: Si True, incluye prueba end-to-end con API real
        
    Returns:
        TestResults con resumen de ejecución
    """
```

## Data Models

### TestResults

```python
@dataclass
class TestResults:
    """Resultados de ejecución de pruebas"""
    total: int
    passed: int
    failed: int
    skipped: int
    duration_seconds: float
    failures: List[TestFailure]
    
    def success_rate(self) -> float:
        """Calcula porcentaje de éxito"""
        return (self.passed / self.total) * 100 if self.total > 0 else 0
```

### TestFailure

```python
@dataclass
class TestFailure:
    """Información de una prueba fallida"""
    test_name: str
    error_message: str
    traceback: str
    stage: str  # 'setup', 'execution', 'teardown'
```

### MockVideoResponse

```python
@dataclass
class MockVideoResponse:
    """Respuesta mockeada de la API"""
    video_uri: str
    video_bytes: bytes
    duration_seconds: int
    aspect_ratio: str
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Configuration loading consistency
*For any* valid configuration source (environment variable or .env file) containing an API key, loading the configuration should return the exact value that was set
**Validates: Requirements 1.1, 1.2**

### Property 2: Invalid API key detection
*For any* string that is not a valid Gemini API key format, attempting to initialize the client should result in an authentication error being detected
**Validates: Requirements 1.5**

### Property 3: Image format loading consistency
*For any* valid image file in a supported format (JPEG, PNG, WebP), loading the image should successfully read the bytes and the byte count should match the file size
**Validates: Requirements 2.1, 2.2**

### Property 4: MIME type detection accuracy
*For any* image file with a known format, the detected MIME type should correctly correspond to the actual file format
**Validates: Requirements 2.4**

### Property 5: Valid request returns operation
*For any* valid combination of image, prompt, and configuration parameters, sending a generation request should return an Operation object
**Validates: Requirements 3.1**

### Property 6: Polling completion guarantee
*For any* operation that eventually completes, the polling mechanism should continue checking until the operation is marked as done
**Validates: Requirements 3.2**

### Property 7: Successful operation yields video URI
*For any* operation that completes successfully, the response should contain a valid video URI
**Validates: Requirements 3.3**

### Property 8: Downloaded video file validity
*For any* video downloaded from a valid URI, the saved file should exist, have non-zero size, and be a valid MP4 file
**Validates: Requirements 3.4**

### Property 9: Configuration parameter preservation
*For any* requested aspect ratio and duration within valid limits, the generated video metadata should reflect the requested configuration
**Validates: Requirements 3.5, 3.6**

### Property 10: Network error handling
*For any* network error that occurs during API communication, the system should catch the exception and provide a descriptive error message without crashing
**Validates: Requirements 4.1**

### Property 11: API error message extraction
*For any* error response from the API, the system should extract and display the error message from the API response
**Validates: Requirements 4.2**

### Property 12: Malformed response handling
*For any* API response with unexpected format or missing fields, the system should handle the error gracefully without crashing
**Validates: Requirements 4.4**

### Property 13: Parameter validation before API call
*For any* request missing required parameters, the system should validate and reject the request before making an API call
**Validates: Requirements 4.5**

## Error Handling

### Error Categories

1. **Configuration Errors**
   - Missing API key
   - Invalid API key format
   - Malformed .env file

2. **File System Errors**
   - Image file not found
   - Insufficient permissions
   - Corrupted image files
   - Disk space issues during video save

3. **API Errors**
   - Authentication failures
   - Rate limiting
   - Invalid parameters
   - Service unavailable
   - Malformed responses

4. **Network Errors**
   - Connection timeout
   - DNS resolution failures
   - SSL/TLS errors

5. **Validation Errors**
   - Missing required parameters
   - Invalid parameter values
   - Unsupported image formats

### Error Handling Strategy

Cada categoría de error debe:

1. **Capturar** la excepción específica
2. **Registrar** información detallada para debugging
3. **Transformar** en un mensaje claro para el usuario
4. **Propagar** o manejar según el contexto

```python
class Veo3Error(Exception):
    """Clase base para errores del sistema"""
    pass

class ConfigurationError(Veo3Error):
    """Error de configuración"""
    pass

class APIError(Veo3Error):
    """Error de la API de Gemini"""
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        super().__init__(message)

class ValidationError(Veo3Error):
    """Error de validación de parámetros"""
    pass
```

### Retry Strategy

Para errores transitorios (red, rate limiting):

- Máximo 3 reintentos
- Backoff exponencial: 1s, 2s, 4s
- Solo para errores recuperables (5xx, timeouts)
- No reintentar errores de autenticación o validación

## Testing Strategy

### Dual Testing Approach

Este proyecto utiliza tanto pruebas unitarias como property-based testing para asegurar corrección completa:

- **Unit tests**: Verifican ejemplos específicos, casos edge, y condiciones de error
- **Property tests**: Verifican propiedades universales que deben cumplirse para todas las entradas

Juntas proporcionan cobertura completa: los unit tests capturan bugs concretos, los property tests verifican corrección general.

### Property-Based Testing

**Framework**: Utilizaremos `hypothesis` para Python, la biblioteca estándar de property-based testing.

**Configuración**:
- Cada property test debe ejecutar mínimo 100 iteraciones
- Cada property test debe estar etiquetado con un comentario que referencie explícitamente la propiedad de corrección del documento de diseño
- Formato del tag: `# Feature: veo3-smoke-test, Property {número}: {texto de la propiedad}`

**Ejemplo de property test**:

```python
from hypothesis import given, strategies as st

# Feature: veo3-smoke-test, Property 1: Configuration loading consistency
@given(api_key=st.text(min_size=10, max_size=100))
def test_config_loading_consistency(api_key):
    """Para cualquier API key válida, cargar configuración debe retornar el valor exacto"""
    # Setup: configurar variable de entorno
    os.environ['GEMINI_API_KEY'] = api_key
    
    # Execute: cargar configuración
    loaded_key = load_api_key()
    
    # Assert: debe ser el mismo valor
    assert loaded_key == api_key
```

### Unit Testing

Los unit tests cubren:

- **Ejemplos específicos**: Casos de uso comunes y esperados
- **Edge cases**: Archivos vacíos, strings vacíos, límites de parámetros
- **Casos de error**: Archivos inexistentes, API keys inválidas, timeouts

**Ejemplo de unit test**:

```python
def test_load_missing_image():
    """Verificar que cargar imagen inexistente genera FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        load_image_bytes("nonexistent.jpg")
```

### Test Organization

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartidos
├── test_config.py           # Configuración de pruebas
├── test_mocks.py            # Mocks de la API
├── unit/
│   ├── test_api_key.py      # Pruebas de carga de API key
│   ├── test_image_loading.py # Pruebas de carga de imágenes
│   └── test_validation.py   # Pruebas de validación
├── integration/
│   ├── test_generation.py   # Pruebas con API mockeada
│   └── test_polling.py      # Pruebas de polling
├── properties/
│   ├── test_config_properties.py    # Property tests de configuración
│   ├── test_image_properties.py     # Property tests de imágenes
│   └── test_generation_properties.py # Property tests de generación
└── e2e/
    └── test_full_flow.py    # Prueba end-to-end (opcional)
```

### Test Execution

```bash
# Ejecutar solo pruebas rápidas (unit + property tests)
pytest tests/ -m "not slow"

# Ejecutar todas las pruebas incluyendo E2E
pytest tests/

# Ejecutar solo property tests
pytest tests/properties/

# Ejecutar con cobertura
pytest tests/ --cov=veo_generator --cov-report=html
```

### Mocking Strategy

Para pruebas de integración, mockearemos:

1. **genai.Client**: Mock completo del cliente de Gemini
2. **Operation polling**: Simular operaciones que completan después de N iteraciones
3. **Video download**: Retornar bytes de video simulados
4. **Network calls**: Usar `responses` o `httpretty` para mockear requests HTTP

No mockearemos en property tests cuando sea posible, para mantener las pruebas simples y cercanas al comportamiento real.

### Success Criteria

Las pruebas se consideran exitosas cuando:

1. ✅ Todas las property tests pasan con 100+ iteraciones
2. ✅ Todos los unit tests pasan
3. ✅ Cobertura de código > 80%
4. ✅ Tiempo de ejecución de pruebas rápidas < 10 segundos
5. ✅ Prueba E2E opcional pasa (cuando se ejecuta)

## Implementation Notes

### Dependencies

```python
# requirements-test.txt
pytest>=7.0.0
pytest-cov>=4.0.0
hypothesis>=6.0.0
pytest-mock>=3.10.0
responses>=0.23.0
```

### Test Data

Crear directorio `tests/fixtures/` con:
- `test_image.jpg`: Imagen JPEG pequeña (100x100)
- `test_image.png`: Imagen PNG pequeña (100x100)
- `test_video.mp4`: Video MP4 pequeño para validación

### CI/CD Integration

Las pruebas deben integrarse en CI/CD:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: pytest tests/ -m "not slow" --cov
```

### Performance Considerations

- Las pruebas unitarias deben completarse en < 5 segundos
- Las property tests pueden tomar hasta 30 segundos (100 iteraciones por propiedad)
- La prueba E2E puede tomar 30-60 segundos (depende de la API)
- Usar `pytest-xdist` para paralelizar pruebas si es necesario

### Maintenance

- Actualizar mocks cuando la API de Gemini cambie
- Revisar property tests si se agregan nuevas funcionalidades
- Mantener imágenes de prueba pequeñas (< 50KB)
- Documentar cualquier quirk o comportamiento inesperado de la API
