from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from modules.forms import ValidationForm
from modules.validate import Validate
import base64
import os
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient


EMAIL_API_KEY = os.getenv('EMAIL_API_KEY')
DEBUG = True
app = Flask(__name__)	#initialising flask
app.config.from_object(__name__)	#configuring flask
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

def send_certificate_by_mail(name, to_email, file_path):
    message = Mail(
        from_email=('rahul@widhya.org','Rahul from Widhya'),
        to_emails=to_email,
        subject='Congratulations Are In Order From Widhya \u2764\uFE0F',
        html_content='<html><body>Hi,<br><br>Thank you for filling up the feedback form. Your feedback really matters. As promised, PFA your certificate for attending the workshop. It\'s great that you took the extra effort to be a part of the workshop as this workshop would really help you hone your fullstack skills. It\'s a great start and we hope to ensure that you continue going a long way in your career. As a result, we would send emails about openings and positions, depending on the areas of interest that you mentioned in the feedback form. Hope to meet you soon! And all the best for your future!<br><strong>Hope you choose Widhya for your upcoming career and learning experiences !</strong><br/> It was great knowing you!<br/><br/>Regards,<br/>Rahul Arulkumaran<br>Co-Founder & CEO - Widhya<br>+91-7893798125</body></html>')
    file_path = file_path
    filename = name.split(" ")[0] + "certificate.png"
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('image/png')
    attachment.file_name = FileName(filename)
    attachment.disposition = Disposition('attachment')
    attachment.content_id = ContentId('cert')
    message.attachment = attachment
    sendgrid_client = SendGridAPIClient(EMAIL_API_KEY)
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ValidationForm(request.form)
    if(request.method == 'POST'):		#If the user submits data in the Form
        if(form.validate()):		#If form is validated
            try:
                email = request.form['email']
                validate = Validate(email)
                name = validate.generate_certificate()
                certificate_path = 'modules/certificates/' + name + '.png'
                send_certificate_by_mail(name, email, certificate_path)
                return render_template("index.html", form=form, accept=1, flag=0)
            except FileNotFoundError:
                return render_template("index.html", form=form, accept=0, flag=1, apologies="Looks like you haven't filled the feedback form and/or followed Widhya on Instagram and LinkedIn! Please do the needful to access your certificate")
    return render_template("index.html", form=form)

@app.errorhandler(404)
def not_found(e):
	return 'Sorry, the page you requested cannot be found! {}'.format(e),404

@app.errorhandler(500)
def application_error(e):
	return 'Sorry, unexpected error: {}'.format(e), 500

if(__name__ == "__main__"):
	app.run()
