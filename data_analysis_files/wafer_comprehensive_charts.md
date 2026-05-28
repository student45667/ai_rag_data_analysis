# Wafer Analysis: Comprehensive Interactive Charts & Visualizations Guide

---

## SECTION 1: BEE SWARM PLOTS (Point Cloud Visualization)

### 1.1 Basic Bee Swarm Plot (Plotly)

**Purpose:** Show individual data points without overlap; ideal for visualizing each die's measurement.

```python
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_bee_swarm_plot(df, y_col='leakage_ua', x_col='wafer_id', 
                           color_col='status', title='Bee Swarm: Test Results'):
    """
    Bee swarm plot showing individual die measurements.
    
    Features:
    - Each point = one die
    - Jittered x-position to avoid overlap
    - Color by status or parameter
    - Hover shows die details
    """
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        hover_data=['die_x', 'die_y', 'retest_count'],
        title=title,
        labels={y_col: y_col, x_col: x_col},
    )
    
    # Add jitter to x-axis to reduce overlap
    fig.update_traces(
        marker=dict(
            size=6,
            opacity=0.6,
            line=dict(width=0.5, color='white'),
        ),
        jitter=0.4,  # Horizontal jitter
    )
    
    # Add mean line per wafer
    means = df.groupby(x_col)[y_col].mean()
    fig.add_trace(go.Scatter(
        x=means.index,
        y=means.values,
        mode='markers',
        marker=dict(size=12, color='red', symbol='line', line=dict(width=3)),
        name='Mean',
        hovertemplate='<b>Mean: %{y:.3f}</b><extra></extra>',
    ))
    
    fig.update_layout(
        width=1200,
        height=600,
        template='plotly_white',
        hovermode='closest',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    )
    
    return fig

# Usage
fig = create_bee_swarm_plot(
    df_tests,
    y_col='leakage_ua',
    x_col='wafer_id',
    color_col='status',
    title='Leakage Measurements: Bee Swarm Plot'
)
fig.show()
fig.write_html('/reports/bee_swarm_basic.html')
```

### 1.2 Advanced Bee Swarm with Size Mapping

```python
def create_advanced_bee_swarm(df, y_col='leakage_ua', x_col='wafer_id',
                               color_col='status', size_col='fmax_mhz',
                               title='Advanced Bee Swarm: Size by Speed'):
    """
    Bee swarm with additional dimension via point size.
    
    Size represents another parameter (e.g., Fmax speed).
    """
    
    # Normalize size for visibility
    size_min, size_max = df[size_col].min(), df[size_col].max()
    df['normalized_size'] = 5 + (df[size_col] - size_min) / (size_max - size_min) * 10
    
    fig = go.Figure()
    
    # Separate PASS and FAIL for better visualization
    for status in df[color_col].unique():
        df_status = df[df[color_col] == status]
        
        fig.add_trace(go.Scatter(
            x=df_status[x_col],
            y=df_status[y_col],
            mode='markers',
            name=status,
            marker=dict(
                size=df_status['normalized_size'],
                color='green' if status == 'PASS' else 'red',
                opacity=0.6,
                line=dict(width=0.5, color='white'),
            ),
            text=[
                f"<b>{status}</b><br>"
                f"Leakage: {row[y_col]:.3f}<br>"
                f"Fmax: {row[size_col]:.0f} MHz<br>"
                f"Die: ({row['die_x']}, {row['die_y']})"
                for _, row in df_status.iterrows()
            ],
            hovertemplate='%{text}<extra></extra>',
            jitter=0.3,
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        width=1200,
        height=650,
        template='plotly_white',
        hovermode='closest',
        showlegend=True,
    )
    
    return fig

# Usage
fig = create_advanced_bee_swarm(
    df_tests,
    y_col='leakage_ua',
    x_col='wafer_id',
    color_col='status',
    size_col='fmax_mhz'
)
fig.show()
```

### 1.3 Bee Swarm with Distribution Statistics Overlay

```python
def create_bee_swarm_with_stats(df, y_col='leakage_ua', x_col='wafer_id',
                                 title='Bee Swarm + Statistics'):
    """
    Bee swarm with overlaid box plot and violin plot outlines.
    """
    
    fig = go.Figure()
    
    wafers = sorted(df[x_col].unique())
    x_positions = np.arange(len(wafers))
    
    # 1. Violin plot (background distribution)
    for i, wafer in enumerate(wafers):
        wafer_data = df[df[x_col] == wafer][y_col].dropna()
        
        fig.add_trace(go.Violin(
            y=wafer_data,
            x=[wafer] * len(wafer_data),
            name=f'{wafer} Distribution',
            side='negative',
            line_color='blue',
            fillcolor='blue',
            opacity=0.2,
            meanline_visible=True,
            points=False,  # Don't show individual points in violin
            hoverinfo='skip',
        ))
    
    # 2. Bee swarm (individual points)
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='markers',
        name='Individual Measurements',
        marker=dict(
            size=6,
            color=df['status'].map({'PASS': 0, 'FAIL': 1}),
            colorscale='RdYlGn_r',
            opacity=0.7,
            line=dict(width=0.5, color='white'),
        ),
        text=[
            f"Status: {row['status']}<br>"
            f"Value: {row[y_col]:.3f}<br>"
            f"Position: ({row['die_x']}, {row['die_y']})"
            for _, row in df.iterrows()
        ],
        hovertemplate='%{text}<extra></extra>',
        jitter=0.3,
    ))
    
    # 3. Box plot overlay (quartiles)
    for wafer in wafers:
        wafer_data = df[df[x_col] == wafer][y_col].dropna()
        
        q1 = wafer_data.quantile(0.25)
        q3 = wafer_data.quantile(0.75)
        median = wafer_data.median()
        
        fig.add_trace(go.Box(
            y=wafer_data,
            x=[wafer],
            name=f'{wafer} Box',
            side='positive',
            line_color='red',
            fillcolor='rgba(255,0,0,0)',  # Transparent fill
            showlegend=False,
            boxmean=True,
            hoverinfo='y',
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        width=1200,
        height=700,
        template='plotly_white',
        hovermode='closest',
        violinmode='group',
    )
    
    return fig

# Usage
fig = create_bee_swarm_with_stats(df_tests, y_col='leakage_ua', x_col='wafer_id')
fig.show()
fig.write_html('/reports/bee_swarm_with_stats.html')
```

---

## SECTION 2: BOX PLOTS (Quartile Analysis)

### 2.1 Interactive Box Plot with Statistical Annotations

```python
def create_interactive_box_plot(df, y_col='leakage_ua', x_col='wafer_id',
                                 lsl=None, usl=None,
                                 title='Box Plot with Spec Limits'):
    """
    Interactive box plot showing quartiles, whiskers, outliers.
    
    Features:
    - Box: Q1-Q3 (interquartile range)
    - Line in box: Median (Q2)
    - Whiskers: Typically 1.5 × IQR
    - Points: Outliers
    - Spec limits overlay
    """
    
    fig = go.Figure()
    
    wafers = sorted(df[x_col].unique())
    
    for wafer in wafers:
        wafer_data = df[df[x_col] == wafer][y_col].dropna()
        
        # Calculate statistics
        q1 = wafer_data.quantile(0.25)
        q2 = wafer_data.quantile(0.50)  # Median
        q3 = wafer_data.quantile(0.75)
        iqr = q3 - q1
        
        # Whisker limits (1.5 × IQR)
        whisker_low = q1 - 1.5 * iqr
        whisker_high = q3 + 1.5 * iqr
        
        # Find outliers
        outliers = wafer_data[(wafer_data < whisker_low) | (wafer_data > whisker_high)]
        
        # Add box plot
        fig.add_trace(go.Box(
            y=wafer_data,
            name=wafer,
            x=[wafer] * len(wafer_data),
            boxmean='sd',  # Show mean and std dev
            marker=dict(opacity=0.5),
            line=dict(width=2),
            hovertemplate=(
                '<b>%{x}</b><br>'
                'Value: %{y:.3f}<br>'
                '<extra></extra>'
            ),
        ))
        
        # Annotate with statistics
        stats_text = (
            f'<b>{wafer}</b><br>'
            f'Q1: {q1:.3f}<br>'
            f'Median: {q2:.3f}<br>'
            f'Q3: {q3:.3f}<br>'
            f'IQR: {iqr:.3f}<br>'
            f'Outliers: {len(outliers)}'
        )
        
        fig.add_annotation(
            text=stats_text,
            x=wafer,
            y=wafer_data.max(),
            showarrow=True,
            arrowhead=2,
            ax=-40,
            ay=-40,
            bgcolor='rgba(255,255,200,0.8)',
            bordercolor='black',
            borderwidth=1,
            font=dict(size=9),
        )
    
    # Add spec limits
    if lsl:
        fig.add_hline(
            y=lsl,
            line_dash='dash',
            line_color='orange',
            line_width=2,
            annotation_text=f'LSL: {lsl}',
            annotation_position='right',
        )
    
    if usl:
        fig.add_hline(
            y=usl,
            line_dash='dash',
            line_color='purple',
            line_width=2,
            annotation_text=f'USL: {usl}',
            annotation_position='right',
        )
    
    # Shade spec region
    if lsl and usl:
        fig.add_hrect(
            y0=lsl, y1=usl,
            fillcolor='green', opacity=0.05,
            layer='below',
            name='In-Spec Region',
        )
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        width=1400,
        height=700,
        template='plotly_white',
        hovermode='closest',
        showlegend=False,
    )
    
    return fig

# Usage
fig = create_interactive_box_plot(
    df_tests,
    y_col='leakage_ua',
    x_col='wafer_id',
    lsl=0.1,
    usl=5.0,
    title='Leakage: Box Plot with Spec Limits'
)
fig.show()
fig.write_html('/reports/box_plot_interactive.html')
```

### 2.2 Multi-Parameter Box Plot Comparison

```python
def create_multiparameter_box_plot(df, parameters=['leakage_ua', 'fmax_mhz', 'iddq_active_ma'],
                                    x_col='wafer_id',
                                    title='Multi-Parameter Box Plot Comparison'):
    """
    Compare multiple test parameters in box plots.
    Each parameter gets its own y-scale.
    """
    
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1,
        cols=len(parameters),
        subplot_titles=parameters,
        specs=[[{'secondary_y': False} for _ in parameters]],
    )
    
    for col_idx, param in enumerate(parameters, 1):
        for wafer in sorted(df[x_col].unique()):
            wafer_data = df[df[x_col] == wafer][param].dropna()
            
            fig.add_trace(
                go.Box(
                    y=wafer_data,
                    name=wafer,
                    x=[wafer] * len(wafer_data),
                    showlegend=(col_idx == 1),  # Legend only on first subplot
                ),
                row=1,
                col=col_idx,
            )
        
        fig.update_yaxes(title_text=param, row=1, col=col_idx)
    
    fig.update_layout(
        title_text=title,
        width=1600,
        height=600,
        template='plotly_white',
        hovermode='closest',
    )
    
    return fig

# Usage
fig = create_multiparameter_box_plot(
    df_tests,
    parameters=['leakage_ua', 'fmax_mhz', 'iddq_active_ma']
)
fig.show()
```

