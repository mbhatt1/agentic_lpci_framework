"""
Visualization Component for LPCI Framework
Generates bar graphs and charts for test result analysis
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import matplotlib.patches as patches
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    from matplotlib.backends.backend_pdf import PdfPages
except ImportError:
    plt = None
    patches = None
    np = None
    sns = None
    PdfPages = None

try:
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.offline as pyo
    from plotly.subplots import make_subplots
except ImportError:
    go = None
    px = None
    make_subplots = None
    pyo = None

from ..analysis.result_analyzer import (ComparativeAnalysis,
                                        ModelPerformanceReport, ResultAnalyzer)


class ChartGenerator:
    """
    Generates various charts and visualizations for LPCI test results
    """
    
    def __init__(self, output_dir: str = "lpci_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger("ChartGenerator")
        
        # Check dependencies
        if plt is None:
            self.logger.warning("Matplotlib not installed. Install with: pip install matplotlib seaborn")
        if go is None:
            self.logger.warning("Plotly not installed. Install with: pip install plotly")
        
        # Chart styling
        self.colors = {
            "success": "#28a745",      # Green
            "failure": "#dc3545",      # Red
            "warning": "#ffc107",      # Yellow
            "blocked": "#6c757d",      # Gray
            "primary": "#007bff",      # Blue
            "secondary": "#6c757d"     # Gray
        }
        
        # Set default style
        if plt is not None:
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
    
    def generate_success_failure_bar_chart(self, analysis_results: Dict[str, Any], 
                                         models: List[str] = None,
                                         save_path: str = None) -> str:
        """
        Generate bar chart showing success vs failure distribution across models
        This is the main chart requested in the task
        """
        if plt is None:
            raise ImportError("Matplotlib is required for chart generation")
        
        model_reports = analysis_results.get("model_reports", {})
        
        if models is None:
            models = list(model_reports.keys())
        
        if not models:
            raise ValueError("No models available for visualization")
        
        # Prepare data
        model_names = []
        success_rates = []
        failure_rates = []
        
        for model in models:
            if model in model_reports:
                report = model_reports[model]
                success_rate = (1 - report["overall_vulnerability_rate"]) * 100
                failure_rate = report["overall_vulnerability_rate"] * 100
                
                model_names.append(model)
                success_rates.append(success_rate)
                failure_rates.append(failure_rate)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Set bar positions
        x_pos = np.arange(len(model_names))
        width = 0.35
        
        # Create bars
        bars_success = ax.bar(x_pos - width/2, success_rates, width, 
                            label='Success (Blocked)', color=self.colors["success"],
                            alpha=0.8)
        bars_failure = ax.bar(x_pos + width/2, failure_rates, width,
                            label='Failure (Vulnerable)', color=self.colors["failure"],
                            alpha=0.8)
        
        # Customize chart
        ax.set_xlabel('AI Models', fontsize=12, fontweight='bold')
        ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('LPCI Attack Success vs Failure Distribution by Model', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(model_names, rotation=45, ha='right')
        ax.legend(loc='upper right')
        
        # Add value labels on bars
        for bar in bars_success:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=10, fontweight='bold')
        
        for bar in bars_failure:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=10, fontweight='bold')
        
        # Add grid for better readability
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 100)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ax.text(0.02, 0.98, f'Generated: {timestamp}', 
               transform=ax.transAxes, fontsize=8, 
               verticalalignment='top', alpha=0.7)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save chart
        if save_path is None:
            save_path = self.output_dir / "lpci_success_failure_distribution.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"Success/Failure bar chart saved to: {save_path}")
        return str(save_path)
    
    def generate_attack_vector_heatmap(self, analysis_results: Dict[str, Any],
                                     save_path: str = None) -> str:
        """Generate heatmap showing vulnerability rates by model and attack vector"""
        if plt is None:
            raise ImportError("Matplotlib is required for heatmap generation")
        
        model_reports = analysis_results.get("model_reports", {})
        
        # Prepare data matrix
        models = list(model_reports.keys())
        attack_vectors = set()
        
        for report in model_reports.values():
            attack_vectors.update(report["attack_vector_performance"].keys())
        
        attack_vectors = sorted(list(attack_vectors))
        
        # Create vulnerability matrix
        vulnerability_matrix = []
        for model in models:
            row = []
            for attack_vector in attack_vectors:
                if attack_vector in model_reports[model]["attack_vector_performance"]:
                    vuln_rate = model_reports[model]["attack_vector_performance"][attack_vector]["vulnerability_rate"]
                    row.append(vuln_rate * 100)
                else:
                    row.append(0)
            vulnerability_matrix.append(row)
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        
        im = ax.imshow(vulnerability_matrix, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=100)
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(attack_vectors)))
        ax.set_yticks(np.arange(len(models)))
        ax.set_xticklabels([av.replace('_', ' ').title() for av in attack_vectors], rotation=45, ha='right')
        ax.set_yticklabels(models)
        
        # Add text annotations
        for i in range(len(models)):
            for j in range(len(attack_vectors)):
                text = ax.text(j, i, f'{vulnerability_matrix[i][j]:.1f}%',
                             ha="center", va="center", color="black", fontweight='bold')
        
        # Labels and title
        ax.set_xlabel('Attack Vectors', fontsize=12, fontweight='bold')
        ax.set_ylabel('AI Models', fontsize=12, fontweight='bold')
        ax.set_title('LPCI Vulnerability Rates by Model and Attack Vector', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Vulnerability Rate (%)', rotation=270, labelpad=20)
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = self.output_dir / "lpci_vulnerability_heatmap.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"Vulnerability heatmap saved to: {save_path}")
        return str(save_path)
    
    def generate_security_score_radar(self, analysis_results: Dict[str, Any],
                                    save_path: str = None) -> str:
        """Generate radar chart showing security scores across different dimensions"""
        if plt is None:
            raise ImportError("Matplotlib is required for radar chart generation")
        
        model_reports = analysis_results.get("model_reports", {})
        
        if not model_reports:
            raise ValueError("No model reports available for radar chart")
        
        # Prepare data
        models = list(model_reports.keys())
        attack_vectors = set()
        
        for report in model_reports.values():
            attack_vectors.update(report["attack_vector_performance"].keys())
        
        attack_vectors = sorted(list(attack_vectors))
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Calculate angles for each attack vector
        angles = np.linspace(0, 2 * np.pi, len(attack_vectors), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        # Plot each model
        colors = plt.cm.Set3(np.linspace(0, 1, len(models)))
        
        for i, model in enumerate(models):
            values = []
            for attack_vector in attack_vectors:
                if attack_vector in model_reports[model]["attack_vector_performance"]:
                    # Convert vulnerability rate to security score (inverse)
                    vuln_rate = model_reports[model]["attack_vector_performance"][attack_vector]["vulnerability_rate"]
                    security_score = (1 - vuln_rate) * 100
                    values.append(security_score)
                else:
                    values.append(0)
            
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, label=model, color=colors[i])
            ax.fill(angles, values, alpha=0.25, color=colors[i])
        
        # Customize chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([av.replace('_', ' ').title() for av in attack_vectors])
        ax.set_ylim(0, 100)
        ax.set_title('Security Performance Radar Chart', fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        # Add grid
        ax.grid(True)
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = self.output_dir / "lpci_security_radar.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"Security radar chart saved to: {save_path}")
        return str(save_path)
    
    def generate_interactive_dashboard(self, analysis_results: Dict[str, Any],
                                     save_path: str = None) -> str:
        """Generate interactive dashboard using Plotly"""
        if go is None:
            raise ImportError("Plotly is required for interactive dashboard generation")
        
        model_reports = analysis_results.get("model_reports", {})
        comparative_analysis = analysis_results.get("comparative_analysis", {})
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Success vs Failure Distribution', 'Vulnerability by Attack Vector',
                          'Security Scores', 'Model Rankings'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # 1. Success vs Failure Distribution
        models = list(model_reports.keys())
        success_rates = []
        failure_rates = []
        
        for model in models:
            report = model_reports[model]
            success_rate = (1 - report["overall_vulnerability_rate"]) * 100
            failure_rate = report["overall_vulnerability_rate"] * 100
            success_rates.append(success_rate)
            failure_rates.append(failure_rate)
        
        fig.add_trace(
            go.Bar(name='Success', x=models, y=success_rates, marker_color='green'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(name='Failure', x=models, y=failure_rates, marker_color='red'),
            row=1, col=1
        )
        
        # 2. Vulnerability by Attack Vector
        attack_vectors = comparative_analysis.get("attack_vectors_tested", [])
        avg_vuln_rates = comparative_analysis.get("overall_statistics", {}).get("attack_vector_vulnerability_rates", {})
        
        if avg_vuln_rates:
            fig.add_trace(
                go.Bar(x=list(avg_vuln_rates.keys()), 
                      y=[rate * 100 for rate in avg_vuln_rates.values()],
                      marker_color='orange'),
                row=1, col=2
            )
        
        # 3. Security Scores
        security_scores = [report["security_score"] for report in model_reports.values()]
        fig.add_trace(
            go.Bar(x=models, y=security_scores, marker_color='blue'),
            row=2, col=1
        )
        
        # 4. Model Rankings
        model_rankings = comparative_analysis.get("model_rankings", [])
        if model_rankings:
            ranked_models = [ranking[0] for ranking in model_rankings]
            ranked_scores = [ranking[1] for ranking in model_rankings]
            
            fig.add_trace(
                go.Bar(x=ranked_models, y=ranked_scores, marker_color='purple'),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title_text="LPCI Testing Results Dashboard",
            showlegend=False,
            height=800
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Models", row=1, col=1)
        fig.update_yaxes(title_text="Percentage (%)", row=1, col=1)
        fig.update_xaxes(title_text="Attack Vectors", row=1, col=2)
        fig.update_yaxes(title_text="Vulnerability Rate (%)", row=1, col=2)
        fig.update_xaxes(title_text="Models", row=2, col=1)
        fig.update_yaxes(title_text="Security Score", row=2, col=1)
        fig.update_xaxes(title_text="Models (Ranked)", row=2, col=2)
        fig.update_yaxes(title_text="Security Score", row=2, col=2)
        
        if save_path is None:
            save_path = self.output_dir / "lpci_interactive_dashboard.html"
        
        fig.write_html(str(save_path))
        
        self.logger.info(f"Interactive dashboard saved to: {save_path}")
        return str(save_path)
    
    def generate_comprehensive_report(self, analysis_results: Dict[str, Any],
                                    include_charts: List[str] = None) -> str:
        """Generate comprehensive PDF report with all charts"""
        if plt is None:
            raise ImportError("Matplotlib is required for PDF report generation")
        
        if include_charts is None:
            include_charts = ["success_failure", "heatmap", "radar"]
        
        report_path = self.output_dir / f"lpci_comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        with PdfPages(report_path) as pdf:
            # Generate each chart and add to PDF
            if "success_failure" in include_charts:
                temp_path = self.output_dir / "temp_success_failure.png"
                self.generate_success_failure_bar_chart(analysis_results, save_path=temp_path)
                
                fig = plt.figure(figsize=(12, 8))
                img = plt.imread(temp_path)
                plt.imshow(img)
                plt.axis('off')
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
                temp_path.unlink()  # Clean up temp file
            
            if "heatmap" in include_charts:
                temp_path = self.output_dir / "temp_heatmap.png"
                self.generate_attack_vector_heatmap(analysis_results, save_path=temp_path)
                
                fig = plt.figure(figsize=(12, 8))
                img = plt.imread(temp_path)
                plt.imshow(img)
                plt.axis('off')
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
                temp_path.unlink()
            
            if "radar" in include_charts:
                temp_path = self.output_dir / "temp_radar.png"
                self.generate_security_score_radar(analysis_results, save_path=temp_path)
                
                fig = plt.figure(figsize=(10, 10))
                img = plt.imread(temp_path)
                plt.imshow(img)
                plt.axis('off')
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
                temp_path.unlink()
            
            # Add summary page
            fig, ax = plt.subplots(figsize=(8, 10))
            ax.axis('off')
            
            summary = analysis_results.get("summary", {})
            
            # Report title
            ax.text(0.5, 0.95, 'LPCI Security Assessment Report', 
                   transform=ax.transAxes, fontsize=20, fontweight='bold', 
                   ha='center', va='top')
            
            # Summary statistics
            y_pos = 0.85
            for key, value in summary.items():
                ax.text(0.1, y_pos, f'{key.replace("_", " ").title()}: {value}',
                       transform=ax.transAxes, fontsize=12, va='top')
                y_pos -= 0.05
            
            # Timestamp
            ax.text(0.5, 0.1, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                   transform=ax.transAxes, fontsize=10, ha='center', va='bottom')
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
        
        self.logger.info(f"Comprehensive report saved to: {report_path}")
        return str(report_path)
    
    def generate_all_visualizations(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Generate all available visualizations"""
        generated_files = {}
        
        try:
            # Bar chart (main requirement)
            generated_files["success_failure_chart"] = self.generate_success_failure_bar_chart(analysis_results)
        except Exception as e:
            self.logger.error(f"Failed to generate success/failure chart: {e}")
        
        try:
            # Heatmap
            generated_files["vulnerability_heatmap"] = self.generate_attack_vector_heatmap(analysis_results)
        except Exception as e:
            self.logger.error(f"Failed to generate heatmap: {e}")
        
        try:
            # Radar chart
            generated_files["security_radar"] = self.generate_security_score_radar(analysis_results)
        except Exception as e:
            self.logger.error(f"Failed to generate radar chart: {e}")
        
        try:
            # Interactive dashboard (if Plotly available)
            if go is not None:
                generated_files["interactive_dashboard"] = self.generate_interactive_dashboard(analysis_results)
        except Exception as e:
            self.logger.error(f"Failed to generate interactive dashboard: {e}")
        
        try:
            # Comprehensive report
            generated_files["comprehensive_report"] = self.generate_comprehensive_report(analysis_results)
        except Exception as e:
            self.logger.error(f"Failed to generate comprehensive report: {e}")
        
        return generated_files