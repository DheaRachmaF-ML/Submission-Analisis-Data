# Submission-Analisis-Data

## Setup Environment - Terminal
```
python -m venv myenv1

myenv\Scripts\activate

pip install -r requirements.txt
```

## Setup Environment - Google Colab
```
!pip install -q streamlit

!npm install localtunnel
```

## Run steamlit app
```
!streamlit run dashboard.py &>/content/logs.txt & npx localtunnel --port 8501 & curl ipv4.icanhazip.com
```