---

## SECTION 3: STANDARD DEVIATION & OUTLIER VISUALIZATION

### 3.1 Standard Deviation Bands with Outlier Detection

```python
def create_std_dev_plot(df, y_col='leakage_ua', x_col='wafer_id',
                         title='Standard Deviation Bands with Outliers'):
    """
    Plot mean ± 1σ, 2σ, 3σ bands.
    Highlight outliers beyond 3σ.
    """
    
    fig = go.Figure()
    
    wafers = sorted(df[x_col].unique())
    x_positions = np.arange(len(wafers))
    
    means = []
    stds = []
    all_outliers_x = []
    all_outliers_y = []
    
    for wafer in wafers:
        wafer_data = df[df[x_col] == wafer][y_col].dropna()
        mean = wafer_data.mean()
        std = wafer_data.std()
        
        means.append(mean)
        stds.append(std)
        
        # Identify outliers (> 3σ from mean)
        outliers = wafer_data[np.abs(wafer_data - mean) > 3 * std]
        all_outliers_x.extend([wafer] * len(outliers))
        all_outliers_y.extend(outliers.values)
    
    means = np.array(means)
    stds = np.array(stds)
    
    # Plot bands (3σ → 2σ → 1σ)
    
    # ±3σ band (lightest)
    fig.add_trace(go.Scatter(
        x=wafers + wafers[::-1],
        y=list(means + 3*stds) + list((means - 3*stds)[::-1]),
        fill='toself',
        fillcolor='rgba(255,0,0,0.05)',
        line=dict(color='rgba(255,0,0,0)'),
        name='±3σ Band',
        hoverinfo='skip',
    ))
    
    # ±2σ band
    fig.add_trace(go.Scatter(
        x=wafers + wafers[::-1],
        y=list(means + 2*stds) + list((means - 2*stds)[::-1]),
        fill='toself',
        fillcolor='rgba(255,165,0,0.1)',
        line=dict(color='rgba(255,165,0,0)'),
        name='±2σ Band',
        hoverinfo='skip',
    ))
    
    # ±1σ band (darkest)
    fig.add_trace(go.Scatter(
        x=wafers + wafers[::-1],
        y=list(means + stds) + list((means - stds)[::-1]),
        fill='toself',
        fillcolor='rgba(0,100,0,0.15)',
        line=dict(color='rgba(0,100,0,0)'),
        name='±1σ Band',
        hoverinfo='skip',
    ))
    
    # Mean line
    fig.add_trace(go.Scatter(
        x=wafers,
        y=means,
        mode='lines+markers',
        name='Mean',
        line=dict(color='blue', width=2),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Mean: %{y:.3f}<extra></extra>',
    ))
    
    # ±1σ markers
    fig.add_trace(go.Scatter(
        x=wafers,
        y=means + stds,
        mode='markers',
        name='±1σ',
        marker=dict(size=4, color='green', symbol='line', line=dict(width=1)),
        hovertemplate='Mean+1σ: %{y:.3f}<extra></extra>',
    ))
    
    fig.add_trace(go.Scatter(
        x=wafers,
        y=means - stds,
        mode='markers',
        name='−1σ',
        marker=dict(size=4, color='green', symbol='line', line=dict(width=1)),
        hovertemplate='Mean-1σ: %{y:.3f}<extra></extra>',
    ))
    
    # Outliers (points > 3σ)
    if all_outliers_x:
        fig.add_trace(go.Scatter(
            x=all_outliers_x,
            y=all_outliers_y,
            mode='markers',
            name='Outliers (>3σ)',
            marker=dict(
                size=10,
                color='red',
                symbol='x',
                line=dict(width=2),
            ),
            hovertemplate='<b>OUTLIER</b><br>%{x}<br>%{y:.3f}<extra></extra>',
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        width=1200,
        height=600,
        template='plotly_white',
        hovermode='closest',
        showlegend=True,
    )
    
    return fig

# Usage
fig = create_std_dev_plot(df_tests, y_col='leakage_ua', x_col='wafer_id')
fig.show()
fig.write_html('/reports/std_dev_outliers.html')
```

### 3.2 Outlier Detection with Z-Score & IQR Methods

```python
def detect_and_visualize_outliers(df, y_col='leakage_ua', x_col='wafer_id',
                                   method='zscore',  # 'zscore' or 'iqr'
                                   threshold=3):
    """
    Detect outliers using Z-score or IQR method.
    Visualize with color coding.
    
    method='zscore': Points > threshold × σ from mean
    method='iqr': Points > 1.5 × IQR from Q1/Q3
    """
    
    df_plot = df.copy()
    
    if method == 'zscore':
        # Z-score: how many standard deviations from mean?
        df_plot['z_score'] = np.abs((df_plot[y_col] - df_plot[y_col].mean()) / df_plot[y_col].std())
        df_plot['is_outlier'] = df_plot['z_score'] > threshold
        outlier_label = f'Z-Score > {threshold}'
        
    elif method == 'iqr':
        # IQR method
        q1 = df_plot[y_col].quantile(0.25)
        q3 = df_plot[y_col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        df_plot['is_outlier'] = (df_plot[y_col] < lower_bound) | (df_plot[y_col] > upper_bound)
        outlier_label = f'IQR Method (1.5 × IQR)'
    
    # Separate normal and outlier points
    df_normal = df_plot[~df_plot['is_outlier']]
    df_outliers = df_plot[df_plot['is_outlier']]
    
    fig = go.Figure()
    
    # Normal points
    fig.add_trace(go.Scatter(
        x=df_normal[x_col],
        y=df_normal[y_col],
        mode='markers',
        name='Normal',
        marker=dict(
            size=6,
            color='blue',
            opacity=0.6,
            line=dict(width=0.5, color='white'),
        ),
        hovertemplate='<b>Normal</b><br>%{x}<br>%{y:.3f}<extra></extra>',
        jitter=0.3,
    ))
    
    # Outlier points (larger, red)
    fig.add_trace(go.Scatter(
        x=df_outliers[x_col],
        y=df_outliers[y_col],
        mode='markers',
        name=outlier_label,
        marker=dict(
            size=12,
            color='red',
            symbol='star',
            line=dict(width=2, color='darkred'),
        ),
        text=[
            f"<b>OUTLIER</b><br>"
            f"Wafer: {row[x_col]}<br>"
            f"Value: {row[y_col]:.3f}<br>"
            f"Die: ({row['die_x']}, {row['die_y']})"
            for _, row in df_outliers.iterrows()
        ],
        hovertemplate='%{text}<extra></extra>',
        jitter=0.3,
    ))
    
    # Add statistics annotation
    outlier_pct = len(df_outliers) / len(df_plot) * 100
    
    fig.add_annotation(
        text=(
            f"<b>Outlier Statistics</b><br>"
            f"Method: {method.upper()}<br>"
            f"Outliers Found: {len(df_outliers)}<br>"
            f"Percentage: {outlier_pct:.2f}%<br>"
            f"Total Points: {len(df_plot)}"
        ),
        xref='paper', yref='paper',
        x=0.02, y=0.98,
        xanchor='left', yanchor='top',
        showarrow=False,
        bgcolor='rgba(255,255,200,0.9)',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=11, family='monospace'),
    )
    
    fig.update_layout(
        title=f'Outlier Detection: {method.upper()} Method',
        xaxis_title=x_col,
        yaxis_title=y_col,
        width=1200,
        height=600,
        template='plotly_white',
        hovermode='closest',
    )
    
    return fig, df_plot

# Usage
fig, df_with_outliers = detect_and_visualize_outliers(
    df_tests,
    y_col='leakage_ua',
    method='zscore',
    threshold=3
)
fig.show()
fig.write_html('/reports/outlier_detection.html')
```

---

## SECTION 4: HISTOGRAM WITH DATA DENSITY OVERLAY

### 4.1 Advanced Histogram with KDE Density

```python
def create_histogram_with_density(df, param_col='leakage_ua', 
                                   group_col='wafer_id',
                                   bins=40,
                                   title='Histogram with Density Overlay'):
    """
    Histogram with kernel density estimation (KDE) overlay.
    
    Features:
    - Multiple histograms (one per wafer)
    - Smooth density curve overlay
    - Overlaid for easy comparison
    """
    
    fig = go.Figure()
    
    wafers = sorted(df[group_col].unique())
    colors = px.colors.qualitative.Set2
    
    for idx, wafer in enumerate(wafers):
        wafer_data = df[df[group_col] == wafer][param_col].dropna()
        
        # Histogram
        fig.add_trace(go.Histogram(
            x=wafer_data,
            name=f'{wafer} (n={len(wafer_data)})',
            nbinsx=bins,
            opacity=0.5,
            marker=dict(color=colors[idx % len(colors)]),
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
        ))
        
        # KDE Density curve
        from scipy.stats import gaussian_kde
        
        kde = gaussian_kde(wafer_data)
        x_range = np.linspace(wafer_data.min(), wafer_data.max(), 200)
        density = kde(x_range)
        
        # Scale density to match histogram height
        hist_max = len(wafer_data) / bins * 1.5
        density_scaled = density * len(wafer_data) / density.max() * 0.8
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=density_scaled,
            mode='lines',
            name=f'{wafer} (KDE)',
            line=dict(color=colors[idx % len(colors)], width=3),
            hovertemplate='Density: %{y:.3f}<extra></extra>',
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=param_col,
        yaxis_title='Frequency',
        barmode='overlay',
        width=1200,
        height=600,
        template='plotly_white',
        hovermode='x unified',
    )
    
    return fig

# Usage
fig = create_histogram_with_density(
    df_tests,
    param_col='leakage_ua',
    group_col='wafer_id',
    title='Leakage Distribution: Histogram + KDE'
)
fig.show()
fig.write_html('/reports/histogram_density.html')
```

### 4.2 Stacked Histogram (Pass vs Fail)

