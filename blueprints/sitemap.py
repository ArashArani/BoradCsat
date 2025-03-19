from flask import Blueprint , Response

from models.course import Course

from models.blog import Blog

from models.experience import Experience


app = Blueprint("sitemap",__name__)

@app.route('/sitemap.xml')
def sitemap():
    # لیست مسیرها
    pages = [
        {'loc': '/', 'changefreq': 'daily', 'priority': 1.0},
        {'loc': '/courses', 'changefreq': 'weekly', 'priority': 0.8},
        {'loc': '/consults', 'changefreq': 'monthly', 'priority': 0.5},
        {'loc': '/blogs', 'changefreq': 'weekly', 'priority': 0.8},
        {'loc': '/experiences', 'changefreq': 'weekly', 'priority': 0.8},
    ]

    # اضافه کردن مسیرهای دوره‌ها
    courses = Course.query.all()
    for course in courses:
        pages.append({'loc': f'/courses/{course.name}', 'changefreq': 'weekly', 'priority': 0.6})

    # اضافه کردن مسیرهای وبلاگ‌ها
    blogs = Blog.query.all()
    for blog in blogs:
        pages.append({'loc': f'/blogs/{blog.name}', 'changefreq': 'weekly', 'priority': 0.6})

    # اضافه کردن مسیرهای تجربیات
    experiences = Experience.query.all()
    for exp in experiences:
        pages.append({'loc': f'/experiences/{exp.name}', 'changefreq': 'weekly', 'priority': 0.6})

    # تولید XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap-image/1.1">'
    for page in pages:
        xml += '<url>'
        xml += f'<loc>{page["loc"]}</loc>'
        xml += f'<changefreq>{page["changefreq"]}</changefreq>'
        xml += f'<priority>{page["priority"]}</priority>'
        xml += '</url>'
    xml += '</urlset>'

    return Response(xml, mimetype='application/xml')