import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'Imports_Exports_Dataset.csv'  # User-specified file path
sample_df = pd.read_csv(file_path).sample(n=3001, random_state=55054)

# Set up the Streamlit page configuration
st.set_page_config(page_title="Imports/Exports Dashboard", layout="wide")

# Sidebar for navigation and filters
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Welcome Page", "Data Preview", "Analysis Dashboard", "Key Observations and Insights"])

# Welcome Page
if page == "Welcome Page":
    st.title("Welcome to the Imports/Exports Dashboard")
    st.markdown("""
    #### Purpose:
    This dashboard provides a comprehensive view of global imports and exports data, aiming to support strategic decision-making with detailed insights into trade volumes, product categories, shipping methods, and financial impacts.
    
    #### Key Features:
    - **Data Preview**: Filter and explore raw data directly.
    - **Analysis Dashboard**: Visualize trends and patterns in global trade with interactive charts.
    - **Key Observations and Insights**: Summarize the most critical findings and managerial insights to guide strategic actions.
    """)

elif page == "Data Preview":
    st.title("📊 Data Preview Dashboard")

    # Sidebar Filters
    selected_countries = st.sidebar.multiselect("Select Countries", sample_df['Country'].unique())
    selected_product = st.sidebar.selectbox("Select Product", ["All"] + list(sample_df['Product'].unique()))

    # Filter Data based on selections
    if selected_countries or selected_product != "All":
        filtered_df = sample_df[
            (sample_df['Country'].isin(selected_countries) if selected_countries else True) &
            (sample_df['Product'] == selected_product if selected_product != "All" else True)
        ]
        st.subheader("Filtered Data")
    else:
        filtered_df = sample_df.head(10)
        st.subheader("First 10 Rows of Data")

    # Display the data
    st.dataframe(filtered_df)

    # Summary Statistics for displayed data
    st.subheader("Summary Statistics")
    summary_df = filtered_df[['Quantity', 'Value', 'Weight']].describe().T
    st.table(summary_df)

    # Save filtered data option
    if st.button("Save Filtered Data"):
        filtered_df.to_csv("Filtered_Data.csv", index=False)
        st.success("Filtered data saved as 'Filtered_Data.csv'")