```python
def create_stacked_histogram(df, param_col='leakage_ua', 
                              title='Stacked Histogram: Pass vs Fail'):
    """
    Stacked histogram separating PASS and FAIL distributions.
    Useful for identifying pass/fail boundaries.
    """
    
    df_pass = df[df['status'] == 'PASS'][param_col].dropna()
    df_fail = df[df['status'] == 'FAIL'][param_col].dropna()
    
    fig = go.Figure()
    
    # PASS histogram (bottom)
    fig.add_trace(go.Histogram(
        x=df_pass,
        name='PASS',
        nbinsx=40,
        marker=dict(color='green'),
        opacity=0.7,
        hovertemplate='<b>PASS</b><br>Range: %{x}<br>Count: %{y}<extra></extra>',
    ))
    
    # FAIL histogram (top)
    fig.add_trace(go.Histogram(
        x=df_fail,
        name='FAIL',
        nbinsx=40,
        marker=dict(color='red'),
        opacity=0.7,
        hovertemplate='<b>FAIL</b><br>Range: %{x}<br>Count: %{y}<extra></extra>',
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=param_col,
        yaxis_title='Count',
        barmode='stack',
        width=1200,
        height=600,
        template='plotly_white',
        hovermode='x unified',
    )
    
    return fig

# Usage
fig = create_stacked_histogram(df_tests, param_col='leakage_ua')
fig.show()
fig.write_html('/reports/stacked_histogram.html')
```

### 4.3 2D Histogram (Parameter Correlations)

```python
def create_2d_histogram(df, x_param='leakage_ua', y_param='fmax_mhz',
                         title='2D Histogram: Parameter Correlation Density'):
    """
    2D histogram showing density of parameter combinations.
    Useful for identifying parameter correlations and clusters.
    """
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram2d(
        x=df[x_param],
        y=df[y_param],
        colorscale='Viridis',
        nbinsx=30,
        nbinsy=30,
        colorbar=dict(title='Count'),
        hovertemplate='%{x}<br>%{y}<br>Count: %{z}<extra></extra>',
    ))
    
    # Add contour overlay for better visualization
    fig.add_trace(go.Histogram2dContour(
        x=df[x_param],
        y=df[y_param],
        contours=dict(showlabels=True),
        line=dict(width=0),
        hoverinfo='skip',
        showscale=False,
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_param,
        yaxis_title=y_param,
        width=900,
        height=800,
        template='plotly_white',
        hovermode='closest',
    )
    
    return fig

# Usage
fig = create_2d_histogram(
    df_tests,
    x_param='leakage_ua',
    y_param='fmax_mhz',
    title='Leakage vs Speed: 2D Histogram'
)
fig.show()
fig.write_html('/reports/histogram_2d.html')
```

---

## SECTION 5: HEATMAPS (X-COORD vs Y-COORD)

### 5.1 Parametric Heatmap (Die-by-Die Value Map)

```python
def create_parametric_heatmap(df, wafer_id='W1', value_col='leakage_ua',
                               title='Parametric Heatmap: Wafer Surface'):
    """
    Heatmap showing parameter values across wafer (X, Y coordinates).
    Each cell = one die, color = parameter value.
    """
    
    df_wafer = df[df['wafer_id'] == wafer_id].copy()
    
    # Pivot to create matrix (X columns, Y rows)
    heatmap_data = df_wafer.pivot_table(
        index='die_y',
        columns='die_x',
        values=value_col,
        aggfunc='mean'  # If multiple measurements per die
    )
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis',
        colorbar=dict(title=value_col),
        hovertemplate='X: %{x}<br>Y: %{y}<br>' + value_col + ': %{z:.3f}<extra></extra>',
    ))
    
    fig.update_layout(
        title=f'{title} - {wafer_id}',
        xaxis_title='Die X Position',
        yaxis_title='Die Y Position',
        width=900,
        height=800,
        template='plotly_white',
    )
    
    return fig

# Usage
fig = create_parametric_heatmap(
    df_tests,
    wafer_id='W001',
    value_col='leakage_ua',
    title='Leakage Distribution Heatmap'
)
fig.show()
fig.write_html('/reports/heatmap_parametric.html')
```

### 5.2 Pass/Fail Heatmap (Yield Map)

```python
def create_passfail_heatmap(df, wafer_id='W1', bin_size=5,
                             title='Pass/Fail Heatmap: Binned Yield'):
    """
    Heatmap showing yield percentage in spatial bins.
    Useful for identifying yield loss regions.
    """
    
    df_wafer = df[df['wafer_id'] == wafer_id].copy()
    
    # Create spatial bins
    df_wafer['x_bin'] = pd.cut(df_wafer['die_x'], bins=bin_size)
    df_wafer['y_bin'] = pd.cut(df_wafer['die_y'], bins=bin_size)
    
    # Calculate yield per bin
    yield_map = df_wafer.groupby(['y_bin', 'x_bin']).apply(
        lambda g: (g['status'] == 'PASS').sum() / len(g) * 100
    ).unstack()
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=yield_map.values,
        colorscale='RdYlGn',
        vmin=0,
        vmax=100,
        colorbar=dict(title='Yield (%)'),
        hovertemplate='Yield: %{z:.1f}%<extra></extra>',
    ))
    
    fig.update_layout(
        title=f'{title} - {wafer_id}',
        xaxis_title='X Bins',
        yaxis_title='Y Bins',
        width=800,
        height=800,
        template='plotly_white',
    )
    
    return fig

# Usage
fig = create_passfail_heatmap(
    df_tests,
    wafer_id='W001',
    bin_size=8,
    title='Spatial Yield Distribution'
)
fig.show()
fig.write_html('/reports/heatmap_yield.html')
```

### 5.3 Test Count Heatmap (Which Tests Fail Most?)

```python
def create_test_failure_heatmap(df, wafer_id='W1',
                                 title='Test Failure Heatmap by Position'):
    """
    Heatmap showing which die positions fail most tests.
    """
    
    df_wafer = df[df['wafer_id'] == wafer_id][df['status'] == 'FAIL'].copy()
    
    # Count failures per position
    failure_map = df_wafer.groupby(['die_y', 'die_x']).size().unstack(fill_value=0)
    
    fig = go.Figure(data=go.Heatmap(
        z=failure_map.values,
        colorscale='Reds',
        colorbar=dict(title='Failure Count'),
        hovertemplate='X: %{x}<br>Y: %{y}<br>Failures: %{z}<extra></extra>',
    ))
    
    fig.update_layout(
        title=f'{title} - {wafer_id}',
        xaxis_title='Die X Position',
        yaxis_title='Die Y Position',
        width=900,
        height=800,
        template='plotly_white',
    )
    
    return fig

# Usage
fig = create_test_failure_heatmap(
    df_tests,
    wafer_id='W001',
    title='Test Failure Locations'
)
fig.show()
fig.write_html('/reports/heatmap_test_failures.html')
```

---

## SECTION 6: CORRELATION ANALYSIS

### 6.1 Interactive Correlation Matrix Heatmap

```python
def create_correlation_heatmap(df, numeric_cols=None,
                                title='Parameter Correlation Matrix'):
    """
    Correlation matrix showing relationships between test parameters.
    """
    
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Calculate correlation
    corr_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        zmid=0,
        zmin=-1,
        zmax=1,
        colorbar=dict(title='Correlation'),
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont=dict(size=10),
        hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.3f}<extra></extra>',
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Parameter',
        yaxis_title='Parameter',
        width=1000,
        height=900,
        template='plotly_white',
    )
    
    return fig

# Usage
fig = create_correlation_heatmap(
    df_tests,
    numeric_cols=['leakage_ua', 'fmax_mhz', 'iddq_active_ma', 'delay_ns'],
    title='Test Parameter Correlations'
)
fig.show()
fig.write_html('/reports/correlation_matrix.html')
```

### 6.2 Scatter Plot Matrix (Pairplot) - Interactive

```python
def create_scatter_matrix(df, parameters=['leakage_ua', 'fmax_mhz', 'iddq_active_ma'],
                          color_col='status',
                          title='Parameter Scatter Matrix'):
    """
    Pairplot showing relationships between all parameter pairs.
    Diagonal shows distributions.
    """
    
    from plotly.subplots import make_subplots
    
    n_params = len(parameters)
    
    fig = make_subplots(
        rows=n_params,
        cols=n_params,
        vertical_spacing=0.05,
        horizontal_spacing=0.05,
        specs=[[{} for _ in range(n_params)] for _ in range(n_params)],
    )
    
    color_map = {'PASS': 0, 'FAIL': 1}
    colors = df[color_col].map(color_map)
    
    for row, param_y in enumerate(parameters, 1):
        for col, param_x in enumerate(parameters, 1):
            
            if row == col:
                # Diagonal: histogram
                fig.add_trace(
                    go.Histogram(
                        x=df[param_x],
                        nbinsx=20,
                        marker=dict(color='blue'),
                        showlegend=False,
                        hovertemplate='%{x}<br>Count: %{y}<extra></extra>',
                    ),
                    row=row,
                    col=col,
                )
            else:
                # Off-diagonal: scatter
                fig.add_trace(
                    go.Scatter(
                        x=df[param_x],
                        y=df[param_y],
                        mode='markers',
                        marker=dict(
                            color=colors,
                            colorscale='RdYlGn_r',
                            size=4,
                            opacity=0.5,
                        ),
                        showlegend=False,
                        hovertemplate=f'{param_x}: %{{x:.3f}}<br>{param_y}: %{{y:.3f}}<extra></extra>',
                    ),
                    row=row,
                    col=col,
                )
            
            # Update axes labels
            if col == 1:
                fig.update_yaxes(title_text=param_y, row=row, col=col)
            if row == n_params:
                fig.update_xaxes(title_text=param_x, row=row, col=col)
    
    fig.update_layout(
        title_text=title,
        showlegend=False,
        width=1200,
        height=1200,
        template='plotly_white',
    )
    
    return fig

# Usage
fig = create_scatter_matrix(
    df_tests,
    parameters=['leakage_ua', 'fmax_mhz', 'iddq_active_ma'],
    color_col='status'
)
fig.show()
fig.write_html('/reports/scatter_matrix.html')
```

### 6.3 Correlation Network (Chord Diagram Alternative)

