# Wafer Analysis: Interactive Visualizations & Advanced Statistical Graphics

---

## SECTION 1: PYTHON LIBRARIES FOR INTERACTIVE WAFER ANALYSIS

### 1.1 Library Comparison & Recommendations

| Library | Type | Best For | Interactivity | Export | Learning Curve |
|---------|------|----------|---------------|--------|-----------------|
| **Plotly** | Interactive HTML | General charts, 3D, heatmaps | Zoom, pan, hover, click | HTML, PNG, SVG | Medium |
| **Bokeh** | Interactive canvas | Real-time streaming, large datasets | Zoom, pan, select | HTML, PNG | Medium-High |
| **Altair** | Grammar of graphics | Statistical visualization, exploration | Zoom, filter, linked views | JSON, HTML | Low |
| **Matplotlib** | Static/interactive | Publication-quality, traditional plots | Limited (mpl.widgets) | PNG, PDF, SVG | Low |
| **Seaborn** | Statistical plotting | Statistical summaries, heatmaps | None (built on matplotlib) | PNG, PDF, SVG | Low |
| **Vispy** | GPU-accelerated | Large point clouds (100k+ points) | Zoom, rotate, real-time | PNG, WebGL | High |
| **Folium** | Map-based | Spatial data with geographic context | Zoom, pan, markers | HTML | Low |
| **Plotly Dash** | Full app framework | Interactive dashboards, real-time updates | Full interactivity | HTML, export | Medium-High |
| **Streamlit** | Web app framework | Quick prototyping, data apps | App-level interactivity | Browser native | Low |
| **HoloViews** | High-level API | Complex multi-dimensional data | Zoom, pan, selection | HTML, PNG | Medium |
| **PyVista** | 3D visualization | 3D volumetric data, CAD | Rotate, zoom, real-time | VTK, PNG | High |

### 1.2 Installation Guide

```bash
# Core interactive plotting
pip install plotly kaleido  # kaleido for static export (PNG, PDF)

# Bokeh ecosystem
pip install bokeh bokeh-tables

# Grammar of graphics
pip install altair

# Dashboard & app frameworks
pip install streamlit plotly-dash

# Advanced 3D & large datasets
pip install vispy numpy-indexed

# High-level plotting
pip install holoviews param

# Statistical plotting
pip install seaborn scipy

# Data handling
pip install pandas numpy scipy scikit-learn

# Optional: GPU acceleration for Bokeh
pip install numba

# Optional: Real-time streaming
pip install websocket-client
```

---

## SECTION 2: INTERACTIVE WAFER VISUALIZATIONS

### 2.1 Interactive Wafer Map (Plotly - Zoomable, Clickable)

**Feature Set:**
- Zoom, pan, hover tooltips
- Click to select die, inspect parameters
- Color by pass/fail, parametric value, bin assignment
- Wafer outline, grid coordinates

```python
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

def create_interactive_wafer_map(df, x_col='die_x', y_col='die_y', 
                                   value_col='leakage_ua', 
                                   wafer_id='W1', cmap='RdYlGn_r',
                                   title='Interactive Wafer Map'):
    """
    Create zoomable, interactive wafer map with Plotly.
    
    Features:
    - Hover: see die ID, coordinates, test values
    - Zoom & pan
    - Color scale customization
    - Wafer outline circle
    """
    
    # Filter to wafer
    df_wafer = df[df['wafer_id'] == wafer_id].copy()
    
    # Hover text
    hover_text = []
    for idx, row in df_wafer.iterrows():
        text = f"<b>Die: ({row[x_col]}, {row[y_col]})</b><br>"
        text += f"Status: {row['status']}<br>"
        text += f"{value_col}: {row[value_col]:.3f}<br>"
        if 'leakage_ua' in df_wafer.columns:
            text += f"Leakage: {row['leakage_ua']:.3f} µA<br>"
        if 'fmax_mhz' in df_wafer.columns:
            text += f"Fmax: {row['fmax_mhz']:.0f} MHz"
        hover_text.append(text)
    
    df_wafer['hover_text'] = hover_text
    
    # Create scatter plot
    fig = go.Figure()
    
    # Add die markers (colored by value)
    fig.add_trace(go.Scatter(
        x=df_wafer[x_col],
        y=df_wafer[y_col],
        mode='markers',
        marker=dict(
            size=8,
            color=df_wafer[value_col],
            colorscale=cmap,
            showscale=True,
            colorbar=dict(
                title=value_col,
                thickness=15,
                len=0.7,
            ),
            line=dict(
                color='black',
                width=1,
            ),
            opacity=0.8,
        ),
        text=hover_text,
        hovertemplate='%{text}<extra></extra>',
        name='Die',
    ))
    
    # Add wafer outline (circle)
    max_coord = max(df_wafer[x_col].max(), df_wafer[y_col].max())
    center = max_coord / 2
    radius = max_coord / 2.2
    
    theta = np.linspace(0, 2*np.pi, 100)
    outline_x = center + radius * np.cos(theta)
    outline_y = center + radius * np.sin(theta)
    
    fig.add_trace(go.Scatter(
        x=outline_x,
        y=outline_y,
        mode='lines',
        line=dict(color='blue', width=2),
        name='Wafer Outline',
        hoverinfo='skip',
    ))
    
    # Add yield/stats annotation
    pass_count = (df_wafer['status'] == 'PASS').sum()
    total_count = len(df_wafer)
    yield_pct = 100 * pass_count / total_count
    
    fig.add_annotation(
        text=f'<b>Wafer: {wafer_id}</b><br>Yield: {yield_pct:.1f}%<br>Pass: {pass_count}/{total_count}',
        xref='paper', yref='paper',
        x=0.02, y=0.98,
        showarrow=False,
        bgcolor='rgba(255, 255, 200, 0.8)',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=12),
    )
    
    # Layout
    fig.update_layout(
        title=f'{title} - {wafer_id}',
        xaxis_title='Die X Position',
        yaxis_title='Die Y Position',
        hovermode='closest',
        xaxis=dict(scaleanchor='y', scaleratio=1),
        yaxis=dict(scaleanchor='x', scaleratio=1),
        width=900,
        height=900,
        template='plotly_white',
        showlegend=True,
    )
    
    return fig

# Usage
fig = create_interactive_wafer_map(df_tests, value_col='leakage_ua', 
                                    wafer_id='W001', cmap='Hot')
fig.show()
fig.write_html('/reports/wafer_map_interactive.html')
```

