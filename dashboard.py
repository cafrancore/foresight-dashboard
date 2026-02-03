import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Strategic Foresight - Social Protection Reform Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #374151;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .highlight {
        background-color: #DBEAFE;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_and_prepare_data():
    """Load the classification results and prepare for visualization"""
    try:
        # Load the processed data
        df = pd.read_excel("strategic_analysis.xlsx")
        
        # Rename 'Country' to 'country' for consistency (if it exists)
        if 'Country' in df.columns and 'country' not in df.columns:
            df.rename(columns={'Country': 'country'}, inplace=True)
        
        # Ensure required columns exist
        required_columns = ['strategic_classification', 'link_type', 'country', 'summary']
        for col in required_columns:
            if col not in df.columns:
                if col == 'link_type':
                    df['link_type'] = 'Unclassified'
                elif col == 'country':
                    df['country'] = 'Unknown'
        
        return df
    except FileNotFoundError:
        st.error("Please run the analysis first to generate 'strategic_analysis.xlsx'")
        return None
    """Load the classification results and prepare for visualization"""
    try:
        # Load the processed data
        df = pd.read_excel("strategic_analysis.xlsx")
        
        # Ensure required columns exist
        required_columns = ['strategic_classification', 'link_type', 'country', 'summary']
        for col in required_columns:
            if col not in df.columns:
                if col == 'link_type':
                    # If link_type doesn't exist, create a default
                    df['link_type'] = 'Unclassified'
                elif col == 'country':
                    # Try to extract country from other columns or create dummy
                    df['country'] = 'Unknown'
        
        return df
    except FileNotFoundError:
        st.error("Please run the analysis first to generate 'strategic_analysis.xlsx'")
        return None

