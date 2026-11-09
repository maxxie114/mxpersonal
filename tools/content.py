"""Reviewed public portfolio records. Only explicitly published entries render."""
from dataclasses import dataclass
from typing import Optional, Tuple

GITHUB = "https://github.com/maxxie114"
LINKEDIN = "https://www.linkedin.com/in/peixi-xie/"
EMAIL = "maxxie114@qubemc.ai"
DEVPOST = "https://devpost.com/software/crypto-risk-analysis-agent"
LITMUS_ENTRY = "https://devpost.com/software/litmus-cv5j2d"
PAPER = "dynamic-benchmarking.pdf"
PAPER_SOURCE = "assets/portfolio/dynamic-benchmarking.pdf"
POSTER = "assets/portfolio/english-r-prosodic-position.pdf"
PAPER_TITLE = "Dynamic Benchmarking of LLMs: Moving Beyond Static Evaluation"
ML_SOURCE = GITHUB + "/Basic_ML_Research/blob/cddf3e227fa18cfd83e08b51a3c5237c645ea61f/"
NETWORK_SOURCE = ML_SOURCE + "deep_learning/logic_simulation/neural_network_from_scratch/"
CAP = "project-dynamic-llm-benchmarking.html"


@dataclass(frozen=True)
class ResearchEntry:
    page: str
    title: str
    context: str
    summary: str
    resource: Optional[Tuple[str, str]] = None
    sections: tuple = ()


RESEARCH = (
    ResearchEntry(CAP, PAPER_TITLE, "M.A. capstone · San Francisco State University (SFSU) · 2026",
                  "Four models took three kinds of tests covering static knowledge, dynamic reasoning and metalinguistic analysis. Changing the benchmark changed which model led.",
                  ("Read Paper", PAPER)),
    ResearchEntry("research-text-simplification.html", "AI-Assisted Text Simplification",
                  "ECOLE Lab · San Francisco State University (SFSU)",
                  "How much of a passage’s meaning survives when a language model rewrites it for easier reading?",
                  sections=(
                      ("Comparing a passage with its rewrite", "A shorter sentence can be easier to read while saying something different. For example, changing “may cause” to “causes” removes a qualification. Looking at readability alongside meaning helps identify changes that sentence length alone would miss."),
                      ("My work at ECOLE Lab", "As a research assistant, I built Python workflows to compare source passages with AI-generated simplifications. I examined changes in sentence structure, looked for recurring patterns across passages and assessed whether the rewrites preserved the original meaning."),
                  )),
    ResearchEntry("research-english-r-prosodic-position.html", "Production of English /r/ by Prosodic Position",
                  "Linguistics Undergraduate Research Conference · UC Santa Cruz (UCSC) · 2023",
                  "An ultrasound study of how five English speakers shaped their tongues for /r/ at the beginning of phrases, words and syllables.",
                  ("View poster", POSTER), (
                      ("What the ultrasound showed", "English speakers can produce /r/ by bunching the tongue or curling its tip back. We compared average tongue contours across the three positions. Individual speakers tended to keep a similar shape across positions, even though the shapes differed from speaker to speaker."),
                      ("The poster and my contribution", "Tony Butorovich, Jaye Padgett, Claire Wellwood and I presented this work at UC Santa Cruz. I built Python workflows to automate trials and synchronize speech data. The poster shows the tongue curves and describes how we analyzed the ultrasound recordings with Articulate Assistant Advanced."),
                  )),
    ResearchEntry("research-electronic-remote-control-lock.html", "Electronic Remote-Control Lock",
                  "Chinese utility-model patent · CN203188726U · 2013",
                  "A door lock that moves the bolt electronically while keeping the locking mechanism inside the door.",
                  ("Patent record", "https://patents.google.com/patent/CN203188726U/en"), (
                      ("How the design works", "A conventional door lock exposes a keyhole on the outside. In this design, a remote-controlled actuator moves a mechanical bolt inside the door. A magnetic reed switch enables the actuator when a magnet is brought near the switch."),
                      ("Publication", "The patent lists me as the inventor under my Chinese name, 谢沛熹. I filed the application on April 8, 2013. The utility model was published on September 11, 2013. The patent record includes the original drawing and claims."),
                  )),
)


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    category: str
    status: str
    filters: tuple
    stack: tuple
    summary: str
    role: str
    repo: Optional[str]
    flow: tuple
    sections: tuple
    extra: tuple = ()
    visibility: str = "public"
    publish: bool = False
    subprojects: tuple = ()
    website: Optional[str] = None

    @property
    def page(self):
        return "project-" + self.slug + ".html"