```python
def create_correlation_network(df, numeric_cols=None, threshold=0.5):
    """
    Visualize strong correlations as connections.
    Each parameter is a node; edges show correlation strength.
    """
    
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Calculate correlation
    corr_matrix = df[numeric_cols].corr()
    
    # Extract strong correlations (above threshold)
    edges_x = []
    edges_y = []
    edge_colors = []
    
    for i, col1 in enumerate(numeric_cols):
        for j, col2 in enumerate(numeric_cols):
            if i < j:  # Avoid duplicates
                corr_val = corr_matrix.loc[col1, col2]
                if abs(corr_val) > threshold:
                    # For simplicity, arrange in circle
                    angle1 = 2 * np.pi * i / len(numeric_cols)
                    angle2 = 2 * np.pi * j / len(numeric_cols)
                    
                    edges_x.extend([np.cos(angle1), np.cos(angle2), None])
                    edges_y.extend([np.sin(angle1), np.sin(angle2), None])
                    
                    edge_colors.append(corr_val)
    
    # Node positions (circle)
    node_x = [np.cos(2 * np.pi * i / len(numeric_cols)) for i in range(len(numeric_cols))]
    node_y = [np.sin(2 * np.pi * i / len(numeric_cols)) for i in range(len(numeric_cols))]
    
    fig = go.Figure()
    
    # Edges
    fig.add_trace(go.Scatter(
        x=edges_x, y=edges_y,
        mode='lines',
        line=dict(width=0.5, color='gray'),
        hoverinfo='none',
        showlegend=False,
    ))
    
    # Nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=numeric_cols,
        textposition='top center',
        marker=dict(
            size=20,
            color='lightblue',
            line=dict(width=2, color='blue'),
        ),
        hovertemplate='%{text}<extra></extra>',
    ))
    
    fig.update_layout(
        title='Parameter Correlation Network',
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=800,
        height=800,
        template='plotly_white',
    )
    
    return fig

# Usage
fig = create_correlation_network(
    df_tests,
    numeric_cols=['leakage_ua', 'fmax_mhz', 'iddq_active_ma'],
    threshold=0.3
)
fig.show()
fig.write_html('/reports/correlation_network.html')
```

---

## SECTION 7: BAR GRAPH - TEST FAILURES & RANKINGS

### 7.1 Test Failure Count & Rate Bar Chart

```python
def create_test_failure_chart(df, top_n=15,
                               title='Top Failing Tests: Count & Rate'):
    """
    Horizontal bar chart ranking tests by failure count and rate.
    """
    
    # Calculate per-test statistics
    test_stats = df.groupby('test_name').agg({
        'status': [
            ('total', 'count'),
            ('pass', lambda x: (x == 'PASS').sum()),
            ('fail', lambda x: (x == 'FAIL').sum()),
        ]
    }).round(2)
    
    test_stats.columns = ['Total', 'Pass', 'Fail']
    test_stats['Fail_Rate_%'] = (test_stats['Fail'] / test_stats['Total'] * 100).round(2)
    test_stats = test_stats.sort_values('Fail', ascending=True).tail(top_n)
    
    fig = go.Figure()
    
    # Fail count (primary bar)
    fig.add_trace(go.Bar(
        y=test_stats.index,
        x=test_stats['Fail'],
        name='Fail Count',
        orientation='h',
        marker=dict(color='red', opacity=0.7),
        hovertemplate='<b>%{y}</b><br>Failures: %{x}<extra></extra>',
    ))
    
    # Overlay with fail rate (secondary y-axis)
    fig.add_trace(go.Scatter(
        y=test_stats.index,
        x=test_stats['Fail_Rate_%'],
        name='Fail Rate (%)',
        mode='markers+lines',
        marker=dict(size=10, color='darkred'),
        line=dict(width=2, color='darkred'),
        yaxis='y1',
        xaxis='x2',
        hovertemplate='<b>%{y}</b><br>Fail Rate: %{x:.1f}%<extra></extra>',
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Failure Count',
        xaxis2_title='Failure Rate (%)',
        yaxis_title='Test Name',
        width=1200,
        height=600,
        template='plotly_white',
        hovermode='closest',
        xaxis2=dict(
            overlaying='x',
            side='top',
        ),
    )
    
    return fig

# Usage
fig = create_test_failure_chart(df_tests, top_n=15)
fig.show()
fig.write_html('/reports/test_failures_bar.html')
```

### 7.2 Stacked Bar Chart (Test Results Composition)

```python
def create_stacked_test_bar_chart(df, param_col='wafer_id',
                                    title='Test Results by Wafer: Pass/Fail Composition'):
    """
    Stacked bar chart showing pass/fail composition for each wafer.
    """
    
    # Count pass/fail per wafer
    test_results = df.groupby([param_col, 'status']).size().unstack(fill_value=0)
    
    fig = go.Figure()
    
    # Add bars for each status
    for status in test_results.columns:
        fig.add_trace(go.Bar(
            x=test_results.index,
            y=test_results[status],
            name=status,
            marker=dict(color='green' if status == 'PASS' else 'red'),
            hovertemplate='<b>%{x}</b><br>' + status + ': %{y}<extra></extra>',
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=param_col,
        yaxis_title='Device Count',
        barmode='stack',
        width=1200,
        height=600,
        template='plotly_white',
        hovermode='x unified',
    )
    
    return fig

# Usage
fig = create_stacked_test_bar_chart(df_tests, param_col='wafer_id')
fig.show()
fig.write_html('/reports/test_composition_stacked.html')
```

### 7.3 Pareto Chart (80/20 Failing Tests)

```python
def create_pareto_chart(df, title='Pareto Chart: Test Failures (80/20 Rule)'):
    """
    Pareto chart showing cumulative failure impact.
    Identifies which 20% of tests cause 80% of failures.
    """
    
    # Count failures per test
    test_failures = df[df['status'] == 'FAIL'].groupby('test_name').size().sort_values(ascending=False)
    
    # Calculate cumulative percentage
    cumulative_pct = (test_failures.cumsum() / test_failures.sum() * 100)
    
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    
    # Bar chart (failure count)
    fig.add_trace(
        go.Bar(
            x=test_failures.index,
            y=test_failures.values,
            name='Failure Count',
            marker=dict(color='red'),
            yaxis='y1',
        ),
        secondary_y=False,
    )
    
    # Line chart (cumulative percentage)
    fig.add_trace(
        go.Scatter(
            x=cumulative_pct.index,
            y=cumulative_pct.values,
            mode='lines+markers',
            name='Cumulative %',
            line=dict(color='blue', width=3),
            marker=dict(size=8),
            yaxis='y2',
        ),
        secondary_y=True,
    )
    
    # Add 80% reference line
    fig.add_hline(
        y=80,
        line_dash='dash',
        line_color='green',
        secondary_y=True,
        annotation_text='80% Threshold',
        annotation_position='right',
    )
    
    fig.update_yaxes(title_text='Failure Count', secondary_y=False)
    fig.update_yaxes(title_text='Cumulative %', secondary_y=True)
    fig.update_xaxes(title_text='Test Name')
    
    fig.update_layout(
        title=title,
        width=1400,
        height=600,
        template='plotly_white',
        hovermode='x unified',
    )
    
    return fig

# Usage
fig = create_pareto_chart(df_tests)
fig.show()
fig.write_html('/reports/pareto_failures.html')
```

---

## SECTION 8: ADDITIONAL STATISTICAL CHARTS

### 8.1 Cumulative Distribution Function (CDF)

```python
def create_cdf_plot(df, param_col='leakage_ua', group_col='wafer_id',
                     lsl=None, usl=None,
                     title='Cumulative Distribution Function'):
    """
    CDF shows percentage of devices below each parameter value.
    Useful for identifying yield loss at spec limits.
    """
    
    fig = go.Figure()
    
    for wafer in sorted(df[group_col].unique()):
        wafer_data = np.sort(df[df[group_col] == wafer][param_col].dropna())
        
        # CDF calculation
        cdf = np.arange(1, len(wafer_data) + 1) / len(wafer_data)
        
        fig.add_trace(go.Scatter(
            x=wafer_data,
            y=cdf * 100,
            mode='lines',
            name=wafer,
            line=dict(width=2),
            hovertemplate=f'{param_col}: %{{x:.3f}}<br>CDF: %{{y:.1f}}%<extra></extra>',
        ))
    
    # Spec limits
    if lsl:
        fig.add_vline(
            x=lsl,
            line_dash='dash',
            line_color='orange',
            annotation_text=f'LSL: {lsl}',
        )
    
    if usl:
        fig.add_vline(
            x=usl,
            line_dash='dash',
            line_color='purple',
            annotation_text=f'USL: {usl}',
        )
    
    fig.update_layout(
        title=title,
        xaxis_title=param_col,
        yaxis_title='Cumulative % (Yield)',
        width=1200,
        height=600,
        template='plotly_white',
        hovermode='x unified',
    )
    
    return fig

# Usage
fig = create_cdf_plot(
    df_tests,
    param_col='leakage_ua',
    group_col='wafer_id',
    lsl=0.1,
    usl=5.0,
    title='Leakage CDF: Yield Analysis'
)
fig.show()
fig.write_html('/reports/cdf_plot.html')
```

### 8.2 Reliability Bathtub Curve (Weibull-like)

```python
def create_reliability_curve(df, fail_col='iddq_active_ma',
                              title='Bathtub Curve: Failure Rate Profile'):
    """
    Reliability curve showing estimated failure rate vs operating time/stress.
    Simplified version using parameter tail analysis.
    """
    
    # Segment data into bins (simulating time progression)
    fail_data = df[fail_col].dropna()
    bins = pd.cut(fail_data, bins=10)
    
    # Count failures in each bin
    bin_stats = df.groupby(pd.cut(fail_col, bins=10)).apply(
        lambda b: {
            'count': len(b),
            'fail_rate': (b['status'] == 'FAIL').sum() / len(b) * 100 if len(b) > 0 else 0,
        }
    )
    
    # Extract for plotting
    bin_labels = [str(i) for i in range(len(bin_stats))]
    fail_rates = [s['fail_rate'] for s in bin_stats.values()]
    
    fig = go.Figure()
    
    # Failure rate curve
    fig.add_trace(go.Scatter(
        x=bin_labels,
        y=fail_rates,
        mode='lines+markers',
        name='Failure Rate',
        line=dict(color='red', width=3),
        marker=dict(size=10),
        fill='tozeroy',
        hovertemplate='Bin: %{x}<br>Fail Rate: %{y:.1f}%<extra></extra>',
    ))
    
    # Reference zones
    fig.add_hrect(
        y0=0, y1=max(fail_rates) * 0.3,
        fillcolor='green', opacity=0.1,
        layer='below',
        annotation_text='Normal Operation',
        annotation_position='top right',
    )
    
    fig.add_hrect(
        y0=max(fail_rates) * 0.7, y1=max(fail_rates),
        fillcolor='red', opacity=0.1,
        layer='below',
        annotation_text='Wear-Out',
        annotation_position='bottom right',
    )
    
    fig.update_layout(
        title=title,
        xaxis_title='Parameter Bin / Operating Condition',
        yaxis_title='Failure Rate (%)',
        width=1200,
        height=600,
        template='plotly_white',
        hovermode='x unified',
    )
    
    return fig

# Usage
fig = create_reliability_curve(df_tests, fail_col='iddq_active_ma')
fig.show()
fig.write_html('/reports/reliability_curve.html')
```

