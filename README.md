# 🏭 End-to-End Supply Chain Simulation

## 1️⃣ Project Overview
This project simulates and analyses an end-to-end supply chain network from suppliers to retailers.  
It models the flow of goods, costs, and demand across multiple nodes (suppliers ➜ factories ➜ warehouses ➜ retailers),  
with the goal of building a realistic dataset that can be used for:

- Demand forecasting (Machine Learning)
- Inventory and logistics optimisation
- Cost-to-serve and risk scenario simulation
- Interactive “what-if” analytics dashboard

---

## 2️⃣ Environment Setup
**Python version:** 3.11.9  
**Conda environment:** `supplychain`

All commands should be executed inside the project folder:  
`D:\Project\End-To-End Supply Chain Simulation`

### 🧩 Create environment
```bash
conda create -n supplychain python=3.11.9
conda activate supplychain
pip install -r requirements.txt
📂 Folder Structure
graphql
Copy code
End-To-End Supply Chain Simulation/
│
├── data/
│   ├── raw/              # Base CSVs and manual inputs
│   └── processed/        # Generated and cleaned datasets
│
├── notebooks/            # Prototypes and analysis notebooks
│   ├── 02_rule_prototype.ipynb
│   └── 03_network_prototype.ipynb
│
├── src/
│   └── data/
│       └── generate_synthetic.py   # Script to generate synthetic demand dataset
│
├── reports/              # Outputs (figures, results, summaries)
│
├── config.yaml           # Central configuration file
├── README.md
├── .gitignore
└── .pre-commit-config.yaml
3️⃣ Current Progress
✅ Step 1 – Project Initialization
Created project skeleton under D:\Project\End-To-End Supply Chain Simulation

Set up folders (data/raw, src, etc.)

Added .gitignore and README.md

✅ Step 2 – Base Dataset Setup
Created 7 base CSVs with headers:

suppliers.csv, factories.csv, warehouses.csv,
retailers.csv, lanes.csv, demands.csv, inventory_init.csv

Each file includes small sample rows for structure testing.

✅ Step 3 – Synthetic Data Generation Script
Developed a Python script (src/data/generate_synthetic.py) to automatically generate realistic demand data.

The script uses configuration parameters from config.yaml:

Seasonal variation, yearly trend, promotion uplift, random noise, and base demand range.

Produces dataset:
data/processed/demand_simulated.csv (~936 rows)

Each record represents demand per week per retailer per SKU.

Example columns:

objectivec
Copy code
retailer_id, sku_id, week, demand_units
RET_1, SKU_1, 1, 123.45
RET_1, SKU_1, 2, 98.67
...
▶️ Run script

bash
Copy code
python src/data/generate_synthetic.py
Output:

bash
Copy code
✅ Demand simulation dataset saved to data/processed/demand_simulated.csv
✅ Step 4 – Supply Chain Network Generation
Built the core network connecting all supply chain nodes:
Suppliers → Factories → Warehouses → Retailers

Implemented using 03_network_prototype.ipynb.

Logic includes automatic lane creation with realistic parameters:

base_lead_days from supplier/factory configuration

Randomized transport_cost_per_unit based on cost range

Region-based retailer mapping to primary warehouses

Generated outputs:

data/processed/nodes_master.csv

data/processed/lanes_generated.csv

Verified lane connectivity:

yaml
Copy code
SF lanes: 2
FW lanes: 2
WR lanes: 2
✅ Saved nodes_master.csv and lanes_generated.csv
🔮 Next Step
Step 5 – Logistics Simulation & What-If Scenarios
Use the generated network and demand data to simulate product flows.

Apply random reliability noise to compute realized lead times and on-time delivery %.

Output shipment-level data for further KPI and forecasting analysis.