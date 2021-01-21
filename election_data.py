
import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
import urllib, altair as alt
'''
# Election Data
**Powered by Streamlit.io**
'''

'''
#
## 538 Democratic Primary Election Data Example
**By Nathan Silvers**
'''
df_online=pd.read_csv("https://raw.githubusercontent.com/fivethirtyeight/data/master/media-mentions-2020/online_weekly.csv")
df_online.head()
dfO= df_online[['name','matched_stories']]
dfO= dfO.groupby("name")["matched_stories"].sum()
dfO = pd.DataFrame(dfO)
dfToShow= dfO.sort_values("matched_stories", ascending=False)
dfToShow.head()
st.bar_chart(dfToShow)

'''
#
## UN Data
'''
def get_UN_data():
    AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")

df = get_UN_data()
countries = st.multiselect(
    "Choose countries", list(df.index), ["China", "United States of America"]
)
if not countries:
    st.error("Please select at least one country.")
else:
    data = df.loc[countries]
    data /= 1000000.0
    st.write("### Gross Agricultural Production ($B)", data.sort_index())
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["index"]).rename(
        columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
    )
    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.3)
        .encode(
            x="year:T",
            y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
            color="Region:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)