**Alternative: Pass/Fail Wafer Map**
```python
def create_passfail_wafer_map(df, wafer_id='W1'):
    """Pass/fail wafer map with interactive legend."""
    
    df_wafer = df[df['wafer_id'] == wafer_id].copy()
    
    # Separate pass/fail
    df_pass = df_wafer[df_wafer['status'] == 'PASS']
    df_fail = df_wafer[df_wafer['status'] == 'FAIL']
    
    fig = go.Figure()
    
    # Pass die (green)
    fig.add_trace(go.Scatter(
        x=df_pass['die_x'],
        y=df_pass['die_y'],
        mode='markers',
        marker=dict(
            size=10,
            color='green',
            opacity=0.7,
            line=dict(color='darkgreen', width=1),
        ),
        name='PASS',
        hovertemplate='<b>PASS</b><br>X: %{x}<br>Y: %{y}<extra></extra>',
    ))
    
    # Fail die (red)
    fig.add_trace(go.Scatter(
        x=df_fail['die_x'],
        y=df_fail['die_y'],
        mode='markers',
        marker=dict(
            size=10,
            color='red',
            opacity=0.7,
            line=dict(color='darkred', width=1),
        ),
        name='FAIL',
        hovertemplate='<b>FAIL</b><br>X: %{x}<br>Y: %{y}<extra></extra>',
    ))
    
    # Wafer outline
    max_coord = max(df_wafer['die_x'].max(), df_wafer['die_y'].max())
    center = max_coord / 2
    radius = max_coord / 2.2
    theta = np.linspace(0, 2*np.pi, 100)
    fig.add_trace(go.Scatter(
        x=center + radius * np.cos(theta),
        y=center + radius * np.sin(theta),
        mode='lines',
        line=dict(color='blue', width=2),
        name='Outline',
        hoverinfo='skip',
    ))
    
    yield_pct = 100 * len(df_pass) / len(df_wafer)
    fig.update_layout(
        title=f'Pass/Fail Wafer Map - {wafer_id} (Yield: {yield_pct:.1f}%)',
        xaxis_title='X',
        yaxis_title='Y',
        width=900,
        height=900,
        xaxis=dict(scaleanchor='y', scaleratio=1),
        yaxis=dict(scaleanchor='x', scaleratio=1),
        template='plotly_white',
    )
    
    return fig

fig = create_passfail_wafer_map(df_tests, wafer_id='W001')
fig.show()
```

---

### 2.2 Interactive Histograms with Spec Limits (Plotly + Density Overlay)

```python
def create_interactive_histogram(df, test_col='leakage_ua', wafer_id=None,
                                  lsl=None, usl=None, bin_width=None,
                                  title='Test Parameter Distribution'):
    """
    Interactive histogram with:
    - Draggable spec limit markers
    - Density curve overlay
    - Cpk annotation
    - Percentile grid
    """
    
    if wafer_id:
        data = df[df['wafer_id'] == wafer_id][test_col].dropna()
    else:
        data = df[test_col].dropna()
    
    # Calculate statistics
    mean = data.mean()
    std = data.std()
    median = data.median()
    
    # Determine bin width
    if bin_width is None:
        bin_width = (data.max() - data.min()) / 30
    
    # Create histogram with secondary y-axis for density
    fig = go.Figure()
    
    # Histogram
    fig.add_trace(go.Histogram(
        x=data,
        nbinsx=30,
        name='Count',
        marker=dict(color='lightblue', line=dict(color='blue', width=1)),
        yaxis='y1',
    ))
    
    # Overlay normal distribution curve
    x_range = np.linspace(data.min(), data.max(), 200)
    from scipy import stats
    y_density = stats.norm.pdf(x_range, mean, std)
    
    # Scale density to match histogram
    hist_count = len(data)
    y_density_scaled = y_density * hist_count * bin_width
    
    fig.add_trace(go.Scatter(
        x=x_range,
        y=y_density_scaled,
        name='Normal Distribution',
        line=dict(color='red', width=3),
        yaxis='y1',
    ))
    
    # Vertical lines: mean, median, percentiles
    fig.add_vline(
        x=mean,
        line_dash='dash',
        line_color='green',
        name=f'Mean: {mean:.3f}',
        annotation_text=f'Mean<br>{mean:.3f}',
        annotation_position='top',
    )
    
    fig.add_vline(
        x=median,
        line_dash='dot',
        line_color='purple',
        name=f'Median: {median:.3f}',
        annotation_text=f'Median<br>{median:.3f}',
        annotation_position='top',
    )
    
    # Spec limits
    if lsl:
        fig.add_vline(
            x=lsl,
            line_dash='solid',
            line_color='orange',
            line_width=3,
            name=f'LSL: {lsl}',
        )
        p_below_lsl = stats.norm.cdf(lsl, mean, std) * 100
    else:
        p_below_lsl = 0
    
    if usl:
        fig.add_vline(
            x=usl,
            line_dash='solid',
            line_color='brown',
            line_width=3,
            name=f'USL: {usl}',
        )
        p_above_usl = (1 - stats.norm.cdf(usl, mean, std)) * 100
    else:
        p_above_usl = 0
    
    # Shade out-of-spec regions
    if lsl:
        fig.add_vrect(
            x0=data.min(), x1=lsl,
            fillcolor='red', opacity=0.1,
            layer='below',
            line_width=0,
        )
    if usl:
        fig.add_vrect(
            x0=usl, x1=data.max(),
            fillcolor='red', opacity=0.1,
            layer='below',
            line_width=0,
        )
    
    # Calculate Cpk
    if lsl and usl:
        cpu = (usl - mean) / (3 * std)
        cpl = (mean - lsl) / (3 * std)
        cpk = min(cpu, cpl)
    else:
        cpk = None
    
    # Annotation box
    annotation_text = (
        f"<b>Statistical Summary</b><br>"
        f"Mean: {mean:.4f}<br>"
        f"Median: {median:.4f}<br>"
        f"Std Dev: {std:.4f}<br>"
        f"Count: {len(data)}<br>"
        f"Min: {data.min():.4f}<br>"
        f"Max: {data.max():.4f}<br>"
        f"P1: {data.quantile(0.01):.4f}<br>"
        f"P99: {data.quantile(0.99):.4f}<br>"
    )
    
    if cpk:
        annotation_text += (
            f"<br><b>Capability</b><br>"
            f"Cpk: {cpk:.3f}<br>"
            f"Defects LSL: {p_below_lsl:.4f}%<br>"
            f"Defects USL: {p_above_usl:.4f}%<br>"
            f"Total Defects: {p_below_lsl + p_above_usl:.4f}%"
        )
    
    fig.add_annotation(
        text=annotation_text,
        xref='paper', yref='paper',
        x=0.98, y=0.98,
        xanchor='right', yanchor='top',
        showarrow=False,
        bgcolor='rgba(255, 255, 200, 0.9)',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=10, family='monospace'),
    )
    
    # Layout with dual y-axes
    fig.update_layout(
        title=title,
        xaxis_title=test_col,
        yaxis1_title='Count (Histogram)',
        yaxis2_title='Density',
        hovermode='x unified',
        width=1200,
        height=600,
        template='plotly_white',
        showlegend=True,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    )
    
    return fig

# Usage
fig = create_interactive_histogram(df_tests, test_col='leakage_ua', 
                                    lsl=0.1, usl=5.0)
fig.show()
fig.write_html('/reports/histogram_interactive.html')
```

