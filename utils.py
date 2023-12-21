from fpdf import FPDF
from datetime import datetime


def innerWriteFile(pdf, content):
    for i, j in content.items():
        print(j)
        # print(i)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(w=0, h=10, txt=i, ln=1, align="L")

        if isinstance(j, dict):
            for key, val in j.items():
                pdf.set_font("Arial", "I", 12)

                pdf.cell(
                    w=0,
                    h=5,
                    txt=key + " : " + val,
                    ln=1,
                    align="L",
                )


def writetoPDF(content):
    now = datetime.now()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(w=0, h=10, txt=content.get("title"), ln=1, align="C")
    pdf.set_font("Arial", "I", 8)

    pdf.cell(
        w=0,
        h=25,
        txt="Report Generted at " + now.strftime("%d/%m/%Y %H:%M:%S"),
        ln=5,
        align="R",
    )

    # UserDetails
    # pdf.set_font("Arial", "B", 12)
    # pdf.cell(w=0, h=10, txt="User Login Details", ln=1, align="L")

    # pdf.set_font("Arial", "I", 12)

    # pdf.cell(
    #     w=0,
    #     h=1,
    #     txt="User Name :" + content.get("UserDetails").get("userName"),
    #     ln=1,
    #     align="L",
    # )
    innerWriteFile(pdf, content.get("dict"))

    pdf.output(content.get("name") + ".pdf", "F")
    return {
        "sucess": True,
        "message": "Report Generated",
        "name": content.get("name") + ".pdf",
    }




# writetoPDF(
#     {
#         "name": "test",
#         "title": "Zessta Softwares",
#         # "timestamp": str(time.asctime(time.localtime()))
#         "dict": {
#             "UserDetails": {
#                 "userName": "test",
#             },
            
            
#              "PersonalDetails": {
#                 "FirstName": "test",
#                 "lastName": "test",

#             },
#         },
#     }
# )
