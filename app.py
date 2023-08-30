from flask import Flask, render_template, request
from summarizer.sbert import SBertSummarizer
from flask_mail import Mail, Message
import os

model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server address
app.config['MAIL_PORT'] = 587  # Replace with your SMTP server port (usually 587 for TLS)
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'k.vikaskumar986@gmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = 'wtjpelitrptlzdbl'  # Replace with your Gmail password

mail = Mail(app)

@app.route("/")
def msg():
    return render_template('index.html')

@app.route("/summarize", methods=['POST', 'GET'])
def getSummary():
    # ... Your existing code for summarization ...
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                # Create the "uploads" directory if it does not exist
                if not os.path.exists('uploads'):
                    os.makedirs('uploads')

                # Save the uploaded file to a temporary location
                temp_path = os.path.join('uploads', uploaded_file.filename)
                uploaded_file.save(temp_path)

                # Read the content of the uploaded file
                with open(temp_path, 'r') as file:
                    body = file.read()

                # Perform summarization on the text
                result = model(body, num_sentences=5)

                # Counting words in the original text and the summary
                original_word_count = len(body.split())
                summary_word_count = len(result.split())

                # Remove the temporary file
                os.remove(temp_path)

                # Render the summary results
                return render_template('summary.html', original_text=body, original_word_count=original_word_count, summary_text=result, summary_word_count=summary_word_count)

    # If no file was uploaded or the request method is GET, use the text input from the form
    body = request.form['data']
    result = model(body, num_sentences=5)

    # Counting words in the original text and the summary
    original_word_count = len(body.split())
    summary_word_count = len(result.split())

    return render_template('summary.html', original_text=body, original_word_count=original_word_count, summary_text=result, summary_word_count=summary_word_count)

@app.route("/contact", methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route("/send_message", methods=['POST'])
def send_message():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
 # Create the email message
    subject = "Contact Form Submission"
    sender = email  # Replace with your email address or a custom email address
    recipients = ["k.vikaskumar986@gmail.com"]  # Replace with your recipient email address or a list of email addresses

    message_body = f"Name: {name}\n"
    message_body += f"Email: {email}\n"
    message_body += f"Message: {message}\n"

    message = Message(subject=subject, sender=sender, recipients=recipients, body=message_body)

    # Send the email
    try:
        mail.send(message)
        return "MESSAGE SENT SUCCESSFULLY!"
    except Exception as e:
        return "Error sending email: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True, port=8000)