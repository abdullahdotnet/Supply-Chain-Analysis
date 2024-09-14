import pandas as pd
import numpy as np
from datetime import timedelta

def update_delivery_date(row):
    # Set default days to add
    days_to_add = 0

    # Define minimum and maximum days for each shipping mode
    min_days = {
        'First Class': 2,
        'Second Class': 5,
        'Standard Class': 8
    }
    max_days = {
        'First Class': 3,   # Maximum of the range 2-3 for 'First Class'
        'Second Class': 6,  # Maximum of the range 5-6 for 'Second Class'
        'Standard Class': 11 # Maximum of the range 8-11 for 'Standard Class'
    }

    # Check market and shipping mode
    if row['market'] in ['LATAM', 'USCA']:
        # Use minimum days for specific markets
        if row['shipping_mode'] in min_days:
            days_to_add = min_days[row['shipping_mode']]
    elif row['market'] == 'Pacific Asia':
        # Use maximum days for 'Pacific Asia'
        if row['shipping_mode'] in max_days:
            days_to_add = max_days[row['shipping_mode']]
    else:
        # Randomly add days based on shipping mode
        if row['shipping_mode'] == 'First Class':
            days_to_add = np.random.randint(2, 4)
        elif row['shipping_mode'] == 'Second Class':
            days_to_add = np.random.randint(5, 7)
        elif row['shipping_mode'] == 'Standard Class':
            days_to_add = np.random.randint(8, 12)

    # Update the delivery date
    return row['delivery_date'] + timedelta(days=days_to_add)

def calculate_product_profit(df):
    # Define minimum and maximum price for scaling
    min_price = df['product_price'].min()
    max_price = df['product_price'].max()
    
    # Define initial and maximum profit percentages
    min_profit_percentage = 0.03
    max_profit_percentage = 0.30
    
    # Calculate the linear profit percentage for each price
    linear_profit_percentage = min_profit_percentage + (max_profit_percentage - min_profit_percentage) * (
        (df['product_price'] - min_price) / (max_price - min_price))
    
    # Add random fluctuation
    np.random.seed(0)  # For reproducibility
    fluctuation = np.random.uniform(-0.20, 0.20, size=df.shape[0]) # Random fluctuation between -20% and +20%
    
    # Adding randomness to product price to introduce variability in the lower values
    random_price_fluctuation = np.random.uniform(-0.05, 0.05, size=df.shape[0])
    df['product_price'] = df['product_price'] * (1 + random_price_fluctuation)
    
    # Adjust profit percentage with the added fluctuation
    df['profit_percentage'] = np.clip(linear_profit_percentage + fluctuation, min_profit_percentage, max_profit_percentage)
    
    # Calculate the profit based on the adjusted price and profit percentage
    df['product_profit'] = df['product_price'] * df['profit_percentage']
    
    # Drop the intermediate 'profit_percentage' column if not needed
    df.drop(columns=['profit_percentage'], inplace=True)
    
    return df['product_profit']



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
    df['delivery_date'] = df['order_date']
    df['delivery_date'] = df.apply(update_delivery_date, axis=1)

    temp_df = df[df['shipping_mode'] == 'Same Day']
    num_rows_to_modify = int(len(temp_df) * 0.08)
    num_rows_to_modify2 = int(len(temp_df) * 0.02)
    random_indices = np.random.choice(temp_df.index, num_rows_to_modify, replace=False)
    random_indices2 = np.random.choice(temp_df.index, num_rows_to_modify2, replace=False)
    temp_df.loc[random_indices, 'delivery_date'] += pd.Timedelta(days=1)
    temp_df.loc[random_indices2, 'delivery_date'] += pd.Timedelta(days=2)
    df.loc[df['shipping_mode'] == 'Same Day', 'delivery_date'] = temp_df['delivery_date']
    df['shipping_duration'] = (df['delivery_date'] - df['order_date']).dt.days

    df['order_weekday'] = df['order_date'].dt.day_name()

    temp_df = df[df['order_weekday'] == 'Monday']
    temp_df.iloc[:200, temp_df.columns.get_loc('order_weekday')] = 'Saturday'
    df[df['order_weekday'] == 'Monday'] = temp_df

    temp_df = df[df['order_weekday'] == 'Tuesday']
    temp_df.iloc[:200, temp_df.columns.get_loc('order_weekday')] = 'Saturday'
    df[df['order_weekday'] == 'Tuesday'] = temp_df

    temp_df = df[df['order_weekday'] == 'Wednesday']
    temp_df.iloc[:200, temp_df.columns.get_loc('order_weekday')] = 'Sunday'
    df[df['order_weekday'] == 'Wednesday'] = temp_df

    temp_df = df[df['order_weekday'] == 'Thursday']
    temp_df.iloc[:200, temp_df.columns.get_loc('order_weekday')] = 'Sunday'
    df[df['order_weekday'] == 'Thursday'] = temp_df

   

    df['product_profit'] = calculate_product_profit(df)

    return df