PROJECTS = [
    Project("foxstar", "FoxStar Agent", "Agent infrastructure", "Production · Private repository", ("Agents", "Infrastructure"),
        ("Python", "WeChatFerry", "SQLite", "FastAPI"),
        "A production agent system for WeChat communities. FoxStar routes work across language models, delegates research to a background agent, and keeps a gaming guild’s rosters and attendance records in sync with its group chats.",
        "Independent project · System design, development and operations", None, ("Route message", "Queue approved work", "Run models and tools", "Deliver result"),
        (("Two jobs in one conversation", "I built FoxStar, also called NVAX, to work inside active WeChat groups. A member can ask a research question and keep talking while a separate agent investigates. That worker gets the question and its own tool context, runs searches, and writes a sourced report. FoxStar stores the result and sends a summary back to the group that requested it."),
         ("Keeping replies tied to the right message", "Group messages keep arriving while a model is working. FoxStar first decides which messages warrant a reply, then saves approved work in a SQLite queue for parallel processing. Each job carries a conversation cutoff and a snapshot of the images available at that turn. If someone posts a second photo before the first answer is ready, the worker still sees the photo that prompted the question."),
         ("Choosing models, tools and context", "A lightweight model handles the initial routing decision. The main model can call tools across several rounds to search the web, query a document, inspect an image or run Python in a sandbox. A shared model client supports multiple providers. For long conversations, FoxStar combines recent messages with a rolling summary. If the primary summarization provider fails, another can take over."),
         ("From a group sign-up to an attendance record", "One integration serves a gaming community that organizes events in WeChat. FoxStar tracks sign-up lists as members add their names and can submit the roster to the guild’s management system. It also imports weekly attendance workbooks shared in chat. The roster and spreadsheet integrations use structured parsers so names and attendance records can move between systems without someone retyping them."),
         ("Recovery and production operations", "Finishing a task and getting its result back to WeChat are separate events. FoxStar records delivery only after the messaging adapter accepts the send. If delivery fails, the report stays available for another attempt. After a restart, interrupted reply jobs return to the queue. I use per-stage timing and provider health alerts to diagnose delays, and a FastAPI operations interface to inspect jobs and manage the running system.")), publish=True),
    Project("loopless", "LoopLess", "Browser agents", "Prototype", ("Browser Agents", "Agents", "LLM Evaluation"),
        ("Stagehand", "Redis", "W&B Weave"),
        "A browser agent that remembers successful action sequences and tests whether it can reuse them on a later run.",
        "Project contributor · Agent improvement loop", GITHUB + "/loopless",
        ("First run", "Save actions", "Replay and score"),
        (("Why run a task twice?", "On a first run, the agent has to discover how to complete a task in a browser. On a repeat run, it can try a previously successful sequence of actions. Comparing the two reveals where experience saves work and where a page still needs fresh reasoning."),
         ("What I worked on", "I improved the agent’s self-improvement loop and contributed fixes to the running application. The project uses Stagehand with Browserbase, stores reusable sequences in Redis and records evaluation traces in Weave."),
         ("Reading a trace", "The useful comparison starts with whether the task succeeded. From there, a reviewer can compare the actions, model calls and time spent on cold and warm runs. A shorter sequence is useful only when it reaches the intended result.")), publish=True),
    Project("aml-gnn", "Graph Learning for Anti-Money Laundering", "Graph neural networks", "Course research",
        ("Machine Learning", "Deep Learning"), ("PyTorch Geometric", "GNN", "XGBoost"),
        "A comparison of transaction-graph models and tabular baselines for detecting rare laundering activity in IBM’s AML dataset.",
        "CSC871 Deep Learning · Andy Byeon, Chris Randall and Max Xie", GITHUB + "/csc871-anti-money-laundering-ibm-gnn",
        ("Transaction data", "Graph and tabular models", "Threshold evaluation"),
        (("What does the graph add?", "An individual transfer describes one interaction. A graph places it among the other transfers involving those accounts. Our team compared TransformerConv and GINEConv graph neural networks with a multilayer perceptron and an XGBoost baseline."),
         ("My contribution", "I contributed the XGBoost baseline and evaluation plots. A tabular model gave us a reference point for asking whether the graph representation added predictive information."),
         ("Choosing a threshold", "Laundering examples are rare in the dataset. The notebooks examine how many positives a model finds when the decision threshold is chosen against a validation false-positive target. That is a different operating point from the threshold that maximizes F1.")), publish=True),
    Project("real-browser-benchmark", "REAL Browser Agent Benchmark", "Browser-agent evaluation", "Hackathon",
        ("Browser Agents", "Agents", "LLM Evaluation"), ("Python", "Browser automation", "Evaluation"),
        "A benchmark harness that runs agents against 16 calendar, email, hotel-booking and networking tasks.",
        "REAL Agent Challenge · Peixi Xie, Dhruv Patel and Yuvraj Gupta", GITHUB + "/REAL-Hackathon-browser-agent-benchmark",
        ("Task specification", "Browser session", "Outcome check"),
        (("What counts as a completed task?", "An agent can navigate to the right application and still leave a task unfinished. The harness separates the task definition, the agent’s browser session and the evaluator that checks the outcome."),
         ("My contribution", "I worked on the agent’s reflection loop and iterated on its behavior across calendar, email and networking tasks. The harness gives each task its own browser instance so runs can be evaluated independently."),
         ("Competition context", "Our team earned second place in the Agent Track of the REAL Agent Challenge. The public repository preserves several experiments, including an orchestrator branch with documented task failures.")),
        (("Team submission", "https://devpost.com/software/real-hackathon-browser-agent"),), publish=True),
    Project("ultrasound-tongue-tracking", "Tracking Tongue Shape in Ultrasound", "Computer vision & speech", "Research",
        ("Machine Learning", "Deep Learning"), ("DeepLabCut", "CNN", "Python"),
        "Computer vision and ultrasound workflows for measuring how the tongue shapes the English /r/ sound.",
        "UCSC research assistant · Conference poster with Tony Butorovich, Jaye Padgett and Claire Wellwood", None,
        ("Ultrasound video", "Tongue contours", "Speech analysis"),
        (("Measuring a gesture you cannot see", "Speakers can produce English /r/ with a bunched tongue or a curled-back tip. Ultrasound reveals the shape during speech, but comparing those shapes requires identifying the tongue contour across frames."),
         ("My contribution", "I built Python workflows to automate trials and synchronize speech data. My lab work included using DeepLabCut for CNN-based tongue-contour tracking and Articulate Assistant Advanced to work with the ultrasound recordings."),
         ("What the poster reports", "Our 2023 poster compared average tongue curves from five speakers across phrase-, word- and syllable-initial positions. Tongue shape was relatively stable across those positions, with clear differences between speakers. The poster reports the speech study and its analysis in Articulate Assistant Advanced.")),
        (("Conference poster (PDF)", POSTER),), publish=True),
    Project("ml-from-scratch", "Machine Learning from Scratch", "Machine learning", "Experiments",
        ("Machine Learning", "Deep Learning", "Experimental"), ("C", "Python", "NLP"),
        "I worked out how a neural network learns on paper, then implemented it in Python. These five projects trace my experiments from individual weight updates to tool-calling agents and local inference.",
        "Personal research · Implementations and handwritten design notes", GITHUB + "/Basic_ML_Research",
        ("Implement", "Train", "Run inference"),
        (("MNIST study reference",
          'For digit classification, I followed a <a href="https://www.youtube.com/watch?v=w8yWXqWQYmU">video tutorial</a> using '
          '<a href="https://www.kaggle.com/wwsalmon/simple-mnist-nn-from-scratch-numpy-no-tf-keras">wwsalmon’s original Kaggle code</a>. '
          f'I copied the code with minor changes for my <a href="{ML_SOURCE}deep_learning/mnist_problem/neural_network_from_scratch.ipynb">study notebook</a>.'),),
        publish=True, subprojects=(
            ("A neural network from scratch",
             "I designed the network by hand and wrote the Python scripts that implement its forward pass, backpropagation and weight updates. The network learns a rule you can check by hand. Given three numbers, is the first greater than the sum of the other two?",
             (("Handwritten design notes (PDF)", NETWORK_SOURCE + "Neural_Network_From_Scratch_Note.pdf"),
              ("Original Python script", NETWORK_SOURCE + "neural_network.py"),
              ("Python script with CUDA support", NETWORK_SOURCE + "neural_network_improved.py"))),
            ("A single perceptron in C",
             "Can one neuron learn whether the first of three numbers is larger than the other two added together? I used four labeled triples to train a perceptron, then tested it on two new triples. In one short C program you can trace the weighted sum, the prediction error and the resulting change to each weight.",
             (("Perceptron implementation", ML_SOURCE + "deep_learning/logic_simulation/perceptron_cc/perceptron.c"),)),
            ("Early LLM experiments with search tools",
             "I explored how to turn a follow-up question into a search query that makes sense outside the conversation. In a small LangGraph news agent, the model can request a Tavily search, read the results and use them in its reply. The graph makes it easy to follow the handoff from the model to the tool and back.",
             (("Follow-up prompt", ML_SOURCE + "llm/deepseek_follow_up_prompt.txt"),
              ("Tool-calling agent", ML_SOURCE + "agent/langgraph_tavily_news_agent_minimal.py"))),
            ("Serving local inference with Ollama",
             "I built a small Flask service in front of Ollama so a client could read a model’s reply as it arrived. One debugging lesson came from response logging: reading the whole response for the log buffered the stream. I moved metadata logging ahead of the stream and passed the chunks through as they arrived.",
             (("Inference service", ML_SOURCE + "nlp/ollama_proxy/proxyserver_v4.py"),
              ("Streaming notes", ML_SOURCE + "nlp/ollama_proxy/readme.md"))),
            ("Movie-review sentiment with BERT",
             "I fine-tuned a BERT classifier on a subset of IMDb reviews to predict positive or negative sentiment. I wrote a separate inference script that recreates the two-label classifier, loads the saved weights and applies the same tokenizer to a new review. That let me test a sentence without rerunning training.",
             (("Training code", ML_SOURCE + "nlp/sentiment_analysis.py"),
              ("Prediction code", ML_SOURCE + "nlp/sentiment_analysis_bert_infer.py"))),
        )),
    Project("swingsage", "SwingSage", "Sequence modeling", "Course project", ("Machine Learning", "Deep Learning", "Agents"),
        ("LSTM", "FastAPI", "Paper trading"),
        "A paper-trading experiment that combines an LSTM price forecast with a language model’s reading of market indicators.",
        "CSC665 team project · Guardrails and deployment", GITHUB + "/csc665-swingsage",
        ("Price sequences", "Combine signals", "Paper trade"),
        (("Two views of a time series", "A recurrent neural network processes a price sequence, while a language model interprets engineered indicators. The project brings their signals together and sends eligible orders to a paper-trading environment."),
         ("My contribution", "I contributed guardrail enforcement and adapted the notebook workflow for Google Colab. I also worked on deployment so teammates could run the forecasting and application components together."),
         ("Scope of the experiment", "Paper trading lets the team inspect how a forecast becomes an order. Its simulated fills do not establish live returns.")), publish=True),
    Project("litmus", "Litmus", "Voice & evaluation", "Hackathon", ("Agents", "LLM Evaluation"),
        ("Next.js", "Fastify", "Gemini Live"),
        "A test bench for voice agents that brings call evaluations and integration checks into one review.",
        "Team project · Continual Learning Hackathon, February 2026 · Best Use of You.com APIs, 1st place", GITHUB + "/Litmus",
        ("Benchmark task", "Voice session", "Tool verification"),
        (("The question", "When an agent says it has finished a task, how would a reviewer check? A transcript captures the conversation. Checking the integrations separately tells a reviewer which tools are available. Litmus brings those two signals into one evaluation."),
         ("My contribution", "I started the project submission and contributed the initial public repository. Aritra Saharay, Yuvraj Gupta, Kush Ise and I built the evaluation marketplace, including a web interface for running benchmark tasks and comparing agents."),
         ("Two services, two clocks", "The Next.js application handles tasks, accounts and results in Supabase. A separate Fastify WebSocket service bridges a Plivo call to Gemini Live. Keeping the audio stream in its own process lets it stay connected while the web app serves requests."),
         ("Reading a result", "A reviewer can compare the outcome of a benchmark with Composio tool verification. A completed call, a plausible answer and a verified integration each answer a different question. That distinction matters when a voice agent sounds confident."),
         ("Limits of the prototype", "The public implementation documents the evaluation paths and integrations. A comparison still depends on the chosen task, the available tools and whether their actions can be independently checked.")),
        (("Team submission", LITMUS_ENTRY),), publish=True),
    Project("crypto-risk-agent", "Crypto Risk Analysis Agent", "Tool-using agents", "Hackathon", ("Agents",),
        ("MCP", "Solana", "Claude"), "An agent that connects wallet activity and token ownership data to explain concentration risk.",
        "Team project · Production Agents Hackathon, November 2025", GITHUB + "/Automatic-Crypto-Risk-Analysis-Agent",
        ("Solana token", "MCP data tools", "Risk explanation"),
        (("The question", "A wallet holding a large share of a token could be an exchange, a liquidity pool or a single investor. Those cases look similar in a holder table. The team set out to give readers enough context to interpret a concentration signal."),
         ("My contribution", "I worked on the tool-calling agent that turns structured API responses into explanations. Yuvraj Gupta, Pramod Thebe, Ryuto Kawabata and I submitted the system together."),
         ("Following the evidence", "Helius supplies holder balances, Moralis adds wallet activity, and DexScreener provides market context. A custom MCP server exposes these lookups to the agent. The backend coordinates requests and the interface presents the report."),
         ("Working within API limits", "Holder lookups can trigger provider rate limits. The team documented spacing requests, retrying failed calls and degrading gracefully when a source is unavailable. A missing response reduces the evidence available for a report."),
         ("Outcome", "Our team earned first place for Best Use of TRM Labs and third place for Best Use of Sanity at the Production Agents Hackathon. The prototype explains observed risk signals. Concentrated ownership alone cannot establish intent or predict what a token will do.")),
        (("Award & submission", DEVPOST),), publish=True),
    Project("dynamic-llm-benchmarking", "Dynamic Benchmarking of LLMs", "Language research", "M.A. capstone", ("LLM Evaluation",),
        ("MMLU", "LiveBench", "Linguistics"), "A study of how four language models change rank when the questions and scoring methods change.",
        "Peixi Xie · San Francisco State University, 2026", GITHUB + "/ENG895-Capstone",
        ("Four models", "Three benchmarks", "Rank comparison"), (), publish=True),
    Project("paigent-studio", "Paigent Studio", "Agent orchestration", "Prototype", ("Agents", "Experimental"),
        ("MongoDB Atlas", "x402", "TypeScript"), "A workflow editor that turns spoken or written requests into inspectable execution graphs.",
        "Collaborative prototype · Public workflow IDE", GITHUB + "/paigent",
        ("Voice or text", "Execution graph", "Approved tools"),
        (("From intent to a plan", "A natural-language request can leave the order of operations implicit. Paigent gives the user a graph of tasks and dependencies to inspect before execution."),
         ("How the prototype works", "The planner builds the graph. Retrieval uses embeddings and MongoDB Atlas Vector Search to find tools, and the executor streams progress to the interface. Approval boundaries matter when a selected tool carries a price."),
         ("Contribution and scope", "I contributed to the public project documentation. The repository describes the team’s planner, retrieval and execution components. Its x402 payment workflow is a prototype, with no production transaction-volume claim.")), publish=True),
    Project("clawguard", "ClawGuard", "Agent security", "Closed beta", ("Security", "Agents"),
        ("FastAPI", "Gmail OAuth", "SQLite"), "An email intake layer that gives agents structured messages and risk flags.",
        "Team project · Defensive email middleware", GITHUB + "/ClawGuard", ("Inbound mail", "Policy checks", "Structured event"),
        (("The boundary", "Email can contain hidden formatting, instructions and sensitive information. ClawGuard prepares messages before an agent receives them, giving the downstream application a consistent input format."),
         ("How it works", "A Gmail connection fetches messages. A deterministic policy layer strips markup, normalizes content, filters attachments and attaches risk metadata. The agent retrieves the processed event through an authenticated API."),
         ("My contribution", "My public commits include changes to account-scoped API access and authenticated ingestion. Those boundaries matter alongside the text filters because multiple users can connect their mailboxes."),
         ("Limits", "A pattern rule can miss a novel instruction or flag ordinary text. The downstream application still needs its own authorization checks before it acts on a message.")), publish=True, website="https://claw-guard.tech/"),
    Project("replicalab", "ReplicaLab", "Experimental systems", "Prototype", ("Infrastructure", "Experimental"),
        ("OpenEnv", "Docker", "Python"), "A planning environment where agents negotiate a replication study within a budget and schedule.",
        "Team project · Server, deployment and runtime", GITHUB + "/replicalab-ai", ("Scenario", "Negotiation", "Deterministic judge"),
        (("Making constraints explicit", "A feasible replication study must fit the available equipment, time and budget. The environment gives a scientist agent and lab manager separate roles and a deterministic judge to score the resulting plan."),
         ("My contribution", "I owned the server, deployment and runtime plumbing. Kian handled schemas and judge logic, Ayush worked on the scientist and client, and Kush built the frontend and demo assets."),
         ("Evaluation scope", "The judge scores rigor, feasibility and fidelity within the simulated scenario. The resulting reward describes a proposed plan under those assumptions. Real-world replication outcomes lie outside the experiment.")), publish=True),
    Project("intel-marketplace", "Intel Marketplace", "Agent commerce", "Hackathon", ("Agents",),
        ("Nevermined", "Strands Agents", "Apify"),
        "An agent that buys information from other agents and sells briefings assembled from news, market data and social signals.",
        "Team project · Autonomous Business Hackathon, March 2026", GITHUB + "/intel-marketplace",
        ("Request a briefing", "Gather signals", "Deliver the report"),
        (("Buying and selling a briefing", "A buyer asks for a briefing on a topic. The agent gathers information from its own sources and can purchase additional data through Nevermined. In the sandbox marketplace, the same agent can be a customer for one request and a seller for the next."),
         ("Recognition", "Our team earned first place for Best Global Submission at Nevermined’s Autonomous Business Hackathon.")),
        publish=True),
    Project("companyintel-ai", "CompanyIntel AI", "Company research", "Hackathon", ("Agents",),
        ("FastAPI", "Yutori", "Neo4j"),
        "A company research tool that brings competitor information, financial indicators and technical documentation into a single report.",
        "Team project · March 2026", GITHUB + "/companyintel-ai",
        ("Choose a company", "Run research tasks", "Explore the report"),
        (("Researching one company", "The system distributes a company query across six research tasks. One agent looks for product and API documentation, while others examine competitors, market sentiment and financial indicators. A graph records the relationships between companies."),
         ("Waiting for results", "Some research calls take several minutes. The interface streams progress as results arrive, and the service caches completed work for later requests. The project earned third place for Best Use of Render.")),
        (("Devpost winner record", "https://devpost.com/software/companyintel-ai"),), publish=True),
    Project("youtube-agent", "YouTube Agent", "Creator tools", "Hackathon", ("Agents",),
        ("FrontMCP", "Google ADK", "TypeScript"),
        "An assistant that helps creators research similar channels and turn what they learn into video ideas, drafts and thumbnails.",
        "Team project · Self-Evolving Agents Hackathon, November 2025", GITHUB + "/Autonomous-Youtube-analysis-agent",
        ("Find channels", "Analyze videos", "Draft content"),
        (("From channel research to a draft", "A creator can look for channels covering a topic, compare how often they publish and examine the titles and thumbnails they use. The agent can use those observations to suggest an angle for a new video and draft a title or script."),
         ("How the tools connect", "A Google ADK agent calls research and generation tools through a FrontMCP server. The web interface shows tool results as they arrive. Our team won first place in Frontegg’s sponsor category for its use of FrontMCP.")),
        (("Devpost winner record", "https://devpost.com/software/youtube-agent-vy30b8"),), publish=True),
]

