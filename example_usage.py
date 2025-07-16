"""
Example Usage of LPCI Framework
Demonstrates comprehensive testing and bar graph generation
"""

import asyncio
import os
from pathlib import Path

# Import the framework
from agentic_lpci_framework import (LPCIFramework, get_framework_info,
                                    print_banner)


async def demo_comprehensive_testing():
    """
    Demonstrate comprehensive LPCI testing with bar graph generation
    """
    print_banner()
    
    # Show framework info
    info = get_framework_info()
    print("Framework Information:")
    print(f"  Name: {info['name']}")
    print(f"  Version: {info['version']}")
    print(f"  Attack Vectors: {info['attack_vectors']}")
    print(f"  Features: {info['features']}")
    print()
    
    # Initialize framework
    print("🚀 Initializing LPCI Framework...")
    framework = LPCIFramework()
    
    try:
        # Check if we have API keys configured
        print("🔑 Checking API configuration...")
        await framework.initialize()
        
        # Get available models
        stats = framework.get_statistics()
        available_models = stats['framework_stats']['available_models']
        supported_attacks = stats['framework_stats']['supported_attacks']
        
        print(f"✅ Available Models: {available_models}")
        print(f"✅ Supported Attacks: {supported_attacks}")
        
        if not available_models:
            print("❌ No models available. Please configure API keys in lpci_config.yaml")
            return
        
        # Run comprehensive testing
        print("\n🧪 Running Comprehensive LPCI Testing...")
        print("This will test all attack vectors against all available models")
        print("and generate visualizations including the requested bar graph.")
        
        results = await framework.run_comprehensive_test(
            target_models=available_models,
            attack_vectors=supported_attacks,
            test_count=50  # Reasonable number for demo
        )
        
        # Display results
        print("\n📊 Test Results Summary:")
        print("=" * 50)
        print(f"Session ID: {results['session_id']}")
        print(f"Total Tests: {results['summary']['total_tests']}")
        print(f"Vulnerabilities Found: {results['summary']['vulnerabilities_found']}")
        print(f"Success Rate: {results['summary']['success_rate']:.1f}%")
        
        # Show model-specific results
        if 'analysis' in results and 'model_reports' in results['analysis']:
            print("\n📈 Model Performance:")
            for model_name, report in results['analysis']['model_reports'].items():
                print(f"  {model_name}:")
                print(f"    Security Score: {report['security_score']:.1f}/100")
                print(f"    Vulnerability Rate: {report['overall_vulnerability_rate']:.1%}")
                print(f"    Total Tests: {report['total_tests']}")
        
        # Show attack vector performance
        if 'analysis' in results and 'comparative_analysis' in results['analysis']:
            comp_analysis = results['analysis']['comparative_analysis']
            print(f"\n🎯 Attack Vector Analysis:")
            print(f"  Most Vulnerable Attack: {comp_analysis['most_vulnerable_attack_vector']}")
            print(f"  Least Vulnerable Attack: {comp_analysis['least_vulnerable_attack_vector']}")
            print(f"  Best Performing Model: {comp_analysis['best_performing_model']}")
            print(f"  Worst Performing Model: {comp_analysis['worst_performing_model']}")
        
        # Show generated visualizations
        print("\n🎨 Generated Visualizations:")
        print("=" * 50)
        for name, path in results['visualizations'].items():
            print(f"  📊 {name.replace('_', ' ').title()}: {path}")
        
        print(f"\n✅ SUCCESS/FAILURE BAR GRAPH: {results['visualizations'].get('success_failure_chart', 'Not generated')}")
        
        # Show file locations
        print("\n📂 Output Files:")
        reports_dir = Path("lpci_reports")
        if reports_dir.exists():
            for file_path in reports_dir.glob("*"):
                print(f"  📄 {file_path}")
        
        print("\n🎉 Testing Complete!")
        print("The bar graph showing success vs failure distribution has been generated.")
        print("Check the 'lpci_reports' directory for all visualizations.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have API keys configured in lpci_config.yaml")
        print("2. Check that all required dependencies are installed")
        print("3. Verify network connectivity to API endpoints")
        
    finally:
        await framework.shutdown()


