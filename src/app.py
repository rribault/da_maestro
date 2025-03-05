import json
import shutil
import os
import pandas as pd
import datetime
from pathlib import Path
from models import DA, DAxlsx
from shiny import App, reactive, ui, Inputs, Outputs, Session, render
from shiny.types import FileInfo
from pprint import pformat
from pydantic import ValidationError 

from quotation_data_extraction import extract_data_from_png, Model_choices
from codes_analytiques import codes_dict, spending_lines



app_ui = ui.page_fluid(
        # ui.sidebar("Sidebar", 
        #            ui.input_selectize("user", "Select User", choices=get_available_users(), selected="RomainRibault"),
        #            ui.output_code('display_selected_user'),
        #            width=500,
        #            bg="#f8f8f8", open="closed"), 
        ui.include_css(Path(__file__).parent/ "styles.css"),
        ui.panel_title(title='', window_title="Créer une Demande D'Achat"),    
        ui.layout_columns(
            ui.card(
                ui.card(
                    ui.card_header('DEVIS'),
                    ui.layout_columns(
                        ui.input_file("file1", "Choose PNG File", accept=[".png"]),
                        ui.input_selectize("choosen_one", "Modèle IA", choices=Model_choices, selected='gemini')
                    ),
                ),                
                ui.card(
                    ui.card_header('IDENTITE DU FOURNISSEUR'),
                    ui.layout_columns(
                        ui.input_text("provider_company", 'Société', value=None, placeholder='OBLIGATOIRE'),
                        ui.input_text("provider_phone", 'T. Bureau')
                    ),
                    ui.layout_columns(
                            ui.input_text("provider_contact_name", 'Nom du contact'),
                            ui.input_text("provider_mobile_phone", 'T. Portable')
                    ),
                    ui.layout_columns(
                            ui.input_text("provider_adress", 'Adresse'),
                            ui.input_text("provider_email", 'E-mail')
                    ),
                    ui.layout_columns(
                            ui.input_text("quotation_id", 'Ref devis', placeholder='OBLIGATOIRE'),
                            ui.input_date("quotation_date", 'daté du', language='fr')
                    ),
                    ui.layout_columns(
                        ui.input_checkbox('paid', 'Commande déjà payée', value=False),
                        ui.input_checkbox('internet', 'Commande internet', value=False),
                        ui.input_checkbox('bdc_to_be_send', 'BDC à envoyer au fournisseur', value=True)
                    ),
                ),
                ui.card(
                    ui.card_header('NATURE ET MONTANT DE LA DA'),
                    ui.layout_columns(
                        ui.input_selectize("analytic_code", 'Analytique', choices=codes_dict, selected='', remove_button=True ),
                        ui.input_selectize('spending_line', 'Ligne de depense', choices=spending_lines, selected='Sous-traitance Hors partenaires             '),
                    ),
                    ui.layout_columns(
                    ui.output_data_frame("parsed_file"),
                    ui.output_data_frame("calculate_tva_total"),
                    ),
                    ui.input_text('employee_name', "Nom demandeur"),
                    min_height = '300px',
                ),
                ui.download_button("create_da_xlsx", "Create XLSX"),
                
            ),
            ui.card(
                ui.output_image("display_create_da_img"),
                full_screen=True
                    ),

            min_height = '1000px',
            col_widths=[5, 7]
        ),          
    )

def server(input: Inputs, output: Outputs, session: Session):

    create_da_path = reactive.value('')

    @render.code
    def display_selected_user():
        with open(input.user(), 'r', encoding='utf-8') as file:
            user = json.load(file)

        return pformat(user)

    @render.data_frame
    def parsed_file():
        file: list[FileInfo] | None = input.file1()
        if file is None:
            return {}
        
        # Use IA model to extract data from document
        new_da = extract_data_from_png( 
            file[0]["datapath"]
        )
        item_list = pd.json_normalize(new_da['items'])
        new_da.pop('items')

        for key, value in new_da.items():
            # if key in ['paid', 'internet', 'bdc_to_be_send'] :
            #     ui.update_checkbox(key, value=value)
            if 'date' in key :
                ui.update_date(key, value=value)
            else :
                ui.update_text(key, value=value) 

        # create new file name
        filename = os.path.basename(file[0]["datapath"])
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{timestamp}_{filename}'
        # www_dir = Path(__file__).parent / "www"

        #copy to static_assets
        os.makedirs('user_documents', exist_ok=True)
        destination_path = os.path.join('user_documents', filename)
        shutil.copy2(file[0]["datapath"], destination_path)
        create_da_path.set(destination_path)

        return render.DataGrid(
            item_list,
            editable=True
        )
    
    @render.image
    def display_create_da_img():
        try :
            img_path=create_da_path.get()
            img = {"src": img_path}
            return img
        except FileNotFoundError:
            raise FileNotFoundError('Selectionne un devis')

    @render.data_frame
    def calculate_tva_total():
        items = parsed_file.data_view()

        # Ensure 'qty' and 'price_no_tax' are numeric
        items['qty'] = pd.to_numeric(items['qty'], errors='coerce')
        items['price_no_tax'] = pd.to_numeric(items['price_no_tax'], errors='coerce')

        # Calculate Tva and price as per DA template (for info only)
        tva = (items['qty'] * items['price_no_tax'])*0.2
        total = (items['qty'] * items['price_no_tax'])*1.2
        df = pd.DataFrame(data={'tva': [tva.sum()], 'total': [total.sum()]}).round(1)
        return render.DataGrid(df)

    @render.download()
    def create_da_xlsx():
        json_items = parsed_file.data_view().to_json(orient='records')
        json_items = json.loads(json_items)
        
        da = DA().model_dump()
        da.pop('items', None)
        # get DA from LLM and modified by user
        for key, _ in da.items() :
            if input.__contains__(key) :
                da[key] = input.__getattr__(key)._value

                # if empty, set mandatrory fields to None to raise a user error further down
                if key in ['provider_company', 'analytic_code', 'quotation_date', 'quotation_id' ] :
                    if da[key] in ['']:
                        da[key]=None

        da['items'] = json_items

        # with open(input.user(), 'r', encoding='utf-8') as file:
        #     for_validation_fields = json.load(file)
        # da.update(for_validation_fields)

        try :
            new_da = DAxlsx(**da)
        except ValidationError as e:
            error_messages = []
            
            try:
                for error in e.errors():
                    field = ".".join(error["loc"])  # Construct field name
                    msg = error["msg"]
                    error_messages.append(f"Field '{field}': {msg}")
            except TypeError:
                error_messages = [str(e)]

            error_str = "\n".join(error_messages)
            ui.modal_show(ui.modal(
                ui.TagList(
                    ui.p(f"Error creating DA:"),
                    ui.p(ui.code(error_str)),
                ),
                title="DA Creation Error",
                easy_close=True,
            ))

            return None

        quotation_path=Path(create_da_path.get())
        save_path = str(quotation_path.with_suffix(".xlsx"))
        
        new_da.xlsx_exporter(save_path=save_path)

        return save_path

www_dir = Path(__file__).parent.parent / "www"        
app = App(app_ui, server, static_assets=www_dir)