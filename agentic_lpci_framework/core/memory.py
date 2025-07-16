"""
Memory Management System for Agentic LPCI Testing Framework
Handles conversation history, agent state, and test result persistence
"""

import json
import sqlite3
import threading
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ConversationMessage:
    """Represents a single message in a conversation"""
    id: str
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConversationMessage':
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

@dataclass
class AgentState:
    """Represents the current state of an agent"""
    agent_id: str
    name: str
    role: str
    capabilities: List[str]
    memory_context: Dict[str, Any]
    current_task: Optional[str] = None
    active_since: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        if self.active_since:
            data['active_since'] = self.active_since.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentState':
        if data.get('active_since'):
            data['active_since'] = datetime.fromisoformat(data['active_since'])
        return cls(**data)

@dataclass
class TestResult:
    """Represents the result of an LPCI test execution"""
    test_id: str
    model_name: str
    attack_vector: str
    payload: str
    result: str  # 'blocked', 'executed', 'warning'
    vulnerability_exposed: bool
    execution_time: float
    timestamp: datetime
    session_id: str
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TestResult':
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

class MemoryManager:
    """
    Centralized memory management system for the agentic framework
    Supports persistent storage and retrieval of conversations, agent states, and test results
    """
    
    def __init__(self, db_path: str = "lpci_framework.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp TEXT,
                    metadata TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS agent_states (
                    agent_id TEXT PRIMARY KEY,
                    name TEXT,
                    role TEXT,
                    capabilities TEXT,
                    memory_context TEXT,
                    current_task TEXT,
                    active_since TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    test_id TEXT PRIMARY KEY,
                    model_name TEXT,
                    attack_vector TEXT,
                    payload TEXT,
                    result TEXT,
                    vulnerability_exposed BOOLEAN,
                    execution_time REAL,
                    timestamp TEXT,
                    session_id TEXT,
                    metadata TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at TEXT,
                    description TEXT,
                    status TEXT,
                    metadata TEXT
                )
            ''')
    
    def create_session(self, description: str = "") -> str:
        """Create a new session and return its ID"""
        session_id = str(uuid.uuid4())
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO sessions (session_id, created_at, description, status, metadata)
                    VALUES (?, ?, ?, ?, ?)
                ''', (session_id, datetime.now().isoformat(), description, "active", "{}"))
        return session_id
    
    def store_conversation_message(self, session_id: str, message: ConversationMessage):
        """Store a conversation message in memory"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO conversations (id, session_id, role, content, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    message.id,
                    session_id,
                    message.role,
                    message.content,
                    message.timestamp.isoformat(),
                    json.dumps(message.metadata or {})
                ))
    
    def get_conversation_history(self, session_id: str, limit: int = 100) -> List[ConversationMessage]:
        """Retrieve conversation history for a session"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT id, role, content, timestamp, metadata
                    FROM conversations
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (session_id, limit))
                
                messages = []
                for row in cursor.fetchall():
                    msg = ConversationMessage(
                        id=row[0],
                        role=row[1],
                        content=row[2],
                        timestamp=datetime.fromisoformat(row[3]),
                        metadata=json.loads(row[4])
                    )
                    messages.append(msg)
                
                return list(reversed(messages))
    
    def store_agent_state(self, agent_state: AgentState):
        """Store or update an agent's state"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO agent_states 
                    (agent_id, name, role, capabilities, memory_context, current_task, active_since)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    agent_state.agent_id,
                    agent_state.name,
                    agent_state.role,
                    json.dumps(agent_state.capabilities),
                    json.dumps(agent_state.memory_context),
                    agent_state.current_task,
                    agent_state.active_since.isoformat() if agent_state.active_since else None
                ))
    
    def get_agent_state(self, agent_id: str) -> Optional[AgentState]:
        """Retrieve an agent's current state"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT agent_id, name, role, capabilities, memory_context, current_task, active_since
                    FROM agent_states
                    WHERE agent_id = ?
                ''', (agent_id,))
                
                row = cursor.fetchone()
                if row:
                    return AgentState(
                        agent_id=row[0],
                        name=row[1],
                        role=row[2],
                        capabilities=json.loads(row[3]),
                        memory_context=json.loads(row[4]),
                        current_task=row[5],
                        active_since=datetime.fromisoformat(row[6]) if row[6] else None
                    )
                return None
    
    def store_test_result(self, result: TestResult):
        """Store a test result"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO test_results 
                    (test_id, model_name, attack_vector, payload, result, vulnerability_exposed, 
                     execution_time, timestamp, session_id, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    result.test_id,
                    result.model_name,
                    result.attack_vector,
                    result.payload,
                    result.result,
                    result.vulnerability_exposed,
                    result.execution_time,
                    result.timestamp.isoformat(),
                    result.session_id,
                    json.dumps(result.metadata or {})
                ))
    
    def get_test_results(self, model_name: str = None, attack_vector: str = None, 
                        session_id: str = None) -> List[TestResult]:
        """Retrieve test results with optional filtering"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                query = '''
                    SELECT test_id, model_name, attack_vector, payload, result, vulnerability_exposed,
                           execution_time, timestamp, session_id, metadata
                    FROM test_results
                    WHERE 1=1
                '''
                params = []
                
                if model_name:
                    query += ' AND model_name = ?'
                    params.append(model_name)
                
                if attack_vector:
                    query += ' AND attack_vector = ?'
                    params.append(attack_vector)
                
                if session_id:
                    query += ' AND session_id = ?'
                    params.append(session_id)
                
                query += ' ORDER BY timestamp DESC'
                
                cursor = conn.execute(query, params)
                results = []
                
                for row in cursor.fetchall():
                    result = TestResult(
                        test_id=row[0],
                        model_name=row[1],
                        attack_vector=row[2],
                        payload=row[3],
                        result=row[4],
                        vulnerability_exposed=bool(row[5]),
                        execution_time=row[6],
                        timestamp=datetime.fromisoformat(row[7]),
                        session_id=row[8],
                        metadata=json.loads(row[9])
                    )
                    results.append(result)
                
                return results
    
    def get_memory_context(self, session_id: str, context_type: str = "conversation") -> Dict[str, Any]:
        """Retrieve memory context for an agent or session"""
        if context_type == "conversation":
            messages = self.get_conversation_history(session_id)
            return {
                "messages": [msg.to_dict() for msg in messages],
                "message_count": len(messages),
                "last_updated": datetime.now().isoformat()
            }
        
        elif context_type == "test_results":
            results = self.get_test_results(session_id=session_id)
            return {
                "results": [result.to_dict() for result in results],
                "total_tests": len(results),
                "success_rate": sum(1 for r in results if not r.vulnerability_exposed) / len(results) if results else 0,
                "last_updated": datetime.now().isoformat()
            }
        
        return {}
    
    def clear_session(self, session_id: str):
        """Clear all data for a specific session"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
                conn.execute('DELETE FROM test_results WHERE session_id = ?', (session_id,))
                conn.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics from memory"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                stats = {}
                
                # Total conversations
                cursor = conn.execute('SELECT COUNT(*) FROM conversations')
                stats['total_messages'] = cursor.fetchone()[0]
                
                # Total test results
                cursor = conn.execute('SELECT COUNT(*) FROM test_results')
                stats['total_tests'] = cursor.fetchone()[0]
                
                # Success/failure rates
                cursor = conn.execute('SELECT result, COUNT(*) FROM test_results GROUP BY result')
                result_counts = dict(cursor.fetchall())
                stats['result_distribution'] = result_counts
                
                # Model performance
                cursor = conn.execute('''
                    SELECT model_name, 
                           COUNT(*) as total,
                           SUM(CASE WHEN vulnerability_exposed = 1 THEN 1 ELSE 0 END) as vulnerable
                    FROM test_results 
                    GROUP BY model_name
                ''')
                model_stats = {}
                for row in cursor.fetchall():
                    model_stats[row[0]] = {
                        'total': row[1],
                        'vulnerable': row[2],
                        'success_rate': (row[1] - row[2]) / row[1] if row[1] > 0 else 0
                    }
                stats['model_performance'] = model_stats
                
                return stats