import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE CONFIG & DESCENT BACKGROUND STYLING ---
st.set_page_config(page_title="EduPro Research Dashboard", layout="wide", page_icon="🎓")

# Professional CSS: Soft Steel Blue Background with White Cards
st.markdown("""
    <style>
    /* Descent Dashboard Background */
    .stApp {
        background-color: #f1f4f9; 
    }
    
    .block-container {
        padding-top: 1.5rem;
    }

    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }

    /* Professional Graph Cards */
    .chart-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }

    /* Professional Answer Tags */
    .answer-tag {
        background-color: #f8fafc;
        border-left: 5px solid #2563eb;
        padding: 15px;
        margin-top: 10px;
        color: #1e293b;
        font-weight: 500;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE (Slide 1: Methodology) ---
@st.cache_data
def load_data():
    try:
        # Load datasets
        u = pd.read_csv('Users.csv')
        c = pd.read_csv('Courses.csv')
        t = pd.read_csv('Transactions.csv')
        
        # Methodology: Integration
        df = t.merge(u, on='UserID').merge(c, on='CourseID')
        
        # Methodology: Age Banding
        bins = [0, 18, 25, 35, 45, 100]
        labels = ['<18', '18-25', '26-35', '36-45', '45+']
        df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)
        return df
    except:
        return None

df = load_data()

if df is None:
    st.error("🚨 Dataset files missing! Please ensure Users.csv, Courses.csv, and Transactions.csv are in the folder.")
    st.stop()

# --- 3. SIDEBAR & DEFAULT CASE LOGIC ---
with st.sidebar:
    st.title("🛡️ Research Controls")
    st.markdown(f"**Researcher:** Devaraj Sagar\n**Guide:** Prof. Sai Kagne")
    st.divider()
    
    age_f = st.multiselect("Select Age Group", df['AgeGroup'].unique().categories.tolist())
    gen_f = st.multiselect("Select Gender", df['Gender'].unique().tolist())
    cat_f = st.multiselect("Select Category", df['CourseCategory'].unique().tolist())

# --- THE DEFAULT CASE OUTPUT LOGIC ---
# If no filters are selected, show Global Data automatically
f_df = df.copy()
is_default = True

if age_f or gen_f or cat_f:
    is_default = False
    if age_f: f_df = f_df[f_df['AgeGroup'].isin(age_f)]
    if gen_f: f_df = f_df[f_df['Gender'].isin(gen_f)]
    if cat_f: f_df = f_df[f_df['CourseCategory'].isin(cat_f)]

# --- 4. HEADER & KPIs (Slide 3) ---
st.title("Learner Demographics & Behavioral Intelligence Dashboard")

if is_default:
    st.info("📊 **Default Case Output:** No filters active. Displaying total platform data for broad context.")

# Top Metrics Row
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Enrollments", f"{len(f_df):,}")
k2.metric("Dominant Demographic", f_df['AgeGroup'].mode()[0])
k3.metric("Gender Purity (Max)", f"{f_df['Gender'].value_counts(normalize=True).max()*100:.1f}%")
k4.metric("Market Leader", f_df['CourseCategory'].mode()[0])

st.divider()

# --- 5. TABBED ANALYSIS (Slide 2: Key Questions) ---
t1, t2, t3 = st.tabs(["👤 Demographic Reach", "📚 Enrollment Trends", "🧠 Behavioral Patterns"])

# TAB 1: DEMOGRAPHICS
with t1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.subheader("Q1: Age Distribution Analysis")
        # Color Palette: Blues
        fig1 = px.bar(f_df['AgeGroup'].value_counts().sort_index().reset_index(), 
                      x='AgeGroup', y='count', color='AgeGroup', 
                      color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(f"<div class='answer-tag'><b>Answer:</b> The platform's core audience is the <b>{f_df['AgeGroup'].mode()[0]}</b> age group.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with c2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.subheader("Q3: Gender Variation")
        # Color Palette: Red/Blue Contrast
        fig2 = px.pie(f_df, names='Gender', hole=0.5, color_discrete_sequence=['#1e3a8a', '#f43f5e'], template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(f"<div class='answer-tag'><b>Answer:</b> <b>{f_df['Gender'].value_counts().idxmax()}</b> learners show a stronger enrollment volume.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# TAB 2: ENROLLMENT VARIANCE (The Improved Part)
with t2:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.subheader("Q2: Enrollment Variance (Age Group vs. Course Category)")
    # CORRECT VISUALIZATION: Heatmap for Variance/Concentration
    # Color Palette: Viridis (Scientific Standard)
    heat_data = f_df.groupby(['AgeGroup', 'CourseCategory'], observed=False).size().unstack(fill_value=0)
    fig_heat = px.imshow(heat_data, text_auto=True, color_continuous_scale='Viridis', aspect="auto", template="plotly_white")
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("<div class='answer-tag'><b>Analytical Method:</b> We use a Heatmap to visualize variance. Darker/Brighter spots identify 'Hotspots' where specific age groups prefer certain subjects (e.g., Programming for 18-25).</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.subheader("Q4: Category Enrollment Volume")
    # Color Palette: Greens
    fig_cat = px.bar(f_df['CourseCategory'].value_counts().reset_index(), 
                     x='count', y='CourseCategory', orientation='h', color='count', 
                     color_continuous_scale="Greens", template="plotly_white")
    st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown(f"<div class='answer-tag'><b>Answer:</b> <b>{f_df['CourseCategory'].mode()[0]}</b> is the most popular subject.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# TAB 3: BEHAVIORAL PATTERNS
with t3:
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.subheader("Q5: Beginner Format Preferences")
        # Color Palette: Purples
        beg_df = f_df[f_df['CourseLevel'] == 'Beginner']
        if not beg_df.empty:
            fig5 = px.bar(beg_df['CourseType'].value_counts().reset_index(), x='CourseType', y='count', color='CourseType', color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig5, use_container_width=True)
            st.markdown(f"<div class='answer-tag'><b>Answer:</b> Beginners show a preference for <b>{beg_df['CourseType'].mode()[0]}</b> course types.</div>", unsafe_allow_html=True)
        else:
            st.info("No beginner-level data found.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with c4:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.subheader("Skill Level Progression Funnel")
        # Color Palette: Gold/Sunset
        fig6 = px.funnel(f_df['CourseLevel'].value_counts().reset_index(), y='CourseLevel', x='count', color_discrete_sequence=['#fbbf24'])
        st.plotly_chart(fig6, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Footer Master Table
with st.expander("📂 Integrated Research Data Table"):
    st.dataframe(f_df.head(100), use_container_width=True)