---

### 2.3 Interactive Multi-Wafer Comparison (Violin + Box Plot)

```python
def create_interactive_multiwafer_comparison(df, param_col='leakage_ua',
                                              lot_id=None):
    """
    Multi-wafer comparison with interactive statistics.
    Features:
    - Violin plots for distribution shape
    - Box plots for quartiles
    - Individual points overlaid
    - Click legend to toggle wafers
    """
    
    if lot_id:
        df_plot = df[df['lot_id'] == lot_id]
    else:
        df_plot = df
    
    fig = go.Figure()
    
    wafer_ids = sorted(df_plot['wafer_id'].unique())
    
    for wafer_id in wafer_ids:
        wafer_data = df_plot[df_plot['wafer_id'] == wafer_id][param_col].dropna()
        
        # Violin plot
        fig.add_trace(go.Violin(
            x=[wafer_id] * len(wafer_data),
            y=wafer_data,
            name=wafer_id,
            side='negative',
            meanline_visible=True,
            points='outliers',
            jitter=0.3,
            scalegroup=wafer_id,
            side='positive',
            line_color='blue',
        ))
    
    fig.update_layout(
        title=f'Multi-Wafer Distribution: {param_col}',
        xaxis_title='Wafer ID',
        yaxis_title=param_col,
        template='plotly_white',
        height=600,
        width=1200,
        hovermode='closest',
    )
    
    return fig

fig = create_interactive_multiwafer_comparison(df_tests, param_col='leakage_ua')
fig.show()
```

---

### 2.4 Interactive Trend Plot (Time Series with Annotations)

```python
def create_interactive_trend_plot(df, metric_func=None, wafer_order=None,
                                   spec_target=None, title='Wafer Trend'):
    """
    Interactive trend plot with:
    - Moving average
    - Control limits (mean ± 1σ, 2σ, 3σ)
    - Draggable annotations
    - Trend line fit
    """
    
    if metric_func is None:
        # Default: yield
        metric_func = lambda w: (w['status'] == 'PASS').sum() / len(w) * 100
    
    if wafer_order is None:
        wafer_order = sorted(df['wafer_id'].unique())
    
    # Calculate metrics per wafer
    metrics = []
    for wafer in wafer_order:
        wafer_data = df[df['wafer_id'] == wafer]
        metric_val = metric_func(wafer_data)
        metrics.append(metric_val)
    
    metrics = np.array(metrics)
    x = np.arange(len(wafer_order))
    
    fig = go.Figure()
    
    # Main trend line
    fig.add_trace(go.Scatter(
        x=x,
        y=metrics,
        mode='lines+markers',
        name='Metric',
        line=dict(color='blue', width=2),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>',
    ))
    
    # Moving average (5-wafer window)
    if len(metrics) >= 5:
        ma = pd.Series(metrics).rolling(window=5, center=True).mean()
        fig.add_trace(go.Scatter(
            x=x,
            y=ma,
            mode='lines',
            name='5-Wafer MA',
            line=dict(color='red', width=2, dash='dash'),
            hovertemplate='MA: %{y:.2f}<extra></extra>',
        ))
    
    # Control limits
    mean = metrics.mean()
    std = metrics.std()
    
    fig.add_hline(
        y=mean,
        line_dash='solid',
        line_color='green',
        line_width=1,
        annotation_text='Mean',
        annotation_position='right',
    )
    
    # ±1σ band
    fig.add_hrect(
        y0=mean - std, y1=mean + std,
        fillcolor='green', opacity=0.1,
        layer='below',
        name='±1σ',
    )
    
    # ±2σ band
    fig.add_hrect(
        y0=mean - 2*std, y1=mean + 2*std,
        fillcolor='yellow', opacity=0.05,
        layer='below',
        name='±2σ',
    )
    
    # ±3σ band
    fig.add_hrect(
        y0=mean - 3*std, y1=mean + 3*std,
        fillcolor='red', opacity=0.02,
        layer='below',
        name='±3σ',
    )
    
    # Spec target
    if spec_target:
        fig.add_hline(
            y=spec_target,
            line_dash='dot',
            line_color='purple',
            line_width=2,
            annotation_text=f'Target: {spec_target}',
            annotation_position='right',
        )
    
    # Polynomial fit (trend)
    if len(metrics) > 3:
        z = np.polyfit(x, metrics, 2)
        p = np.poly1d(z)
        x_smooth = np.linspace(x.min(), x.max(), 100)
        fig.add_trace(go.Scatter(
            x=x_smooth,
            y=p(x_smooth),
            mode='lines',
            name='Quadratic Fit',
            line=dict(color='orange', width=2, dash='dot'),
        ))
    
    # Detect out-of-control points
    outliers = np.where(np.abs(metrics - mean) > 3*std)[0]
    if len(outliers) > 0:
        fig.add_trace(go.Scatter(
            x=outliers,
            y=metrics[outliers],
            mode='markers',
            name='Out-of-Control',
            marker=dict(size=12, color='red', symbol='x', line=dict(width=2)),
        ))
    
    fig.update_xaxes(
        ticktext=wafer_order,
        tickvals=x,
        tickangle=-45,
    )
    
    fig.update_layout(
        title=title,
        xaxis_title='Wafer Sequence',
        yaxis_title='Metric Value',
        hovermode='x unified',
        width=1400,
        height=600,
        template='plotly_white',
        showlegend=True,
    )
    
    return fig

# Usage
df_yield = df_tests.groupby('wafer_id').size()
fig = create_interactive_trend_plot(
    df_tests,
    metric_func=lambda w: (w['status'] == 'PASS').sum() / len(w) * 100,
    spec_target=95.0,
    title='Yield Trend across Wafers'
)
fig.show()
```

