# ==============================================
# FILE: views/model_compare.py
# PURPOSE: Streamlit-based Model Comparison Page
# ==============================================
import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.markdown("""
    <div class="vi-page-title">⚖️ Model <span>Comparison</span></div>
    <div class="vi-page-subtitle">
        Comprehensive performance analysis of three classifier models
    </div>
    """, unsafe_allow_html=True)

    # --- Best Model Banner ---
    st.markdown("""
    <div class="bestModelBanner">
        <div class="badgeContent">
            <span class="crown">🏆</span>
            <div>
                <h3 class="badgeTitle">RECOMMENDED MODEL</h3>
                <p class="badgeText"><strong>SVM (RBF Kernel)</strong> — Best accuracy at 87% with confidence score of 0.92 AUC</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Model Data ---
    model_data = {
        'KNN': {'accuracy': 0.78, 'precision': 0.76, 'recall': 0.8, 'f1':0.78, 'training_time':2.1, 'auc':0.84, 'description':'Simple and fast. Works well for this dataset by finding similar images in training data.'},
        'SVM': {'accuracy': 0.87, 'precision': 0.89, 'recall': 0.85, 'f1':0.87, 'training_time':5.3, 'auc':0.92, 'description':'Finds the best boundary between normal and defective screens. Most accurate for crack detection.', 'isBest': True},
        'Random Forest': {'accuracy':0.84,'precision':0.85,'recall':0.83,'f1':0.84,'training_time':4.8,'auc':0.89, 'description':'Ensemble of decision trees. Robust and interpretable, good balance of speed and accuracy.'}
    }

    # --- Metrics Table ---
    df_metrics = pd.DataFrame(model_data).T
    df_display = df_metrics.copy()
    df_display[['accuracy','precision','recall','f1','auc']] *= 100
    df_display = df_display.rename(columns={
        'accuracy':'Accuracy (%)',
        'precision':'Precision (%)',
        'recall':'Recall (%)',
        'f1':'F1-Score (%)',
        'auc':'AUC (%)',
        'training_time':'Training Time (s)'
    })
    st.subheader("Detailed Metrics Summary")
    st.table(df_display)

    # --- Performance Metrics Comparison Chart ---
    st.subheader("Performance Metrics Comparison")
    metrics = ['Accuracy (%)','Precision (%)','Recall (%)','F1-Score (%)','AUC (%)']
    df_plot = df_display.reset_index().melt(id_vars='index', var_name='Metric', value_name='Value')
    fig = px.bar(df_plot, x='Metric', y='Value', color='index', barmode='group',
                color_discrete_map={'KNN':'#4A9EFF','SVM':'#FF6B6B','Random Forest':'#00D4AA'})
    fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827', font=dict(color='#E8EDF5', family='Inter'))
    st.plotly_chart(fig, use_container_width=True)

    # --- Training Time vs Accuracy Trade-off ---
    st.subheader("Training Time vs Accuracy Trade-off")
    df_speed = df_display.reset_index()
    # Ensure 'Accuracy (%)' column is numeric
    df_speed['Accuracy (%)'] = pd.to_numeric(df_speed['Accuracy (%)'], errors='coerce')

    # Drop rows where conversion failed (optional, safe)
    df_speed = df_speed.dropna(subset=['Accuracy (%)'])

    fig2 = px.scatter(
        df_speed,
        x='Training Time (s)',
        y='Accuracy (%)',
        text='index',
        size='Accuracy (%)',  # now guaranteed numeric
        color='index',
        color_discrete_map={'KNN':'#4A9EFF','SVM':'#FF6B6B','Random Forest':'#00D4AA'}
    )
    fig2.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827', font=dict(color='#E8EDF5', family='Inter'))
    st.plotly_chart(fig2, use_container_width=True)

    # --- Model Descriptions ---
    st.subheader("How Each Model Works")
    for name, model in model_data.items():
        is_best = model.get('isBest', False)
        best_html = '<span class="bestBadge">BEST</span>' if is_best else ''
        st.markdown(f"""
        <div class="descCard" style="border-left:3px solid {('#FF6B6B' if name=='SVM' else '#4A9EFF' if name=='KNN' else '#00D4AA')}">
            <div class="descHeader">
                <span class="descIcon">{"🔍" if name=="KNN" else "⚡" if name=="SVM" else "🌲"}</span>
                <h3 class="descTitle">{name} {best_html}</h3>
            </div>
            <p class="descText">{model['description']}</p>
            <div class="descStats">
                <div class="stat">
                    <span class="statLabel">Accuracy</span>
                    <span class="statValue">{model['accuracy']*100:.1f}%</span>
                </div>
                <div class="stat">
                    <span class="statLabel">Speed</span>
                    <span class="statValue">{model['training_time']}s</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- GridSearch Heatmap (SVM) ---
    st.subheader("SVM Hyperparameter Tuning (GridSearch)")
    grid_data = [
        {'C':'0.1','scale':82.1,'auto':80.5,'0.001':78.3,'0.01':81.2},
        {'C':'1','scale':84.5,'auto':83.2,'0.001':81.8,'0.01':84.1},
        {'C':'10','scale':87.2,'auto':86.9,'0.001':85.4,'0.01':86.8},
        {'C':'100','scale':86.8,'auto':86.5,'0.001':85.1,'0.01':86.3}
    ]

    # Render heatmap table
    heatmap_html = '<table class="heatmapTable"><thead><tr><th>C / Gamma</th><th>scale</th><th>auto</th><th>0.001</th><th>0.01</th></tr></thead><tbody>'
    for row in grid_data:
        heatmap_html += f"<tr><td><strong>{row['C']}</strong></td>"
        for key in ['scale','auto','0.001','0.01']:
            heatmap_html += f'<td class="heatmapCell" style="background-color: rgba(255,107,107,{row[key]/100});">{row[key]:.1f}</td>'
        heatmap_html += "</tr>"
    heatmap_html += "</tbody></table>"
    st.markdown(heatmap_html, unsafe_allow_html=True)

    # --- Key Takeaways ---
    st.subheader("Key Takeaways")
    st.markdown("""
    <div class="takeawaysGrid">
    <div class="takeaway">
        <span class="takeawayIcon">🎯</span>
        <h4>SVM Outperforms</h4>
        <p>SVM with RBF kernel achieves the highest accuracy and AUC, making it the production choice.</p>
    </div>
    <div class="takeaway">
        <span class="takeawayIcon">⚡</span>
        <h4>KNN Speed</h4>
        <p>KNN trains fastest but sacrifices ~9% accuracy. Good for rapid prototyping.</p>
    </div>
    <div class="takeaway">
        <span class="takeawayIcon">🌳</span>
        <h4>Random Forest Balance</h4>
        <p>RF offers good balance between speed and accuracy with high interpretability.</p>
    </div>
    <div class="takeaway">
        <span class="takeawayIcon">🔬</span>
        <h4>Recall is Critical</h4>
        <p>In defect detection, missing a crack is costlier than a false alarm. All models perform well on recall.</p>
    </div>
    </div>
    """, unsafe_allow_html=True)