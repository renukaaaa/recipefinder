from streamlit_option_menu import option_menu
import requests
import streamlit as st
with st.sidebar:
    selected = option_menu(
        menu_title="Recipe Finder",  # required
        options=["Home", "App"],  # required
        menu_icon="cast",  # optional
        default_index=0,  # optional
            styles={
                "container": {"padding": "10" ,"background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",

                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )

if selected == "Home":
    import streamlit as st  # pip install streamlit

    from streamlit_lottie import st_lottie  # pip install streamlit-lottie


    def header(url):
        st.markdown(f'<p style="background-color:none;color:green;font-size:45px;width:100%;align:centre;">{url}</p>',
                    unsafe_allow_html=True)


    header('Recipe Finder ')


    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


    lottie_hello = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_ysas4vcp.json")

    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        width=200,
    )

    st.write("It is an app where you can can find recipes based on the ingredients,meal type and diet.")




if selected == "App":
    import requests
    import streamlit as st
    from PIL import Image
    import config

    api_id = 'a6ecdfa9'
    api_key = '2bc312f48448207959f8b0d99f6487a6'
    import streamlit as st  # pip install streamlit

    from streamlit_lottie import st_lottie  # pip install streamlit-lottie




    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


    lottie_hello = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_qX4zwY.json")

    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        width=200,
    )


    # Function to make API request and retrieve recipe results
    def get_recipe_results(ingredients, meal_type=None, diet_type=None):
        # Join the ingredients with 'AND' for the API query
        query = ' AND '.join(ingredients)

        # Add meal type and diet type to the query if provided
        if meal_type:
            query += f'&mealType={meal_type}'
        if diet_type:
            query += f'&diet={diet_type}'

        # Make the API request
        url = f'https://api.edamam.com/api/recipes/v2?type=public&q={query}&app_id={api_id}&app_key={api_key}'
        response = requests.get(url)

        # Process the response
        if response.status_code == 200:
            data = response.json()
            hits = data['hits']
            return hits
        else:
            return None


    # Streamlit app
    def main():
        st.title('Recipe Search')

        # User input for ingredients
        ingredients_input = st.text_input('Enter ingredients (comma-separated):')

        # Meal type selection
        meal_types = ['Any', 'Breakfast', 'Lunch', 'Dinner', 'Snack', 'Teatime']
        selected_meal = st.selectbox('Select meal type:', meal_types)

        # Diet type selection
        diet_types = ['Any', 'Vegetarian', 'Vegan', 'Gluten Free', 'Ketogenic', 'Paleo']
        selected_diet = st.selectbox('Select diet type:', diet_types)

        if st.button('Search'):
            # Split the input into a list of ingredients
            ingredients_list = [ingredient.strip() for ingredient in ingredients_input.split(',')]

            # Get the selected meal type
            meal_type = None if selected_meal == 'Any' else selected_meal.lower()

            # Get the selected diet type
            diet_type = None if selected_diet == 'Any' else selected_diet.lower()

            # Get recipe results
            recipe_results = get_recipe_results(ingredients_list, meal_type, diet_type)

            if recipe_results:
                # Display recipe information
                for hit in recipe_results:
                    recipe = hit['recipe']
                    title = recipe['label']
                    ingredients = recipe['ingredientLines']
                    instructions = recipe['url']
                    image_url = recipe['image']

                    st.subheader(title)
                    st.write('Ingredients:', ingredients)
                    st.write('Instructions:', instructions)

                    # Display image
                    image = Image.open(requests.get(image_url, stream=True).raw)
                    st.image(image)

                    st.write('---')
            else:
                st.write('Error: Failed to retrieve recipe results.')


    if __name__ == '__main__':
        main()


