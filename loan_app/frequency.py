# Define the frequency ranges and transaction types dynamically
frequency_ranges = {
    'Send Money': {
        'Send Money_1': (10, 500),
        'Send Money_2': (501, 3000),
        'Send Money_3': (3001, 25000)
    },
    'Received Money': {
        'Received Money_1': (10, 500),
        'Received Money_2': (501, 3000),
        'Received Money_3': (3001, 25000)
    },
    'Cash In': {
        'Cash In_1': (10, 500),
        'Cash In_2': (501, 3000),
        'Cash In_3': (3001, 30000)
    },
    'Cash Out': {
        'Cash Out_1': (50, 500),
        'Cash Out_2': (501, 3000),
        'Cash Out_3': (3001, 25000)
    },
    'Make_Payment': {
        'Make Payment_1': (1, 500),
        'Make Payment_2': (501, 3000),
        'Make Payment_3': (3001, 300000)
    },

    'Pay_Bill': {
      'Pay Bill_1': (1, 2000),
      'Pay Bill_2': (2001, 300000)
    },

    'Add_Money': {
      'Add Money_1': (50, 500),
      'Add Money_2': (501, 3000),
      'Add Money_3': (3001, 50000)
    },

    'Fund_Transfer': {
      'Fund Transfer_1': (10, 500),
      'Fund Transfer_2': (501, 3000),
      'Fund Transfer_3': (3001, 50000)
    },

    'Request Money': {
      'Request Money': (10, 25000)
    },

    'Remittance': {
      'Remittance_1': (1, 10000),
      'Remittance_2': (10001, 125000)
    },

    'Donation': {
      'Donation_1': (10, 1500),
      'Donation_2': (1501, 300000)
    },

    'Others': {
      'Others_1': (1, 1500),
      'Others_2': (1501, 3000),
      'Others_3': (3001, 300000)
    },

}