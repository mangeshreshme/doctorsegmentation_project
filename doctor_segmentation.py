# 1 Reading the Dataset
import pandas as pd
from fontTools.misc.arrayTools import intRect

df = pd.read_csv("Data/doctor_sales_data.csv")
print(df.head(5))
print(df.columns)

# 2 converting 'Last_Visit_Date' to datetime Format.
df['Last_Visit_Date'] = pd.to_datetime(df['Last_Visit_Date'])

# setting refrence date for recency calculation
ref_date = df['Last_Visit_Date'].max()+pd.Timedelta(days=1)

# 3 calculating Recency,from last visit
df['Recency'] = (ref_date-df['Last_Visit_Date']).dt.days

# 4renaming frequency and colums for verify
df.rename(columns={'Frequency':'Frequency_Rx','Value':'Monetary'},inplace=True)

# 5 Selecting final RFM columns
RFM_df = df[["Doctor_ID","Recency","Frequency_Rx","Monetary"]]
print(RFM_df.head())
print(RFM_df.describe())


# 6 converting strigs to numric in Monetary columns
df['Monetary'] = pd.to_numeric(df["Monetary"],errors='coerce')

# 7 RFM emty scoaring columns
df['R_Score']=0
df['F_Score']=0
df['M_Score']=0

# 8 Assining Recency score(R_Score)
df['R_Score'] = pd.qcut(df['Recency'],q=5,labels=[5,4,3,2,1])

# 9 Assining Frequency score(F_Score)
def get_freq_score(freq):
    if freq == 'Weekly':
        return 5
    elif freq=='Biweekly':
        return 4
    elif freq=='Monthly':
        return 3
    elif freq=='Quaterly':
        return 2
    else:
        return 1
df["F_Score"] = df["Frequency_Rx"].apply(get_freq_score)

# assining Monetary score (M_score)
def get_monetary_score(value):
    if value>=20000:
        return 5
    elif value>=15000:
        return 5
    elif value>=10000:
        return 5
    elif value>=5000:
        return 5
    else:
        return 1
df['M_Score']=df['Monetary'].apply(get_monetary_score)

# combining RFM score
df['RFM_score'] = (df['R_Score'].astype(str)+
                   df['F_Score'].astype(str)+
                   df['M_Score'].astype(str))

# final RFM score
print(df[['Doctor_ID','Recency','Frequency_Rx','Monetary',
          'R_Score','F_Score','M_Score','RFM_score']])
# print(df['R_Score'])
def segment_doctor(row):
    r=int(row["R_Score"])
    f=int(row["F_Score"])
    m=int(row["M_Score"])

    if r == 5 and f>4 and m>4:
        return "Champion"
    elif r>=4 and f>=3:
        return "Loyal Doctor"
    elif r==5:
        return "Frequent Visitor"
    elif m==5:
        return "High Spenders"
    elif r<=2 and f<=2 and m<=2:
        return "Lost"
    else:
        return "Need Attention"

df["Segment"]=df.apply(segment_doctor,axis=1)

print(df[['Doctor_ID','Recency','Frequency_Rx','Monetary',
          'R_Score','F_Score','M_Score','RFM_score','Segment']])

# counting of Segment colunms
segment_counts = df['Segment'].value_counts()
print("\n Segment Distribution:\n",segment_counts)

# visualization of segment destibution using pie chart

import matplotlib.pyplot as plt

segment_counts.plot.pie(autopct='%1.1f%%',startangle=140)
plt.title("Doctor Segment Distribution")
plt.ylabel('')
plt.show()
plt.savefig("pie chart")

df.to_csv('Segmented_doctor.csv',index=False)