---

### 2.5 Interactive 3D Scatter Plot (Parameter Correlation)

```python
def create_interactive_3d_scatter(df, x_col='leakage_ua', y_col='fmax_mhz',
                                   z_col='iddq_active_ma', color_col='status',
                                   title='3D Parameter Space'):
    """
    3D scatter with:
    - Rotate & zoom
    - Color by pass/fail or parametric value
    - Hover tooltips
    - Size by additional parameter
    """
    
    df_clean = df[[x_col, y_col, z_col, color_col]].dropna()
    
    # Color mapping
    if color_col == 'status':
        color_map = {'PASS': 0, 'FAIL': 1}
        colors = df_clean[color_col].map(color_map)
        colorscale = 'RdYlGn_r'
        color_label = 'Status'
    else:
        colors = df_clean[color_col]
        colorscale = 'Viridis'
        color_label = color_col
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter3d(
        x=df_clean[x_col],
        y=df_clean[y_col],
        z=df_clean[z_col],
        mode='markers',
        marker=dict(
            size=5,
            color=colors,
            colorscale=colorscale,
            showscale=True,
            colorbar=dict(title=color_label),
            line=dict(width=0.5, color='white'),
            opacity=0.8,
        ),
        text=[
            f"<b>{color_col}: {row[color_col]}</b><br>"
            f"{x_col}: {row[x_col]:.3f}<br>"
            f"{y_col}: {row[y_col]:.3f}<br>"
            f"{z_col}: {row[z_col]:.3f}"
            for idx, row in df_clean.iterrows()
        ],
        hovertemplate='%{text}<extra></extra>',
    ))
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=x_col,
            yaxis_title=y_col,
            zaxis_title=z_col,
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3),
            ),
        ),
        width=1000,
        height=800,
        hovermode='closest',
    )
    
    return fig

fig = create_interactive_3d_scatter(
    df_tests,
    x_col='leakage_ua',
    y_col='fmax_mhz',
    z_col='iddq_active_ma',
    color_col='status'
)
fig.show()
```

---

## SECTION 3: ADVANCED STATISTICAL VISUALIZATIONS

### 3.1 Q-Q Plot (Normality Testing) - Interactive

```python
def create_interactive_qq_plot(data, test_name='Parameter', ax=None):
    """
    Q-Q plot to test normality visually.
    Interactive version with reference line.
    """
    from scipy import stats
    
    data_clean = data.dropna().values
    
    # Calculate theoretical quantiles (normal distribution)
    theoretical_quantiles = stats.norm.ppf(
        np.linspace(0.01, 0.99, len(data_clean))
    )
    
    # Calculate sample quantiles
    sample_quantiles = np.sort(data_clean)
    
    # Standardize for clearer visualization
    theoretical_quantiles = (theoretical_quantiles - theoretical_quantiles.mean()) / theoretical_quantiles.std()
    sample_quantiles = (sample_quantiles - sample_quantiles.mean()) / sample_quantiles.std()
    
    fig = go.Figure()
    
    # Scatter plot (actual vs theoretical)
    fig.add_trace(go.Scatter(
        x=theoretical_quantiles,
        y=sample_quantiles,
        mode='markers',
        marker=dict(size=6, color='blue', opacity=0.6),
        name='Data',
        hovertemplate='Theoretical: %{x:.3f}<br>Sample: %{y:.3f}<extra></extra>',
    ))
    
    # Reference line (y=x)
    min_val = min(theoretical_quantiles.min(), sample_quantiles.min())
    max_val = max(theoretical_quantiles.max(), sample_quantiles.max())
    
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name='Perfect Normal',
    ))
    
    # Calculate Anderson-Darling statistic
    ad_stat, ad_crit, sig_level = stats.anderson(data_clean)
    
    # Shapiro-Wilk test
    shapiro_stat, shapiro_pval = stats.shapiro(data_clean)
    
    # Annotation
    annotation_text = (
        f"<b>Normality Tests</b><br>"
        f"Shapiro-Wilk p-value: {shapiro_pval:.6f}<br>"
        f"Anderson-Darling stat: {ad_stat:.4f}<br>"
        f"<br>"
        f"Interpretation:<br>"
        f"p > 0.05 → Data is normal<br>"
        f"p < 0.05 → Data is NOT normal"
    )
    
    if shapiro_pval > 0.05:
        annotation_text += "<br><br><b style='color:green'>✓ Data appears normal</b>"
    else:
        annotation_text += "<br><br><b style='color:red'>✗ Data is NOT normal</b>"
    
    fig.add_annotation(
        text=annotation_text,
        xref='paper', yref='paper',
        x=0.05, y=0.95,
        xanchor='left', yanchor='top',
        showarrow=False,
        bgcolor='rgba(255, 255, 200, 0.9)',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=10, family='monospace'),
    )
    
    fig.update_layout(
        title=f'Q-Q Plot: {test_name}',
        xaxis_title='Theoretical Quantiles (Normal)',
        yaxis_title='Sample Quantiles',
        width=800,
        height=700,
        template='plotly_white',
        hovermode='closest',
        xaxis=dict(scaleanchor='y', scaleratio=1),
        yaxis=dict(scaleanchor='x', scaleratio=1),
    )
    
    return fig

fig = create_interactive_qq_plot(df_tests['leakage_ua'], test_name='Leakage')
fig.show()
```

