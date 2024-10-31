# FitQ

FitQ is a wellness tracking application designed to help users monitor and improve their fitness and health habits by tracking various metrics such as workout duration, food intake, sleep patterns, and lifestyle choices.

## Features

- **Workout Tracking**: Log daily workouts and track duration.
- **Nutrition Monitoring**: Categorize and track food types consumed (healthy vs. junk).
- **Sleep Tracking**: Monitor sleep duration and patterns through heatmaps.
- **Lifestyle Insights**: Track alcohol consumption and smoking habits.
- **Data Visualization**: Interactive charts and graphs to visualize progress and trends.

## Demo

![FitQ Demo](link-to-your-demo-image.gif) *(Optional: You can provide a demo image or link to a live demo here)*

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Django
- Highcharts (for data visualization)
- A database (SQLite is recommended for development)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/FitQ.git
    cd FitQ
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6. **Access the app:**
    Open your web browser and navigate to `http://127.0.0.1:8000`.

## Usage

### User Registration and Login

- Navigate to the registration page.
- Fill out the required fields to create a new account.
- Log in with your credentials to access the dashboard.

### Tracking Workouts

- Go to the **Workout** section to log your workout duration by day.
- Select the type of workout and specify the duration.

### Monitoring Nutrition

- In the **Nutrition** section, categorize your food intake as "Healthy" or "Junk."
- Review your food distribution on the dashboard pie chart.

### Analyzing Sleep Patterns

- Log your sleep hours daily.
- View your sleep data in the heatmap for a visual representation of your sleep habits.

### Lifestyle Tracking

- Record your alcohol consumption and smoking habits.
- Analyze your lifestyle choices through dedicated charts.

## Data Visualization

FitQ uses Highcharts to display user data visually. Each chart offers insights into specific health metrics:

1. **Workout Duration Chart**: A column chart that shows workout durations by day.
2. **Food Type Distribution**: A pie chart illustrating the balance between healthy and junk food.
3. **Sleep Duration Heatmap**: Visual representation of sleep duration across days.
4. **Alcohol Consumption Donut Chart**: A donut chart showing the distribution of alcohol consumption.
5. **Smoking Habits Radar Chart**: A radar chart representing different smoking habits.

## Contributing

We welcome contributions to FitQ! If you'd like to contribute, please follow these steps:

1. **Fork the repository**.
2. Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature
    ```

3. Make your changes and commit them:
    ```bash
    git commit -m "Add a new feature"
    ```

4. Push your branch:
    ```bash
    git push origin feature/your-feature
    ```

5. Open a pull request detailing your changes and the motivation behind them.

## License

FitQ is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions or support, please reach out to us at [your-email@example.com](mailto:your-email@example.com).
