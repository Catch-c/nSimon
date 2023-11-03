# Overview [![CodeFactor](https://www.codefactor.io/repository/github/kavenci/nsimon/badge/main)](https://www.codefactor.io/repository/github/kavenci/nsimon/overview/main)
nSimon is a restyled version of the SFX Simon website that makes API calls to SFX Simon to enhance its functionality and improve the overall look and feel. It has been developed to provide students with a more user-friendly and visually appealing experience while still leveraging the existing data and functionality of SFX Simon.

# Features
## Improved User Interface: 
nSimon offers a modern and intuitive user interface, making it easier for students to navigate and use SFX Simon's features.

## Enhanced Integration: 
By making API calls to SFX Simon and having control over frontend code, nSimon allows for smoother integration with other tools and services, enabling students to streamline their academic activities.

## Custom Styling: 
nSimon comes with custom styling to enhance the visual appeal of the website, making it more engaging and user-friendly.

## Responsive Design: 
The website is designed to be responsive, ensuring a seamless experience across various devices, including desktops, tablets, and mobile phones.

## Accessibility: 
We have prioritized accessibility to ensure that all students, regardless of their abilities, can use nSimon effectively.

# Getting Started
Follow these steps to get started with nSimon:

Clone the Repository:

Copy code
```
git clone https://github.com/yourusername/nSimon.git
```
Make a config.ini file as followed and set a secure flask secret
```
[Flask]
flask.secret = setthis
```

Install Dependencies:

```
cd nSimon
pip install -r requirements.txt
playwright install
```
Run the Application:

```
python start.py
```
Access nSimon:
Open your web browser and go to http://localhost:8080 to access nSimon.

# Contributing
We welcome contributions from the community to help make nSimon even better. If you'd like to contribute, please follow these guidelines:

# Fork the repository on GitHub.
Create a new branch from the main branch for your work.
Make your changes, ensuring that your code follows best practices and style guidelines.
Submit a pull request with a clear description of your changes and their purpose.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Thank you for using nSimon! We hope it enhances your student life and makes your experience with SFX Simon more enjoyable.
