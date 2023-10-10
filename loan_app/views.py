import csv
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import WalletInfo 
import pandas as pd
import joblib
from .frequency import frequency_ranges
from .constant import addresses,occupations
from django.http import HttpResponse
from django.contrib import messages
    
# Load the pre-trained decision tree model
Upay_Loan_System_model = joblib.load('Models/Upay_Loan_System_model.pkl')

# def upload_csv_customer_info(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#         # Read CSV data in text mode
#         csv_reader = csv.DictReader(TextIOWrapper(csv_file, encoding='utf-8'))

#         predictions_with_wallet = []  # A list to temporarily store the data
#          # Initialize label encoders for categorical features
#         address_encoder = LabelEncoder()
#         gender_encoder = LabelEncoder()

#         addresses = []
#         genders = []

#         for row in csv_reader:
#             address = row.get('Address')
#             gender = row.get('Gender')

#             addresses.append(address)
#             genders.append(gender)

#         address_encoder.fit(addresses)
#         gender_encoder.fit(genders)
#         # Rewind the CSV file to read it again
#         csv_file.seek(0)
#         # Skip the header row
#         next(csv_reader)

#         for row in csv_reader:
#             # Extract relevant fields from the CSV data
#             name = row.get('Name')
#             wallet_no = row.get('Wallet No')
#             address = row.get('Address')
#             gender = row.get('Gender')
#             balance = float(row.get('Balance'))
#             age = int(row.get('Age'))
#              # Encode categorical features
#             encoded_address = address_encoder.transform([address])[0]
#             encoded_gender = gender_encoder.transform([gender])[0]

#             # Prepare features for prediction
#             features = [[encoded_address, encoded_gender, balance, age]]
#             predictions = decision_tree_model.predict(features)
#             predictions_with_wallet.append({'name': name,'wallet_no': wallet_no, 'prediction': predictions[0]})
            
#         return render(request, 'result.html', {'predictions_with_wallet': predictions_with_wallet}) 
       
#     return render(request, 'upload_csv.html')



