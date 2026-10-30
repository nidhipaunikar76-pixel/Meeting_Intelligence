class LocalRAGEngine:
    def __init__(self, knowledge_base_array: list):
        self.kb = knowledge_base_array

    def query_internal_standards(self, transcript_text: str) -> str:
        """Parses core text triggers to dynamically extract internal enterprise standard guidelines."""
        matched_context = []
        keywords = ["security", "encryption", "mfa", "auth", "devops", "pipeline", "database", "sms"]
        
        lower_transcript = transcript_text.lower()
        for word in keywords:
            if word in lower_transcript:
                for rule in self.kb:
                    if word in rule.lower() and rule not in matched_context:
                        matched_context.append(rule)
                        
        if not matched_context:
            return "No matching internal enterprise engineering policies located for current discussion topic."
            
        return "\n".join([f"- {item}" for item in matched_context])
