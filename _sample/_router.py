from flask import jsonify, make_response
from _sample import (
    sample_level_chk,
    sample_sendgrid,
    sample_xlsx,
    sample_pdf,
    sample_upload,
    sample_firestore_normal,
    sample_firestore_like,
    sample_collection,
    sample_gmail_api,
)


def router(app):
    # sample get collection
    @app.post("/sample/collection")
    def router_sample_collection():
        dic = sample_collection.sample_get_collection()
        return jsonify(dic), 201

    # sample level check
    @app.post("/sample/level_chk")
    def router_sample_level_chk():
        dic = sample_level_chk.sample_level_chk()
        return jsonify(dic), 201

    @app.post("/sample/firestore/<subpath>")
    def router_sample_firestore(subpath):
        if subpath == "normal":
            dic = sample_firestore_normal.sample_firestore_normal()
        if subpath == "like":
            dic = sample_firestore_like.sample_firestore_like()
        return jsonify(dic), 201

    # sample sendgrid
    @app.post("/sample/sendgrid/<subpath>")
    def router_sample_sendgrid(subpath):
        dic = sample_sendgrid.sample_sendgrid_exe(subpath)
        return jsonify(dic), 201

    # sample sgmail api
    @app.post("/sample/gmail_api/<subpath>")
    def router_sample_gmail_api(subpath):
        dic = sample_gmail_api.sample_gmail_api_exe(subpath)
        return jsonify(dic), 201

    # sample file upload
    @app.post("/sample/file/upload/<subpath>")
    def router_sample_file_upload(subpath):
        if subpath == "csv":
            dic = sample_upload.sample_file_upload_csv()
        if subpath == "all":
            dic = sample_upload.sample_file_upload_all()
        return dic

    # sample file download
    @app.post("/sample/file/download/<subpath>")
    def router_sample_file_download(subpath):
        if subpath == "xlsx":
            create_file, mime_type, file_name = sample_xlsx.sample_xlsx()
        else:
            create_file, mime_type, file_name = sample_pdf.pdf_download(subpath)
        response = make_response()
        response.data = create_file
        response.headers["Content-Disposition"] = "attachment; filename=" + file_name
        response.mimetype = mime_type
        return response

    # sample pdf file open
    @app.post("/sample/file/open/<subpath>")
    def router_sample_file_open(subpath):
        if subpath == "pdf_basic":
            create_file, mime_type, file_name = sample_pdf.pdf_basic()
        if subpath == "pdf_line":
            create_file, mime_type, file_name = sample_pdf.pdf_line()
        if subpath == "pdf_randam":
            create_file, mime_type, file_name = sample_pdf.pdf_randam()
        if subpath == "pdf_barcode":
            create_file, mime_type, file_name = sample_pdf.pdf_barcode()
        if subpath == "pdf_ean":
            create_file, mime_type, file_name = sample_pdf.pdf_ean()
        if subpath == "pdf_qr":
            create_file, mime_type, file_name = sample_pdf.pdf_qr()
        response = make_response()
        response.data = create_file
        response.headers["Content-Disposition"] = "attachment; filename=" + file_name
        response.mimetype = mime_type
        return response
