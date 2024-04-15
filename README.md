# What is this project?
This is to showcase some of my early Python projects

### Customer Detection and Email Alert System

This Python application leverages your webcam to detect new customers entering a designated space. Upon detection, it will:

    Capture a snapshot of the scene.
    Send an email notification with the snapshot as an attachment.

Key Files

    emailing.py: Contains the functionality responsible for sending emails with image attachments.
    main.py: Core application logic for motion detection, image capture, and email notifications.

Prerequisites

    Python 3 (https://www.python.org/downloads/)
    OpenCV (install with pip install opencv-python)
    smtplib, email, imghdr (standard Python libraries)
    A Gmail account

Setup

    Generate App Password:
        Enable 2-factor authentication on your Gmail account.
        Navigate to App Passwords settings (https://myaccount.google.com/apppasswords).
        Generate a new app password specifically for this script.

    Update emailing.py:
        Replace "Your password here" with your generated app password.
        Replace "your@email_address.com" with both your sender and receiver email addresses.

    Create an "images" folder: This is where captured images will be stored.

Usage

    Run the main script: python main.py
    The application will begin monitoring your webcam.
    When motion is detected, an image will be captured and emailed.

Important Security Note

Storing a password directly within code is not recommended for production environments. Environment variables or secure storage methods for sensitive credentials should be used to ensure proper security. This is for demonstration purposes only.