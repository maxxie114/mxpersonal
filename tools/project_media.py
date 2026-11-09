"""Case-study illustrations and their source documents."""
from dataclasses import dataclass

from content import GITHUB, POSTER


@dataclass(frozen=True)
class Figure:
    asset: str
    width: int
    height: int
    alt: str
    caption: str
    source: str = ""


FEATURED = ("foxstar", "aml-gnn", "intel-marketplace", "loopless", "litmus", "ml-from-scratch")

FIGURES = {
    "foxstar": (
        Figure("figures/foxstar.webp", 2400, 1600,
               "WeChat messages enter a queue, pass through routing and reply checks, and reach the model or a specialized tool.",
               "The FoxStar Agent architecture shows where it decides to reply and how a message reaches the model, scheduler or tools."),
    ),
    "aml-gnn": (
        Figure("figures/aml-gnn.webp", 594, 432,
               "Test confusion matrix: 131 true positives, 905 false negatives, 87,716 false positives and 926,917 true negatives.",
               "At the threshold used in this notebook run, the model detected 131 of 1,036 labeled positives. The 87,716 false alarms show the cost of operating at that threshold.",
               GITHUB + "/csc871-anti-money-laundering-ibm-gnn/blob/cf27b156af0d/anti_money_laundering_ibm.ipynb"),
        Figure("aml-baseline-curves.webp", 1100, 450, "Validation and test ROC and precision–recall curves for the tabular MLP.",
               "The tabular baseline provides a comparison for the graph models. The precision–recall curve shows how precision changes as more positives are recovered.",
               GITHUB + "/csc871-anti-money-laundering-ibm-gnn/blob/cf27b156af0d/plots/roc_pr_mlp.png"),
    ),
    "loopless": (
        Figure("figures/loopless.webp", 1046, 674, "Cold run, LLM judge and warm replay using a browser, cache and trace store.",
               "The README shows where the agent records actions on a first run and reuses them on a repeat visit.",
               GITHUB + "/loopless/blob/352b518076a8/README.md"),
    ),
    "real-browser-benchmark": (
        Figure("figures/real-browser-benchmark.webp", 806, 537, "A browser task and a terminal running the agent, from the team's demo.",
               "Our hackathon submission pairs the browser environment with the agent’s execution trace.",
               "https://devpost.com/software/real-hackathon-browser-agent"),
    ),
    "ultrasound-tongue-tracking": (
        Figure("figures/ultrasound-tongue-tracking.webp", 1801, 1350, "Conference poster with tongue contours for five speakers and example ultrasound frames.",
               "Our UCSC poster plots tongue shape by speaker and prosodic position. Each panel in the results column represents a different speaker.", POSTER),
    ),
    "ml-from-scratch": (
        Figure("figures/ml-from-scratch.webp", 1800, 2548, "Handwritten network design with connections between neurons, weights and equations.",
               "The first page of my handwritten design notes lays out the network and the calculations behind my Python implementation.",
               GITHUB + "/Basic_ML_Research/blob/cddf3e227fa1/deep_learning/logic_simulation/neural_network_from_scratch/Neural_Network_From_Scratch_Note.pdf"),
    ),
    "swingsage": (
        Figure("figures/swingsage.webp", 2048, 813, "The strategy and prediction modules feed a backtest before trade approval.",
               "The team report traces an order from market data through the decision modules, backtest and guardrails.",
               GITHUB + "/csc665-swingsage/blob/08671cc6e259/csc_665_final_report_team1.pdf"),
    ),
    "litmus": (
        Figure("figures/litmus.webp", 1117, 1067, "Web and WebSocket services connect the evaluation dashboard to storage, live calls and tool verification.",
               "The hackathon design specifies how a voice evaluation crosses the web application and the separate audio service.",
               GITHUB + "/Litmus/blob/8277a597d97e/Litmus_Hackathon_Spec.md"),
    ),
    "crypto-risk-agent": (
        Figure("figures/crypto-risk-agent.svg", 820, 396, "Market data, holder balances and wallet activity reach the agent through MCP tools.",
               "Data flow adapted from the repository’s tool descriptions. Each provider supplies a different part of the explanation.",
               GITHUB + "/Automatic-Crypto-Risk-Analysis-Agent/blob/ce4837082cd1/README.md"),
    ),
    "paigent-studio": (
        Figure("figures/paigent-studio.webp", 1173, 2082, "Architecture layers connecting the workflow interface, orchestrator, tools and storage.",
               "The README maps the components involved in planning a workflow and executing its tools.",
               GITHUB + "/paigent/blob/bedd82156a24/README.md"),
    ),
    "clawguard": (
        Figure("figures/clawguard.webp", 653, 314, "Gmail messages pass through retrieval, sanitization and risk scoring before delivery to the agent.",
               "The repository’s intake sequence shows where mail is checked before the agent receives a structured message.",
               GITHUB + "/ClawGuard/blob/26a524a71351/README.md"),
    ),
    "replicalab": (
        Figure("figures/replicalab.webp", 2400, 1800, "ReplicaLab system architecture connecting the scientist, lab manager, environment and judge.",
               "The team’s system diagram shows how the participants, simulation and scoring components fit together.",
               GITHUB + "/replicalab-ai/blob/3e6fec93b4ce/ReplicaLab_Architecture_Final.svg"),
    ),
    "intel-marketplace": (
        Figure("figures/intel-marketplace.webp", 1258, 542, "A buyer calls a paid endpoint, and an agent gathers information from tools and other sellers.",
               "The README traces a paid briefing request through Nevermined and into the agent’s research tools.",
               GITHUB + "/intel-marketplace/blob/725ebc1174f1/README.md"),
    ),
    "companyintel-ai": (
        Figure("figures/companyintel-ai.webp", 934, 314, "The React interface calls a FastAPI service connected to research, browsing, search, financial data, a graph and a cache.",
               "The architecture sketch identifies the services behind a company report.",
               GITHUB + "/companyintel-ai/blob/293fac1fb4d6/README.md"),
    ),
    "youtube-agent": (
        Figure("awards/frontegg.jpg", 1280, 720, "The team's YouTube Agent presentation slide for the Self-Evolving Agent Hackathon.",
               "The opening slide from our demo introduces the channel analytics project and its contributors.",
               GITHUB + "/Autonomous-Youtube-analysis-agent/blob/a06d7a8ce36c/README.md"),
    ),
}
