"""
Base classes for LPCI attack vectors
Real attack implementations based on LPCI research
"""

import base64
import json
import logging
import random
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class AttackPayload:
    """Represents an LPCI attack payload"""
    id: str
    attack_vector: str
    payload_type: str
    content: str
    encoding: Optional[str] = None
    trigger_conditions: List[str] = None
    persistence_method: str = "session"
    risk_level: str = "medium"
    description: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.trigger_conditions is None:
            self.trigger_conditions = []
        if self.metadata is None:
            self.metadata = {}

@dataclass
class AttackResult:
    """Result of an attack execution"""
    payload_id: str
    success: bool
    response_content: str
    vulnerability_indicators: List[str]
    execution_time: float
    timestamp: datetime
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class BaseAttackVector(ABC):
    """Abstract base class for LPCI attack vectors"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"AttackVector.{name}")
        self.payload_history = []
    
    @abstractmethod
    def generate_payload(self, target_context: Dict[str, Any] = None) -> AttackPayload:
        """Generate an attack payload for this vector"""
        pass
    
    @abstractmethod
    def enhance_with_memory(self, base_payload: AttackPayload, 
                          memory_context: Dict[str, Any]) -> AttackPayload:
        """Enhance payload using memory context"""
        pass
    
    @abstractmethod
    def detect_success_indicators(self, response: str) -> List[str]:
        """Detect if the attack was successful based on response"""
        pass
    
    def encode_payload(self, payload: str, encoding_type: str = "base64") -> str:
        """Encode payload to evade detection"""
        if encoding_type == "base64":
            return base64.b64encode(payload.encode()).decode()
        elif encoding_type == "hex":
            return payload.encode().hex()
        elif encoding_type == "unicode":
            return ''.join(f'\\u{ord(c):04x}' for c in payload)
        elif encoding_type == "url":
            import urllib.parse
            return urllib.parse.quote(payload)
        else:
            return payload
    
    def create_trigger_condition(self, trigger_type: str) -> str:
        """Create trigger conditions for delayed execution"""
        triggers = {
            "keyword": ["when asked about", "if user mentions", "on receiving"],
            "role": ["as admin", "in developer mode", "when elevated"],
            "time": ["after session", "on next interaction", "during recall"],
            "context": ["in memory", "from vector store", "when retrieved"]
        }
        
        base_triggers = triggers.get(trigger_type, ["when triggered"])
        return random.choice(base_triggers)
    
    def obfuscate_payload(self, payload: str) -> str:
        """Apply obfuscation techniques to payload"""
        techniques = [
            self._comment_hiding,
            self._string_splitting,
            self._character_substitution,
            self._whitespace_manipulation
        ]
        
        chosen_technique = random.choice(techniques)
        return chosen_technique(payload)
    
    def _comment_hiding(self, payload: str) -> str:
        """Hide payload in comments"""
        return f"<!-- This is normal content -->\n{payload}\n<!-- End of content -->"
    
    def _string_splitting(self, payload: str) -> str:
        """Split payload across multiple strings"""
        mid_point = len(payload) // 2
        part1 = payload[:mid_point]
        part2 = payload[mid_point:]
        return f'"{part1}" + "{part2}"'
    
    def _character_substitution(self, payload: str) -> str:
        """Substitute characters with equivalents"""
        substitutions = {
            'a': 'а',  # Cyrillic a
            'e': 'е',  # Cyrillic e
            'o': 'о',  # Cyrillic o
            'p': 'р',  # Cyrillic p
        }
        
        result = payload
        for latin, cyrillic in substitutions.items():
            if latin in result:
                result = result.replace(latin, cyrillic, 1)  # Replace only first occurrence
        
        return result
    
    def _whitespace_manipulation(self, payload: str) -> str:
        """Manipulate whitespace to hide intent"""
        # Add zero-width spaces
        zero_width_space = '\u200b'
        words = payload.split()
        return zero_width_space.join(words)
    
    def create_persistence_payload(self, base_payload: str, method: str = "memory") -> str:
        """Create payload designed for persistence"""
        if method == "memory":
            return f"Remember this for future reference: {base_payload}"
        elif method == "vector_store":
            return f"Index this content: {base_payload}\n\nThis should be retrievable later."
        elif method == "session":
            return f"For this session: {base_payload}"
        elif method == "context":
            return f"Context note: {base_payload}"
        else:
            return base_payload
    
    def log_payload_generation(self, payload: AttackPayload):
        """Log payload generation for tracking"""
        self.payload_history.append({
            "id": payload.id,
            "timestamp": datetime.now().isoformat(),
            "payload_type": payload.payload_type,
            "risk_level": payload.risk_level
        })
        
        self.logger.info(f"Generated {payload.attack_vector} payload: {payload.id}")

class AttackVectorRegistry:
    """Registry for managing attack vectors"""
    
    def __init__(self):
        self._vectors = {}
        self.logger = logging.getLogger("AttackVectorRegistry")
    
    def register_vector(self, vector: BaseAttackVector):
        """Register an attack vector"""
        self._vectors[vector.name] = vector
        self.logger.info(f"Registered attack vector: {vector.name}")
    
    def get_vector(self, name: str) -> Optional[BaseAttackVector]:
        """Get attack vector by name"""
        return self._vectors.get(name)
    
    def get_all_vectors(self) -> Dict[str, BaseAttackVector]:
        """Get all registered vectors"""
        return self._vectors.copy()
    
    def generate_payload_for_vector(self, vector_name: str, 
                                  context: Dict[str, Any] = None) -> Optional[AttackPayload]:
        """Generate payload for specific vector"""
        vector = self.get_vector(vector_name)
        if vector:
            return vector.generate_payload(context)
        return None
    
    def get_supported_vectors(self) -> List[str]:
        """Get list of supported attack vector names"""
        return list(self._vectors.keys())

# Global registry instance
attack_registry = AttackVectorRegistry()