# Comprehensive Local Meeting Intelligence & Document Suite 🤖📊

An enterprise-grade, privacy-first AI Agent orchestration pipeline engineered to ingest raw unstructured corporate meeting notes, audit stakeholder engagement metrics, cross-reference local RAG compliance libraries, and programmatically generate production business documentation without token costs or hardcoded parameters.

## 💡 System Architecture Design
- **Zero Hardcoding Design Patterns:** Collects human stakeholder parameters, conversation logs, and sprint item sizing inputs dynamically at runtime via an interactive CLI prompt channel.
- **Config-Driven Orchestration:** Decouples prompt workflows, vector database rules, and corporate styling details into an external orchestration configuration file (`config/settings.json`).
- **Advanced Data Processing Suite:** Combines structural log parsers (`data_parsers.py`) with local keyword index tracking engines (`vector_search.py`) to supply context arrays to a local **Ollama (`llama3.2`)** client wrapper.

## 🛠️ Local System Installation & Run Guide

1. **Ensure Ollama is initialized and running the target model stack locally:**
   ```bash
   ollama run llama3.2
   ```

2. **Initialize workspace structures and download necessary document adapters:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the master workflow orchestrator pipeline:**
   ```bash
   python main.py
   ```

## 📁 Artifact Registries Output Overview
Upon program completion, the framework writes these production-ready corporate data models into the local `output_artifacts/` directory:
- `[Project_Name]_Meeting_MOM.txt`: Audited participant engagement tracker recording dialogue turn tallies.
- `[Project_Name]_Project_PRD.docx`: A structured engineering requirement specification document mapping cross-functional blockers.
- `[Project_Name]_Project_Estimation.xlsx`: A polished sprint tracking spreadsheet styled with auto-fitting margins, formula-driven cells (`SUM`), and **custom conditional cell alert tags highlighting high-complexity milestones**.