### 8.3 Yield Loss Waterfall Chart

```python
def create_yield_waterfall(df, title='Yield Loss Waterfall: Failure Contribution'):
    """
    Waterfall chart showing cumulative yield loss by test.
    Shows which tests contribute most to total fallout.
    """
    
    # Calculate yield loss per test
    total_dies = len(df)
    
    yield_loss = []
    test_names = []
    
    for test in df['test_name'].unique():
        test_data = df[df['test_name'] == test]
        failures = (test_data['status'] == 'FAIL').sum()
        loss_pct = failures / total_dies * 100
        
        yield_loss.append(loss_pct)
        test_names.append(test)
    
    # Sort by loss
    sorted_indices = np.argsort(yield_loss)[::-1]
    yield_loss = [yield_loss[i] for i in sorted_indices[:10]]  # Top 10
    test_names = [test_names[i] for i in sorted_indices[:10]]
    
    # Calculate cumulative
    cumulative = np.cumsum(yield_loss)
    
    fig = go.Figure(go.Waterfall(
        name='Yield Loss',
        x=test_names,
        y=yield_loss,
        connector=dict(line=dict(color='red')),
        decreasing=dict(marker=dict(color='red')),
        hovertemplate='<b>%{x}</b><br>Loss: %{y:.1f}%<extra></extra>',
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Test Name',
        yaxis_title='Yield Loss (%)',
        width=1200,
        height=600,
        template='plotly_white',
    )
    
    return fig

# Usage
fig = create_yield_waterfall(df_tests)
fig.show()
fig.write_html('/reports/yield_waterfall.html')
```

### 8.4 Parameter Distribution by Bin (Violin + Box)

```python
def create_bin_distribution_comparison(df, param_col='leakage_ua',
                                        bin_col='fmax_mhz', nbins=4,
                                        title='Parameter Distribution by Bin'):
    """
    Compare parameter distributions across speed/power bins.
    """
    
    # Create bins
    df['param_bin'] = pd.qcut(df[bin_col], q=nbins, labels=[f'Bin{i}' for i in range(nbins)])
    
    fig = go.Figure()
    
    for bin_label in sorted(df['param_bin'].unique()):
        bin_data = df[df['param_bin'] == bin_label][param_col].dropna()
        
        # Violin plot
        fig.add_trace(go.Violin(
            y=bin_data,
            name=bin_label,
            side='negative',
            points=False,
            meanline_visible=True,
        ))
        
        # Box plot
        fig.add_trace(go.Box(
            y=bin_data,
            name=f'{bin_label} (stats)',
            side='positive',
            showlegend=False,
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Bin',
        yaxis_title=param_col,
        violinmode='group',
        width=1200,
        height=600,
        template='plotly_white',
    )
    
    return fig

# Usage
fig = create_bin_distribution_comparison(
    df_tests,
    param_col='leakage_ua',
    bin_col='fmax_mhz',
    nbins=4
)
fig.show()
fig.write_html('/reports/bin_distribution.html')
```

---

## SECTION 9: COMPREHENSIVE DASHBOARD COMBINING ALL CHARTS

```python
# dashboard_comprehensive.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title='Wafer Analysis: Comprehensive Dashboard', layout='wide')

st.title('📊 Complete Wafer Sort Analysis Dashboard')

# Sidebar
st.sidebar.header('Controls')
uploaded_file = st.sidebar.file_uploader('Upload CSV', type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Filters
    col1, col2 = st.sidebar.columns(2)
    with col1:
        selected_wafers = st.multiselect('Wafers', df['wafer_id'].unique())
    with col2:
        selected_tests = st.multiselect('Tests', df['test_name'].unique() if 'test_name' in df.columns else [])
    
    # Filter data
    if selected_wafers:
        df = df[df['wafer_id'].isin(selected_wafers)]
    if selected_tests:
        df = df[df['test_name'].isin(selected_tests)]
    
    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric('Total Dies', len(df))
    with col2:
        yield_pct = (df['status'] == 'PASS').sum() / len(df) * 100
        st.metric('Yield', f'{yield_pct:.1f}%')
    with col3:
        st.metric('Wafers', df['wafer_id'].nunique())
    with col4:
        outliers = (np.abs((df['leakage_ua'] - df['leakage_ua'].mean()) / df['leakage_ua'].std()) > 3).sum()
        st.metric('Outliers (>3σ)', outliers)
    with col5:
        fail_count = (df['status'] == 'FAIL').sum()
        st.metric('Total Failures', fail_count)
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        'Swarm & Box',
        'Distributions',
        'Heatmaps',
        'Correlations',
        'Test Failures',
        'Advanced',
        'Statistics'
    ])
    
    with tab1:
        st.subheader('Bee Swarm + Box Plot')
        col1, col2 = st.columns(2)
        
        with col1:
            param1 = st.selectbox('Parameter 1', df.select_dtypes(include=[np.number]).columns)
            fig1 = create_bee_swarm_with_stats(df, y_col=param1)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            param2 = st.selectbox('Parameter 2', df.select_dtypes(include=[np.number]).columns, index=1)
            fig2 = create_interactive_box_plot(df, y_col=param2)
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader('Histograms & Density')
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_histogram_with_density(df, param_col='leakage_ua')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_stacked_histogram(df, param_col='leakage_ua')
            st.plotly_chart(fig, use_container_width=True)
        
        # Std Dev plot
        fig = create_std_dev_plot(df, y_col='leakage_ua')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader('Spatial Heatmaps')
        col1, col2 = st.columns(2)
        
        wafer_select = st.selectbox('Select Wafer', df['wafer_id'].unique())
        
        with col1:
            fig = create_parametric_heatmap(df, wafer_id=wafer_select, value_col='leakage_ua')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_passfail_heatmap(df, wafer_id=wafer_select)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader('Parameter Correlations')
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_correlation_heatmap(df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_2d_histogram(df, x_param='leakage_ua', y_param='fmax_mhz')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.subheader('Test Failures Analysis')
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_test_failure_chart(df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_stacked_test_bar_chart(df)
            st.plotly_chart(fig, use_container_width=True)
        
        # Pareto
        fig = create_pareto_chart(df)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab6:
        st.subheader('Advanced Analysis')
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_cdf_plot(df, param_col='leakage_ua')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig, _ = detect_and_visualize_outliers(df, y_col='leakage_ua', method='zscore')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab7:
        st.subheader('Statistical Summary')
        param_select = st.selectbox('Select Parameter', df.select_dtypes(include=[np.number]).columns)
        
        param_data = df[param_select].dropna()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Mean', f'{param_data.mean():.4f}')
        with col2:
            st.metric('Median', f'{param_data.median():.4f}')
        with col3:
            st.metric('Std Dev', f'{param_data.std():.4f}')
        with col4:
            st.metric('Count', len(param_data))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Min', f'{param_data.min():.4f}')
        with col2:
            st.metric('Max', f'{param_data.max():.4f}')
        with col3:
            st.metric('Range', f'{param_data.max() - param_data.min():.4f}')
        
        # Percentiles
        st.subheader('Percentiles')
        perc_data = {
            'P1': param_data.quantile(0.01),
            'P5': param_data.quantile(0.05),
            'P10': param_data.quantile(0.10),
            'P25': param_data.quantile(0.25),
            'P50': param_data.quantile(0.50),
            'P75': param_data.quantile(0.75),
            'P90': param_data.quantile(0.90),
            'P95': param_data.quantile(0.95),
            'P99': param_data.quantile(0.99),
        }
        
        perc_df = pd.DataFrame(list(perc_data.items()), columns=['Percentile', 'Value'])
        st.dataframe(perc_df, use_container_width=True)

else:
    st.info('👈 Upload a CSV file to begin')
```

Run with: `streamlit run dashboard_comprehensive.py`

---

## SUMMARY TABLE: ALL VISUALIZATION TYPES

| Chart Type | Best For | Interactivity | File Size | Ideal Audience |
|-----------|----------|---------------|-----------|--------------|
| **Bee Swarm** | Individual point distribution | Excellent | Medium | Engineers |
| **Box Plot** | Quartile/outlier summary | Good | Small | Managers |
| **Std Dev Bands** | Process stability | Good | Small | Quality |
| **Histogram + KDE** | Distribution shape | Good | Medium | Analysts |
| **Stacked Histogram** | Pass/Fail composition | Good | Small | Product |
| **2D Histogram** | Parameter correlation density | Good | Medium | Design |
| **Parametric Heatmap** | Spatial patterns | Excellent | Medium | Process |
| **Pass/Fail Heatmap** | Yield loss locations | Excellent | Small | Fab |
| **Correlation Matrix** | Parameter relationships | Excellent | Medium | Design |
| **Scatter Matrix** | Multi-parameter pairs | Excellent | Large | Analysts |
| **Test Failure Bar** | Ranking limiting tests | Good | Small | Engineering |
| **Pareto Chart** | 80/20 failure analysis | Good | Small | Management |
| **CDF Plot** | Yield at spec limits | Good | Medium | Yield |
| **Waterfall Chart** | Cumulative loss | Good | Small | Reporting |

---

## SECTION 10: QUICK START & COMPLETE PYTHON EXAMPLES

### 10.1 Minimal Working Example (MWE)

