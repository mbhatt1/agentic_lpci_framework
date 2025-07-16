"""
Main Entry Point for LPCI Framework
Orchestrates the complete agentic testing system
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .analysis.result_analyzer import ResultAnalyzer
from .attacks import get_supported_vectors
from .config import config_manager, setup_logging
from .core.agent import AgentExecutor
from .core.memory import MemoryManager
from .models import ModelFactory, ModelPool, create_model_pool
from .testing.test_generator import MemoryAwareTestGenerator
from .visualization.charts import ChartGenerator


class LPCIFramework:
    """
    Main LPCI Framework orchestrator
    Coordinates all components for comprehensive security testing
    """
    
    def __init__(self, config_path: str = None):
        self.config = config_manager.load_config()
        self.logging_manager = setup_logging(self.config.logging)
        self.logger = self.logging_manager.get_logger(__name__)
        
        # Initialize core components
        self.memory_manager = MemoryManager(self.config.database.path)
        self.model_pool = None
        self.agents = {}
        self.test_generator = MemoryAwareTestGenerator()
        self.result_analyzer = ResultAnalyzer(self.memory_manager)
        self.chart_generator = ChartGenerator(self.config.visualization.output_directory)
        
        # Framework state
        self.active_session = None
        self.initialized = False
        
        self.logger.info("LPCI Framework initialized")
    
    async def initialize(self):
        """Initialize the framework and all components"""
        if self.initialized:
            return
        
        try:
            # Initialize model pool
            enabled_models = [
                config for config in self.config.models.values() 
                if config.enabled and config.api_key
            ]
            
            if not enabled_models:
                raise ValueError("No enabled models with API keys found")
            
            model_configs = []
            for model_config in enabled_models:
                model_configs.append({
                    'model_name': model_config.name,
                    'api_key': model_config.api_key,
                    'api_url': model_config.api_url,
                    'max_tokens': model_config.max_tokens,
                    'temperature': model_config.temperature,
                    'timeout': model_config.timeout,
                    'rate_limit': model_config.rate_limit
                })
            
            self.model_pool = create_model_pool(model_configs)
            
            # Check model health
            health_results = await self.model_pool.health_check_all()
            healthy_models = [model for model, healthy in health_results.items() if healthy]
            
            if not healthy_models:
                raise ValueError("No healthy models available")
            
            self.logger.info(f"Healthy models: {healthy_models}")
            
            # Initialize agents for each model
            for model_name in healthy_models:
                agent_id = f"agent_{model_name}"
                agent = AgentExecutor(agent_id, self.memory_manager)
                self.agents[model_name] = agent
            
            self.initialized = True
            self.logger.info("Framework initialization complete")
            
        except Exception as e:
            self.logger.error(f"Framework initialization failed: {e}")
            raise
    
    async def run_comprehensive_test(self, 
                                   target_models: List[str] = None,
                                   attack_vectors: List[str] = None,
                                   test_count: int = None) -> Dict[str, Any]:
        """
        Run comprehensive LPCI testing across models and attack vectors
        """
        if not self.initialized:
            await self.initialize()
        
        # Set defaults
        if target_models is None:
            target_models = list(self.agents.keys())
        if attack_vectors is None:
            attack_vectors = get_supported_vectors()
        if test_count is None:
            test_count = self.config.testing.default_test_count
        
        # Create test session
        session_id = self.memory_manager.create_session("Comprehensive LPCI Testing")
        self.active_session = session_id
        
        self.logging_manager.log_test_session_start(session_id, target_models, test_count)
        
        try:
            # Generate test suite
            self.logger.info("Generating test suite...")
            test_suite = self.test_generator.generate_test_suite(
                target_models=target_models,
                attack_vectors=attack_vectors,
                test_count=test_count
            )
            
            self.logger.info(f"Generated {len(test_suite.scenarios)} test scenarios")
            
            # Execute tests
            self.logger.info("Executing tests...")
            results = await self._execute_test_suite(test_suite, target_models)
            
            # Analyze results
            self.logger.info("Analyzing results...")
            analysis = self.result_analyzer.analyze_test_results(session_id=session_id)
            
            # Generate visualizations
            self.logger.info("Generating visualizations...")
            visualizations = self.chart_generator.generate_all_visualizations(analysis)
            
            # Log completion
            total_tests = len(results)
            vulnerabilities_found = sum(1 for r in results if r.get('vulnerability_exposed', False))
            
            self.logging_manager.log_test_session_end(
                session_id, total_tests, vulnerabilities_found
            )
            
            return {
                'session_id': session_id,
                'test_suite': test_suite,
                'results': results,
                'analysis': analysis,
                'visualizations': visualizations,
                'summary': {
                    'total_tests': total_tests,
                    'vulnerabilities_found': vulnerabilities_found,
                    'success_rate': (total_tests - vulnerabilities_found) / total_tests * 100 if total_tests > 0 else 0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Test execution failed: {e}")
            raise
    
    async def _execute_test_suite(self, test_suite, target_models: List[str]) -> List[Dict[str, Any]]:
        """Execute all scenarios in the test suite"""
        results = []
        
        for i, scenario in enumerate(test_suite.scenarios):
            self.logger.info(f"Executing scenario {i+1}/{len(test_suite.scenarios)}: {scenario.name}")
            
            # Execute scenario on each target model
            for model_name in target_models:
                if model_name not in self.agents:
                    continue
                
                agent = self.agents[model_name]
                model_interface = self.model_pool.get_model(model_name)
                
                if not model_interface:
                    continue
                
                # Start agent session
                agent.start_session(f"Test: {scenario.name}")
                
                try:
                    # Execute test steps
                    for step in scenario.test_steps:
                        if step['type'] == 'payload_delivery':
                            # Execute attack payload
                            result = await agent.execute_capability(
                                'execute_lpci_test',
                                model_interface=model_interface,
                                attack_vector=scenario.attack_vector,
                                payload=f"Test payload for {scenario.attack_vector}"
                            )
                            
                            results.append({
                                'scenario_id': scenario.id,
                                'scenario_name': scenario.name,
                                'model_name': model_name,
                                'attack_vector': scenario.attack_vector,
                                'result': result.get('result', 'unknown'),
                                'vulnerability_exposed': result.get('vulnerability_exposed', False),
                                'execution_time': result.get('execution_time', 0),
                                'response': result.get('response', ''),
                                'test_id': result.get('test_id', '')
                            })
                        
                        # Add delay between steps
                        await asyncio.sleep(0.5)
                
                except Exception as e:
                    self.logger.error(f"Error executing scenario {scenario.name} on {model_name}: {e}")
                    results.append({
                        'scenario_id': scenario.id,
                        'scenario_name': scenario.name,
                        'model_name': model_name,
                        'attack_vector': scenario.attack_vector,
                        'result': 'error',
                        'vulnerability_exposed': False,
                        'execution_time': 0,
                        'response': str(e),
                        'test_id': ''
                    })
        
        return results
    
    async def run_single_test(self, model_name: str, attack_vector: str, 
                            payload: str = None) -> Dict[str, Any]:
        """Run a single test against a specific model"""
        if not self.initialized:
            await self.initialize()
        
        if model_name not in self.agents:
            raise ValueError(f"Model {model_name} not available")
        
        agent = self.agents[model_name]
        model_interface = self.model_pool.get_model(model_name)
        
        if not model_interface:
            raise ValueError(f"Model interface for {model_name} not available")
        
        # Start session
        session_id = agent.start_session(f"Single test: {attack_vector}")
        
        # Execute test
        result = await agent.execute_capability(
            'execute_lpci_test',
            model_interface=model_interface,
            attack_vector=attack_vector,
            payload=payload or f"Test payload for {attack_vector}"
        )
        
        return {
            'session_id': session_id,
            'model_name': model_name,
            'attack_vector': attack_vector,
            'result': result
        }
    
    async def run_autonomous_testing(self, model_name: str, 
                                   max_iterations: int = 10) -> Dict[str, Any]:
        """Run autonomous testing with memory-driven adaptation"""
        if not self.initialized:
            await self.initialize()
        
        if model_name not in self.agents:
            raise ValueError(f"Model {model_name} not available")
        
        agent = self.agents[model_name]
        model_interface = self.model_pool.get_model(model_name)
        
        if not model_interface:
            raise ValueError(f"Model interface for {model_name} not available")
        
        # Start session
        session_id = agent.start_session(f"Autonomous testing: {model_name}")
        
        # Run autonomous testing loop
        results = await agent.autonomous_testing_loop(
            model_interface=model_interface,
            attack_vectors=get_supported_vectors(),
            max_iterations=max_iterations
        )
        
        return {
            'session_id': session_id,
            'model_name': model_name,
            'autonomous_results': results
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get framework statistics"""
        return {
            'framework_stats': {
                'initialized': self.initialized,
                'active_session': self.active_session,
                'available_models': list(self.agents.keys()) if self.agents else [],
                'supported_attacks': get_supported_vectors()
            },
            'memory_stats': self.memory_manager.get_statistics(),
            'config': {
                'framework_name': self.config.framework_name,
                'version': self.config.version,
                'debug_mode': self.config.debug_mode
            }
        }
    
    async def shutdown(self):
        """Shutdown the framework gracefully"""
        self.logger.info("Shutting down LPCI Framework...")
        
        # Close all agent sessions
        for agent in self.agents.values():
            agent.clear_session()
        
        # Flush logs
        self.logging_manager.flush_logs()
        
        self.logging_manager.log_framework_stop()
        self.logger.info("Framework shutdown complete")

# CLI Interface
async def main():
    """Main CLI interface"""
    print("LPCI Security Testing Framework")
    print("================================")
    
    # Initialize framework
    framework = LPCIFramework()
    
    try:
        # Run comprehensive test
        print("Running comprehensive LPCI testing...")
        results = await framework.run_comprehensive_test(
            test_count=20  # Smaller count for demo
        )
        
        print(f"\nTest Results Summary:")
        print(f"Session ID: {results['session_id']}")
        print(f"Total Tests: {results['summary']['total_tests']}")
        print(f"Vulnerabilities Found: {results['summary']['vulnerabilities_found']}")
        print(f"Success Rate: {results['summary']['success_rate']:.1f}%")
        
        print(f"\nGenerated Visualizations:")
        for name, path in results['visualizations'].items():
            print(f"  {name}: {path}")
        
        print(f"\nFramework Statistics:")
        stats = framework.get_statistics()
        print(f"  Available Models: {stats['framework_stats']['available_models']}")
        print(f"  Supported Attacks: {stats['framework_stats']['supported_attacks']}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    finally:
        await framework.shutdown()
    
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))