elif page == "Analysis Dashboard":
    st.title("📊 Comprehensive Analysis Dashboard")

    # Top metrics displayed in cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="Total Records", value=sample_df.shape[0])
    col2.metric(label="Unique Products", value=sample_df['Product'].nunique())
    col3.metric(label="Unique Countries", value=sample_df['Country'].nunique())
    col4.metric(label="Most Used Shipping Method", value=sample_df['Shipping_Method'].mode()[0])
    col5.metric(label="Top Product", value=sample_df['Product'].mode()[0])

    # Filters for analysis
    st.sidebar.title("Filters")
    selected_country = st.sidebar.selectbox("Country", ["All"] + list(sample_df['Country'].unique()))
    import_export_choice = st.sidebar.radio("Import/Export", ["All", "Import", "Export"])

    filtered_data = sample_df.copy()
    if selected_country != "All":
        filtered_data = filtered_data[filtered_data['Country'] == selected_country]
    if import_export_choice != "All":
        filtered_data = filtered_data[filtered_data['Import_Export'] == import_export_choice]

    # Section for graphs and charts
    st.subheader("Data Visualizations")

    # Row 1: Top 5 Countries by Volume and Weight Heatmap
    col6, col7 = st.columns(2)
    
    with col6:
        st.subheader(f"Top 5 Countries by {import_export_choice if import_export_choice != 'All' else 'Total'} Volume")
        top_countries = filtered_data['Country'].value_counts().head(5)
        fig, ax1 = plt.subplots(figsize=(6, 3))
        sns.barplot(x=top_countries.index, y=top_countries.values, palette="Blues", ax=ax1)
        ax1.set_title("Top 5 Countries by Volume")
        ax1.set_ylabel("Volume")
        st.pyplot(fig)

    with col7:
        st.subheader("Maximum Weight in KGs per Shipping Method and Category")
        heatmap_data = pd.DataFrame({
            "Clothing": [4988.04, 4994.90, 4982.45],
            "Electronics": [4996.43, 4990.74, 4990.24],
            "Furniture": [4979.17, 4932.57, 4970.20],
            "Machinery": [4987.92, 4985.67, 4996.15],
            "Toys": [4999.93, 4989.29, 4995.70]
        }, index=["Air", "Land", "Sea"])
        fig, ax2 = plt.subplots(figsize=(6, 3))
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
        ax2.set_title("Weight Distribution by Shipping Method and Category")
        st.pyplot(fig)

    # Row 2: Stacked Bar Chart for Payment Terms and Pie Chart for Category Ranking
    col8, col9 = st.columns(2)
    
    with col8:
        st.subheader("Count of Products by Payment Terms per Category")
        payment_terms_data = pd.DataFrame({
            "Cash on Delivery": [168, 149, 171, 168, 130],
            "Net 30": [134, 146, 144, 123, 144],
            "Net 60": [158, 145, 141, 165, 145],
            "Prepaid": [167, 144, 159, 149, 151]
        }, index=["Clothing", "Electronics", "Furniture", "Machinery", "Toys"])
        fig, ax3 = plt.subplots(figsize=(6, 3))
        payment_terms_data.plot(kind="bar", stacked=True, ax=ax3, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ax3.set_title("Stacked Bar Chart of Payment Terms by Category")
        ax3.set_xlabel("Category")
        ax3.set_ylabel("Count of Products")
        ax3.legend(title="Payment Terms")
        st.pyplot(fig)

    with col9:
        st.subheader("Category Ranking by Total Economic Impact")
        economic_impact_data = pd.DataFrame({
            "Category": ["Clothing", "Furniture", "Machinery", "Electronics", "Toys"],
            "Total Economic Impact in $": [3158986.65, 3072763.57, 3014336.55, 2956832.00, 2780069.80]
        })
        fig, ax4 = plt.subplots(figsize=(6, 3))
        ax4.pie(economic_impact_data["Total Economic Impact in $"], labels=economic_impact_data["Category"],
                autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        ax4.set_title("Economic Impact Distribution by Category")
        st.pyplot(fig)
    
    # Minimum and Maximum tables
    st.subheader("Minimum and Maximum Values")
    min_data = {
        "Field": ["Country", "Product", "Import_Export", "Category", "Port", "Shipping Method", "Supplier", "Customer", "Payment Terms"],
        "Minimum Value": [
            sample_df['Country'].min(),
            sample_df['Product'].min(),
            sample_df['Import_Export'].min(),
            sample_df['Category'].min(),
            sample_df['Port'].min(),
            sample_df['Shipping_Method'].min(),
            sample_df['Supplier'].min(),
            sample_df['Customer'].min(),
            sample_df['Payment_Terms'].min()
        ],
        "Maximum Value": [
            sample_df['Country'].max(),
            sample_df['Product'].max(),
            sample_df['Import_Export'].max(),
            sample_df['Category'].max(),
            sample_df['Port'].max(),
            sample_df['Shipping_Method'].max(),
            sample_df['Supplier'].max(),
            sample_df['Customer'].max(),
            sample_df['Payment_Terms'].max()
        ]
    }
    min_max_table = pd.DataFrame(min_data)

    # Display tables side-by-side
    col10, col11 = st.columns(2)
    with col10:
        st.write("Minimum Values")
        st.table(min_max_table[['Field', 'Minimum Value']])
    with col11:
        st.write("Maximum Values")
        st.table(min_max_table[['Field', 'Maximum Value']])

elif page == "Key Observations and Insights":
    st.title("🔍 Key Observations and Insights")
    
    st.markdown("## Summary of Key Findings")
    st.markdown("""
    - **Top Countries**: The countries with the highest import/export volumes are critical players and could offer strategic partnership opportunities. Focusing on these could enhance business reach and customer base.
    - **Shipping Methods**: The most frequently used shipping method is identified, indicating a preference that can streamline logistics operations. Investing in optimizing this method could lead to cost savings and efficiency.
    - **Category Impact**: The categories with the highest economic impact—such as Clothing and Furniture—should be prioritized for marketing and inventory planning as they contribute significantly to revenue.
    - **Product and Payment Terms Preferences**: The stacked bar chart illustrates that prepaid and cash-on-delivery are popular payment terms across categories. Offering incentives for prepaid payments might improve cash flow and reduce risk.
    """)

    st.markdown("## Managerial Insights")
    st.markdown("""
    - **Strategic Partnerships**: Developing relationships with top countries involved in import/export can foster better trade routes and competitive pricing.
    - **Operational Focus on Top Shipping Method**: Since the most used shipping method is identified, investing in optimizing this process can reduce turnaround times and improve customer satisfaction.
    - **Targeted Marketing**: Categories like Clothing and Furniture, which have high economic impacts, should be prioritized for targeted marketing campaigns to maximize returns.
    - **Financial Strategy**: Offering discounts for prepaid orders can enhance liquidity, while monitoring cash-on-delivery trends can inform risk management practices.
    - **Resource Allocation**: The preference for certain categories suggests areas where resource allocation (e.g., inventory, workforce) should be focused to meet demand efficiently.
    """)

    st.markdown("## Recommendations")
    st.markdown("""
    - **Enhance Shipping Capabilities**: Given the weight distribution across shipping methods, consider enhancing capabilities in the most utilized methods (e.g., Air and Sea) to ensure quality and timeliness.
    - **Diversify Payment Options**: While prepaid and cash-on-delivery are popular, introducing digital wallets or BNPL (Buy Now, Pay Later) options could attract a broader customer base.
    - **Regular Data Analysis**: Ongoing data analysis of import/export trends and shipping preferences can help in dynamically adjusting strategies to meet market demands.
    - **Leverage Technology**: Implementing automated systems for managing frequently used shipping methods and optimizing inventory for top products can lead to significant operational efficiencies.
    """)

    st.markdown("### Conclusion")
    st.markdown("""
    This analysis highlights key areas for optimization in imports and exports. By focusing on strategic partnerships, optimizing shipping methods, targeting high-impact categories, and offering diverse payment options, the business can enhance its operational efficiency and expand its market reach. Continuous data analysis and leveraging technology will be essential in staying competitive and responsive to market changes.
    """)

    # Optional footer for aesthetic purposes or additional information
st.sidebar.info("Developed by [Amitanshu Tiwari- 055054]")