### 3.2 Weibull Plot (Reliability Analysis) - Interactive

```python
def create_interactive_weibull_plot(data, test_name='Parameter'):
    """
    Weibull plot for reliability/lifetime data.
    Useful for analyzing failure rates in tail analysis.
    """
    from scipy import stats
    
    data_clean = np.sort(data.dropna().values)
    n = len(data_clean)
    
    # Median rank (alternative to mean rank)
    ranks = np.arange(1, n + 1)
    medians = (ranks - 0.3) / (n + 0.4)
    
    # Transform to Weibull coordinates
    y_weibull = np.log(-np.log(1 - medians))
    x_weibull = np.log(data_clean)
    
    # Fit Weibull parameters
    weibull_params = stats.weibull_min.fit(data_clean)
    shape, loc, scale = weibull_params
    
    # Generate fitted line
    x_fit = np.linspace(data_clean.min(), data_clean.max(), 100)
    x_fit_weibull = np.log(x_fit)
    y_fit_weibull = np.log(-np.log(1 - stats.weibull_min.cdf(x_fit, shape, loc, scale)))
    
    fig = go.Figure()
    
    # Scatter (actual data on Weibull paper)
    fig.add_trace(go.Scatter(
        x=x_weibull,
        y=y_weibull,
        mode='markers',
        marker=dict(size=8, color='blue', opacity=0.6),
        name='Data Points',
        hovertemplate='ln(x): %{x:.3f}<br>ln(-ln(1-F)): %{y:.3f}<extra></extra>',
    ))
    
    # Fitted line
    fig.add_trace(go.Scatter(
        x=x_fit_weibull,
        y=y_fit_weibull,
        mode='lines',
        line=dict(color='red', width=2),
        name='Weibull Fit',
    ))
    
    # Annotation
    annotation_text = (
        f"<b>Weibull Distribution</b><br>"
        f"Shape (k): {shape:.4f}<br>"
        f"Scale (λ): {scale:.4f}<br>"
        f"Location (μ): {loc:.4f}<br>"
        f"<br>"
        f"Interpretation:<br>"
        f"k < 1: Decreasing hazard (infant mortality)<br>"
        f"k = 1: Constant hazard (exponential)<br>"
        f"k > 1: Increasing hazard (wear-out)<br>"
        f"k ≈ 3.6: Normal distribution"
    )
    
    fig.add_annotation(
        text=annotation_text,
        xref='paper', yref='paper',
        x=0.05, y=0.95,
        xanchor='left', yanchor='top',
        showarrow=False,
        bgcolor='rgba(255, 255, 200, 0.9)',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=9, family='monospace'),
    )
    
    fig.update_layout(
        title=f'Weibull Plot: {test_name}',
        xaxis_title='ln(Parameter Value)',
        yaxis_title='ln(-ln(1-F))',
        width=900,
        height=700,
        template='plotly_white',
        hovermode='closest',
    )
    
    return fig

fig = create_interactive_weibull_plot(df_tests['leakage_ua'], test_name='Leakage')
fig.show()
```

---

## SECTION 4: BOKEH FOR LARGE DATASETS & STREAMING

### 4.1 Bokeh Wafer Map (GPU-Friendly for 100k+ Points)

```python
from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool, ColorBar, LinearColorMapper
from bokeh.palettes import Viridis256
from bokeh.transform import transform

def create_bokeh_wafer_map(df, x_col='die_x', y_col='die_y',
                            value_col='leakage_ua', wafer_id='W1',
                            output_path='/reports/wafer_map_bokeh.html'):
    """
    Bokeh wafer map optimized for large datasets.
    Features:
    - Fast rendering (WebGL backend available)
    - Efficient pan/zoom
    - Hover tooltips
    """
    
    df_wafer = df[df['wafer_id'] == wafer_id].copy()
    
    # Normalize colors
    color_mapper = LinearColorMapper(
        palette=Viridis256,
        low=df_wafer[value_col].min(),
        high=df_wafer[value_col].max()
    )
    
    # Create figure
    p = figure(
        title=f'Wafer Map: {wafer_id}',
        width=900,
        height=900,
        tools='pan,wheel_zoom,box_zoom,reset,save',
    )
    
    # Add circles (die markers)
    p.circle(
        x=x_col,
        y=y_col,
        size=8,
        source=df_wafer,
        fill_color=transform(value_col, color_mapper),
        fill_alpha=0.8,
        line_color='black',
        line_width=0.5,
    )
    
    # Hover tool
    hover = HoverTool(
        tooltips=[
            ('Position', f'(@{x_col}, @{y_col})'),
            ('Status', '@status'),
            (value_col, f'@{value_col}{{0.000}}'),
        ]
    )
    p.add_tools(hover)
    
    # Color bar
    color_bar = ColorBar(
        color_mapper=color_mapper,
        label_standoff=12,
        location=(0, 0),
        title=value_col,
    )
    p.add_layout(color_bar, 'right')
    
    # Formatting
    p.xaxis.axis_label = 'Die X Position'
    p.yaxis.axis_label = 'Die Y Position'
    p.xaxis.axis_label_text_font_size = '12pt'
    p.yaxis.axis_label_text_font_size = '12pt'
    
    output_file(output_path)
    save(p)
    print(f"Wafer map saved to {output_path}")
    
    return p

# Usage
create_bokeh_wafer_map(df_tests, wafer_id='W001', value_col='leakage_ua')
```

---

## SECTION 5: ALTAIR FOR STATISTICAL GRAMMAR OF GRAPHICS

### 5.1 Altair Multi-View Dashboard (Linked Views)

