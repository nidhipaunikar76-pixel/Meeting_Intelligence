class AnalyticalDataAuditor:
    @staticmethod
    def audit_transcript_attendance(transcript: str, team_directory: list) -> dict:
        """Analyzes text line frequencies to calculate active speaker footprint structures."""
        attendance_report = {
            member: {"speech_contribution_turns": 0, "engagement_status": "Absent / Muted"} 
            for member in team_directory
        }
        
        for line in transcript.strip().split("\n"):
            if not line:
                continue
            for member in team_directory:
                first_name_token = member.split(" ")[0]
                if f"{first_name_token}:" in line or f"({first_name_token})" in line:
                    attendance_report[member]["speech_contribution_turns"] += 1
                    attendance_report[member]["engagement_status"] = "Active Present"
                    
        return attendance_report
