from flask import jsonify
from salary import salary_calc, salary_excel


def router(app):
    # salary
    @app.post("/salary/<subpath>")
    def router_salary(subpath):
        # salary_calc
        if subpath == "salary_calc_start":
            dic = salary_calc.salary_calc_start()

        if subpath == "salary_calc_exe":
            dic = salary_calc.salary_calc_exe()

        if subpath == "salary_calc_task":
            dic = salary_calc.salary_calc_task()

        # salary_excel
        if subpath == "salary_excel_start":
            dic = salary_excel.salary_excel_start()

        if subpath == "salary_excel_exe":
            dic = salary_excel.salary_excel_exe()

        if subpath == "salary_excel_task":
            dic = salary_excel.salary_excel_task()

        return jsonify(dic), 201
