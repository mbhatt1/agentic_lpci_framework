"""
LPCI Attack Vectors Module
Real implementations of Logic-layer Prompt Control Injection attacks
"""

from .base import (AttackPayload, AttackResult, AttackVectorRegistry,
                   BaseAttackVector, attack_registry)
from .lpci_core import LPCICoreAttack
from .role_override import RoleOverrideAttack
from .tool_poisoning import ToolPoisoningAttack
from .vector_store_payload import VectorStorePayloadAttack

__all__ = [
    "BaseAttackVector",
    "AttackPayload", 
    "AttackResult",
    "AttackVectorRegistry",
    "attack_registry",
    "ToolPoisoningAttack",
    "LPCICoreAttack", 
    "RoleOverrideAttack",
    "VectorStorePayloadAttack"
]

# All attack vectors are automatically registered via their module imports
SUPPORTED_ATTACK_VECTORS = [
    "tool_poisoning",
    "lpci_core", 
    "role_override",
    "vector_store_payload"
]

def get_all_attack_vectors():
    """Get all registered attack vectors"""
    return attack_registry.get_all_vectors()

def generate_attack_payload(vector_name: str, context: dict = None):
    """Generate attack payload for specific vector"""
    return attack_registry.generate_payload_for_vector(vector_name, context)

def get_supported_vectors():
    """Get list of supported attack vector names"""
    return attack_registry.get_supported_vectors()