from typing import List
from pydantic import  BaseModel, Field
import openpyxl
from datetime import datetime
import os

TEMPLATE_PATH = r"src\ressources\FORMULAIRE_SAS_demande_achat_FR2.xlsx"

class Item(BaseModel):
    description: str | None = Field(None, example="2025-01-20", description="Description de l'article en moins de 50 caractères")
    qty: int = 0
    price_no_tax: float = 0

class DA(BaseModel):
    analytic_code: int | None = None
    quotation_date: datetime | None = Field(None, example="2025-01-20", format="date")
    quotation_path: str | None = None
    quotation_id: str | None = Field(None, example="VP_U1021R", description="Le numéro de commande ou de devis défini par le fournisseur")
    provider_email: str | None = None
    provider_company: str | None = Field(None, example="Maritech", description="Le nom du fournisseur qui a rédigé le devis")
    provider_email: str | None = None
    provider_contact_name: str | None = None
    provider_adress: str | None = Field(None, example="10 rue du buis, 13012 Pertuis", description="L'adresse du siège du fournisseur, si elle est disponible.")
    provider_mobile_phone: str | None = None 
    provider_phone: str | None = None
    paid: bool = False
    internet: bool = False
    spending_line: str | None = None
    bdc_to_be_send: bool = True
    items: List[Item] = []
    comments: str | None = None
    employee_name: str | None = Field(None, example="John Doe", description='Le nom du salarié destinataire du devis ou de la facture')
    employee_email: str | None = None
    employee_date: datetime | None = Field(datetime.date(datetime.now()), example="2025-01-20", format="date")
    employee_signature_path: str | None = None
    responsible_name: str | None = None
    responsible_email: str | None = None

    def xlsx_exporter(self, save_path:str):
        # Load the workbook and select the active worksheet
        workbook = openpyxl.load_workbook(TEMPLATE_PATH)
        sheet = workbook.active

        # ANALYTIQUE
        sheet['J1'] = self.analytic_code

        # IDENTITE DU FOURNISSEUR
        sheet['D9'] = self.provider_company
        sheet['D10'] = self.provider_contact_name
        sheet['D11'] = self.provider_adress
        sheet['I9'] = self.provider_phone
        sheet['I10'] = self.provider_mobile_phone
        sheet['I12'] = self.provider_email

        sheet['C13'] = self.quotation_id
        sheet['G13'] = self.quotation_date
        sheet['E18'] = self.spending_line

        row = 19
        for item in self.items :
            sheet[f'B{row}'] = item.description
            sheet[f'G{row}'] = item.qty
            sheet[f'H{row}'] = item.price_no_tax
            row+=1
        
        sheet['F47'] = 'oui'

        # POUR VALIDATION
        sheet['C56'] = self.employee_name
        # sheet['C57'] = self.employee_email
        sheet['C58'] = self.employee_date
        # sheet['F56'] = self.responsible_name
        # sheet['F57'] = self.responsible_email

        # # Load the image
        # img = Image(self.employee_signature_path)  # Replace with the path to your image file

        # # Add the image to the worksheet at a specific cell
        # sheet.add_image(img, 'C59')

        # Save the modified workbook
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        workbook.save(save_path)

        return save_path
    
class DAxlsx(DA):
    analytic_code: int
    quotation_id: str
    quotation_date: datetime
    provider_company: str