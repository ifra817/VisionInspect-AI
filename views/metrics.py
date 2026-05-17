# ==============================================
# FILE: views/metrics.py
# PURPOSE: Streamlit Metrics & Evaluation Page
# ==============================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# --- Load CSS ---
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# --- Page Config ---
st.set_page_config(page_title="Model Evaluation & Metrics", layout="wide")

# --- Header ---
st.markdown("""
<div class="header">
    <h1>📊 <span class="accent">Model Metrics & Evaluation</span></h1>
    <p class="subtitle">In-depth performance evaluation and error analysis</p>
</div>
""", unsafe_allow_html=True)

# --- Sample Metrics Data ---
model_metrics = {
    'KNN': {'accuracy': 0.78, 'precision': 0.76, 'recall':0.80, 'f1':0.78, 'auc':0.84},
    'SVM': {'accuracy': 0.87, 'precision': 0.89, 'recall':0.85, 'f1':0.87, 'auc':0.92},
    'Random Forest': {'accuracy': 0.84, 'precision':0.85, 'recall':0.83, 'f1':0.84, 'auc':0.89}
}

df_metrics = pd.DataFrame(model_metrics).T
df_metrics_display = df_metrics.copy()
df_metrics_display *= 100
df_metrics_display = df_metrics_display.rename(columns={
    'accuracy':'Accuracy (%)',
    'precision':'Precision (%)',
    'recall':'Recall (%)',
    'f1':'F1-Score (%)',
    'auc':'AUC (%)'
})

# --- Show Metrics Table ---
st.subheader("Summary Table")
st.table(df_metrics_display)

# --- Interactive Metric Selection ---
st.subheader("Compare Models by Metric")
metric_choice = st.selectbox("Select Metric", options=df_metrics_display.columns)

# Bar chart for selected metric
df_bar = df_metrics_display.reset_index()
fig_bar = px.bar(df_bar, x='index', y=metric_choice, color='index',
                 color_discrete_map={'KNN':'#4A9EFF','SVM':'#FF6B6B','Random Forest':'#00D4AA'})
fig_bar.update_layout(
    title=f"{metric_choice} Comparison",
    plot_bgcolor='#111827',
    paper_bgcolor='#111827',
    font=dict(color='#E8EDF5', family='Inter'),
    showlegend=False
)
st.plotly_chart(fig_bar, use_container_width=True)

# --- Confusion Matrix Section ---
st.subheader("Confusion Matrices (Example)")

# Example confusion matrices
import numpy as np
cm_data = {
    'KNN': np.array([[78, 22],[18, 82]]),
    'SVM': np.array([[85, 15],[12, 88]]),
    'Random Forest': np.array([[83, 17],[14, 86]])
}

selected_model_cm = st.selectbox("Select Model for Confusion Matrix", options=list(cm_data.keys()))
cm = cm_data[selected_model_cm]

fig_cm = ff.create_annotated_heatmap(
    z=cm,
    x=['Pred Normal','Pred Defective'],
    y=['Actual Normal','Actual Defective'],
    colorscale='Reds',
    showscale=True
)
fig_cm.update_layout(
    plot_bgcolor='#111827',
    paper_bgcolor='#111827',
    font=dict(color='#E8EDF5', family='Inter')
)
st.plotly_chart(fig_cm, use_container_width=True)

# --- ROC Curves ---
st.subheader("ROC Curves")
roc_data = {
    'KNN':[0.0,0.3,0.5,0.7,1.0],
    'SVM':[0.0,0.2,0.4,0.6,1.0],
    'Random Forest':[0.0,0.25,0.45,0.65,1.0]
}
fig_roc = px.area()
for model, fpr in roc_data.items():
    tpr = np.array([0,0.6,0.7,0.85,1.0])
    fig_roc.add_scatter(x=fpr, y=tpr, name=model, mode='lines+markers')
fig_roc.update_layout(
    title="ROC Curves",
    xaxis_title="False Positive Rate",
    yaxis_title="True Positive Rate",
    plot_bgcolor='#111827',
    paper_bgcolor='#111827',
    font=dict(color='#E8EDF5', family='Inter')
)
st.plotly_chart(fig_roc, use_container_width=True)

# --- Key Takeaways Section ---
st.subheader("Key Insights")
st.markdown("""
<ul class="takeawaysGrid">
<li class="takeaway"><span class="takeawayIcon">🎯</span> SVM provides highest overall accuracy and AUC.</li>
<li class="takeaway"><span class="takeawayIcon">⚡</span> KNN is fastest but less accurate.</li>
<li class="takeaway"><span class="takeawayIcon">🌳</span> Random Forest balances speed and accuracy well.</li>
<li class="takeaway"><span class="takeawayIcon">🔬</span> Confusion matrices show low misclassification for SVM.</li>
</ul>
""", unsafe_allow_html=True)