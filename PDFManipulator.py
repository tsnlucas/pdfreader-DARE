import fitz

class PDFManipulator:
    @staticmethod
    def extract_info_from_pdf(pdf_path):
        pdf_document = fitz.open(pdf_path)
        extracted_info = {}
        current_field = None

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text().splitlines()

            for line in text:
                if "01 - Nome / Razão Social" in line:
                    current_field = "Nome / Razão Social"
                elif "07 - Data de Vencimento" in line:
                    current_field = "Data de Vencimento"
                elif "09 - Número do DARE" in line:
                    current_field = "Número do DARE"
                elif current_field and line.strip():
                    extracted_info[current_field] = line.strip()
                    current_field = None

        pdf_document.close()
        return extracted_info