```python
#!/usr/bin/env python3
"""
Minimal wafer analysis example - run this to generate sample data + charts
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================================================================
# STEP 1: GENERATE SAMPLE WAFER TEST DATA
# ============================================================================

def generate_sample_wafer_data(n_wafers=3, dies_per_wafer=100, n_tests=5):
    """Generate realistic synthetic wafer test data."""
    
    np.random.seed(42)
    data = []
    
    wafer_ids = [f'W{i:03d}' for i in range(n_wafers)]
    test_names = [f'Test_{i}' for i in range(n_tests)]
    
    for wafer_id in wafer_ids:
        for die_idx in range(dies_per_wafer):
            die_x = die_idx % 10
            die_y = die_idx // 10
            
            for test_name in test_names:
                # Simulate realistic measurements
                if test_name == 'Test_0':  # Leakage (µA)
                    value = np.random.lognormal(mean=0.5, sigma=0.3)
                    lsl, usl = 0.1, 5.0
                elif test_name == 'Test_1':  # Fmax (MHz)
                    value = np.random.normal(loc=1000, scale=100)
                    lsl, usl = 500, 1500
                elif test_name == 'Test_2':  # Iddq (mA)
                    value = np.random.gamma(shape=2, scale=5)
                    lsl, usl = 10, 50
                elif test_name == 'Test_3':  # Delay (ns)
                    value = np.random.normal(loc=10, scale=1)
                    lsl, usl = 5, 15
                else:  # Test_4: Power (mW)
                    value = np.random.gamma(shape=3, scale=10)
                    lsl, usl = 20, 100
                
                # Determine pass/fail
                status = 'PASS' if lsl <= value <= usl else 'FAIL'
                
                # Add some correlation (higher leakage → lower speed)
                if test_name == 'Test_0':
                    leakage_val = value
                
                data.append({
                    'wafer_id': wafer_id,
                    'die_x': die_x,
                    'die_y': die_y,
                    'test_name': test_name,
                    'value': value,
                    'status': status,
                    'lsl': lsl,
                    'usl': usl,
                    'leakage_ua': leakage_val if test_name == 'Test_0' else None,
                    'fmax_mhz': value if test_name == 'Test_1' else None,
                    'iddq_active_ma': value if test_name == 'Test_2' else None,
                    'delay_ns': value if test_name == 'Test_3' else None,
                    'power_mw': value if test_name == 'Test_4' else None,
                })
    
    return pd.DataFrame(data)

# Generate data
print("Generating sample wafer test data...")
df = generate_sample_wafer_data(n_wafers=3, dies_per_wafer=100, n_tests=5)
print(f"✓ Generated {len(df)} test records")
print(df.head())

# ============================================================================
# STEP 2: CREATE ALL VISUALIZATIONS
# ============================================================================

# Bee Swarm Plot
print("\n[1/12] Creating Bee Swarm Plot...")
fig_bee = go.Figure()
fig_bee.add_trace(go.Scatter(
    x=df[df['test_name'] == 'Test_0']['wafer_id'],
    y=df[df['test_name'] == 'Test_0']['value'],
    mode='markers',
    marker=dict(size=6, opacity=0.6, color='blue', line=dict(width=0.5)),
    jitter=0.4,
))
fig_bee.update_layout(title='Bee Swarm: Leakage by Wafer', 
                       xaxis_title='Wafer', yaxis_title='Leakage (µA)',
                       width=1000, height=600, template='plotly_white')
fig_bee.write_html('/tmp/01_bee_swarm.html')

# Box Plot
print("[2/12] Creating Box Plot...")
fig_box = go.Figure()
for wafer in df['wafer_id'].unique():
    wafer_data = df[(df['wafer_id'] == wafer) & (df['test_name'] == 'Test_0')]['value']
    fig_box.add_trace(go.Box(y=wafer_data, name=wafer))
fig_box.update_layout(title='Box Plot: Leakage Distribution', 
                       xaxis_title='Wafer', yaxis_title='Leakage (µA)',
                       width=1000, height=600, template='plotly_white')
fig_box.write_html('/tmp/02_box_plot.html')

# Std Dev with Outliers
print("[3/12] Creating Std Dev Plot with Outliers...")
test_data = df[df['test_name'] == 'Test_0']['value'].dropna()
mean = test_data.mean()
std = test_data.std()
outliers = test_data[np.abs(test_data - mean) > 3 * std]

fig_std = go.Figure()
fig_std.add_trace(go.Scatter(
    x=range(len(test_data)), y=test_data, mode='markers',
    marker=dict(size=5, color='blue'), name='Data'
))
fig_std.add_hline(y=mean, line_dash='dash', line_color='green', name='Mean')
fig_std.add_hline(y=mean + 3*std, line_dash='dash', line_color='orange', name='±3σ')
fig_std.add_hline(y=mean - 3*std, line_dash='dash', line_color='orange')
fig_std.add_trace(go.Scatter(
    x=[i for i, v in enumerate(test_data) if v in outliers.values],
    y=outliers, mode='markers', marker=dict(size=10, color='red', symbol='star'),
    name='Outliers'
))
fig_std.update_layout(title='Std Dev & Outliers', xaxis_title='Index', yaxis_title='Value',
                       width=1000, height=600, template='plotly_white')
fig_std.write_html('/tmp/03_std_dev.html')

# Histogram with Density
print("[4/12] Creating Histogram with Density...")
from scipy.stats import gaussian_kde
test_data = df[df['test_name'] == 'Test_0']['value'].dropna()
kde = gaussian_kde(test_data)
x_range = np.linspace(test_data.min(), test_data.max(), 200)
density = kde(x_range)

fig_hist = go.Figure()
fig_hist.add_trace(go.Histogram(x=test_data, nbinsx=30, name='Histogram', opacity=0.6))
fig_hist.add_trace(go.Scatter(x=x_range, y=density * len(test_data) / density.max(),
                               mode='lines', name='KDE', line=dict(color='red', width=3)))
fig_hist.update_layout(title='Histogram with KDE Density', xaxis_title='Leakage (µA)',
                        yaxis_title='Frequency', width=1000, height=600, template='plotly_white')
fig_hist.write_html('/tmp/04_histogram_density.html')

# Stacked Histogram
print("[5/12] Creating Stacked Histogram...")
df_pass = df[(df['test_name'] == 'Test_0') & (df['status'] == 'PASS')]['value'].dropna()
df_fail = df[(df['test_name'] == 'Test_0') & (df['status'] == 'FAIL')]['value'].dropna()

fig_stack = go.Figure()
fig_stack.add_trace(go.Histogram(x=df_pass, nbinsx=30, name='PASS', marker_color='green', opacity=0.7))
fig_stack.add_trace(go.Histogram(x=df_fail, nbinsx=30, name='FAIL', marker_color='red', opacity=0.7))
fig_stack.update_layout(barmode='stack', title='Stacked Histogram: Pass vs Fail',
                         xaxis_title='Leakage (µA)', yaxis_title='Count',
                         width=1000, height=600, template='plotly_white')
fig_stack.write_html('/tmp/05_stacked_histogram.html')

# 2D Histogram
print("[6/12] Creating 2D Histogram...")
df_test0 = df[df['test_name'] == 'Test_0'][['value']].dropna()
df_test1 = df[df['test_name'] == 'Test_1'][['value']].dropna()

# Merge to get paired data
df_paired = pd.concat([df_test0.reset_index(drop=True), 
                        df_test1.reset_index(drop=True)], axis=1)
df_paired.columns = ['leakage', 'fmax']

fig_2d = go.Figure()
fig_2d.add_trace(go.Histogram2d(x=df_paired['leakage'], y=df_paired['fmax'],
                                nbinsx=20, nbinsy=20, colorscale='Viridis'))
fig_2d.update_layout(title='2D Histogram: Leakage vs Fmax', xaxis_title='Leakage (µA)',
                      yaxis_title='Fmax (MHz)', width=900, height=800, template='plotly_white')
fig_2d.write_html('/tmp/06_histogram_2d.html')

# Heatmap (Parametric)
print("[7/12] Creating Parametric Heatmap...")
wafer_id = df['wafer_id'].iloc[0]
df_wafer = df[(df['wafer_id'] == wafer_id) & (df['test_name'] == 'Test_0')]
heatmap_data = df_wafer.pivot_table(index='die_y', columns='die_x', values='value', aggfunc='mean')

fig_hmap = go.Figure()
fig_hmap.add_trace(go.Heatmap(z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index,
                               colorscale='Viridis'))
fig_hmap.update_layout(title=f'Parametric Heatmap: {wafer_id}', xaxis_title='Die X',
                        yaxis_title='Die Y', width=800, height=800, template='plotly_white')
fig_hmap.write_html('/tmp/07_heatmap_parametric.html')

# Heatmap (Pass/Fail)
print("[8/12] Creating Pass/Fail Heatmap...")
df_wafer_pf = df[(df['wafer_id'] == wafer_id)]
yield_map = df_wafer_pf.groupby(['die_y', 'die_x']).apply(
    lambda g: (g['status'] == 'PASS').sum() / len(g) * 100).unstack()

fig_pf = go.Figure()
fig_pf.add_trace(go.Heatmap(z=yield_map.values, colorscale='RdYlGn', vmin=0, vmax=100))
fig_pf.update_layout(title=f'Yield Heatmap: {wafer_id}', xaxis_title='Die X',
                      yaxis_title='Die Y', width=800, height=800, template='plotly_white')
fig_pf.write_html('/tmp/08_heatmap_passfail.html')

# Correlation Matrix
print("[9/12] Creating Correlation Matrix...")
numeric_cols = ['leakage_ua', 'fmax_mhz', 'iddq_active_ma', 'delay_ns']
df_numeric = df[numeric_cols].fillna(df[numeric_cols].mean())
corr_matrix = df_numeric.corr()

fig_corr = go.Figure()
fig_corr.add_trace(go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns,
                               y=corr_matrix.index, colorscale='RdBu', zmid=0,
                               text=np.round(corr_matrix.values, 2), texttemplate='%{text}'))
fig_corr.update_layout(title='Correlation Matrix', width=900, height=800, template='plotly_white')
fig_corr.write_html('/tmp/09_correlation_matrix.html')

# Test Failure Bar Chart
print("[10/12] Creating Test Failure Bar Chart...")
test_stats = df.groupby('test_name').agg({
    'status': [('total', 'count'), ('fail', lambda x: (x == 'FAIL').sum())]
}).round(2)
test_stats.columns = ['Total', 'Fail']
test_stats['Fail_Rate_%'] = (test_stats['Fail'] / test_stats['Total'] * 100).round(2)
test_stats = test_stats.sort_values('Fail', ascending=True)

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(y=test_stats.index, x=test_stats['Fail'], orientation='h',
                          marker_color='red', name='Fail Count'))
fig_bar.update_layout(title='Test Failure Count', xaxis_title='Failures', yaxis_title='Test',
                       width=1000, height=600, template='plotly_white')
fig_bar.write_html('/tmp/10_test_failures_bar.html')

# Pareto Chart
print("[11/12] Creating Pareto Chart...")
test_failures = df[df['status'] == 'FAIL'].groupby('test_name').size().sort_values(ascending=False)
cumulative_pct = (test_failures.cumsum() / test_failures.sum() * 100)

from plotly.subplots import make_subplots
fig_pareto = make_subplots(specs=[[{'secondary_y': True}]])
fig_pareto.add_trace(go.Bar(x=test_failures.index, y=test_failures.values, name='Failures'),
                      secondary_y=False)
fig_pareto.add_trace(go.Scatter(x=cumulative_pct.index, y=cumulative_pct.values,
                                 mode='lines+markers', name='Cumulative %', line=dict(color='red')),
                      secondary_y=True)
fig_pareto.add_hline(y=80, secondary_y=True, line_dash='dash', annotation_text='80%')
fig_pareto.update_layout(title='Pareto Chart: Test Failures', width=1000, height=600, template='plotly_white')
fig_pareto.write_html('/tmp/11_pareto_chart.html')

# CDF Plot
print("[12/12] Creating CDF Plot...")
test_data_sorted = np.sort(df[df['test_name'] == 'Test_0']['value'].dropna())
cdf = np.arange(1, len(test_data_sorted) + 1) / len(test_data_sorted)

fig_cdf = go.Figure()
fig_cdf.add_trace(go.Scatter(x=test_data_sorted, y=cdf * 100, mode='lines', name='CDF',
                              line=dict(width=2, color='blue')))
fig_cdf.add_vline(x=0.1, line_dash='dash', line_color='orange', annotation_text='LSL')
fig_cdf.add_vline(x=5.0, line_dash='dash', line_color='purple', annotation_text='USL')
fig_cdf.update_layout(title='CDF: Leakage Distribution', xaxis_title='Leakage (µA)',
                       yaxis_title='Cumulative %', width=1000, height=600, template='plotly_white')
fig_cdf.write_html('/tmp/12_cdf_plot.html')

print("\n" + "="*60)
print("✓ All visualizations generated successfully!")
print("="*60)
print("Generated files:")
for i in range(1, 13):
    print(f"  /{i:02d}_*.html")
```

