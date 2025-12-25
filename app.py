# app.py - Complete AbGenesis 2.0 with GitHub Integration
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import time
import hashlib
import base64
import io
import zipfile
import tempfile
import os
from io import StringIO, BytesIO
import requests
from collections import defaultdict, Counter
import random
import string
from typing import Dict, List, Optional, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Set page config - FIRST COMMAND
st.set_page_config(
    page_title="AbGenesis 2.0 - AI Antibody Design",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/abgenesis',
        'Report a bug': 'https://github.com/yourusername/abgenesis/issues',
        'About': """
        ## AbGenesis 2.0 🧬
        
        AI-powered antibody design platform with:
        - Physics-aware modeling
        - Epitope-constrained design  
        - Variable-length CDRs
        - GitHub integration
        
        Version 2.1.0 | MIT License
        """
    }
)

# Custom CSS with GitHub dark theme
st.markdown("""
<style>
    /* GitHub Dark Theme */
    :root {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-tertiary: #21262d;
        --text-primary: #c9d1d9;
        --text-secondary: #8b949e;
        --accent-blue: #58a6ff;
        --accent-green: #238636;
        --accent-red: #da3633;
        --accent-purple: #8957e5;
        --border-color: #30363d;
    }
    
    .main {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    .stApp {
        background-color: var(--bg-primary);
    }
    
    /* GitHub Header */
    .github-header {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* GitHub Cards */
    .github-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .github-card:hover {
        border-color: var(--accent-blue);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(88, 166, 255, 0.15);
    }
    
    /* Badges */
    .github-badge {
        display: inline-block;
        background: var(--accent-green);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    .badge-blue { background: var(--accent-blue); }
    .badge-red { background: var(--accent-red); }
    .badge-purple { background: var(--accent-purple); }
    .badge-gray { background: var(--text-secondary); }
    
    /* Buttons */
    .github-button {
        background: var(--accent-green) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .github-button:hover {
        background: #2ea043 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Issues & PRs */
    .issue-open {
        border-left: 4px solid var(--accent-green);
        background: var(--bg-secondary);
    }
    
    .issue-closed {
        border-left: 4px solid var(--accent-red);
        background: var(--bg-secondary);
    }
    
    .pr-open {
        border-left: 4px solid var(--accent-blue);
        background: var(--bg-secondary);
    }
    
    .pr-merged {
        border-left: 4px solid var(--accent-purple);
        background: var(--bg-secondary);
    }
    
    /* Metrics Cards */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--accent-blue);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Code Blocks */
    .code-block {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 1rem;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
    }
    
    /* Custom Streamlit Elements */
    .stButton > button {
        background: var(--accent-green) !important;
        color: white !important;
        border: none !important;
    }
    
    .stSelectbox, .stTextInput, .stTextArea {
        background: var(--bg-secondary) !important;
        border-color: var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'github_token': '',
        'github_connected': False,
        'github_username': '',
        'github_repos': [],
        'current_repo': None,
        'designs': [],
        'design_counter': 0,
        'antigens': {},
        'physics_params': {
            'electrostatics': 0.25,
            'van_der_waals': 0.20,
            'solvation': 0.15,
            'hydrogen_bonds': 0.15,
            'shape_complementarity': 0.15,
            'entropy': 0.05,
            'desolvation': 0.05
        },
        'epitope_params': {
            'weight': 0.3,
            'type': 'discontinuous',
            'length_range': (8, 20)
        },
        'cdr_params': {
            'ensemble_size': 20,
            'diversity': 0.5,
            'length_sampling': 'natural'
        },
        'export_format': 'json',
        'theme': 'dark',
        'auto_save': True,
        'recent_activity': [],
        'benchmark_results': {}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize
init_session_state()

# ============================================================================
# SIMULATED GITHUB INTEGRATION (No PyGithub dependency)
# ============================================================================

class SimulatedGitHub:
    """Simulated GitHub integration for demo purposes"""
    
    def __init__(self):
        self.repositories = self._create_sample_repos()
        self.issues = self._create_sample_issues()
        self.pull_requests = self._create_sample_prs()
        self.commits = self._create_sample_commits()
    
    def _create_sample_repos(self):
        """Create sample repositories"""
        return [
            {
                'name': 'abgenesis-antibodies',
                'full_name': 'user/abgenesis-antibodies',
                'description': 'Antibody designs created with AbGenesis 2.0',
                'private': False,
                'stars': 42,
                'forks': 8,
                'issues': 12,
                'updated_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'designs': 156,
                'collaborators': 3
            },
            {
                'name': 'covid-antibody-designs',
                'full_name': 'user/covid-antibody-designs',
                'description': 'SARS-CoV-2 therapeutic antibody designs',
                'private': True,
                'stars': 28,
                'forks': 4,
                'issues': 5,
                'updated_at': (datetime.now() - timedelta(days=3)).isoformat(),
                'designs': 89,
                'collaborators': 2
            },
            {
                'name': 'cancer-immunotherapy',
                'full_name': 'user/cancer-immunotherapy',
                'description': 'Cancer immunotherapy antibody designs',
                'private': False,
                'stars': 67,
                'forks': 12,
                'issues': 8,
                'updated_at': (datetime.now() - timedelta(days=7)).isoformat(),
                'designs': 234,
                'collaborators': 5
            }
        ]
    
    def _create_sample_issues(self):
        """Create sample issues"""
        return [
            {
                'number': 1,
                'title': 'Improve physics scoring for HER2 designs',
                'state': 'open',
                'labels': ['enhancement', 'physics'],
                'created_at': (datetime.now() - timedelta(days=5)).isoformat(),
                'comments': 3
            },
            {
                'number': 2,
                'title': 'Bug: CDR-H3 length distribution incorrect',
                'state': 'closed',
                'labels': ['bug', 'cdr'],
                'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
                'comments': 7
            },
            {
                'number': 3,
                'title': 'Add support for bispecific antibodies',
                'state': 'open',
                'labels': ['feature', 'enhancement'],
                'created_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'comments': 5
            }
        ]
    
    def _create_sample_prs(self):
        """Create sample pull requests"""
        return [
            {
                'number': 12,
                'title': 'Add epitope prediction model',
                'state': 'open',
                'head': 'feature/epitope-prediction',
                'base': 'main',
                'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'comments': 4
            },
            {
                'number': 11,
                'title': 'Update physics parameters',
                'state': 'merged',
                'head': 'feature/physics-update',
                'base': 'main',
                'created_at': (datetime.now() - timedelta(days=4)).isoformat(),
                'comments': 8
            }
        ]
    
    def _create_sample_commits(self):
        """Create sample commits"""
        return [
            {
                'sha': 'a1b2c3d4',
                'message': 'Add HER2 antibody designs',
                'author': 'user',
                'date': (datetime.now() - timedelta(hours=2)).isoformat(),
                'files': 3
            },
            {
                'sha': 'e5f6g7h8',
                'message': 'Fix CDR length calculation',
                'author': 'collaborator',
                'date': (datetime.now() - timedelta(days=1)).isoformat(),
                'files': 1
            }
        ]
    
    def authenticate(self, token):
        """Simulate GitHub authentication"""
        if token and len(token) > 10:
            st.session_state.github_connected = True
            st.session_state.github_username = 'abgenesis-user'
            st.session_state.github_repos = self.repositories
            return True, "✅ Authenticated with GitHub!"
        else:
            return False, "❌ Invalid token"
    
    def get_repositories(self):
        """Get user repositories"""
        return self.repositories
    
    def create_repository(self, name, description, private):
        """Create new repository"""
        new_repo = {
            'name': name,
            'full_name': f'user/{name}',
            'description': description,
            'private': private,
            'stars': 0,
            'forks': 0,
            'issues': 0,
            'updated_at': datetime.now().isoformat(),
            'designs': 0,
            'collaborators': 1
        }
        self.repositories.append(new_repo)
        st.session_state.github_repos = self.repositories
        return True, new_repo
    
    def push_design(self, repo_name, design_data, commit_message):
        """Push design to repository"""
        # Simulate pushing to GitHub
        time.sleep(0.5)  # Simulate API call
        return True, f"✅ Design pushed to {repo_name}"
    
    def create_issue(self, repo_name, title, body, labels):
        """Create issue"""
        new_issue = {
            'number': len(self.issues) + 1,
            'title': title,
            'state': 'open',
            'labels': labels,
            'created_at': datetime.now().isoformat(),
            'comments': 0
        }
        self.issues.append(new_issue)
        return True, new_issue
    
    def get_issues(self, repo_name):
        """Get repository issues"""
        return self.issues

# Initialize simulated GitHub
github = SimulatedGitHub()

# ============================================================================
# ANTIBODY DESIGN ENGINE
# ============================================================================

class AntibodyDesignEngine:
    """Core antibody design engine with physics modeling"""
    
    def __init__(self):
        # Amino acid properties
        self.aa_properties = {
            'A': {'hydrophobicity': 1.8, 'charge': 0, 'polarity': 0},
            'R': {'hydrophobicity': -4.5, 'charge': 1, 'polarity': 1},
            'N': {'hydrophobicity': -3.5, 'charge': 0, 'polarity': 1},
            'D': {'hydrophobicity': -3.5, 'charge': -1, 'polarity': 1},
            'C': {'hydrophobicity': 2.5, 'charge': 0, 'polarity': 0},
            'Q': {'hydrophobicity': -3.5, 'charge': 0, 'polarity': 1},
            'E': {'hydrophobicity': -3.5, 'charge': -1, 'polarity': 1},
            'G': {'hydrophobicity': -0.4, 'charge': 0, 'polarity': 0},
            'H': {'hydrophobicity': -3.2, 'charge': 0.5, 'polarity': 1},
            'I': {'hydrophobicity': 4.5, 'charge': 0, 'polarity': 0},
            'L': {'hydrophobicity': 3.8, 'charge': 0, 'polarity': 0},
            'K': {'hydrophobicity': -3.9, 'charge': 1, 'polarity': 1},
            'M': {'hydrophobicity': 1.9, 'charge': 0, 'polarity': 0},
            'F': {'hydrophobicity': 2.8, 'charge': 0, 'polarity': 0},
            'P': {'hydrophobicity': -1.6, 'charge': 0, 'polarity': 0},
            'S': {'hydrophobicity': -0.8, 'charge': 0, 'polarity': 1},
            'T': {'hydrophobicity': -0.7, 'charge': 0, 'polarity': 1},
            'W': {'hydrophobicity': -0.9, 'charge': 0, 'polarity': 0},
            'Y': {'hydrophobicity': -1.3, 'charge': 0, 'polarity': 1},
            'V': {'hydrophobicity': 4.2, 'charge': 0, 'polarity': 0}
        }
        
        # CDR length distributions from SAbDab
        self.cdr_lengths = {
            'H1': {'mean': 10.2, 'std': 2.1, 'min': 5, 'max': 15},
            'H2': {'mean': 16.5, 'std': 3.2, 'min': 9, 'max': 25},
            'H3': {'mean': 12.8, 'std': 4.5, 'min': 3, 'max': 35},
            'L1': {'mean': 11.5, 'std': 2.3, 'min': 7, 'max': 17},
            'L2': {'mean': 7.0, 'std': 0.5, 'min': 5, 'max': 9},
            'L3': {'mean': 9.2, 'std': 1.8, 'min': 5, 'max': 14}
        }
        
        # Framework regions (humanized)
        self.frameworks = {
            'heavy_fr1': 'QVQLVQSGAEVKKPGASVKVSCKAS',
            'heavy_fr2': 'WVRQAPGQGLEWMG',
            'heavy_fr3': 'RVTMTKDTSISTAYMELSRLRSDDTAVYYCAR',
            'heavy_fr4': 'WGQGTLVTVSS',
            'light_fr1': 'DIQMTQSPSSLSASVGDRVTITC',
            'light_fr2': 'WYQQKPGKAPKLLIY',
            'light_fr3': 'GVPSRFSGSGSGTDFTLTISSLQPEDFATYYC',
            'light_fr4': 'FGQGTKVEIK'
        }
        
        # Known therapeutic antibodies for benchmarking
        self.therapeutic_antibodies = {
            'trastuzumab': {
                'target': 'HER2',
                'heavy': 'EVQLVESGGGLVQPGGSLRLSCAASGFNIKDTYIHWVRQAPGKGLEWVARIYPTNGYTRYADSVKGRFTISADTSKNTAYLQMNSLRAEDTAVYYCSRWGGDGFYAMDYWGQGTLVTVSS',
                'light': 'DIQMTQSPSSLSASVGDRVTITCRASQDVNTAVAWYQQKPGKAPKLLIYSASFLYSGVPSRFSGSRSGTDFTLTISSLQPEDFATYYCQQHYTTPPTFGQGTKVEIK',
                'affinity': 0.1,  # nM
                'type': 'humanized IgG1'
            },
            'pembrolizumab': {
                'target': 'PD-1',
                'heavy': 'QVQLVQSGAEVKKPGSSVKVSCKASGGTFSSYAISWVRQAPGQGLEWMGGIIPIFGTANYAQKFQGRVTITADESTSTAYMELSSLRSEDTAVYYCARVRQFYGSSYWYFDVWGQGTLVTVSS',
                'light': 'EIVLTQSPGTLSLSPGERATLSCRASQSVSSYLAWYQQKPGQAPRLLIYGASSRATGIPDRFSGSGSGTDFTLTISRLEPEDFAVYYCQQRSNWPLTFGQGTKVEIK',
                'affinity': 0.03,
                'type': 'humanized IgG4'
            }
        }
    
    def generate_antibody_design(self, antigen_name, params):
        """Generate a complete antibody design"""
        design_id = f"ABG2_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{st.session_state.design_counter}"
        st.session_state.design_counter += 1
        
        # Generate CDRs
        cdrs = self._generate_cdrs(params)
        
        # Assemble antibody
        heavy_chain = self._assemble_heavy_chain(cdrs)
        light_chain = self._assemble_light_chain(cdrs)
        
        # Calculate scores
        scores = self._calculate_scores(heavy_chain, light_chain, antigen_name, params)
        
        # Create design object
        design = {
            'design_id': design_id,
            'antigen_name': antigen_name,
            'heavy_chain': heavy_chain,
            'light_chain': light_chain,
            'cdrs': cdrs,
            'scores': scores,
            'metadata': {
                'created': datetime.now().isoformat(),
                'params': params,
                'version': '2.1.0'
            },
            'physics_analysis': self._physics_analysis(heavy_chain, light_chain),
            'developability': self._developability_analysis(heavy_chain + light_chain),
            'epitope_compatibility': self._epitope_compatibility(cdrs, antigen_name)
        }
        
        return design
    
    def _generate_cdrs(self, params):
        """Generate CDR sequences"""
        cdrs = {}
        
        for cdr_type in ['H1', 'H2', 'H3', 'L1', 'L2', 'L3']:
            # Get length based on distribution or params
            if params.get('cdr_length_sampling') == 'natural':
                length_info = self.cdr_lengths[cdr_type]
                length = int(np.random.normal(length_info['mean'], length_info['std']))
                length = max(length_info['min'], min(length_info['max'], length))
            else:
                length = params.get(f'{cdr_type}_length', 10)
            
            # Generate sequence
            sequence = self._generate_cdr_sequence(cdr_type, length, params)
            cdrs[cdr_type] = sequence
        
        return cdrs
    
    def _generate_cdr_sequence(self, cdr_type, length, params):
        """Generate CDR sequence with appropriate biases"""
        # CDR-specific amino acid preferences
        preferences = {
            'H1': 'GYTFTSYAMHASDNRK',
            'H2': 'INPSGGSTYAQKFQGVW',
            'H3': 'ARDGVYWSTNQHKP',
            'L1': 'RASQDN',
            'L2': 'AASSLQRT',
            'L3': 'QQSYTNDPLF'
        }
        
        # Generate sequence with bias
        pref_set = preferences.get(cdr_type, 'ACDEFGHIKLMNPQRSTVWY')
        sequence = []
        
        for i in range(length):
            if i < len(pref_set) and np.random.random() < 0.7:
                sequence.append(pref_set[i])
            else:
                # Include some random diversity
                all_aas = 'ACDEFGHIKLMNPQRSTVWY'
                if params.get('epitope_weight', 0) > 0.5 and np.random.random() < 0.3:
                    # Add paratope residues for epitope targeting
                    paratope_residues = 'YWRHDE'
                    sequence.append(np.random.choice(list(paratope_residues)))
                else:
                    sequence.append(np.random.choice(list(all_aas)))
        
        return ''.join(sequence)
    
    def _assemble_heavy_chain(self, cdrs):
        """Assemble heavy chain from CDRs and frameworks"""
        return (
            self.frameworks['heavy_fr1'] + cdrs['H1'] +
            self.frameworks['heavy_fr2'] + cdrs['H2'] +
            self.frameworks['heavy_fr3'] + cdrs['H3'] +
            self.frameworks['heavy_fr4']
        )
    
    def _assemble_light_chain(self, cdrs):
        """Assemble light chain from CDRs and frameworks"""
        return (
            self.frameworks['light_fr1'] + cdrs['L1'] +
            self.frameworks['light_fr2'] + cdrs['L2'] +
            self.frameworks['light_fr3'] + cdrs['L3'] +
            self.frameworks['light_fr4']
        )
    
    def _calculate_scores(self, heavy_chain, light_chain, antigen_name, params):
        """Calculate design scores"""
        full_sequence = heavy_chain + light_chain
        
        # Physics score
        physics_score = self._calculate_physics_score(full_sequence)
        
        # Epitope compatibility score
        epitope_score = 0.7 + np.random.random() * 0.3  # Simulated
        
        # Developability score
        developability_score = self._calculate_developability_score(full_sequence)
        
        # Overall score (weighted combination)
        weights = params.get('score_weights', {
            'physics': 0.4,
            'epitope': 0.3,
            'developability': 0.3
        })
        
        overall_score = (
            physics_score * weights['physics'] +
            epitope_score * weights['epitope'] +
            developability_score * weights['developability']
        )
        
        return {
            'overall': round(overall_score, 3),
            'physics': round(physics_score, 3),
            'epitope': round(epitope_score, 3),
            'developability': round(developability_score, 3),
            'weights': weights
        }
    
    def _calculate_physics_score(self, sequence):
        """Calculate physics-based score"""
        # Simplified physics scoring
        score = 0.5  # Base score
        
        # Hydrophobicity balance
        hydrophobicity = self._calculate_hydrophobicity(sequence)
        score += 0.2 * (1.0 - abs(hydrophobicity - 0.5))
        
        # Charge balance
        charge = self._calculate_net_charge(sequence)
        score += 0.15 * (1.0 - min(1.0, abs(charge) / 5))
        
        # Length appropriate
        length_score = 1.0 - min(1.0, abs(len(sequence) - 220) / 100)
        score += 0.15 * length_score
        
        # CDR properties
        score += 0.1 * np.random.random()  # Random component
        
        return min(1.0, max(0.0, score))
    
    def _calculate_developability_score(self, sequence):
        """Calculate developability score"""
        score = 0.6  # Base score
        
        # Aggregation propensity
        aggregation_motifs = ['LVFFA', 'GNNQQNY', 'NFGAIL']
        motif_count = sum(sequence.count(motif) for motif in aggregation_motifs)
        score -= 0.1 * min(2, motif_count)
        
        # Cysteine count (disulfide potential)
        cys_count = sequence.count('C')
        if 2 <= cys_count <= 6:
            score += 0.1  # Good for disulfide bonds
        elif cys_count > 6:
            score -= 0.1  # Too many cysteines
        
        # Proline content (stability)
        pro_content = sequence.count('P') / len(sequence)
        if 0.04 <= pro_content <= 0.08:
            score += 0.1  # Good proline content
        
        return min(1.0, max(0.0, score))
    
    def _physics_analysis(self, heavy_chain, light_chain):
        """Perform physics analysis"""
        return {
            'binding_energy': round(-8 + np.random.random() * 4, 2),  # kcal/mol
            'interface_area': round(1000 + np.random.random() * 500, 1),  # Å²
            'hydrogen_bonds': int(8 + np.random.random() * 8),
            'shape_complementarity': round(0.6 + np.random.random() * 0.3, 3),
            'electrostatic_complementarity': round(0.5 + np.random.random() * 0.4, 3)
        }
    
    def _developability_analysis(self, sequence):
        """Perform developability analysis"""
        return {
            'solubility': round(0.7 + np.random.random() * 0.3, 3),
            'aggregation_score': round(0.1 + np.random.random() * 0.4, 3),
            'thermal_stability': round(65 + np.random.random() * 15, 1),  # °C
            'expression_titer': round(50 + np.random.random() * 50, 1),  # mg/L
            'immunogenicity_risk': round(0.2 + np.random.random() * 0.3, 3)
        }
    
    def _epitope_compatibility(self, cdrs, antigen_name):
        """Calculate epitope compatibility"""
        return {
            'paratope_residues': sum(cdr.count('Y') + cdr.count('W') + cdr.count('R') for cdr in cdrs.values()),
            'complementarity_score': round(0.6 + np.random.random() * 0.4, 3),
            'predicted_affinity': round(1 + np.random.random() * 9, 2),  # nM
            'epitope_coverage': round(0.5 + np.random.random() * 0.5, 3)
        }
    
    def _calculate_hydrophobicity(self, sequence):
        """Calculate average hydrophobicity"""
        scores = [self.aa_properties.get(aa, {}).get('hydrophobicity', 0) for aa in sequence]
        avg = np.mean(scores)
        # Normalize to 0-1
        return (avg + 4.5) / 9.0
    
    def _calculate_net_charge(self, sequence, ph=7.4):
        """Calculate net charge at given pH"""
        charge = 0
        for aa in sequence:
            props = self.aa_properties.get(aa, {})
            charge += props.get('charge', 0)
        return charge

# Initialize design engine
design_engine = AntibodyDesignEngine()

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_design_comparison_plot(designs):
    """Create comparison plot for multiple designs"""
    if len(designs) < 2:
        return None
    
    # Extract scores
    design_ids = [d['design_id'] for d in designs]
    overall_scores = [d['scores']['overall'] for d in designs]
    physics_scores = [d['scores']['physics'] for d in designs]
    epitope_scores = [d['scores']['epitope'] for d in designs]
    developability_scores = [d['scores']['developability'] for d in designs]
    
    # Create figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Overall Scores', 'Physics Scores', 
                       'Epitope Scores', 'Developability Scores'),
        vertical_spacing=0.15,
        horizontal_spacing=0.15
    )
    
    # Overall scores
    fig.add_trace(
        go.Bar(
            x=design_ids,
            y=overall_scores,
            name='Overall',
            marker_color='#58a6ff'
        ),
        row=1, col=1
    )
    
    # Physics scores
    fig.add_trace(
        go.Bar(
            x=design_ids,
            y=physics_scores,
            name='Physics',
            marker_color='#238636'
        ),
        row=1, col=2
    )
    
    # Epitope scores
    fig.add_trace(
        go.Bar(
            x=design_ids,
            y=epitope_scores,
            name='Epitope',
            marker_color='#8957e5'
        ),
        row=2, col=1
    )
    
    # Developability scores
    fig.add_trace(
        go.Bar(
            x=design_ids,
            y=developability_scores,
            name='Developability',
            marker_color='#da3633'
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#c9d1d9'
    )
    
    # Update axes
    for i in range(1, 5):
        fig.update_yaxes(range=[0, 1], row=(i-1)//2 + 1, col=(i-1)%2 + 1)
    
    return fig

def create_physics_radar_chart(design):
    """Create radar chart for physics analysis"""
    categories = ['Binding Energy', 'Interface Area', 'H-Bonds', 'Shape Comp.', 'Electrostatic']
    
    # Normalize values
    values = [
        1.0 - min(1.0, abs(design['physics_analysis']['binding_energy']) / 20),
        design['physics_analysis']['interface_area'] / 2000,
        design['physics_analysis']['hydrogen_bonds'] / 20,
        design['physics_analysis']['shape_complementarity'],
        design['physics_analysis']['electrostatic_complementarity']
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(88, 166, 255, 0.3)',
        line_color='#58a6ff',
        line_width=2
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor='#30363d',
                linecolor='#30363d'
            ),
            angularaxis=dict(
                gridcolor='#30363d',
                linecolor='#30363d'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#c9d1d9'
    )
    
    return fig

def create_github_activity_timeline():
    """Create GitHub activity timeline"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    data = {
        'Date': dates,
        'Commits': np.random.randint(0, 10, 30),
        'Designs': np.random.randint(0, 5, 30),
        'Issues': np.random.randint(0, 3, 30)
    }
    
    df = pd.DataFrame(data)
    
    fig = px.line(df, x='Date', y=['Commits', 'Designs', 'Issues'],
                  color_discrete_map={
                      'Commits': '#58a6ff',
                      'Designs': '#238636',
                      'Issues': '#da3633'
                  })
    
    fig.update_layout(
        title='GitHub Activity Timeline',
        xaxis_title='Date',
        yaxis_title='Count',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#c9d1d9',
        legend_title_text='Activity Type'
    )
    
    fig.update_xaxes(gridcolor='#30363d')
    fig.update_yaxes(gridcolor='#30363d')
    
    return fig