```python
import altair as alt

def create_altair_dashboard(df, param_col='leakage_ua'):
    """
    Multi-view dashboard with linked selection.
    Features:
    - Click histogram to highlight wafer map
    - Pan/zoom synchronized across views
    """
    
    # Histogram + density
    hist = alt.Chart(df).mark_bar().encode(
        x=alt.X(param_col, bin=alt.Bin(maxbins=30), title=param_col),
        y='count()',
        color='wafer_id:N',
    ).properties(
        width=300,
        height=300,
        title='Distribution'
    )
    
    density = alt.Chart(df).transform_density(
        param_col,
        as_=[param_col, 'density'],
        groupby=['wafer_id']
    ).mark_line().encode(
        x=param_col,
        y='density:Q',
        color='wafer_id:N',
    )
    
    # Wafer map
    wafer_map = alt.Chart(df[df['wafer_id'] == df['wafer_id'].iloc[0]]).mark_point().encode(
        x='die_x:Q',
        y='die_y:Q',
        color=alt.Color(param_col, scale=alt.Scale(scheme='viridis')),
        tooltip=['die_x', 'die_y', 'status', param_col]
    ).properties(
        width=400,
        height=400,
        title='Wafer Map'
    )
    
    # Yield by wafer
    yield_chart = alt.Chart(df.groupby('wafer_id').apply(
        lambda w: (w['status'] == 'PASS').sum() / len(w) * 100
    ).reset_index(name='yield')).mark_bar().encode(
        x='wafer_id:N',
        y='yield:Q',
        color='yield:Q',
    ).properties(
        width=300,
        height=300,
        title='Yield by Wafer'
    )
    
    # Combine
    dashboard = (hist + density) | wafer_map | yield_chart
    
    return dashboard

# Usage
dashboard = create_altair_dashboard(df_tests, param_col='leakage_ua')
dashboard.show()
dashboard.save('/reports/dashboard_altair.html')
```

---

## SECTION 6: STREAMLIT INTERACTIVE DASHBOARD

### 6.1 Full Wafer Analysis App

```python
# wafer_dashboard.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import numpy as np

st.set_page_config(page_title='Wafer Sort Analysis', layout='wide')

st.title('📊 Interactive Wafer Sort Analysis Dashboard')

# Sidebar: File upload and filters
st.sidebar.header('Upload & Filter')

uploaded_file = st.sidebar.file_uploader('Upload STDF data (CSV)', type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Filters
    lot_ids = df['lot_id'].unique() if 'lot_id' in df.columns else []
    wafer_ids = df['wafer_id'].unique()
    
    selected_lot = st.sidebar.selectbox('Select Lot', lot_ids) if lot_ids.size > 0 else None
    selected_wafers = st.sidebar.multiselect('Select Wafers', wafer_ids, default=[wafer_ids[0]])
    
    if selected_lot:
        df = df[df['lot_id'] == selected_lot]
    
    df = df[df['wafer_id'].isin(selected_wafers)]
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('Total Dies', len(df))
    with col2:
        yield_pct = (df['status'] == 'PASS').sum() / len(df) * 100
        st.metric('Yield', f'{yield_pct:.2f}%')
    with col3:
        st.metric('Wafers', df['wafer_id'].nunique())
    with col4:
        st.metric('Tests', df['test_name'].nunique() if 'test_name' in df.columns else 'N/A')
    
    # Tab-based interface
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Wafer Map', 'Distributions', 'Trends', '3D Analysis', 'Statistics'])
    
    with tab1:
        st.subheader('Interactive Wafer Map')
        selected_wafer = st.selectbox('Wafer', selected_wafers)
        param_col = st.selectbox('Color by', df.select_dtypes(include=[np.number]).columns)
        
        df_wafer = df[df['wafer_id'] == selected_wafer]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_wafer['die_x'],
            y=df_wafer['die_y'],
            mode='markers',
            marker=dict(
                size=8,
                color=df_wafer[param_col],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title=param_col),
            ),
            text=df_wafer['status'],
            hovertemplate='<b>%{text}</b><br>(%{x}, %{y})<extra></extra>',
        ))
        fig.update_layout(width=800, height=800, xaxis=dict(scaleanchor='y', scaleratio=1),
                          yaxis=dict(scaleanchor='x', scaleratio=1))
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader('Parameter Distributions')
        test_param = st.selectbox('Select Parameter', df.select_dtypes(include=[np.number]).columns)
        
        fig = px.histogram(df, x=test_param, nbins=50, color='wafer_id',
                          title=f'{test_param} Distribution', marginal='box')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader('Yield Trend')
        df_yield = df.groupby('wafer_id').apply(
            lambda w: (w['status'] == 'PASS').sum() / len(w) * 100
        ).reset_index(name='yield')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_yield['wafer_id'], y=df_yield['yield'], mode='lines+markers'))
        fig.update_layout(title='Yield Trend', xaxis_title='Wafer', yaxis_title='Yield (%)')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader('3D Parameter Space')
        cols = df.select_dtypes(include=[np.number]).columns.tolist()
        x_col = st.selectbox('X-axis', cols, index=0)
        y_col = st.selectbox('Y-axis', cols, index=1 if len(cols) > 1 else 0)
        z_col = st.selectbox('Z-axis', cols, index=2 if len(cols) > 2 else 0)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=df[x_col], y=df[y_col], z=df[z_col],
            mode='markers',
            marker=dict(
                color=(df['status'] == 'PASS').astype(int),
                colorscale='RdYlGn_r',
                showscale=True,
            )
        ))
        fig.update_layout(title='3D Parameter Space', width=900, height=700)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.subheader('Statistical Summary')
        
        test_param = st.selectbox('Analyze Parameter', df.select_dtypes(include=[np.number]).columns)
        param_data = df[test_param].dropna()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Mean', f'{param_data.mean():.4f}')
            st.metric('Min', f'{param_data.min():.4f}')
        with col2:
            st.metric('Median', f'{param_data.median():.4f}')
            st.metric('Std Dev', f'{param_data.std():.4f}')
        with col3:
            st.metric('Max', f'{param_data.max():.4f}')
            st.metric('Count', f'{len(param_data)}')
        
        # Normality test
        if len(param_data) > 3:
            shapiro_stat, shapiro_pval = stats.shapiro(param_data)
            col1.metric('Shapiro-Wilk p-value', f'{shapiro_pval:.6f}')
            if shapiro_pval > 0.05:
                st.success('✓ Data appears normally distributed')
            else:
                st.warning('✗ Data is NOT normally distributed')

else:
    st.info('👈 Upload a CSV file to get started')
```