### 10.2 Complete Production Script

```python
#!/usr/bin/env python3
"""
Production-grade wafer analysis script
Processes STDF CSV data and generates comprehensive report
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde, zscore, shapiro, norm
from pathlib import Path
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WaferAnalysisReport:
    """Complete wafer analysis and reporting pipeline."""
    
    def __init__(self, csv_file, output_dir='/reports'):
        """Initialize with input CSV and output directory."""
        self.csv_file = Path(csv_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.df = None
        
    def load_data(self):
        """Load and validate data."""
        logger.info(f"Loading data from {self.csv_file}")
        self.df = pd.read_csv(self.csv_file)
        logger.info(f"✓ Loaded {len(self.df)} records from {self.df['wafer_id'].nunique()} wafers")
        return self
    
    def create_bee_swarm(self, param='leakage_ua', wafer_col='wafer_id'):
        """Create bee swarm plot."""
        logger.info("Creating bee swarm plot...")
        
        fig = go.Figure()
        for wafer in sorted(self.df[wafer_col].unique()):
            wafer_data = self.df[self.df[wafer_col] == wafer][param].dropna()
            mean = wafer_data.mean()
            
            fig.add_trace(go.Scatter(
                x=[wafer] * len(wafer_data), y=wafer_data,
                mode='markers', name=wafer,
                marker=dict(size=6, opacity=0.6, line=dict(width=0.5)),
                jitter=0.3,
            ))
            
            # Add mean line
            fig.add_trace(go.Scatter(
                x=[wafer], y=[mean], mode='markers',
                marker=dict(size=12, color='red', symbol='line', line=dict(width=3)),
                name=f'{wafer} Mean', showlegend=False,
            ))
        
        fig.update_layout(
            title=f'Bee Swarm: {param} Distribution',
            xaxis_title='Wafer', yaxis_title=param,
            width=1200, height=600, template='plotly_white'
        )
        
        self._save_fig(fig, 'bee_swarm')
        return self
    
    def create_box_plots(self, param='leakage_ua', wafer_col='wafer_id', lsl=None, usl=None):
        """Create box plots with outliers."""
        logger.info("Creating box plots...")
        
        fig = go.Figure()
        
        for wafer in sorted(self.df[wafer_col].unique()):
            wafer_data = self.df[self.df[wafer_col] == wafer][param].dropna()
            
            fig.add_trace(go.Box(
                y=wafer_data, x=[wafer] * len(wafer_data),
                name=wafer, boxmean='sd'
            ))
        
        if lsl:
            fig.add_hline(y=lsl, line_dash='dash', line_color='orange', name='LSL')
        if usl:
            fig.add_hline(y=usl, line_dash='dash', line_color='purple', name='USL')
        
        fig.update_layout(
            title=f'Box Plot: {param}',
            xaxis_title='Wafer', yaxis_title=param,
            width=1200, height=600, template='plotly_white'
        )
        
        self._save_fig(fig, 'box_plot')
        return self
    
    def create_std_dev_plot(self, param='leakage_ua', wafer_col='wafer_id'):
        """Create std dev band plot with outliers."""
        logger.info("Creating std dev plot with outliers...")
        
        wafers = sorted(self.df[wafer_col].unique())
        x_pos = np.arange(len(wafers))
        
        means = []
        stds = []
        
        for wafer in wafers:
            data = self.df[self.df[wafer_col] == wafer][param].dropna()
            means.append(data.mean())
            stds.append(data.std())
        
        means = np.array(means)
        stds = np.array(stds)
        
        fig = go.Figure()
        
        # ±3σ band
        fig.add_trace(go.Scatter(
            x=list(wafers) + list(wafers[::-1]),
            y=list(means + 3*stds) + list((means - 3*stds)[::-1]),
            fill='toself', fillcolor='rgba(255,0,0,0.1)',
            line=dict(color='rgba(255,0,0,0)'),
            name='±3σ'
        ))
        
        # ±1σ band
        fig.add_trace(go.Scatter(
            x=list(wafers) + list(wafers[::-1]),
            y=list(means + stds) + list((means - stds)[::-1]),
            fill='toself', fillcolor='rgba(0,100,0,0.2)',
            line=dict(color='rgba(0,100,0,0)'),
            name='±1σ'
        ))
        
        # Mean line
        fig.add_trace(go.Scatter(
            x=wafers, y=means, mode='lines+markers',
            name='Mean', line=dict(color='blue', width=2)
        ))
        
        # Detect and plot outliers
        for idx, wafer in enumerate(wafers):
            data = self.df[self.df[wafer_col] == wafer][param].dropna()
            outliers = data[np.abs(data - means[idx]) > 3 * stds[idx]]
            
            if len(outliers) > 0:
                fig.add_trace(go.Scatter(
                    x=[wafer] * len(outliers), y=outliers,
                    mode='markers', name='Outliers',
                    marker=dict(size=10, color='red', symbol='star', line=dict(width=2)),
                    showlegend=(idx == 0),
                ))
        
        fig.update_layout(
            title=f'Std Dev Bands with Outliers: {param}',
            xaxis_title='Wafer', yaxis_title=param,
            width=1200, height=600, template='plotly_white'
        )
        
        self._save_fig(fig, 'std_dev_outliers')
        return self
    
    def create_histogram_density(self, param='leakage_ua', wafer_col='wafer_id'):
        """Create histogram with KDE overlay."""
        logger.info("Creating histogram with density...")
        
        fig = go.Figure()
        colors = ['blue', 'green', 'red', 'purple', 'orange']
        
        for idx, wafer in enumerate(sorted(self.df[wafer_col].unique())):
            wafer_data = self.df[self.df[wafer_col] == wafer][param].dropna()
            
            # Histogram
            fig.add_trace(go.Histogram(
                x=wafer_data, nbinsx=30, name=f'{wafer}',
                marker=dict(color=colors[idx % len(colors)], opacity=0.5)
            ))
            
            # KDE
            kde = gaussian_kde(wafer_data)
            x_range = np.linspace(wafer_data.min(), wafer_data.max(), 200)
            density = kde(x_range)
            density_scaled = density * len(wafer_data) / density.max() * 0.8
            
            fig.add_trace(go.Scatter(
                x=x_range, y=density_scaled, mode='lines',
                name=f'{wafer} (KDE)', line=dict(color=colors[idx % len(colors)], width=3)
            ))
        
        fig.update_layout(
            title=f'Histogram + KDE Density: {param}',
            xaxis_title=param, yaxis_title='Frequency',
            barmode='overlay', width=1200, height=600, template='plotly_white'
        )
        
        self._save_fig(fig, 'histogram_density')
        return self
    
    def create_heatmaps(self, wafer_id=None, param='leakage_ua'):
        """Create parametric and pass/fail heatmaps."""
        logger.info("Creating heatmaps...")
        
        if wafer_id is None:
            wafer_id = self.df['wafer_id'].iloc[0]
        
        df_wafer = self.df[self.df['wafer_id'] == wafer_id]
        
        # Parametric heatmap
        df_param = df_wafer[df_wafer['value'].notna() if param not in df_wafer.columns else True]
        if param in df_wafer.columns:
            heatmap_data = df_wafer.pivot_table(index='die_y', columns='die_x', values=param, aggfunc='mean')
        else:
            heatmap_data = df_wafer.pivot_table(index='die_y', columns='die_x', values='value', aggfunc='mean')
        
        fig1 = go.Figure()
        fig1.add_trace(go.Heatmap(z=heatmap_data.values, x=heatmap_data.columns,
                                   y=heatmap_data.index, colorscale='Viridis'))
        fig1.update_layout(title=f'Parametric Heatmap: {wafer_id} ({param})',
                           xaxis_title='Die X', yaxis_title='Die Y',
                           width=800, height=800, template='plotly_white')
        self._save_fig(fig1, f'heatmap_param_{wafer_id}')
        
        # Pass/Fail heatmap
        yield_map = df_wafer.groupby(['die_y', 'die_x']).apply(
            lambda g: (g['status'] == 'PASS').sum() / len(g) * 100 if len(g) > 0 else 0
        ).unstack()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Heatmap(z=yield_map.values, colorscale='RdYlGn', vmin=0, vmax=100))
        fig2.update_layout(title=f'Yield Heatmap: {wafer_id}',
                           xaxis_title='Die X', yaxis_title='Die Y',
                           width=800, height=800, template='plotly_white')
        self._save_fig(fig2, f'heatmap_yield_{wafer_id}')
        
        return self
    
    def create_correlation_matrix(self):
        """Create correlation heatmap."""
        logger.info("Creating correlation matrix...")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [c for c in numeric_cols if c not in ['die_x', 'die_y']]
        
        if len(numeric_cols) < 2:
            logger.warning("Not enough numeric columns for correlation analysis")
            return self
        
        df_numeric = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
        corr_matrix = df_numeric.corr()
        
        fig = go.Figure()
        fig.add_trace(go.Heatmap(
            z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.index,
            colorscale='RdBu', zmid=0, zmin=-1, zmax=1,
            text=np.round(corr_matrix.values, 2), texttemplate='%{text}'
        ))
        
        fig.update_layout(
            title='Parameter Correlation Matrix',
            width=1000, height=900, template='plotly_white'
        )
        
        self._save_fig(fig, 'correlation_matrix')
        return self
    
    def create_test_failure_charts(self):
        """Create test failure bar chart and Pareto."""
        logger.info("Creating test failure charts...")
        
        test_stats = self.df.groupby('test_name').agg({
            'status': [('total', 'count'), ('fail', lambda x: (x == 'FAIL').sum())]
        }).round(2)
        test_stats.columns = ['Total', 'Fail']
        test_stats['Fail_Rate_%'] = (test_stats['Fail'] / test_stats['Total'] * 100).round(2)
        test_stats = test_stats.sort_values('Fail', ascending=True)
        
        # Bar chart
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(y=test_stats.index, x=test_stats['Fail'],
                              orientation='h', marker_color='red'))
        fig1.update_layout(
            title='Test Failure Count',
            xaxis_title='Failures', yaxis_title='Test',
            width=1200, height=600, template='plotly_white'
        )
        self._save_fig(fig1, 'test_failures_bar')
        
        # Pareto
        test_failures = self.df[self.df['status'] == 'FAIL'].groupby('test_name').size().sort_values(ascending=False)
        cumulative_pct = (test_failures.cumsum() / test_failures.sum() * 100)
        
        fig2 = make_subplots(specs=[[{'secondary_y': True}]])
        fig2.add_trace(go.Bar(x=test_failures.index, y=test_failures.values, name='Failures'),
                       secondary_y=False)
        fig2.add_trace(go.Scatter(x=cumulative_pct.index, y=cumulative_pct.values,
                                  mode='lines+markers', name='Cumulative %',
                                  line=dict(color='red', width=3)), secondary_y=True)
        fig2.add_hline(y=80, secondary_y=True, line_dash='dash')
        fig2.update_layout(title='Pareto: Test Failures', width=1200, height=600, template='plotly_white')
        self._save_fig(fig2, 'pareto_failures')
        
        return self
    
    def create_cdf_plot(self, param='leakage_ua', lsl=None, usl=None):
        """Create CDF plot."""
        logger.info("Creating CDF plot...")
        
        fig = go.Figure()
        
        for wafer in sorted(self.df['wafer_id'].unique()):
            data_sorted = np.sort(self.df[self.df['wafer_id'] == wafer][param].dropna())
            cdf = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
            
            fig.add_trace(go.Scatter(x=data_sorted, y=cdf * 100, mode='lines',
                                     name=wafer, line=dict(width=2)))
        
        if lsl:
            fig.add_vline(x=lsl, line_dash='dash', line_color='orange')
        if usl:
            fig.add_vline(x=usl, line_dash='dash', line_color='purple')
        
        fig.update_layout(
            title=f'CDF: {param}',
            xaxis_title=param, yaxis_title='Cumulative Yield %',
            width=1200, height=600, template='plotly_white'
        )
        
        self._save_fig(fig, 'cdf_plot')
        return self
    
    def generate_statistics_report(self):
        """Generate text statistics report."""
        logger.info("Generating statistics report...")
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║               WAFER SORT ANALYSIS REPORT                       ║
║               Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                      ║
╚════════════════════════════════════════════════════════════════╝

DATASET SUMMARY
───────────────────────────────────────────────────────────────
Total Records:              {len(self.df):,}
Wafers Analyzed:            {self.df['wafer_id'].nunique()}
Dies Per Wafer:             {len(self.df) // self.df['wafer_id'].nunique():,}
Test Types:                 {self.df['test_name'].nunique() if 'test_name' in self.df.columns else 'N/A'}

YIELD METRICS
───────────────────────────────────────────────────────────────
Overall Yield:              {(self.df['status'] == 'PASS').sum() / len(self.df) * 100:.2f}%
Pass Count:                 {(self.df['status'] == 'PASS').sum():,}
Fail Count:                 {(self.df['status'] == 'FAIL').sum():,}

"""
        
        # Parameter statistics
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [c for c in numeric_cols if c not in ['die_x', 'die_y']]
        
        if numeric_cols:
            report += "PARAMETER STATISTICS\n"
            report += "───────────────────────────────────────────────────────────────\n"
            
            for col in numeric_cols[:5]:  # First 5 numeric columns
                data = self.df[col].dropna()
                report += f"\n{col.upper()}\n"
                report += f"  Mean:          {data.mean():.4f}\n"
                report += f"  Median:        {data.median():.4f}\n"
                report += f"  Std Dev:       {data.std():.4f}\n"
                report += f"  Min:           {data.min():.4f}\n"
                report += f"  Max:           {data.max():.4f}\n"
                report += f"  P1:            {data.quantile(0.01):.4f}\n"
                report += f"  P99:           {data.quantile(0.99):.4f}\n"
                
                # Normality test
                if len(data) > 3:
                    stat, pval = shapiro(data)
                    report += f"  Shapiro-Wilk:  p={pval:.6f} {'(Normal)' if pval > 0.05 else '(NOT Normal)'}\n"
        
        # Save report
        report_path = self.output_dir / f'statistics_report_{self.timestamp}.txt'
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info(f"✓ Report saved: {report_path}")
        print(report)
        
        return self
    
    def _save_fig(self, fig, name):
        """Save figure to HTML."""
        output_path = self.output_dir / f'{name}_{self.timestamp}.html'
        fig.write_html(str(output_path))
        logger.info(f"✓ Saved: {name}")
    
    def run_full_analysis(self):
        """Run complete analysis pipeline."""
        logger.info("=" * 60)
        logger.info("STARTING FULL WAFER ANALYSIS PIPELINE")
        logger.info("=" * 60)
        
        self.load_data()
        self.create_bee_swarm()
        self.create_box_plots()
        self.create_std_dev_plot()
        self.create_histogram_density()
        self.create_heatmaps()
        self.create_correlation_matrix()
        self.create_test_failure_charts()
        self.create_cdf_plot()
        self.generate_statistics_report()
        
        logger.info("=" * 60)
        logger.info("✓ ANALYSIS COMPLETE")
        logger.info(f"✓ Reports saved to: {self.output_dir}")
        logger.info("=" * 60)
        
        return self

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == '__main__':
    # Example 1: Load your STDF CSV and run full analysis
    # pipeline = WaferAnalysisReport('/path/to/wafer_data.csv', output_dir='/reports')
    # pipeline.run_full_analysis()
    
    # Example 2: Generate sample data and analyze
    print("Generating sample data...")
    df = generate_sample_wafer_data(n_wafers=3, dies_per_wafer=100, n_tests=5)
    df.to_csv('/tmp/sample_wafer_data.csv', index=False)
    
    print("Running analysis...")
    pipeline = WaferAnalysisReport('/tmp/sample_wafer_data.csv', output_dir='/tmp/wafer_reports')
    pipeline.run_full_analysis()
```

