# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- DATA CREATION (DO NOT MODIFY) -----
np.random.seed(42)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                  'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']
quarterly_data = []
for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:
                seasonal_factor = 1.3
            elif quarter.quarter == 1:
                seasonal_factor = 0.8
            location_factor = {'Tampa': 1.0, 'Miami': 1.2, 'Orlando': 0.9, 'Jacksonville': 0.8}[location]
            category_factor = {'Electronics': 1.5, 'Clothing': 1.0, 'Home Goods': 0.8, 'Sporting Goods': 0.7, 'Beauty': 0.9}[category]
            growth_factor = (1 + 0.05/4) ** quarter_idx
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            quarterly_data.append({
                'Quarter': quarter, 'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location, 'Category': category,
                'Sales': round(sales, 2), 'AdSpend': round(ad_spend, 2), 'Year': quarter.year
            })
customer_data = []
total_customers = 2000
age_params = {'Tampa': (45, 15), 'Miami': (35, 12), 'Orlando': (38, 14), 'Jacksonville': (42, 13)}
for location in locations:
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {'Tampa': 0.3, 'Miami': 0.35, 'Orlando': 0.2, 'Jacksonville': 0.15}[location])
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)
    for age in ages:
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        base_amount = np.random.gamma(shape=5, scale=20)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], p=[0.3, 0.5, 0.2])
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        purchase_amount = base_amount * tier_factor
        customer_data.append({'Location': location, 'Age': age, 'Category': category_preference,
                               'PurchaseAmount': round(purchase_amount, 2), 'PriceTier': price_tier})
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization
def plot_quarterly_sales_trend():
    """Line chart showing total quarterly sales across all locations and categories."""
    quarterly_totals = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(quarter_labels, quarterly_totals.values, marker='o', linewidth=2, color='steelblue')
    ax.set_title('SunCoast Retail: Total Quarterly Sales Trend', fontsize=14)
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Total Sales ($)')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_location_sales_comparison():
    """Multi-line chart comparing quarterly sales trends across locations."""
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['steelblue', 'tomato', 'green', 'purple']
    markers = ['o', 's', '^', 'D']
    for i, location in enumerate(locations):
        loc_data = sales_df[sales_df['Location'] == location].groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
        ax.plot(quarter_labels, loc_data.values, marker=markers[i], color=colors[i],
                linewidth=2, label=location)
    ax.set_title('Quarterly Sales by Location', fontsize=14)
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Total Sales ($)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# TODO 2: Categorical Comparison
def plot_category_performance_by_location():
    """Grouped bar chart for category performance by location (most recent quarter)."""
    recent = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']
    pivot = recent.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot.plot(kind='bar', ax=ax, width=0.8)
    ax.set_title('Category Performance by Location (Q4 2023)', fontsize=14)
    ax.set_xlabel('Location')
    ax.set_ylabel('Sales ($)')
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1))
    plt.xticks(rotation=0)
    plt.tight_layout()
    return fig


def plot_sales_composition_by_location():
    """Stacked bar chart showing sales composition by category for each location."""
    pivot = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_pct.plot(kind='bar', stacked=True, ax=ax, colormap='tab10')
    ax.set_title('Sales Composition by Location (%)', fontsize=14)
    ax.set_xlabel('Location')
    ax.set_ylabel('Percentage of Sales (%)')
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1))
    plt.xticks(rotation=0)
    plt.tight_layout()
    return fig


# TODO 3: Relationship Analysis
def plot_ad_spend_vs_sales():
    """Scatter plot of ad spend vs sales with best-fit line."""
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.4, color='steelblue', edgecolors='none')
    # Best-fit line
    m, b = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    x_line = np.linspace(sales_df['AdSpend'].min(), sales_df['AdSpend'].max(), 100)
    ax.plot(x_line, m * x_line + b, color='tomato', linewidth=2, label='Best-fit line')
    ax.set_title('Advertising Spend vs. Sales', fontsize=14)
    ax.set_xlabel('Ad Spend ($)')
    ax.set_ylabel('Sales ($)')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig


