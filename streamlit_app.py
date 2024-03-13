import streamlit as st
import pandas as pd
import pickle

# Function to load the model
@st.cache_data
def load_model():
    with open('rf_model', 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model

# with open('saved _model/rf_model', 'rb') as file:
#     loaded_model = pickle.load(file)

# Load your model
loaded_model = load_model()

# Function to create the input datafram
def create_input_df(user_inputs, category_map):
    data = {f'{category}_{sub_category}': 0 for category, sub_categories in category_map.items() for sub_category in sub_categories}
    data.update({'size': 0, 'total_sqft': 0, 'bath': 0})  # Initialize numeric fields
    input_df = pd.DataFrame(data, index=[0])
    
    for category, value in user_inputs.items():
        if category in ['size', 'total_sqft', 'bath']:  # Direct assignment for numeric fields
            input_df[category] = value
        else:  # One-hot encoding for categorical fields
            if value in category_map[category]:
                input_df[f'{category}_{value}'] = 1
    
    # Drop the DataFrame index to prevent unnamed columns when saving/loading
    input_df.reset_index(drop=True, inplace=True)
    input_df = input_df.reindex(columns=sorted(input_df.columns))
    return input_df


# Define your category_map
category_map = {
    'availability': ['Ready To Move', 'Future Possession'],
    'location': ['others', 'Ramamurthy Nagar', 'Hebbal', 'Bellandur', 'R.T. Nagar',
       'Attibele', 'Mahadevpura', 'Whitefield', 'Dodda Nekkundi',
       'Marathahalli', 'Uttarahalli', 'Bannerghatta Road',
       'Yelachenahalli', 'Kanakpura Road', 'Hoodi', '8th Phase JP Nagar',
       'Electronic City', 'Kalena Agrahara', 'Jakkur', 'Indira Nagar',
       'Raja Rajeshwari Nagar', 'Hegde Nagar', 'Begur Road',
       'Padmanabhanagar', 'Akshaya Nagar', 'Kundalahalli', 'Hennur Road',
       'Gottigere', 'Gunjur', 'Ulsoor', 'Bisuvanahalli', 'Rachenahalli',
       'Sarjapur  Road', 'Electronic City Phase II', 'Panathur',
       'Lakshminarayana Pura', 'Brookefield', 'Yelahanka', 'Yeshwanthpur',
       'Kengeri', 'Ambedkar Nagar', 'Hormavu', 'Sarjapur', 'Kudlu',
       'Electronics City Phase 1', 'Thanisandra', 'Sanjay nagar',
       'Thigalarapalya', 'Kothannur', 'Kothanur', 'Green Glen Layout',
       '7th Phase JP Nagar', 'KR Puram', 'Jigani', '6th Phase JP Nagar',
       'Ramagondanahalli', 'Jalahalli', 'Amruthahalli', 'Malleshwaram',
       'JP Nagar', 'Harlur', 'Kodichikkanahalli', 'Hosa Road', 'Hulimavu',
       'Munnekollal', 'Chikkalasandra', 'Kadugodi', 'Hoskote',
       'Basavangudi', 'Kudlu Gate', 'Yelahanka New Town',
       'Kaval Byrasandra', 'Margondanahalli', 'TC Palaya', 'Bommanahalli',
       'Rajaji Nagar', 'Hosakerehalli', '2nd Stage Nagarbhavi',
       'EPIP Zone', 'Kasavanhalli', 'Varthur', '9th Phase JP Nagar',
       'Haralur Road', 'Balagere', 'Horamavu Agara', 'Hebbal Kempapura',
       'Domlur', 'Kogilu', 'Tumkur Road', 'Vittasandra', 'Devanahalli',
       'HSR Layout', 'Kaggadasapura', 'Seegehalli', 'Singasandra',
       'Kumaraswami Layout', 'Sahakara Nagar', 'Subramanyapura',
       'Vidyaranyapura', 'Kengeri Satellite Town', 'Talaghattapura',
       '1st Phase JP Nagar', 'Nagarbhavi', 'Banashankari Stage III',
       'Vijayanagar', 'Kathriguppe', 'Hennur', 'Bhoganhalli',
       'Somasundara Palya', 'Anandapura', 'Kambipura', 'Hosur Road',
       'Magadi Road', 'Kammasandra', 'Banashankari', 'Mysore Road',
       'Old Madras Road', 'Babusapalaya', 'Kanakapura', 'Doddathoguru',
       'Abbigere', 'Rayasandra', 'Bommasandra', 'Old Airport Road',
       'HBR Layout', 'Gubbalala', 'Thubarahalli', 'Anekal',
       'Horamavu Banaswadi', 'BTM 2nd Stage', 'Koramangala', 'Ambalipura',
       'Iblur Village', 'Lingadheeranahalli', 'Budigere', 'Frazer Town',
       '5th Phase JP Nagar', 'Basaveshwara Nagar', 'Poorna Pragna Layout',
       'Channasandra', 'Ananth Nagar', 'Sonnenahalli', 'Chandapura',
       'Battarahalli', 'CV Raman Nagar', 'Ardendale',
       'Bommasandra Industrial Area', 'Choodasandra', 'Binny Pete']
}    

# Sidebar for navigation
st.sidebar.title('Navigation')
options = st.sidebar.selectbox('Select a page:', 
                           ['Prediction', 'Code', 'About'])

if options == 'Prediction': # Prediction page
    st.title('House Price Prediction Web App')

    # User inputs
    availability = st.selectbox('Availability', category_map['availability'])
    location = st.selectbox('Location', category_map['location'])  # Make sure this includes all options
    size = st.slider('Size', min_value=1, max_value=10, value=2)
    total_sqft = st.slider('Total Sqft', min_value=300, max_value=10000, value=1100)
    bath = st.slider('Bath', min_value=1, max_value=10, value=2)

    user_inputs = {
        'availability': availability,
        'location': location,
        'size': size,
        'total_sqft': total_sqft,
        'bath': bath
    }

    if st.button('Predict'):
        input_df = create_input_df(user_inputs, category_map)
        prediction = loaded_model.predict(input_df)
        st.markdown(f'**The predicted house price is: {prediction[0]:,.2f}**')  # Display prediction with bold
        
        with st.expander("Show more details"):
            st.write("Details of the prediction:")
            # You can include more details about the prediction
            # For example, display the parameters of the loaded model
            st.json(loaded_model.get_params())
            st.write('Model used: Random Forest Regressor')
            
elif options == 'Code':
    st.header('Code')
    # Add a button to download the Jupyter notebook (.ipynb) file
    notebook_path = 'House_Price_Prediction.ipynb'
    with open(notebook_path, "rb") as file:
        btn = st.download_button(
            label="Download Jupyter Notebook",
            data=file,
            file_name="House_Price_Prediction.ipynb",
            mime="application/x-ipynb+json"
        )
    st.write('You can download the Jupyter notebook to view the code and the model building process.')
    st.write('--'*50)

    st.header('Data')
    # Add a button to download your dataset
    data_path = 'Bengaluru_House_Data.csv'
    with open(data_path, "rb") as file:
        btn = st.download_button(
            label="Download Dataset",
            data=file,
            file_name="Bengaluru_House_Data.csv",
            mime="text/csv"
        )
    st.write('You can download the dataset to use it for your own analysis or model building.')
    st.write('--'*50)

    st.header('GitHub Repository')
    st.write('You can view the code and the dataset used in this web app from the GitHub repository:')
    st.write('[GitHub Repository](https://github.com/gokulnpc)')
    st.write('--'*50)

    st.header('Google Colab')
    st.write('You can view the code and the model building process in a Google Colab notebook:')
    st.write('[Google Colab](https://colab.research.google.com/drive/1brfnxPsjH4GSY3RL1RG_UvZiCCLL-xJ3?usp=sharing)')
    
elif options == 'About':
    st.title('About')
    st.write('This web app is a simple house price prediction tool. It uses a Random Forest model to predict the price of a house in Bengaluru, India. The model was trained on a dataset from Kaggle. The web app is built using Streamlit, a popular Python library for building web apps.')

    st.write('The model was trained using the following features:')
    st.write('- Availability: Ready To Move, Future Possession')
    st.write('- Location: 130 different locations in Bengaluru')
    st.write('- Size: Number of bedrooms')
    st.write('- Total Sqft: Total square feet area of the house')
    st.write('- Bath: Number of bathrooms')

    st.write('The web app is open-source. You can view the code and the dataset used in this web app from the GitHub repository:')
    st.write('[GitHub Repository](https://github.com/gokulnpc)')
    st.write('--'*50)