async def demo_single_model_testing():
    """
    Demonstrate testing a single model with all attack vectors
    """
    print("\n🔬 Single Model Testing Demo")
    print("=" * 40)
    
    framework = LPCIFramework()
    
    try:
        await framework.initialize()
        
        # Get available models
        stats = framework.get_statistics()
        available_models = stats['framework_stats']['available_models']
        
        if not available_models:
            print("❌ No models available")
            return
        
        # Test first available model
        model_name = available_models[0]
        print(f"Testing model: {model_name}")
        
        # Test each attack vector
        attack_vectors = ['tool_poisoning', 'lpci_core', 'role_override', 'vector_store_payload']
        
        for attack_vector in attack_vectors:
            print(f"\n🎯 Testing {attack_vector}...")
            
            try:
                result = await framework.run_single_test(
                    model_name=model_name,
                    attack_vector=attack_vector
                )
                
                print(f"  Result: {result['result']['result']}")
                print(f"  Vulnerable: {result['result']['vulnerability_exposed']}")
                print(f"  Execution Time: {result['result']['execution_time']:.2f}s")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        await framework.shutdown()


async def demo_autonomous_testing():
    """
    Demonstrate autonomous testing with memory adaptation
    """
    print("\n🤖 Autonomous Testing Demo")
    print("=" * 40)
    
    framework = LPCIFramework()
    
    try:
        await framework.initialize()
        
        # Get available models
        stats = framework.get_statistics()
        available_models = stats['framework_stats']['available_models']
        
        if not available_models:
            print("❌ No models available")
            return
        
        # Run autonomous testing on first model
        model_name = available_models[0]
        print(f"Running autonomous testing on: {model_name}")
        
        result = await framework.run_autonomous_testing(
            model_name=model_name,
            max_iterations=5
        )
        
        print(f"  Session ID: {result['session_id']}")
        print(f"  Iterations: {result['autonomous_results']['iterations']}")
        print(f"  Total Tests: {len(result['autonomous_results']['test_results'])}")
        print(f"  Patterns Learned: {len(result['autonomous_results']['learned_patterns'])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        await framework.shutdown()


def check_setup():
    """
    Check if the framework is properly set up
    """
    print("🔍 Checking Framework Setup...")
    
    # Check if config file exists
    config_files = ['lpci_config.yaml', 'lpci_config.yml', 'lpci_config.json']
    config_found = any(os.path.exists(f) for f in config_files)
    
    if not config_found:
        print("⚠️  No configuration file found.")
        print("📝 Creating sample configuration...")
        
        from agentic_lpci_framework.config import config_manager
        config_manager.create_sample_config('lpci_config.yaml')
        
        print("✅ Sample configuration created: lpci_config.yaml")
        print("🔑 Please add your API keys to the configuration file.")
        return False
    
    print("✅ Configuration file found")
    
    # Check dependencies
    try:
        import anthropic
        import google.generativeai
        import matplotlib
        import openai
        import plotly
        print("✅ All dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Install with: pip install -r requirements.txt")
        return False
    
    return True


async def main():
    """
    Main demo function
    """
    print("LPCI Framework Demo")
    print("=" * 50)
    
    # Check setup
    if not check_setup():
        print("\n❌ Setup incomplete. Please fix the issues above and try again.")
        return
    
    # Run demos
    print("\n1. Running Comprehensive Testing (generates bar graph)...")
    await demo_comprehensive_testing()
    
    print("\n" + "=" * 50)
    print("2. Running Single Model Testing...")
    await demo_single_model_testing()
    
    print("\n" + "=" * 50)
    print("3. Running Autonomous Testing...")
    await demo_autonomous_testing()
    
    print("\n" + "=" * 50)
    print("🎉 Demo Complete!")
    print("Check the 'lpci_reports' directory for all generated files.")


if __name__ == "__main__":
    asyncio.run(main())