import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("Send an Email")

st.write("Fill in the details below:")

# Email form inputs
sender = st.text_input("From (your Gmail):")
password = st.text_input("App Password (not Gmail password):", type="password")
to = st.text_input("To:")
subject = st.text_input("Subject:")
msg = st.text_area("Message")

if st.button("Send Email"):
    if not all([sender, password, to, subject, msg]):
        st.error("Please fill all fields!")
    else:
        try:
            # Create the email message
            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = to
            message["Subject"] = subject
            message.attach(MIMEText(msg, "plain"))

            # Send email via Gmail SMTP
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(message)
                st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")



