def plot_ad_efficiency_over_time():
    """Line chart showing sales per dollar spent on advertising over time."""
    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean().reindex(quarter_labels)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(quarter_labels, efficiency.values, marker='o', linewidth=2, color='green')
    ax.set_title('Average Ad Efficiency Over Time (Sales per $1 Ad Spend)', fontsize=14)
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales per Dollar Spent')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# TODO 4: Distribution Analysis
def plot_customer_age_distribution():
    """Histograms of customer age distribution overall and by location."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    # Overall
    axes[0, 0].hist(customer_df['Age'], bins=20, color='steelblue', edgecolor='white')
    axes[0, 0].axvline(customer_df['Age'].mean(), color='red', linestyle='--', label=f"Mean: {customer_df['Age'].mean():.1f}")
    axes[0, 0].axvline(customer_df['Age'].median(), color='orange', linestyle='--', label=f"Median: {customer_df['Age'].median():.1f}")
    axes[0, 0].set_title('All Locations')
    axes[0, 0].legend()
    # By location
    colors = ['tomato', 'green', 'purple', 'brown']
    for i, location in enumerate(locations):
        row, col = (i + 1) // 3, (i + 1) % 3
        loc_ages = customer_df[customer_df['Location'] == location]['Age']
        axes[row, col].hist(loc_ages, bins=15, color=colors[i], edgecolor='white')
        axes[row, col].axvline(loc_ages.mean(), color='red', linestyle='--', label=f"Mean: {loc_ages.mean():.1f}")
        axes[row, col].axvline(loc_ages.median(), color='orange', linestyle='--', label=f"Median: {loc_ages.median():.1f}")
        axes[row, col].set_title(location)
        axes[row, col].legend()
    axes[1, 2].axis('off')
    fig.suptitle('Customer Age Distribution by Location', fontsize=15)
    plt.tight_layout()
    return fig


def plot_purchase_by_age_group():
    """Box plots of purchase amounts by age group."""
    bins = [18, 30, 45, 60, 80]
    labels = ['18-30', '31-45', '46-60', '61+']
    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins=bins, labels=labels, right=True)
    fig, ax = plt.subplots(figsize=(9, 6))
    groups = [customer_df[customer_df['AgeGroup'] == g]['PurchaseAmount'].values for g in labels]
    ax.boxplot(groups, labels=labels, patch_artist=True,
               boxprops=dict(facecolor='steelblue', alpha=0.6))
    ax.set_title('Purchase Amounts by Age Group', fontsize=14)
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Purchase Amount ($)')
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig


# TODO 5: Sales Distribution
def plot_purchase_amount_distribution():
    """Histogram of purchase amounts."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(customer_df['PurchaseAmount'], bins=40, color='steelblue', edgecolor='white')
    ax.set_title('Distribution of Purchase Amounts', fontsize=14)
    ax.set_xlabel('Purchase Amount ($)')
    ax.set_ylabel('Number of Customers')
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    return fig


def plot_sales_by_price_tier():
    """Pie chart of sales by price tier with largest slice exploded."""
    tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    explode = [0.05 if tier == tier_sales.idxmax() else 0 for tier in tier_sales.index]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(tier_sales.values, labels=tier_sales.index, autopct='%1.1f%%',
           explode=explode, startangle=140, colors=['#ff9999', '#66b3ff', '#99ff99'])
    ax.set_title('Sales Breakdown by Price Tier', fontsize=14)
    plt.tight_layout()
    return fig


