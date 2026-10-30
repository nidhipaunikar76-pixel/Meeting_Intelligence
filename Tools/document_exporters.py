import os
from docx import Document
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

class DocumentPublisher:
    def __init__(self, theme_config: dict, output_dir: str = "output_artifacts"):
        self.output_dir = output_dir
        self.theme = theme_config
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.font_family = self.theme.get("font_family", "Segoe UI")
        self.border_thin = Border(
            left=Side(style='thin', color='D9D9D9'),
            right=Side(style='thin', color='D9D9D9'),
            top=Side(style='thin', color='D9D9D9'),
            bottom=Side(style='thin', color='D9D9D9')
        )

    def generate_txt_mom(self, filename: str, content: str) -> str:
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        return f"[Text MOM Generated Successfully] at: {path}"

    def generate_docx_prd(self, filename: str, product_name: str, prd_markdown: str) -> str:
        path = os.path.join(self.output_dir, filename)
        doc = Document()
        doc.add_heading(f"Project Layout Specification: {product_name}", level=0)
        doc.add_heading("AI Generated Product Requirement Document (PRD)", level=1)
        
        blocks = prd_markdown.split("\n\n")
        for block in blocks:
            cleaned = block.strip()
            if not cleaned: continue
            
            if cleaned.startswith("###"):
                doc.add_heading(cleaned.replace("###", "").strip(), level=2)
            elif cleaned.startswith("##"):
                doc.add_heading(cleaned.replace("##", "").strip(), level=1)
            else:
                doc.add_paragraph(cleaned)
                
        doc.save(path)
        return f"[Word PRD Generated Successfully] at: {path}"

    def generate_estimation_xlsx(self, filename: str, product_name: str, structured_tasks: list) -> str:
        path = os.path.join(self.output_dir, filename)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sprint Estimation Matrix"
        ws.views.sheetView.showGridLines = True
        
        header_fill = PatternFill(start_color=self.theme["header_color_hex"], end_color=self.theme["header_color_hex"], fill_type="solid")
        stripe_fill = PatternFill(start_color=self.theme["stripe_color_hex"], end_color=self.theme["stripe_color_hex"], fill_type="solid")
        alert_fill = PatternFill(start_color=self.theme["alert_color_hex"], end_color=self.theme["alert_color_hex"], fill_type="solid")
        total_fill = PatternFill(start_color=self.theme["total_color_hex"], end_color=self.theme["total_color_hex"], fill_type="solid")
        
        title_font = Font(name=self.font_family, size=16, bold=True, color=self.theme["header_color_hex"])
        header_font = Font(name=self.font_family, size=11, bold=True, color="FFFFFF")
        data_font = Font(name=self.font_family, size=11, color="000000")
        alert_font = Font(name=self.font_family, size=11, bold=True, color=self.theme["alert_font_hex"])
        bold_font = Font(name=self.font_family, size=11, bold=True, color="000000")

        ws['A1'] = f"{product_name}: Resource Deployment & Effort Estimation Metrics"
        ws['A1'].font = title_font
        ws.merge_cells('A1:E1')
        ws.row_dimensions.height = 35
        
        headers = ["Task Breakdown Deliverable", "Resource Lead Assignment", "Complexity Tier", "Sizing Footprint (Hours)", "Timeline Estimate (Weeks)"]
        ws.append([]) 
        ws.append(headers) 
        ws.row_dimensions.height = 25
        
        for col_idx, col_name in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col_idx)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center" if col_idx > 1 else "left", vertical="center")
            cell.border = self.border_thin

        start_row = 4
        for idx, task_tuple in enumerate(structured_tasks):
            current_row = start_row + idx
            task_desc, resource, complexity, hours = task_tuple
            
            row_data = [task_desc, resource, complexity, hours, f"=D{current_row}/40"]
            ws.append(row_data)
            ws.row_dimensions[current_row].height = 20
            
            is_high_risk = str(complexity).strip().lower() == "high"
            
            for col_idx in range(1, 6):
                cell = ws.cell(row=current_row, column=col_idx)
                cell.font = data_font
                cell.border = self.border_thin
                
                if idx % 2 == 1:
                    cell.fill = stripe_fill
                    
                if is_high_risk and col_idx == 3:
                    cell.fill = alert_fill
                    cell.font = alert_font
                
                if col_idx == 1: 
                    cell.alignment = Alignment(horizontal="left", vertical="center")
                elif col_idx in (2, 3): 
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                elif col_idx == 4:
                    cell.alignment = Alignment(horizontal="right", vertical="center")
                    cell.number_format = "#,##0"
                elif col_idx == 5:
                    cell.alignment = Alignment(horizontal="right", vertical="center")
                    cell.number_format = "0.0"

        end_row = start_row + len(structured_tasks)
        ws.cell(row=end_row, column=1, value="Total Estimated Footprint").font = bold_font
        ws.merge_cells(start_row=end_row, start_column=1, end_row=end_row, end_column=3)
        
        border_summary_bottom = Border(top=Side(style='thin', color='A0A0A0'), bottom=Side(style='double', color=self.theme["header_color_hex"]))
        for col in range(1, 4):
            c = ws.cell(row=end_row, column=col)
            c.border = border_summary_bottom
            c.fill = total_fill

        h_sum = ws.cell(row=end_row, column=4, value=f"=SUM(D{start_row}:D{end_row-1})")
        h_sum.font = bold_font
        h_sum.fill = total_fill
        h_sum.border = border_summary_bottom
        h_sum.number_format = "#,##0"
        h_sum.alignment = Alignment(horizontal="right", vertical="center")

        w_sum = ws.cell(row=end_row, column=5, value=f"=SUM(E{start_row}:E{end_row-1})")
        w_sum.font = bold_font
        w_sum.fill = total_fill
        w_sum.border = border_summary_bottom
        w_sum.number_format = "0.0"
        w_sum.alignment = Alignment(horizontal="right", vertical="center")
        
        ws.row_dimensions[end_row].height = 25

        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col.column)
            for cell in col:
                if cell.coordinate in ws.merged_cells: continue
                if cell.value: max_len = max(max_len, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

        wb.save(path)
        return f"[Excel Sheet Generated Successfully] at: {path}"
