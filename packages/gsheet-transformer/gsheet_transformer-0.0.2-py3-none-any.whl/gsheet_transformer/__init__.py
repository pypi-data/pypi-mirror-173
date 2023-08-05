import gspread
import pandas as pd


class TransformGsheet:

    def transform_gsheet_to_df(self, service_account: dict, url: str, sheet_name: str) -> pd.DataFrame:
        """_summary_

        Args:
            service_account (dict): _description_
            url (str): _description_
            sheet_name (str): _description_

        Returns:
            pd.DataFrame: _description_
        """
        try:
            gc = gspread.service_account_from_dict(service_account)
            get_gsheet_url = gc.open_by_url(url)
            ws = get_gsheet_url.worksheet(sheet_name)
            df = pd.DataFrame(ws.get_all_records())
            return df
        except Exception as error_msg:
            print(error_msg)
