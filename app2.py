from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function for fetching data related to C Programming courses
def get_data_c(url, title_class, spans_class):
    r = requests.get(url)
    htmlContent = r.content

    soup = BeautifulSoup(htmlContent, 'html.parser')

    title = soup.title
    spans = soup.find_all("span", class_=spans_class)
    title_info = soup.find("div", class_=title_class)

    if url == "https://onlinecourses.swayam2.ac.in/cec24_cs05/preview":
        url_1 = "https://onlinecourses.swayam2.ac.in/cec24_cs05/preview"
        s = requests.get(url_1)
        htmlContent_2 = s.content
        soup_2 = BeautifulSoup(htmlContent_2, 'html.parser')
        spans_2 = soup_2.find("div", class_="learnerEnrolled")
        return {
            "title": title.text if title else "",
            "spans": [span.get_text() for span in spans],
            "title_info": title_info.get_text() if title_info else "",
            "learner_enrolled": spans_2.get_text() if spans_2 else "",
        }
    else:
        return {
            "title": title.text if title else "",
            "spans": [span.get_text() for span in spans],
            "title_info": title_info.get_text() if title_info else "",
            "learner_enrolled": "",
        }

# Function for fetching data related to CPP Programming courses
def get_data_cpp(url, spans_class):
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')


    title = soup.title
    spans_1 = soup.find_all("span", class_=spans_class)

    return {
        'title': title.text if title else "",
        'spans': [span.get_text() for span in spans_1]
    }

# Function for fetching data related to FullStack Web Dev courses
def get_data_web(url, spans_class):
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')


    title = soup.title
    spans_1 = soup.find_all("span", class_=spans_class)

    return {
        'title': title.text if title else "",
        'spans': [span.get_text() for span in spans_1]
    }


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET'])
def search_results():
    query = request.args.get('query')

    # Perform the search or redirect to home if no query
    if query:
        if query.lower() == 'c programming':
            return redirect(url_for('index'))
        elif query.lower() == 'cpp programming':
            return redirect(url_for('index_2'))
        elif query.lower() == 'FullStack Web Dev':
            return redirect(url_for('index_3'))
        else:
            # Handle other search queries or redirect to home
            return render_template('home.html')

    return render_template('home.html')

@app.route('/index')
def index():
    # Fetch data for C Programming courses
    udemy_1 = get_data_c("https://www.udemy.com/course/c-programming-for-beginners-programming-in-c/", "ud-component--title-with-price--clp", "ud-sr-only")
    udemy_2 = get_data_c("https://www.udemy.com/course/c-programming-for-beginners-/", "ud-component--title-with-price--clp", "ud-sr-only")
    coursera_1 = get_data_c("https://www.coursera.org/specializations/coding-for-everyone", "css-lt1dx1", "sr-only")
    coursera_2 = get_data_c("https://www.coursera.org/specializations/c-programming", "css-lt1dx1", "sr-only")
    swayam = get_data_c("https://onlinecourses.swayam2.ac.in/cec24_cs05/preview", "instructorName", "learnerEnrolled")

    return render_template('index.html', udemy_1=udemy_1, udemy_2=udemy_2, coursera_1=coursera_1, coursera_2=coursera_2, swayam=swayam)

@app.route('/index_2')
def index_2():
    # Fetch data for CPP Programming courses
    udemy_1 = get_data_cpp("https://www.udemy.com/course/cpp-programming-from-scratch-to-advanced/", "ud-sr-only")
    udemy_2 = get_data_cpp("https://www.udemy.com/course/learn-cpp-programming-beginner-to-advanced/", "ud-sr-only")
    coursera = get_data_cpp("https://www.coursera.org/specializations/hands-on-cpp", "css-lt1dx1")
    codecademy = get_data_cpp("https://www.codecademy.com/learn/learn-c-plus-plus", "gamut-ewoanq-StyledText e8i0p5k0")

    return render_template('index_2.html', udemy_1=udemy_1, udemy_2=udemy_2, coursera=coursera, codecademy=codecademy)

@app.route('/index_3')
def index_3():
    # Fetch data for FullStack Web Dev courses
    udemy_1 = get_data_web("https://www.udemy.com/course/the-complete-web-development-bootcamp/", "ud-sr-only")
    udemy_2 = get_data_web("https://www.udemy.com/course/fullstack-web-development-course-projects-base/", "ud-sr-only")
    coursera = get_data_web("https://www.coursera.org/professional-certificates/ibm-full-stack-cloud-developer", "css-lt1dx1")
    codecademy = get_data_web("https://www.codecademy.com/learn/paths/full-stack-engineer-career-path", "gamut-1bmxxg1-StyledText e8i0p5k0")

    return render_template('index_3.html', udemy_1=udemy_1, udemy_2=udemy_2, coursera=coursera, codecademy=codecademy)


if __name__ == '__main__':
    app.run(debug=True)
