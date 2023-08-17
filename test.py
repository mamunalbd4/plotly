import plotly.express as px
df = px.data.tips()
fig = px.box(df, y="total_bill")
fig.show()