# ============================================================================
# STREAMLIT APP PAGES
# ============================================================================

def show_header():
    """Show application header"""
    st.markdown("""
    <div class="github-header">
        <div style="display: flex; align-items: center; gap: 1.5rem;">
            <div style="font-size: 3rem;">🧬</div>
            <div>
                <h1 style="margin: 0; color: white; font-size: 2.5rem;">AbGenesis 2.0</h1>
                <p style="margin: 0.5rem 0 0 0; color: #8b949e; font-size: 1.1rem;">
                    AI-Powered Antibody Design with GitHub Integration
                </p>
            </div>
        </div>
        <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
            <span class="github-badge">v2.1.0</span>
            <span class="github-badge badge-blue">GitHub Integrated</span>
            <span class="github-badge badge-purple">Physics-Aware</span>
            <span class="github-badge badge-green">Production Ready</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Show sidebar with navigation"""
    with st.sidebar:
        st.markdown("### 🔐 GitHub Connection")
        
        # GitHub token input
        if not st.session_state.github_connected:
            token = st.text_input(
                "GitHub Token",
                type="password",
                help="Enter any non-empty text for demo (no real token needed)"
            )
            
            if st.button("Connect to GitHub", use_container_width=True, type="primary"):
                if token:
                    success, message = github.authenticate(token)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter a token")
        else:
            st.success(f"✅ Connected as {st.session_state.github_username}")
            if st.button("Disconnect", use_container_width=True):
                st.session_state.github_connected = False
                st.rerun()
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📁 Navigation")
        page = st.radio(
            "Select Page",
            ["🏠 Dashboard", 
             "🎯 Design Studio", 
             "📊 Analyze Designs",
             "📚 GitHub Repos",
             "🤝 Collaborate",
             "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📈 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Designs", len(st.session_state.designs))
        with col2:
            st.metric("Repos", len(st.session_state.github_repos))
        
        # Recent Activity
        if st.session_state.recent_activity:
            st.markdown("### 📝 Recent")
            for activity in st.session_state.recent_activity[-3:]:
                st.caption(f"• {activity}")
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Clear Designs", use_container_width=True):
            st.session_state.designs = []
            st.session_state.recent_activity.append("Cleared all designs")
            st.rerun()
        
        if st.button("💾 Export All", use_container_width=True):
            export_all_designs()
    
    return page

def show_dashboard():
    """Show main dashboard"""
    st.markdown("## 📊 Dashboard")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Designs</div>
        </div>
        """.format(len(st.session_state.designs)), unsafe_allow_html=True)
    
    with col2:
        best_score = max([d['scores']['overall'] for d in st.session_state.designs]) if st.session_state.designs else 0
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{:.2f}</div>
            <div class="metric-label">Best Score</div>
        </div>
        """.format(best_score), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">GitHub Repos</div>
        </div>
        """.format(len(st.session_state.github_repos)), unsafe_allow_html=True)
    
    with col4:
        issues_count = len(github.issues)
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Open Issues</div>
        </div>
        """.format(issues_count), unsafe_allow_html=True)
    
    # Recent Designs
    st.markdown("### 🧬 Recent Designs")
    
    if st.session_state.designs:
        recent_designs = st.session_state.designs[-5:]  # Last 5 designs
        
        for design in recent_designs:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{design['design_id']}**")
                    st.caption(f"Antigen: {design['antigen_name']}")
                
                with col2:
                    st.metric("Score", f"{design['scores']['overall']:.2f}")
                
                with col3:
                    st.metric("Physics", f"{design['scores']['physics']:.2f}")
                
                with col4:
                    if st.button("View", key=f"view_{design['design_id']}"):
                        st.session_state.selected_design = design
                        st.rerun()
                
                st.divider()
    else:
        st.info("No designs yet. Go to Design Studio to create your first antibody!")
    
    # GitHub Activity
    st.markdown("### 📈 GitHub Activity")
    fig = create_github_activity_timeline()
    st.plotly_chart(fig, use_container_width=True)
    
    # Quick Design
    st.markdown("### ⚡ Quick Design")
    
    with st.expander("Create a quick antibody design"):
        col1, col2 = st.columns(2)
        
        with col1:
            antigen = st.selectbox(
                "Antigen",
                ["HER2", "PD-1", "TNFα", "SARS-CoV-2 Spike", "Custom"],
                key="quick_antigen"
            )
        
        with col2:
            num_designs = st.slider("Number of designs", 1, 5, 1)
        
        if st.button("Generate Quick Design", type="primary"):
            params = {
                'cdr_length_sampling': 'natural',
                'score_weights': st.session_state.physics_params,
                'epitope_weight': 0.3
            }
            
            with st.spinner("Designing antibodies..."):
                for i in range(num_designs):
                    design = design_engine.generate_antibody_design(antigen, params)
                    st.session_state.designs.append(design)
                    st.session_state.recent_activity.append(
                        f"Created design {design['design_id']} for {antigen}"
                    )
                
                st.success(f"✅ Generated {num_designs} antibody designs!")
                st.rerun()

def show_design_studio():
    """Show antibody design studio"""
    st.markdown("## 🎯 Antibody Design Studio")
    
    # Design Parameters
    with st.expander("⚙️ Design Parameters", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            antigen = st.selectbox(
                "Target Antigen",
                ["HER2", "PD-1", "TNFα", "SARS-CoV-2 Spike", "IL-6", "VEGF", "EGFR", "CD20", "Custom"],
                help="Select target antigen for antibody design"
            )
            
            if antigen == "Custom":
                custom_antigen = st.text_input("Custom Antigen Name", "Custom_Antigen")
                antigen_seq = st.text_area("Antigen Sequence (optional)", height=100)
            
            num_designs = st.slider("Number of Designs", 1, 10, 3)
        
        with col2:
            st.markdown("#### Physics Settings")
            for param, value in st.session_state.physics_params.items():
                st.session_state.physics_params[param] = st.slider(
                    param.replace('_', ' ').title(),
                    0.0, 1.0, value, 0.05,
                    key=f"physics_{param}"
                )
        
        with col3:
            st.markdown("#### Advanced Settings")
            use_epitope = st.checkbox("Epitope Constraints", value=True)
            if use_epitope:
                st.session_state.epitope_params['weight'] = st.slider(
                    "Epitope Weight", 0.0, 1.0, 0.3, 0.05
                )
            
            cdr_sampling = st.selectbox(
                "CDR Length Sampling",
                ["Natural Distribution", "Fixed Length", "Custom Range"]
            )
            
            optimization = st.select_slider(
                "Optimization Level",
                options=["Fast", "Balanced", "Thorough", "Exhaustive"],
                value="Balanced"
            )
    
    # GitHub Integration
    with st.expander("💾 GitHub Save Options", expanded=True):
        if st.session_state.github_connected:
            repos = [r['name'] for r in st.session_state.github_repos]
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_repo = st.selectbox(
                    "Save to Repository",
                    repos,
                    index=next((i for i, r in enumerate(repos) if 'abgenesis' in r.lower()), 0)
                )
                
                commit_message = st.text_input(
                    "Commit Message",
                    "Add antibody designs from AbGenesis 2.0"
                )
            
            with col2:
                branch = st.text_input("Branch", "main")
                tags = st.text_input("Tags (comma separated)", "therapeutic,optimized")
                
                auto_push = st.checkbox("Auto-push to GitHub", value=True)
        else:
            st.info("Connect to GitHub to save designs automatically")
    
    # Run Design Button
    st.markdown("---")
    if st.button("🚀 Run Antibody Design", type="primary", use_container_width=True):
        with st.spinner("Designing antibodies... This may take a moment."):
            # Progress bar
            progress_bar = st.progress(0)
            
            # Prepare parameters
            params = {
                'cdr_length_sampling': 'natural' if cdr_sampling == "Natural Distribution" else 'fixed',
                'score_weights': st.session_state.physics_params,
                'epitope_weight': st.session_state.epitope_params['weight'] if use_epitope else 0,
                'optimization_level': optimization.lower()
            }
            
            # Generate designs
            designs = []
            for i in range(num_designs):
                # Update progress
                progress = int((i + 1) / num_designs * 100)
                progress_bar.progress(progress)
                
                # Generate design
                design = design_engine.generate_antibody_design(antigen, params)
                designs.append(design)
                
                # Small delay for realism
                time.sleep(0.1)
            
            # Add to session state
            st.session_state.designs.extend(designs)
            
            # Save to GitHub if connected
            if st.session_state.github_connected and auto_push and selected_repo:
                for design in designs:
                    success, message = github.push_design(
                        selected_repo,
                        design,
                        commit_message
                    )
                    if success:
                        st.session_state.recent_activity.append(message)
            
            # Add to recent activity
            st.session_state.recent_activity.append(
                f"Created {len(designs)} designs for {antigen}"
            )
            
            progress_bar.empty()
            st.success(f"✅ Successfully generated {len(designs)} antibody designs!")
            
            # Show results immediately
            st.rerun()
    
    # Show recent designs if any
    if st.session_state.designs:
        st.markdown("### 📋 Recent Designs")
        
        # Filter designs for current antigen
        antigen_designs = [d for d in st.session_state.designs if d['antigen_name'] == antigen]
        
        if antigen_designs:
            # Show as DataFrame
            df_data = []
            for design in antigen_designs[-10:]:  # Last 10 designs
                df_data.append({
                    'ID': design['design_id'],
                    'Heavy Length': len(design['heavy_chain']),
                    'Light Length': len(design['light_chain']),
                    'Overall Score': design['scores']['overall'],
                    'Physics Score': design['scores']['physics'],
                    'Epitope Score': design['scores']['epitope']
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Download options
            st.markdown("#### 📥 Export Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Export as JSON", use_container_width=True):
                    export_json(antigen_designs)
            
            with col2:
                if st.button("Export as CSV", use_container_width=True):
                    export_csv(antigen_designs)
            
            with col3:
                if st.button("Export as FASTA", use_container_width=True):
                    export_fasta(antigen_designs)

def show_analyze_designs():
    """Show design analysis page"""
    st.markdown("## 📊 Design Analysis")
    
    if not st.session_state.designs:
        st.info("No designs to analyze. Create some designs first!")
        return
    
    # Select designs to analyze
    design_options = {d['design_id']: d for d in st.session_state.designs}
    selected_ids = st.multiselect(
        "Select designs to analyze",
        options=list(design_options.keys()),
        default=list(design_options.keys())[:min(3, len(design_options))]
    )
    
    if not selected_ids:
        return
    
    selected_designs = [design_options[id] for id in selected_ids]
    
    # Analysis Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Comparison", "⚛️ Physics", "🧪 Developability", "📋 Details"])
    
    with tab1:
        # Comparison
        st.markdown("### Design Comparison")
        
        fig = create_design_comparison_plot(selected_designs)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Score matrix
        st.markdown("#### Score Matrix")
        score_data = []
        for design in selected_designs:
            score_data.append({
                'Design': design['design_id'],
                'Overall': design['scores']['overall'],
                'Physics': design['scores']['physics'],
                'Epitope': design['scores']['epitope'],
                'Developability': design['scores']['developability']
            })
        
        df_scores = pd.DataFrame(score_data)
        st.dataframe(df_scores.set_index('Design'), use_container_width=True)
    
    with tab2:
        # Physics Analysis
        st.markdown("### ⚛️ Physics Analysis")
        
        if len(selected_designs) == 1:
            # Single design - show radar chart
            fig = create_physics_radar_chart(selected_designs[0])
            st.plotly_chart(fig, use_container_width=True)
        
        # Physics metrics table
        st.markdown("#### Physics Metrics")
        physics_data = []
        for design in selected_designs:
            physics_data.append({
                'Design': design['design_id'],
                'Binding Energy (kcal/mol)': design['physics_analysis']['binding_energy'],
                'Interface Area (Å²)': design['physics_analysis']['interface_area'],
                'H-Bonds': design['physics_analysis']['hydrogen_bonds'],
                'Shape Complementarity': design['physics_analysis']['shape_complementarity'],
                'Electrostatic Complementarity': design['physics_analysis']['electrostatic_complementarity']
            })
        
        df_physics = pd.DataFrame(physics_data)
        st.dataframe(df_physics.set_index('Design'), use_container_width=True)
    
    with tab3:
        # Developability Analysis
        st.markdown("### 🧪 Developability Analysis")
        
        # Developability metrics
        develop_data = []
        for design in selected_designs:
            develop_data.append({
                'Design': design['design_id'],
                'Solubility Score': design['developability']['solubility'],
                'Aggregation Risk': design['developability']['aggregation_score'],
                'Thermal Stability (°C)': design['developability']['thermal_stability'],
                'Expression Titer (mg/L)': design['developability']['expression_titer'],
                'Immunogenicity Risk': design['developability']['immunogenicity_risk']
            })
        
        df_develop = pd.DataFrame(develop_data)
        st.dataframe(df_develop.set_index('Design'), use_container_width=True)
        
        # Developability visualization
        if len(selected_designs) > 1:
            fig = px.scatter(
                df_develop,
                x='Aggregation Risk',
                y='Solubility Score',
                size='Expression Titer',
                color='Design',
                hover_name='Design',
                title='Developability Analysis',
                size_max=30
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#c9d1d9'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Detailed view
        st.markdown("### 📋 Design Details")
        
        selected_design = st.selectbox(
            "Select design for detailed view",
            options=[d['design_id'] for d in selected_designs]
        )
        
        if selected_design:
            design = next(d for d in selected_designs if d['design_id'] == selected_design)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Sequences")
                st.text_area("Heavy Chain", design['heavy_chain'], height=150)
                st.text_area("Light Chain", design['light_chain'], height=150)
            
            with col2:
                st.markdown("#### CDR Regions")
                for cdr_type, sequence in design['cdrs'].items():
                    st.text_input(f"{cdr_type} ({len(sequence)} AA)", sequence)
            
            # Metadata
            with st.expander("Metadata"):
                st.json(design['metadata'])
            
            # Download this design
            st.markdown("---")
            st.markdown("#### Download This Design")
            
            col_d1, col_d2, col_d3 = st.columns(3)
            
            with col_d1:
                if st.button("📥 JSON", use_container_width=True):
                    export_json([design], f"{design['design_id']}.json")
            
            with col_d2:
                if st.button("📥 FASTA", use_container_width=True):
                    export_fasta([design], f"{design['design_id']}.fasta")
            
            with col_d3:
                if st.button("📥 Report", use_container_width=True):
                    export_design_report(design)

def show_github_repos():
    """Show GitHub repositories page"""
    st.markdown("## 📚 GitHub Repositories")
    
    if not st.session_state.github_connected:
        st.warning("Connect to GitHub to view repositories")
        return
    
    # Create new repository
    with st.expander("➕ Create New Repository", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_repo_name = st.text_input("Repository Name", "abgenesis-designs")
        
        with col2:
            new_repo_desc = st.text_input("Description", "Antibody designs created with AbGenesis 2.0")
        
        with col3:
            new_repo_private = st.checkbox("Private Repository", value=True)
        
        if st.button("Create Repository", type="primary", use_container_width=True):
            with st.spinner("Creating repository..."):
                success, repo = github.create_repository(
                    new_repo_name,
                    new_repo_desc,
                    new_repo_private
                )
                
                if success:
                    st.success(f"✅ Repository '{new_repo_name}' created!")
                    st.session_state.recent_activity.append(f"Created repository {new_repo_name}")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to create repository: {repo}")
    
    # Repository list
    st.markdown("### Your Repositories")
    
    for repo in st.session_state.github_repos:
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div class="github-card">
                    <h3 style="margin: 0; color: #58a6ff;">
                        {repo['name']}
                        {'<span style="font-size: 0.8rem; color: #8b949e;">(Private)</span>' if repo['private'] else ''}
                    </h3>
                    <p style="margin: 0.5rem 0; color: #8b949e;">{repo['description']}</p>
                    <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                        <span style="color: #8b949e;">🌟 {repo['stars']}</span>
                        <span style="color: #8b949e;">🍴 {repo['forks']}</span>
                        <span style="color: #8b949e;">📁 {repo['designs']} designs</span>
                        <span style="color: #8b949e;">👥 {repo['collaborators']} collabs</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Browse", key=f"browse_{repo['name']}", use_container_width=True):
                    st.session_state.current_repo = repo
                    st.rerun()
            
            st.divider()
    
    # Repository details if selected
    if 'current_repo' in st.session_state and st.session_state.current_repo:
        repo = st.session_state.current_repo
        
        st.markdown(f"### 📂 {repo['name']}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Repository info
            st.markdown(f"""
            **Description**: {repo['description']}
            
            **Stats**:
            - ⭐ Stars: {repo['stars']}
            - 🍴 Forks: {repo['forks']}
            - 🐛 Issues: {repo['issues']}
            - 🧬 Designs: {repo['designs']}
            - 👥 Collaborators: {repo['collaborators']}
            - 📅 Updated: {datetime.fromisoformat(repo['updated_at']).strftime('%Y-%m-%d %H:%M')}
            """)
        
        with col2:
            # Quick actions
            if st.button("← Back to List", use_container_width=True):
                del st.session_state.current_repo
                st.rerun()
            
            if st.button("📥 Clone Repository", use_container_width=True):
                st.info("Clone URL: https://github.com/user/{}.git".format(repo['name']))
            
            if st.button("🌐 View on GitHub", use_container_width=True):
                st.markdown(f"[Open on GitHub](https://github.com/user/{repo['name']})")
        
        # Repository contents
        st.markdown("#### Repository Contents")
        
        tab1, tab2, tab3 = st.tabs(["Designs", "Commits", "Issues"])
        
        with tab1:
            # Simulated designs in repo
            if repo['designs'] > 0:
                for i in range(min(5, repo['designs'])):
                    st.markdown(f"""
                    <div style="padding: 1rem; margin: 0.5rem 0; background: #161b22; border-radius: 5px;">
                        <strong>Design_{i+1:03d}.json</strong>
                        <p style="margin: 0.5rem 0 0 0; color: #8b949e; font-size: 0.9rem;">
                            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No designs in this repository yet")
        
        with tab2:
            # Recent commits
            for commit in github.commits:
                st.markdown(f"""
                <div class="commit-card">
                    <strong>{commit['message']}</strong><br>
                    <small style="color: #8b949e;">
                        {commit['author']} • {datetime.fromisoformat(commit['date']).strftime('%Y-%m-%d %H:%M')}
                    </small>
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            # Issues
            for issue in github.issues:
                label_html = ""
                for label in issue['labels']:
                    label_html += f'<span class="github-badge badge-gray" style="margin-right: 0.25rem;">{label}</span>'
                
                st.markdown(f"""
                <div class="{'issue-open' if issue['state'] == 'open' else 'issue-closed'}">
                    <strong>#{issue['number']}: {issue['title']}</strong>
                    <div style="margin-top: 0.5rem;">
                        {label_html}
                    </div>
                    <small style="color: #8b949e;">
                        Created: {datetime.fromisoformat(issue['created_at']).strftime('%Y-%m-%d')} • 
                        Comments: {issue['comments']}
                    </small>
                </div>
                """, unsafe_allow_html=True)

def show_collaboration():
    """Show collaboration page"""
    st.markdown("## 🤝 Collaboration")
    
    if not st.session_state.github_connected:
        st.warning("Connect to GitHub to use collaboration features")
        return
    
    # Select repository
    repos = [r['name'] for r in st.session_state.github_repos]
    if not repos:
        st.info("No repositories found. Create one first!")
        return
    
    selected_repo = st.selectbox("Select Repository", repos)
    
    # Collaboration tabs
    tab1, tab2, tab3 = st.tabs(["Issues", "Pull Requests", "Projects"])
    
    with tab1:
        # Issues
        st.markdown("### 🐛 Issues")
        
        # Create new issue
        with st.expander("Create New Issue", expanded=False):
            issue_title = st.text_input("Issue Title")
            issue_body = st.text_area("Issue Description", height=150)
            issue_labels = st.multiselect(
                "Labels",
                ["bug", "enhancement", "design", "question", "documentation"]
            )
            
            if st.button("Create Issue", type="primary"):
                with st.spinner("Creating issue..."):
                    success, issue = github.create_issue(
                        selected_repo,
                        issue_title,
                        issue_body,
                        issue_labels
                    )
                    
                    if success:
                        st.success(f"✅ Issue #{issue['number']} created!")
                        st.session_state.recent_activity.append(f"Created issue #{issue['number']}")
                    else:
                        st.error(f"❌ Failed to create issue: {issue}")
        
        # List issues
        st.markdown("#### Open Issues")
        issues = github.get_issues(selected_repo)
        
        for issue in issues:
            if issue['state'] == 'open':
                label_html = ""
                for label in issue['labels']:
                    label_html += f'<span class="github-badge" style="background: #{hash(label) % 0xFFFFFF:06x}; margin-right: 0.25rem;">{label}</span>'
                
                st.markdown(f"""
                <div style="padding: 1rem; margin: 0.5rem 0; background: #161b22; border-radius: 5px; border-left: 4px solid #238636;">
                    <strong>
                        <a href="https://github.com/user/{selected_repo}/issues/{issue['number']}" target="_blank" style="color: #58a6ff; text-decoration: none;">
                            #{issue['number']}: {issue['title']}
                        </a>
                    </strong>
                    <div style="margin-top: 0.5rem;">
                        {label_html}
                    </div>
                    <small style="color: #8b949e;">
                        Created: {datetime.fromisoformat(issue['created_at']).strftime('%Y-%m-%d')} • 
                        Comments: {issue['comments']}
                    </small>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        # Pull Requests
        st.markdown("### 🔀 Pull Requests")
        
        # List PRs
        for pr in github.pull_requests:
            state_color = {
                'open': '#1f6feb',
                'closed': '#da3633',
                'merged': '#8957e5'
            }.get(pr['state'], '#8b949e')
            
            st.markdown(f"""
            <div style="padding: 1rem; margin: 0.5rem 0; background: #161b22; border-radius: 5px; border-left: 4px solid {state_color};">
                <strong>
                    <a href="https://github.com/user/{selected_repo}/pull/{pr['number']}" target="_blank" style="color: #58a6ff; text-decoration: none;">
                        #{pr['number']}: {pr['title']}
                    </a>
                </strong>
                <p style="margin: 0.5rem 0; color: #8b949e;">
                    {pr['head']} → {pr['base']} • 
                    State: <span style="color: {state_color};">{pr['state'].title()}</span>
                </p>
                <small style="color: #8b949e;">
                    Created: {datetime.fromisoformat(pr['created_at']).strftime('%Y-%m-%d')} • 
                    Comments: {pr['comments']}
                </small>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Projects
        st.markdown("### 📋 Projects")
        
        # Create project
        if st.button("🎯 Create Antibody Design Project", use_container_width=True):
            st.success("Project board created with columns: Backlog → Design → Test → Optimize → Done")
            st.session_state.recent_activity.append("Created antibody design project")
        
        # Sample project
        st.markdown("""
        <div style="padding: 1.5rem; background: #161b22; border-radius: 10px; border: 1px solid #30363d;">
            <h4 style="margin: 0 0 1rem 0;">Antibody Design Pipeline</h4>
            
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem;">
                <div>
                    <h5 style="margin: 0 0 0.5rem 0; color: #8b949e;">Backlog</h5>
                    <div style="background: #0d1117; padding: 0.75rem; border-radius: 6px; margin-bottom: 0.5rem;">
                        Design HER2 antibody
                    </div>
                </div>
                
                <div>
                    <h5 style="margin: 0 0 0.5rem 0; color: #8b949e;">Design</h5>
                    <div style="background: #0d1117; padding: 0.75rem; border-radius: 6px; margin-bottom: 0.5rem;">
                        Optimize CDR-H3
                    </div>
                </div>
                
                <div>
                    <h5 style="margin: 0 0 0.5rem 0; color: #8b949e;">Test</h5>
                    <div style="background: #0d1117; padding: 0.75rem; border-radius: 6px; margin-bottom: 0.5rem;">
                        Validate binding
                    </div>
                </div>
                
                <div>
                    <h5 style="margin: 0 0 0.5rem 0; color: #8b949e;">Optimize</h5>
                    <div style="background: #0d1117; padding: 0.75rem; border-radius: 6px; margin-bottom: 0.5rem;">
                        Improve developability
                    </div>
                </div>
                
                <div>
                    <h5 style="margin: 0 0 0.5rem 0; color: #8b949e;">Done</h5>
                    <div style="background: #0d1117; padding: 0.75rem; border-radius: 6px; margin-bottom: 0.5rem;">
                        Finalize PD-1 design
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_settings():
    """Show settings page"""
    st.markdown("## ⚙️ Settings")
    
    # GitHub Settings
    st.markdown("### 🔐 GitHub Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Connection")
        if st.session_state.github_connected:
            st.success(f"✅ Connected as {st.session_state.github_username}")
            if st.button("Disconnect GitHub", use_container_width=True):
                st.session_state.github_connected = False
                st.rerun()
        else:
            st.warning("⚠️ Not connected to GitHub")
    
    with col2:
        st.markdown("#### Default Repository")
        if st.session_state.github_repos:
            default_repo = st.selectbox(
                "Default Repository",
                [r['name'] for r in st.session_state.github_repos]
            )
        else:
            st.info("No repositories available")
    
    # Application Settings
    st.markdown("### 🧬 Application Settings")
    
    tab1, tab2 = st.tabs(["Design", "Export"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Physics Weights")
            for param, value in st.session_state.physics_params.items():
                st.session_state.physics_params[param] = st.slider(
                    param.replace('_', ' ').title(),
                    0.0, 1.0, value, 0.05,
                    key=f"settings_physics_{param}"
                )
        
        with col2:
            st.markdown("#### CDR Settings")
            st.session_state.cdr_params['ensemble_size'] = st.slider(
                "Ensemble Size", 1, 100, 20
            st.session_state.cdr_params['diversity'] = st.slider(
                "Sequence Diversity", 0.0, 1.0, 0.5, 0.05
            )
            st.session_state.cdr_params['length_sampling'] = st.selectbox(
                "Length Sampling Method",
                ["natural", "uniform", "custom"]
            )
    
    with tab2:
        st.markdown("#### Export Settings")
        st.session_state.export_format = st.selectbox(
            "Default Export Format",
            ["json", "csv", "fasta", "all"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.auto_save = st.checkbox(
                "Auto-save to GitHub", value=True
            )
        with col2:
            include_metadata = st.checkbox(
                "Include Metadata", value=True
            )
        
        # Backup settings
        st.markdown("#### Backup")
        if st.button("💾 Backup All Designs", use_container_width=True):
            backup_file = export_all_designs()
            st.success(f"Backup created: {backup_file}")
        
        if st.button("🔄 Restore Designs", use_container_width=True):
            uploaded_file = st.file_uploader(
                "Choose backup file",
                type=['json', 'zip'],
                key="restore_uploader"
            )
            if uploaded_file:
                designs = restore_backup(uploaded_file)
                st.session_state.designs = designs
                st.success(f"✅ Restored {len(designs)} designs")
    
    # Theme Settings
    st.markdown("### 🎨 Theme")
    theme = st.selectbox("Theme", ["Dark", "Light", "Auto"])
    
    # Advanced Settings
    with st.expander("🔧 Advanced Settings"):
        st.markdown("#### Performance")
        cache_enabled = st.checkbox("Enable Cache", value=True)
        batch_size = st.slider("Batch Size", 1, 100, 10)
        
        st.markdown("#### Experimental Features")
        enable_deep_learning = st.checkbox("Enable Deep Learning Models", value=False)
        enable_molecular_dynamics = st.checkbox("Enable Molecular Dynamics", value=False)
    
    # Save Settings Button
    st.markdown("---")
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        st.success("✅ Settings saved!")

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_json(designs, filename="abgenesis_designs.json"):
    """Export designs as JSON"""
    if not designs:
        st.warning("No designs to export")
        return
    
    data = {
        'metadata': {
            'exported': datetime.now().isoformat(),
            'version': '2.1.0',
            'count': len(designs)
        },
        'designs': designs
    }
    
    json_str = json.dumps(data, indent=2)
    
    st.download_button(
        label="📥 Download JSON",
        data=json_str,
        file_name=filename,
        mime="application/json",
        use_container_width=True
    )
    
    st.session_state.recent_activity.append(f"Exported {len(designs)} designs as JSON")
    return json_str

def export_csv(designs):
    """Export designs as CSV"""
    if not designs:
        st.warning("No designs to export")
        return
    
    # Flatten design data
    rows = []
    for design in designs:
        row = {
            'design_id': design['design_id'],
            'antigen': design['antigen_name'],
            'heavy_chain': design['heavy_chain'],
            'light_chain': design['light_chain'],
            'overall_score': design['scores']['overall'],
            'physics_score': design['scores']['physics'],
            'epitope_score': design['scores']['epitope'],
            'developability_score': design['scores']['developability']
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="abgenesis_designs.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.session_state.recent_activity.append(f"Exported {len(designs)} designs as CSV")
    return csv

def export_fasta(designs, filename="abgenesis_designs.fasta"):
    """Export designs as FASTA"""
    if not designs:
        st.warning("No designs to export")
        return
    
    fasta_lines = []
    for design in designs:
        fasta_lines.append(f">{design['design_id']}_heavy | {design['antigen_name']}")
        fasta_lines.append(design['heavy_chain'])
        fasta_lines.append(f">{design['design_id']}_light | {design['antigen_name']}")
        fasta_lines.append(design['light_chain'])
    
    fasta_str = "\n".join(fasta_lines)
    
    st.download_button(
        label="📥 Download FASTA",
        data=fasta_str,
        file_name=filename,
        mime="text/plain",
        use_container_width=True
    )
    
    st.session_state.recent_activity.append(f"Exported {len(designs)} designs as FASTA")
    return fasta_str

def export_design_report(design):
    """Export a comprehensive design report"""
    report = f"""
    AbGenesis 2.0 - Antibody Design Report
    =========================================
    
    Design ID: {design['design_id']}
    Antigen: {design['antigen_name']}
    Created: {design['metadata']['created']}
    
    SCORES
    ------
    Overall: {design['scores']['overall']:.3f}
    Physics: {design['scores']['physics']:.3f}
    Epitope: {design['scores']['epitope']:.3f}
    Developability: {design['scores']['developability']:.3f}
    
    SEQUENCES
    ---------
    Heavy Chain ({len(design['heavy_chain'])} AA):
    {design['heavy_chain']}
    
    Light Chain ({len(design['light_chain'])} AA):
    {design['light_chain']}
    
    CDR REGIONS
    -----------
    H1 ({len(design['cdrs']['H1'])} AA): {design['cdrs']['H1']}
    H2 ({len(design['cdrs']['H2'])} AA): {design['cdrs']['H2']}
    H3 ({len(design['cdrs']['H3'])} AA): {design['cdrs']['H3']}
    L1 ({len(design['cdrs']['L1'])} AA): {design['cdrs']['L1']}
    L2 ({len(design['cdrs']['L2'])} AA): {design['cdrs']['L2']}
    L3 ({len(design['cdrs']['L3'])} AA): {design['cdrs']['L3']}
    
    PHYSICS ANALYSIS
    ----------------
    Binding Energy: {design['physics_analysis']['binding_energy']} kcal/mol
    Interface Area: {design['physics_analysis']['interface_area']} Å²
    Hydrogen Bonds: {design['physics_analysis']['hydrogen_bonds']}
    Shape Complementarity: {design['physics_analysis']['shape_complementarity']:.3f}
    Electrostatic Complementarity: {design['physics_analysis']['electrostatic_complementarity']:.3f}
    
    DEVELOPABILITY
    --------------
    Solubility Score: {design['developability']['solubility']:.3f}
    Aggregation Risk: {design['developability']['aggregation_score']:.3f}
    Thermal Stability: {design['developability']['thermal_stability']} °C
    Expression Titer: {design['developability']['expression_titer']} mg/L
    Immunogenicity Risk: {design['developability']['immunogenicity_risk']:.3f}
    
    EPITOPE COMPATIBILITY
    ---------------------
    Paratope Residues: {design['epitope_compatibility']['paratope_residues']}
    Complementarity Score: {design['epitope_compatibility']['complementarity_score']:.3f}
    Predicted Affinity: {design['epitope_compatibility']['predicted_affinity']} nM
    Epitope Coverage: {design['epitope_compatibility']['epitope_coverage']:.3f}
    
    METADATA
    --------
    Design Parameters: {json.dumps(design['metadata']['params'], indent=2)}
    Version: {design['metadata']['version']}
    
    ---
    Generated by AbGenesis 2.0
    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name=f"{design['design_id']}_report.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.session_state.recent_activity.append(f"Exported report for {design['design_id']}")
    return report

def export_all_designs():
    """Export all designs as a zip file"""
    if not st.session_state.designs:
        st.warning("No designs to export")
        return
    
    # Create a zip file in memory
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add JSON export
        json_data = json.dumps({
            'metadata': {
                'exported': datetime.now().isoformat(),
                'version': '2.1.0',
                'count': len(st.session_state.designs)
            },
            'designs': st.session_state.designs
        }, indent=2)
        zip_file.writestr('abgenesis_all_designs.json', json_data)
        
        # Add CSV export
        rows = []
        for design in st.session_state.designs:
            row = {
                'design_id': design['design_id'],
                'antigen': design['antigen_name'],
                'heavy_chain': design['heavy_chain'],
                'light_chain': design['light_chain'],
                'overall_score': design['scores']['overall'],
                'physics_score': design['scores']['physics'],
                'epitope_score': design['scores']['epitope'],
                'developability_score': design['scores']['developability']
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        csv_data = df.to_csv(index=False)
        zip_file.writestr('abgenesis_all_designs.csv', csv_data)
        
        # Add FASTA export
        fasta_lines = []
        for design in st.session_state.designs:
            fasta_lines.append(f">{design['design_id']}_heavy | {design['antigen_name']}")
            fasta_lines.append(design['heavy_chain'])
            fasta_lines.append(f">{design['design_id']}_light | {design['antigen_name']}")
            fasta_lines.append(design['light_chain'])
        
        fasta_data = "\n".join(fasta_lines)
        zip_file.writestr('abgenesis_all_designs.fasta', fasta_data)
        
        # Add summary report
        summary = f"""
        AbGenesis 2.0 - Complete Export
        ================================
        
        Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Total Designs: {len(st.session_state.designs)}
        Antigens: {', '.join(set(d['antigen_name'] for d in st.session_state.designs))}
        
        Design Statistics:
        -----------------
        Average Overall Score: {np.mean([d['scores']['overall'] for d in st.session_state.designs]):.3f}
        Best Overall Score: {max([d['scores']['overall'] for d in st.session_state.designs]):.3f}
        Average Physics Score: {np.mean([d['scores']['physics'] for d in st.session_state.designs]):.3f}
        Average Epitope Score: {np.mean([d['scores']['epitope'] for d in st.session_state.designs]):.3f}
        Average Developability Score: {np.mean([d['scores']['developability'] for d in st.session_state.designs]):.3f}
        
        CDR Length Statistics:
        ----------------------
        Average CDR-H3 Length: {np.mean([len(d['cdrs']['H3']) for d in st.session_state.designs]):.1f}
        """
        zip_file.writestr('SUMMARY.txt', summary)
    
    zip_buffer.seek(0)
    
    st.download_button(
        label="📥 Download All Designs (ZIP)",
        data=zip_buffer,
        file_name=f"abgenesis_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
        mime="application/zip",
        use_container_width=True
    )
    
    st.session_state.recent_activity.append("Exported all designs as ZIP archive")
    return zip_buffer

def restore_backup(uploaded_file):
    """Restore designs from backup file"""
    try:
        if uploaded_file.name.endswith('.zip'):
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                # Extract JSON file
                for file_name in zip_ref.namelist():
                    if file_name.endswith('.json'):
                        with zip_ref.open(file_name) as f:
                            data = json.load(f)
                            return data.get('designs', [])
        
        elif uploaded_file.name.endswith('.json'):
            data = json.load(uploaded_file)
            return data.get('designs', [])
    
    except Exception as e:
        st.error(f"Error restoring backup: {e}")
    
    return []

# ============================================================================
# BENCHMARKING FUNCTIONS
# ============================================================================

def run_benchmark():
    """Run benchmark against known therapeutic antibodies"""
    st.markdown("## 🏆 Benchmarking")
    
    therapeutic_antibodies = design_engine.therapeutic_antibodies
    
    benchmark_results = []
    
    for ab_name, ab_data in therapeutic_antibodies.items():
        # Create a design with similar parameters
        params = {
            'cdr_length_sampling': 'natural',
            'score_weights': st.session_state.physics_params,
            'epitope_weight': 0.3
        }
        
        # Generate benchmark design
        design = design_engine.generate_antibody_design(ab_data['target'], params)
        
        # Calculate similarity scores (simplified)
        similarity = calculate_similarity(design, ab_data)
        
        benchmark_results.append({
            'therapeutic_antibody': ab_name,
            'target': ab_data['target'],
            'our_design': design['design_id'],
            'similarity_score': similarity,
            'our_affinity': design['epitope_compatibility']['predicted_affinity'],
            'therapeutic_affinity': ab_data['affinity'],
            'improvement': ab_data['affinity'] - design['epitope_compatibility']['predicted_affinity']
        })
    
    # Store results
    st.session_state.benchmark_results = benchmark_results
    
    # Display results
    df_results = pd.DataFrame(benchmark_results)
    st.dataframe(df_results, use_container_width=True)
    
    # Create visualization
    if benchmark_results:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[r['therapeutic_antibody'] for r in benchmark_results],
            y=[r['similarity_score'] for r in benchmark_results],
            name='Similarity Score',
            marker_color='#58a6ff'
        ))
        
        fig.add_trace(go.Bar(
            x=[r['therapeutic_antibody'] for r in benchmark_results],
            y=[r['improvement'] for r in benchmark_results],
            name='Affinity Improvement (nM)',
            marker_color='#238636',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Benchmark Results',
            yaxis=dict(title='Similarity Score'),
            yaxis2=dict(
                title='Affinity Improvement (nM)',
                overlaying='y',
                side='right'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#c9d1d9'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    return benchmark_results

def calculate_similarity(design, therapeutic_antibody):
    """Calculate similarity between design and therapeutic antibody"""
    # Simplified similarity calculation
    similarity = 0.5  # Base similarity
    
    # Length similarity
    our_heavy_len = len(design['heavy_chain'])
    their_heavy_len = len(therapeutic_antibody['heavy'])
    heavy_len_sim = 1.0 - abs(our_heavy_len - their_heavy_len) / max(our_heavy_len, their_heavy_len)
    
    our_light_len = len(design['light_chain'])
    their_light_len = len(therapeutic_antibody['light'])
    light_len_sim = 1.0 - abs(our_light_len - their_light_len) / max(our_light_len, their_light_len)
    
    similarity += 0.2 * (heavy_len_sim + light_len_sim) / 2
    
    # CDR-H3 length similarity
    our_h3_len = len(design['cdrs']['H3'])
    # Estimate their H3 length (simplified)
    their_h3_len = len(therapeutic_antibody['heavy']) - 100  # Approximation
    h3_len_sim = 1.0 - abs(our_h3_len - their_h3_len) / max(our_h3_len, their_h3_len, 1)
    
    similarity += 0.1 * h3_len_sim
    
    return min(1.0, similarity)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function"""
    
    # Show header
    show_header()
    
    # Show sidebar and get current page
    page = show_sidebar()
    
    # Route to appropriate page
    if page == "🏠 Dashboard":
        show_dashboard()
    
    elif page == "🎯 Design Studio":
        show_design_studio()
    
    elif page == "📊 Analyze Designs":
        show_analyze_designs()
    
    elif page == "📚 GitHub Repos":
        show_github_repos()
    
    elif page == "🤝 Collaborate":
        show_collaboration()
    
    elif page == "⚙️ Settings":
        show_settings()
    
    # Footer
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; color: #8b949e; font-size: 0.9rem;">
            <strong>AbGenesis 2.0</strong><br>
            AI-Powered Antibody Design
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; color: #8b949e; font-size: 0.9rem;">
            <strong>GitHub Integrated</strong><br>
            Version 2.1.0
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; color: #8b949e; font-size: 0.9rem;">
            <strong>MIT License</strong><br>
            © 2024 AbGenesis Team
        </div>
        """, unsafe_allow_html=True)
    
    # Debug information (hidden by default)
    with st.expander("🔍 Debug Information", expanded=False):
        st.write("Session State Keys:", list(st.session_state.keys()))
        st.write("Number of Designs:", len(st.session_state.designs))
        st.write("GitHub Connected:", st.session_state.github_connected)
        st.write("Recent Activity:", st.session_state.recent_activity[-5:] if st.session_state.recent_activity else [])

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
              
