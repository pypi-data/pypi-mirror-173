import gspread
import pandas as pd


class TransformGsheet:   
    def transform_gsheet_to_df(self, service_account: dict, url: str, sheet_name: str) -> pd.DataFrame:
        try:
            gc = gspread.service_account_from_dict()
            get_gsheet_url = gc.open_by_url(url)
            ws = get_gsheet_url.worksheet(sheet_name)
            df = pd.DataFrame(ws.get_all_records())
            return df
        except Exception as error_msg:
            print(error_msg)
            raise