# TODO 6: Market Share Analysis
def plot_category_market_share():
    """Pie chart of category market share with largest segment exploded."""
    cat_sales = sales_df.groupby('Category')['Sales'].sum()
    explode = [0.05 if cat == cat_sales.idxmax() else 0 for cat in cat_sales.index]
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.pie(cat_sales.values, labels=cat_sales.index, autopct='%1.1f%%',
           explode=explode, startangle=140)
    ax.set_title('Market Share by Product Category', fontsize=14)
    plt.tight_layout()
    return fig


def plot_location_sales_distribution():
    """Pie chart of sales distribution by location."""
    loc_sales = sales_df.groupby('Location')['Sales'].sum()
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(loc_sales.values, labels=loc_sales.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Sales Distribution by Location', fontsize=14)
    plt.tight_layout()
    return fig


# TODO 7: Comprehensive Dashboard
def create_business_dashboard():
    """Dashboard with 4 key subplots."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('SunCoast Retail Business Dashboard', fontsize=16, fontweight='bold')

    # 1. Quarterly sales trend
    quarterly_totals = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
    axes[0, 0].plot(quarter_labels, quarterly_totals.values, marker='o', color='steelblue', linewidth=2)
    axes[0, 0].set_title('Total Quarterly Sales')
    axes[0, 0].set_xlabel('Quarter')
    axes[0, 0].set_ylabel('Sales ($)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, linestyle='--', alpha=0.5)

    # 2. Sales by location (bar)
    loc_sales = sales_df.groupby('Location')['Sales'].sum()
    axes[0, 1].bar(loc_sales.index, loc_sales.values, color=['steelblue', 'tomato', 'green', 'purple'])
    axes[0, 1].set_title('Total Sales by Location')
    axes[0, 1].set_xlabel('Location')
    axes[0, 1].set_ylabel('Sales ($)')
    axes[0, 1].grid(True, linestyle='--', alpha=0.4)

    # 3. Category market share (pie)
    cat_sales = sales_df.groupby('Category')['Sales'].sum()
    axes[1, 0].pie(cat_sales.values, labels=cat_sales.index, autopct='%1.1f%%', startangle=140)
    axes[1, 0].set_title('Category Market Share')

    # 4. Age distribution
    axes[1, 1].hist(customer_df['Age'], bins=20, color='steelblue', edgecolor='white')
    axes[1, 1].axvline(customer_df['Age'].mean(), color='red', linestyle='--',
                       label=f"Mean: {customer_df['Age'].mean():.1f}")
    axes[1, 1].set_title('Customer Age Distribution')
    axes[1, 1].set_xlabel('Age')
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].legend()

    plt.tight_layout()
    return fig


# Main function
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    fig1  = plot_quarterly_sales_trend()
    fig2  = plot_location_sales_comparison()
    fig3  = plot_category_performance_by_location()
    fig4  = plot_sales_composition_by_location()
    fig5  = plot_ad_spend_vs_sales()
    fig6  = plot_ad_efficiency_over_time()
    fig7  = plot_customer_age_distribution()
    fig8  = plot_purchase_by_age_group()
    fig9  = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    fig13 = create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("""
1. SALES GROWTH: Overall sales show a consistent upward trend with strong Q4 
   seasonality. Q4 consistently outperforms other quarters due to holiday demand.

2. MIAMI LEADS: Miami generates the highest revenue across all quarters due to 
   its location factor advantage. Jacksonville underperforms and may benefit from 
   targeted marketing investment.

3. ELECTRONICS DOMINATES: Electronics holds the largest category market share. 
   SunCoast should ensure adequate Electronics inventory, especially heading into Q4.

4. ADVERTISING EFFICIENCY: Sales per dollar of ad spend is relatively stable, 
   suggesting current advertising is effective. Monitor for diminishing returns 
   as ad budgets grow.

5. CUSTOMER DEMOGRAPHICS: Tampa skews older (mean ~45) while Miami is younger 
   (~35). Tailoring product mix and marketing messaging by location demographics 
   could improve conversion rates.
    """)

    plt.show()


if __name__ == "__main__":
    main()