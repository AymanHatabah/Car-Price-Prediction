import pandas as pd

def optimize_memory(df):
    """
    Optimizes the memory usage of a pandas DataFrame by downcasting numeric
    columns and converting low-cardinality object columns to category dtype.
    """
    start_mem = df.memory_usage(deep=True).sum() / 1024**2

    for col in df.columns:
        col_type = df[col].dtype

        if pd.api.types.is_numeric_dtype(col_type):
            if pd.api.types.is_integer_dtype(col_type):
                df[col] = pd.to_numeric(df[col], downcast='integer')
            elif pd.api.types.is_float_dtype(col_type):
                df[col] = pd.to_numeric(df[col], downcast='float')

        elif pd.api.types.is_object_dtype(col_type):
            num_unique_values = len(df[col].unique())
            num_total_values = len(df[col])

            if num_unique_values / num_total_values < 0.5:
                df[col] = df[col].astype('category')

    end_mem = df.memory_usage(deep=True).sum() / 1024**2
    reduction = 100 * (start_mem - end_mem) / start_mem

    print(f"Memory decreased from {start_mem:.2f} MB to {end_mem:.2f} MB ({reduction:.1f}% reduction).")

    return df


def describe_with_whisker(df):
    """
    Extends the standard pandas describe() to include IQR and outlier whisker boundaries.
    
     """
    own_describe = df.describe(include='all')
    own_describe.loc['IQR'] = own_describe.loc['75%'] - own_describe.loc['25%']
    own_describe.loc['1.5IQR'] = 1.5 * own_describe.loc['IQR']
    own_describe.loc['max_whisker'] = own_describe.loc['75%'] + own_describe.loc['1.5IQR']
    own_describe.loc['min_whisker'] = own_describe.loc['25%'] - own_describe.loc['1.5IQR']
    
    return own_describe



from pydantic import BaseModel, Field, ValidationError
import pandas as pd

# ==========================================
# 1. Validation Schema: The Car Input Rules
# ==========================================
class CarInput(BaseModel):
    # Numeric validations
    car_age: int = Field(ge=0, description="Car age cannot be negative. 0 means brand new.")
    km_driven: float = Field(ge=0, description="Kilometers driven must be zero or positive.")
    
    # Categorical fields with smart defaults
    brand: str = 'Unknown'
    fuel: str = 'Unknown'
    seller_type: str = 'Unknown'
    transmission: str = 'Unknown'
    owner: str = 'Unknown'
    model: str = 'Unknown'
    
    class Config:
        # Allow extra columns to pass (the FeatureAligner will drop them later)
        extra = "allow"
# ==========================================
# 2. Validation Function: The Inspector
# ==========================================
def validate_car_data(df):
    """
    This function checks the dataframe row by row against Pydantic rules.
    It keeps the good rows and removes the bad ones.
    """
    valid_rows = []
    error_count = 0
    
    # Loop through each row in the dataframe
    for index, row in df.iterrows():
        try:
            # Try to validate the row using the CarInput rules
            valid_record = CarInput(**row.to_dict())
            
            # If successful, save the clean row
            valid_rows.append(valid_record.model_dump()) # model_dump() replaces dict() in Pydantic v2
            
        except ValidationError as e:
            # If the row breaks the rules, count the error and ignore the row
            error_count += 1
            
            # Print only the first two errors as examples
            if error_count <= 2:
                print(f"❌ Row {index} failed because:\n {e}\n")
                
    print(f"✅ Accepted {len(valid_rows)} clean rows.")
    if error_count > 0:
        print(f"⛔ Rejected {error_count} bad rows.")
        
    # Return a new dataframe containing only the clean rows
    return pd.DataFrame(valid_rows)        