def create_summary_metrics(df):
    """Create summary metrics cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Reforms",
            value=len(df),
            help="Total number of analyzed reforms"
        )
    
    with col2:
        classified_reforms = len(df[df['strategic_classification'] != 'Unclassified'])
        st.metric(
            label="Classified Reforms",
            value=classified_reforms,
            delta=f"{(classified_reforms/len(df)*100):.1f}%",
            help="Reforms classified into megatrends"
        )
    
    with col3:
        direct_reforms = len(df[df['link_type'] == 'Direct'])
        st.metric(
            label="Direct Reforms",
            value=direct_reforms,
            help="Reforms with direct links to megatrends"
        )
    
    with col4:
        indirect_reforms = len(df[df['link_type'] == 'Indirect'])
        st.metric(
            label="Indirect Reforms",
            value=indirect_reforms,
            help="Reforms with indirect links to megatrends"
        )

def create_trend_distribution_chart(df):
    """Create bar chart for observations per category"""
    # Count reforms by category
    trend_counts = df['strategic_classification'].value_counts().reset_index()
    trend_counts.columns = ['Category', 'Count']
    
    # Sort by count
    trend_counts = trend_counts.sort_values('Count', ascending=False)
    
    # Create bar chart
    fig = px.bar(
        trend_counts,
        x='Category',
        y='Count',
        title='Number of Reforms by Megatrend',
        color='Count',
        color_continuous_scale='Viridis',
        text='Count'
    )
    
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5
    )
    
    fig.update_layout(
        xaxis_title="Megatrend",
        yaxis_title="Number of Reforms",
        plot_bgcolor='white',
        height=500,
        xaxis={'categoryorder': 'total descending'}
    )
    
    return fig

def create_link_type_distribution(df):
    """Create donut charts showing direct/indirect distribution per category"""
    # Filter out unclassified
    classified_df = df[df['strategic_classification'] != 'Unclassified']
    
    if len(classified_df) == 0:
        return None
    
    # Create pivot table
    pivot_data = pd.crosstab(
        classified_df['strategic_classification'],
        classified_df['link_type'],
        normalize='index'
    ).reset_index()
    
    # Melt for plotting
    melted_data = pd.melt(
        pivot_data,
        id_vars=['strategic_classification'],
        var_name='Link Type',
        value_name='Percentage'
    )
    
    # Get unique categories
    categories = melted_data['strategic_classification'].unique()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type':'domain'}, {'type':'domain'}],
               [{'type':'domain'}, {'type':'domain'}]],
        subplot_titles=categories
    )
    
    colors = {'Direct': '#2E86AB', 'Indirect': '#A23B72', 'Weak/Unclear': '#F18F01', 'None': '#C73E1D'}
    
    for i, category in enumerate(categories):
        row = i // 2 + 1
        col = i % 2 + 1
        
        cat_data = melted_data[melted_data['strategic_classification'] == category]
        
        fig.add_trace(
            go.Pie(
                labels=cat_data['Link Type'],
                values=cat_data['Percentage'],
                hole=0.4,
                marker_colors=[colors.get(lt, '#999999') for lt in cat_data['Link Type']],
                textinfo='label+percent',
                textposition='inside',
                showlegend=False if i > 0 else True,
                hovertemplate=f"<b>{category}</b><br>" +
                            "%{label}: %{percent}<extra></extra>"
            ),
            row=row, col=col
        )
    
    fig.update_layout(
        title_text="Direct vs Indirect Reforms by Megatrend",
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_country_analysis(df):
    """Create visualizations for countries with most direct/indirect reforms"""
    # Ensure we have country data
    if 'country' not in df.columns or df['country'].isnull().all():
        st.warning("Country data not available for analysis")
        return None
    
    # Filter out unknown countries
    country_df = df[df['country'] != 'Unknown'].copy()
    
    if len(country_df) == 0:
        return None
    
    # 1. Countries with most direct reforms
    direct_by_country = country_df[country_df['link_type'] == 'Direct'].groupby('country').size().reset_index()
    direct_by_country.columns = ['Country', 'Direct Reforms']
    direct_by_country = direct_by_country.sort_values('Direct Reforms', ascending=False).head(10)
    
    # 2. Countries with most indirect reforms
    indirect_by_country = country_df[country_df['link_type'] == 'Indirect'].groupby('country').size().reset_index()
    indirect_by_country.columns = ['Country', 'Indirect Reforms']
    indirect_by_country = indirect_by_country.sort_values('Indirect Reforms', ascending=False).head(10)
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Top 10 Countries - Direct Reforms', 'Top 10 Countries - Indirect Reforms'),
        horizontal_spacing=0.2
    )
    
    # Direct reforms bar chart
    fig.add_trace(
        go.Bar(
            x=direct_by_country['Direct Reforms'],
            y=direct_by_country['Country'],
            orientation='h',
            marker_color='#2E86AB',
            name='Direct',
            text=direct_by_country['Direct Reforms'],
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Indirect reforms bar chart
    fig.add_trace(
        go.Bar(
            x=indirect_by_country['Indirect Reforms'],
            y=indirect_by_country['Country'],
            orientation='h',
            marker_color='#A23B72',
            name='Indirect',
            text=indirect_by_country['Indirect Reforms'],
            textposition='outside'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        plot_bgcolor='white'
    )
    
    fig.update_xaxes(title_text="Number of Reforms", row=1, col=1)
    fig.update_xaxes(title_text="Number of Reforms", row=1, col=2)
    fig.update_yaxes(title_text="Country", row=1, col=1)
    fig.update_yaxes(title_text="Country", row=1, col=2)
    
    return fig, direct_by_country, indirect_by_country

def create_treemap_visualization(df):
    """Create treemap showing hierarchical structure of reforms"""
    # Prepare data for treemap
    treemap_data = df.copy()
    
    # Create a column for the hierarchical structure
    treemap_data['path'] = treemap_data.apply(
        lambda x: f"All Reforms/{x['strategic_classification']}/{x.get('link_type', 'Unclassified')}",
        axis=1
    )
    
    # Count reforms at each level
    path_counts = treemap_data.groupby('path').size().reset_index()
    path_counts.columns = ['path', 'count']
    
    # Create treemap
    fig = px.treemap(
        path_counts,
        path=['path'],
        values='count',
        title='Reform Distribution Hierarchy',
        color='count',
        color_continuous_scale='RdYlBu',
        hover_data={'count': True}
    )
    
    fig.update_traces(
        textinfo="label+value",
        texttemplate="<b>%{label}</b><br>%{value} reforms",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
    )
    
    fig.update_layout(
        height=600,
        margin=dict(t=50, l=25, r=25, b=25)
    )
    
    return fig
    """Create treemap showing hierarchical structure of reforms"""
    # Prepare data for treemap
    treemap_data = df.copy()
    
    # Create a column for the hierarchical structure
    treemap_data['path'] = treemap_data.apply(
        lambda x: f"All Reforms/{x['strategic_classification']}/{x.get('link_type', 'Unclassified')}",
        axis=1
    )
    
    # Count reforms at each level
    path_counts = treemap_data.groupby('path').size().reset_index()
    path_counts.columns = ['path', 'count']
    
    # Create treemap
    fig = px.treemap(
        path_counts,
        path=['path'],
        values='count',
        title='Reform Distribution Hierarchy',
        color='count',
        color_continuous_scale='RdYlBu',
        hover_data={'count': True}
    )
    
    fig.update_traces(
        textinfo="label+value",
        texttemplate="<b>%{label}</b><br>%{value} reforms",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
    )
    
    fig.update_layout(
        height=600,
        margin=dict(t=50, l=25, r=25, b=25)
    )
    
    return fig

    """Create time series visualization if date data exists"""
    if 'year' in df.columns or 'date' in df.columns:
        # Determine which date column to use
        date_col = 'year' if 'year' in df.columns else 'date'
        
        # Ensure it's datetime
        if date_col == 'date':
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df['year'] = df[date_col].dt.year
            date_col = 'year'
        
        # Group by year and category
        yearly_trends = df.groupby([date_col, 'strategic_classification']).size().reset_index()
        yearly_trends.columns = [date_col, 'Category', 'Count']
        
        # Create line chart
        fig = px.line(
            yearly_trends,
            x=date_col,
            y='Count',
            color='Category',
            title='Reform Trends Over Time',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Number of Reforms",
            plot_bgcolor='white',
            height=500
        )
        
        return fig
    return None

def create_reform_details_table(df):
    """Create an interactive table with reform details"""
    # Select columns to display
    display_columns = ['country', 'strategic_classification', 'link_type',  'summary' ]
    display_columns = [col for col in display_columns if col in df.columns]
    
    # Create a subset dataframe
    display_df = df[display_columns].copy()
    
    # Truncate summary for better display
    if 'summary' in display_df.columns:
        display_df['summary'] = display_df['summary'].apply(
            lambda x: (x[:100] + '...') if isinstance(x, str) and len(x) > 100 else x
        )
    
    return display_df

def main():
    """Main dashboard function"""
    st.title("📊 Strategic Foresight: Social Protection Reform Analysis Dashboard")
    st.subheader("Social Protection Digest 2025")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_and_prepare_data()
    
    if df is None:
        return
    
    # Sidebar for filters
    st.sidebar.title("🔍 Filters")
    
    # Category filter
    all_categories = ['All'] + list(df['strategic_classification'].unique())
    selected_category = st.sidebar.selectbox(
        "Select Megatrend",
        all_categories
    )
    
    # Link type filter
    all_link_types = ['All'] + list(df['link_type'].unique())
    selected_link_type = st.sidebar.selectbox(
        "Select Link Type",
        all_link_types
    )
    
    # Apply filters
    filtered_df = df.copy()
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['strategic_classification'] == selected_category]
    
    if selected_link_type != 'All':
        filtered_df = filtered_df[filtered_df['link_type'] == selected_link_type]
    
    # Country filter (if available)
    if 'country' in filtered_df.columns:
        countries = ['All'] + list(filtered_df['country'].unique())
        selected_country = st.sidebar.selectbox(
            "Select Country",
            countries
        )
        
        if selected_country != 'All':
            filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    # Display summary metrics
    st.markdown("### 📈 Overview Metrics")
    create_summary_metrics(filtered_df)
    
    st.markdown("---")
    
    # Row 1: Distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            create_trend_distribution_chart(filtered_df),
            use_container_width=True
        )
    
    with col2:
        link_chart = create_link_type_distribution(filtered_df)
        if link_chart:
            st.plotly_chart(
                link_chart,
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Row 2: Country analysis
    st.markdown("### 🌍 Country Analysis")
    country_results = create_country_analysis(filtered_df)
    
    if country_results:
        country_chart, direct_countries, indirect_countries = country_results
        
        # Display charts
        st.plotly_chart(
            country_chart,
            use_container_width=True
        )
        
        # Display data tables
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top Countries - Direct Reforms")
            st.dataframe(
                direct_countries,
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.markdown("#### Top Countries - Indirect Reforms")
            st.dataframe(
                indirect_countries,
                use_container_width=True,
                hide_index=True
            )
    
    st.markdown("---")
    
     
    
    # Row 3: Treemap
    st.markdown("### 📊 Reform Distribution Hierarchy")
    st.plotly_chart(
        create_treemap_visualization(filtered_df),
        use_container_width=True
    )
   
    
    st.markdown("---")
    
    # Detailed reform table
    st.markdown("### 📋 Reform Details")
    
    # Search functionality
    search_term = st.text_input("🔍 Search in reform summaries", "")
    
    if search_term:
        search_df = filtered_df[filtered_df['summary'].str.contains(search_term, case=False, na=False)]
    else:
        search_df = filtered_df
    
    # Display table
    st.dataframe(
        create_reform_details_table(search_df),
        use_container_width=True,
        height=400
    )
    
    # Export option
    if st.button("📥 Export Filtered Data"):
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_reforms.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
            Dashboard created with Streamlit • Data last updated: automatically generated
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