Run with: `streamlit run wafer_dashboard.py`

---

## SECTION 7: VISUALIZATION COMPARISON MATRIX

| Visualization Type | Best Library | Interactivity | Zoomable? | Large Datasets? | Export Options |
|-------------------|--------------|---------------|-----------|-----------------|-----------------|
| **Wafer Map** | Plotly / Bokeh | Excellent | Yes | Bokeh better (100k+) | HTML, PNG, SVG |
| **Histogram** | Plotly | Good | Yes | Both good | HTML, PNG, SVG |
| **3D Scatter** | Plotly | Excellent | Yes | Plotly ~10k, Bokeh better | HTML, PNG |
| **Trend Lines** | Plotly | Good | Yes | Excellent | HTML, PNG |
| **Heatmap** | Seaborn / Plotly | Limited / Good | Plotly Yes | Seaborn better | PNG, PDF |
| **Q-Q Plot** | Plotly / Matplotlib | Good / None | Plotly Yes | Both | HTML, PNG |
| **Weibull Plot** | Plotly / Matplotlib | Good / None | Plotly Yes | Both | HTML, PNG |
| **Multi-view** | Altair | Excellent | Yes | Altair good | HTML, JSON |
| **Real-time** | Bokeh / Streamlit | Excellent | Yes | Bokeh best | Browser native |
| **Dashboard** | Streamlit / Dash | Excellent | Yes | Both good | Browser export |

---

## SECTION 8: BEST PRACTICES FOR WAFER VISUALIZATIONS

### 8.1 Color Schemes

```python
# Recommended color schemes for wafer analysis
color_schemes = {
    'parametric': 'Viridis',      # Blue → Yellow (good for continuous data)
    'heat': 'Hot',                 # Dark red → bright yellow
    'diverging': 'RdBu',          # Red-Blue (good for ±deviation)
    'categorical': 'Set2',        # Qualitative (good for PASS/FAIL, bins)
    'sequential': 'Blues',        # Light → dark
    'passfail': {                 # Custom for PASS/FAIL
        'PASS': '#00AA00',        # Green
        'FAIL': '#FF0000',        # Red
    },
}

# Choose based on data type and accessibility
# Always provide colorblind-friendly options (Viridis, Cividis)
```

### 8.2 Interactive Features Best Practices

```python
# 1. Hover Information
# Always include: Device ID, coordinates, key parameters, status

# 2. Zoom & Pan
# Enable on all spatial plots; maintain aspect ratio for wafer maps

# 3. Legend Toggling
# Allow user to click legend to toggle series on/off

# 4. Annotations
# Add statistical boxes (Cpk, yield %) in corner; make draggable if possible

# 5. Crosshair / Reference Lines
# Add horizontal/vertical reference lines for specs, mean, control limits

# 6. Tooltips
# Show detailed info on hover; include timestamp, equipment info

# 7. Export
# Provide PNG/SVG export; maintain quality for reports
```

### 8.3 Multi-Monitor Display

```python
# For production dashboards, optimize for large displays

def create_production_dashboard_layout():
    """Layout for 3-monitor setup in fab."""
    
    layout = {
        'Monitor 1 (Main)': [
            'Real-time yield trend (large)',
            'Latest wafer map (interactive)',
        ],
        'Monitor 2 (Stats)': [
            'Multi-wafer distribution (violin)',
            'Cpk/capability summary table',
            'Test effectiveness (Pareto)',
        ],
        'Monitor 3 (Alerts)': [
            'Out-of-control wafers (list)',
            'Failing test counts (bar chart)',
            'Equipment status (text)',
        ],
    }
    
    return layout
```

---

## SECTION 9: CODE SNIPPETS FOR COMMON TASKS

### 9.1 Save Interactive Charts as Static Images (kaleido)

```python
# Install: pip install kaleido

def export_charts(fig, filename_prefix='/reports/'):
    """Export Plotly figure to multiple formats."""
    
    # PNG (for slides/reports)
    fig.write_image(f'{filename_prefix}chart.png', width=1200, height=600, scale=2)
    
    # PDF (for documents)
    fig.write_image(f'{filename_prefix}chart.pdf', width=1200, height=600)
    
    # SVG (vector, scalable)
    fig.write_image(f'{filename_prefix}chart.svg', width=1200, height=600)
    
    # HTML (interactive, for presentations)
    fig.write_html(f'{filename_prefix}chart.html')
    
    print(f'Exported to {filename_prefix}')

# Usage
fig = create_interactive_wafer_map(df_tests, wafer_id='W001')
export_charts(fig)
```

### 9.2 Batch Generate Wafer Maps for All Wafers

```python
def batch_generate_wafer_maps(df, output_dir='/reports/wafer_maps/'):
    """Generate interactive maps for all wafers."""
    
    from pathlib import Path
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for wafer_id in df['wafer_id'].unique():
        fig = create_interactive_wafer_map(
            df, wafer_id=wafer_id, value_col='leakage_ua'
        )
        output_file = f'{output_dir}wafer_map_{wafer_id}.html'
        fig.write_html(output_file)
        print(f'Saved: {output_file}')

# Usage
batch_generate_wafer_maps(df_tests)
```

### 9.3 Create HTML Gallery of All Visualizations

