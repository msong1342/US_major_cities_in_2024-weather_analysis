from flask import Flask, render_template, request
from module import WeatherData, populate_database, db
from weather_analysis import WeatherAnalysis

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_app.db'
db.init_app(app)

@app.route('/')
def show_results():
    """Render results with paginated weather data."""
    try:
        # Pagination parameters
        page = int(request.args.get('page', 1))  # Current page
        per_page = 100  # Rows per page
        offset = (page - 1) * per_page

        # Retrieve a subset of weather data
        weather_data = WeatherData.query.offset(offset).limit(per_page).all()
        total_rows = WeatherData.query.count()
        total_pages = (total_rows + per_page - 1) // per_page  # Calculate total pages

        # Analyze predefined CSV file for stats and visualizations
        file_path = "C:/Users/msong/OneDrive/Documents/cs3270/weather_analysis_project/weather_data.csv"
        analysis = WeatherAnalysis(file_path)
        analysis.fetch_data()
        stats = analysis.calculate_statistics()

        # Return results template with paginated data
        return render_template(
            'results.html',
            stats=stats,
            weather_data=weather_data,
            current_page=page,
            total_pages=total_pages,
            message="Analysis completed successfully!",
        )
    except Exception as e:
        return render_template('results.html', stats={}, weather_data=[], message=f"Error: {str(e)}")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        populate_database("C:/Users/msong/OneDrive/Documents/cs3270/weather_analysis_project/weather_data.csv")
    app.run(debug=True)