def upload_csv_customer_info(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        if csv_file.name.endswith('.csv'):
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:
                WalletInfo.objects.create(
                    name=row['Name'],
                    wallet_no=row['Wallet No'],
                    address=row['Address'],
                    gender=row['Gender'],
                    balance=row['Balance'],
                    age=row['Age'],
                    occupation=row['Occupation']
                )

            messages.success(request, f'Customer Information File has been uploaded successfully!')
            return redirect('upload_csv')    
    return render(request, 'upload_csv.html')


def home(request):
    return render(request, 'home.html')


def transaction_history_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        if csv_file.name.endswith('.csv'):
            # Read the uploaded CSV file into a Pandas DataFrame
            uploaded_file = request.FILES['csv_file']
            transaction_history_df = pd.read_csv(uploaded_file)
            request.session['transaction_history_df'] = transaction_history_df.to_json()
            return redirect('calculate_transaction_frequencies')
    
    # If the request method is not POST or the file doesn't end with '.csv', return an error response
    return HttpResponse("Invalid request or file format", status=400)



def calculate_transaction_frequencies(request):
    transaction_history_df_json = request.session.get('transaction_history_df')

    if transaction_history_df_json is None:
         return HttpResponse("transaction history data not found", status=400)
    
    transaction_history_df = pd.read_json(transaction_history_df_json)

    # Define a function to calculate the coefficient of variation

    def coefficient_of_variation(data):
        if len(data) < 2:
            return 0
        mean_balance = data['Balance'].mean()
        data['Mean Balance'] = data['Balance'].mean()
        std_balance = data['Balance'].std()
        return (std_balance / mean_balance) * 100
    
    mean_balance_dict = {}

# Iterate over the DataFrame and calculate the mean balance for each wallet number
    for wallet_no, balances in transaction_history_df.groupby('Wallet No')['Balance']:
        mean_balance = balances.mean()
        mean_balance_dict[wallet_no] = mean_balance

    # print(mean_balance_dict)
    # Calculate the coefficient of variation for each wallet's balances
    cv_df = transaction_history_df.groupby('Wallet No').apply(coefficient_of_variation).reset_index(name='Balance Deviation (CV)')

    # Iterate through each transaction type and count transactions within the specified ranges
    for transaction_type, ranges in frequency_ranges.items():
        if transaction_type == 'Others':
            # Check for specific transaction types and count them within the 'Others' ranges
            for range_name, (min_amount, max_amount) in ranges.items():
                cv_df[range_name] = 0
                for wallet_no, group in transaction_history_df.groupby('Wallet No'):
                    # print(cv_df)
                    transaction_count = ((group['Transaction Type'].isin(['Land Tax', 'E-Porcha', 'DNCC Holding Tax', 'E-Mutation'])) & (group['Amount'] >= min_amount) & (group['Amount'] <= max_amount)).sum()
                    cv_df.loc[cv_df['Wallet No'] == wallet_no, range_name] = transaction_count
        else:
            # For other transaction types, count transactions based on the transaction type
            for range_name, (min_amount, max_amount) in ranges.items():
                cv_df[range_name] = 0
                for wallet_no, group in transaction_history_df.groupby('Wallet No'):                    
                    transaction_count = ((group['Transaction Type'] == transaction_type) & (group['Amount'] >= min_amount) & (group['Amount'] <= max_amount)).sum()
                    cv_df.loc[cv_df['Wallet No'] == wallet_no, range_name] = transaction_count
       
    # Convert the frequency columns to integer format
    cv_df = cv_df.fillna(0).astype({'Wallet No': int}).reset_index(drop=True)

    customer_info_queryset = WalletInfo.objects.all()
    # Convert the queryset to a DataFrame
    customer_info_df = pd.DataFrame.from_records(customer_info_queryset.values())
    customer_info_df = customer_info_df.rename(columns={'wallet_no': 'Wallet No'})

    # Perform the merge operation based on the 'Wallet No' column
    merged_df = pd.merge(customer_info_df, cv_df, on='Wallet No', how='inner')
    

    # Replace values with keys
    merged_df['address'].replace(addresses, inplace=True)
    merged_df['occupation'].replace(occupations, inplace=True)
    
    columns_to_drop = ["id","name", "gender", "Wallet No"]
    wallet_no_list = merged_df['Wallet No'].tolist()
    name_list = merged_df['name'].tolist()
    X = merged_df.drop(columns = columns_to_drop, axis=1)

    predictions_with_wallet = []
    for index, row in X.iterrows():
        row[1] = float(row[1])
        row_entry = list(row)
        row_entry = [row_entry]

        # Get probability predictions for each class
        probability_predictions = Upay_Loan_System_model.predict_proba(row_entry)
        percentage_predictions = [f"{prob * 100:.2f}%" for prob in probability_predictions[0]]
        max_value, max_index = max((value, index) for index, value in enumerate(percentage_predictions))

        if max_index == 0:
            if wallet_no_list[index] in mean_balance_dict:
                if 0 <= mean_balance_dict[wallet_no_list[index]] <= 5000: 
                    pack_value = '1000 tk'
                    pack_type = 'Type C'
                elif 5001 <= mean_balance_dict[wallet_no_list[index]] <= 20000: 
                    pack_value = '5000 tk'
                    pack_type = 'Type B'
                else:
                    pack_value = '10000 tk'
                    pack_type = 'Type A'

        else:
            pack_value = '-'
            pack_type = 'Not Applicable'



        predictions_with_wallet.append({'wallet_no': wallet_no_list[index], 'name': name_list[index], 'max_pecentage': max_value, 'status':max_index, 'Eligibility': percentage_predictions[0], 'Non_Eligibility': percentage_predictions[1], 'Under_Consideration': percentage_predictions[2], 'Package_Amount': pack_value, 'Package_Type': pack_type,})
        # # Convert the probability predictions to a percentage format
        
    # print(predictions_with_wallet)
    
    # predictions_with_wallet = predictions_with_wallet.to_dict(orient='records')
    
    
    return render(request, 'transaction_frequencies.html', {'merged_data': predictions_with_wallet})
