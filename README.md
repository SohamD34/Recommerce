# E-Commerce Recommendation System

## Project Overview
This project demonstrates the development of an e-commerce recommendation system using Flask and machine learning techniques. The system provides personalized product suggestions to users, enhancing their shopping experience. It incorporates content-based, collaborative filtering, hybrid, and multi-model recommendation approaches, and integrates seamlessly with a Flask-based e-commerce website.

---

## Project Directory Structure
```
E-Commerce-Recommendation-System/
├── README.md
├── LICENSE
├── static/
├── templates/
│   ├── main.html
│   └── index.html
├── data/
│   ├── marketing_sample_for_walmart_com-walmart_com_product_review__20200701_20201231__5k_data.tsv    (raw data)
│   ├── processed_train_data.csv        (processed data)
│   └── trending_products.csv           (trending products log)
├── utils/
│   ├── preprocessing.py
│   └── recommendation.py
├── app.py
├── preprocess.ipynb
├── recommendations.ipynb
├── requirements.txt
└── setup.sh
```

---

## Setting Up the Project Directory
Follow these steps to set up the project directory and run the project:

1. **Clone the repository:**
    ```bash
    git clone https://www.github.com/SohamD34/Recommerce.git
    cd Recommerce/
    ```

2. **Set up the Python environment:**
    Use the provided `setup.sh` script to create and activate a Python virtual environment, and install the required dependencies:
    ```bash
    bash setup.sh
    source venv/bin/activate
    ```

3. **Run the Flask application:**
    Start the application by running the `app.py` script:
    ```bash
    python app.py
    ```

Your project is now set up and ready for development!