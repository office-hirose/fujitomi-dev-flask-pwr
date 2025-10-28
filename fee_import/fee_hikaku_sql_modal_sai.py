# -------------------------------------------
# sai/dic
# -------------------------------------------
def mz_sai(nyu_date_int, coltd_cd, fk_data, fs_data, bal_data):
    sai_data = {
        #
        "fee_withtax": fk_data["fee_withtax"] - fs_data["fee_withtax"] - bal_data["fee_withtax"],
        "fee_notax": fk_data["fee_notax"] - fs_data["fee_notax"] - bal_data["fee_notax"],
        "fee_tax_num": fk_data["fee_tax_num"] - fs_data["fee_tax_num"] - bal_data["fee_tax_num"],
        #
        "furi_kazei_withtax": fk_data["furi_kazei_withtax"]
        - fs_data["furi_kazei_withtax"]
        - bal_data["furi_kazei_withtax"],
        "furi_kazei_notax": fk_data["furi_kazei_notax"] - fs_data["furi_kazei_notax"] - bal_data["furi_kazei_notax"],
        "furi_kazei_tax_num": fk_data["furi_kazei_tax_num"]
        - fs_data["furi_kazei_tax_num"]
        - bal_data["furi_kazei_tax_num"],
        #
        "furi_hikazei_withtax": fk_data["furi_hikazei_withtax"]
        - fs_data["furi_hikazei_withtax"]
        - bal_data["furi_hikazei_withtax"],
        "furi_hikazei_notax": fk_data["furi_hikazei_notax"]
        - fs_data["furi_hikazei_notax"]
        - bal_data["furi_hikazei_notax"],
        "furi_hikazei_tax_num": fk_data["furi_hikazei_tax_num"]
        - fs_data["furi_hikazei_tax_num"]
        - bal_data["furi_hikazei_tax_num"],
        #
        "fee_withtax_total": fk_data["fee_withtax_total"]
        - fs_data["fee_withtax_total"]
        - bal_data["fee_withtax_total"],
        "fee_notax_total": fk_data["fee_notax_total"] - fs_data["fee_notax_total"] - bal_data["fee_notax_total"],
        "fee_tax_num_total": fk_data["fee_tax_num_total"]
        - fs_data["fee_tax_num_total"]
        - bal_data["fee_tax_num_total"],
    }
    return sai_data
