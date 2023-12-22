from email import encoders
from email.mime.base import MIMEBase
from gzip import FNAME
from fpdf import FPDF
from datetime import datetime


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


import os
from dotenv import load_dotenv


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


def writetoPDF(content, email):
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
    # Automatino for Dict Parsing
    innerWriteFile(pdf, content.get("dict"))
    
    fileName = content.get("name") + ".pdf"
    pdf.output(fileName, "F")
    if sendEmail(email, content.get("dict").get("Personal Details").get("firstName"), fileName) == True:
        return {
            "sucess": True,
            "message": "Report Generated",
            "email" : "email has been successfully sent",
            "name": fileName,
        }


def sendEmail(email, user, filename):
    load_dotenv()
    port = os.environ["port"]
    smtp_server = os.environ["smtp_server"]
    login = os.environ["login"]
    password = os.environ["password"]

    sender_email = "info@dsksolutions.tech"  # paste your sender email
    receiver_email = email
    message = MIMEMultipart("alternative")
    message["Subject"] = "User Profile PDF - Zessta"
    message["From"] = sender_email
    message["To"] = receiver_email

    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(filename, "rb").read())
    encoders.encode_base64(part)

    part.add_header("Content-Disposition", 'attachment; filename="' + filename + '"')

    message.attach(part)

    # write the HTML part
    html = """\
 
<html lang="en">
 
  <body>
    <img src="cid:ZesstaLogo" width="200px" />
    <h1>Zessta Software Services</h1>
    <p>
      Dear {fname}, you have requested to send user profile information. Please find the
      information attached to this email.!
    </p>
    <br />
    <p>Thank you for using Zessta Software Services.</p>
    <br />
    <p>
      Regards,<br />
      Zessta Software Services, Hyderabad,
    </p>
  </body>
</html>

    """.format(fname=user)

    part = MIMEText(html, "html")
    message.attach(part)

    # We assume that the image file is in the same directory that you run your Python script from
    fp = open("zesstalogo.png", "rb")
    image = MIMEImage(fp.read())
    fp.close()

    # Specify the  ID according to the img src in the HTML part
    image.add_header("Content-ID", "<ZesstaLogo>")
    message.attach(image)
    context = ssl.create_default_context()
    # send your email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    return True


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
