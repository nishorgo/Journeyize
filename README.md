# Journeyize: Your Ultimate Travel Companion

Journeyize is a Django web application that helps you plan your travel itinerary based on weather conditions, recommends famous local foods, and allows you to save and edit your itinerary seamlessly. It leverages various APIs and modern frontend technologies to make your journey planning a breeze.

## Features

### 1. Weather-Based Itinerary Generation

Journeyize uses the OpenWeather API to fetch real-time weather data for your chosen travel destination. It ensures your plans align with the weather conditions, so you can make the most of your trip without unexpected surprises.

### 2. Local Food Recommendations

Discover the culinary delights of your destination! Journeyize suggests famous local foods and restaurants to satisfy your taste buds.

### 3. Itinerary Management

Create, save, and edit your travel itinerary. Journeyize provides a user-friendly interface to manage your plans effortlessly.

### 4. Tailwind CSS Frontend

The frontend of Journeyize is built using Tailwind CSS, a highly customizable CSS framework, to ensure a sleek and responsive user experience.

## Technologies Used

- Django: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- Tailwind CSS: A utility-first CSS framework for rapidly building custom user interfaces.
- Google Places API: Provides detailed information about places, including geographic locations, photos, and more.
- OpenWeather API: Offers current weather, forecasts, and historical weather data.
- OpenAI Generative AI: Used for generating intelligent and context-aware suggestions.

## Getting Started

Follow these steps to get Journeyize up and running on your local machine:

### Prerequisites

- Python 3.11
- Pipenv
- openai
- OpenWeather API Key (Get it [here](https://openweathermap.org/api))
- Google Places API Key (Get it [here](https://cloud.google.com/maps-platform/places))
- OpenAI API Key (For generative AI, get it [here](https://beta.openai.com/signup/))

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/nishorgo/Journeyize.git
   cd Journeyize
   ```

2. Install the project dependencies using Pipenv:

   ```bash
   pipenv install
   ```

3. Create a `.env` file in the project's root directory and add your API keys:

   ```plaintext
   OPENWEATHER_API_KEY=your_openweather_api_key
   GOOGLE_MAPS_API_KEY=your_google_places_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Activate the virtual environment:

   ```bash
   pipenv shell
   ```

5. Run database migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Access the application in your web browser at `http://localhost:8000`.

## Contributing

Contributions are welcome! If you have ideas for improvements or new features, please open an issue or submit a pull request. For major changes, please discuss them in advance.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