### 10.3 Command-Line Usage

```bash
# Install dependencies
pip install pandas numpy plotly scipy scikit-learn streamlit

# Run minimal example
python minimal_wafer_example.py

# Run production pipeline
python production_wafer_analysis.py /path/to/wafer_data.csv --output /reports

# Run Streamlit dashboard
streamlit run dashboard_comprehensive.py
```

### 10.4 Integration with Existing Code

```python
# Import and use functions in your own scripts
from wafer_analysis_comprehensive import (
    create_bee_swarm_plot,
    create_interactive_box_plot,
    create_std_dev_plot,
    create_histogram_with_density,
    create_parametric_heatmap,
    create_correlation_heatmap,
    create_test_failure_chart,
    create_pareto_chart,
    create_cdf_plot,
)

import pandas as pd

# Load your data
df = pd.read_csv('your_wafer_data.csv')

# Generate individual charts
fig1 = create_bee_swarm_plot(df, y_col='leakage_ua')
fig2 = create_histogram_with_density(df, param_col='leakage_ua')
fig3 = create_correlation_heatmap(df)

# Display
fig1.show()
fig2.show()
fig3.show()

# Or save to files
fig1.write_html('bee_swarm.html')
fig2.write_html('histogram.html')
fig3.write_html('correlation.html')
```

---

## SECTION 11: BATCH PROCESSING LARGE DATASETS

```python
#!/usr/bin/env python3
"""
Batch process multiple wafer files and generate consolidated report
"""

from pathlib import Path
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def batch_process_wafers(input_dir='/data/stdf_csv', output_dir='/reports'):
    """Process all CSV files in directory."""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    csv_files = list(input_path.glob('*.csv'))
    logger.info(f"Found {len(csv_files)} CSV files")
    
    results = []
    
    for csv_file in csv_files:
        logger.info(f"Processing {csv_file.name}...")
        
        try:
            df = pd.read_csv(csv_file)
            
            # Calculate metrics
            yield_pct = (df['status'] == 'PASS').sum() / len(df) * 100
            wafer_count = df['wafer_id'].nunique() if 'wafer_id' in df.columns else 1
            
            results.append({
                'File': csv_file.name,
                'Total_Dies': len(df),
                'Yield_%': yield_pct,
                'Wafers': wafer_count,
                'Pass_Count': (df['status'] == 'PASS').sum(),
                'Fail_Count': (df['status'] == 'FAIL').sum(),
            })
            
            # Generate report for this file
            from wafer_analysis_comprehensive import WaferAnalysisReport
            pipeline = WaferAnalysisReport(csv_file, output_dir=output_path / csv_file.stem)
            pipeline.run_full_analysis()
            
        except Exception as e:
            logger.error(f"Error processing {csv_file.name}: {e}")
    
    # Save consolidated summary
    summary_df = pd.DataFrame(results)
    summary_path = output_path / 'batch_summary.csv'
    summary_df.to_csv(summary_path, index=False)
    logger.info(f"✓ Summary saved: {summary_path}")
    
    print("\n" + summary_df.to_string())

if __name__ == '__main__':
    batch_process_wafers(input_dir='/data/wafer_csvs', output_dir='/reports/batch')
```

---

## SECTION 12: DATA FORMAT REFERENCE

### Input CSV Format Expected

```csv
wafer_id,die_x,die_y,test_name,value,status,lsl,usl,leakage_ua,fmax_mhz,iddq_active_ma,delay_ns,power_mw
W001,0,0,Test_0,1.23,PASS,0.1,5.0,1.23,1050,12.5,9.8,45.2
W001,0,1,Test_0,1.45,PASS,0.1,5.0,1.45,980,13.1,10.1,46.1
W001,1,0,Test_1,1100,PASS,500,1500,1.23,1100,12.5,9.8,45.2
W001,1,1,Test_1,850,FAIL,500,1500,1.45,850,13.1,10.1,46.1
```

### Minimum Required Columns
- `wafer_id`: Wafer identifier
- `die_x`: Die X coordinate
- `die_y`: Die Y coordinate
- `status`: PASS or FAIL
- `value`: Test parameter value

### Optional Columns (enhances analysis)
- `test_name`: Test identifier
- `lsl`, `usl`: Lower/Upper spec limits
- `leakage_ua`: Leakage current (µA)
- `fmax_mhz`: Maximum frequency (MHz)
- `iddq_active_ma`: Active supply current (mA)
- `delay_ns`: Propagation delay (ns)
- `power_mw`: Power consumption (mW)

