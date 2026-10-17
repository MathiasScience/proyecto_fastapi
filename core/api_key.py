import hashlib
import hmac
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException, Header, Request, status


load_dotenv()
load_dotenv()

class APIKeyConfig:
    """Configuración centralizada para API Keys"""
    API_KEY: str = os.getenv("API_KEY", "")
    API_KEY_HEADER_NAME: str = os.getenv("API_KEY_HEADER_NAME", "Api-Key")
    ENABLE_API_KEY_VALIDATION: bool = os.getenv("ENABLE_API_KEY_VALIDATION", "true").lower() == "true"


class APIKeyValidator:
    """Validador mejorado para API Keys"""

    @staticmethod
    def _secure_compare(key1: str, key2: str) -> bool:
        """Comparación segura de API keys para prevenir timing attacks"""
        if not key1 or not key2:
            return False

        # Usar hmac.compare_digest para comparación segura
        return hmac.compare_digest(key1.encode(), key2.encode())

    @staticmethod
    def _hash_api_key(api_key: str) -> str:
        """Genera hash de la API key para logs seguros"""
        return hashlib.sha256(api_key.encode()).hexdigest()[:8]


def validar_api_key(
        request: Request,
        api_key: Optional[str] = Header(None, alias=APIKeyConfig.API_KEY_HEADER_NAME)
) -> str:
    """
    Valida la API key enviada en los headers de la solicitud.

    Args:
        request: Objeto de solicitud HTTP
        api_key: API key enviada en el header

    Returns:
        str: API key validada

    Raises:
        HTTPException: Si la API key es inválida o faltante
    """
    # Si la validación está deshabilitada (para desarrollo)
    if not APIKeyConfig.ENABLE_API_KEY_VALIDATION:
#        logger.warning("⚠️ Validación de API Key deshabilitada")
        return "development-mode"

    # Verificar si existe API key configurada
    if not APIKeyConfig.API_KEY:
#        logger.error("❌ API Key no configurada en variables de entorno")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de configuración del servidor"
        )

    # Verificar si se envió API key
    if not api_key:
#        logger.warning(f"🚫 Solicitud sin API Key desde IP: {request.client.host}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key requerida",
            headers={"WWW-Authenticate": "ApiKey"}
        )

    # Validar API key
    if not APIKeyValidator._secure_compare(api_key, APIKeyConfig.API_KEY):
        # Log con hash parcial para seguridad
        api_key_hash = APIKeyValidator._hash_api_key(api_key)
#        logger.warning(
#            f"🚫 API Key inválida desde IP: {request.client.host}, "
#            f"Hash parcial: {api_key_hash}"
#        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida"
        )

#    logger.debug(f"✔️ API Key válida desde IP: {request.client.host}")
    return api_key


# Función de compatibilidad con versión anterior
def validar_api_key_legacy(api_key: str = Header(None)) -> None:
    """Función legacy para compatibilidad hacia atrás"""
    if api_key != APIKeyConfig.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clave API inválida o faltante"
        )