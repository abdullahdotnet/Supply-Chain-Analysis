import pandas as pd



def preprocess():
    df = pd.read_csv('../data.csv')
    drop = df[df['customer_state'] == '91732'].index
    df.drop(drop)
    df['order_date'] = pd.to_datetime(df['order_date'], utc=True)

    df = df.dropna(subset=['order_date'])

    df['order_date'] = df['order_date'].dt.tz_localize(None)


    state_mapping = {
        'PR': 'Puerto Rico', 'CA': 'California', 'KY': 'Kentucky', 'NJ': 'New Jersey', 'AZ': 'Arizona', 
        'PA': 'Pennsylvania', 'NY': 'New York', 'OH': 'Ohio', 'CO': 'Colorado', 'MT': 'Montana', 
        'WI': 'Wisconsin', 'IL': 'Illinois', 'DC': 'District of Columbia', 'CT': 'Connecticut', 
        'WV': 'West Virginia', 'UT': 'Utah', 'FL': 'Florida', 'TX': 'Texas', 'MI': 'Michigan', 
        'NM': 'New Mexico', 'NV': 'Nevada', 'WA': 'Washington', 'NC': 'North Carolina', 'GA': 'Georgia', 
        'MD': 'Maryland', 'SC': 'South Carolina', 'TN': 'Tennessee', 'IN': 'Indiana', 'MO': 'Missouri', 
        'MN': 'Minnesota', 'OR': 'Oregon', 'VA': 'Virginia', 'MA': 'Massachusetts', 'HI': 'Hawaii', 
        'RI': 'Rhode Island', 'DE': 'Delaware', 'ID': 'Idaho', 'LA': 'Louisiana', 'ND': 'North Dakota', 
        'KS': 'Kansas', 'IA': 'Iowa', 'OK': 'Oklahoma', 'AL': 'Alabama'
    }


    df['customer_state'] = df['customer_state'].map(state_mapping)
    return df


