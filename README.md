SkinSense – AI-Based Skin Analysis System

SkinSense is an AI-powered web application designed to support preliminary skin condition analysis through image classification. It provides personalized skincare recommendations and connects users with dermatologists through an online consultation platform.

Features

- AI-Based Skin Analysis: Analyzes uploaded skin images using a deep learning image classification model.
- Personalized Skincare Recommendations: Suggests skincare products based on the analysis results.
- Doctor Consultation: Allows users to connect with doctors through appointment booking and video consultations.
- User Management: Supports user registration, login, and profile management.
- Doctor Management: Provides features for doctors to manage their profiles and appointments.
- Admin Dashboard: Allows administrators to manage users, doctors, products, and complaints.

AI Model

SkinSense uses a fine-tuned DINOv2-base Vision Transformer (ViT) model for skin condition image classification.

The model integration uses Hugging Face Transformers for image processing and classification.

Technologies Used

Category| Technologies
Programming Language| Python
Backend Framework| Django
Frontend| HTML, CSS, JavaScript
Database| SQLite3
Deep Learning| Vision Transformer (ViT), DINOv2
AI Framework| Hugging Face Transformers

System Modules

1. User Module – Upload skin images, view analysis results, explore skincare recommendations, and book doctor appointments.
2. Doctor Module – Manage doctor profiles and handle consultation appointments.
3. Admin Module – Manage users, doctors, products, and complaints.

Installation and Setup

1. Clone the repository

git clone https://github.com/Adithyakrishna-rs/SkinSense-AI-Skin-Analysis.git

2. Navigate to the project directory

cd SkinSense-AI-Skin-Analysis

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Configure the required environment variables for Django, email services, and API integrations.

Never upload passwords, API keys, or secret keys to GitHub.

5. Apply database migrations

python manage.py migrate

6. Start the development server

python manage.py runserver

Open the following address in your browser:

"http://127.0.0.1:8000/"

Project Purpose

The main objective of SkinSense is to combine artificial intelligence with web-based healthcare services to make preliminary skin condition analysis and dermatology consultations more accessible.

Future Enhancements

- Development of a mobile application.
- Improved AI model accuracy and classification capabilities.
- Additional skin condition categories.
- Enhanced telemedicine features.

Project Information

Project Name: SkinSense – AI-Based Skin Analysis System
Project Type: Academic Major Project
Framework: Django
AI Model: DINOv2-base Vision Transformer

---

Note: SkinSense is intended for preliminary analysis and educational purposes. It does not replace professional medical diagnosis or consultation.
