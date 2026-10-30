# main.py
import json
import os
import sys

# Forces Python to explicitly look inside the active directory for packages
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Core.ollama_client import LocalLLMClient
from Tools.data_parsers import AnalyticalDataAuditor
from Tools.vector_search import LocalRAGEngine
from Tools.web_search import LocalWebSearchEngine
from Tools.document_exporters import DocumentPublisher

def load_system_configurations(config_path: str = "config/settings.json") -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Critical configuration data layout missing at: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def prompt_user_for_dynamic_inputs() -> tuple:
    print("\n=======================================================")
    print("👤 ENTER INTERACTIVE PROJECT CONTEXT SCOPE")
    print("=======================================================")
    product_name = input("Enter Target Product/Project Name (e.g. Project Nexus): ").strip()
    
    pm_name = input("Enter Product Manager (PM) Full Name: ").strip() + " (Product Manager)"
    dev_name = input("Enter Lead Developer Full Name: ").strip() + " (Technical Lead)"
    tester_name = input("Enter QA Engineer Full Name: ").strip() + " (QA Lead)"
    
    team_directory = [pm_name, dev_name, tester_name]
    
    print("\n--- 📂 TRANSCRIPT INGESTION STRATEGY ---")
    transcript_file_path = input("Enter path to transcript text file (or hit Enter to run simulated test loop): ").strip()
    
    if transcript_file_path and os.path.exists(transcript_file_path):
        with open(transcript_file_path, "r", encoding="utf-8") as f:
            transcript_content = f.read()
    else:
        print("⚠️ No user file discovered. Initializing execution simulation tracing...")
        transcript_content = f"""
        [00:01:05] {pm_name}: Welcome all. Let's align on {product_name} core functionalities. We need a secure login portal featuring multi-factor authentication (MFA) via SMS.
        [00:02:40] {dev_name}: Got it. I'll engineer AES-256 data payload encryption matrix standards. However, the database schema isn't finalized yet, which will stall our migrations.
        [00:04:15] {tester_name}: I'll build out structural validation test routines to monitor endpoint latency values.
        """
        
    return product_name, team_directory, transcript_content

def prompt_user_for_sprint_tasks(team_directory: list, complexity_matrix: dict) -> list:
    print("\n=======================================================")
    print("📊 DYNAMIC TASK SIZING & ESTIMATION MATRIX")
    print("=======================================================")
    print("Instructions: Enter engineering items below. Type 'done' to compile assets.")
    
    tasks_list = []
    while True:
        task_title = input("\nEnter Task/Deliverable Description: ").strip()
        if task_title.lower() == 'done':
            break
        if not task_title:
            continue
            
        print("Select Assigned Lead Assignment:")
        for idx, person in enumerate(team_directory, 1):
            print(f"  [{idx}] {person}")
        try:
            selection = int(input("Choice (Number Index): ")) - 1
            assigned_owner = team_directory[selection]
        except Exception:
            print("❌ Selection out of bounds. Defaulting task allocation to: 'Unassigned Core'")
            assigned_owner = "Unassigned Core"
            
        complexity = input("Enter Complexity Rating Tier (Low / Medium / High): ").strip().lower()
        if complexity not in complexity_matrix:
            print("❌ Unknown rating choice. Defaulting metrics to: 'Medium'")
            complexity = "medium"
            
        allocated_hours = complexity_matrix[complexity]
        tasks_list.append((task_title, assigned_owner, complexity.capitalize(), allocated_hours))
        print(f"✔️ Added Task: {task_title} -> Assigned: {assigned_owner} ({complexity.capitalize()} | {allocated_hours} Hours)")
        
    return tasks_list

def execute_complete_mesh_pipeline():
    # 1. Load Setup Parameters
    try:
        config_data = load_system_configurations()
    except Exception as err:
        print(f"❌ Application boot error: {err}")
        return

    # 2. Extract CLI Boundaries
    product_name, team_directory, transcript_content = prompt_user_for_dynamic_inputs()
    
    # 3. Step 1: Execute Logs/Attendance Auditing
    print("\n🔍 Step 1: Running Logs Auditing Pass...")
    attendance_report = AnalyticalDataAuditor.audit_transcript_attendance(transcript_content, team_directory)
    print(json.dumps(attendance_report, indent=2))
    
    # 4. Step 2: Query Local RAG Knowledge context
    print("\n📚 Step 2: Querying local Vector RAG Engine rules database...")
    rag_engine = LocalRAGEngine(config_data["mock_internal_kb"])
    internal_context_rules = rag_engine.query_internal_standards(transcript_content)
    print(internal_context_rules)
    
    # 5. Step 3: Call Web Data Context Ingestion
    print("\n🌐 Step 3: Triggering external industry tech stack intelligence lookup...")
    web_context_rules = LocalWebSearchEngine.fetch_live_industry_context(product_name)
    print(web_context_rules)

    # 6. Collect Sprint Estimates
    tasks_payload = prompt_user_for_sprint_tasks(team_directory, config_data["complexity_weights"])
    if not tasks_payload:
        tasks_payload = [(f"{product_name} Core Deployment Blueprint", team_directory[1], "Medium", 32)]

    # 7. Step 4: Run Prompt Synthesis via local LLM Client Orchestrator
    print(f"\n🧠 Step 4: Querying local Ollama engine for semantic processing...")
    llm = LocalLLMClient(model_name="llama3.2")
    
    prompt_blueprint = config_data["prompts"]["analysis_template"]
    formatted_prompt = prompt_blueprint.format(
        product_name=product_name, 
        transcript=transcript_content,
        internal_context=internal_context_rules,
        web_context=web_context_rules
    )
    
    try:
        prd_markdown_response = llm.query_model(
            prompt=formatted_prompt,
            system_instruction=config_data["prompts"]["system_instruction"]
        )
        print("✅ Semantic PRD Extraction complete.")
    except Exception as e:
        print(f"❌ Aborted pipeline layout: {str(e)}")
        return

    # 8. Step 5: Invoke Programmatic Document Publishers
    print("\n💾 Step 5: Launching file compilation tool chains...")
    publisher = DocumentPublisher(theme_config=config_data["theme"])
    
    mom_formatted_text = f"EXECUTIVE MINUTES OF MEETING: {product_name}\n"
    mom_formatted_text += f"========================================================\n\n"
    mom_formatted_text += f"AUTOMATED ATTENDANCE AUDIT LOGS:\n{json.dumps(attendance_report, indent=2)}\n\n"
    mom_formatted_text += f"DETAILED ENGINEERING REQUIREMENTS SUMMARY:\n{prd_markdown_response}"
    
    safe_filename_prefix = "".join(c for c in product_name if c.isalnum() or c in (' ', '_')).rstrip().replace(' ', '_')
    
    status_txt = publisher.generate_txt_mom(f"{safe_filename_prefix}_Meeting_MOM.txt", mom_formatted_text)
    status_docx = publisher.generate_docx_prd(f"{safe_filename_prefix}_Project_PRD.docx", product_name, prd_markdown_response)
    status_xlsx = publisher.generate_estimation_xlsx(f"{safe_filename_prefix}_Project_Estimation.xlsx", product_name, tasks_payload)
    
    print("\n========================================================================")
    print("🏁 PIPELINE LIFECYCLE COMPLETE: ARTIFACT GENERATION REGISTER")
    print("========================================================================")
    print(status_txt)
    print(status_docx)
    print(status_xlsx)
    print(f"\n💡 High-impact corporate metrics generated cleanly inside: '{os.path.abspath('output_artifacts')}'")

if __name__ == "__main__":
    execute_complete_mesh_pipeline()
