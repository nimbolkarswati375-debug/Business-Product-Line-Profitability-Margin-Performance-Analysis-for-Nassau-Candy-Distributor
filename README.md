🍫 Nassau Candy Product Line Profitability Analysis
**Project Overview
This project analyzes the profitability of Nassau Candy's product portfolio using data analytics and visualization techniques. The objective is to identify key profit-generating products, evaluate gross margins and costs, compare division performance, analyze pricing and unit economics, and identify products requiring strategic attention.
An interactive Streamlit dashboard was developed to help stakeholders explore profitability and make data-driven product portfolio decisions.
🎯 Business Objectives
- Identify the most profitable products and product lines
- Analyze gross margin and profit per unit
- Compare profitability across divisions
- Evaluate cost-to-sales efficiency
- Identify pricing and margin risks
- Analyze profit concentration using Pareto analysis
- Identify products for retention, growth, or review
- Provide actionable recommendations to stakeholders
📊 Key Findings
- Average Gross Margin: 66.51%
- Total Gross Profit: $93,442.80
- Chocolate Division Profit Contribution: 95.06%
- Top 4 Products Profit Contribution: 77.30%
- Top 5 Core Products Profit Contribution: 95.06%
- Highest-priority margin concern: Kazookles with a 7.69% gross margin
- Key geographic markets: California and New York
The findings demonstrate strong overall profitability but also highlight significant dependence on a small number of products and the Chocolate division.
🔍 Analysis Performed
1. Product Profitability
- Product-level sales and cost analysis
- Gross profit calculation
- Gross margin analysis
- Profit-per-unit analysis
- Product profitability ranking
2. Division Performance
- Revenue comparison
- Gross profit comparison
- Margin analysis
- Profit contribution by division
3. Cost & Margin Diagnostics
- Cost vs. sales analysis
- Cost-to-sales ratio
- Margin risk identification
- Low-margin product assessment
4. Pricing Analysis
- Selling price per unit
- Cost per unit
- Profit per unit
- Pricing and margin evaluation
5. Profit Concentration
- Pareto analysis
- Cumulative profit contribution
- Top-product dependency analysis
- Identification of products contributing to 80% of profit
6. Geographic Analysis
- State-level sales performance
- State-level gross profit
- Revenue contribution by geography
📈 Streamlit Dashboard
The interactive dashboard includes:
- Executive KPI overview
- Product profitability leaderboard
- Gross margin analysis
- Profit contribution charts
- Division performance dashboard
- Cost vs. sales diagnostics
- Margin risk flags
- Pricing analysis
- Pareto profit concentration analysis
- Geographic performance
- Shipping lead-time diagnostics
- Strategic product recommendations
- Filtered dataset download
Dashboard Filters
Users can filter the analysis by:
- Order date range
- Division
- Product name
- Minimum gross margin
🛠️ Technologies Used
- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Jupyter Notebook
- Git & GitHub
📁 Project Structure
Nassau Candy Profitability/
│
├── app.py
├── requirements.txt
│
├── Nassau_Candy_Cleaned.csv
├── Product_Level_Profitability.csv
├── Division_Performance_Analysis.csv
├── Cost_Efficiency_Analysis.csv
├── Pricing_Analysis.csv
└── Strategic_Product_Recommendations.csv

⚙️ Installation & Setup
Clone the repository:
git clone <YOUR_GITHUB_REPOSITORY_URL>

Navigate to the project directory:
cd "Nassau Candy Profitability"

Create a virtual environment:
python -m venv venv

Activate the environment on Windows:
venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

▶️ Run the Streamlit Dashboard
python -m streamlit run app.py

The application will open at:
http://localhost:8501

💡 Business Recommendations
1. Protect and invest in the five core Chocolate products that generate the majority of profit.
2. Conduct a detailed cost and pricing review of low-margin products such as Kazookles.
3. Evaluate low-profit products based on growth potential and strategic importance before discontinuation.
4. Monitor dependency on the Chocolate division and diversify profitable product lines.
5. Use pricing and cost analytics regularly to identify margin deterioration.
6. Focus customer retention and growth initiatives on high-performing geographic markets.
📌 Conclusion
The analysis demonstrates that Nassau Candy has a strong profitability base, but profitability is highly concentrated among a small number of products and within the Chocolate division. The dashboard provides stakeholders with an interactive tool to monitor profitability, identify margin risks, optimize pricing and costs, and support data-driven product portfolio decisions.
👩‍💻 Author
Swati Nimbolkar
Data Analytics | Machine Learning | Business Intelligence
