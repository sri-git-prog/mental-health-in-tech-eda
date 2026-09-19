# Mental Health in Tech: An EDA of Workplace Attitudes and Treatment Seeking

An exploratory data analysis of the 2014 OSMI Mental Health in Tech survey, looking at what
predicts whether a tech employee seeks treatment for a mental health condition, and where employer
policy actually makes a difference.

## Project overview

The dataset has 1259 responses covering demographics, workplace policies, and personal attitudes
toward mental health. This project cleans the raw data, explores it through 15 charts plus a
correlation heatmap and pair plot, and closes with concrete recommendations for tech employers
based on what the data actually shows.

The core finding: personal factors like family history and symptom severity are the strongest
predictors of treatment seeking, and employers cannot influence either. Among the factors employers
can control, clarity of communication around benefits, care options, and leave policy stood out.
Employees who were unsure what was available to them behaved much more like employees with no
support at all than like employees who knew their support clearly.

## Files in this repository

| File | Description |
|---|---|
| `EDA_Mental_Health_in_Tech.ipynb` | Full analysis notebook, cleaning, 15 charts with written insights, correlation heatmap, pair plot, and business recommendations |
| `survey.csv` | The raw dataset |
| `streamlit_app.py` | Interactive app to explore the data by country, gender, company size, and age |
| `requirements.txt` | Python dependencies for the Streamlit app |
| `video_script.md` | Script used for the video walkthrough of this project |

## Running the notebook

```
pip install -r requirements.txt
jupyter notebook EDA_Mental_Health_in_Tech.ipynb
```

## Running the Streamlit app locally

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Live app

https://mental-health-in-tech-eda-crssgodm9g9v9d6uu6yu3r.streamlit.app/

## Dataset source

2014 OSMI Mental Health in Tech Survey

## Author

Vemula Sai Srikar
[LinkedIn](https://linkedin.com/in/srikarvemula) | [GitHub](https://github.com/sri-git-prog)
