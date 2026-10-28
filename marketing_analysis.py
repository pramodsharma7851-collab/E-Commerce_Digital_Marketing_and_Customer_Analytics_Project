
"""E-commerce Digital Marketing Portfolio - reproducible analysis.
Run: pip install pandas matplotlib seaborn
     python marketing_analysis.py
All included data is synthetic/demo data.
"""
import pandas as pd
import matplotlib.pyplot as plt

campaign = pd.read_csv("campaign_performance.csv", parse_dates=["date"])
orders = pd.read_csv("orders.csv", parse_dates=["order_date"])
survey = pd.read_csv("demo_survey_responses_synthetic.csv")

# Campaign-level aggregated KPIs
channel = campaign.groupby("channel").agg(
    spend=("spend_inr","sum"), impressions=("impressions","sum"),
    clicks=("clicks","sum"), sessions=("sessions","sum"),
    conversions=("orders","sum"), revenue=("revenue_inr","sum")
).reset_index()
channel["CTR"] = channel.clicks / channel.impressions
channel["CPC"] = channel.spend / channel.clicks
channel["CVR"] = channel.conversions / channel.sessions
channel["CPA"] = channel.spend / channel.conversions
channel["ROAS"] = channel.revenue / channel.spend
print("\\nCHANNEL PERFORMANCE\\n", channel.round(2).to_string(index=False))

# Delivered-order performance
delivered = orders[orders.order_status.eq("Delivered")]
print("\\nREVENUE BY ACQUISITION CHANNEL\\n",
      delivered.groupby("acquisition_channel").net_revenue_inr.sum().sort_values(ascending=False))
print("\\nCATEGORY PERFORMANCE\\n",
      delivered.groupby("category").net_revenue_inr.sum().sort_values(ascending=False))

# Survey insights
print("\\nDISCOVERY CHANNEL\\n", survey.discovery_channel.value_counts(normalize=True).mul(100).round(1))
print("\\nCART ABANDONMENT\\n", survey.cart_abandon_reason.value_counts(normalize=True).mul(100).round(1))

# Chart: ROAS by channel
ax = channel.sort_values("ROAS").plot(x="channel",y="ROAS",kind="bar",legend=False,
                                      title="Synthetic campaign ROAS by channel")
ax.set_ylabel("Revenue / ad spend")
ax.set_xlabel("")
plt.tight_layout()
plt.savefig("roas_by_channel.png",dpi=160)
plt.show()

# Chart: monthly spend and attributed revenue
campaign["month"] = campaign.date.dt.to_period("M").astype(str)
monthly = campaign.groupby("month")[["spend_inr","revenue_inr"]].sum()
monthly.plot(kind="bar",title="Monthly campaign spend vs attributed revenue")
plt.ylabel("INR")
plt.tight_layout()
plt.savefig("monthly_spend_revenue.png",dpi=160)
plt.show()

# Important: campaign-attributed revenue is a separate synthetic dataset from order-level sales.
# Do not add these two revenue measures together.