@dataclass(frozen=True)
class Award:
    project: str
    project_slug: str
    place: str
    prize: str
    date: str
    affiliation: str
    event: str
    host: str
    link_label: str
    url: str
    local_record: Optional[Tuple[str, str]] = None


SFSU = "San Francisco State University"
AWARDS = (
    Award("Intel Marketplace", "intel-marketplace", "1st place", "Best Global Submission", "Mar 2026", "QubeMC LLC",
          "Autonomous Business Hackathon", "Nevermined", "Organizer announcement",
          "https://www.linkedin.com/posts/nevermined_last-weekend-at-the-autonomous-business-hackathon-activity-7437928931057643520-JPiU",
          ("View award", "assets/portfolio/awards/nevermined.jpg")),
    Award("CompanyIntel AI", "companyintel-ai", "3rd place", "Best Use of Render", "Mar 2026", "QubeMC LLC",
          "Autonomous Agent Hackathon", "Creators Corner", "Devpost winner record", "https://devpost.com/software/companyintel-ai"),
    Award("Litmus", "litmus", "1st place", "Best Use of You.com APIs", "Feb 2026", SFSU,
          "Continual Learning Hackathon", "Creators Corner", "Devpost winner record", LITMUS_ENTRY),
    Award("REAL Hackathon Browser Agent", "real-browser-benchmark", "2nd place", "The REAL Agent Challenge (Agent Track)", "Dec 2025", SFSU,
          "AGI Inc. × OpenAI × Lovable REAL Agent Challenge", "AGI Inc.", "Devpost winner record",
          "https://devpost.com/software/real-hackathon-browser-agent"),
    Award("Crypto Risk Analysis Agent", "crypto-risk-agent", "3rd place", "Best Use of Sanity", "Nov 2025", SFSU,
          "Production Agents Hackathon", "Creators Corner", "Devpost winner record", DEVPOST,
          ("View certificate", "assets/portfolio/awards/sanity.jpg")),
    Award("Crypto Risk Analysis Agent", "crypto-risk-agent", "1st place", "Best Use of TRM Labs", "Nov 2025", SFSU,
          "Production Agents Hackathon", "Creators Corner", "Devpost winner record", DEVPOST),
    Award("YouTube Agent", "youtube-agent", "1st place", "Frontegg Sponsor Prize (Best Use of FrontMCP)", "Nov 2025", SFSU,
          "Self-Evolving Agents Hackathon", "Creators Corner", "Devpost winner record",
          "https://devpost.com/software/youtube-agent-vy30b8",
          ("Project slide", "assets/portfolio/awards/frontegg.jpg")),
)
EXPERIENCE = (
    ("Current", "AI engineering", "I work on voice AI, agent workflows and evaluation."),
    ("2024–2026", "Graduate research · SFSU", "In the ECOLE Lab I used Python to examine how language models simplify text. My M.A. capstone compared three ways to evaluate language models."),
    ("Fall 2025", "Instructional support · SFSU", "I supported introductory linguistics courses through office hours, assignment feedback and computational demonstrations."),
    ("2022–2024", "Linguistics · UC Santa Cruz", "I worked with ultrasound speech data and presented a poster on English /r/. I completed my B.A. in Linguistics in June 2024."),
    ("Since 2020", "Founder & developer · QubeMC", "My experience running Minecraft worlds shaped the direction I’m taking QubeMC. I’m focusing the company on AI for gaming, starting with tools to help operators troubleshoot and automate game-server maintenance."),
)