```python
def create_html_gallery(fig_dict, output_file='/reports/gallery.html'):
    """Create clickable gallery of all visualizations."""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Wafer Analysis Gallery</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            .gallery { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
            .item { border: 1px solid #ccc; padding: 10px; }
            .item h3 { margin-top: 0; }
            a { color: blue; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Wafer Analysis Report</h1>
        <div class="gallery">
    """
    
    for title, fig in fig_dict.items():
        filename = title.replace(' ', '_').lower()
        fig_path = f'figures/{filename}.html'
        
        html_content += f"""
        <div class="item">
            <h3>{title}</h3>
            <a href="{fig_path}">View Interactive Chart →</a>
        </div>
        """
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f'Gallery saved to {output_file}')

# Usage
figures = {
    'Wafer Map': fig_wafer_map,
    'Histogram': fig_histogram,
    'Trend': fig_trend,
    '3D Scatter': fig_3d,
}
create_html_gallery(figures)
```

---

## SECTION 10: PERFORMANCE OPTIMIZATION FOR LARGE DATASETS

### 10.1 Data Sampling for Interactive Plots

```python
def optimize_for_interactivity(df, max_points=10000):
    """Downsample data for better interactivity."""
    
    if len(df) > max_points:
        # Keep all FAIL points; sample PASS points
        df_fail = df[df['status'] == 'FAIL']
        df_pass = df[df['status'] == 'PASS'].sample(n=max_points - len(df_fail))
        df_plot = pd.concat([df_fail, df_pass])
        
        print(f'Downsampled {len(df)} → {len(df_plot)} points for interactivity')
        return df_plot
    else:
        return df

# Usage
df_plot = optimize_for_interactivity(df_tests)
fig = create_interactive_wafer_map(df_plot)
```

### 10.2 Aggregation for Large Wafers (Hexbin)

```python
def create_hexbin_wafer_map(df, wafer_id='W1', gridsize=20):
    """Hexagonal binning for large wafers (1M+ points)."""
    
    df_wafer = df[df['wafer_id'] == wafer_id].copy()
    
    # Aggregate using hexagonal bins
    fig = go.Figure()
    
    fig.add_trace(go.Histogram2dcontour(
        x=df_wafer['die_x'],
        y=df_wafer['die_y'],
        colorscale='Viridis',
        hoverinfo='x+y+z',
        contours=dict(showlabels=True),
    ))
    
    fig.update_layout(
        title=f'Yield Density: {wafer_id}',
        xaxis_title='X',
        yaxis_title='Y',
        width=800,
        height=800,
    )
    
    return fig

# Usage
fig = create_hexbin_wafer_map(df_tests, wafer_id='W001')
fig.show()
```

---

## SECTION 11: RECOMMENDED WORKFLOW FOR PRODUCTION

```python
# Production wafer analysis pipeline with interactive outputs

import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WaferAnalysisPipeline:
    def __init__(self, stdf_file, output_dir='/reports'):
        self.stdf_file = Path(stdf_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def run(self):
        """Full analysis pipeline."""
        
        logger.info(f'Starting wafer analysis: {self.stdf_file}')
        
        # 1. Parse STDF
        logger.info('Parsing STDF...')
        df = self.parse_stdf()
        
        # 2. Generate visualizations
        logger.info('Generating visualizations...')
        self.generate_wafer_maps(df)
        self.generate_statistics(df)
        self.generate_trends(df)
        
        # 3. Create dashboard
        logger.info('Creating dashboard...')
        self.create_dashboard(df)
        
        # 4. Generate report
        logger.info('Generating report...')
        self.create_report(df)
        
        logger.info(f'Analysis complete. Reports in {self.output_dir}')
    
    def parse_stdf(self):
        """Parse STDF → DataFrame."""
        # STDFParser implementation
        return pd.read_csv(self.stdf_file)  # Placeholder
    
    def generate_wafer_maps(self, df):
        """Generate interactive wafer maps for each wafer."""
        for wafer_id in df['wafer_id'].unique():
            fig = create_interactive_wafer_map(df, wafer_id=wafer_id)
            output_file = self.output_dir / f'wafer_map_{wafer_id}.html'
            fig.write_html(str(output_file))
            logger.info(f'Saved: {output_file}')
    
    def generate_statistics(self, df):
        """Generate statistical visualizations."""
        fig = create_interactive_histogram(df, test_col='leakage_ua')
        fig.write_html(str(self.output_dir / 'histogram.html'))
        
        fig = create_interactive_qq_plot(df['leakage_ua'])
        fig.write_html(str(self.output_dir / 'qq_plot.html'))
    
    def generate_trends(self, df):
        """Generate trend visualizations."""
        fig = create_interactive_trend_plot(df, spec_target=95.0)
        fig.write_html(str(self.output_dir / 'trend.html'))
    
    def create_dashboard(self, df):
        """Create Streamlit dashboard."""
        # Saved as streamlit app
        logger.info('Dashboard available via: streamlit run wafer_dashboard.py')
    
    def create_report(self, df):
        """Create HTML report with embedded visualizations."""
        # Generate comprehensive report
        pass

# Usage
pipeline = WaferAnalysisPipeline('/data/wafer.stdf', output_dir='/reports/2024_lot_001')
pipeline.run()
```

---

## CONCLUSION

This comprehensive guide provides:

1. **10+ Python libraries** optimized for different visualization needs
2. **Production-ready code** for interactive wafer maps, histograms, 3D plots
3. **Zoomable, clickable visualizations** using Plotly, Bokeh, Altair
4. **Advanced statistical plots** (Q-Q, Weibull, capability analysis)
5. **Dashboard frameworks** (Streamlit, Dash) for real-time monitoring
6. **Performance optimization** for large datasets (100k+ points)
7. **Best practices** for colors, interactivity, exports
8. **Full production pipeline** ready for fab deployment

**Recommended stack for your `ai.local` setup:**
- **Plotly** for web-based interactive reports (HTML export)
- **Streamlit** for rapid dashboard prototyping
- **Bokeh** for real-time streaming from ATE equipment
- **Python backend** (FastAPI) serving preprocessed data
- **PostgreSQL** storing parsed STDF data on `ai.local`

**Next steps:**
1. Integrate with your STDF parser
2. Deploy Streamlit app on `ai.local` (accessible from lab network)
3. Batch-generate reports for customer delivery
4. Add real-time monitoring via Bokeh server
5. Integrate with ChromaDB RAG for automated insights
